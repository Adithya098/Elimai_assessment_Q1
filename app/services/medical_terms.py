# Dictionary of standardized medical terms organized by type (lab_test, procedure, diagnosis, etc.)
# Each entry maps a specific term (or its lowercase variation) to:
#   - a unique code (used for standardization or integration with other systems)
#   - a standard_name (clean, human-readable version of the term)

MEDICAL_TERMS = {
    "lab_test": {
        "complete blood count": {"code": "LAB023", "standard_name": "Complete Blood Count"},
        "cbc": {"code": "LAB023", "standard_name": "Complete Blood Count"},
        "blood panel": {"code": "LAB024", "standard_name": "Comprehensive Metabolic Panel"},
        "metabolic panel": {"code": "LAB024", "standard_name": "Comprehensive Metabolic Panel"},
        "thyroid panel": {"code": "LAB025", "standard_name": "Thyroid Function Panel"},
        "hemoglobin a1c": {"code": "LAB026", "standard_name": "Hemoglobin A1C"},
        "a1c": {"code": "LAB026", "standard_name": "Hemoglobin A1C"},
    },
    "procedure": {
        "x-ray": {"code": "RAD001", "standard_name": "X-Ray"},
        "chest x-ray": {"code": "RAD002", "standard_name": "Chest X-Ray"},
        "mri": {"code": "RAD003", "standard_name": "Magnetic Resonance Imaging"},
        "ct scan": {"code": "RAD004", "standard_name": "Computed Tomography Scan"},
        "ultrasound": {"code": "RAD005", "standard_name": "Ultrasound"},
        "echocardiogram": {"code": "RAD006", "standard_name": "Echocardiogram"},
        "ekg": {"code": "CAR001", "standard_name": "Electrocardiogram"},
        "electrocardiogram": {"code": "CAR001", "standard_name": "Electrocardiogram"},
    },
    "diagnosis": {
        "hypertension": {"code": "DX001", "standard_name": "Essential Hypertension"},
        "high blood pressure": {"code": "DX001", "standard_name": "Essential Hypertension"},
        "diabetes": {"code": "DX002", "standard_name": "Diabetes Mellitus Type 2"},
        "type 2 diabetes": {"code": "DX002", "standard_name": "Diabetes Mellitus Type 2"},
        "asthma": {"code": "DX003", "standard_name": "Asthma"},
        "pneumonia": {"code": "DX004", "standard_name": "Pneumonia"},
        "bronchitis": {"code": "DX005", "standard_name": "Acute Bronchitis"},
    },
    "medication": {
        "lisinopril": {"code": "MED001", "standard_name": "Lisinopril"},
        "metformin": {"code": "MED002", "standard_name": "Metformin"},
        "atorvastatin": {"code": "MED003", "standard_name": "Atorvastatin"},
        "albuterol": {"code": "MED004", "standard_name": "Albuterol"},
        "insulin": {"code": "MED005", "standard_name": "Insulin"},
        "prednisone": {"code": "MED006", "standard_name": "Prednisone"},
    },
    "vital_sign": {
        "blood pressure": {"code": "VS001", "standard_name": "Blood Pressure"},
        "heart rate": {"code": "VS002", "standard_name": "Heart Rate"},
        "pulse": {"code": "VS002", "standard_name": "Heart Rate"},
        "temperature": {"code": "VS003", "standard_name": "Body Temperature"},
        "respiratory rate": {"code": "VS004", "standard_name": "Respiratory Rate"},
        "oxygen saturation": {"code": "VS005", "standard_name": "Oxygen Saturation"},
        "o2 sat": {"code": "VS005", "standard_name": "Oxygen Saturation"},
    },
    "symptom": {
        "pain": {"code": "SYM001", "standard_name": "Pain"},
        "chest pain": {"code": "SYM002", "standard_name": "Chest Pain"},
        "shortness of breath": {"code": "SYM003", "standard_name": "Dyspnea"},
        "sob": {"code": "SYM003", "standard_name": "Dyspnea"},
        "nausea": {"code": "SYM004", "standard_name": "Nausea"},
        "vomiting": {"code": "SYM005", "standard_name": "Vomiting"},
        "dizziness": {"code": "SYM006", "standard_name": "Dizziness"},
        "fever": {"code": "SYM007", "standard_name": "Fever"},
        "fatigue": {"code": "SYM008", "standard_name": "Fatigue"},
    }
}

# ------------------------------------------------------------------

# Dictionary mapping term *variations* (synonyms or alternative phrasings)
# to a single standardized base term, which will be used internally
# for classification and further mapping (e.g., to codes or types).
VARIATION_MAP = {
    # Procedures
    "mri": "MRI",
    "sugar": "blood sugar",
    "mri scan": "MRI",
    "magnetic resonance imaging": "MRI",
    "x-ray": "X-ray",
    "x ray": "X-ray",
    "xray": "X-ray",
    "ct scan": "CT scan",
    "ct": "CT scan",
    "computed tomography": "CT scan",
    "ultrasound": "ultrasound",
    "sonogram": "ultrasound",
    "colonoscopy": "colonoscopy",
    "endoscopy": "endoscopy",
    "upper endoscopy": "endoscopy",

    # Diagnoses
    "pneumonia": "pneumonia",
    "diabetes": "diabetes",
    "type 1 diabetes": "diabetes",
    "type 2 diabetes": "diabetes",
    "hypertension": "hypertension",
    "high blood pressure": "hypertension",
    "htn": "hypertension",
    "asthma": "asthma",
    "bronchitis": "bronchitis",
    "acute bronchitis": "bronchitis",
    "copd": "COPD",
    "chronic obstructive pulmonary disease": "COPD",

    # Lab Tests
    "cbc": "CBC",
    "complete blood count": "CBC",
    "blood count": "CBC",
    "blood glucose": "blood glucose",
    "glucose test": "blood glucose",
    "glucose": "blood glucose",
    "lipid panel": "lipid panel",
    "cholesterol test": "lipid panel",
    "lipids": "lipid panel",
    "urinalysis": "urinalysis",
    "urine test": "urinalysis",
    "ua": "urinalysis",
    "hba1c": "HbA1c",
    "a1c": "HbA1c",
    "glycated hemoglobin": "HbA1c"
}
