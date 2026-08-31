import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.backends.backend_pdf import PdfPages

# =====================================================
# SETTINGS
# =====================================================

sns.set_style("whitegrid")

plt.rcParams['figure.max_open_warning'] = 0

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
# TIME FEATURES
# =====================================================

df['Month'] = (
    df['Date_of_admission']
    .dt.to_period('M')
    .dt.to_timestamp()
)

df['Month_Num'] = df['Date_of_admission'].dt.month

# =====================================================
# TOP + LEAST DISEASES
# =====================================================

disease_counts = (
    df['Disease']
    .value_counts()
    .reset_index()
)

disease_counts.columns = [
    'Disease',
    'Total_Cases'
]

top10_df = disease_counts.head(10)

least10_df = disease_counts.tail(10)

top10_diseases = top10_df['Disease'].tolist()

# =====================================================
# SAVE DISEASE SUMMARY EXCEL
# =====================================================

with pd.ExcelWriter(
    "Disease_Summary_Report.xlsx"
) as writer:

    disease_counts.to_excel(
        writer,
        sheet_name='All_Diseases',
        index=False
    )

    top10_df.to_excel(
        writer,
        sheet_name='Top_10_Diseases',
        index=False
    )

    least10_df.to_excel(
        writer,
        sheet_name='Least_10_Diseases',
        index=False
    )

# =====================================================
# MONTHLY ANALYSIS
# =====================================================

monthly = df.groupby(
    ['Month', 'Disease'],
    observed=True
).size().reset_index(name='Cases')

pivot = monthly.pivot(
    index='Month',
    columns='Disease',
    values='Cases'
).fillna(0)

# =====================================================
# SAVE COMPLETE MONTHLY ANALYSIS
# =====================================================

monthly.to_excel(
    "All_Disease_Monthly_Analysis.xlsx",
    index=False
)

pivot.to_excel(
    "Disease_Monthly_Pivot_Table.xlsx"
)

# =====================================================
# 1. MONTHLY TREND PDF
# VISUALIZATION ONLY TOP 10
# =====================================================

with PdfPages("Disease_Monthly_Trends_Report.pdf") as pdf:

    for disease in top10_diseases:

        if disease not in pivot.columns:
            continue

        fig, ax = plt.subplots(figsize=(14, 7))

        series = pivot[disease]

        rolling = series.rolling(
            window=3,
            min_periods=1
        ).mean()

        ax.plot(
            series.index,
            series.values,
            marker='o',
            label='Actual'
        )

        ax.plot(
            series.index,
            rolling.values,
            linestyle='--',
            label='Moving Average'
        )

        ax.set_title(
            f"Monthly Trend - {disease}"
        )

        ax.set_xlabel("Month")

        ax.set_ylabel("Cases")

        ax.tick_params(
            axis='x',
            rotation=45
        )

        ax.legend()

        plt.tight_layout()

        pdf.savefig(fig)

        plt.close(fig)

# =====================================================
# 2. SEASONAL ANALYSIS
# ANALYZE ALL DISEASES
# =====================================================

def get_season(month):

    if month in [12, 1, 2]:
        return "Winter"

    elif month in [3, 4, 5]:
        return "Spring"

    elif month in [6, 7, 8]:
        return "Summer"

    return "Autumn"

df['Season'] = df['Month_Num'].apply(
    get_season
)

seasonal = df.groupby(
    ['Season', 'Disease'],
    observed=True
).size().reset_index(name='Cases')

# =====================================================
# SAVE ALL SEASONAL ANALYSIS
# =====================================================

seasonal.to_excel(
    "All_Disease_Seasonality_Analysis.xlsx",
    index=False
)

# =====================================================
# VISUALIZE TOP 10 ONLY
# =====================================================
seasonal_top = seasonal[
    seasonal['Disease'].isin(top10_diseases)
]

with PdfPages("Disease_Seasonality_Report.pdf") as pdf:

    fig, ax = plt.subplots(figsize=(18, 9))

    sns.barplot(
        data=seasonal_top,
        x='Season',
        y='Cases',
        hue='Disease',
        ax=ax
    )

    ax.set_title(
        "Top 10 Disease Seasonality"
    )

    ax.set_xlabel("Season")

    ax.set_ylabel("Cases")

    # Show legend properly
    ax.legend(
        title='Disease',
        bbox_to_anchor=(1.02, 1),
        loc='upper left',
        borderaxespad=0
    )

    # Prevent legend cutoff
    plt.tight_layout(
        rect=(0, 0, 0.82, 1)
    )
    pdf.savefig(
        fig,
        bbox_inches='tight'
    )

    plt.close(fig)

# =====================================================
# 3. SPIKE ANALYSIS
# ANALYZE ALL DISEASES
# =====================================================

spike_results = []

for disease in pivot.columns:

    series = pivot[disease]

    mean_cases = series.mean()

    std_cases = series.std()

    threshold = mean_cases + std_cases

    spikes = series[series > threshold]

    spike_results.append([
        disease,
        round(mean_cases, 2),
        round(std_cases, 2),
        round(threshold, 2),
        len(spikes)
    ])

spike_df = pd.DataFrame(
    spike_results,
    columns=[
        'Disease',
        'Average_Cases',
        'Std_Deviation',
        'Spike_Threshold',
        'Spike_Months'
    ]
)

# =====================================================
# SAVE ALL SPIKE ANALYSIS
# =====================================================

spike_df.to_excel(
    "All_Disease_Spike_Analysis.xlsx",
    index=False
)

# =====================================================
# VISUALIZE TOP 10 ONLY
# =====================================================

spike_top = spike_df[
    spike_df['Disease'].isin(top10_diseases)
]

with PdfPages("Disease_Spike_Report.pdf") as pdf:

    fig, ax = plt.subplots(figsize=(16, 8))

    sns.barplot(
        data=spike_top,
        x='Disease',
        y='Spike_Months',
        ax=ax
    )

    ax.set_title(
        "Disease Spike Analysis"
    )

    ax.tick_params(
        axis='x',
        rotation=45
    )

    plt.tight_layout()

    pdf.savefig(fig)

    plt.close(fig)

# =====================================================
# 4. CORRELATION ANALYSIS
# ANALYZE ALL DISEASES
# =====================================================

pivot_clean = pivot.loc[
    :,
    pivot.nunique() > 1
]

if pivot_clean.shape[1] > 1:

    corr = pivot_clean.corr()

    corr.to_excel(
        "Disease_Correlation_Report.xlsx"
    )

    # =============================================
    # VISUALIZE TOP 10 ONLY
    # =============================================

    corr_top = corr.loc[
        top10_diseases,
        top10_diseases
    ]

    with PdfPages("Disease_Correlation_Report.pdf") as pdf:

        fig, ax = plt.subplots(figsize=(14, 10))

        sns.heatmap(
            corr_top,
            cmap='coolwarm',
            annot=True,
            fmt='.2f',
            linewidths=0.5,
            ax=ax
        )

        ax.set_title(
            "Top 10 Disease Correlation"
        )

        plt.tight_layout()

        pdf.savefig(fig)

        plt.close(fig)

else:

    print(
        "Not enough diseases for correlation analysis."
    )

# =====================================================
# 5. AGE GROUP ANALYSIS
# ANALYZE ALL DISEASES
# =====================================================

age_df = df[['AGE', 'Disease']].copy()

age_df['AGE'] = pd.to_numeric(
    age_df['AGE'],
    errors='coerce'
)

age_df = age_df.dropna()

age_df = age_df[
    (age_df['AGE'] > 0)
    &
    (age_df['AGE'] < 110)
]

bins = [0, 13, 20, 36, 51, 66, 160]

labels = [
    'Child',
    'Teen',
    'Young Adult',
    'Adult',
    'Senior',
    'Old'
]

age_df['Age_Group'] = pd.cut(
    age_df['AGE'],
    bins=bins,
    labels=labels,
    right=False
)

# =====================================================
# AGE GROUP DISEASE COUNTS
# =====================================================

age_group_disease = age_df.groupby(
    ['Age_Group', 'Disease'],
    observed=True
).size().reset_index(name='Cases')

# =====================================================
# MOST AFFECTED AGE GROUP
# =====================================================

most_affected_age = (
    age_df['Age_Group']
    .value_counts()
    .reset_index()
)

most_affected_age.columns = [
    'Age_Group',
    'Total_Patients'
]

# =====================================================
# YOUNG VS OLD
# ANALYZE ALL DISEASES
# =====================================================

young_old = age_df[
    age_df['Age_Group'].isin(
        ['Young Adult', 'Old']
    )
]

young_old_analysis = young_old.groupby(
    ['Age_Group', 'Disease'],
    observed=True
).size().reset_index(name='Cases')

# =====================================================
# SAVE ALL AGE ANALYSIS
# =====================================================

with pd.ExcelWriter(
    "Age_Group_Disease_Analysis_Report.xlsx"
) as writer:

    age_group_disease.to_excel(
        writer,
        sheet_name='All_Age_Group_Disease',
        index=False
    )

    young_old_analysis.to_excel(
        writer,
        sheet_name='Young_vs_Old_All',
        index=False
    )

    most_affected_age.to_excel(
        writer,
        sheet_name='Most_Affected_Age',
        index=False
    )

# =====================================================
# VISUALIZATION ONLY TOP 10
# =====================================================

with PdfPages(
    "Age_Group_Disease_Visual_Reports.pdf"
) as pdf:

    # =============================================
    # TOP 10 DISEASES IN EACH AGE GROUP
    # =============================================

    for group in labels:

        subset = age_group_disease[
            age_group_disease['Age_Group'] == group
        ]

        subset = subset.sort_values(
            by='Cases',
            ascending=False
        ).head(10)

        if subset.empty:
            continue

        fig, ax = plt.subplots(figsize=(14, 7))

        sns.barplot(
            data=subset,
            x='Cases',
            y='Disease',
            ax=ax
        )

        ax.set_title(
            f"Top 10 Diseases - {group}"
        )

        plt.tight_layout()

        pdf.savefig(fig)

        plt.close(fig)

    # =============================================
    # YOUNG VS OLD TOP 10
    # =============================================

    young_old_top = (
        young_old_analysis
        .sort_values(
            by='Cases',
            ascending=False
        )
        .groupby(
            'Age_Group',
            observed=True
        )
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(16, 8))

    sns.barplot(
        data=young_old_top,
        x='Disease',
        y='Cases',
        hue='Age_Group',
        ax=ax
    )

    ax.set_title(
        "Young Adult vs Old Disease Comparison"
    )

    ax.tick_params(
        axis='x',
        rotation=45
    )

    plt.tight_layout()

    pdf.savefig(fig)

    plt.close(fig)

    # =============================================
    # MOST AFFECTED AGE GROUP
    # =============================================

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.barplot(
        data=most_affected_age,
        x='Age_Group',
        y='Total_Patients',
        ax=ax
    )

    ax.set_title(
        "Most Affected Age Group"
    )

    plt.tight_layout()

    pdf.savefig(fig)

    plt.close(fig)

# =====================================================
# FINAL MESSAGE
# =====================================================

print(
    "ALL REPORTS GENERATED SUCCESSFULLY"
)