# 📊 Customer Churn Analysis
> **Telco Customer Dataset — Exploratory Data Analysis & Business Insights**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0-green)](https://pandas.pydata.org)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.12-orange)](https://seaborn.pydata.org)

---

## 📌 Project Overview

This project analyzes the IBM Telco Customer Churn dataset to identify patterns, risk factors, and behavioral segments that contribute to customer churn. The goal is to equip business teams with data-driven insights to improve customer retention.

---

## 📁 Project Structure

```
customer-churn-analysis/
│
├── data/
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv   # Raw dataset
│
├── notebooks/
│   └── churn_analysis.ipynb                    # Jupyter Notebook (full analysis)
│
├── visuals/
│   ├── 01_churn_distribution.png
│   ├── 02_gender_vs_churn.png
│   ├── 03_contract_vs_churn.png
│   ├── 04_monthly_charges_vs_churn.png
│   ├── 05_tenure_vs_churn.png
│   ├── 06_payment_method_vs_churn.png
│   ├── 07_correlation_heatmap.png
│   ├── 08_internet_service_vs_churn.png
│   └── 09_risk_factors.png
│
├── analysis.py                                 # Standalone Python script
└── README.md
```

---

## 📦 Dataset Description

| Column | Description |
|--------|-------------|
| `customerID` | Unique customer identifier |
| `gender` | Male / Female |
| `SeniorCitizen` | Whether the customer is a senior citizen (0/1) |
| `Partner` | Whether the customer has a partner |
| `Dependents` | Whether the customer has dependents |
| `tenure` | Number of months with the company |
| `PhoneService` | Has phone service |
| `InternetService` | DSL / Fiber optic / No |
| `Contract` | Month-to-month / One year / Two year |
| `PaymentMethod` | Electronic check / Mailed check / Bank transfer / Credit card |
| `MonthlyCharges` | Monthly amount charged ($) |
| `TotalCharges` | Total amount charged to date ($) |
| `Churn` | Whether the customer churned (Yes/No) |

- **Total Records:** 7,043
- **Features:** 21 columns
- **Target Variable:** `Churn`

---

## 🛠 Tools & Technologies

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Core language |
| Pandas | Data loading, cleaning, manipulation |
| NumPy | Numerical operations |
| Matplotlib | Base visualizations |
| Seaborn | Statistical plots and heatmaps |
| Jupyter Notebook | Interactive analysis environment |

---

## 🧹 Data Cleaning Process

1. **Missing Values** — `TotalCharges` contained 11 whitespace entries (new customers with 0 tenure). Converted to numeric and filled with `0`.
2. **Duplicates** — Checked for and removed any duplicate rows (none found).
3. **Data Type Fixes** — `SeniorCitizen` converted from int (0/1) to categorical (No/Yes). `Churn` converted to binary int (0/1) for analysis.
4. **Feature Encoding** — Derived binary indicator features for correlation analysis.

---

## 📊 Visualizations

| # | Chart | Insight |
|---|-------|---------|
| 1 | Churn Distribution | 26.5% of customers churned |
| 2 | Gender vs Churn | Gender has minimal impact on churn |
| 3 | Contract Type vs Churn | Month-to-month = ~43% churn |
| 4 | Monthly Charges vs Churn | Churners pay higher monthly charges |
| 5 | Tenure vs Churn | New customers churn most (~48%) |
| 6 | Payment Method vs Churn | Electronic check = ~45% churn |
| 7 | Correlation Heatmap | Strong negative: tenure ↔ churn |
| 8 | Internet Service vs Churn | Fiber optic = ~42% churn |
| 9 | Risk Factor Summary | All high-risk factors vs average |

---

## 🔍 Key Findings

- **Churn Rate:** 26.54%
- **Average Monthly Charges:** ~$64.76
- **Average Tenure:** ~32.4 months

| Risk Factor | Churn Rate |
|------------|------------|
| Month-to-Month Contract | ~43% |
| Electronic Check Payment | ~45% |
| Fiber Optic Internet | ~42% |
| New Customers (≤12 months) | ~48% |
| No Online Security | ~42% |
| Senior Citizens | ~41% |

---

## 💡 Business Recommendations

1. **Contract Upgrade Campaign** — Incentivize month-to-month customers to switch to annual plans via discounts.
2. **Auto-Pay Incentive** — Offer a monthly discount for switching from electronic check to automatic payment.
3. **Fiber Quality Audit** — Review fiber optic pricing and service quality vs competitors.
4. **Early Onboarding Program** — Proactive support in the first 90 days to reduce early churn.
5. **Security & Support Bundles** — Package tech support + online security at a reduced rate.
6. **Senior Citizen Plan** — Dedicated support and simplified billing for senior customers.

---

## ✅ Conclusion

Customer churn is primarily driven by **contract flexibility, payment friction, early tenure, and service quality issues**. With targeted interventions—particularly around contract upgrades and first-year onboarding—churn rates could realistically drop by **8–12 percentage points**, representing significant revenue retention.

---

## 🚀 How to Run

```bash
# Clone the repository
git clone https://github.com/<your-username>/customer-churn-analysis.git
cd customer-churn-analysis

# Install dependencies
pip install pandas numpy matplotlib seaborn jupyter

# Run the Python script
python analysis.py

# Or open the notebook
jupyter notebook notebooks/churn_analysis.ipynb
```

---

*Built as a Data Analyst portfolio project.*
