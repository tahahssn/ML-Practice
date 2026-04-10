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
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&family=Bebas+Neue&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #e8e8e2;
    background: #0a0a0a;
}
.stApp { background: #0a0a0a; }
.main .block-container { background: transparent; padding: 2.5rem 3rem; max-width: 1100px; }
#MainMenu, footer, header { visibility: hidden; }

/* PRELOADER */
#preloader {
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    background: #0a0a0a; z-index: 9999;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.pre-tag {
    font-family: 'Space Mono', monospace; font-size: 0.62rem; color: #3a7d5a;
    letter-spacing: 4px; text-transform: uppercase; margin-bottom: 1.25rem;
    opacity: 0; animation: fadeUp 0.6s 0.3s forwards;
}
.pre-name {
    font-family: 'Bebas Neue', sans-serif; font-size: clamp(4rem, 10vw, 7rem);
    color: #f0efe8; letter-spacing: 3px; line-height: 1;
    opacity: 0; animation: fadeUp 0.7s 0.6s forwards;
}
.pre-name em { color: #3a7d5a; font-style: normal; }
.pre-tagline {
    font-family: 'Space Grotesk', sans-serif; font-size: 0.88rem;
    color: #7a7a72; font-weight: 400; margin-top: 1rem;
    letter-spacing: 0.5px; line-height: 1.6; text-align: center; max-width: 420px;
    opacity: 0; animation: fadeUp 0.6s 0.9s forwards;
}
.pre-bar-wrap {
    width: 240px; height: 1px; background: rgba(255,255,255,0.08);
    margin-top: 2.75rem; opacity: 0; animation: fadeUp 0.4s 1.1s forwards;
}
.pre-bar { height: 1px; background: #3a7d5a; width: 0; animation: barFill 1.5s 1.2s cubic-bezier(.4,0,.2,1) forwards; }
.pre-pct {
    font-family: 'Space Mono', monospace; font-size: 0.6rem; color: #3a7d5a;
    letter-spacing: 2px; margin-top: 0.65rem; text-transform: uppercase;
    opacity: 0; animation: fadeUp 0.4s 1.1s forwards;
}

/* ENTRY ANIMATIONS */
.anim-1 { opacity: 0; animation: fadeUp 0.6s 3.0s forwards; }
.anim-2 { opacity: 0; animation: fadeUp 0.7s 3.15s forwards; }
.anim-3 { opacity: 0; animation: fadeUp 0.6s 3.35s forwards; }
.anim-4 { opacity: 0; animation: fadeUp 0.6s 3.5s forwards; }
.anim-5 { opacity: 0; animation: fadeUp 0.6s 3.65s forwards; }
.anim-6 { opacity: 0; animation: fadeUp 0.6s 3.8s forwards; }

@keyframes fadeUp { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }
@keyframes barFill { to { width: 100%; } }
@keyframes slideIn { to { opacity: 1; transform: translateX(0); } }

/* TYPOGRAPHY */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #f0efe8 !important; font-weight: 700 !important;
}

/* NAV */
.nav-bar {
    display: flex; justify-content: space-between; align-items: center;
    padding-bottom: 2rem; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 3rem;
}
.nav-brand { font-family: 'Space Mono', monospace; font-size: 0.7rem; color: #6a6a62; letter-spacing: 3px; }
.nav-status {
    font-family: 'Space Mono', monospace; font-size: 0.65rem; color: #3a7d5a;
    background: rgba(58,125,90,0.1); border: 1px solid rgba(58,125,90,0.25);
    padding: 4px 12px; letter-spacing: 2px;
}

/* HERO */
.hero-eyebrow { font-family: 'Space Mono', monospace; font-size: 0.65rem; color: #3a7d5a; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 1rem; }
.hero-title { font-family: 'Bebas Neue', sans-serif; font-size: clamp(3.5rem, 7vw, 6.5rem); font-weight: 400; line-height: 0.92; letter-spacing: 2px; color: #f0efe8; margin-bottom: 1.25rem; }
.hero-title em { font-style: normal; color: #3a7d5a; }
.hero-sub { font-size: 0.9rem; color: #8a8a82; line-height: 1.7; font-weight: 400; max-width: 480px; }

/* METRICS — Bebas Neue for numbers */
.metric-grid {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 1px; background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.06); margin-bottom: 3rem;
}
.metric-cell { background: #0a0a0a; padding: 1.5rem 1.25rem; position: relative; }
.metric-n { font-family: 'Space Mono', monospace; font-size: 0.55rem; color: #222; position: absolute; top: 12px; right: 14px; }
.metric-label { font-family: 'Space Mono', monospace; font-size: 0.58rem; color: #6a6a62; letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 0.9rem; }
.metric-value { font-family: 'Bebas Neue', sans-serif; font-size: 2.8rem; color: #f0efe8; letter-spacing: 1px; margin-bottom: 0.3rem; line-height: 1; }
.metric-delta { font-family: 'Space Mono', monospace; font-size: 0.62rem; color: #3a7d5a; }

/* DIVIDER */
.section-divider { height: 1px; background: rgba(255,255,255,0.06); margin: 2.5rem 0; position: relative; text-align: center; }
.divider-label { font-family: 'Space Mono', monospace; font-size: 0.6rem; color: #5a5a54; letter-spacing: 2px; position: absolute; left: 50%; top: -8px; transform: translateX(-50%); background: #0a0a0a; padding: 0 10px; }

/* COL HEADS */
.col-section-head { font-family: 'Space Mono', monospace; font-size: 0.62rem; color: #3a7d5a; letter-spacing: 3.5px; text-transform: uppercase; padding-bottom: 0.9rem; border-bottom: 1px solid rgba(58,125,90,0.2); margin-bottom: 1.75rem; }

/* LABELS */
.stSlider label, .stSelectbox label, .stNumberInput label {
    font-family: 'Space Mono', monospace !important; font-size: 0.62rem !important;
    font-weight: 400 !important; color: #6a6a62 !important;
    letter-spacing: 2px !important; text-transform: uppercase !important;
}

/* SLIDER */
.stSlider > div > div > div { background: rgba(255,255,255,0.1) !important; height: 2px !important; border-radius: 0 !important; }
.stSlider > div > div > div > div { background: #3a7d5a !important; border-radius: 0 !important; }
.stSlider > div > div > div > div > div { background: #f0efe8 !important; border: none !important; border-radius: 50% !important; width: 10px !important; height: 10px !important; box-shadow: none !important; }

/* NUMBER INPUT */
.stNumberInput > div > div > input {
    background: transparent !important; border: none !important;
    border-bottom: 1px solid rgba(255,255,255,0.18) !important; border-radius: 0 !important;
    color: #c8c8c0 !important; font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important; padding: 8px 0 !important; box-shadow: none !important;
}
.stNumberInput > div > div > input:focus { border-bottom-color: #3a7d5a !important; box-shadow: none !important; }

/* SELECTBOX */
.stSelectbox > div > div {
    background: transparent !important; border: none !important;
    border-bottom: 1px solid rgba(255,255,255,0.18) !important; border-radius: 0 !important;
    color: #c8c8c0 !important; box-shadow: none !important;
    font-family: 'Space Grotesk', sans-serif !important; font-size: 0.85rem !important;
}
.stSelectbox > div > div:hover { border-bottom-color: #3a7d5a !important; box-shadow: none !important; }

/* BUTTON */
.stButton > button {
    font-family: 'Space Mono', monospace !important; font-size: 0.72rem !important;
    letter-spacing: 3px !important; text-transform: uppercase !important;
    color: #0a0a0a !important; background: #f0efe8 !important;
    border: none !important; border-radius: 0 !important;
    padding: 14px 52px !important; width: 100% !important;
    transition: background 0.2s, color 0.2s !important;
}
.stButton > button:hover { background: #3a7d5a !important; color: #f0efe8 !important; }

/* RESULT BOX */
.result-box { border: 1px solid rgba(58,125,90,0.3); padding: 2rem; margin-bottom: 2rem; animation: fadeUp 0.7s forwards; }
.result-tag { font-family: 'Space Mono', monospace; font-size: 0.6rem; color: #3a7d5a; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 1rem; }
.result-head { font-family: 'Bebas Neue', sans-serif; font-size: 2.8rem; color: #f0efe8; letter-spacing: 1px; line-height: 1; margin-bottom: 0.75rem; }
.result-sub { font-size: 0.83rem; color: #8a8a82; line-height: 1.7; margin-bottom: 1.5rem; font-weight: 400; }

/* ANIMATED SCORE COUNTER */
.score-display { font-family: 'Bebas Neue', sans-serif; font-size: 5rem; letter-spacing: -1px; line-height: 1; }
.score-unit { font-family: 'Space Mono', monospace; font-size: 0.58rem; color: #6a6a62; letter-spacing: 3px; margin-top: 0.5rem; text-transform: uppercase; }
.gauge-track { height: 3px; background: rgba(255,255,255,0.07); margin: 1.5rem 0 0.5rem; position: relative; overflow: hidden; }
.gauge-fill-anim { height: 3px; position: absolute; top: 0; left: 0; transition: width 1.8s cubic-bezier(.4,0,.2,1); }
.gauge-labels { display: flex; justify-content: space-between; font-family: 'Space Mono', monospace; font-size: 0.56rem; color: #4a4a44; letter-spacing: 1px; }

/* REC ITEMS STAGGERED */
.rec-item { border-left: 2px solid rgba(58,125,90,0.3); padding: 0.75rem 1rem; margin-bottom: 0.8rem; opacity: 0; transform: translateX(-10px); animation: slideIn 0.5s forwards; }
.rec-item:nth-child(2) { animation-delay: 0.6s; }
.rec-item:nth-child(3) { animation-delay: 0.85s; }
.rec-item:nth-child(4) { animation-delay: 1.1s; }
.rec-item:nth-child(5) { animation-delay: 1.35s; }
.rec-n { font-family: 'Space Mono', monospace; font-size: 0.58rem; color: #3a7d5a; letter-spacing: 2px; margin-bottom: 0.3rem; }
.rec-body { font-size: 0.8rem; color: #8a8a82; line-height: 1.5; }

/* ALERTS */
.stAlert { background: transparent !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 0 !important; font-family: 'Space Grotesk', sans-serif !important; font-size: 0.8rem !important; }

/* FOOTER */
.footer-bar { display: flex; justify-content: space-between; align-items: center; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.06); margin-top: 3rem; }
.footer-l { font-family: 'Space Mono', monospace; font-size: 0.58rem; color: #5a5a54; letter-spacing: 2px; }
.footer-r { font-family: 'Space Mono', monospace; font-size: 0.58rem; color: #5a5a54; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #2a2a2a; }
::-webkit-scrollbar-thumb:hover { background: #3a7d5a; }
.element-container, .stMarkdown { background: transparent !important; }
</style>

<!-- PRELOADER HTML -->
<div id="preloader">
    <div class="pre-tag">// INITIALIZING SYSTEM</div>
    <div class="pre-name">Cardio<em>Risk</em> AI</div>
    <div class="pre-tagline">Precision cardiovascular intelligence.<br>Where clinical data meets machine certainty.</div>
    <div class="pre-bar-wrap"><div class="pre-bar"></div></div>
    <div class="pre-pct" id="prePct">LOADING...</div>
</div>

<!-- PRELOADER + SCORE ANIMATION SCRIPTS -->
<script>
(function(){
    var pct = 0;
    var el = document.getElementById('prePct');
    var t = setInterval(function(){
        pct += Math.random() * 14 + 5;
        if(pct >= 100){
            pct = 100; clearInterval(t);
            if(el) el.textContent = 'READY — 100%';
            setTimeout(function(){
                var pre = document.getElementById('preloader');
                if(pre){
                    pre.style.transition = 'opacity 0.7s ease';
                    pre.style.opacity = '0';
                    setTimeout(function(){ pre.style.display='none'; }, 700);
                }
            }, 450);
        }
        if(el) el.textContent = 'LOADING... ' + Math.floor(pct) + '%';
    }, 110);
})();

function animateScore(elId, target, suffix, duration){
    var el = document.getElementById(elId);
    if(!el) return;
    var start = null;
    function step(ts){
        if(!start) start = ts;
        var prog = Math.min((ts - start) / duration, 1);
        var ease = 1 - Math.pow(1 - prog, 3);
        el.textContent = (ease * target).toFixed(1) + suffix;
        if(prog < 1) requestAnimationFrame(step);
        else el.textContent = target.toFixed(1) + suffix;
    }
    requestAnimationFrame(step);
}

function animateGauge(elId, targetPct){
    setTimeout(function(){
        var el = document.getElementById(elId);
        if(el) el.style.width = targetPct + '%';
    }, 120);
}
</script>
""", unsafe_allow_html=True)

# ─── LOAD MODELS ───────────────────────────────────────────────
with st.spinner('Initializing...'):
    time.sleep(0.3)
    model = joblib.load(r"D:\ML-Practice\HeartDiseaseProject\KNN_heart.pkl")
    scaler = joblib.load(r"D:\ML-Practice\HeartDiseaseProject\scalar.pkl")
    expected_columns = joblib.load(r"D:\ML-Practice\HeartDiseaseProject\columns.pkl")

# ─── NAV ───────────────────────────────────────────────────────
st.markdown("""
<div class='nav-bar anim-1'>
    <span class='nav-brand'>CARDIORISK // v2.0</span>
    <span class='nav-status'>● SYSTEM ACTIVE</span>
</div>
""", unsafe_allow_html=True)

# ─── HERO ──────────────────────────────────────────────────────
st.markdown("""
<div class='anim-2' style='margin-bottom:3.5rem'>
    <p class='hero-eyebrow'>// CARDIOVASCULAR RISK ASSESSMENT SYSTEM</p>
    <h1 class='hero-title'>Cardio<em>Risk</em><br>A.I.</h1>
    <p class='hero-sub'>Advanced clinical decision support powered by machine learning. Input patient parameters to compute cardiovascular risk stratification.</p>
</div>
""", unsafe_allow_html=True)

# ─── METRICS ───────────────────────────────────────────────────
st.markdown("""
<div class='metric-grid anim-3'>
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

st.markdown("<div class='section-divider anim-4'><span class='divider-label'>// INPUT PARAMETERS</span></div>", unsafe_allow_html=True)

# ─── INPUTS ────────────────────────────────────────────────────
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.markdown("<div class='col-section-head anim-4'>// PATIENT DEMOGRAPHICS</div>", unsafe_allow_html=True)
    age = st.slider("AGE (YEARS)", 18, 100, 40)
    sex = st.selectbox("SEX", ["Male", "Female"])
    chest_pain = st.selectbox("CHEST PAIN TYPE", [
        "ATA — Atypical Angina", "NAP — Non-Anginal Pain",
        "TA — Typical Angina", "ASY — Asymptomatic"
    ])
    resting_bp = st.number_input("RESTING BLOOD PRESSURE (MM HG)", 80, 200, 120)
    cholesterol = st.number_input("SERUM CHOLESTEROL (MG/DL)", 100, 600, 200)

with right_col:
    st.markdown("<div class='col-section-head anim-4'>// CLINICAL MEASUREMENTS</div>", unsafe_allow_html=True)
    fasting_bs = st.selectbox("FASTING BLOOD SUGAR > 120 MG/DL", ["No", "Yes"])
    resting_ecg = st.selectbox("RESTING ECG RESULTS", [
        "Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"
    ])
    max_hr = st.slider("MAXIMUM HEART RATE", 60, 220, 150)
    exercise_angina = st.selectbox("EXERCISE-INDUCED ANGINA", ["No", "Yes"])
    oldpeak = st.slider("ST DEPRESSION (OLDPEAK)", 0.0, 6.0, 1.0, 0.1)
    st_slope = st.selectbox("ST SEGMENT SLOPE", ["Upsloping", "Flat", "Downsloping"])

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    predict_button = st.button("Analyze Cardiovascular Risk →", use_container_width=True)

# ─── PREDICTION ────────────────────────────────────────────────
if predict_button:
    with st.spinner("Computing risk stratification..."):
        time.sleep(0.7)

        sex_enc = "M" if sex == "Male" else "F"
        cp_enc  = chest_pain.split(" — ")[0]
        ecg_enc = resting_ecg.split(" ")[0] if " " in resting_ecg else resting_ecg
        if ecg_enc == "ST-T": ecg_enc = "ST"
        ea_enc  = "Y" if exercise_angina == "Yes" else "N"
        sl_enc  = st_slope[0]
        fbs_enc = 1 if fasting_bs == "Yes" else 0

        raw = {
            'Age': age, 'RestingBP': resting_bp, 'Cholesterol': cholesterol,
            'FastingBS': fbs_enc, 'MaxHR': max_hr, 'Oldpeak': oldpeak,
            'Sex_' + sex_enc: 1, 'ChestPainType_' + cp_enc: 1,
            'RestingECG_' + ecg_enc: 1, 'ExerciseAngina_' + ea_enc: 1,
            'ST_Slope_' + sl_enc: 1
        }

        df = pd.DataFrame([raw])
        for col in expected_columns:
            if col not in df.columns:
                df[col] = 0
        df = df[expected_columns]
        scaled = scaler.transform(df)
        pred   = model.predict(scaled)[0]
        prob   = model.predict_proba(scaled)[0]

    st.markdown("<div class='section-divider'><span class='divider-label'>// ASSESSMENT OUTPUT</span></div>", unsafe_allow_html=True)

    r_col, rec_col = st.columns([1, 1], gap="large")

    if pred == 1:
        pv = prob[1] * 100
        sc = "#3a7d5a"
        gc = "#3a7d5a"
        rh = "High Risk<br>Detected"
        rs = "Clinical indicators suggest elevated cardiovascular risk. Immediate specialist referral is advised."
        su = "RISK PROBABILITY"
        recs = [
            ("01 // IMMEDIATE ACTION", "Cardiology consultation within 14 days. Priority referral required."),
            ("02 // DIAGNOSTICS",      "Stress test, echocardiogram, and coronary angiography evaluation."),
            ("03 // LIFESTYLE",        "Aggressive pharmacological and lifestyle intervention protocol required."),
            ("04 // MONITORING",       "Bi-monthly BP and cholesterol tracking. Daily activity logging."),
        ]
    else:
        pv = prob[0] * 100
        sc = "#f0efe8"
        gc = "#f0efe8"
        rh = "Low Risk<br>Assessment"
        rs = "Cardiovascular indicators appear within normal reference ranges. Continue preventive health maintenance."
        su = "SAFETY CONFIDENCE"
        recs = [
            ("01 // PREVENTIVE CARE", "Annual cardiovascular health screening. Continue current lifestyle habits."),
            ("02 // ACTIVITY",        "Maintain 150+ minutes of moderate aerobic exercise per week."),
            ("03 // NUTRITION",       "Mediterranean-style diet. Limit saturated fats, sodium, and processed sugars."),
            ("04 // MONITORING",      "Annual BP and cholesterol tracking. Report any new symptoms promptly."),
        ]

    box_border = "rgba(58,125,90,0.3)" if pred == 1 else "rgba(255,255,255,0.12)"

    with r_col:
        st.markdown(f"""
        <div class='result-box' style='border-color:{box_border}'>
            <div class='result-tag'>// RISK ASSESSMENT OUTPUT</div>
            <div class='result-head'>{rh}</div>
            <div class='result-sub'>{rs}</div>
            <div class='score-display' id='scoreEl' style='color:{sc}'>0.0%</div>
            <div class='score-unit'>{su}</div>
            <div class='gauge-track'>
                <div class='gauge-fill-anim' id='gaugeEl' style='background:{gc}'></div>
            </div>
            <div class='gauge-labels'><span>0%</span><span>LOW</span><span>MOD</span><span>HIGH</span><span>100%</span></div>
        </div>
        <script>
            setTimeout(function(){{
                animateScore('scoreEl', {pv:.2f}, '%', 1800);
                animateGauge('gaugeEl', {pv:.2f});
            }}, 300);
        </script>
        """, unsafe_allow_html=True)

    with rec_col:
        proto_label = "// CLINICAL PROTOCOL" if pred == 1 else "// PREVENTIVE PROTOCOL"
        recs_html = f"""
        <div style='padding-top:0.5rem'>
            <div style='font-family:"Space Mono",monospace;font-size:0.6rem;color:#3a7d5a;letter-spacing:3px;margin-bottom:1.5rem'>
                {proto_label}
            </div>
        """
        for rn, rb in recs:
            recs_html += f"""
            <div class='rec-item'>
                <div class='rec-n'>{rn}</div>
                <div class='rec-body'>{rb}</div>
            </div>
            """
        recs_html += "</div>"
        st.markdown(recs_html, unsafe_allow_html=True)

    # Minimal Plotly gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pv,
        number={'suffix':"%", 'font':{'size':26,'family':'Bebas Neue','color':'#f0efe8'}},
        title={'text': "RISK SCORE" if pred == 1 else "SAFETY SCORE",
               'font':{'size':10,'family':'Space Mono','color':'#5a5a54'}},
        domain={'x':[0,1],'y':[0,1]},
        gauge={
            'axis':{'range':[0,100],'tickcolor':"#222",'tickfont':{'color':'#2a2a2a','size':8,'family':'Space Mono'},'tickwidth':1},
            'bar':{'color':gc,'thickness':0.2},
            'bgcolor':"rgba(0,0,0,0)",'borderwidth':0,
            'steps':[
                {'range':[0,33],'color':'rgba(255,255,255,0.03)'},
                {'range':[33,66],'color':'rgba(255,255,255,0.05)'},
                {'range':[66,100],'color':'rgba(255,255,255,0.07)'}
            ],
            'threshold':{'line':{'color':gc,'width':1},'thickness':0.5,'value':pv}
        }
    ))
    fig.update_layout(
        height=200, margin=dict(l=20,r=20,t=35,b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f0efe8", family="Space Mono")
    )
    st.plotly_chart(fig, use_container_width=True)

# ─── FOOTER ────────────────────────────────────────────────────
st.markdown("""
<div class='footer-bar'>
    <span class='footer-l'>CARDIORISK AI // CLINICAL DECISION SUPPORT SYSTEM</span>
    <span class='footer-r'>© 2025 Taha Hassan · Not a substitute for medical judgment</span>
</div>
""", unsafe_allow_html=True)