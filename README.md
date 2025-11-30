# Mobile Banking App Customer Satisfaction Analysis

## Task 1: Data Collection and Preprocessing

## Task Overview
This project, conducted as a Data Analyst for **Omega Consultancy**, focuses on analyzing customer satisfaction with mobile banking applications for three major Ethiopian banks: **Commercial Bank of Ethiopia (CBE)**, **Bank of Abyssinia (BOA)**, and **Dashen Bank**.

**Task 1** specifically involved setting up the project environment, collecting raw user reviews from the **Google Play Store** using web scraping, and performing initial data preprocessing to create a clean, unified dataset ready for in-depth analysis in subsequent tasks.

---

##  Methodology and Implementation

### 1. Git and Environment Setup

* **Repository Structure:** The project adheres to a standard data science repository structure.
* **Branching Strategy:** Work was conducted on the `task-1` branch, with frequent commits documenting logical steps.
* **Dependencies:** All required Python packages are listed in the `requirements.txt` file (e.g., `google-play-scraper`, `pandas`).

### 2. Web Scraping (Data Collection)

The goal was to collect a **minimum of 400 reviews** for each bank's app, totaling at least 1,200 reviews.

* **Tool Used:** The `google-play-scraper` Python library was employed.
* **Target Applications and Current Metrics (Scraped on 2025-11-29):**
    * **Commercial Bank of Ethiopia (CBE):** App ID: `com.combanketh.mobilebanking` (Rating: 4.32)
    * **Bank of Abyssinia (BOA):** App ID: `com.boa.boaMobileBanking` (Rating: 4.18)
    * **Dashen Bank:** App ID: `com.dashen.dashensuperapp` (Rating: 4.16)
* **Result (Raw Collection):** A total of **2,100** reviews were initially collected.
    * CBE: 700 reviews
    * BOA: 700 reviews
    * Dashen Bank: 700 reviews

### 3. Data Preprocessing

The scraped data underwent cleaning and transformation to ensure consistency and quality.

| Step | Action Taken | Rationale |
| :--- | :--- | :--- |
| **Handling Missing Data** | Critical fields (`review` and `rating`) had **0** missing values. The highly sparse `reply_content` and non-critical `app_id` columns were handled. | Confirms data completeness for core analysis features. |
| **Handling Duplicates** | **31** duplicates were identified and removed from the raw dataset. | Ensures each unique piece of feedback is counted only once. |
| **Text Filtering** | **905** non-English reviews were detected and removed. | Essential for accurate English-based Sentiment Analysis and Topic Modeling (planned for Task 2). This resulted in a data retention rate of **56.90%**. |
| **Date Normalization** | Converted all review timestamps to a standardized **YYYY-MM-DD** format. The date range spans from **2024-05-11 to 2025-11-29**. | Essential for time-series analysis in later tasks. |
| **Feature Engineering** | Columns were simplified and renamed to the final required schema (`review`, `rating`, `date`, `bank`, `source`). | Standardizes the dataset and clearly identifies the origin of each review. |

---

### 4. Visualizations 


##  Output Dataset Structure

The final preprocessed dataset (`reviews_processed.csv`) contains **1,195** records and the following columns:

| Column Name | Data Type | Description | Example |
| :--- | :--- | :--- | :--- |
| **review** | `string` | The user's feedback text (English only). | "This app is fast and very reliable." |
| **rating** | `int` | The 1-5 star rating given by the user. | 5 |
| **date** | `date` | The normalized date the review was posted (YYYY-MM-DD). | 2025-11-28 |
| **bank** | `string` | The code for the bank reviewed (CBE, BOA, or Dashen). | Dashen Bank |
| **source** | `string` | The platform the review was scraped from. | Google Play |

---

## Cleaned Data Distribution Summary

| Metric | Detail |
| :--- | :--- |
| **Final Records** | **1,195** |
| **Reviews per Bank** | Dashen Bank: 444, Bank of Abyssinia: 411, CBE: 340 |
| **Date Range** | 2024-05-11 to 2025-11-29 |
| **Top Rating** | ⭐⭐⭐⭐⭐: 608 reviews (50.9%) |
| **Lowest Rating** | ⭐: 373 reviews (31.2%) |

---

## Key Performance Indicators (KPIs)

| KPI | Target | Achieved | Notes |
| :--- | :--- | :--- | :--- |
| **Total Reviews Collected** | 1,200+ | **1,195** | Slightly below the 1,200 target due to strict removal of non-English content. **444** reviews for Dashen, **411** for BOA, and **340** for CBE. |
| **Missing Data** | <5% | **0%** (for critical data) | No missing values in the final `review` and `rating` fields. |
| **Clean CSV Dataset** | Clean CSV | **Generated** | Final dataset successfully saved to `data/processed/reviews_processed.csv`. |
| **Organized Git Repo** | Clear commits, `requirements.txt` | **Confirmed** | Repository is organized and commits are meaningful. |

---

## Repository Contents

| File/Folder | Description |
| :--- | :--- |
| `data/` | Directory for storing raw (`reviews_raw.csv`) and cleaned datasets (`reviews_processed.csv`). |
| `notebooks/` | Contains the `scrape_EDA.ipynb` used for data collection and initial exploration. |
| `src/` | Contains reusable Python modules, including `scraper.py` and `preprocessor.py`. |
| `requirements.txt` | List of all project dependencies. |
| `.gitignore` | Ensures unnecessary files (like large datasets or temporary files) are not committed. |
| `README.md` | This documentation file. |


---