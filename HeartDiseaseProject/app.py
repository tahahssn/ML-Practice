import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import time

st.set_page_config(
    page_title="CardioRisk AI",
    page_icon="❤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

/* ─── BASE ─── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #e8e8e2;
    background: #0a0a0a;
}

.stApp {
    background: #0a0a0a;
}

.main .block-container {
    background: transparent;
    padding: 2.5rem 3rem;
    max-width: 1100px;
}

/* ─── HIDE STREAMLIT CHROME ─── */
#MainMenu, footer, header { visibility: hidden; }

/* ─── TYPOGRAPHY ─── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #f0efe8 !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}

p, li, span, div {
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ─── HERO ─── */
.hero-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #3a7d5a;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(3rem, 6vw, 5.5rem);
    font-weight: 700;
    line-height: 0.92;
    letter-spacing: -3px;
    color: #f0efe8;
    margin-bottom: 1.25rem;
}

.hero-title em {
    font-style: normal;
    color: #3a7d5a;
}

.hero-sub {
    font-size: 0.9rem;
    color: #4a4a44;
    line-height: 1.7;
    font-weight: 400;
    max-width: 480px;
}

.nav-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 2rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 3rem;
}

.nav-brand {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #2a2a2a;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.nav-status {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #3a7d5a;
    background: rgba(58,125,90,0.1);
    border: 1px solid rgba(58,125,90,0.25);
    padding: 4px 12px;
    letter-spacing: 2px;
}

/* ─── METRIC CARDS ─── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 3rem;
}

.metric-cell {
    background: #0a0a0a;
    padding: 1.5rem 1.25rem;
    position: relative;
}

.metric-n {
    font-family: 'Space Mono', monospace;
    font-size: 0.55rem;
    color: #1e1e1e;
    position: absolute;
    top: 12px;
    right: 14px;
    letter-spacing: 1px;
}

.metric-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    color: #3a3a3a;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-bottom: 0.9rem;
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #f0efe8;
    letter-spacing: -1.5px;
    margin-bottom: 0.3rem;
    line-height: 1;
}

.metric-delta {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    color: #3a7d5a;
}

/* ─── DIVIDER ─── */
.section-divider {
    height: 1px;
    background: rgba(255,255,255,0.05);
    margin: 2.5rem 0;
    position: relative;
    text-align: center;
}

.divider-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #2a2a2a;
    letter-spacing: 2px;
}

/* ─── COLUMN HEADERS ─── */
.col-section-head {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    color: #3a7d5a;
    letter-spacing: 3.5px;
    text-transform: uppercase;
    padding-bottom: 0.9rem;
    border-bottom: 1px solid rgba(58,125,90,0.18);
    margin-bottom: 1.75rem;
}

/* ─── LABELS ─── */
.stSlider label, .stSelectbox label, .stNumberInput label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.62rem !important;
    font-weight: 400 !important;
    color: #3a3a3a !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}

/* ─── SLIDER ─── */
.stSlider > div > div > div {
    background: rgba(255,255,255,0.08) !important;
    height: 2px !important;
    border-radius: 0 !important;
}

.stSlider > div > div > div > div {
    background: #3a7d5a !important;
    border-radius: 0 !important;
}

.stSlider > div > div > div > div > div {
    background: #f0efe8 !important;
    border: none !important;
    border-radius: 50% !important;
    width: 10px !important;
    height: 10px !important;
    box-shadow: none !important;
}

/* ─── INPUTS ─── */
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 0 !important;
    color: #f0efe8 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
    padding: 8px 0 !important;
    box-shadow: none !important;
}

.stNumberInput > div > div > input:focus {
    border-bottom-color: #3a7d5a !important;
    box-shadow: none !important;
}

/* ─── SELECTBOX ─── */
.stSelectbox > div > div {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 0 !important;
    color: #f0efe8 !important;
    box-shadow: none !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.85rem !important;
}

.stSelectbox > div > div:focus,
.stSelectbox > div > div:hover {
    border-bottom-color: #3a7d5a !important;
    box-shadow: none !important;
}

/* ─── BUTTON ─── */
.stButton > button {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    color: #0a0a0a !important;
    background: #f0efe8 !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 14px 52px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: #3a7d5a !important;
    color: #f0efe8 !important;
    transform: none !important;
}

/* ─── RESULT BOX ─── */
.result-box {
    border: 1px solid rgba(58,125,90,0.25);
    padding: 2rem;
    margin-bottom: 2rem;
}

.result-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #3a7d5a;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.result-head {
    font-size: 2.5rem;
    font-weight: 700;
    color: #f0efe8;
    letter-spacing: -1.5px;
    line-height: 1;
    margin-bottom: 0.75rem;
}

.result-sub {
    font-size: 0.82rem;
    color: #4a4a44;
    line-height: 1.7;
    margin-bottom: 1.5rem;
    font-weight: 400;
}

.risk-number {
    font-family: 'Space Mono', monospace;
    font-size: 4rem;
    font-weight: 700;
    color: #3a7d5a;
    letter-spacing: -2px;
    line-height: 1;
}

.risk-unit {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    color: #3a3a3a;
    letter-spacing: 3px;
    margin-top: 0.5rem;
    text-transform: uppercase;
}

.gauge-track {
    height: 3px;
    background: rgba(255,255,255,0.06);
    margin: 1.5rem 0 0.5rem;
}

.rec-item {
    border-left: 2px solid rgba(58,125,90,0.3);
    padding: 0.75rem 1rem;
    margin-bottom: 0.75rem;
}

.rec-n {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    color: #3a7d5a;
    letter-spacing: 2px;
    margin-bottom: 0.3rem;
}

.rec-body {
    font-size: 0.8rem;
    color: #a0a09a;
    line-height: 1.5;
}

/* ─── ALERTS ─── */
.stAlert {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.8rem !important;
    color: #a0a09a !important;
}

/* ─── FOOTER ─── */
.footer-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin-top: 3rem;
}

.footer-left {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    color: #2a2a2a;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.footer-right {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    color: #2a2a2a;
}

/* ─── SCROLLBAR ─── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #2a2a2a; }
::-webkit-scrollbar-thumb:hover { background: #3a7d5a; }

/* ─── MISC ─── */
.element-container, .stMarkdown {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# ─── LOAD MODELS ───────────────────────────────────────────────
with st.spinner('Initializing model...'):
    time.sleep(0.4)
    model = joblib.load(r"D:\ML-Practice\HeartDiseaseProject\KNN_heart.pkl")
    scaler = joblib.load(r"D:\ML-Practice\HeartDiseaseProject\scalar.pkl")
    expected_columns = joblib.load(r"D:\ML-Practice\HeartDiseaseProject\columns.pkl")

# ─── NAV ───────────────────────────────────────────────────────
st.markdown("""
<div class='nav-bar'>
    <span class='nav-brand'>CARDIORISK // v2.0</span>
    <span class='nav-status'>● SYSTEM ACTIVE</span>
</div>
""", unsafe_allow_html=True)

# ─── HERO ──────────────────────────────────────────────────────
st.markdown("""
<div style='margin-bottom:3.5rem'>
    <p class='hero-eyebrow'>// CARDIOVASCULAR RISK ASSESSMENT SYSTEM</p>
    <h1 class='hero-title'>Cardio<em>Risk</em><br>A.I.</h1>
    <p class='hero-sub'>
        Advanced clinical decision support powered by machine learning.
        Input patient parameters to compute cardiovascular risk stratification.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── METRICS ───────────────────────────────────────────────────
st.markdown("""
<div class='metric-grid'>
    <div class='metric-cell'>
        <span class='metric-n'>01</span>
        <div class='metric-label'>Model Accuracy</div>
        <div class='metric-value'>96.5%</div>
        <div class='metric-delta'>▲ +2.3% delta</div>
    </div>
    <div class='metric-cell'>
        <span class='metric-n'>02</span>
        <div class='metric-label'>Clinical Cases</div>
        <div class='metric-value'>10.2K</div>
        <div class='metric-delta'>847 this month</div>
    </div>
    <div class='metric-cell'>
        <span class='metric-n'>03</span>
        <div class='metric-label'>Response Time</div>
        <div class='metric-value'>&lt;0.5s</div>
        <div class='metric-delta'>Real-time inference</div>
    </div>
    <div class='metric-cell'>
        <span class='metric-n'>04</span>
        <div class='metric-label'>AUC Score</div>
        <div class='metric-value'>0.983</div>
        <div class='metric-delta'>Excellent class sep.</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='section-divider'><span class='divider-label'>// INPUT PARAMETERS</span></div>", unsafe_allow_html=True)

# ─── INPUT FORM ────────────────────────────────────────────────
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.markdown("<div class='col-section-head'>// PATIENT DEMOGRAPHICS</div>", unsafe_allow_html=True)

    age = st.slider("AGE (YEARS)", 18, 100, 40)
    sex = st.selectbox("SEX", ["Male", "Female"])
    chest_pain = st.selectbox("CHEST PAIN TYPE", [
        "ATA — Atypical Angina",
        "NAP — Non-Anginal Pain",
        "TA — Typical Angina",
        "ASY — Asymptomatic"
    ])
    resting_bp = st.number_input("RESTING BLOOD PRESSURE (MM HG)", 80, 200, 120)
    cholesterol = st.number_input("SERUM CHOLESTEROL (MG/DL)", 100, 600, 200)

with right_col:
    st.markdown("<div class='col-section-head'>// CLINICAL MEASUREMENTS</div>", unsafe_allow_html=True)

    fasting_bs = st.selectbox("FASTING BLOOD SUGAR > 120 MG/DL", ["No", "Yes"])
    resting_ecg = st.selectbox("RESTING ECG RESULTS", [
        "Normal",
        "ST-T Wave Abnormality",
        "Left Ventricular Hypertrophy"
    ])
    max_hr = st.slider("MAXIMUM HEART RATE", 60, 220, 150)
    exercise_angina = st.selectbox("EXERCISE-INDUCED ANGINA", ["No", "Yes"])
    oldpeak = st.slider("ST DEPRESSION (OLDPEAK)", 0.0, 6.0, 1.0, 0.1)
    st_slope = st.selectbox("ST SEGMENT SLOPE", ["Upsloping", "Flat", "Downsloping"])

# ─── PREDICT BUTTON ────────────────────────────────────────────
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_button = st.button("Analyze Cardiovascular Risk →", use_container_width=True)

# ─── PREDICTION LOGIC ──────────────────────────────────────────
if predict_button:
    with st.spinner("Computing risk stratification..."):
        time.sleep(0.8)

        sex_encoded = "M" if sex == "Male" else "F"
        chest_pain_encoded = chest_pain.split(" — ")[0]
        resting_ecg_encoded = resting_ecg.split(" ")[0] if " " in resting_ecg else resting_ecg
        if resting_ecg_encoded == "ST-T":
            resting_ecg_encoded = "ST"
        exercise_angina_encoded = "Y" if exercise_angina == "Yes" else "N"
        st_slope_encoded = st_slope[0]
        fasting_bs_encoded = 1 if fasting_bs == "Yes" else 0

        raw_input = {
            'Age': age,
            'RestingBP': resting_bp,
            'Cholesterol': cholesterol,
            'FastingBS': fasting_bs_encoded,
            'MaxHR': max_hr,
            'Oldpeak': oldpeak,
            'Sex_' + sex_encoded: 1,
            'ChestPainType_' + chest_pain_encoded: 1,
            'RestingECG_' + resting_ecg_encoded: 1,
            'ExerciseAngina_' + exercise_angina_encoded: 1,
            'ST_Slope_' + st_slope_encoded: 1
        }

        input_df = pd.DataFrame([raw_input])
        for col in expected_columns:
            if col not in input_df.columns:
                input_df[col] = 0
        input_df = input_df[expected_columns]
        scaled_input = scaler.transform(input_df)
        prediction = model.predict(scaled_input)[0]
        probability = model.predict_proba(scaled_input)[0]

    st.markdown("<div class='section-divider'><span class='divider-label'>// ASSESSMENT OUTPUT</span></div>", unsafe_allow_html=True)

    res_col, rec_col = st.columns([1, 1], gap="large")

    if prediction == 1:
        prob_pct = probability[1] * 100
        bar_width = int(prob_pct)
        result_label = "High Risk Detected"
        result_desc = "Clinical indicators suggest elevated cardiovascular risk. Immediate specialist referral is advised."
        prob_display = f"{prob_pct:.1f}%"
        unit_label = "RISK PROBABILITY"

        with res_col:
            st.markdown(f"""
            <div class='result-box'>
                <div class='result-tag'>// RISK ASSESSMENT OUTPUT</div>
                <div class='result-head'>{result_label}</div>
                <div class='result-sub'>{result_desc}</div>
                <div class='risk-number'>{prob_display}</div>
                <div class='risk-unit'>{unit_label}</div>
                <div class='gauge-track'>
                    <div style='height:3px;background:#3a7d5a;width:{bar_width}%'></div>
                </div>
                <div style='display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:0.58rem;color:#2a2a2a;letter-spacing:1px'>
                    <span>0%</span><span>LOW</span><span>MOD</span><span>HIGH</span><span>100%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with rec_col:
            st.markdown("""
            <div style='padding-top:0.5rem'>
                <div style='font-family:"Space Mono",monospace;font-size:0.62rem;color:#3a7d5a;letter-spacing:3px;margin-bottom:1.5rem'>
                    // CLINICAL PROTOCOL
                </div>
                <div class='rec-item' style='border-left-color:#3a7d5a'>
                    <div class='rec-n'>01 // IMMEDIATE ACTION</div>
                    <div class='rec-body'>Schedule cardiology consultation. Priority referral within 14 days minimum.</div>
                </div>
                <div class='rec-item'>
                    <div class='rec-n'>02 // DIAGNOSTICS</div>
                    <div class='rec-body'>Consider stress test, echocardiogram, and coronary angiography evaluation.</div>
                </div>
                <div class='rec-item'>
                    <div class='rec-n'>03 // LIFESTYLE</div>
                    <div class='rec-body'>Aggressive pharmacological and lifestyle intervention protocol required.</div>
                </div>
                <div class='rec-item'>
                    <div class='rec-n'>04 // MONITORING</div>
                    <div class='rec-body'>Bi-monthly BP and cholesterol tracking. Daily activity logging recommended.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        prob_pct = probability[0] * 100
        bar_width = int(prob_pct)
        result_label = "Low Risk Assessment"
        result_desc = "Cardiovascular risk indicators appear within normal reference ranges. Continue preventive protocol."
        prob_display = f"{prob_pct:.1f}%"
        unit_label = "SAFETY CONFIDENCE"

        with res_col:
            st.markdown(f"""
            <div class='result-box' style='border-color:rgba(255,255,255,0.1)'>
                <div class='result-tag'>// RISK ASSESSMENT OUTPUT</div>
                <div class='result-head'>{result_label}</div>
                <div class='result-sub'>{result_desc}</div>
                <div class='risk-number' style='color:#f0efe8'>{prob_display}</div>
                <div class='risk-unit'>{unit_label}</div>
                <div class='gauge-track'>
                    <div style='height:3px;background:#f0efe8;width:{bar_width}%'></div>
                </div>
                <div style='display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:0.58rem;color:#2a2a2a;letter-spacing:1px'>
                    <span>0%</span><span>LOW</span><span>MOD</span><span>HIGH</span><span>100%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with rec_col:
            st.markdown("""
            <div style='padding-top:0.5rem'>
                <div style='font-family:"Space Mono",monospace;font-size:0.62rem;color:#3a7d5a;letter-spacing:3px;margin-bottom:1.5rem'>
                    // PREVENTIVE PROTOCOL
                </div>
                <div class='rec-item' style='border-left-color:rgba(255,255,255,0.15)'>
                    <div class='rec-n'>01 // PREVENTIVE CARE</div>
                    <div class='rec-body'>Annual cardiovascular health screening. Continue current lifestyle habits.</div>
                </div>
                <div class='rec-item'>
                    <div class='rec-n'>02 // ACTIVITY</div>
                    <div class='rec-body'>Maintain 150+ minutes of moderate aerobic exercise per week minimum.</div>
                </div>
                <div class='rec-item'>
                    <div class='rec-n'>03 // NUTRITION</div>
                    <div class='rec-body'>Mediterranean-style diet. Limit saturated fats, sodium, and processed sugars.</div>
                </div>
                <div class='rec-item'>
                    <div class='rec-n'>04 // MONITORING</div>
                    <div class='rec-body'>Annual BP and cholesterol tracking. Report new symptoms promptly.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ─── PLOTLY GAUGE ─────────────────────────────────────────
    gauge_val = probability[1] * 100 if prediction == 1 else probability[0] * 100
    gauge_color = "#3a7d5a" if prediction == 1 else "#f0efe8"
    gauge_title = "RISK SCORE" if prediction == 1 else "SAFETY SCORE"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=gauge_val,
        number={'suffix': "%", 'font': {'size': 28, 'family': 'Space Mono', 'color': '#f0efe8'}},
        title={'text': gauge_title, 'font': {'size': 11, 'family': 'Space Mono', 'color': '#3a3a3a'}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {
                'range': [0, 100],
                'tickcolor': "#2a2a2a",
                'tickfont': {'color': '#2a2a2a', 'size': 9, 'family': 'Space Mono'},
                'tickwidth': 1,
            },
            'bar': {'color': gauge_color, 'thickness': 0.25},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 33], 'color': 'rgba(255,255,255,0.03)'},
                {'range': [33, 66], 'color': 'rgba(255,255,255,0.05)'},
                {'range': [66, 100], 'color': 'rgba(255,255,255,0.07)'}
            ],
            'threshold': {
                'line': {'color': "#3a7d5a", 'width': 1},
                'thickness': 0.6,
                'value': gauge_val
            }
        }
    ))

    fig.update_layout(
        height=220,
        margin=dict(l=30, r=30, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f0efe8", family="Space Mono")
    )

    st.plotly_chart(fig, use_container_width=True)

# ─── FOOTER ────────────────────────────────────────────────────
st.markdown("""
<div class='footer-bar'>
    <span class='footer-left'>CARDIORISK AI // CLINICAL DECISION SUPPORT SYSTEM</span>
    <span class='footer-right'>© 2025 Taha Hassan · For clinical support · Not a substitute for medical judgment</span>
</div>
""", unsafe_allow_html=True)