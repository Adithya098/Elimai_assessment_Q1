# file: entity_extractor.py

'''
Provides functionality to load medical terminology from an Excel file and
extract relevant medical entities from input text by exact keyword matching.
Returns structured entity data including codes, standard names, confidence,
and position of the matched term within the text.
'''

import pandas as pd
import re
from typing import List
from app.models.schemas import MedicalEntity

# Load the Excel file into a pandas DataFrame and organize terms into categories
def load_medical_terms(file_path: str) -> dict:
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        raise ValueError(f"Error loading the Excel file: {e}")

    # Dictionary to hold terms by category, each maps term text to metadata
    medical_terms = {
        "procedure": {},
        "diagnosis": {},
        "lab_test": {}
    }

    # Populate dictionary from Excel rows: each term has code, standard name, confidence
    for _, row in df.iterrows():
        term_type = row['Type']     # e.g., procedure, diagnosis, lab_test
        term = row['Term'].lower()  # Normalize to lowercase for matching
        code = row['Code']
        standard_name = row['Standard Name']
        confidence = 0.95  # Fixed confidence for all loaded terms

        if term_type in medical_terms:
            medical_terms[term_type][term] = {
                'code': code,
                'standard_name': standard_name,
                'confidence': confidence
            }

    return medical_terms

# Global variable holding medical terms loaded from Excel once at module import
MEDICAL_TERMS = load_medical_terms('mock_data/medical_terms.xlsx')

# Extract medical entities from text by matching loaded terms via regex word boundaries
def extract_medical_entities(text: str) -> List[MedicalEntity]:
    if not text:
        return []

    text_lower = text.lower()
    found_entities = []

    # Check each term category and match terms against the text
    for term_type, terms in MEDICAL_TERMS.items():
        for term, data in terms.items():
            # Regex pattern to match whole words exactly (case-insensitive)
            pattern = r'\b' + re.escape(term) + r'\b'
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                # Create a MedicalEntity with matched info including matched span offsets
                found_entities.append(
                    MedicalEntity(
                        text=term,
                        type=term_type,
                        code=data['code'],
                        standard_name=data['standard_name'],
                        confidence=data['confidence'],
                        span={
                            "matched_text": match.group(0),
                            "start": match.start(),
                            "end": match.end()
                        }
                    )
                )

    return found_entities
