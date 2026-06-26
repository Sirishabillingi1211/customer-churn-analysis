# =============================================================================
# Customer Churn Analysis
# Telco Customer Dataset - Complete EDA & Business Insights
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.dpi'] = 120

# Ensure visuals directory exists
os.makedirs('visuals', exist_ok=True)

# =============================================================================
# 1. LOAD DATA
# =============================================================================
df = pd.read_csv('data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
print("Dataset loaded:", df.shape)
print(df.head(3))

# =============================================================================
# 2. DATA CLEANING
# =============================================================================
print("\n--- DATA CLEANING REPORT ---")

# 2a. Missing values
print("\nMissing values per column:")
print(df.isnull().sum())

# TotalCharges has whitespace strings that should be NaN
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
missing_after = df.isnull().sum()
print("\nAfter fixing TotalCharges:")
print(missing_after[missing_after > 0])

# Fill TotalCharges NaN with 0 (new customers with 0 tenure)
df['TotalCharges'].fillna(0, inplace=True)

# 2b. Duplicates
dupes = df.duplicated().sum()
print(f"\nDuplicate rows: {dupes}")
df.drop_duplicates(inplace=True)

# 2c. Data types
df['SeniorCitizen'] = df['SeniorCitizen'].map({0: 'No', 1: 'Yes'})
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

print("\nData types after fixing:")
print(df.dtypes)
print(f"\nFinal dataset shape: {df.shape}")

# =============================================================================
# 3. KEY METRICS
# =============================================================================
churn_rate = df['Churn'].mean() * 100
avg_monthly_charges = df['MonthlyCharges'].mean()
avg_tenure = df['tenure'].mean()

print("\n--- KEY METRICS ---")
print(f"Churn Rate          : {churn_rate:.2f}%")
print(f"Avg Monthly Charges : ${avg_monthly_charges:.2f}")
print(f"Avg Tenure (months) : {avg_tenure:.1f}")

# =============================================================================
# 4. CUSTOMER SEGMENTATION
# =============================================================================
def segment_customer(row):
    if row['tenure'] <= 12:
        return 'New'
    elif row['tenure'] <= 36:
        return 'Mid-Term'
    else:
        return 'Long-Term'

df['Segment'] = df.apply(segment_customer, axis=1)

segment_churn = df.groupby('Segment')['Churn'].agg(['mean', 'count']).reset_index()
segment_churn.columns = ['Segment', 'ChurnRate', 'Count']
segment_churn['ChurnRate'] = (segment_churn['ChurnRate'] * 100).round(2)
print("\nCustomer Segmentation by Churn:\n", segment_churn)

# =============================================================================
# 5. EXPLORATORY DATA ANALYSIS - STATISTICAL SUMMARY
# =============================================================================
print("\n--- STATISTICAL SUMMARY ---")
print(df[['tenure', 'MonthlyCharges', 'TotalCharges']].describe())

churn_groups = df.groupby('Churn')[['MonthlyCharges', 'tenure', 'TotalCharges']].mean()
churn_groups.index = ['Retained', 'Churned']
print("\nMean values by Churn status:\n", churn_groups.round(2))

# =============================================================================
# 6. VISUALIZATIONS
# =============================================================================

CHURN_COLORS = ['#2ecc71', '#e74c3c']   # green=retained, red=churned

# --- 6.1 Churn Distribution ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Churn Distribution', fontsize=14, fontweight='bold')

counts = df['Churn'].value_counts()
labels = ['Retained', 'Churned']
axes[0].bar(labels, counts.values, color=CHURN_COLORS, edgecolor='white', width=0.5)
axes[0].set_ylabel('Count')
for i, v in enumerate(counts.values):
    axes[0].text(i, v + 30, str(v), ha='center', fontweight='bold')

axes[1].pie(counts.values, labels=labels, colors=CHURN_COLORS,
            autopct='%1.1f%%', startangle=140, wedgeprops={'edgecolor': 'white'})
axes[1].set_title(f'Churn Rate: {churn_rate:.1f}%')

plt.tight_layout()
plt.savefig('visuals/01_churn_distribution.png')
plt.close()
print("Saved: visuals/01_churn_distribution.png")

# --- 6.2 Gender vs Churn ---
fig, ax = plt.subplots(figsize=(8, 5))
gender_churn = df.groupby('gender')['Churn'].mean().reset_index()
gender_churn['ChurnRate'] = gender_churn['Churn'] * 100
bars = ax.bar(gender_churn['gender'], gender_churn['ChurnRate'],
              color=['#3498db', '#e91e63'], width=0.4, edgecolor='white')
ax.set_title('Churn Rate by Gender', fontsize=13, fontweight='bold')
ax.set_ylabel('Churn Rate (%)')
ax.set_ylim(0, 35)
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{bar.get_height():.1f}%', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('visuals/02_gender_vs_churn.png')
plt.close()
print("Saved: visuals/02_gender_vs_churn.png")

# --- 6.3 Contract Type vs Churn ---
fig, ax = plt.subplots(figsize=(9, 5))
contract_churn = df.groupby('Contract')['Churn'].mean().reset_index()
contract_churn['ChurnRate'] = contract_churn['Churn'] * 100
contract_churn = contract_churn.sort_values('ChurnRate', ascending=False)
colors = ['#e74c3c', '#f39c12', '#2ecc71']
bars = ax.bar(contract_churn['Contract'], contract_churn['ChurnRate'],
              color=colors, edgecolor='white', width=0.5)
ax.set_title('Churn Rate by Contract Type', fontsize=13, fontweight='bold')
ax.set_ylabel('Churn Rate (%)')
ax.set_ylim(0, 55)
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{bar.get_height():.1f}%', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('visuals/03_contract_vs_churn.png')
plt.close()
print("Saved: visuals/03_contract_vs_churn.png")

# --- 6.4 Monthly Charges vs Churn ---
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('Monthly Charges vs Churn', fontsize=14, fontweight='bold')

churned = df[df['Churn'] == 1]['MonthlyCharges']
retained = df[df['Churn'] == 0]['MonthlyCharges']

axes[0].hist(retained, bins=30, alpha=0.6, color='#2ecc71', label='Retained')
axes[0].hist(churned, bins=30, alpha=0.6, color='#e74c3c', label='Churned')
axes[0].set_xlabel('Monthly Charges ($)')
axes[0].set_ylabel('Count')
axes[0].legend()
axes[0].set_title('Distribution')

axes[1].boxplot([retained, churned], labels=['Retained', 'Churned'],
                patch_artist=True,
                boxprops=dict(facecolor='#f0f0f0'),
                medianprops=dict(color='black', linewidth=2))
axes[1].set_ylabel('Monthly Charges ($)')
axes[1].set_title('Boxplot')

plt.tight_layout()
plt.savefig('visuals/04_monthly_charges_vs_churn.png')
plt.close()
print("Saved: visuals/04_monthly_charges_vs_churn.png")

# --- 6.5 Tenure vs Churn ---
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('Tenure vs Churn', fontsize=14, fontweight='bold')

churned_t = df[df['Churn'] == 1]['tenure']
retained_t = df[df['Churn'] == 0]['tenure']

axes[0].hist(retained_t, bins=30, alpha=0.6, color='#2ecc71', label='Retained')
axes[0].hist(churned_t, bins=30, alpha=0.6, color='#e74c3c', label='Churned')
axes[0].set_xlabel('Tenure (months)')
axes[0].set_ylabel('Count')
axes[0].legend()
axes[0].set_title('Distribution')

segment_order = ['New', 'Mid-Term', 'Long-Term']
seg_rates = df.groupby('Segment')['Churn'].mean().reindex(segment_order) * 100
seg_colors = ['#e74c3c', '#f39c12', '#2ecc71']
bars = axes[1].bar(segment_order, seg_rates.values, color=seg_colors, edgecolor='white', width=0.5)
axes[1].set_ylabel('Churn Rate (%)')
axes[1].set_title('Churn Rate by Customer Segment')
for bar in bars:
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f'{bar.get_height():.1f}%', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('visuals/05_tenure_vs_churn.png')
plt.close()
print("Saved: visuals/05_tenure_vs_churn.png")

# --- 6.6 Payment Method vs Churn ---
fig, ax = plt.subplots(figsize=(11, 5))
pay_churn = df.groupby('PaymentMethod')['Churn'].mean().reset_index()
pay_churn['ChurnRate'] = pay_churn['Churn'] * 100
pay_churn = pay_churn.sort_values('ChurnRate', ascending=True)
colors_pay = ['#2ecc71', '#27ae60', '#f39c12', '#e74c3c']
bars = ax.barh(pay_churn['PaymentMethod'], pay_churn['ChurnRate'],
               color=colors_pay, edgecolor='white')
ax.set_title('Churn Rate by Payment Method', fontsize=13, fontweight='bold')
ax.set_xlabel('Churn Rate (%)')
for bar in bars:
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f'{bar.get_width():.1f}%', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('visuals/06_payment_method_vs_churn.png')
plt.close()
print("Saved: visuals/06_payment_method_vs_churn.png")

# --- 6.7 Correlation Heatmap ---
fig, ax = plt.subplots(figsize=(11, 8))
numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'Churn']
# Encode key categoricals
corr_df = df[numeric_cols].copy()
# Add internet service and contract as numeric
corr_df['IsFiberOptic'] = (df['InternetService'] == 'Fiber optic').astype(int)
corr_df['IsMonthToMonth'] = (df['Contract'] == 'Month-to-month').astype(int)
corr_df['IsSenior'] = (df['SeniorCitizen'] == 'Yes').astype(int)
corr_df['ElectronicCheck'] = (df['PaymentMethod'] == 'Electronic check').astype(int)
corr_df['PaperlessBilling'] = (df['PaperlessBilling'] == 'Yes').astype(int)

corr_matrix = corr_df.corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdYlGn',
            center=0, ax=ax, linewidths=0.5,
            annot_kws={'size': 9})
ax.set_title('Correlation Heatmap (Churn & Key Features)', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('visuals/07_correlation_heatmap.png')
plt.close()
print("Saved: visuals/07_correlation_heatmap.png")

# --- 6.8 Internet Service vs Churn ---
fig, ax = plt.subplots(figsize=(9, 5))
internet_churn = df.groupby('InternetService')['Churn'].mean().reset_index()
internet_churn['ChurnRate'] = internet_churn['Churn'] * 100
internet_churn = internet_churn.sort_values('ChurnRate', ascending=False)
colors_net = ['#e74c3c', '#f39c12', '#2ecc71']
bars = ax.bar(internet_churn['InternetService'], internet_churn['ChurnRate'],
              color=colors_net, edgecolor='white', width=0.5)
ax.set_title('Churn Rate by Internet Service', fontsize=13, fontweight='bold')
ax.set_ylabel('Churn Rate (%)')
ax.set_ylim(0, 50)
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{bar.get_height():.1f}%', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('visuals/08_internet_service_vs_churn.png')
plt.close()
print("Saved: visuals/08_internet_service_vs_churn.png")

print("\nAll 8 visualizations saved to 'visuals/' folder.")

# =============================================================================
# 7. KEY FACTORS INFLUENCING CHURN
# =============================================================================
print("\n--- KEY FACTORS INFLUENCING CHURN ---")

factors = {
    'Contract Type (Month-to-Month)': df[df['Contract'] == 'Month-to-month']['Churn'].mean(),
    'Payment Method (Electronic Check)': df[df['PaymentMethod'] == 'Electronic check']['Churn'].mean(),
    'Internet Service (Fiber Optic)': df[df['InternetService'] == 'Fiber optic']['Churn'].mean(),
    'Paperless Billing': df[df['PaperlessBilling'] == 'Yes']['Churn'].mean(),
    'Senior Citizens': df[df['SeniorCitizen'] == 'Yes']['Churn'].mean(),
    'No Online Security': df[df['OnlineSecurity'] == 'No']['Churn'].mean(),
    'No Tech Support': df[df['TechSupport'] == 'No']['Churn'].mean(),
}

for k, v in sorted(factors.items(), key=lambda x: x[1], reverse=True):
    print(f"  {k:<40}: {v*100:.1f}%")

# =============================================================================
# 8. BUSINESS INSIGHTS & RECOMMENDATIONS
# =============================================================================
insights = """
--- BUSINESS INSIGHTS & RECOMMENDATIONS ---

1. CONTRACT STRATEGY
   Month-to-month customers churn at ~43% vs ~3% for
   2-year contracts. Offer incentives to upgrade to
   annual or 2-year plans (discounts, loyalty perks).

2. PAYMENT METHOD
   Electronic check users churn at ~45%. Encourage
   auto-payment (bank/credit card) with small discount.

3. FIBER OPTIC QUALITY
   Fiber optic customers churn at ~42%. Investigate
   service quality, speed, and pricing vs competition.

4. ONBOARDING & EARLY RETENTION
   New customers (<=12 months) churn most. Implement
   proactive onboarding, 90-day check-ins, welcome packs.

5. TECH SUPPORT & SECURITY UPSELL
   Customers without tech support/online security churn
   significantly more. Bundle these services at low cost.

6. SENIOR CITIZEN PROGRAM
   Senior citizens (~41% churn). Create tailored plans
   with simplified billing and dedicated support.
"""
print(insights)

print("=" * 60)
print("ANALYSIS COMPLETE — Check 'visuals/' for all charts.")
print("=" * 60)
