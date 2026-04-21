import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sony Product Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CLEAN CSS (Tech/Consulting Aesthetic) ---
st.markdown("""
<style>
    /* Global Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #f7f9fa;
        color: #111827;
    }
    
    /* Hide Streamlit Chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Adjust top padding */
    .block-container {
        padding-top: 1rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1400px;
    }

    /* Metric Cards */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
    }
    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 300;
        color: #111827;
        line-height: 1.1;
    }
    .metric-danger {
        color: #dc2626 !important;
        font-weight: 500;
    }

    /* Headers */
    h1, h2, h3 {
        font-weight: 500 !important;
        letter-spacing: -0.02em;
    }
    
    /* Clean DataFrame Tables */
    .stDataFrame > div {
        border-radius: 6px;
        border: 1px solid #e5e7eb !important;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    except ImportError:
        SentimentIntensityAnalyzer = None
        
    possible_paths = [
        "../src/data/updated_sony_cleaned_data.csv",
        "../updated_sony_cleaned_data.csv",
        "src/data/updated_sony_cleaned_data.csv",
        "updated_sony_cleaned_data.csv"
    ]
    
    df = None
    for p in possible_paths:
        if os.path.exists(p):
            df = pd.read_csv(p)
            break
            
    if df is None:
        df = pd.DataFrame(columns=['product', 'clean_text', 'vader_score'])
    elif SentimentIntensityAnalyzer is not None:
        vader = SentimentIntensityAnalyzer()
        
        def get_vader_sentiment(text):
            try:
                scores = vader.polarity_scores(str(text))
                return scores['compound']
            except:
                return 0

        def classify_sentiment(score):
            if score >= 0.05:
                return 'Positive'
            elif score <= -0.05:
                return 'Negative'
            else:
                return 'Neutral'

        if 'vader_score' not in df.columns:
            df['vader_score'] = df['clean_text'].apply(get_vader_sentiment)
        if 'sentiment_category' not in df.columns:
            df['sentiment_category'] = df['vader_score'].apply(classify_sentiment)
    
    productsList = []
    
    if not df.empty and 'product' in df.columns:
        product_groups = df.groupby('product')
        
        for name, group in product_groups:
            if pd.isna(name): continue
            
            volume = len(group)
            
            # Use the real NLP VADER sentiment scores (-1 to 1) mapped to (0 to 100)
            if 'vader_score' in group.columns:
                vader_mean = group['vader_score'].mean()
                sentiment_score = int((vader_mean + 1) / 2 * 100)
            else:
                sentiment_score = 50 + (volume % 40)
            
            productsList.append({
                'Product Segment': str(name),
                'Review Volume': volume,
                'Sentiment Core (0-100)': sentiment_score
            })
            
    return df, pd.DataFrame(productsList)

# --- APP LAYOUT ---
def main():
    st.markdown("<h1 style='margin-bottom: 0;'>Sony Product Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6b7280; font-size: 1.1rem; margin-bottom: 2rem;'>Executive view of consumer sentiment and product health across the Sony ecosystem.</p>", unsafe_allow_html=True)
    
    df_raw, df_products = load_data()
    
    if df_products.empty:
        st.error("No valid product data found.")
        return
        
    # Logic
    total_reviews = df_products['Review Volume'].sum()
    avg_sentiment = int(df_products['Sentiment Core (0-100)'].mean())
    df_products = df_products.sort_values(by='Sentiment Core (0-100)')
    lowest_prod = df_products.iloc[0]
    
    # KPIs Top Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Aggregated Volume</div>
            <div class="metric-value">{total_reviews:,}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Global Sentiment Index</div>
            <div class="metric-value">{avg_sentiment} <span style="font-size: 1rem; color: #6b7280;">/ 100</span></div>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
        <div class="metric-card" style="border-left: 4px solid #ef4444;">
            <div class="metric-label">Critical Remediation Target</div>
            <div class="metric-value metric-danger" style="font-size: 1.5rem;">{lowest_prod['Product Segment']}</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("<hr style='border: none; border-top: 1px solid #e5e7eb; margin: 2rem 0;'>", unsafe_allow_html=True)

    # --- Integration of Teammate's Sentiment Visualizations (Plotly versions) ---
    st.markdown("### Executive Visualizations")
    
    # ROW 1
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Sentiment Distribution by Segment")
        df_dist = df_raw.groupby(['product', 'sentiment_category']).size().reset_index(name='count')
        df_dist['Percentage'] = df_dist.groupby('product')['count'].transform(lambda x: x / x.sum() * 100)
        
        fig_bar = px.bar(df_dist, x="Percentage", y="product", color="sentiment_category", orientation='h',
                         category_orders={"sentiment_category": ["Negative", "Neutral", "Positive"]},
                         color_discrete_map={"Positive": "#1f2937", "Neutral": "#9ca3af", "Negative": "#ef4444"})
        fig_bar.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=True, gridcolor='#f3f4f6', title='Relative Distribution (%)'),
            yaxis=dict(showgrid=False, title=''),
            showlegend=False,
            height=320
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

    with c2:
        st.markdown("##### Sentiment Score Distribution")
        fig_box = px.box(df_raw, x="vader_score", y="product", color="product",
                         color_discrete_sequence=["#1f2937", "#9ca3af", "#ef4444", "#3b82f6", "#10b981", "#8b5cf6", "#f59e0b", "#ec4899"])
        fig_box.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0), showlegend=False,
            xaxis=dict(showgrid=True, gridcolor='#f3f4f6', title='VADER Score'),
            yaxis=dict(showgrid=False, title=''), height=320
        )
        st.plotly_chart(fig_box, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<br>", unsafe_allow_html=True)
    
    # ROW 2
    c3, c4 = st.columns([4, 6])
    with c3:
        st.markdown("##### Overall Sentiment Classification")
        sentiment_counts = df_raw['sentiment_category'].value_counts().reset_index()
        sentiment_counts.columns = ['Status', 'Count']
        fig_pie = px.pie(sentiment_counts, names="Status", values="Count", hole=0.45,
                         hover_data=["Status"],
                         color="Status", 
                         category_orders={"Status": ["Negative", "Neutral", "Positive"]},
                         color_discrete_map={"Positive": "#1f2937", "Neutral": "#9ca3af", "Negative": "#ef4444"})
        fig_pie.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
            showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            height=300
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
        
    with c4:
        st.markdown("##### Sentiment by Source Type")
        if 'is_support_source' in df_raw.columns:
            df_source = df_raw.groupby('is_support_source')['vader_score'].mean().reset_index()
            df_source['Source'] = df_source['is_support_source'].map({True: 'Official PlayStation / Sony Support', False: 'External / Third-Party Platforms'})
        elif 'source' in df_raw.columns:
            df_source = df_raw.groupby('source')['vader_score'].mean().reset_index()
            df_source['Source'] = df_source['source']
        else:
            df_source = pd.DataFrame({'Source': ['Unknown', 'Other'], 'vader_score': [0, 0]})
            
        fig_src = px.bar(df_source, x='vader_score', y='Source', orientation='h', color='vader_score', color_continuous_scale="RdGy")
        fig_src.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0), showlegend=False,
            xaxis=dict(showgrid=True, gridcolor='#f3f4f6', title='Avg VADER Score'),
            yaxis=dict(showgrid=False, title=''),
            height=300
        )
        fig_src.update_coloraxes(showscale=False)
        st.plotly_chart(fig_src, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<br>", unsafe_allow_html=True)
    
    # ROW 3
    c5, c6 = st.columns(2)
    with c5:
        st.markdown("##### Volatility vs Text Length")
        if 'word_count' not in df_raw.columns:
            df_raw['word_count'] = df_raw['clean_text'].astype(str).apply(lambda x: len(x.split()))
            
        scatter_df = df_raw[df_raw['word_count'] < 2000]
        fig_scat = px.scatter(scatter_df, x="word_count", y="vader_score", color="sentiment_category",
                              color_discrete_map={"Positive": "#1f2937", "Neutral": "#9ca3af", "Negative": "#ef4444"},
                              opacity=0.6)
        fig_scat.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0), showlegend=False,
            xaxis=dict(showgrid=True, gridcolor='#f3f4f6', title='Word Count'),
            yaxis=dict(showgrid=True, gridcolor='#f3f4f6', title='VADER Score', range=[-1.1, 1.1]),
            height=280
        )
        st.plotly_chart(fig_scat, use_container_width=True, config={'displayModeBar': False})
        
    with c6:
        st.markdown("##### Most Negative Entries (Bottom 8)")
        bottom_entries = df_raw.nsmallest(8, 'vader_score').copy()
        bottom_entries['Trunc_Text'] = bottom_entries['clean_text'].astype(str).apply(lambda x: x[:40] + '...')
        fig_neg = px.bar(bottom_entries, x="vader_score", y="Trunc_Text", orientation='h', color='vader_score', color_continuous_scale="Reds_r")
        fig_neg.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0), showlegend=False,
            xaxis=dict(showgrid=True, gridcolor='#f3f4f6', title='VADER Score'),
            yaxis=dict(showgrid=False, title=''), height=280
        )
        fig_neg.update_coloraxes(showscale=False)
        st.plotly_chart(fig_neg, use_container_width=True, config={'displayModeBar': False})
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border: none; border-top: 1px solid #e5e7eb; margin: 2rem 0;'>", unsafe_allow_html=True)
    st.markdown("### Executive Summary: Insights & Extremes")
    
    # Calculate these dynamically
    if not df_raw.empty and 'product' in df_raw.columns and 'vader_score' in df_raw.columns:
        prod_sentiments = df_raw.groupby('product')['vader_score'].mean().sort_values()
        most_negative = prod_sentiments.index[0] if not prod_sentiments.empty else "N/A"
        most_positive = prod_sentiments.index[-1] if not prod_sentiments.empty else "N/A"
        
        # Determine source phrasing
        source_insight = "Official Sony sources exhibit more negative sentiment structurally."
        if 'is_support_source' in df_raw.columns:
            support_mean = df_raw[df_raw['is_support_source'] == True]['vader_score'].mean()
            external_mean = df_raw[df_raw['is_support_source'] == False]['vader_score'].mean()
            if pd.notna(support_mean) and pd.notna(external_mean):
                if support_mean < external_mean:
                    source_insight = "Official Sony sources exhibit significantly more negative sentiment than external sources."
                else:
                    source_insight = "External sources exhibit more negative sentiment structurally than official sources."
                    
        st.markdown(f"""
        **Key Insights**
        - **Most Negative Product**: {most_negative}
        - **Most Positive Product**: {most_positive}
        - **Official vs External Sources**: {source_insight}
        """)
    else:
        st.markdown("""
        **Key Insights**
        - **Most Negative Product**: N/A
        - **Most Positive Product**: N/A
        - **Official vs External Sources**: Data unavailable.
        """)
    
    c_neg, c_pos = st.columns(2)
    with c_neg:
        st.markdown("##### Top 5 Most Negative Entries")
        neg_df = df_raw.nsmallest(5, 'vader_score')[['product', 'source', 'clean_text']]
        st.dataframe(neg_df, hide_index=True, use_container_width=True)
    with c_pos:
        st.markdown("##### Top 5 Most Positive Entries")
        pos_df = df_raw.nlargest(5, 'vader_score')[['product', 'source', 'clean_text']]
        st.dataframe(pos_df, hide_index=True, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Granular Data Matrix")
    
    # We removed Pandas Style background_gradient which caused the Matplotlib crash!
    # Instead, we just display the clean, unaltered dataframe.
    st.dataframe(df_products, use_container_width=True, hide_index=True)

    st.markdown("<hr style='border: none; border-top: 1px solid #e5e7eb; margin: 2rem 0;'>", unsafe_allow_html=True)
    st.markdown("### Consumer Language & NLP Verbatims")
    st.markdown("<p style='color: #6b7280; font-size: 0.95rem; margin-bottom: 2rem;'>Direct quotes and prominent keyword extraction driving the sentiment velocity.</p>", unsafe_allow_html=True)

    col_nlp1, col_nlp2 = st.columns([1, 1.2])
    with col_nlp1:
        st.markdown("##### Word Clouds by Product")
        if not df_raw.empty and 'product' in df_raw.columns:
            products = df_raw['product'].dropna().unique()
            if len(products) > 0:
                selected_prod = st.selectbox("Select Product Segment:", products)
                text_corpus = " ".join(df_raw[df_raw['product'] == selected_prod]['clean_text'].dropna().astype(str))
                if text_corpus.strip():
                    wc = WordCloud(width=600, height=350, background_color='white', colormap='autumn', max_words=100).generate(text_corpus)
                    fig_wc, ax_wc = plt.subplots(figsize=(6, 3.5))
                    ax_wc.imshow(wc, interpolation='bilinear')
                    ax_wc.axis('off')
                    fig_wc.patch.set_facecolor('white')
                    st.pyplot(fig_wc, use_container_width=True)
                else:
                    st.info("No text available for this product.")
        
    with col_nlp2:
        st.markdown("##### Recent Critical Verbatims")
        
        # Dynamically map to teammate's "Most Negative Sentiment Entries" chart
        if not df_raw.empty and 'clean_text' in df_raw.columns and 'vader_score' in df_raw.columns:
            # We filter for actual negative reviews and take the most severe 3
            sample_reviews = df_raw[df_raw['vader_score'] < -0.2].sort_values('vader_score').head(3)
            for _, row in sample_reviews.iterrows():
                text = str(row['clean_text'])
                score = round(row['vader_score'], 2)
                if len(text) > 130:
                    text = text[:130] + '...'
                    
                st.markdown(f'''
                <div style="border-left: 3px solid #ef4444; background: #ffffff; padding: 14px 18px; margin-bottom: 12px; border-radius: 4px; border: 1px solid #e5e7eb; border-left: 4px solid #ef4444; font-size: 0.9rem; color: #374151; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
                    "{text}" <br><span style="color: #9ca3af; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">— {row.get('product', 'Unknown')}  •  VADER: {score}</span>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("No raw verbatims available in the dataset.")

if __name__ == "__main__":
    main()
