# Consumer Sentiment Analytics Dashboard  
**Group 2 – Web Analytics Project**

---

## 1. Project Overview
This project analyzes consumer sentiment from product reviews to support **data-driven product portfolio decisions**.

The objective is to identify which product category can be discontinued while minimizing:
- customer dissatisfaction  
- reputational risk  
- negative sentiment impact  

The project integrates:
- web scraping  
- data cleaning  
- sentiment analysis  
- dashboard visualization  

---

## 2. Repository Structure

group-2-web-analytics/  
│  
├── src/                        # UI / dashboard scaffold  
├── sony_scraper.ipynb          # data scraping script  
├── Data_cleaning_script.ipynb  # data cleaning process  
├── sentiment_analysis.ipynb    # sentiment analysis  
├── sony_raw_data.csv           # raw scraped data  
├── sony_cleaned_data.csv       # cleaned dataset  
├── app.py                      # Streamlit dashboard app  
├── requirements.txt            # dependencies  
└── README.md  

---

## 3. How to Run the Project

### Step 1 — Install Dependencies
pip install -r requirements.txt  

---

### Step 2 — Run Scraping Script
Open and execute:  
sony_scraper.ipynb  

This script collects product review data.

---

### Step 3 — Data Cleaning
Open and execute:  
Data_cleaning_script.ipynb  

This step:
- removes noise  
- standardizes text  
- prepares structured dataset  

---

### Step 4 — Sentiment Analysis
Open and execute:  
sentiment_analysis.ipynb  

This generates:
- sentiment scores (positive / neutral / negative)  
- polarity values  
- structured outputs for dashboard use  

---

### Step 5 — Run Dashboard
streamlit run app.py  

---

## 4. Live Dashboard

https://group-2-dashboard-4tagjp2dgeqfmjsrzm7x93.streamlit.app/

The dashboard provides:
- product-level sentiment comparison  
- feature-level insights  
- consumer language patterns  
- decision recommendation  

---

## 5. Key Features

- Sentiment classification of product reviews  
- Product comparison based on sentiment  
- Feature-level insight extraction  
- Consumer language / keyword analysis  
- Backlash risk interpretation  
- Executive decision-support interface  

---

## 6. Notes

- Scraping scripts are designed to retrieve **at least partial datasets**, meeting project requirements.  
- The dashboard uses processed data and can be extended with additional inputs.  
- The UI is structured to support future integration with automated pipelines.  

---

## 7. Team

Group 2 – Web Analytics Course  
Fordham University
