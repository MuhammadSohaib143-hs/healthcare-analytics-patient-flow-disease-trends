import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

sns.set_style("whitegrid")

# =====================================================
# Load Dataset
# =====================================================

data = pd.read_excel(
    "D:\\pythoncoding\\Final_year_project\\Patient flow and Disease trend A case study of Medical Department DHQ hospital Timergara.xlsx"
)
data['Date_of_admission'] = pd.to_datetime(data['Date_of_admission'])
data['Date_of_discharge'] = pd.to_datetime(data['Date_of_discharge'])
# =====================================================
# Clean Columns (IMPORTANT FIX)
# =====================================================

data['Type_of_Discharge'] = (
    data['Type_of_Discharge']
    .astype(str)
    .str.strip()
)

# =====================================================
# Date Conversion (KEEP DATETIME SAFE)
# =====================================================

data['Date_of_admission'] = pd.to_datetime(data['Date_of_admission'])
data['Date_of_discharge'] = pd.to_datetime(data['Date_of_discharge'])

# =====================================================
# LOS Calculation
# =====================================================

data['LOS'] = (
    data['Date_of_discharge'] - data['Date_of_admission']
).dt.days

data = data[data['LOS'] >= 0]



# =====================================================
# Q1 - MOST COMMON DISCHARGE TYPE
# =====================================================

discharge_counts = data['Type_of_Discharge'].value_counts().reset_index()
discharge_counts.columns = ['Type_of_Discharge', 'Count']

discharge_counts['Percentage'] = (
    discharge_counts['Count'] / discharge_counts['Count'].sum() * 100
).round(2)

plt.figure(figsize=(10,5))
plt.bar(discharge_counts['Type_of_Discharge'].astype(str),
        discharge_counts['Count'])

plt.title("Most Common Discharge Types")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("discharge_types.pdf")
plt.close()

discharge_counts.to_excel("discharge_types.xlsx", index=False)

# =====================================================
# Q2 - DAILY / WEEKLY / MONTHLY DISCHARGE
# =====================================================

def discharge_group(freq):
    return (
        data.groupby([
            pd.Grouper(key='Date_of_discharge', freq=freq),
            'Type_of_Discharge'
        ])
        .size()
        .reset_index(name='Count')
    )

daily = discharge_group('D')
weekly = discharge_group('W')
monthly = discharge_group('ME')

# Convert for plotting
weekly['Date_of_discharge'] = weekly['Date_of_discharge'].dt.date
monthly['Date_of_discharge'] = monthly['Date_of_discharge'].dt.date

with PdfPages("discharge_trend.pdf") as pdf:
    for df, title in [(daily,"Daily"), (weekly,"Weekly"), (monthly,"Monthly")]:

        plt.figure(figsize=(12,5))

        for t in df['Type_of_Discharge'].unique():
            temp = df[df['Type_of_Discharge'] == t]

            plt.plot(temp.iloc[:,0], temp['Count'], label=t)

        plt.title(f"{title} Discharge Trend")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        pdf.savefig()
        plt.close()

# Save
daily.to_excel("daily_discharge.xlsx", index=False)
weekly.to_excel("weekly_discharge.xlsx", index=False)
monthly.to_excel("monthly_discharge.xlsx", index=False)

# =====================================================
# Q3 - LOS BY DISCHARGE TYPE
# =====================================================

los_discharge = data.groupby('Type_of_Discharge')['LOS'].agg([
    'mean','max','min','count'
]).reset_index()

los_discharge.columns = [
    'Type_of_Discharge','Avg_LOS','Max_LOS','Min_LOS','Patients'
]

los_discharge['Avg_LOS'] = los_discharge['Avg_LOS'].round(2)

plt.figure(figsize=(10,5))
plt.bar(los_discharge['Type_of_Discharge'].astype(str),
        los_discharge['Avg_LOS'])

plt.title("LOS by Discharge Type")
plt.xticks(rotation=45)
plt.ylabel("Avg_LOS in Days")
plt.tight_layout()
plt.savefig("los_discharge.pdf")
plt.close()

los_discharge.to_excel("los_discharge.xlsx", index=False)

# =====================================================
# Q4 - SEASONAL DISCHARGE
# =====================================================

data['Season'] = data['Date_of_discharge'].dt.month.map(lambda m:
    'Winter' if m in [12,1,2]
    else 'Spring' if m in [3,4,5]
    else 'Summer' if m in [6,7,8]
    else 'Autumn'
)

seasonal = data.groupby(['Season','Type_of_Discharge']).size().reset_index(name='Count')

plt.figure(figsize=(10,5))

for t in seasonal['Type_of_Discharge'].unique():
    temp = seasonal[seasonal['Type_of_Discharge'] == t]
    plt.plot(temp['Season'], temp['Count'], marker='o', label=t)

plt.title("Seasonal Discharge Pattern")
plt.legend()
plt.tight_layout()
plt.savefig("seasonal_discharge.pdf")
plt.close()

seasonal.to_excel("seasonal_discharge.xlsx", index=False)

# =====================================================
# Q5 - SUCCESS RATE
# =====================================================

successful = ["DOR"]

success_count = data[data['Type_of_Discharge'].isin(successful)].shape[0]

success_rate = round((success_count / len(data)) * 100, 2)

success_df = pd.DataFrame([{
    "Total": len(data),
    "Successful": success_count,
    "Success_Rate": success_rate
}])

plt.figure(figsize=(5,5))
plt.bar(["Success Rate"], [success_rate])
plt.ylim(0,100)
plt.title("Successful Discharge %")
plt.savefig("success_rate.pdf")
plt.close()

success_df.to_excel("success_rate.xlsx", index=False)

print("CLEAN ANALYSIS COMPLETED SUCCESSFULLY")