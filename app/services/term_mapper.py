# file : term_mapper.py

'''
Loads medical terms from an Excel file and maps Azure-recognized medical entities to
internal standardized terms with codes and confidence scores. Uses exact and fuzzy 
matching to align Azure entities with known medical terms.
'''

import pandas as pd
from typing import List, Dict, Any
from difflib import get_close_matches
from app.models.schemas import MappedTerm, AzureEntity
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Mapping from Azure entity categories to internal standardized types
AZURE_CATEGORY_MAP = {
    "Medication": "medication",
    "MedicalCondition": "diagnosis",
    "Symptom": "symptom",
    "Test": "lab_test",
    "TreatmentName": "procedure",
    "BodyPart": "anatomy",
    "Vital": "vital_sign",
}

# Load medical terms from Excel into nested dictionary by category and term
def load_medical_terms():
    try:
        df = pd.read_excel('mock_data/medical_terms.xlsx')  # Load Excel file
        terms = {}

        # Organize terms by their type, normalize keys to lowercase
        for _, row in df.iterrows():
            type_ = row['Type'].lower()  # Ensure case consistency
            term = row['Term'].lower()
            if type_ not in terms:
                terms[type_] = {}
            terms[type_][term] = {
                "code": row['Code'],
                "standard_name": row['StandardName']
            }
        return terms
    except Exception as e:
        logger.warning(f"Failed to load medical terms from Excel: {e}")
        return {}  # Return empty dict on failure

# Normalize text by trimming and lowercasing
def normalize(text: str) -> str:
    """Normalize text to lower case and remove leading/trailing spaces."""
    return text.lower().strip()

# Map Azure entities to internal MappedTerm objects using exact and fuzzy matching
def map_terms_from_azure(entities: List[Dict[str, Any]]) -> List[MappedTerm]:
    medical_terms = load_medical_terms()
    mapped_terms = []

    for entity_dict in entities:
        try:
            entity = AzureEntity(**entity_dict)  # Validate and parse entity dict
        except Exception as e:
            logger.warning(f"Invalid Azure entity skipped: {e}")
            continue

        entity_type = AZURE_CATEGORY_MAP.get(entity.category, "other")
        entity_text = normalize(entity.text)

        if entity_type in medical_terms:
            type_terms = medical_terms[entity_type]

            # Try exact match first
            if entity_text in type_terms:
                term_info = type_terms[entity_text]
                confidence = entity.confidence_score * 0.9
            else:
                # Try fuzzy matching as fallback
                logger.info(f"No exact match found for '{entity_text}' in category '{entity_type}', trying fuzzy matching.")
                close_matches = get_close_matches(entity_text, type_terms.keys(), n=3, cutoff=0.8)
                if close_matches:
                    matched_term = close_matches[0]
                    term_info = type_terms[matched_term]
                    confidence = entity.confidence_score * 0.75  # Reduced confidence for fuzzy match
                    logger.info(f"Fuzzy matched '{entity_text}' to '{matched_term}' with confidence {confidence}")
                else:
                    # No match found - fallback with default unknown code
                    logger.info(f"No close match found for '{entity_text}' in category '{entity_type}'. Using fallback.")
                    matched_term = entity.text
                    confidence = entity.confidence_score * 0.6
                    term_info = {"code": f"UNK-{entity_type[:3].upper()}", "standard_name": entity.text.title()}
        else:
            # Unknown category handling
            logger.info(f"Unknown category '{entity.category}' not mapped.")
            term_info = {"code": "UNK-OTH", "standard_name": entity.text.title()}
            entity_type = "other"
            confidence = entity.confidence_score * 0.5  # Lowest confidence for unknown categories

        # Append mapped term to results
        mapped_terms.append(MappedTerm(
            text=entity.text,
            type=entity_type,
            code=term_info["code"],
            standard_name=term_info["standard_name"],
            confidence=confidence
        ))

    return mapped_terms
