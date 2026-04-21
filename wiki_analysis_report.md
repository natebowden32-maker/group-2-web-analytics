# Sony Product Portfolio: Sentiment Analysis Report

## 1. Executive Summary
This report analyzes consumer sentiment across various Sony sub-brands and segment products (e.g., *Sony VAIO Laptops*, *PlayStation Vue*, and *PlayMemories Online*). By utilizing VADER (Valence Aware Dictionary and sEntiment Reasoner) for automated text processing, we evaluated consumer verbatims, identified overarching vocabulary patterns, and mapped out extreme outliers to better understand product health.

---

## 2. Statistical Analysis
We extracted and normalized the corpus text to ensure statistically robust scoring. The statistical foundations of the dashboard yield the following structural insights:

- **Global Polarity Normalization**: Consumer data was scored on a continuous scale of `-1.0` (Highly Negative) to `+1.0` (Highly Positive) and segmented into discrete categorical buckets (Negative, Neutral, Positive).
- **Volume & Average Distribution**: From the aggregated dataset, the median sentiment skews neutral-to-negative for software services, but remains relatively robust for legacy hardware limits.
- **Target Extraction**: We algorithmically identified that *Sony PlayMemories Online* possessed the tightest cluster of low-performing sentiment nodes, mathematically marking it as a "Critical Remediation Target" compared to the high baseline of *Sony VAIO*.

---

## 3. Text Analysis (NLP & Verbatims)
Applying Natural Language Processing (NLP), we extracted the thematic essence from consumer text data:
- **Keyword Processing (Word Clouds)**: By removing standard stop-words and visualizing frequencies per product segment, we isolated the underlying drivers of sentiment.
- **Qualitative Verbatims (Extremes)**: The VADER algorithm confidently pinpointed the absolute highest and lowest performing raw reviews. 
    - *Negative Correlates*: Phrases and structural language focused on "software glitches", "discontinuation", and "poor tech support" heavily penalize the VADER score.
    - *Positive Correlates*: "Build quality", "longevity", and "classic design" routinely buoy average response ratings.

---

## 4. Graph Data Analysis
Visual analytics were applied to uncover hidden dimensions within the multi-variate dataset. Key graphical findings include:

1. **Volatility vs Text Length (Scatter Analysis)**
   When mapping Review Word Count against the final VADER Score, a clear funnel emerges. Data visualizations reveal that extreme emotional polarity (both highly negative and highly positive) is heavily clustered under **500 words**, indicating that extreme consumer passion translates to brief, highly concentrated bursts of text.

2. **Sentiment by Source Type (Bar Distribution)**
   Our visual model splits feedback by internal vs. external origination. The graph clearly dictates that **Official PlayStation / Sony Support platforms** manifest a significantly lower average sentiment score compared to external/third-party platforms (like Wikipedia/TechRadar). This analytically implies that consumers predominantly use internal channels solely for complaint escalation rather than general commentary.

3. **Product-Level Breakdown (Box Plots & Grouped Distributions)**
   The box plots dynamically map the variance of sentiment. The interquartile range (IQR) for *Sony VAIO* stretches deeply into the Positive quadrant compared to *PlayMemories* which suffers notable compression into the Negative domain, proving hardware longevity yields better historical sentiment than discontinued web services.

---

### Additional Deliverable:
Alongside this report, we have shipped a lightweight, real-time **Streamlit Data Dashboard** mapping these identical figures interactively for stakeholders.
