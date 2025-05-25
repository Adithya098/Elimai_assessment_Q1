#  file: config.py
'''
This configuration module defines application settings for the FastAPI backend. 
It loads environment variables (e.g., Azure credentials, file paths) using `pydantic-settings` 
and ensures necessary directories like the upload path are created at runtime.
'''

from pydantic_settings import BaseSettings
from pathlib import Path
import os

# Define a class for environment-based settings using Pydantic's BaseSettings
class Settings(BaseSettings):
    AZURE_SPEECH_KEY: str                # Required: Azure Speech API key
    AZURE_SPEECH_REGION: str = "eastus"  # Optional: defaults to 'eastus' if not set

    UPLOAD_DIR: str = "uploads"                                 # Directory where logs and uploaded files are stored
    MEDICAL_TERMS_PATH: str = "mock_data/medical_terms.xlsx"    # Path to Excel file containing medical code mappings

    class Config:
        # Specify the location of the .env file (two levels up from this file)
        env_file = Path(__file__).resolve().parent.parent / ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure the upload directory exists at runtime (created if not found)
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        print(f"Upload directory created at: {self.UPLOAD_DIR}")

# Create a singleton instance of the settings to be used across the app
settings = Settings()
