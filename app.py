"""
app.py — HealthLens: India Disease Outbreak Story Dashboard
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_all, load_covid, load_dengue, load_tb, load_malaria, get_disease_story, STATES, YEARS

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HealthLens India",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0a0f1e; }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    .main { background-color: #0a0f1e; color: #e2e8f0; }

    .story-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border-radius: 14px;
        padding: 24px;
        border-left: 5px solid var(--accent);
        margin-bottom: 16px;
    }
    .story-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #64748b;
        margin-bottom: 4px;
    }
    .story-text {
        font-size: 15px;
        color: #e2e8f0;
        line-height: 1.7;
    }
    .insight-box {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 16px 20px;
        font-size: 14px;
        color: #94a3b8;
        margin-top: 8px;
    }
    .insight-box strong { color: #f8fafc; }
    .kpi-card {
        background: #1e293b;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border-top: 3px solid;
    }
    .kpi-val { font-size: 28px; font-weight: 700; }
    .kpi-label { font-size: 12px; color: #64748b; margin-top: 4px; }
    h1, h2 { color: #f1f5f9 !important; }
    h3 { color: #94a3b8 !important; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_all()

df = get_data()

DISEASE_COLORS = {
    "COVID-19":      "#ef4444",
    "Dengue":        "#f97316",
    "Tuberculosis":  "#8b5cf6",
    "Malaria":       "#06b6d4",
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏥 HealthLens India")
    st.markdown("*Disease Outbreak Story Dashboard*")
    st.markdown("---")
    page = st.radio("Navigate", [
        "🌍 National Overview",
        "📖 Disease Stories",
        "🗺️ State Heatmap",
        "📊 Compare Diseases",
        "🔍 Deep Dive",
    ])
    st.markdown("---")
    st.caption("Data sourced from WHO & India data.gov.in\n(2015–2023)")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — NATIONAL OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "🌍 National Overview":
    st.title("🌍 India Disease Burden — National Overview")
    st.markdown("*A bird's eye view of how four major diseases have shaped India's public health landscape from 2015 to 2023.*")
    st.markdown("---")

    total_cases  = df["Cases"].sum()
    total_deaths = df["Deaths"].sum()
    cfr = round(total_deaths / total_cases * 100, 2)
    worst_state  = df.groupby("State")["Cases"].sum().idxmax()

    c1, c2, c3, c4 = st.columns(4)
    for col, val, label, color in [
        (c1, f"{total_cases/1e6:.1f}M", "Total Cases (all diseases)", "#ef4444"),
        (c2, f"{total_deaths/1e6:.2f}M", "Total Deaths", "#f97316"),
        (c3, f"{cfr}%", "Avg Case Fatality Rate", "#8b5cf6"),
        (c4, worst_state, "Highest Burden State", "#06b6d4"),
    ]:
        col.markdown(f"""
        <div class="kpi-card" style="border-color:{color}">
            <div class="kpi-val" style="color:{color}">{val}</div>
            <div class="kpi-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        yearly = df.groupby(["Year", "Disease"])["Cases"].sum().reset_index()
        fig = px.line(
            yearly, x="Year", y="Cases", color="Disease",
            color_discrete_map=DISEASE_COLORS,
            title="📈 Cases Over Time — All Diseases",
            markers=True,
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#e2e8f0", legend_title="Disease")
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(gridcolor="#1e293b")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        disease_total = df.groupby("Disease")["Cases"].sum().reset_index()
        fig2 = px.pie(
            disease_total, values="Cases", names="Disease",
            color="Disease", color_discrete_map=DISEASE_COLORS,
            title="🥧 Share of Total Disease Burden",
            hole=0.55,
        )
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
        st.plotly_chart(fig2, use_container_width=True)

    # Deaths bar
    death_by_disease = df.groupby("Disease")["Deaths"].sum().reset_index().sort_values("Deaths", ascending=False)
    fig3 = px.bar(
        death_by_disease, x="Disease", y="Deaths",
        color="Disease", color_discrete_map=DISEASE_COLORS,
        title="💀 Total Deaths by Disease (2015–2023)",
        text_auto=".2s",
    )
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       font_color="#e2e8f0", showlegend=False)
    fig3.update_traces(textposition="outside")
    st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — DISEASE STORIES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📖 Disease Stories":
    st.title("📖 Disease Stories")
    st.markdown("*Every outbreak has a story — an origin, a peak, a turning point, and a lesson.*")
    st.markdown("---")

    disease = st.selectbox("Choose a disease to read its story", list(DISEASE_COLORS.keys()))
    story   = get_disease_story(disease)
    color   = DISEASE_COLORS[disease]

    st.markdown(f"## {story['emoji']} {disease}")
    st.markdown(f"<p style='font-size:18px;color:{color};font-style:italic;'>{story['tagline']}</p>",
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    chapters = [
        ("🌱 Origin",        story["origin"]),
        ("🔺 The Peak",      story["peak"]),
        ("🔄 The Turning Point", story["turn"]),
        ("📍 Where We Are Now",  story["now"]),
    ]

    for label, text in chapters:
        st.markdown(f"""
        <div class="story-card" style="--accent:{color}">
            <div class="story-label">{label}</div>
            <div class="story-text">{text}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-box">
        💡 <strong>Key Insight:</strong> {story['key_insight']}
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Disease-specific yearly chart
    d_df = df[df["Disease"] == disease].groupby("Year")[["Cases", "Deaths"]].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=d_df["Year"], y=d_df["Cases"], name="Cases",
                         marker_color=color, opacity=0.8))
    fig.add_trace(go.Scatter(x=d_df["Year"], y=d_df["Deaths"], name="Deaths",
                             mode="lines+markers", line=dict(color="#f8fafc", width=2),
                             yaxis="y2"))
    fig.update_layout(
        title=f"{disease} — Cases & Deaths by Year",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        yaxis=dict(title="Cases", showgrid=False),
        yaxis2=dict(title="Deaths", overlaying="y", side="right", showgrid=False),
        legend=dict(orientation="h", y=1.1),
    )
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — STATE HEATMAP
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ State Heatmap":
    st.title("🗺️ State-wise Disease Heatmap")
    st.markdown("*Which states bore the heaviest burden? Explore the geography of outbreaks.*")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        selected_disease = st.selectbox("Disease", list(DISEASE_COLORS.keys()))
    with col2:
        selected_year = st.selectbox("Year", sorted(df["Year"].unique(), reverse=True))

    filtered = df[(df["Disease"] == selected_disease) & (df["Year"] == selected_year)]
    state_data = filtered.groupby("State")[["Cases", "Deaths"]].sum().reset_index()
    state_data["CFR %"] = (state_data["Deaths"] / state_data["Cases"] * 100).round(2)

    color = DISEASE_COLORS[selected_disease]

    fig = px.bar(
        state_data.sort_values("Cases", ascending=True),
        x="Cases", y="State", orientation="h",
        color="Cases",
        color_continuous_scale=["#1e293b", color],
        title=f"{selected_disease} Cases by State — {selected_year}",
        text="Cases",
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="#e2e8f0", height=600, coloraxis_showscale=False)
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    # Top 5 and Bottom 5
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🔴 Top 5 Highest Burden States")
        top5 = state_data.nlargest(5, "Cases")[["State", "Cases", "Deaths", "CFR %"]]
        top5["Cases"] = top5["Cases"].apply(lambda x: f"{x:,}")
        top5["Deaths"] = top5["Deaths"].apply(lambda x: f"{x:,}")
        st.dataframe(top5.reset_index(drop=True), use_container_width=True)
    with col2:
        st.markdown("#### 🟢 Top 5 Lowest Burden States")
        bot5 = state_data.nsmallest(5, "Cases")[["State", "Cases", "Deaths", "CFR %"]]
        bot5["Cases"] = bot5["Cases"].apply(lambda x: f"{x:,}")
        bot5["Deaths"] = bot5["Deaths"].apply(lambda x: f"{x:,}")
        st.dataframe(bot5.reset_index(drop=True), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — COMPARE DISEASES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Compare Diseases":
    st.title("📊 Compare Two Diseases Side by Side")
    st.markdown("*How do two diseases compare in scale, mortality, and trend?*")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        d1 = st.selectbox("Disease 1", list(DISEASE_COLORS.keys()), index=0)
    with col2:
        d2 = st.selectbox("Disease 2", list(DISEASE_COLORS.keys()), index=1)

    if d1 == d2:
        st.warning("Please select two different diseases.")
        st.stop()

    def summary(disease):
        d = df[df["Disease"] == disease]
        return {
            "Total Cases":  d["Cases"].sum(),
            "Total Deaths": d["Deaths"].sum(),
            "CFR %":        round(d["Deaths"].sum() / d["Cases"].sum() * 100, 2),
            "Peak Year":    d.groupby("Year")["Cases"].sum().idxmax(),
            "Worst State":  d.groupby("State")["Cases"].sum().idxmax(),
        }

    s1, s2 = summary(d1), summary(d2)

    metrics = ["Total Cases", "Total Deaths", "CFR %", "Peak Year", "Worst State"]
    c1, c2 = st.columns(2)
    for col, s, disease in [(c1, s1, d1), (c2, s2, d2)]:
        color = DISEASE_COLORS[disease]
        col.markdown(f"### {get_disease_story(disease)['emoji']} {disease}")
        for m in metrics:
            val = s[m]
            if isinstance(val, (int, float)) and m not in ["CFR %", "Peak Year"]:
                val = f"{val:,}"
            col.markdown(f"""
            <div style="padding:10px 0;border-bottom:1px solid #1e293b;">
                <span style="color:#64748b;font-size:12px;">{m}</span><br>
                <span style="color:{color};font-size:20px;font-weight:600;">{val}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Side by side yearly trend
    yearly = df[df["Disease"].isin([d1, d2])].groupby(["Year", "Disease"])["Cases"].sum().reset_index()
    fig = px.line(
        yearly, x="Year", y="Cases", color="Disease",
        color_discrete_map=DISEASE_COLORS,
        markers=True,
        title=f"📈 {d1} vs {d2} — Case Trend (2015–2023)",
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="#e2e8f0")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#1e293b")
    st.plotly_chart(fig, use_container_width=True)

    # CFR comparison
    cfr_df = pd.DataFrame({
        "Disease": [d1, d2],
        "CFR %":   [s1["CFR %"], s2["CFR %"]],
    })
    fig2 = px.bar(
        cfr_df, x="Disease", y="CFR %",
        color="Disease", color_discrete_map=DISEASE_COLORS,
        title="💀 Case Fatality Rate Comparison",
        text="CFR %",
    )
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       font_color="#e2e8f0", showlegend=False)
    fig2.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(fig2, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — DEEP DIVE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Deep Dive":
    st.title("🔍 Deep Dive — State & Disease Explorer")
    st.markdown("*Pick any state and disease to explore a detailed multi-year breakdown.*")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        state = st.selectbox("Select State", sorted(STATES))
    with col2:
        disease = st.selectbox("Select Disease", list(DISEASE_COLORS.keys()))

    filtered = df[(df["State"] == state) & (df["Disease"] == disease)].sort_values("Year")
    color = DISEASE_COLORS[disease]

    if filtered.empty:
        st.warning("No data found.")
        st.stop()

    total_c = filtered["Cases"].sum()
    total_d = filtered["Deaths"].sum()
    total_r = filtered["Recovered"].sum()
    cfr     = round(total_d / total_c * 100, 2)
    peak_yr = filtered.loc[filtered["Cases"].idxmax(), "Year"]

    c1, c2, c3, c4 = st.columns(4)
    for col, val, label in [
        (c1, f"{total_c:,}",  "Total Cases"),
        (c2, f"{total_d:,}",  "Total Deaths"),
        (c3, f"{total_r:,}",  "Total Recovered"),
        (c4, f"{peak_yr}",    "Peak Year"),
    ]:
        col.markdown(f"""
        <div class="kpi-card" style="border-color:{color}">
            <div class="kpi-val" style="color:{color}">{val}</div>
            <div class="kpi-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Stacked area — Cases vs Recovered vs Deaths
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered["Year"], y=filtered["Recovered"],
                             name="Recovered", fill="tozeroy",
                             line=dict(color="#22c55e"), fillcolor="rgba(34,197,94,0.2)"))
    fig.add_trace(go.Scatter(x=filtered["Year"], y=filtered["Cases"],
                             name="Cases", fill="tonexty",
                             line=dict(color=color), fillcolor=f"rgba(239,68,68,0.15)"))
    fig.add_trace(go.Scatter(x=filtered["Year"], y=filtered["Deaths"],
                             name="Deaths", mode="lines+markers",
                             line=dict(color="#f8fafc", width=2, dash="dot")))
    fig.update_layout(
        title=f"{disease} in {state} — Year-wise Breakdown",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False, gridcolor="#1e293b"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Raw data table
    st.markdown("#### 📋 Year-wise Data Table")
    display = filtered[["Year", "Cases", "Deaths", "Recovered"]].copy()
    display["CFR %"] = (display["Deaths"] / display["Cases"] * 100).round(2)
    display = display.reset_index(drop=True)
    st.dataframe(display, use_container_width=True)

    # Auto-generated insight
    max_row = filtered.loc[filtered["Cases"].idxmax()]
    min_row = filtered.loc[filtered["Cases"].idxmin()]
    change  = round((filtered["Cases"].iloc[-1] - filtered["Cases"].iloc[0]) / filtered["Cases"].iloc[0] * 100, 1)
    direction = "increased" if change > 0 else "decreased"

    st.markdown(f"""
    <div class="insight-box">
        💡 <strong>Auto Insight:</strong> {state} saw its highest {disease} burden in
        <strong>{int(max_row['Year'])}</strong> with <strong>{int(max_row['Cases']):,} cases</strong>.
        The lowest was in <strong>{int(min_row['Year'])}</strong> with <strong>{int(min_row['Cases']):,} cases</strong>.
        Overall, cases have <strong>{direction} by {abs(change)}%</strong> from 2015 to 2023.
    </div>""", unsafe_allow_html=True)
