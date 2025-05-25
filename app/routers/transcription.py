# file: transcription.py
'''
This module defines the FastAPI routes for handling medical audio file transcription. 
It supports uploading audio files (MP3, WAV, WEBM), handles format conversion, and integrates with Azure Speech-to-Text. 
It also extracts structured medical entities either via Azure or fallback keyword extraction.
'''

import os
import tempfile
import ffmpeg
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Form
from fastapi.responses import JSONResponse
from typing import Optional, List
import logging

from app.services.azure_speech import transcribe_audio_file
from app.services.term_mapper import map_terms_from_azure
from app.models.schemas import TranscriptionResponse, MappedTerm, MedicalEntity
from app.services.entity_extractor import extract_medical_entities

# Initialize FastAPI router for transcription-related endpoints
router = APIRouter(
    prefix="/transcribe",
    tags=["transcription"],
)

logger = logging.getLogger(__name__)

# File size and type validation constants
MAX_FILE_SIZE_MB = 10
SUPPORTED_MIME_TYPES = {
    "audio/mpeg",
    "audio/mp3", 
    "audio/wav",
    "audio/x-wav",
    "audio/wave",
    "audio/webm",  
    "audio/webm;codecs=opus"  
}

def convert_webm_to_wav(webm_file_path: str) -> str:
    """Convert a webm file to wav using ffmpeg"""
    try:
        output_path = f"{webm_file_path}.wav"
        ffmpeg.input(webm_file_path).output(output_path).run()
        return output_path
    except Exception as e:
        logger.error(f"Error converting webm to wav: {e}")
        raise HTTPException(status_code=400, detail="Error converting webm to wav")

def convert_entities_to_mapped(entities: List[MedicalEntity]) -> List[MappedTerm]:
    """
    Convert keyword-extracted MedicalEntity objects to MappedTerm objects.
    Adds fallback code and standard name if not provided.
    """
    return [
        MappedTerm(
            text=e.text,
            type=e.type,
            code=e.code if e.code else f"UNK-{e.type[:3].upper()}",
            standard_name=e.standard_name if e.standard_name else e.text.title(),
            confidence=e.confidence
        ) for e in entities
    ]

@router.post("/file", response_model=TranscriptionResponse)
async def transcribe_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    language: Optional[str] = Form("en-US"),
    include_entities: Optional[bool] = Form(False)
    ):
    """
    Endpoint to transcribe an uploaded audio file and optionally extract structured medical data.
    Validates file type/size, converts formats if needed, calls Azure transcription, 
    and extracts medical terms from result.
    """
    # Validate file type
    if file.content_type not in SUPPORTED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Only MP3, WAV, and WEBM files are supported")

    try:
        # Save the uploaded file to a temporary location on disk
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[-1]) as tmp:
            content = await file.read()              # Read file content from the upload
            tmp.write(content)                       # Write content to temporary file
            tmp.flush()                              # Ensure all content is written
            os.fsync(tmp.fileno())                   # Force write to disk (especially useful on some systems)
            file_path = tmp.name                     # Store temp file path for further use

        # Ensure temp file is cleaned up after the request finishes
        background_tasks.add_task(os.unlink, file_path)

        logger.info(f"Transcribing file: {file.filename}, saved to: {file_path}")

        # Check if file exceeds max size
        if os.path.getsize(file_path) > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File size exceeds 10MB limit")

        # Convert WebM files to WAV if necessary
        if file.content_type == "audio/webm" or file.content_type == "audio/webm;codecs=opus":
            file_path = convert_webm_to_wav(file_path)
            logger.info(f"Converted webm file to wav: {file_path}")

        # Transcribe audio using Azure Speech-to-Text
        transcription_result = await transcribe_audio_file(file_path, language)
        transcription = transcription_result.get("transcription", "")
        azure_entities = transcription_result.get("entities", [])

        # Map Azure entities to standard format, or fallback to keyword-based extraction
        if azure_entities:
            structured_data = map_terms_from_azure(azure_entities)
        else:
            # Fallback: extract medical entities using in-house NLP extractor
            fallback_entities = extract_medical_entities(transcription)
            structured_data = convert_entities_to_mapped(fallback_entities)
            logger.info(f"Fallback extracted entities: {[e.text for e in fallback_entities]}")

        # Compose response with transcription and structured entities
        response = TranscriptionResponse(
            transcription=transcription,
            structured_data=structured_data  # Already a list of MappedTerm
        )

        if include_entities:
            extended_response = response.model_dump()
            extended_response["azure_entities"] = azure_entities
            extended_response["source"] = "azure" if azure_entities else "keyword_extractor"
            return JSONResponse(content=extended_response)

        # ✅ Ensure frontend receives proper JSON
        return JSONResponse(content=response.model_dump())

    # Handle missing temp file error
    except FileNotFoundError as e:
        logger.error(f"Temporary file error: {e}")
        raise HTTPException(status_code=404, detail="Temporary file not found")

    # Handle general errors in transcription pipeline
    except Exception as e:
        logger.error("Transcription failed", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Transcription failed due to an internal error"
        )
