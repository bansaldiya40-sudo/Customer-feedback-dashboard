# 💬 Customer Feedback Dashboard

A full-featured sentiment analysis dashboard built with **Streamlit**, **TextBlob**, and **Plotly**.

---

## 📁 Project Structure

```
customer_feedback_dashboard/
├── app.py                  ← Main Streamlit app
├── requirements.txt        ← Python dependencies
├── README.md               ← This file
└── data/
    └── feedback.csv        ← Sample feedback data (40 records)
```

---

## ✅ Prerequisites

- Python 3.8 or higher
- pip (comes with Python)
- VS Code (recommended) or any terminal

---

## 🚀 Step-by-Step Execution in VS Code

### Step 1 — Open the Project Folder

1. Launch **VS Code**
2. Go to `File → Open Folder`
3. Select the `customer_feedback_dashboard` folder

---

### Step 2 — Open the Integrated Terminal

- Press **`` Ctrl + ` ``** (backtick) to open the VS Code terminal
- Or go to `Terminal → New Terminal`

---

### Step 3 — Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

---

### Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
| Package | Purpose |
|---------|---------|
| `streamlit` | Web app framework |
| `pandas` | Data manipulation |
| `plotly` | Interactive charts |
| `textblob` | NLP sentiment analysis |
| `numpy` | Numerical operations |

---

### Step 5 — Download TextBlob Corpora (One-Time)

```bash
python -m textblob.download_corpora
```

This downloads the NLTK data TextBlob needs for sentiment analysis.

---

### Step 6 — Run the Dashboard

```bash
streamlit run app.py
```

---

### Step 7 — View in Browser

Streamlit will print:

```
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open **http://localhost:8501** in your browser. The dashboard loads instantly!

---

## 🎛️ Features

### Sidebar
- 📂 **Upload your own CSV** (must have: `feedback`, `rating`, `category`, `date`, `customer_name` columns)
- 🎚️ Filter by **category**, **sentiment**, **rating range**, **date range**

### Tab 1 — Overview
- ⭐ Rating distribution bar chart
- 🥧 Reviews by category (donut chart)
- 📊 Average rating per category (horizontal bar)

### Tab 2 — Sentiment
- 😊 Sentiment breakdown (Positive / Neutral / Negative)
- 🔵 Polarity vs Subjectivity scatter plot
- 📚 Stacked sentiment by category
- 📈 Polarity score distribution histogram

### Tab 3 — Trends
- 📅 Monthly review volume & average rating (dual-axis)
- 📉 Polarity trend over time
- 📐 Sentiment area chart over time
- 🔥 Rating heatmap by category & month

### Tab 4 — Reviews
- 🔍 Keyword search across feedback text
- 📋 Individual review cards with sentiment badges
- ⬇️ Download enriched CSV (with sentiment scores)

---

## 📋 CSV Format (for custom uploads)

Your CSV must have these columns:

```
id, date, customer_name, product, rating, feedback, category
```

- `date`: Any parseable date format (`YYYY-MM-DD` recommended)
- `rating`: Integer 1–5
- `feedback`: Free-form text (TextBlob analyses this)
- `category`: e.g. App, Support, Delivery, Website, Product

---

## 🛑 Common Issues

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| TextBlob errors | Run `python -m textblob.download_corpora` |
| Port 8501 in use | Run `streamlit run app.py --server.port 8502` |
| CSV not found | Make sure you run from inside `customer_feedback_dashboard/` |
| Blank charts | Check your filter settings — try resetting them |

---

## 🔄 Stop the Server

Press `Ctrl + C` in the terminal to stop Streamlit.

---

## 🧪 Tech Stack

- **[Streamlit](https://streamlit.io/)** — Python web UI framework
- **[TextBlob](https://textblob.readthedocs.io/)** — Sentiment & subjectivity analysis
- **[Plotly](https://plotly.com/python/)** — Interactive charts (bar, pie, scatter, heatmap, area)
- **[Pandas](https://pandas.pydata.org/)** — Data manipulation & filtering
