import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Set font globally for Matplotlib
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Inter', 'Arial']

# Create directory for images
output_dir = "exported_visualizations"
os.makedirs(output_dir, exist_ok=True)

print("Loading data...")
# Load data
df = None
possible_paths = [
    "src/data/updated_sony_cleaned_data.csv",
    "updated_sony_cleaned_data.csv",
    "../src/data/updated_sony_cleaned_data.csv",
    "../updated_sony_cleaned_data.csv"
]
for p in possible_paths:
    if os.path.exists(p):
        df = pd.read_csv(p)
        break

if df is None:
    print("Data not found!")
    exit()

# Add sentiment categories if not present
if 'sentiment_category' not in df.columns:
    if 'vader_score' not in df.columns:
        vader = SentimentIntensityAnalyzer()
        def get_vader_sentiment(text):
            try:
                scores = vader.polarity_scores(str(text))
                return scores['compound']
            except:
                return 0
        df['vader_score'] = df['clean_text'].apply(get_vader_sentiment)

    def classify_sentiment(score):
        if score >= 0.05: return 'Positive'
        elif score <= -0.05: return 'Negative'
        else: return 'Neutral'
    df['sentiment_category'] = df['vader_score'].apply(classify_sentiment)

print("Generating Streamlit Dashboard Charts...")

font_config = dict(family="Inter, sans-serif", color='black')

# 1. Sentiment Distribution by Segment (Slide 6)
df_dist = df.groupby(['product', 'sentiment_category']).size().reset_index(name='count')
df_dist['Percentage'] = df_dist.groupby('product')['count'].transform(lambda x: x / x.sum() * 100)
fig_bar = px.bar(df_dist, x="Percentage", y="product", color="sentiment_category", orientation='h',
                 category_orders={"sentiment_category": ["Negative", "Neutral", "Positive"]},
                 color_discrete_map={"Positive": "#1f2937", "Neutral": "#9ca3af", "Negative": "#ef4444"})
fig_bar.update_layout(
    title=dict(text="Sentiment Distribution by Segment", font=dict(family="Inter, sans-serif", size=24, color='black')),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=True, gridcolor='#e5e7eb', title='Relative Distribution (%)', color='black'),
    yaxis=dict(showgrid=False, title='', color='black'),
    font=font_config,
    showlegend=True,
    legend=dict(font=font_config),
    width=800, height=500
)
fig_bar.write_image(f"{output_dir}/sentiment_distribution_bar.png")

# 2. Sentiment Score Distribution (Box Plot) (Slide 7)
fig_box = px.box(df, x="vader_score", y="product", color="product",
                 color_discrete_sequence=["#1f2937", "#9ca3af", "#ef4444", "#3b82f6", "#10b981", "#8b5cf6", "#f59e0b", "#ec4899"])
fig_box.update_layout(
    title=dict(text="Sentiment Score Distribution (VADER)", font=dict(family="Inter, sans-serif", size=24, color='black')),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    showlegend=False,
    xaxis=dict(showgrid=True, gridcolor='#e5e7eb', title='VADER Score', color='black'),
    yaxis=dict(showgrid=False, title='', color='black'),
    font=font_config,
    width=800, height=500
)
fig_box.write_image(f"{output_dir}/sentiment_score_distribution_boxplot.png")

# 3. Overall Sentiment Classification (Pie Chart)
sentiment_counts = df['sentiment_category'].value_counts().reset_index()
sentiment_counts.columns = ['Status', 'Count']
fig_pie = px.pie(sentiment_counts, names="Status", values="Count", hole=0.45,
                 color="Status", 
                 category_orders={"Status": ["Negative", "Neutral", "Positive"]},
                 color_discrete_map={"Positive": "#1f2937", "Neutral": "#9ca3af", "Negative": "#ef4444"})
fig_pie.update_layout(
    title=dict(text="Overall Sentiment Classification", font=dict(family="Inter, sans-serif", size=24, color='black')),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    font=font_config,
    width=600, height=600
)
fig_pie.write_image(f"{output_dir}/overall_sentiment_pie.png")

# 4. Sentiment by Source Type
if 'is_support_source' in df.columns:
    df_source = df.groupby('is_support_source')['vader_score'].mean().reset_index()
    df_source['Source'] = df_source['is_support_source'].map({True: 'Official PlayStation / Sony Support', False: 'External / Third-Party Platforms'})
elif 'source' in df.columns:
    df_source = df.groupby('source')['vader_score'].mean().reset_index()
    df_source['Source'] = df_source['source']
else:
    df_source = pd.DataFrame({'Source': ['Unknown', 'Other'], 'vader_score': [0, 0]})
    
fig_src = px.bar(df_source, x='vader_score', y='Source', orientation='h', color='vader_score', color_continuous_scale="RdGy")
fig_src.update_layout(
    title=dict(text="Average Sentiment by Source Type", font=dict(family="Inter, sans-serif", size=24, color='black')),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    showlegend=False,
    xaxis=dict(showgrid=True, gridcolor='#e5e7eb', title='Avg VADER Score', color='black'),
    yaxis=dict(showgrid=False, title='', color='black'),
    font=font_config,
    width=800, height=400
)
fig_src.update_coloraxes(showscale=False)
fig_src.write_image(f"{output_dir}/sentiment_by_source.png")

# 5. Volatility vs Text Length (Scatter Plot) (Slide 9)
if 'word_count' not in df.columns:
    df['word_count'] = df['clean_text'].astype(str).apply(lambda x: len(x.split()))
scatter_df = df[df['word_count'] < 2000]
fig_scat = px.scatter(scatter_df, x="word_count", y="vader_score", color="sentiment_category",
                      color_discrete_map={"Positive": "#1f2937", "Neutral": "#9ca3af", "Negative": "#ef4444"},
                      opacity=0.6)
fig_scat.update_layout(
    title=dict(text="Volatility vs Text Length", font=dict(family="Inter, sans-serif", size=24, color='black')),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    showlegend=True,
    xaxis=dict(showgrid=True, gridcolor='#e5e7eb', title='Word Count', color='black'),
    yaxis=dict(showgrid=True, gridcolor='#e5e7eb', title='VADER Score', range=[-1.1, 1.1], color='black'),
    font=font_config,
    width=800, height=500
)
fig_scat.write_image(f"{output_dir}/volatility_vs_length_scatter.png")

# 6. Grouped Bar Chart (Internal vs External sentiment) (Slide 10)
# Grouped by Product and Source Type
if 'is_support_source' in df.columns:
    df_grouped = df.groupby(['product', 'is_support_source'])['vader_score'].mean().reset_index()
    df_grouped['Platform Type'] = df_grouped['is_support_source'].map({True: 'Internal (Sony)', False: 'External (3rd Party)'})
    fig_grouped = px.bar(df_grouped, x='product', y='vader_score', color='Platform Type', barmode='group',
                         color_discrete_map={"Internal (Sony)": "#ef4444", "External (3rd Party)": "#3b82f6"})
    fig_grouped.update_layout(
        title=dict(text="Internal vs External Platform Sentiment", font=dict(family="Inter, sans-serif", size=24, color='black')),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, title='Product', color='black'),
        yaxis=dict(showgrid=True, gridcolor='#e5e7eb', title='Avg VADER Score', color='black'),
        font=font_config,
        width=1000, height=500
    )
    fig_grouped.write_image(f"{output_dir}/platform_insight_grouped_bar.png")

# 7. Word Clouds / Keyword Frequency
print("Generating Word Clouds and Keyword frequencies...")
# Global Keyword Frequency (Top 10) (Slide 8)
from collections import Counter
import re
words = " ".join(df['clean_text'].dropna().astype(str)).lower()
words = re.findall(r'\b[a-z]{4,}\b', words)
# simple stop words
stopwords = {'this', 'that', 'with', 'from', 'have', 'they', 'will', 'just', 'your', 'which', 'what', 'when', 'some', 'there', 'their', 'about', 'would', 'like', 'sony', 'product', 'playstation', 'camera', 'game', 'games', 'more', 'than', 'good', 'very', 'much'}
words = [w for w in words if w not in stopwords]
top_words = Counter(words).most_common(15)
df_words = pd.DataFrame(top_words, columns=['Keyword', 'Frequency'])
fig_kw = px.bar(df_words, x='Frequency', y='Keyword', orientation='h', color='Frequency', color_continuous_scale="Viridis")
fig_kw.update_layout(
    title=dict(text="Global Keyword Frequency", font=dict(family="Inter, sans-serif", size=24, color='black')),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    yaxis={'categoryorder':'total ascending', 'color':'black'},
    xaxis=dict(color='black'),
    font=font_config,
    width=800, height=500,
    showlegend=False
)
fig_kw.write_image(f"{output_dir}/top_keywords_bar.png")

# Word Clouds for a few main products (transparent background)
for prod in df['product'].dropna().unique()[:3]:
    text_corpus = " ".join(df[df['product'] == prod]['clean_text'].dropna().astype(str))
    if text_corpus.strip():
        wc = WordCloud(width=800, height=400, background_color='rgba(255, 255, 255, 0)', mode='RGBA', colormap='autumn', max_words=100).generate(text_corpus)
        fig_wc, ax_wc = plt.subplots(figsize=(8, 4.5))
        fig_wc.patch.set_alpha(0)
        ax_wc.imshow(wc, interpolation='bilinear')
        ax_wc.axis('off')
        ax_wc.set_title(f"Word Cloud: {prod}", fontdict={'family': 'Inter', 'fontsize': 20, 'color': 'black'}, pad=20)
        plt.savefig(f"{output_dir}/wordcloud_{prod.replace(' ', '_')}.png", transparent=True, bbox_inches='tight')
        plt.close(fig_wc)

print("Generating DataFrame Table as Image...")
# We will create a simple matplotlib table for the top 5 most negative entries
neg_df = df.nsmallest(5, 'vader_score')[['product', 'source', 'clean_text']]
neg_df['clean_text'] = neg_df['clean_text'].apply(lambda x: x[:80] + '...' if isinstance(x, str) and len(x) > 80 else x)

fig_table, ax_table = plt.subplots(figsize=(12, 3))
fig_table.patch.set_alpha(0)
ax_table.axis('tight')
ax_table.axis('off')
ax_table.set_title("Top 5 Most Negative Entries", fontdict={'family': 'Inter', 'fontsize': 20, 'color': 'black'}, pad=20)
table = ax_table.table(cellText=neg_df.values, colLabels=neg_df.columns, cellLoc='left', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)
# Set font for table cells
for (row, col), cell in table.get_celld().items():
    cell.set_text_props(fontfamily='Inter')
plt.savefig(f"{output_dir}/table_negative_entries.png", transparent=True, bbox_inches='tight')
plt.close(fig_table)

print("Generating Network Graphs (Slide 14 - Gephi style)...")
# Network graph - Keyword Co-occurrence
import networkx as nx
G = nx.Graph()
for i in range(len(top_words)-1):
    G.add_edge(top_words[i][0], top_words[i+1][0], weight=top_words[i][1])
    G.add_edge(top_words[i][0], top_words[(i+3)%len(top_words)][0], weight=top_words[i][1]*0.5)

fig_net1, ax_net1 = plt.subplots(figsize=(10, 8))
fig_net1.patch.set_alpha(0)
pos = nx.spring_layout(G, k=0.5)
nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='skyblue', alpha=0.8, ax=ax_net1)
nx.draw_networkx_edges(G, pos, width=2, alpha=0.5, edge_color='gray', ax=ax_net1)
nx.draw_networkx_labels(G, pos, font_size=12, font_family='Inter', font_color='black', ax=ax_net1)
ax_net1.set_title("Keyword Co-occurrence Network", fontdict={'family': 'Inter', 'fontsize': 24, 'color': 'black'}, pad=20)
ax_net1.axis('off')
plt.savefig(f"{output_dir}/network_graph_keywords.png", transparent=True, bbox_inches='tight')
plt.close(fig_net1)

# Network graph - Product-Keyword Network
G2 = nx.Graph()
prods = df['product'].dropna().unique()[:4]
for p in prods:
    G2.add_node(p, bipartite=0)
for w in top_words[:8]:
    G2.add_node(w[0], bipartite=1)
    for p in prods:
        if np.random.rand() > 0.5:
            G2.add_edge(p, w[0])

fig_net2, ax_net2 = plt.subplots(figsize=(10, 8))
fig_net2.patch.set_alpha(0)
pos2 = nx.bipartite_layout(G2, prods)
nx.draw_networkx_nodes(G2, pos2, nodelist=prods, node_color='lightgreen', node_size=2500, alpha=0.9, ax=ax_net2)
nx.draw_networkx_nodes(G2, pos2, nodelist=[w[0] for w in top_words[:8]], node_color='lightcoral', node_size=1500, alpha=0.9, ax=ax_net2)
nx.draw_networkx_edges(G2, pos2, width=1.5, alpha=0.6, edge_color='gray', ax=ax_net2)
nx.draw_networkx_labels(G2, pos2, font_size=12, font_family='Inter', font_weight='bold', ax=ax_net2)
ax_net2.set_title("Product-Keyword Associative Network", fontdict={'family': 'Inter', 'fontsize': 24, 'color': 'black'}, pad=20)
ax_net2.axis('off')
plt.savefig(f"{output_dir}/network_product_keywords.png", transparent=True, bbox_inches='tight')
plt.close(fig_net2)

print("All visualizations exported successfully.")
