# Patient Flow and Disease Trends Analytics

## Healthcare Analytics for Patient Flow and Disease Trends Forecasting

An end-to-end healthcare analytics and time-series forecasting project developed as a case study of the **Medical Department, DHQ Hospital Timergara, Lower Dir, Khyber Pakhtunkhwa, Pakistan**.

The project transforms paper-based hospital admission records into structured data and applies **Python-based data preprocessing, exploratory data analysis, disease trend analysis, Prophet time-series forecasting, model evaluation, and Power BI visualization**.

The primary objective is to analyze historical patient flow and disease patterns and provide a data-driven decision-support dashboard for monitoring patient admissions and forecasting future disease trends.

---

## 📌 Project Overview

Public-sector hospitals often maintain patient information through handwritten registers. Although these records contain valuable information, manual record-keeping makes it difficult to efficiently analyze patient flow, disease trends, and historical patterns.

This project digitizes and analyzes patient admission records from the Medical Department of DHQ Hospital Timergara covering **July 2024 to July 2025**.

The analysis focuses on:

* Patient admission patterns
* Daily, weekly, and monthly patient flow
* Seasonal variations
* Age and gender distributions
* Disease frequency and trends
* Patient discharge outcomes
* Future disease forecasting
* Forecast model evaluation
* Interactive Power BI visualization

---

# 🎯 Project Objectives

The project was developed to achieve the following objectives:

1. Digitize and prepare hospital patient records for analysis.
2. Clean and preprocess the collected clinical data.
3. Analyze patient admission patterns at daily, weekly, and monthly levels.
4. Identify seasonal variations in patient flow.
5. Analyze disease distribution across different age groups and genders.
6. Identify frequently occurring diseases in the medical department.
7. Forecast future disease trends using **Facebook Prophet**.
8. Evaluate forecasting performance using **MAE, RMSE, and MAPE**.
9. Develop an interactive Power BI dashboard for hospital-level decision support.

---

# 🔄 Project Workflow

```text
┌──────────────────────────────┐
│   Handwritten Hospital       │
│   Patient Registers          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   Data Digitization          │
│   Excel / Structured Data    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   Data Cleaning &            │
│   Preprocessing              │
│   Python + Pandas            │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   Exploratory Data Analysis  │
│   Patient Flow & Diseases    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   Disease Trend Analysis     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   Prophet Forecasting        │
│   Model Training & Testing   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   Model Evaluation           │
│   MAE | RMSE | MAPE          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   Power BI Dashboard         │
│   Analysis & Forecasting     │
└──────────────────────────────┘
```

---

# 🛠️ Tech Stack & Tools

| Technology           | Purpose                                                |
| -------------------- | ------------------------------------------------------ |
| **Python**           | Data preprocessing, analysis, and forecasting workflow |
| **Pandas**           | Data cleaning and manipulation                         |
| **Jupyter Notebook** | Analysis and experimentation                           |
| **Prophet**          | Time-series forecasting                                |
| **Scikit-learn**     | Model evaluation metrics                               |
| **Microsoft Excel**  | Data digitization and initial data preparation         |
| **Power BI Desktop** | Interactive dashboard and visualization                |
| **Git & GitHub**     | Version control and project documentation              |

---

# 📊 Dataset

The dataset was prepared from handwritten patient admission registers maintained by the **Medical Department of DHQ Hospital Timergara**.

### Study Period

**July 2024 – July 2025**

### Original Dataset

**10,361 patient records**

### Main Variables

The dataset contains information including:

* Patient Name
* Age
* Gender
* Address
* Date of Admission
* Date of Discharge
* Diagnosis
* Diagnosis Unspecified
* Type of Discharge

The project focuses specifically on the **Medical Department** and does not attempt to model hospital-wide staffing, bed capacity, doctor availability, or other resources that were not present in the collected dataset.

---

# 🧹 Data Cleaning & Preprocessing

The raw hospital records required substantial preprocessing before analysis.

The preprocessing workflow included:

* Converting handwritten register information into structured data.
* Checking data types and data consistency.
* Standardizing disease names.
* Handling unspecified diagnoses.
* Checking missing values.
* Validating admission and discharge dates.
* Identifying invalid records where discharge occurred before admission.
* Creating age groups.
* Preparing disease-specific datasets for forecasting.
* Generating cleaned datasets for analysis and Power BI.

A total of **101 records** were identified where the discharge date occurred before the admission date.

Records with unspecified diagnoses were retained and explicitly identified rather than being silently removed.

---

# 📈 Exploratory Data Analysis

The exploratory analysis examined patient flow and disease patterns at multiple temporal levels.

### Patient Flow

The analysis investigated:

* Daily admissions
* Weekly admissions
* Monthly admissions
* Seasonal admission patterns
* Minimum and maximum admission volumes

The average daily patient flow was approximately **26 patients per day**, with daily admissions ranging from **1 to 77 patients**.

The highest weekly admission volume was **254 patients**, recorded during the second week of June 2025.

The highest monthly admission volume was **1,000 patients in October 2024**, while July 2024 recorded the lowest monthly volume at **654 patients**.

---

# 🌦️ Seasonal Analysis

Patient admissions were grouped into four seasons.

| Season | Admissions | Percentage |
| ------ | ---------: | ---------: |
| Summer |      3,126 |     30.17% |
| Autumn |      2,508 |     24.21% |
| Spring |      2,419 |     23.35% |
| Winter |      2,307 |     22.27% |

Summer recorded the highest number of admissions during the study period.

---

# 👥 Demographic Analysis

Age-group analysis showed that older patients represented a substantial proportion of medical department admissions.

| Age Group | Records | Percentage |
| --------- | ------: | ---------: |
| 66+       |   2,653 |     30.76% |
| 51–65     |   2,440 |     28.29% |

Patients aged **66 years and above** represented the largest age group in the analyzed disease dataset.

---

# 🦠 Disease Trend Analysis

The analysis identified the most frequently recorded diseases in the medical department.

### Top Conditions

| Rank | Disease                        | Cases |
| ---: | ------------------------------ | ----: |
|    1 | Diabetes Mellitus (DM)         | 1,126 |
|    2 | Hypertension (HTN)             |   867 |
|    3 | Cerebrovascular Accident (CVA) |   681 |
|    4 | Acute Gastroenteritis (AGE)    |   648 |
|    5 | Fever                          |   431 |

These results were used as part of the disease trend analysis and forecasting workflow.

---

# 🔮 Time-Series Forecasting

**Facebook Prophet** was used to forecast future disease trends.

The forecasting workflow included:

1. Preparing disease-specific time-series datasets.
2. Sorting observations chronologically.
3. Splitting the data chronologically into training and testing periods.
4. Training Prophet models.
5. Generating forecasts.
6. Comparing predictions with actual test-period values.
7. Evaluating model performance using MAE, RMSE, and MAPE.
8. Generating future forecasts for Power BI visualization.

The forecasting analysis covered **44 clinical conditions**.

---

# 📏 Model Evaluation

Forecasting performance was evaluated using:

### MAE — Mean Absolute Error

Measures the average absolute difference between actual and predicted values.

### RMSE — Root Mean Squared Error

Measures prediction error while giving greater weight to larger errors.

### MAPE — Mean Absolute Percentage Error

Measures prediction error as a percentage of actual values.

### Representative Results

| Disease                                  |   MAPE |
| ---------------------------------------- | -----: |
| Hypertension (HTN)                       |  8.23% |
| Lower Respiratory Tract Infection (LRTI) | 10.64% |
| Tuberculosis (TB)                        | 19.55% |
| Diabetes Mellitus (DM)                   | 30.38% |
| Cerebrovascular Accident (CVA)           | 30.62% |

Forecast accuracy varied considerably across diseases, particularly for conditions with lower case volumes or irregular occurrence patterns.

For example, the AGE forecast showed a **MAPE of 107.5%**, demonstrating that percentage-based error can become very large when actual case counts are low or highly variable.

---

# 📊 Power BI Dashboard

The final analytical results were integrated into an interactive **Power BI dashboard** designed for hospital management and decision-support purposes.

The dashboard provides:

* Patient flow analysis
* Disease distribution
* Demographic analysis
* Age-group analysis
* Gender analysis
* Seasonal trends
* Top disease analysis
* Actual vs. forecast trends
* Future disease forecasts
* Key performance indicators

### Dashboard Structure

The dashboard is organized into multiple analytical views to allow users to move from overall patient flow to disease-specific trends and forecasts.

### Dashboard Preview

Add your Power BI screenshot here:

```markdown
![Patient Flow and Disease Trends Dashboard](Dashboard.png)
```

---

# 📌 Key Findings

The project identified several important patterns within the analyzed hospital records:

* Average daily admissions were approximately **26 patients**.
* Daily admissions ranged from **1 to 77 patients**.
* Summer recorded the highest seasonal admission volume with **3,126 admissions**.
* October 2024 recorded the highest monthly admission volume with **1,000 admissions**.
* Patients aged **66+ years** represented the largest age group.
* Diabetes Mellitus was the most frequently recorded condition with **1,126 cases**.
* Hypertension accounted for **867 cases**.
* CVA accounted for **681 cases**.
* Prophet forecasting performance varied substantially between diseases.
* HTN, LRTI, and TB produced comparatively lower MAPE values, while some lower-frequency conditions produced substantially higher percentage errors.

---

# 🧪 Project Methodology

The overall methodology can be summarized as:

```text
Data Collection
      ↓
Data Digitization
      ↓
Data Cleaning
      ↓
Exploratory Data Analysis
      ↓
Patient Flow Analysis
      ↓
Disease Trend Analysis
      ↓
Disease-Specific Dataset Preparation
      ↓
Chronological Train/Test Split
      ↓
Prophet Forecasting
      ↓
MAE / RMSE / MAPE Evaluation
      ↓
Power BI Dashboard
      ↓
Decision-Support Visualization
```

---

# 🎓 Academic Context

**Project Title:**

> Healthcare Analytics for Patient Flow and Disease Trends Forecasting: A Case Study of Medical Department DHQ Hospital Timergara

**Department:** Department of Computer Science
**University:** University of Malakand
**Session:** 2022–2026

### Case Study

**Medical Department, DHQ Hospital Timergara**
Lower Dir, Khyber Pakhtunkhwa, Pakistan

---

# 👨‍💻 Authors

* **Muhammad Sohaib**
* **Muhammad Ilyas**
* **Khushbakht Hanif**

---

# 🔐 Data Privacy & Ethical Considerations

The project was developed for academic and research purposes.

The analysis focuses on aggregated patient-flow and disease-trend information. Patient information was handled for the purpose of academic analysis, with consideration given to patient anonymity and data privacy.

---

# 🚀 Future Improvements

Potential future extensions include:

* Incorporating additional hospital departments.
* Integrating larger historical datasets.
* Comparing multiple forecasting algorithms.
* Developing automated data-refresh pipelines.
* Adding additional operational variables when reliable data becomes available.
* Deploying the dashboard through an appropriate institutional reporting environment.

---

## ⭐ Project Summary

This project demonstrates a complete healthcare data analytics pipeline:

**Hospital Registers → Data Digitization → Python/Pandas → EDA → Disease Analysis → Prophet Forecasting → Model Evaluation → Power BI Dashboard**

It combines **data preprocessing, exploratory analytics, time-series forecasting, model evaluation, and business intelligence** to transform historical hospital records into an analytical decision-support resource.
