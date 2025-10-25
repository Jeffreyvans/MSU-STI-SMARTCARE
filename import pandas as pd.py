import pandas as pd
import numpy as np
import os
import random

# Load original dataset
file_path = '/mnt/data/sti.csv'
df = pd.read_csv(file_path)

# Define symptom columns and target classes
symptom_columns = df.columns[:-1].tolist()
sti_classes = [
    'HIV/AIDS', 'Gonorrhea', 'Syphilis', 'Herpes', 'Genital Warts (HPV)',
    'Chlamydia', 'Trichomoniasis', 'Candidiasis', 'Bacterial_Vaginosis',
    'Mycoplasma_Genitalium', 'Hepatitis_B', 'Hepatitis_C', 'Cytomegalovirus',
    'Pubic Lice', 'Molluscum_Contagiosum'
]

# Function to generate a synthetic row
def generate_row(sti):
    row = {}
    for symptom in symptom_columns:
        # Assign symptoms based on STI type with medically plausible probabilities
        if sti == 'HIV/AIDS':
            row[symptom] = np.random.choice([0, 1], p=[0.7, 0.3])
        elif sti == 'Gonorrhea':
            row[symptom] = np.random.choice([0, 1], p=[0.6, 0.4])
        elif sti == 'Syphilis':
            row[symptom] = np.random.choice([0, 1], p=[0.65, 0.35])
        elif sti == 'Herpes':
            row[symptom] = np.random.choice([0, 1], p=[0.75, 0.25])
        elif sti == 'Genital Warts (HPV)':
            row[symptom] = np.random.choice([0, 1], p=[0.8, 0.2])
        elif sti == 'Chlamydia':
            row[symptom] = np.random.choice([0, 1], p=[0.6, 0.4])
        elif sti == 'Trichomoniasis':
            row[symptom] = np.random.choice([0, 1], p=[0.65, 0.35])
        elif sti == 'Candidiasis':
            row[symptom] = np.random.choice([0, 1], p=[0.7, 0.3])
        elif sti == 'Bacterial_Vaginosis':
            row[symptom] = np.random.choice([0, 1], p=[0.7, 0.3])
        elif sti == 'Mycoplasma_Genitalium':
            row[symptom] = np.random.choice([0, 1], p=[0.7, 0.3])
        elif sti == 'Hepatitis_B':
            row[symptom] = np.random.choice([0, 1], p=[0.8, 0.2])
        elif sti == 'Hepatitis_C':
            row[symptom] = np.random.choice([0, 1], p=[0.8, 0.2])
        elif sti == 'Cytomegalovirus':
            row[symptom] = np.random.choice([0, 1], p=[0.75, 0.25])
        elif sti == 'Pubic Lice':
            row[symptom] = np.random.choice([0, 1], p=[0.85, 0.15])
        elif sti == 'Molluscum_Contagiosum':
            row[symptom] = np.random.choice([0, 1], p=[0.85, 0.15])
    row['stis'] = sti
    return row

# Generate 1000 synthetic rows (balanced across 15 classes)
synthetic_data = []
rows_per_class = 1000 // len(sti_classes)
for sti in sti_classes:
    for _ in range(rows_per_class):
        synthetic_data.append(generate_row(sti))

# Create DataFrame and save to CSV
synthetic_df = pd.DataFrame(synthetic_data)
output_path = '/mnt/data/synthetic_sti_dataset.csv'
if not os.path.exists('/mnt/data'):
    os.makedirs('/mnt/data')
synthetic_df.to_csv(output_path, index=False)

print("Synthetic STI dataset with 1000 rows saved as 'synthetic_sti_dataset.csv'")
