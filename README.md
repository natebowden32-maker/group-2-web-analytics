# Consumer Sentiment Analytics Dashboard
**Group 2 – Web Analytics Project**

---

## 1. Project Overview

This project analyzes consumer sentiment from YouTube comments to support **data-driven product portfolio decisions** for Google's discontinued and at-risk product lines.

The objective is to identify which product category can be discontinued while minimizing:
- customer dissatisfaction
- reputational risk
- negative sentiment impact

The three products under analysis are:
- **Google Glass**
- **Google+**
- **Google Stadia**

The project integrates:
- YouTube comment scraping
- data cleaning
- sentiment analysis (general + aspect-based)
- statistical analysis
- dashboard visualization

---

## 2. Repository Structure

```
group-2-web-analytics/
│
├── src/                                          # UI / dashboard scaffold
├── aspect_sentiment_analysis.ipynb               # Aspect-Based Sentiment Analysis (ABSA)
├── sentiment_analysis.ipynb                      # General sentiment analysis
├── statistical_analysis.ipynb                    # Statistical analysis of sentiment outputs
├── Data_cleaning_script.ipynb                    # Data cleaning (Sony legacy)
├── data_cleaning_glass_plus.ipynb                # Data cleaning for Glass and Google+ datasets
├── old_google_glass_youtube_comments_raw.csv     # Raw older Glass comments
├── recent_google_glass_youtube_comments_raw.csv  # Raw recent Glass comments
├── old_plus_youtube_comments_raw.csv             # Raw older Google+ comments
├── recent_plus_youtube_comments_raw.csv          # Raw recent Google+ comments
├── old_stadia_youtube_comments_raw.csv           # Raw older Stadia comments
├── recent_stadia_youtube_comments_raw.csv        # Raw recent Stadia comments
├── cleaned_stadia_youtube_comments_with_wordcount.csv  # Cleaned Stadia dataset
├── absa_extractions.csv                          # ABSA structured output (CSV)
├── absa_extractions.json                         # ABSA structured output (JSON)
├── absa_aspect_sentiment.png                     # ABSA visualization
├── absa_before_after.png                         # Pre/post sentiment comparison
├── tfidf_analysis.ipynb                          # TF-IDF keyword analysis
├── gephi_network_export.ipynb                    # Keyword co-occurrence network analysis
├── tfidf_keywords.csv                            # TF-IDF top keywords per product per period
├── tfidf_keywords.png                            # TF-IDF keyword visualization
├── gephi_nodes.csv                               # Network nodes (keywords + frequency)
├── gephi_edges.csv                               # Network edges (keyword co-occurrences)
├── wiki_analysis_report.md                       # Full analysis report (sentiment, TF-IDF, network, ABSA)
├── app.py                                        # Streamlit dashboard app
├── requirements.txt                              # Dependencies
├── .env.example                                  # Example environment variables
└── README.md
```

---

## 3. Environment Setup

### Step 1 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2 — Configure Environment Variables

Copy `.env.example` to `.env` and add your Gemini API key:

```bash
cp .env.example .env
```

Then open `.env` and fill in:

```
GEMINI_API_KEY=your_key_here
```

---

## 4. How to Run the Project

### Step 1 — Data Cleaning

Open and execute:

```
data_cleaning_glass_plus.ipynb
```

This step:
- removes noise from raw YouTube comment data
- standardizes text fields
- adds word count metrics
- prepares structured datasets for Glass and Google+

The Stadia cleaned dataset (`cleaned_stadia_youtube_comments_with_wordcount.csv`) is already included in the repository.

---

### Step 2 — Sentiment Analysis

Open and execute:

```
sentiment_analysis.ipynb
```

This generates:
- sentiment scores (positive / neutral / negative)
- polarity values
- structured outputs for dashboard use

---

### Step 3 — Aspect-Based Sentiment Analysis (ABSA)

Open and execute:

```
aspect_sentiment_analysis.ipynb
```

This generates:
- aspect-level sentiment extractions per product
- structured ABSA outputs (`absa_extractions.csv`, `absa_extractions.json`)
- visualizations (`absa_aspect_sentiment.png`, `absa_before_after.png`)

Requires a valid Gemini API key in `.env`.

---

### Step 4 — Statistical Analysis

Open and execute:

```
statistical_analysis.ipynb
```

This performs statistical comparison of sentiment distributions across the three products.

---
### Step 5 — TF-IDF Keyword Analysis

Open and execute:tfidf_analysis.ipynb
This generates:
- top distinctive keywords per product per time period
- before vs. after keyword comparison
- structured keyword outputs (`tfidf_keywords.csv`)
- keyword frequency visualization (`tfidf_keywords.png`)

---

### Step 6 — Keyword Co-occurrence Network (Gephi)

Open and execute:gephi_network_export.ipynb
This generates:
- keyword co-occurrence network for each product
- node file (`gephi_nodes.csv`) and edge file (`gephi_edges.csv`) for Gephi import
- NetworkX network preview with degree and betweenness centrality measures

---
### Step 7 — Run Dashboard

```bash
streamlit run app.py
```

---

## 5. Key Features

- YouTube comment collection across old and recent timeframes
- Sentiment classification of consumer reviews across three Google products
- Product comparison based on aggregate sentiment scores
- Aspect-based sentiment extraction (ABSA) using Gemini
- Statistical analysis of sentiment distributions
- Consumer language and keyword analysis
- Backlash risk interpretation
- Executive decision-support interface

---

## 6. Notes

- Raw comment datasets are split into **old** and **recent** files per product to enable temporal sentiment comparison.
- ABSA requires a Gemini API key configured via `.env`.
- The dashboard uses processed data and can be extended with additional inputs.
- The UI is structured to support future integration with automated pipelines.

---

## 7. Team

Group 2 – Web Analytics Course
Fordham University
