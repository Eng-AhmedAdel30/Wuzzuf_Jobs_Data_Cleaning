# 🧹 Wuzzuf Jobs 2020–2021 — Data Cleaning Notebook

A Python notebook that cleans, standardizes, and restructures a raw dataset of job postings scraped from [Wuzzuf](https://wuzzuf.net), Egypt's leading online job marketplace, covering the period **2020–2021**.

---

## 📁 Project Structure

```
Wuzzuf_Jobs_2020-2021.ipynb   ← Main cleaning notebook
cleaned wuzzuf_jobs_2020-2021.csv  ← Output: cleaned dataset
```

---

## 📦 Dependencies

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

Install via pip if needed:

```bash
pip install pandas numpy matplotlib openpyxl
```

---

## 📥 Input Data

| Property | Detail |
|---|---|
| **File** | `Wuzzuf_Jobs_2020-2021 (1).xlsx` |
| **Source** | Wuzzuf job postings portal |
| **Period** | 2020–2021 |
| **Format** | Excel (`.xlsx`) with an index column |

The raw dataset contains job listings with fields such as job title, city, job categories, industry, salary range, career level, experience required, post date, and view counts.

---

## 🔧 Data Cleaning Steps

### 1. Remove Duplicates & Empty Rows

```python
df.drop_duplicates(inplace=True)   # Removed 28 duplicate rows
df.dropna(how='all', inplace=True) # Removed fully empty rows
```

---

### 2. City Name Standardization

- Applied `.str.title()` to capitalize city names consistently.
- Built a correction dictionary mapping **misspelled/abbreviated city names** to their correct canonical forms for over 200 cities (e.g., `'Lexndri'` → `'Alexandria'`, `'Dubi'` → `'Dubai'`, `'Doh'` → `'Doha'`).

```python
df['city'] = df['city'].str.title()
df['city'] = df['city'].replace(replacement_dict)
```

---

### 3. Job Category Cleaning

- Identified rows where `job_category1` was null.
- Created a manual mapping of **job titles → job categories** (e.g., `'Sales Representative'` → `'Marketing & Sales'`, `'HVAC Engineer'` → `'Engineering & Technical'`) to fill in missing values.
- Remaining unfilled rows were assigned the fallback title `'Real Estate Sales Representative'`.
- `job_category2` and `job_category3` null values were replaced with empty strings, then the two columns were **merged into a single `job_category2` column**, and `job_category3` was dropped.

```python
df['job_category1'] = df['job_category1'].fillna(df['job_title'].map(job_category_mapping))
df['job_category2'] = df['job_category2'] + ' ' + df['job_category3']
df.drop(columns=['job_category3'], inplace=True)
```

---

### 4. Industry Column Cleaning

- Null values in `industry1`, `industry2`, and `industry3` replaced with empty strings.
- Standardized `'Information Technology & Services'` → `'IT & Software'`.
- Removed placeholder values (`'Select'`) from all three industry columns.
- Merged `industry2` and `industry3` into a single `industry2` column; `industry3` was then dropped.

```python
df['industry1'].replace('Information Technology & Services', 'IT & Software', inplace=True)
df['industry2'] = df['industry2'] + ' ' + df['industry3']
df.drop(columns=['industry3'], inplace=True)
```

---

### 5. Currency Standardization

- Corrected `'Estonian Kroon'` → `'Euro'` (the Estonian Kroon was retired in 2011 when Estonia joined the Eurozone).

```python
df['currency_name'].replace('Estonian Kroon', 'Euro', inplace=True)
```

---

### 6. Salary Range Splitting & Cleaning

The raw `Salary_range` column held values like `'5000-8000'` as text.

**Steps:**
- Split `Salary_range` on `'-'` into two new columns: `Min_Salary` and `Max_Salary`.
- Replaced `'0'` values with `NaN` (undisclosed salaries).
- Replaced `'0-0'` in `Salary_range` with `'Not Disclosed'`.
- Detected and corrected corrupted date-like values (e.g., `'Aug-00'`, `'Jan-00'`) that appeared due to Excel auto-formatting, replacing them with `'Not Disclosed'`.
- Converted `Min_Salary` and `Max_Salary` to nullable integer type (`Int64`).

```python
df[['Min_Salary', 'Max_Salary']] = df['Salary_range'].str.split('-', expand=True)
df['Min_Salary'] = df['Min_Salary'].replace('0', np.nan).astype('Int64')
df['Max_Salary'] = df['Max_Salary'].replace('0', np.nan).astype('Int64')
```

---

### 7. Salary Outlier Removal

Unrealistic salary values were identified by grouping on `salary_period` and `currency_name`, then rows violating domain-specific thresholds were dropped:

| Condition | Reason |
|---|---|
| Per Hour · USD · Min Salary ≥ 10,000 | Impossibly high hourly rate |
| Per Hour · EGP · Student · Min Salary ≥ 1,000 | Unrealistic for student hourly |
| Per Hour · EGP · Entry Level · Min Salary > 750 | Outside valid range |
| Per Hour · EGP · Min Salary ≥ 6,000 | Extreme outlier |
| Per Month · EGP · Max Salary ≥ 1,000,000 | Data entry error |
| Per Year · EGP · Max Salary ≥ 1,000,000 | Data entry error |
| Per Hour · Yemen Riyal | Negligible/invalid entries |
| Per Month · Iraqi New Dinar | Negligible/invalid entries |

---

### 8. Experience Years Cleaning

- Inspected unique values in `experience_years`.
- Used `pd.to_datetime(..., errors='coerce')` to detect corrupted date-like entries (Excel misformatting), then replaced those with `NaN`.

```python
data_check = pd.to_datetime(df['experience_years'], errors='coerce')
df.loc[data_check.notna(), 'experience_years'] = np.nan
```

---

### 9. Post Date Standardization

- Converted `post_date` to a uniform datetime format: `YYYY-MM-DD HH:MM:SS`.

```python
df['post_date'] = pd.to_datetime(df['post_date'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
```

---

### 10. Column Reordering & Whitespace Cleanup

- Reordered columns to a logical sequence for analysis.
- Stripped leading/trailing whitespace from all column names.

```python
df.columns = df.columns.str.strip()
df = df[['job_title', 'city', 'job_category1', 'job_category2',
         'industry1', 'industry2', 'Salary_range', 'Min_Salary', 'Max_Salary',
         'num_vacancies', 'career_level', 'experience_years',
         'post_date', 'views', 'salary_period', 'currency_name']]
```

---

## 📤 Output

The cleaned dataset is exported as a CSV file:

```python
df.to_csv('cleaned wuzzuf_jobs_2020-2021.csv', index=False)
```

---

## 📊 Visualizations Included

The notebook includes exploratory plots generated with `matplotlib`:

| Chart | Description |
|---|---|
| **Top 5 Cities by Job Count** | Bar chart of cities with the highest number of listings |
| **Career Level Distribution** | Pie chart showing the share of each career level |
| **Top 5 Job Categories** | Bar chart of the most common job categories |
| **Top 5 Entry-Level Jobs by Salary (EGP/Month)** | Bar chart of highest-paying entry-level titles in Egyptian Pounds |
| **Top 3 Hourly Jobs by Salary (USD/Hour)** | Bar chart of highest-paying per-hour roles in US Dollars |
| **Top 5 Industries by Average Salary** | Bar chart of industries offering the highest mean salary |

---

## ✅ Summary of Changes

| Step | Action |
|---|---|
| Duplicates | 28 duplicate rows removed |
| City names | Title-cased + 30+ misspellings corrected |
| Job categories | Nulls filled via title mapping; columns merged |
| Industry | Nulls filled; placeholder values removed; columns merged |
| Currency | Estonian Kroon unified to Euro |
| Salary range | Split into Min/Max; zeros → NaN; anomalies → Not Disclosed |
| Salary outliers | Multiple domain-specific thresholds applied |
| Experience | Date-corrupted values → NaN |
| Post date | Unified to `YYYY-MM-DD HH:MM:SS` |

---

## 👤 Author

**Eng. Ahmed**  
Data Engineering Project — Wuzzuf Jobs 2020–2021 Cleaning Pipeline
