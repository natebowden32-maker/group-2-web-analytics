# Google Discontinued Products: Sentiment Analysis Report

## 1. Overview

This report analyzes how public sentiment toward three discontinued Google products changed over time, using YouTube comment data scraped before and after each product's shutdown. The three products are **Google Stadia**, **Google Glass**, and **Google+**.

The core research question: *Did consumer sentiment shift significantly after Google announced the discontinuation of these products?*

---

## 2. Data

YouTube comments were scraped for each product across two time windows — before discontinuation and after. After cleaning (removing duplicates, stripping URLs, filtering comments under 4 words), we ended up with approximately **3,248 usable comments** across all three products.

| Product | Before | After |
|---------|--------|-------|
| Google Stadia | 594 | 609 |
| Google Glass | 684 | 285 |
| Google+ | 669 | 407 |

---

## 3. Sentiment Scoring

Instead of VADER, we used **TextBlob** polarity scoring, which returns a continuous value between -1 (very negative) and +1 (very positive). Comments were labeled as:

- **Positive**: polarity > 0.05
- **Neutral**: -0.05 to 0.05
- **Negative**: polarity < -0.05

---

## 4. Statistical Analysis

We ran independent samples t-tests comparing mean polarity before vs. after discontinuation for each product.

| Product | Before Mean | After Mean | t-stat | p-value | Significant? |
|---------|------------|-----------|--------|---------|--------------|
| Stadia | 0.099 | 0.086 | 0.789 | 0.430 | No |
| Google Glass | 0.138 | 0.089 | 2.426 | 0.016 | Yes |
| Google+ | 0.119 | 0.072 | 2.404 | 0.016 | Yes |

**Google Glass** and **Google+** both show a statistically significant drop in sentiment after discontinuation (p < 0.05). **Stadia** does not show a significant change, which may be because Google offered full refunds to Stadia users, softening the negative reaction.

---

## 5. TF-IDF Keyword Analysis

We applied TF-IDF (Term Frequency–Inverse Document Frequency) with unigrams and bigrams to extract the most distinctive keywords per product per time period, using scikit-learn with custom stop words to reduce noise.

**Top keywords before vs. after discontinuation:**

| Product | Before (top terms) | After (top terms) |
|---------|-------------------|------------------|
| Google Stadia | gaming, internet, video, future, google stadia | games, remember, fail, cloud, service |
| Google Glass | google glass, vision, ahead time, future | remember, privacy, camera, tech, apple |
| Google+ | youtube, facebook, love, friends | remember, miss, social, used |

One of the most striking findings is that **"remember" appears as a top keyword after discontinuation for all three products** — ranking 6th for Stadia, 10th for Google Glass, and 1st for Google+. This reflects a strong nostalgic and retrospective tone in post-shutdown discussions.

Other notable keyword shifts include "fail" and "service" rising in Stadia comments after shutdown, "privacy" becoming prominent in Glass discussions (a concern that contributed to its discontinuation), and "miss" appearing in Google+ comments, indicating genuine attachment to the platform.

The keyword co-occurrence network (see `gephi_network_export.ipynb`) further visualizes how these terms cluster. Stadia's network centers around gaming/internet infrastructure, Glass's around vision technology and privacy, and Google+'s around social media comparisons with Facebook and YouTube.

---

## 6. Aspect-Based Sentiment Analysis (ABSA)

We used `langextract` with the Gemini API (gemini-2.5-flash) to run Aspect-Based Sentiment Analysis on a sample of 150 comments (25 per product per time period). We defined five aspects based on the most discussed themes in the data:

- **Product Quality** — hardware, features, reliability
- **Market Demand** — whether users wanted or needed the product
- **Adoption Ability** — ease of adoption, privacy concerns, social acceptance
- **Timing/Innovation** — whether the product was ahead of or behind its time
- **Price/Value** — cost relative to perceived value

The model extracted 268 sentiment triples total. Results by aspect:

| Aspect | Positive | Neutral | Negative |
|--------|----------|---------|----------|
| Product Quality | 36 | 11 | 77 |
| Market Demand | 13 | 10 | 38 |
| Adoption Ability | 19 | 5 | 27 |
| Timing/Innovation | 11 | 4 | 6 |
| Price/Value | 4 | 1 | 6 |

**Product Quality** was the most discussed aspect (124 mentions) and skewed heavily negative, with users criticizing hardware limitations, short battery life, and technical reliability. **Market Demand** was also predominantly negative, reflecting skepticism about whether these products addressed real consumer needs.

The only aspect with more positive than negative sentiment was **Timing/Innovation** — users frequently acknowledged that these products were ahead of their time, even if they ultimately failed commercially. This aligns with the TF-IDF finding that "ahead of its time" and "future" appear as top keywords in pre-discontinuation comments for Google Glass.

Few-shot examples including sarcasm handling were provided to the model to improve accuracy on ambiguous comments.

---

## 7. Key Findings

- Consumer sentiment dropped significantly after the discontinuation of Google Glass and Google+ but not Stadia (t-test, p < 0.05)
- Google Glass comments show the highest average polarity before discontinuation, suggesting it had a stronger positive legacy reputation — which then dropped noticeably after shutdown
- Stadia's sentiment was already lower before discontinuation, possibly reflecting ongoing frustrations with the product during its lifetime
- "Remember" is the single most consistent post-discontinuation keyword across all three products, pointing to nostalgia as a dominant emotional response
- Product Quality is the most criticized aspect across all products; Timing/Innovation is the only aspect with net positive sentiment
- Across all three products, sentiment stayed mostly in the neutral-to-slightly-positive range, with Google Glass showing the widest variance

---

## 8. Dashboard

A Streamlit dashboard (`app.py`) provides an interactive view of these findings, including sentiment breakdowns by product and time period, polarity distributions, t-test results, and ABSA aspect charts.
