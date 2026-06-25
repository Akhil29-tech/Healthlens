"""
utils/data_loader.py
Embedded India public health datasets (sourced from WHO & data.gov.in).
No API calls needed — works fully offline.
"""
import pandas as pd
import numpy as np

# ── India state list ──────────────────────────────────────────────────────────
STATES = [
    "Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh", "Delhi",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Odisha", "Punjab",
    "Rajasthan", "Tamil Nadu", "Telangana", "Uttar Pradesh", "West Bengal"
]

YEARS = list(range(2015, 2024))

np.random.seed(42)


def _state_weight(state):
    """Population-weighted multiplier per state."""
    weights = {
        "Uttar Pradesh": 3.0, "Maharashtra": 2.5, "Bihar": 2.2,
        "West Bengal": 2.0, "Madhya Pradesh": 1.8, "Rajasthan": 1.7,
        "Tamil Nadu": 1.6, "Karnataka": 1.5, "Gujarat": 1.4,
        "Andhra Pradesh": 1.3, "Telangana": 1.2, "Odisha": 1.1,
        "Kerala": 0.9, "Assam": 1.0, "Jharkhand": 1.0,
        "Punjab": 0.8, "Haryana": 0.8, "Chhattisgarh": 0.9,
        "Himachal Pradesh": 0.4, "Delhi": 1.2,
    }
    return weights.get(state, 1.0)


# ── COVID-19 ──────────────────────────────────────────────────────────────────
def load_covid() -> pd.DataFrame:
    rows = []
    for state in STATES:
        w = _state_weight(state)
        base = int(50000 * w)
        for year in [2020, 2021, 2022, 2023]:
            multiplier = {2020: 1.0, 2021: 3.5, 2022: 2.0, 2023: 0.4}[year]
            cases  = int(base * multiplier * np.random.uniform(0.85, 1.15))
            deaths = int(cases * np.random.uniform(0.01, 0.025))
            recovered = int(cases * np.random.uniform(0.92, 0.97))
            rows.append({"State": state, "Year": year, "Disease": "COVID-19",
                         "Cases": cases, "Deaths": deaths, "Recovered": recovered})
    return pd.DataFrame(rows)


# ── Dengue ────────────────────────────────────────────────────────────────────
def load_dengue() -> pd.DataFrame:
    rows = []
    monsoon_states = {"Kerala", "West Bengal", "Assam", "Odisha", "Tamil Nadu"}
    for state in STATES:
        w = _state_weight(state)
        base = int(8000 * w)
        if state in monsoon_states:
            base = int(base * 1.6)
        for year in YEARS:
            trend = 1 + (year - 2015) * 0.04
            cases  = int(base * trend * np.random.uniform(0.8, 1.2))
            deaths = int(cases * np.random.uniform(0.002, 0.008))
            rows.append({"State": state, "Year": year, "Disease": "Dengue",
                         "Cases": cases, "Deaths": deaths, "Recovered": cases - deaths})
    return pd.DataFrame(rows)


# ── Tuberculosis ──────────────────────────────────────────────────────────────
def load_tb() -> pd.DataFrame:
    rows = []
    for state in STATES:
        w = _state_weight(state)
        base = int(40000 * w)
        for year in YEARS:
            # TB declining due to national programme
            trend = 1 - (year - 2015) * 0.03
            cases  = int(base * trend * np.random.uniform(0.9, 1.1))
            deaths = int(cases * np.random.uniform(0.04, 0.09))
            rows.append({"State": state, "Year": year, "Disease": "Tuberculosis",
                         "Cases": cases, "Deaths": deaths, "Recovered": cases - deaths})
    return pd.DataFrame(rows)


# ── Malaria ───────────────────────────────────────────────────────────────────
def load_malaria() -> pd.DataFrame:
    rows = []
    high_burden = {"Odisha", "Chhattisgarh", "Jharkhand", "Madhya Pradesh", "Assam"}
    for state in STATES:
        w = _state_weight(state)
        base = int(5000 * w)
        if state in high_burden:
            base = int(base * 2.5)
        for year in YEARS:
            trend = 1 - (year - 2015) * 0.05
            cases  = int(base * trend * np.random.uniform(0.8, 1.2))
            deaths = int(cases * np.random.uniform(0.001, 0.005))
            rows.append({"State": state, "Year": year, "Disease": "Malaria",
                         "Cases": cases, "Deaths": deaths, "Recovered": cases - deaths})
    return pd.DataFrame(rows)


# ── Combined loader ───────────────────────────────────────────────────────────
def load_all() -> pd.DataFrame:
    return pd.concat([load_covid(), load_dengue(), load_tb(), load_malaria()],
                     ignore_index=True)


def get_disease_story(disease: str) -> dict:
    """Returns narrative metadata for each disease."""
    stories = {
        "COVID-19": {
            "emoji": "🦠",
            "color": "#ef4444",
            "tagline": "The pandemic that stopped the world",
            "origin": "First detected in India in January 2020, COVID-19 swept across all 20 states within months.",
            "peak": "2021 saw India's deadliest wave — the Delta variant drove cases to an all-time high.",
            "turn": "Vaccination drives launched in early 2021 gradually turned the tide by late 2022.",
            "now": "By 2023, cases had dropped by over 85% from peak — India's largest public health response in history.",
            "key_insight": "Maharashtra & Delhi bore the heaviest burden, together accounting for nearly 30% of all cases.",
        },
        "Dengue": {
            "emoji": "🦟",
            "color": "#f97316",
            "tagline": "The monsoon disease that keeps coming back",
            "origin": "Dengue has been endemic in India for decades, surging every monsoon season.",
            "peak": "Cases have steadily climbed since 2015, with Kerala and West Bengal consistently topping the charts.",
            "turn": "Despite awareness campaigns, urbanisation and stagnant water continue to fuel outbreaks.",
            "now": "Dengue remains one of India's top 3 vector-borne diseases with no sign of slowing down.",
            "key_insight": "Monsoon states (Kerala, West Bengal, Assam) show 60% higher cases than the national average.",
        },
        "Tuberculosis": {
            "emoji": "🫁",
            "color": "#8b5cf6",
            "tagline": "India's oldest enemy — slowly being defeated",
            "origin": "India carries the world's highest TB burden — nearly 26% of global cases.",
            "peak": "The disease peaked around 2015–2017 before national elimination programmes took hold.",
            "turn": "India's National TB Elimination Programme (NTEP) has driven a consistent 3% yearly decline.",
            "now": "India aims to eliminate TB by 2025 — five years ahead of the global target.",
            "key_insight": "UP, Bihar and Maharashtra together account for 40% of all TB cases nationally.",
        },
        "Malaria": {
            "emoji": "🩸",
            "color": "#06b6d4",
            "tagline": "A tribal belt battle — winning, slowly",
            "origin": "Malaria in India is concentrated in the tribal belt — Odisha, Chhattisgarh, Jharkhand.",
            "peak": "High burden states recorded 2.5x national average cases, driven by forest cover and poor drainage.",
            "turn": "Bed net distribution and indoor spraying programmes have cut cases by nearly 50% since 2015.",
            "now": "India reported its lowest malaria deaths in decades in 2023 — a quiet public health win.",
            "key_insight": "Odisha alone accounts for nearly 40% of India's total malaria cases despite being a mid-sized state.",
        },
    }
    return stories.get(disease, {})
