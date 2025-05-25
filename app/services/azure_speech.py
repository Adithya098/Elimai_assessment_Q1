#  file: azure_speech.py
'''
This file contains functions to transcribe audio using Azure Cognitive Services Speech-to-Text API.
It provides both file-based transcription and live audio byte stream transcription capabilities.
'''

import asyncio
import azure.cognitiveservices.speech as speechsdk
from app.config import settings
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def transcribe_audio_file(file_path: str, language: str = "en-US") -> dict:
    """
    Transcribes an audio file from disk using Azure Speech-to-Text service.
    Supports common audio formats and returns the recognized transcription text along with any extracted entities.
    """
    # Only support certain audio file extensions
    if not file_path.lower().endswith((".wav", ".mp3", ".mp4")):
        raise HTTPException(status_code=400, detail="Unsupported audio format")

    # Setup Azure Speech configuration with subscription key and region
    speech_config = speechsdk.SpeechConfig(
        subscription=settings.AZURE_SPEECH_KEY,
        region=settings.AZURE_SPEECH_REGION
    )
    speech_config.speech_recognition_language = language

    # Configure audio input from the given file path
    try:
        audio_config = speechsdk.audio.AudioConfig(filename=file_path)
    except Exception as e:
        logger.error(f"Invalid audio file: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid audio file: {e}")

    # Initialize the speech recognizer with config and audio source
    try:
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config
        )
    except Exception as e:
        logger.error(f"Failed to initialize recognizer: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to initialize recognizer: {str(e)}")

    # Perform synchronous recognition
    try:
        result = recognizer.recognize_once()  # Blocking call

        # Handle recognized speech
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            transcription_text = result.text.strip()
            return {
                "transcription": transcription_text,
                "entities": []  # No extra entity extraction implemented here
            }

        # Handle no speech matched
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return {"transcription": "", "entities": []}

        # Handle cancellation with error details
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            if cancellation.error_details:
                logger.error(f"Azure Error: {cancellation.error_details}")
            raise HTTPException(status_code=500, detail="Azure Speech Recognition was canceled.")

        else:
            raise HTTPException(status_code=500, detail="Unexpected error in Azure transcription.")
    except Exception as e:
        logger.error(f"Error during transcription: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


async def transcribe_live_audio_bytes(audio_bytes: bytes, language: str = "en-US") -> dict:
    """
    Transcribes live audio streamed as raw bytes using Azure Speech-to-Text service.
    Processes the audio stream in real-time and returns the combined transcription text.
    """
    try:
        # Configure Azure Speech with credentials and language
        speech_config = speechsdk.SpeechConfig(
            subscription=settings.AZURE_SPEECH_KEY,
            region=settings.AZURE_SPEECH_REGION
        )
        speech_config.speech_recognition_language = language

        # Setup a push stream to feed audio data continuously
        stream = speechsdk.audio.PushAudioInputStream()
        audio_config = speechsdk.audio.AudioConfig(stream=stream)
        recognizer = speechsdk.SpeechRecognizer(speech_config, audio_config)

        recognized_text_chunks = []

        # Define event handler to collect recognized chunks
        def recognized_handler(evt):
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                recognized_text_chunks.append(evt.result.text)

        # Attach the handler to recognized event
        recognizer.recognized.connect(recognized_handler)

        # Start continuous speech recognition
        recognizer.start_continuous_recognition()

        # Feed audio bytes to the stream, then close to signal end of input
        stream.write(audio_bytes)
        stream.close()

        # Wait some time for recognition to process the input audio
        await asyncio.sleep(5)

        # Stop the continuous recognition session
        recognizer.stop_continuous_recognition()

        # Combine all recognized text pieces
        full_text = " ".join(recognized_text_chunks).strip()
        return {
            "transcription": full_text,
            "entities": []  # No entity extraction performed here
        }

    except Exception as e:
        logger.error(f"Live transcription failed: {e}")
        raise HTTPException(status_code=500, detail=f"Live transcription failed: {e}")
