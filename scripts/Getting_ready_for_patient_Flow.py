import pandas as pd
#import dataset
df=pd.read_excel("D:\\pythoncoding\\Final_year_project\\data\\raw\\Patient flow and Disease trend A case study of Medical Department DHQ hospital Timergara.xlsx",header=0)

#formatting of date and text columns:
date_columns=("Date_of_admission","Date_of_discharge")
text_columns=("Name","Address")
for col in date_columns:
    df[col]=pd.to_datetime(df[col],format="%d-%b-%y",errors="coerce").dt.date

for col in text_columns:
    df[col]=df[col].str.title()

# Sort dataset by date
df = df.sort_values(by="Date_of_admission")

#Checking consistency of admission date:
#Check Missing / Invalid Dates
missing_dates = df["Date_of_admission"].isna().sum()
print("Missing or invalid admission dates:", missing_dates)
missing_discharge = df["Date_of_discharge"].isna().sum()
print("Records with missing discharge date:", missing_discharge)

#Check Future Dates (Logical Error)
future_dates = df[df["Date_of_admission"] > pd.Timestamp.today().date()]
print("Records with future admission dates:", len(future_dates))

#Check Same-Day Admission & Discharge
same_day_cases = df[
    df["Date_of_discharge"] == df["Date_of_admission"]]
print("Same-day admission & discharge cases:", len(same_day_cases))

#Check Discharge Before Admission (Logical Error)
invalid_discharge_records = df.loc[
    df["Date_of_discharge"] < df["Date_of_admission"]
].copy()
print("invalid_discharge_records:",len(invalid_discharge_records))
invalid_discharge_records["Row_Index"] = invalid_discharge_records.index
invalid_discharge_records.to_excel("invalid indices.xlsx",index=False)

#Finding Duplicates:

# Find exact duplicates
exact_duplicates = df[df.duplicated(keep="first")].copy()

print("Total exact duplicate rows:", len(exact_duplicates))
print(exact_duplicates.head())

# Remove exact duplicates
df = df.drop_duplicates()
exact_duplicates.to_excel("Exact_Duplicates.xlsx", index=False)

df.to_excel("Patient flow and Disease trend A case study of Medical Department DHQ hospital Timergara.xlsx",index=False)

