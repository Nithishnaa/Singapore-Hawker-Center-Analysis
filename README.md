# 🇸🇬 Singapore Hawker Centre Analytics

> Analysing Singapore's hawker culture through data — accessibility, regional distribution, and urban planning insights.

**[🔴 Live Dashboard →](https://singapore-hawker-center-analysis-streamlit.app)** 
---


## 📌 Project Overview

Singapore's hawker centres are a UNESCO-recognised cultural institution — but are they equally accessible to all residents?

This project combines **real Singapore government data** with engineered accessibility features to answer:
- Which regions are underserved by hawker infrastructure?
- How accessible are hawker centres by public transport?
- Are newer centres being built in the right places?

---

## 🔑 Key Findings

| Finding | Insight |
|---|---|
| **47%** of hawker centres are within 500m of MRT | More than half require a bus or long walk |
| **Central** has 3x more stalls than North | Significant regional disparity |
| Centres built **post-2015** are 40% more MRT-accessible | Government is improving co-location with transport |
| **North region** has the largest accessibility gap | Feeder bus routes could meaningfully improve food security |
| **Chinatown Complex** is Singapore's largest | 260+ cooked food stalls, Central location |

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Data Collection | Python `requests`, data.gov.sg GEOJSON API |
| Feature Engineering | Haversine formula, custom accessibility scoring |
| Analysis | SQL (SQLite), Pandas, NumPy |
| Visualisation | Plotly, Streamlit |
| Deployment | Streamlit Community Cloud |

---

## 📊 Dashboard Features

**4 interactive pages:**

**1. Executive Overview** — KPIs, regional stall distribution, size breakdown, top 15 centres

**2. Singapore Map** — Every hawker centre plotted, colour-coded by accessibility score, stall count, or region. Hover for full details.

**3. Deep Dive Explorer** — Scatter plots, box plots, correlation heatmap. Filter by region.

**4. Find Nearest Hawker** — Enter your coordinates → get the N nearest centres with a live mini-map.

---

## 📓 Notebooks

| Notebook | What it covers |
|---|---|
| `01_data_collection.ipynb` | Fetches real data from data.gov.sg API, engineers MRT accessibility scores using Haversine formula across 141 MRT stations |
| `02_sql_analysis.ipynb` | 5 SQL queries with Plotly charts — regional distribution, accessibility breakdown, underserved centres |

---

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/yourusername/sg-hawker-analytics
cd sg-hawker-analytics

# Create virtual environment
python3 -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows

# Install dependencies
pip install streamlit plotly pandas requests numpy matplotlib

# Step 1: Fetch data
jupyter notebook 01_data_collection.ipynb

# Step 2: SQL analysis (optional)
jupyter notebook 02_sql_analysis.ipynb

# Step 3: Launch dashboard
streamlit run 03_streamlit_app.py
```

---

## 📡 Data Sources

| Source | Dataset | Type |
|---|---|---|
| [data.gov.sg](https://data.gov.sg/datasets/d_4a086da0a5553be1d89383cd90d07ecd/view) | Hawker Centres GEOJSON | Live Government API |
| OneMap Singapore | MRT station coordinates | Government reference |

> Data is fetched live from Singapore's official open data API — not a static CSV.
> Hawker centre count reflects current NEA records (120 existing centres as of Mar 2026).

---

## 💡 Original Feature Engineering

The **MRT Accessibility Score (1–10)** is an original feature not present in any source dataset.

It was computed by:
1. Calculating real-world distances from every hawker centre to all 141 MRT stations using the **Haversine formula**
2. Taking the minimum distance (nearest station)
3. Scaling to a 1–10 score where 10 = directly adjacent to MRT, 1 = over 2km away

This enables direct comparison of accessibility across all 120 centres.

---

## 👩‍💻 About

Built by **Nithishna Saravana**
M.Sc. Data Science, Singapore University of Technology and Design (SUTD)
