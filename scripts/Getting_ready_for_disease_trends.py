import pandas as pd

# -------------------------------
# Step 1: Load dataset
# -------------------------------
df = pd.read_excel("D:\\pythoncoding\\Final_year_project\\data\\processed\\Patient flow and Disease trend A case study of DHQ hospital Timergara.xlsx")

df['Date_of_admission'] = pd.to_datetime(df['Date_of_admission'], format="%d-%b-%y", errors="coerce").dt.date

# -------------------------------
# Step 2: Keep relevant columns including Address
# -------------------------------
required_cols = ['Name', 'Age', 'Gender', 'Address', 'Date_of_admission', 'Diagnosis']
df = df[[col for col in required_cols if col in df.columns]]

# -------------------------------
# Step 3: Clean Name and Address and assign robust Patient_ID
# -------------------------------
df['Name_Clean'] = df['Name'].astype(str).str.upper().str.strip()
df['Address_Clean'] = df['Address'].astype(str).str.upper().str.strip()

# Create a unique key combining Name + Address + Date_of_admission
df['Patient_Key'] = df['Name_Clean'] + "_" + df['Address_Clean'] + "_" + df['Date_of_admission'].astype(str)

# Assign unique Patient_IDs
df['Patient_ID'] = pd.factorize(df['Patient_Key'])[0] + 1

# -------------------------------
# Step 4: Remove non-string or invalid Diagnosis rows
# -------------------------------
df = df[df['Diagnosis'].notna()]                          # remove NaN
df = df[df['Diagnosis'].apply(lambda x: isinstance(x, str))]  # keep only strings
df = df[df['Diagnosis'].str.strip() != ""]               # remove empty strings

# -------------------------------
# Step 5: Remove full forms inside parentheses
# -------------------------------
df['Diagnosis'] = df['Diagnosis'].str.upper()
df['Diagnosis'] = df['Diagnosis'].str.replace(r"\s*\(.*?\)", "", regex=True)
df['Diagnosis'] = df['Diagnosis'].str.strip()

# -------------------------------
# Step 6: Split multiple diseases
# -------------------------------
df['Disease_List'] = df['Diagnosis'].str.split('+')

# -------------------------------
# Step 7: Explode into single disease rows
# -------------------------------
df = df.explode('Disease_List')

# -------------------------------
# Step 8: Remove empty or invalid disease entries after explode
# -------------------------------
df = df[df['Disease_List'].notna()]
df = df[df['Disease_List'].apply(lambda x: isinstance(x, str))]
df['Disease_List'] = df['Disease_List'].str.strip()
df = df[df['Disease_List'] != ""]

# -------------------------------
# Step 9: Final dataset including Address
# -------------------------------
final_df = df[['Patient_ID', 'Date_of_admission', 'Disease_List', 'Age', 'Gender', 'Address']].copy()
final_df.rename(columns={'Disease_List':'Disease'}, inplace=True)

# -------------------------------
# Step 10: Save cleaned dataset
# -------------------------------
final_df.to_excel("clean_disease_trends_dataset.xlsx", index=False)

print("Dataset cleaned and saved successfully.")