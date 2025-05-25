#  file: main.py
'''
This is the main entry point of the FastAPI backend for the Medical Voice Dictation Processor. 
It initializes the FastAPI app, configures middleware (e.g., CORS), sets up routes (API and static content), 
provides health check and Azure configuration test endpoints, and configures logging.
'''

# Import necessary modules from FastAPI and Python standard libraries
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import logging

# Import internal modules and settings
from app.routers import transcription
from app.config import settings

# Initialize FastAPI app with metadata and tags for documentation
app = FastAPI(
    title="Medical Voice Dictation Processor",
    description="Convert doctor voice dictations into structured medical data",
    version="1.0.0",
    openapi_tags=[{
        "name": "Transcription",
        "description": "Operations with medical voice transcriptions",
        "externalDocs": {
            "description": "Azure Speech Service Docs",
            "url": f"https://{settings.AZURE_SPEECH_REGION}.api.cognitive.microsoft.com/docs",
        },
    }]
)

# Enable CORS (Cross-Origin Resource Sharing) to allow frontend access from local or external origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "null",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Define the path to the directory where static files (HTML, CSS, JS) are stored
static_dir = Path(__file__).parent / "static"

# Include the transcription router that defines endpoints related to audio transcription
app.include_router(transcription.router, prefix="/api")

# Mount the static directory to serve static files under the "/static" path
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Route to serve the frontend index.html at the root path "/"
@app.get("/", include_in_schema=False)
async def serve_index():
    index_path = static_dir / "index.html"
    print(f"Looking for index.html at: {index_path}")  # Debug print to verify file path
    if not index_path.exists():
        # Return 404 error if index.html does not exist
        raise HTTPException(status_code=404, detail="index.html not found")
    # Return the index.html file as the response with appropriate headers
    return FileResponse(
        index_path,
        headers={
            "Cache-Control": "no-cache",
            "Content-Type": "text/html; charset=utf-8"
        }
    )

# Simple health check endpoint to verify backend is running and properly configured
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "azure_configured": bool(settings.AZURE_SPEECH_KEY),    # Check if Azure Speech Key is set
        "upload_dir": settings.UPLOAD_DIR,                      # Show the directory for uploaded files
        "medical_terms_path": settings.MEDICAL_TERMS_PATH       # Show the path to the Excel term mapping
    }

# Endpoint to verify that Azure Speech credentials are correctly loaded and accessible
@app.post("/api/test-azure-config")
async def test_azure_config():
    """Endpoint to verify Azure credentials are working"""
    if not settings.AZURE_SPEECH_KEY:
        # Return 500 if Azure key is missing
        raise HTTPException(status_code=500, detail="Azure Speech Key not configured")
    
    # Return region and key status if available
    return {
        "message": "Azure credentials loaded",
        "region": settings.AZURE_SPEECH_REGION,
        "key_exists": bool(settings.AZURE_SPEECH_KEY)
    }

# Configure logging to log both to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path(settings.UPLOAD_DIR) / "app.log"),  # Save logs to file in uploads/
        logging.StreamHandler()                                      # Also output logs to console
    ]
)
