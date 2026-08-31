import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_excel(
    r"D:\pythoncoding\Final_year_project\clean_disease_trends_dataset.xlsx"
)

# =====================================================
# CLEAN DATA
# =====================================================

df['Date_of_admission'] = pd.to_datetime(df['Date_of_admission'], errors='coerce')
df = df.dropna(subset=['Date_of_admission', 'Disease']).copy()

df['Disease'] = (
    df['Disease']
    .astype(str)
    .str.upper()
    .str.replace(r"\s*\(.*?\)", "", regex=True)
    .str.strip()
)

df['Month'] = df['Date_of_admission'].dt.to_period('M').dt.to_timestamp()

# =====================================================
# MONTHLY AGGREGATION
# =====================================================

monthly = df.groupby(['Month', 'Disease']).size().reset_index(name='y')

# =====================================================
# SAFE MAPE FUNCTION (FIX)
# =====================================================

def safe_mape(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    # avoid division by zero
    mask = y_true != 0

    if np.sum(mask) == 0:
        return np.nan  # no valid points

    return np.mean(
        np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])
    ) * 100

# =====================================================
# EVALUATION LOOP
# =====================================================

results = []

diseases = monthly['Disease'].unique()

for disease in diseases:

    data = monthly[monthly['Disease'] == disease][['Month', 'y']]
    data = data.sort_values('Month')

    data = data.set_index('Month').asfreq('MS').fillna(0).reset_index()
    data.columns = ['ds', 'y']

    # =================================================
    # SKIP VERY SMALL DATASETS
    # =================================================

    if len(data) < 5 or data['y'].sum() < 5:
        continue

    # =================================================
    # TRAIN TEST SPLIT
    # =================================================

    split = int(len(data) * 0.8)

    train = data[:split]
    test = data[split:]

    if len(test) == 0:
        continue

    # =================================================
    # MODEL
    # =================================================

    model = Prophet(
        yearly_seasonality=False,
        weekly_seasonality=False,
        daily_seasonality=False
    )

    model.fit(train)

    # =================================================
    # PREDICTION
    # =================================================

    future = model.make_future_dataframe(periods=len(test), freq='MS')
    forecast = model.predict(future)

    pred = forecast[['ds', 'yhat']].iloc[-len(test):]

    # =================================================
    # METRICS (FIXED)
    # =================================================

    mae = mean_absolute_error(test['y'], pred['yhat'])
    rmse = np.sqrt(mean_squared_error(test['y'], pred['yhat']))

    mape = safe_mape(test['y'], pred['yhat'])

    results.append([
        disease,
        round(mae, 2),
        round(rmse, 2),
        None if np.isnan(mape) else round(mape, 2),
        len(data)
    ])

# =====================================================
# RESULTS TABLE
# =====================================================

eval_df = pd.DataFrame(
    results,
    columns=['Disease', 'MAE', 'RMSE', 'MAPE(%)', 'Data_Points']
)

# =====================================================
# SORTING (ONLY RELIABLE METRICS)
# =====================================================

best_models = eval_df.sort_values('MAE').head(10)
worst_models = eval_df.sort_values('MAE', ascending=False).head(10)

# =====================================================
# SAVE OUTPUT
# =====================================================

output_folder = "PROPHET_EVALUATION_FIXED"

with pd.ExcelWriter(f"{output_folder}.xlsx") as writer:

    eval_df.to_excel(writer, sheet_name="All_Diseases", index=False)
    best_models.to_excel(writer, sheet_name="Best_Models", index=False)
    worst_models.to_excel(writer, sheet_name="Worst_Models", index=False)

# =====================================================
# FINAL OUTPUT
# =====================================================

print("EVALUATION COMPLETED ")
print("\nTOP BEST MODELS:")
print(best_models.head())

print("\nTOP WORST MODELS:")
print(worst_models.head())