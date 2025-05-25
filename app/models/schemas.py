# file: schemas.py
'''
This module defines Pydantic data models used for API request and response validation. 
These schemas represent recognized entities from Azure Speech, mapped medical terms, and final structured output. 
They ensure consistent and validated data structures across the backend.
'''

from pydantic import BaseModel, Field
from typing import List, Optional

class AzureEntity(BaseModel):
    """Entity as recognized by Azure Speech-to-Text API"""
    category: str  # The category of the entity (e.g., "Healthcare", "Medical Term")
    text: str      # Raw text of the recognized entity
    offset: int    # Position of the entity in the full transcription
    length: int    # Character length of the entity
    confidence_score: Optional[float] = 0.0  # Confidence score from Azure, optional

    class Config:
        # Ensure all strings are stripped of leading/trailing spaces
        min_anystr_length = 1
        anystr_strip_whitespace = True

class MappedTerm(BaseModel):
    """Medical term mapped to an internal hospital code"""
    text: str  # Term text as transcribed or matched
    type: str  # Type/category of the term (e.g., procedure, diagnosis)
    code: Optional[str] = None  # Internal hospital code if matched
    standard_name: Optional[str] = None  # Canonical or standardized name
    confidence: float = 0.0  # Confidence score in recognition/mapping

    class Config:
        # Clean up any string inputs automatically
        anystr_strip_whitespace = True

class TranscriptionResponse(BaseModel):
    """Response returned by the transcription API"""
    transcription: str  # Full transcription from the audio
    structured_data: List[MappedTerm]  # List of structured medical terms extracted

class MedicalEntity(BaseModel):
    """Represents a structured medical entity extracted from transcription"""
    text: str  # Raw entity text
    type: str  # Entity category (e.g., "diagnosis", "medication")
    code: Optional[str] = None  # Internal or standard code if found
    standard_name: Optional[str] = None  # Human-readable canonical name
    confidence: float  # Confidence score in extraction or mapping
