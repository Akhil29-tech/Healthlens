# 🏥 HealthLens — India Disease Outbreak Story Dashboard

A data storytelling platform that turns India's public health data into a narrative-driven interactive dashboard. Covers COVID-19, Dengue, Tuberculosis, and Malaria across 20 Indian states from 2015–2023.

---

## 🗂️ Project Structure

```
healthlens/
├── app.py                  ← Main Streamlit dashboard
├── requirements.txt
├── utils/
│   ├── __init__.py
│   └── data_loader.py      ← Datasets + disease story narratives
└── README.md
```

---

## 🚀 Quick Start

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch dashboard
streamlit run app.py
```

---

## 📊 Dashboard Pages

| Page | What it shows |
|------|--------------|
| 🌍 National Overview | KPI cards, case trends, disease burden pie chart, deaths by disease |
| 📖 Disease Stories | Narrative arc for each disease — origin, peak, turning point, now |
| 🗺️ State Heatmap | State-wise cases for any disease & year, top/bottom 5 states |
| 📊 Compare Diseases | Side-by-side comparison of any two diseases — trend, CFR, worst state |
| 🔍 Deep Dive | Pick any state + disease → full year-wise breakdown + auto-generated insight |

---

## 🦠 Diseases Covered

| Disease | Period | Key Finding |
|---------|--------|-------------|
| COVID-19 | 2020–2023 | Peak in 2021 (Delta wave); 85% drop by 2023 |
| Dengue | 2015–2023 | Steady upward trend; monsoon states worst affected |
| Tuberculosis | 2015–2023 | Declining 3% per year; India aims to eliminate by 2025 |
| Malaria | 2015–2023 | 50% drop since 2015; concentrated in tribal belt |

---

## 🧠 Key Features

- **Scrollytelling narrative** — each disease has a 4-chapter story (Origin → Peak → Turning Point → Now)
- **Auto-generated insights** — plain-English summaries generated from data
- **20-state coverage** — all major Indian states with population-weighted data
- **Side-by-side comparison** — compare any two diseases on cases, deaths, CFR
- **Deep Dive explorer** — granular year-wise breakdown per state per disease

---

## 📁 Resume Description

> *Built HealthLens, a data storytelling dashboard covering 4 major diseases across 20 Indian states (2015–2023) using Python, Pandas, Plotly, and Streamlit. Features narrative-driven disease stories, state heatmaps, side-by-side comparisons, and auto-generated plain-English insights from data.*

---

## 📚 Data Sources

- WHO Global Health Observatory
- India National TB Elimination Programme (NTEP)
- India data.gov.in — Vector Borne Disease data
- COVID-19 India API (historical)
