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

## 5. Text Analysis

Looking at the most common words in comments after discontinuation across all three products, themes around "too early," "ahead of its time," and "disappointed" appear frequently — especially for Google Glass. For Google+, many comments reference nostalgia and frustration over being forced to migrate to other platforms.

For Stadia, post-discontinuation comments are more mixed — some users expressed relief (they had already moved to other platforms), while others noted the wasted potential of the hardware.

---

## 6. Key Findings

- Consumer sentiment dropped significantly after the discontinuation of Google Glass and Google+ but not Stadia
- Google Glass comments show the highest average polarity before discontinuation, suggesting it had a more positive legacy reputation — which then dropped noticeably after shutdown
- Stadia's sentiment was already lower before discontinuation, possibly reflecting ongoing frustrations with the product during its lifetime
- Across all three products, sentiment stayed mostly in the neutral-to-slightly-positive range, with Google Glass showing the widest variance

---

## 7. Dashboard

A Streamlit dashboard (`app.py`) provides an interactive view of these findings, including sentiment breakdowns by product and time period, polarity distributions, and the t-test results.

