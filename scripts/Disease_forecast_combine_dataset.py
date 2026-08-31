import glob
import os
import pandas as pd
from zipfile import BadZipFile

# =====================================================
# SET WORKING DIRECTORY
# =====================================================

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# =====================================================
# LOAD MASTER DATASET
# =====================================================

master_path = r"D:\pythoncoding\Final_year_project\PROPHET_SYSTEM\MASTER_DATASET.xlsx"

df_actuals = pd.read_excel(master_path)
df_actuals = df_actuals.rename(columns={"ds": "Date", "y": "Cases"})
df_actuals["Type"] = "Actual"

# =====================================================
# READ ALL FORECAST FILES
# =====================================================

forecast_folder = r"D:\pythoncoding\Final_year_project\PROPHET_SYSTEM\forecasts"

forecast_files = glob.glob(os.path.join(forecast_folder, "*.xlsx"))

print(f"Forecast files found: {len(forecast_files)}")

forecast_list = []

for file_path in forecast_files:

    file_name = os.path.basename(file_path)

    # Ignore temporary Excel files
    if file_name.startswith("~$"):
        continue

    print(f"Reading: {file_name}")

    try:
        df_fc = pd.read_excel(file_path)

    except BadZipFile:
        print(f"Skipped (corrupt/not real Excel): {file_name}")
        continue

    except Exception as e:
        print(f"Skipped {file_name}: {e}")
        continue

    if not {"ds", "yhat"}.issubset(df_fc.columns):
        print(f"Skipped {file_name}: Missing ds/yhat columns")
        continue

    disease_name = (
        file_name
        .replace("_FORECAST.xlsx", "")
        .replace(".xlsx", "")
    )

    df_fc = df_fc[["ds", "yhat"]].copy()

    df_fc.rename(
        columns={
            "ds": "Date",
            "yhat": "Cases"
        },
        inplace=True
    )

    df_fc["Disease"] = disease_name
    df_fc["Type"] = "Forecast"

    forecast_list.append(df_fc)

# =====================================================
# COMBINE
# =====================================================

if len(forecast_list) == 0:
    raise ValueError("No valid forecast files were found.")

df_forecasts = pd.concat(forecast_list, ignore_index=True)

df_combined = pd.concat(
    [
        df_actuals[["Date", "Disease", "Cases", "Type"]],
        df_forecasts[["Date", "Disease", "Cases", "Type"]]
    ],
    ignore_index=True
)

df_combined["Cases"] = df_combined["Cases"].round()

output_path = r"D:\pythoncoding\Final_year_project\PROPHET_SYSTEM\COMBINED_DISEASE_DATASET.xlsx"

df_combined.to_excel(output_path, index=False)

print("\nDONE")
print(output_path)
print(f"Total rows: {len(df_combined)}")