import pandas as pd

# Load the Excel file (make sure the file is in the right location)
df = pd.read_excel('mock_data/medical_terms.xlsx')

# Prepare a dictionary mapping terms to their respective codes, standard names, and confidence values
MEDICAL_TERMS = {}

for index, row in df.iterrows():
    term = row['Term'].lower()  # normalize term to lowercase
    code = row['Code']
    standard_name = row['Standard Name']
    confidence = 0.9 if 'sugar' in term or 'diabetes' in term else 0.95  # Example logic, adjust as needed

    MEDICAL_TERMS[term] = {
        'code': code,
        'standard_name': standard_name,
        'confidence': confidence
    }

# Print the dictionary to see the results
# print(MEDICAL_TERMS)
