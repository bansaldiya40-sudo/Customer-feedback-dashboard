import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from textblob import TextBlob
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Customer Feedback Dashboard",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main { background-color: #0f1117; }

    .stApp {
        background: linear-gradient(135deg, #0f1117 0%, #1a1f2e 100%);
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1e2235 0%, #252b3d 100%);
        border: 1px solid #2d3550;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 24px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-2px); }
    .metric-value {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6c63ff, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #8892b0;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-top: 6px;
    }
    .metric-delta {
        font-size: 0.8rem;
        margin-top: 4px;
    }

    /* Section headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ccd6f6;
        letter-spacing: 0.04em;
        margin-bottom: 4px;
        border-left: 3px solid #6c63ff;
        padding-left: 12px;
    }

    /* Sentiment badges */
    .badge-positive { background:#0d3d2e; color:#34d399; border-radius:8px; padding:3px 10px; font-size:0.78rem; font-weight:600; }
    .badge-negative { background:#3d0d0d; color:#f87171; border-radius:8px; padding:3px 10px; font-size:0.78rem; font-weight:600; }
    .badge-neutral  { background:#1e2235; color:#94a3b8; border-radius:8px; padding:3px 10px; font-size:0.78rem; font-weight:600; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #141824 0%, #1a1f2e 100%);
        border-right: 1px solid #2d3550;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] h2, h3 {
        color: #ccd6f6 !important;
    }

    /* Feedback table rows */
    .feedback-row {
        background: #1e2235;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
        border-left: 4px solid #6c63ff;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #1a1f2e;
        border-radius: 10px;
        gap: 4px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #8892b0;
        border-radius: 8px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: #6c63ff !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── Helper: Plotly dark theme ───────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#ccd6f6", size=12),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(bgcolor="rgba(30,34,53,0.8)", bordercolor="#2d3550", borderwidth=1),
    xaxis=dict(gridcolor="#2d3550", zerolinecolor="#2d3550"),
    yaxis=dict(gridcolor="#2d3550", zerolinecolor="#2d3550"),
)

COLOR_SCALE = ["#6c63ff", "#a78bfa", "#34d399", "#f59e0b", "#f87171", "#60a5fa"]

# ─── Sentiment Analysis ──────────────────────────────────────────────────────
def analyze_sentiment(text):
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"
    return polarity, subjectivity, label

# ─── Load & Process Data ─────────────────────────────────────────────────────
@st.cache_data
def load_data(uploaded=None):
    if uploaded is not None:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv("data/feedback.csv")

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.strftime("%b %Y")
    df["month_num"] = df["date"].dt.to_period("M").astype(str)

    results = df["feedback"].apply(analyze_sentiment)
    df["polarity"]     = [r[0] for r in results]
    df["subjectivity"] = [r[1] for r in results]
    df["sentiment"]    = [r[2] for r in results]
    return df

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💬 Feedback Dashboard")
    st.markdown("---")

    uploaded_file = st.file_uploader("📂 Upload CSV", type=["csv"])
    df_raw = load_data(uploaded_file)

    st.markdown("### Filters")
    categories = ["All"] + sorted(df_raw["category"].unique().tolist())
    sel_category = st.selectbox("Category", categories)

    sentiments = ["All", "Positive", "Neutral", "Negative"]
    sel_sentiment = st.selectbox("Sentiment", sentiments)

    rating_range = st.slider("Rating Range", 1, 5, (1, 5))

    date_min = df_raw["date"].min().date()
    date_max = df_raw["date"].max().date()
    date_range = st.date_input("Date Range", value=(date_min, date_max), min_value=date_min, max_value=date_max)

    st.markdown("---")
    st.markdown("### About")
    st.caption("Sentiment analysis powered by **TextBlob**. Charts built with **Plotly**. Dashboard via **Streamlit**.")

# ─── Filter Data ─────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_category != "All":
    df = df[df["category"] == sel_category]
if sel_sentiment != "All":
    df = df[df["sentiment"] == sel_sentiment]
df = df[df["rating"].between(rating_range[0], rating_range[1])]
if len(date_range) == 2:
    df = df[(df["date"].dt.date >= date_range[0]) & (df["date"].dt.date <= date_range[1])]

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("<h1 style='color:#ccd6f6;font-size:2rem;font-weight:700;margin-bottom:4px;'>Customer Feedback Dashboard</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:#8892b0;font-size:0.9rem;'>Analyzing <b style='color:#a78bfa'>{len(df)}</b> reviews · Sentiment powered by TextBlob</p>", unsafe_allow_html=True)
st.markdown("---")

# ─── KPI Metrics ─────────────────────────────────────────────────────────────
total   = len(df)
avg_rat = df["rating"].mean() if total else 0
pos_pct = (df["sentiment"] == "Positive").sum() / total * 100 if total else 0
neg_pct = (df["sentiment"] == "Negative").sum() / total * 100 if total else 0
avg_pol = df["polarity"].mean() if total else 0

c1, c2, c3, c4, c5 = st.columns(5)
for col, val, label, delta in [
    (c1, total, "Total Reviews", ""),
    (c2, f"{avg_rat:.1f} ★", "Avg Rating", ""),
    (c3, f"{pos_pct:.0f}%", "Positive", f"<span style='color:#34d399'>▲ Positive</span>"),
    (c4, f"{neg_pct:.0f}%", "Negative", f"<span style='color:#f87171'>▼ Negative</span>"),
    (c5, f"{avg_pol:.2f}", "Avg Polarity", ""),
]:
    col.markdown(f"""
    <div class='metric-card'>
        <p class='metric-value'>{val}</p>
        <p class='metric-label'>{label}</p>
        <p class='metric-delta'>{delta}</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Tabs ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "😊 Sentiment", "📅 Trends", "📝 Reviews"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.markdown("<p class='section-header'>Rating Distribution</p>", unsafe_allow_html=True)
        rating_counts = df["rating"].value_counts().sort_index()
        fig_rat = px.bar(
            x=rating_counts.index, y=rating_counts.values,
            labels={"x": "Star Rating", "y": "Count"},
            color=rating_counts.values,
            color_continuous_scale=["#f87171", "#f59e0b", "#34d399"],
            text=rating_counts.values,
        )
        fig_rat.update_traces(textposition="outside", marker_line_width=0)
        fig_rat.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False,
                              xaxis_title="Star Rating", yaxis_title="Number of Reviews")
        st.plotly_chart(fig_rat, use_container_width=True)

    with col_r:
        st.markdown("<p class='section-header'>Reviews by Category</p>", unsafe_allow_html=True)
        cat_counts = df["category"].value_counts()
        fig_cat = px.pie(
            values=cat_counts.values, names=cat_counts.index,
            color_discrete_sequence=COLOR_SCALE, hole=0.55,
        )
        fig_cat.update_traces(textposition="outside", textinfo="label+percent",
                              marker=dict(line=dict(color="#0f1117", width=2)))
        fig_cat.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("<p class='section-header'>Average Rating per Category</p>", unsafe_allow_html=True)
    avg_by_cat = df.groupby("category")["rating"].mean().sort_values(ascending=True)
    fig_hbar = px.bar(
        x=avg_by_cat.values, y=avg_by_cat.index, orientation="h",
        color=avg_by_cat.values,
        color_continuous_scale=["#f87171", "#f59e0b", "#34d399"],
        text=[f"{v:.1f}" for v in avg_by_cat.values],
   )
    fig_hbar.update_layout(**{k: v for k, v in PLOTLY_LAYOUT.items() if k not in ("xaxis", "yaxis")},
                           coloraxis_showscale=False,
                           xaxis=dict(range=[0, 5.5], gridcolor="#2d3550", color="#ccd6f6"),
                           yaxis=dict(gridcolor="#2d3550", color="#ccd6f6"))
    st.plotly_chart(fig_hbar, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — SENTIMENT
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.markdown("<p class='section-header'>Sentiment Breakdown</p>", unsafe_allow_html=True)
        sent_counts = df["sentiment"].value_counts()
        colors_sent = {"Positive": "#34d399", "Neutral": "#94a3b8", "Negative": "#f87171"}
        fig_sent = px.bar(
            x=sent_counts.index, y=sent_counts.values,
            color=sent_counts.index,
            color_discrete_map=colors_sent,
            text=sent_counts.values,
        )
        fig_sent.update_traces(textposition="outside", marker_line_width=0)
        fig_sent.update_layout(**PLOTLY_LAYOUT, showlegend=False,
                               xaxis_title="Sentiment", yaxis_title="Count")
        st.plotly_chart(fig_sent, use_container_width=True)

    with col_r:
        st.markdown("<p class='section-header'>Polarity vs Subjectivity</p>", unsafe_allow_html=True)
        fig_scatter = px.scatter(
            df, x="polarity", y="subjectivity",
            color="sentiment", size="rating",
            color_discrete_map=colors_sent,
            hover_data=["customer_name", "category", "rating", "feedback"],
            opacity=0.8,
        )
        fig_scatter.update_layout(**PLOTLY_LAYOUT,
                                  xaxis_title="Polarity (negative ← → positive)",
                                  yaxis_title="Subjectivity (objective ← → subjective)")
        fig_scatter.add_vline(x=0, line_dash="dot", line_color="#2d3550")
        fig_scatter.add_hline(y=0.5, line_dash="dot", line_color="#2d3550")
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("<p class='section-header'>Sentiment by Category (Stacked)</p>", unsafe_allow_html=True)
    sent_cat = df.groupby(["category", "sentiment"]).size().reset_index(name="count")
    fig_stack = px.bar(
        sent_cat, x="category", y="count", color="sentiment",
        color_discrete_map=colors_sent, barmode="stack",
        text="count",
    )
    fig_stack.update_traces(textposition="inside")
    fig_stack.update_layout(**PLOTLY_LAYOUT, xaxis_title="", yaxis_title="Count")
    st.plotly_chart(fig_stack, use_container_width=True)

    st.markdown("<p class='section-header'>Polarity Distribution</p>", unsafe_allow_html=True)
    fig_hist = px.histogram(
        df, x="polarity", nbins=20,
        color_discrete_sequence=["#6c63ff"],
        opacity=0.85,
    )
    fig_hist.update_layout(**PLOTLY_LAYOUT, xaxis_title="Polarity Score", yaxis_title="Frequency")
    st.plotly_chart(fig_hist, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — TRENDS
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    monthly = df.groupby("month_num").agg(
        avg_rating=("rating", "mean"),
        count=("rating", "count"),
        avg_polarity=("polarity", "mean"),
    ).reset_index().sort_values("month_num")

    st.markdown("<p class='section-header'>Monthly Review Volume & Avg Rating</p>", unsafe_allow_html=True)
    fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
    fig_dual.add_trace(go.Bar(
        x=monthly["month_num"], y=monthly["count"],
        name="Review Count", marker_color="#6c63ff", opacity=0.7,
    ), secondary_y=False)
    fig_dual.add_trace(go.Scatter(
        x=monthly["month_num"], y=monthly["avg_rating"],
        name="Avg Rating", mode="lines+markers",
        line=dict(color="#34d399", width=3),
        marker=dict(size=8, color="#34d399"),
    ), secondary_y=True)
    fig_dual.update_layout(**PLOTLY_LAYOUT)
    fig_dual.update_yaxes(title_text="Review Count", secondary_y=False,
                          gridcolor="#2d3550", color="#ccd6f6")
    fig_dual.update_yaxes(title_text="Avg Rating", secondary_y=True,
                          range=[0, 5.5], gridcolor="rgba(0,0,0,0)", color="#34d399")
    st.plotly_chart(fig_dual, use_container_width=True)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("<p class='section-header'>Polarity Trend Over Time</p>", unsafe_allow_html=True)
        fig_pol = px.line(
            monthly, x="month_num", y="avg_polarity",
            markers=True,
            color_discrete_sequence=["#a78bfa"],
        )
        fig_pol.add_hline(y=0, line_dash="dot", line_color="#f87171")
        fig_pol.update_layout(**PLOTLY_LAYOUT, xaxis_title="Month", yaxis_title="Avg Polarity")
        st.plotly_chart(fig_pol, use_container_width=True)

    with col_r:
        st.markdown("<p class='section-header'>Sentiment Over Time (Area)</p>", unsafe_allow_html=True)
        sent_time = df.groupby(["month_num", "sentiment"]).size().reset_index(name="count").sort_values("month_num")
        fig_area = px.area(
            sent_time, x="month_num", y="count", color="sentiment",
            color_discrete_map={"Positive": "#34d399", "Neutral": "#94a3b8", "Negative": "#f87171"},
        )
        fig_area.update_layout(**PLOTLY_LAYOUT, xaxis_title="Month", yaxis_title="Count")
        st.plotly_chart(fig_area, use_container_width=True)

    st.markdown("<p class='section-header'>Rating Heatmap by Category & Month</p>", unsafe_allow_html=True)
    heat_data = df.groupby(["category", "month_num"])["rating"].mean().reset_index()
    heat_pivot = heat_data.pivot(index="category", columns="month_num", values="rating")
    fig_heat = px.imshow(
        heat_pivot, color_continuous_scale=["#f87171", "#f59e0b", "#34d399"],
        aspect="auto", text_auto=".1f",
    )
    fig_heat.update_layout(**PLOTLY_LAYOUT, coloraxis_colorbar=dict(title="Avg Rating"))
    st.plotly_chart(fig_heat, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — REVIEWS
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<p class='section-header'>Individual Feedback with Sentiment Analysis</p>", unsafe_allow_html=True)

    col_s, col_o = st.columns([3, 1])
    with col_s:
        search = st.text_input("🔍 Search feedback text", placeholder="Type a keyword…")
    with col_o:
        sort_col = st.selectbox("Sort by", ["date", "rating", "polarity"])

    display_df = df.copy()
    if search:
        display_df = display_df[display_df["feedback"].str.contains(search, case=False, na=False)]
    display_df = display_df.sort_values(sort_col, ascending=False)

    st.caption(f"Showing {len(display_df)} feedback entries")

    for _, row in display_df.head(20).iterrows():
        badge_map = {
            "Positive": "<span class='badge-positive'>● Positive</span>",
            "Negative": "<span class='badge-negative'>● Negative</span>",
            "Neutral":  "<span class='badge-neutral'>● Neutral</span>",
        }
        stars = "★" * int(row["rating"]) + "☆" * (5 - int(row["rating"]))
        st.markdown(f"""
        <div class='feedback-row'>
            <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;'>
                <span style='color:#ccd6f6;font-weight:600;'>{row['customer_name']}</span>
                <span style='display:flex;gap:8px;align-items:center;'>
                    {badge_map[row['sentiment']]}
                    <span style='color:#f59e0b;font-size:1rem;'>{stars}</span>
                </span>
            </div>
            <p style='color:#8892b0;font-size:0.82rem;margin-bottom:8px;'>
                📦 {row['category']} &nbsp;·&nbsp; 📅 {row['date'].strftime('%d %b %Y')}
                &nbsp;·&nbsp; Polarity: <b style='color:#a78bfa;'>{row['polarity']:.2f}</b>
                &nbsp;·&nbsp; Subjectivity: <b style='color:#60a5fa;'>{row['subjectivity']:.2f}</b>
            </p>
            <p style='color:#ccd6f6;font-size:0.9rem;margin:0;'>"{row['feedback']}"</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p class='section-header'>Download Analysed Data</p>", unsafe_allow_html=True)
    csv_out = df[["id","date","customer_name","product","category","rating",
                  "feedback","sentiment","polarity","subjectivity"]].to_csv(index=False)
    st.download_button("⬇️ Download CSV with Sentiment", csv_out,
                       file_name="feedback_with_sentiment.csv", mime="text/csv")
