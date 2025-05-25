# Medical Voice Transcription Backend

This backend system converts doctor voice dictations into structured medical data using the **Azure Speech-to-Text API**, 
mapping transcriptions to predefined medical terms from a hospital template.



## Features

- Accepts audio uploads (.mp3, .wav) or live microphone input via a web UI.
- Transcribes speech using **Azure Speech-to-Text API** (Free Tier).
- Matches medical terms (e.g., CBC,ECG,MRI) with hospital codes from an Excel-based reference.
- Returns structured **JSON** output ready for Excel export or EMR ingestion.
- Includes a REST API and web UI for recording/uploading audio.



## Directory Structure

```plaintext

Question_1/
├── Readme                   		# Project documentation
├── requirements.txt         		# Python dependencies

├── app/
│   ├── main.py              		# FastAPI app entry point
│   ├── config.py            		# App settings and environment loader
│
│   ├── models/
│   │   └── schemas.py       		# Pydantic models for API requests/responses
│
│   ├── routers/
│   │   └── transcription.py 		# Main API route for audio transcription
│
│   ├── services/
│   │   ├── azure_speech.py  		# Azure Speech-to-Text wrapper
│   │   ├── entity_extractor.py 	# Fallback keyword-based NER
│   │   └── term_mapper.py   		# Maps terms from Azure entities to hospital codes
│
│   ├── static/
│   │   ├── index.html       		# Web UI for recording/uploading audio
│   │   ├── app.js           		# JS to record audio and call backend
│   │   └── styles.css       		# CSS styling

├── audio_files/             		# Raw or test audio files
├── mock_data/
│   └── medical_terms.xlsx   		# Hospital-specific medical term/code mapping
├── Output_Screenshots/      		# Captured screenshots (for documentation/debugging)
├── Testing/                 		# Test instructions or sample inputs/outputs
├── uploads/                 		# Stores application logs
```


## Getting Started

### 1. Clone the Repository

```bash
https://github.com/Adithya098/Elimai_assessment_Q1.git
```

### 2. Set Up Environment

Create a `.env` file in the root folder with your Azure credentials:

```env
AZURE_SPEECH_KEY = your_key
AZURE_REGION  = your_region
```

3. Install Dependencies
bash
pip install -r requirements.txt

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Run the App
```bash
python -m uvicorn app.main:app --reload --port 8000
```
Visit the API at: `http://localhost:8000` or open the Web UI at: `http://localhost:8000/static/index.html`.
