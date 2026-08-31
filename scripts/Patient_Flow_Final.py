import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

sns.set_style("whitegrid")

# =====================================================
# Load Data
# =====================================================
data = pd.read_excel(
    "D:\\pythoncoding\\Final_year_project\\Patient flow and Disease trend A case study of Medical Department DHQ hospital Timergara.xlsx"
)
data['Date_of_admission'] = pd.to_datetime(data['Date_of_admission'])
data['Date_of_discharge'] = pd.to_datetime(data['Date_of_discharge'])

# =====================================================
# Core Aggregation (Single Source)
# =====================================================
daily = data.groupby('Date_of_admission').size().reset_index(name='Patient_Count')
weekly = data.resample('W-MON', on='Date_of_admission').size().reset_index(name='Patient_Count')
monthly = data.resample('ME', on='Date_of_admission').size().reset_index(name='Patient_Count')

def add_avg_change_flags(flow_df, period_name):
    # Cumulative average
    flow_df[f'Average_Flow_{period_name}'] = (
        flow_df['Patient_Count'].expanding().mean().round(2)
    )

    # Absolute and percentage change
    flow_df[f'{period_name}_Change'] = flow_df['Patient_Count'].diff()
    flow_df[f'{period_name}_Change_Pct'] = (
        flow_df['Patient_Count'].pct_change() * 100
    ).round(2)

    # Max / Min flags (CALCULATED ONCE, NOT DOUBLY)
    max_val = flow_df['Patient_Count'].max()
    min_val = flow_df['Patient_Count'].min()

    flow_df['Max_Flag'] = flow_df['Patient_Count'] == max_val
    flow_df['Min_Flag'] = flow_df['Patient_Count'] == min_val

add_avg_change_flags(daily, 'Daily')
add_avg_change_flags(weekly, 'Weekly')
add_avg_change_flags(monthly, 'Monthly')

# =====================================================
# Q1 – Average Patient Flow
# =====================================================
with PdfPages("Patient_Flow_Plots.pdf") as pdf:
    for df_obj, title, avg_col in [
        (daily, 'Daily Patient Flow', 'Average_Flow_Daily'),
        (weekly, 'Weekly Patient Flow', 'Average_Flow_Weekly'),
        (monthly, 'Monthly Patient Flow', 'Average_Flow_Monthly')
    ]:
        plt.figure(figsize=(12,5))
        plt.plot(df_obj["Date_of_admission"], df_obj['Patient_Count'], marker='o', label='Count')
        plt.plot(df_obj["Date_of_admission"], df_obj[avg_col], linestyle='--', marker='x', label='Cumulative Avg')
        plt.title(title)
        plt.xlabel('Date')
        plt.ylabel('Number of Patients')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        pdf.savefig()
        plt.close()

with pd.ExcelWriter("Patient_Flow_Averages.xlsx") as writer:
    daily.to_excel(excel_writer=writer, sheet_name='Daily_Flow', index=False)
    weekly.to_excel(excel_writer=writer, sheet_name='Weekly_Flow', index=False)
    monthly.to_excel(excel_writer=writer, sheet_name='Monthly_Flow', index=False)

# =====================================================
# Q2 – Max / Min Crowded Periods
# =====================================================
with PdfPages("Patient_Flow_Max_Min.pdf") as pdf:
    for df_obj, label in [(daily,'Daily'),(weekly,'Weekly'),(monthly,'Monthly')]:
        plt.figure(figsize=(12,5))
        plt.plot(df_obj["Date_of_admission"], df_obj['Patient_Count'], marker='o', label=f'{label} Count')
        plt.scatter(df_obj.loc[df_obj['Max_Flag'], df_obj.columns[0]],
                    df_obj.loc[df_obj['Max_Flag'], 'Patient_Count'], color='red', s=100, label='Max')
        plt.scatter(df_obj.loc[df_obj['Min_Flag'], df_obj.columns[0]],
                    df_obj.loc[df_obj['Min_Flag'], 'Patient_Count'], color='blue', s=100, label='Min')
        plt.title(f'{label} Patient Flow (Max / Min)')
        plt.xlabel('Date')
        plt.ylabel('Patients')
        plt.legend()
        plt.tight_layout()
        pdf.savefig()
        plt.close()

with pd.ExcelWriter("Patient_Flow_Max_Min.xlsx") as writer:
    daily.to_excel(excel_writer=writer, sheet_name='Daily_Flow', index=False)
    weekly.to_excel(excel_writer=writer, sheet_name='Weekly_Flow', index=False)
    monthly.to_excel(excel_writer=writer, sheet_name='Monthly_Flow', index=False)

# =====================================================
# Q3 – Change Analysis
# =====================================================
with PdfPages("Patient_Flow_Changes.pdf") as pdf:
    for df_obj, col, title in [
        (daily,'Daily_Change_Pct','Daily Change (%)'),
        (weekly,'Weekly_Change_Pct','Weekly Change (%)'),
        (monthly,'Monthly_Change_Pct','Monthly Change (%)')
    ]:
        plt.figure(figsize=(10,5))
        plt.plot(df_obj["Date_of_admission"], df_obj[col])
        plt.title(title)
        plt.xlabel('Date')
        plt.ylabel('Percentage Change')
        plt.grid(True)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

with pd.ExcelWriter("Patient_Flow_Changes.xlsx") as writer:
    daily.to_excel(excel_writer=writer, sheet_name='Daily_Flow', index=False)
    weekly.to_excel(excel_writer=writer, sheet_name='Weekly_Flow', index=False)
    monthly.to_excel(excel_writer=writer, sheet_name='Monthly_Flow', index=False)

# =====================================================
# 6. Q4 – Trend Analysis
# =====================================================
trend_df = data.groupby(data['Date_of_admission'].dt.to_period('M')).size().reset_index(name='Patient_Count')
trend_df['Time_Index'] = np.arange(len(trend_df))
slope = np.polyfit(trend_df['Time_Index'], trend_df['Patient_Count'], 1)[0]

trend_result = pd.DataFrame({
    'Metric': ['Trend Slope','Overall Patient Flow Trend'],
    'Value':  [round(float(slope), 3),'Increasing' if slope>0 else 'Decreasing' if slope<0 else 'Stable']
})

with pd.ExcelWriter("Patient_Flow_Trend_Analysis.xlsx") as writer:
    trend_df.to_excel(excel_writer=writer, sheet_name='Monthly_Patient_Flow', index=False)
    trend_result.to_excel(excel_writer=writer, sheet_name='Trend_Conclusion', index=False)

# =====================================================
#  Q5 – Spikes & Drops
# =====================================================
spike_df = daily.copy()
mean_val = spike_df['Patient_Count'].mean()
std_val = spike_df['Patient_Count'].std()
spike_df['Z_Score'] = (spike_df['Patient_Count'] - mean_val) / std_val
spike_df['Spike_or_Drop'] = np.where(
    spike_df['Z_Score']>=2,'Spike',
    np.where(spike_df['Z_Score']<=-2,'Drop','Normal')
)

anomaly_df = spike_df[spike_df['Spike_or_Drop']!='Normal']

plt.figure(figsize=(12,6))
plt.plot(spike_df['Date_of_admission'], spike_df['Patient_Count'])
plt.scatter(anomaly_df['Date_of_admission'], anomaly_df['Patient_Count'])
plt.title('Sudden Spikes and Drops')
plt.tight_layout()
plt.savefig("Patient_Flow_Spikes_Drops.pdf")
plt.close()

with pd.ExcelWriter("Patient_Flow_Spikes_Drops.xlsx") as writer:
    spike_df.to_excel(excel_writer=writer, sheet_name='Daily_Patient_Flow', index=False)
    anomaly_df.to_excel(excel_writer=writer, sheet_name='Detected_Spikes_Drops', index=False)

# =====================================================
# Q6 – Seasonality
# =====================================================
data['Season'] = data['Date_of_admission'].dt.month.map(
    lambda m: 'Winter' if m in [12,1,2]
    else 'Spring' if m in [3,4,5]
    else 'Summer' if m in [6,7,8]
    else 'Autumn'
)

seasonal = data.groupby('Season').size().reset_index(name='Patient_Count')
seasonal['Percentage'] = (seasonal['Patient_Count']/seasonal['Patient_Count'].sum()*100).round(2)

plt.figure(figsize=(8,5))
plt.bar(seasonal['Season'], seasonal['Patient_Count'])
plt.title('Seasonal Patient Flow')
plt.tight_layout()
plt.savefig("Seasonal_Patient_Flow.pdf")
plt.close()

with pd.ExcelWriter("Patient_Flow_Seasonality_One_Year.xlsx") as writer:
    seasonal.to_excel(excel_writer=writer, sheet_name='Seasonal_Patient_Flow', index=False)

# =====================================================
# Q7 – Even Distribution
# =====================================================
mean_p = daily['Patient_Count'].mean()
std_p = daily['Patient_Count'].std()
cv_p = std_p / mean_p

stats = pd.DataFrame([{
    'Mean_Patients_Per_Day': round(mean_p,2),
    'Standard_Deviation': round(std_p,2),
    'Coefficient_of_Variation': round(cv_p,3)
}])

plt.figure(figsize=(10,5))
plt.plot(daily['Date_of_admission'], daily['Patient_Count'])
plt.title('Daily Patient Flow Over Time')
plt.tight_layout()
plt.savefig("patient_flow_even_distribution.pdf")
plt.close()

with pd.ExcelWriter("patient_flow_even_distribution.xlsx") as writer:
    daily.to_excel(excel_writer=writer, sheet_name='Daily_Patient_Flow', index=False)
    stats.to_excel(excel_writer=writer, sheet_name='Distribution_Statistics', index=False)

print("All Excel and PDF files generated successfully.")
