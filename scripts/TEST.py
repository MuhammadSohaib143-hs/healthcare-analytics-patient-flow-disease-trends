import pandas as pd

# Load cleaned dataset
df = pd.read_excel(
    r"D:\pythoncoding\Final_year_project\clean_disease_trends_dataset.xlsx"
)

# Convert Disease column to uppercase string
df['Disease'] = (
    df['Disease']
    .astype(str)
    .str.upper()
    .str.strip()
)

# -----------------------------------------
# Find diseases containing possible full forms
# -----------------------------------------

# Pattern:
# Abbreviation followed by long text
pattern = r"\b[A-Z]{2,10}\b[\s\-:]+[A-Z ]{5,}"

# Filter rows
fullform_rows = df[
    df['Disease'].str.contains(pattern, regex=True, na=False)
]

# Keep only unique disease names
fullform_rows = fullform_rows[['Disease']].drop_duplicates()

# Print results
print("\nDiseases containing possible full forms:\n")
print(fullform_rows.to_string(index=False))

# Save results
fullform_rows.to_excel(
    "diseases_with_fullforms.xlsx",
    index=False
)

print("\nFile saved as diseases_with_fullforms.xlsx")