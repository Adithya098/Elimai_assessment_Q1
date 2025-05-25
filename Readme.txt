# Question 1 : Medical Voice Transcription Backend

This backend system converts doctor voice dictations into structured medical data using 'Azure Speech-to-Text API' 
and maps results to predefined medical terms from a hospital template. It is designed to support electronic medical record (EMR) integration.

---

# Features

- Accepts audio uploads (`.mp3`, `.wav`) or live speech input.
- Uses Azure Speech-to-Text API (Free Tier) to transcribe audio.
- Matches transcribed medical terms (e.g., "CBC") with internal codes from an Excel-based mock hospital database.
- Returns structured JSON output ready for Excel export.
- Includes a REST API and an web UI to upload or record audio.

---

# Project Structure

Question_1/
├── .env                     		# Environment variables (Azure keys, configs)
├── .gitignore               		# Git ignore rules
├── Readme                   		# Project documentation
├── requirements.txt         		# Python dependencies
├── app/
│   ├── main.py              		# FastAPI app entry point
│   ├── config.py            		# App settings and environment loader
│   ├── models/
│   │   └── schemas.py       		# Pydantic models for API requests/responses
│   ├── routers/
│   │   └── transcription.py 		# Main API route for audio transcription
│   ├── services/
│   │   ├── azure_speech.py  		# Azure Speech-to-Text wrapper
│   │   ├── entity_extractor.py 	# Fallback keyword-based NER
│   │   └── term_mapper.py   		# Maps terms from Azure entities to hospital codes
│   ├── static/
│   │   ├── index.html       		# Web UI for recording/uploading audio
│   │   ├── app.js           		# JS to record audio and call backend
│   │   └── styles.css       		# CSS styling
│   └── test.py              		# Test script or basic test harness
│
├── audio_files/             		# Raw or test audio files
├── mock_data/
│   └── medical_terms.xlsx   		# Hospital-specific medical term/code mapping
├── Output_Screenshots/      		# Captured screenshots (for documentation/debugging)
├── Testing/                 		# Test instructions or sample inputs/outputs
├── uploads/                 		# Stores application logs



Go to the main folder : Question 1 and run this command -
	python -m uvicorn app.main:app --reload --port 8000


