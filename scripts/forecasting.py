import pandas as pd
import numpy as np
import os
import re

from prophet import Prophet

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)
import matplotlib.pyplot as plt

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_excel(
    r"D:\pythoncoding\Final_year_project\data\processed\clean_disease_trends_dataset.xlsx"
)
# =====================================================
# CLEAN DATA
# =====================================================

df['Date_of_admission'] = pd.to_datetime(
    df['Date_of_admission'],
    errors='coerce'
)

df = df.dropna(
    subset=['Date_of_admission', 'Disease']
).copy()

df['Disease'] = (
    df['Disease']
    .astype(str)
    .str.upper()
    .str.replace(r"\s*\(.*?\)", "", regex=True)
    .str.strip()
)

# =====================================================
# MONTH COLUMN
# =====================================================

df['Month'] = (
    df['Date_of_admission']
    .dt.to_period('M')
    .dt.to_timestamp()
)

# =====================================================
# MONTHLY AGGREGATION
# =====================================================

monthly = (
    df.groupby(['Month', 'Disease'])
    .size()
    .reset_index(name='y')
)

# =====================================================
# FOLDERS
# =====================================================
'''
base_folder = "PROPHET_SYSTEM"

data_folder = os.path.join(base_folder, "datasets")
forecast_folder = os.path.join(base_folder, "forecasts")
plot_folder = os.path.join(base_folder, "plots")

os.makedirs(base_folder, exist_ok=True)
os.makedirs(data_folder, exist_ok=True)
os.makedirs(forecast_folder, exist_ok=True)
os.makedirs(plot_folder, exist_ok=True)
'''
# =====================================================
# MASTER DATASET
# =====================================================

master = monthly.copy()
master.columns = ['ds', 'Disease', 'y']

master.to_excel(
    os.path.join(base_folder, "MASTER_DATASET.xlsx"),
    index=False
)

# =====================================================
# SETTINGS
# =====================================================

MIN_TOTAL_CASES = 20
TEST_MONTHS = 3

evaluation_results = []

# =====================================================
# DISEASE LOOP
# =====================================================

diseases = monthly['Disease'].unique()

for disease in diseases:

    print(f"\nProcessing: {disease}")

    temp = monthly[
        monthly['Disease'] == disease
    ][['Month', 'y']]

    temp = temp.sort_values('Month')

    # ===============================================
    # COMPLETE MONTH SEQUENCE
    # ===============================================

    temp = temp.set_index('Month')
    temp = temp.asfreq('MS').fillna(0)
    temp = temp.reset_index()

    temp.columns = ['ds', 'y']

    # ===============================================
    # FILTER LOW-FREQUENCY DISEASES
    # ===============================================

    total_cases = temp['y'].sum()

    if total_cases < MIN_TOTAL_CASES:

        print(
            f"Skipping {disease} "
            f"(only {total_cases} cases)"
        )

        continue

    # ===============================================
    # NEED ENOUGH MONTHS
    # ===============================================

    if len(temp) < (TEST_MONTHS + 6):

        print(
            f"Skipping {disease} "
            f"(insufficient months)"
        )

        continue

    # ===============================================
    # SAFE FILE NAME
    # ===============================================

    safe_name = re.sub(
        r'[^A-Z0-9_]',
        '_',
        disease
    )

    # ===============================================
    # SAVE DATASET
    # ===============================================

    temp.to_excel(
        os.path.join(
            data_folder,
            f"{safe_name}_DATA.xlsx"
        ),
        index=False
    )

    # ===============================================
    # TRAIN / TEST SPLIT
    # ===============================================

    train = temp.iloc[:-TEST_MONTHS]
    test = temp.iloc[-TEST_MONTHS:]

    # ===============================================
    # EVALUATION MODEL
    # ===============================================

    model_eval = Prophet(
        yearly_seasonality=False,
        weekly_seasonality=False,
        daily_seasonality=False
    )

    model_eval.fit(train)

    future_test = model_eval.make_future_dataframe(
        periods=TEST_MONTHS,
        freq='MS'
    )

    forecast_test = model_eval.predict(
        future_test
    )

    pred = (
        forecast_test[['ds', 'yhat']]
        .tail(TEST_MONTHS)
        .reset_index(drop=True)
    )

    actual = (
        test[['ds', 'y']]
        .reset_index(drop=True)
    )

    # ===============================================
    # METRICS
    # ===============================================

    mae = mean_absolute_error(
        actual['y'],
        pred['yhat']
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual['y'],
            pred['yhat']
        )
    )

    actual_non_zero = actual['y'].replace(
        0,
        np.nan
    )

    mape = np.nanmean(
        np.abs(
            (
                actual_non_zero -
                pred['yhat']
            ) /
            actual_non_zero
        )
    ) * 100

    evaluation_results.append({

        "Disease": disease,
        "Total_Cases": int(total_cases),
        "Train_Months": len(train),
        "Test_Months": len(test),

        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "MAPE(%)": round(mape, 2)

    })

    print(
        f"MAE={mae:.2f}, "
        f"RMSE={rmse:.2f}, "
        f"MAPE={mape:.2f}%"
    )

    # ===============================================
    # FINAL MODEL USING ALL DATA
    # ===============================================

    final_model = Prophet(
        yearly_seasonality=False,
        weekly_seasonality=False,
        daily_seasonality=False
    )

    final_model.fit(temp)

    future = final_model.make_future_dataframe(
        periods=12,
        freq='MS'
    )

    forecast = final_model.predict(
        future
    )

    forecast.to_excel(
        os.path.join(
            forecast_folder,
            f"{safe_name}_FORECAST.xlsx"
        ),
        index=False
    )

    # ===============================================
    # FORECAST PLOT
    # ===============================================

    fig = final_model.plot(forecast)

    plt.title(
        f"{disease} Forecast "
        f"(Next 12 Months)"
    )

    plt.savefig(
        os.path.join(
            plot_folder,
            f"{safe_name}_FORECAST.png"
        ),
        bbox_inches='tight'
    )

    plt.close()

# =====================================================
# SAVE EVALUATION RESULTS
# =====================================================

evaluation_df = pd.DataFrame(
    evaluation_results
)

evaluation_df = evaluation_df.sort_values(
    by='RMSE'
)

evaluation_df.to_excel(
    os.path.join(
        base_folder,
        "EVALUATION_RESULTS.xlsx"
    ),
    index=False
)

# =====================================================
# DONE
# =====================================================

print("\nPROPHET PIPELINE COMPLETED SUCCESSFULLY")
print(
    "Evaluation Results Saved:"
)
print(
    os.path.join(
        base_folder,
        "EVALUATION_RESULTS.xlsx"
    )
)