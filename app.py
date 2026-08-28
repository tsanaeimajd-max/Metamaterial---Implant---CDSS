import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="CDSS - Metamaterial Femoral Implants",
    page_icon="🦴",
    layout="wide"
)

# App Header
st.title("🦴 Clinical Decision Support System (CDSS)")
st.subheader("Automated Comprehensive Matrix: Cross-Sections & Hybrid Metamaterials")
st.markdown("---")

# --- پایگاه داده کامل پروژه (بدون نیاز به انتخاب دستی مقطع) ---
@st.cache_data
def load_full_fea_database():
    data = [
        # Circular Cross-Section
        {"Cross-Section": "Circular", "Architecture": "Hybrid (Radial Gradient Core)", "Stiffness_Base": 15.8, "FoS": 3.7, "Stress_Shielding": "Optimal (Low)"},
        {"Cross-Section": "Circular", "Architecture": "Gyroid (TPMS)", "Stiffness_Base": 14.5, "FoS": 3.4, "Stress_Shielding": "Low"},
        {"Cross-Section": "Circular", "Architecture": "Diamond (TPMS)", "Stiffness_Base": 18.0, "FoS": 3.9, "Stress_Shielding": "Moderate"},
        {"Cross-Section": "Circular", "Architecture": "Solid Standard (Control)", "Stiffness_Base": 110.0, "FoS": 5.2, "Stress_Shielding": "High"},

        # Elliptical Cross-Section
        {"Cross-Section": "Elliptical", "Architecture": "Hybrid (Radial Gradient Core)", "Stiffness_Base": 16.7, "FoS": 3.6, "Stress_Shielding": "Optimal (Low)"},
        {"Cross-Section": "Elliptical", "Architecture": "Gyroid (TPMS)", "Stiffness_Base": 15.3, "FoS": 3.3, "Stress_Shielding": "Low"},
        {"Cross-Section": "Elliptical", "Architecture": "Diamond (TPMS)", "Stiffness_Base": 19.1, "FoS": 3.8, "Stress_Shielding": "Moderate"},
        {"Cross-Section": "Elliptical", "Architecture": "Solid Standard (Control)", "Stiffness_Base": 118.0, "FoS": 5.0, "Stress_Shielding": "High"},

        # Trapezoidal Cross-Section
        {"Cross-Section": "Trapezoidal", "Architecture": "Hybrid (Radial Gradient Core)", "Stiffness_Base": 17.5, "FoS": 3.5, "Stress_Shielding": "Optimal (Low)"},
        {"Cross-Section": "Trapezoidal", "Architecture": "Gyroid (TPMS)", "Stiffness_Base": 16.0, "FoS": 3.2, "Stress_Shielding": "Low"},
        {"Cross-Section": "Trapezoidal", "Architecture": "Diamond (TPMS)", "Stiffness_Base": 20.2, "FoS": 3.7, "Stress_Shielding": "Moderate"},
        {"Cross-Section": "Trapezoidal", "Architecture": "Solid Standard (Control)", "Stiffness_Base": 125.0, "FoS": 4.8, "Stress_Shielding": "High"}
    ]
    return pd.DataFrame(data)

df_raw = load_full_fea_database()

# Sidebar for Patient Profile Only
st.sidebar.header("📋 Patient Clinical Profile")
patient_weight = st.sidebar.slider("Patient Body Weight (kg)", 40.0, 140.0, 75.0, 1.0)
bone_condition = st.sidebar.selectbox("Bone Pathology / Density", ["Healthy / Normal", "Osteopenia", "Osteoporosis"])

# Clinical Factor Adjustments
pathology_factor = {"Healthy / Normal": 1.0, "Osteopenia": 0.8, "Osteoporosis": 0.58}[bone_condition]
weight_ratio = patient_weight / 75.0

# Process all data dynamically
df_processed = df_raw.copy()
df_processed['Effective Stiffness (GPa)'] = round(df_processed['Stiffness_Base'] * pathology_factor * weight_ratio, 2)
df_processed['Safety Factor'] = round(df_processed['FoS'], 2)

# MCDM Suitability Score Calculation based on target cortical bone stiffness (approx 20 GPa)
target_stiffness = 20.0
scores = []
for idx, row in df_processed.iterrows():
    stiff = row['Effective Stiffness (GPa)']
    shield = row['Stress_Shielding']

    stiff_penalty = abs(stiff - target_stiffness) * 2.2
    shield_penalty = 35 if "High" in shield else (0 if "Optimal" in shield else 10)
    score = max(0.0, round(100.0 - stiff_penalty - shield_penalty, 1))
    scores.append(score)

df_processed['MCDM Suitability Score'] = scores

# Combine Cross-Section and Architecture for display label and sort by score
df_processed['Configuration'] = df_processed['Cross-Section'] + " - " + df_processed['Architecture']
df_display = df_processed[['Configuration', 'Cross-Section', 'Architecture', 'Effective Stiffness (GPa)', 'Stress_Shielding', 'Safety Factor', 'MCDM Suitability Score']].sort_values(by='MCDM Suitability Score', ascending=False).reset_index(drop=True)

# Main Dashboard Layout
col1, col2 = st.columns([1.3, 1])

with col1:
    st.markdown("### 📊 Comprehensive MCDM Ranking Matrix (All Configurations)")
    st.dataframe(df_display[['Configuration', 'Effective Stiffness (GPa)', 'Stress_Shielding', 'Safety Factor', 'MCDM Suitability Score']], use_container_width=True)

    best_row = df_display.iloc[0]
    st.success(f"🌟 **Overall Global Recommendation:** The optimal configuration is **{best_row['Configuration']}** with an MCDM Score of **{best_row['MCDM Suitability Score']}**.")

with col2:
    st.markdown("### 📈 Top Configurations Comparison Chart")
    top_5 = df_display.head(5)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top_5['Configuration'],
        y=top_5['Effective Stiffness (GPa)'],
        marker_color=['#2E86C1', '#28B463', '#F39C12', '#9B59B6', '#E74C3C']
    ))
    fig.update_layout(
        xaxis_title="Implant Configuration",
        yaxis_title="Effective Stiffness (GPa)",
        template="plotly_white",
        height=380,
        xaxis_tickangle=-30
    )
    st.plotly_chart(fig, use_container_width=True)
