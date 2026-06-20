import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json

# ─────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SYVORA FINANCE — Loan Approval",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────
#  DESIGN TOKENS  (Lumina Predict design system)
# ─────────────────────────────────────────────────────────────────────────
# Surfaces
BG          = "#0b1326"   # page background
BG_SIDEBAR  = "#0c1424"   # sidebar background
CARD        = "#171f33"   # surface-container
CARD_HIGH   = "#1b2336"   # inputs
CARD_HIGHEST= "#222a3d"
BORDER      = "#2a3247"   # outline-variant
BORDER_SOFT = "#1f2738"
TEXT        = "#e7ecfd"   # on-surface
TEXT_DIM    = "#9aa3bd"   # on-surface-variant
TEXT_FAINT  = "#6b7390"

# Accents
BLUE        = "#3B82F6"   # primary
BLUE_SOFT   = "rgba(59,130,246,0.14)"
BLUE_LIGHT  = "#adc6ff"
GREEN       = "#10B981"   # secondary / success
GREEN_SOFT  = "rgba(16,185,129,0.14)"
RED         = "#ef4444"   # error
RED_SOFT    = "rgba(239,68,68,0.14)"

# ─────────────────────────────────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Hanken+Grotesk:wght@600;700;800&display=swap');

html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

.stApp {{
    background: {BG};
    color: {TEXT};
}}

/* Hide default chrome */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    height: 2.5rem;
}}
div[data-testid="stToolbar"] {{ right: 1rem; }}

.block-container {{
    padding-top: 1.5rem !important;
    padding-bottom: 4rem !important;
    max-width: 1180px;
}}

h1,h2,h3,h4 {{ font-family: 'Hanken Grotesk', sans-serif; color: {TEXT}; }}

/* ── Sidebar ───────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {{
    background: {BG_SIDEBAR};
    border-right: 1px solid {BORDER_SOFT};
}}
section[data-testid="stSidebar"] .block-container {{ padding-top: 2rem; }}

.lp-logo {{
    font-family: 'Hanken Grotesk', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: {BLUE_LIGHT};
    letter-spacing: -0.02em;
    margin-bottom: 2px;
}}
.lp-logo-sub {{
    font-size: 0.78rem;
    color: {TEXT_DIM};
    margin-bottom: 22px;
}}
.lp-nav-item {{
    display: flex; align-items: center; gap: 10px;
    padding: 11px 14px; border-radius: 10px;
    font-size: 0.75rem; font-weight: 700; letter-spacing: 0.06em;
    text-transform: uppercase; text-decoration: none !important;
    margin-bottom: 6px; transition: all .15s ease;
}}
.lp-nav-item.active {{
    background: {GREEN};
    color: #00231a;
}}
.lp-nav-item:not(.active) {{
    color: {TEXT_DIM};
}}
.lp-nav-item:not(.active):hover {{ background: rgba(255,255,255,0.04); }}

.lp-sidebar-divider {{
    height: 1px; background: {BORDER_SOFT}; margin: 18px 0;
}}
.lp-about-title {{
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; color: {BLUE_LIGHT}; margin-bottom: 10px;
}}
.lp-about-text {{ font-size: 0.85rem; color: {TEXT_DIM}; line-height: 1.65; }}
.lp-about-text b {{ color: {TEXT}; }}
.lp-disclaimer {{
    font-size: 0.76rem; color: {TEXT_FAINT}; line-height: 1.55;
    background: {CARD}; border: 1px solid {BORDER_SOFT};
    border-radius: 10px; padding: 12px 14px; margin-top: 18px;
}}

/* ── Top header bar (custom, in main content) ─────────────────────── */
.lp-header {{
    display: flex; justify-content: space-between; align-items: center;
    padding: 14px 22px; margin-bottom: 28px;
    background: rgba(23,31,51,0.7);
    backdrop-filter: blur(16px);
    border: 1px solid {BORDER_SOFT}; border-radius: 16px;
}}
.lp-header-brand {{
    font-family: 'Hanken Grotesk', sans-serif; font-weight: 800;
    font-size: 1.3rem; color: {BLUE_LIGHT}; letter-spacing: -0.02em;
}}
.lp-header-nav {{ display: flex; gap: 28px; }}
.lp-header-nav span {{ font-size: 0.92rem; color: {TEXT_DIM}; font-weight: 500; }}
.lp-header-nav span.active {{ color: {BLUE_LIGHT}; font-weight: 700; border-bottom: 2px solid {BLUE_LIGHT}; padding-bottom: 4px; }}
.lp-header-icons {{ display: flex; align-items: center; gap: 16px; }}
.lp-avatar {{
    width: 36px; height: 36px; border-radius: 50%;
    background: linear-gradient(135deg, {BLUE}, {BLUE_LIGHT});
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; border: 2px solid rgba(173,198,255,0.3);
}}

/* ── Hero banner ───────────────────────────────────────────────────── */
.lp-hero {{
    display: flex; align-items: center; gap: 28px;
    background: rgba(23,31,51,0.55);
    backdrop-filter: blur(20px);
    border: 1px solid {BORDER_SOFT}; border-radius: 20px;
    padding: 38px; margin-bottom: 34px;
}}
.lp-hero-icon {{
    flex-shrink: 0; width: 88px; height: 88px; border-radius: 18px;
    background: linear-gradient(135deg, {BLUE}, #2563eb);
    display: flex; align-items: center; justify-content: center;
    font-size: 2.4rem; box-shadow: 0 8px 28px rgba(59,130,246,0.35);
}}
.lp-hero-title {{
    font-family: 'Hanken Grotesk', sans-serif; font-weight: 700;
    font-size: 2.1rem; letter-spacing: -0.02em; color: {TEXT}; margin: 0;
}}
.lp-hero-sub {{ color: {TEXT_DIM}; font-size: 0.97rem; margin-top: 6px; max-width: 680px; }}

/* ── Section headers ───────────────────────────────────────────────── */
.lp-section-head {{
    display: flex; align-items: center; gap: 9px;
    color: {BLUE_LIGHT}; font-size: 0.74rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    margin: 30px 0 4px 0;
}}
.lp-section-divider {{ height: 1px; background: {BORDER_SOFT}; margin-bottom: 18px; }}

/* ── Form inputs ───────────────────────────────────────────────────── */
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInputContainer"] {{
    background: {CARD_HIGH} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
}}
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stSlider"] label,
div[data-testid="stRadio"] label[data-testid="stWidgetLabel"] {{
    color: {TEXT_DIM} !important; font-size: 0.85rem !important; font-weight: 500 !important;
}}
div[data-baseweb="base-input"] {{ background: transparent !important; }}
input[data-testid="stNumberInputField"] {{
    color: {TEXT} !important; background: transparent !important;
}}
button[data-testid="stNumberInputStepUp"],
button[data-testid="stNumberInputStepDown"] {{
    background: {CARD_HIGHEST} !important;
}}
button[data-testid="stNumberInputStepUp"] svg,
button[data-testid="stNumberInputStepDown"] svg {{
    color: {TEXT_DIM} !important;
}}

/* Radio as pill toggle group */
div[data-testid="stRadio"] > div[role="radiogroup"] {{
    display: flex; gap: 8px; flex-wrap: nowrap;
}}
div[data-testid="stRadio"] label[data-baseweb="radio"] {{
    background: {CARD_HIGH} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
    padding: 10px 10px !important;
    flex: 1; justify-content: center !important;
    transition: all .15s ease; margin: 0 !important;
    white-space: nowrap;
}}
div[data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child {{ display: none; }}
div[data-testid="stRadio"] label[data-baseweb="radio"] p {{
    white-space: nowrap !important; font-size: 0.88rem !important;
}}
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {{
    background: {BLUE_SOFT} !important; border-color: {BLUE} !important;
}}
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p {{
    color: {BLUE_LIGHT} !important; font-weight: 700 !important;
}}

/* Sliders */
div[data-testid="stSlider"] [data-baseweb="slider"] {{ margin-top: 6px; }}
div[data-testid="stSlider"] [role="slider"] {{
    background-color: {BLUE} !important;
    border: 3px solid #ffffff !important;
    box-shadow: 0 0 14px rgba(59,130,246,0.5) !important;
}}
div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div {{
    background: {BLUE} !important;
}}
div[data-testid="stSliderThumbValue"] p {{
    color: {BLUE_LIGHT} !important; font-weight: 700 !important; font-size: 0.95rem !important;
}}
div[data-testid="stSliderTickBar"] p {{
    color: {TEXT_FAINT} !important; font-size: 0.7rem !important;
}}

/* Bordered containers -> glass cards */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: rgba(23,31,51,0.55) !important;
    backdrop-filter: blur(14px);
    border: 1px solid {BORDER_SOFT} !important;
    border-radius: 16px !important;
}}

/* Buttons */
div.stButton > button {{
    background: linear-gradient(135deg, {BLUE}, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    padding: 0.7rem 1.2rem !important;
    transition: all .2s ease !important;
    box-shadow: 0 4px 16px rgba(59,130,246,0.25);
}}
div.stButton > button:hover {{
    box-shadow: 0 4px 22px rgba(59,130,246,0.5);
    transform: translateY(-1px);
}}
div.stButton > button p {{ font-size: 0.95rem !important; }}

/* Progress bar */
div[data-testid="stProgress"] > div > div > div {{
    background: linear-gradient(90deg, {BLUE}, {BLUE_LIGHT}) !important;
}}

/* Metric cards */
.lp-metric-row {{ display: flex; gap: 14px; margin-top: 14px; flex-wrap: wrap; }}
.lp-metric-card {{
    flex: 1; min-width: 140px;
    background: {CARD}; border: 1px solid {BORDER_SOFT}; border-radius: 14px;
    padding: 16px 18px;
}}
.lp-metric-val {{ font-family: 'Inter', sans-serif; font-size: 1.35rem; font-weight: 700; color: {BLUE_LIGHT}; }}
.lp-metric-lbl {{ font-size: 0.72rem; color: {TEXT_DIM}; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 3px; }}

/* Result cards */
.lp-result {{
    border-radius: 18px; padding: 28px 32px; margin: 26px 0 10px 0;
    display: flex; align-items: center; gap: 20px;
}}
.lp-result.approved {{ background: {GREEN_SOFT}; border: 1px solid {GREEN}; }}
.lp-result.rejected {{ background: {RED_SOFT}; border: 1px solid {RED}; }}
.lp-result-icon {{
    width: 56px; height: 56px; border-radius: 14px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; font-size: 1.6rem;
}}
.lp-result.approved .lp-result-icon {{ background: rgba(16,185,129,0.2); }}
.lp-result.rejected .lp-result-icon {{ background: rgba(239,68,68,0.2); }}
.lp-result-title {{ font-family: 'Hanken Grotesk', sans-serif; font-size: 1.5rem; font-weight: 700; color: {TEXT}; margin: 0; }}
.lp-result-sub {{ color: {TEXT_DIM}; font-size: 0.9rem; margin-top: 4px; }}
.lp-result.approved .lp-result-title {{ color: {GREEN}; }}
.lp-result.rejected .lp-result-title {{ color: {RED}; }}

/* Property image block */
.lp-property-img {{
    width: 100%; height: 84px; border-radius: 14px;
    background: linear-gradient(135deg, #1e3a5f, #2563eb 70%);
    display: flex; align-items: center; justify-content: center;
    font-size: 2.2rem;
}}

/* Warning box */
.lp-warning {{
    background: rgba(251,191,36,0.1); border: 1px solid #fbbf24;
    border-radius: 12px; padding: 14px 18px; font-size: 0.88rem;
    color: #fbbf24; margin-bottom: 20px;
}}

/* Slider value display */
.lp-slider-row {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 2px; }}
.lp-slider-label {{ font-size: 0.85rem; color: {TEXT_DIM}; }}
.lp-slider-val {{ font-family: 'Inter', sans-serif; font-size: 1.25rem; font-weight: 700; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────
#  LOAD MODEL ARTIFACTS
# ─────────────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    try:
        model    = joblib.load("../Model/loan_model.pkl")
        scaler   = joblib.load("../Model/scaler.pkl")
        selector = joblib.load("../Model/selector.pkl")
        with open("../Model/feature_names.json") as f:
            feature_names = json.load(f)
        return model, scaler, selector, feature_names, True
    except Exception:
        return None, None, None, None, False

model, scaler, selector, feature_names, model_loaded = load_model()

# ─────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────
import base64, pathlib

def _img_to_b64(path: str) -> str:
    """Return a base64 data-URI for the given image file."""
    data = pathlib.Path(path).read_bytes()
    ext  = pathlib.Path(path).suffix.lstrip(".")
    mime = "png" if ext == "png" else "jpeg"
    return f"data:image/{mime};base64,{base64.b64encode(data).decode()}"

_logo_b64 = _img_to_b64("C:/Users/shrey/Downloads/syvoralogo.png")

with st.sidebar:
    st.markdown(f'''
        <div class="lp-logo">
            <div>
                <img src="{_logo_b64}" alt="Syvora Finance Logo"
                     style="height:48px;width:48px;object-fit:contain;border-radius:8px;">
                <span>Loan Predictor</span>
            </div>
        </div>''', unsafe_allow_html=True)
    st.markdown('<div class="lp-logo-sub">SYVORA FINANCE · AI Loan Engine</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <a class="lp-nav-item active" href="#personal-information">👤 Personal Info</a>
    <a class="lp-nav-item" href="#financial-details">💳 Financials</a>
    <a class="lp-nav-item" href="#property-details">📍 Property</a>
    <a class="lp-nav-item" href="#prediction-result">📊 Result</a>
    """, unsafe_allow_html=True)

    st.markdown('<div class="lp-sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="lp-about-title">About This App</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="lp-about-text">
    Built for the <b>AIML Summer Internship 2026</b> at IIHMF, MNNIT Allahabad.
    <br><br>
    <b>Models Trained (6):</b><br>
    Logistic Regression · Decision Tree · Random Forest · SVM · KNN · XGBoost
    <br><br>
    <b>Dataset:</b> Kaggle Loan Prediction Dataset
    <br><br>
    <b>Techniques:</b><br>
    SMOTE balancing · Feature engineering (EMI, TotalIncome, BalanceIncome) ·
    SelectKBest feature selection · GridSearchCV tuning
    <br><br>
    <b>Metrics:</b> Accuracy · Precision · Recall · F1 · ROC-AUC
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="lp-disclaimer">
    ⚠️ Educational tool only. Real loan decisions depend on many additional factors
    not captured by this model.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────
#  CUSTOM TOP HEADER
# ─────────────────────────────────────────────────────────────────────────
import base64, pathlib

def _img_to_b64(path: str) -> str:
    """Return a base64 data-URI for the given image file."""
    data = pathlib.Path(path).read_bytes()
    ext  = pathlib.Path(path).suffix.lstrip(".")
    mime = "png" if ext == "png" else "jpeg"
    return f"data:image/{mime};base64,{base64.b64encode(data).decode()}"

_logo_b64 = _img_to_b64("C:/Users/shrey/Downloads/syvoralogo.png")

st.markdown(f"""
<div class="lp-header">
    <div style="display:flex;align-items:center;gap:12px;">
        <img src="{_logo_b64}" alt="Syvora Finance Logo"
             style="height:48px;width:48px;object-fit:contain;border-radius:8px;">
        <span class="lp-header-brand">SYVORA FINANCE</span>
    </div>
    
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="lp-hero">
    <div>
        <span class="lp-hero-title">Loan Approval Predictor</span>
    </div>
</div>
""", unsafe_allow_html=True)

if not model_loaded:
    st.markdown("""
    <div class="lp-warning">
    ⚠️ <strong>Model files not found.</strong> Upload <code>loan_model.pkl</code>,
    <code>scaler.pkl</code>, <code>selector.pkl</code>, and <code>feature_names.json</code>
    to the same folder as this app, then redeploy.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────
#  PERSONAL INFORMATION
# ─────────────────────────────────────────────────────────────────────────
st.markdown('<div id="personal-information"></div>', unsafe_allow_html=True)
st.markdown('<div class="lp-section-head">👤 Personal Information</div>', unsafe_allow_html=True)
st.markdown('<div class="lp-section-divider"></div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    gender = st.selectbox("Gender", ["Male", "Female"])
with c2:
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
with c3:
    st.markdown('<p style="font-size:0.85rem;color:#9aa3bd;margin-bottom:4px;">Marital Status</p>', unsafe_allow_html=True)
    married = st.radio("Marital Status", ["Yes", "No"], horizontal=True, label_visibility="collapsed")

c4, c5, c6 = st.columns(3)
with c4:
    dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
with c5:
    self_employed = st.selectbox("Self Employed", ["No", "Yes"])
with c6:
    st.markdown('<p style="font-size:0.85rem;color:#9aa3bd;margin-bottom:4px;">Credit History</p>', unsafe_allow_html=True)
    credit_label = st.radio("Credit History", ["Good (1.0)", "Poor (0.0)"], horizontal=True, label_visibility="collapsed")
    credit_history = 1 if credit_label.startswith("Good") else 0

# ─────────────────────────────────────────────────────────────────────────
#  FINANCIAL DETAILS
# ─────────────────────────────────────────────────────────────────────────
st.markdown('<div id="financial-details"></div>', unsafe_allow_html=True)
st.markdown('<div class="lp-section-head">💳 Financial Details</div>', unsafe_allow_html=True)
st.markdown('<div class="lp-section-divider"></div>', unsafe_allow_html=True)

fc1, fc2 = st.columns(2)
with fc1:
    with st.container(border=True):
        applicant_income = st.slider(
            "Applicant Monthly Income (₹)", min_value=5000, max_value=500000,
            value=50000, step=5000, format="₹%d"
        )
with fc2:
    with st.container(border=True):
        loan_amount = st.slider(
            "Loan Amount (₹ thousands)", min_value=10, max_value=1000,
            value=150, step=10, format="%dk"
        )

fc3, fc4 = st.columns(2)
with fc3:
    coapplicant_income = st.number_input("Co-applicant Monthly Income (₹)", min_value=0, value=0, step=1000)
with fc4:
    loan_term = st.selectbox("Loan Term (months)", [360, 180, 120, 84, 60, 240, 300, 480])

# ─────────────────────────────────────────────────────────────────────────
#  PROPERTY DETAILS
# ─────────────────────────────────────────────────────────────────────────
st.markdown('<div id="property-details"></div>', unsafe_allow_html=True)
st.markdown('<div class="lp-section-head">📍 Property Details</div>', unsafe_allow_html=True)
st.markdown('<div class="lp-section-divider"></div>', unsafe_allow_html=True)

pc1, pc2 = st.columns([2, 1])
with pc1:
    with st.container(border=True):
        ic1, ic2 = st.columns([1, 3])
        with ic1:
            st.markdown('<div class="lp-property-img">🏙️</div>', unsafe_allow_html=True)
        with ic2:
            property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])
with pc2:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    predict_btn = st.button("📊 Predict Loan Approval", use_container_width=True, type="primary")

# ─────────────────────────────────────────────────────────────────────────
#  PREDICTION LOGIC
# ─────────────────────────────────────────────────────────────────────────
def encode_inputs():
    dep_map  = {"0": 0, "1": 1, "2": 2, "3+": 3}
    area_map = {"Rural": 0, "Semiurban": 1, "Urban": 2}

    gender_enc   = 1 if gender == "Male" else 0
    married_enc  = 1 if married == "Yes" else 0
    dep_enc      = dep_map[dependents]
    edu_enc      = 1 if education == "Graduate" else 0
    self_emp_enc = 1 if self_employed == "Yes" else 0
    area_enc     = area_map[property_area]

    total_income    = applicant_income + coapplicant_income
    loan_amount_log = np.log1p(loan_amount)
    emi             = loan_amount / loan_term if loan_term > 0 else 0
    balance_income  = total_income - (emi * 1000)

    raw = {
        "Gender":          gender_enc,
        "Married":         married_enc,
        "Dependents":      dep_enc,
        "Education":       edu_enc,
        "Self_Employed":   self_emp_enc,
        "Credit_History":  credit_history,
        "Property_Area":   area_enc,
        "TotalIncome":     total_income,
        "LoanAmountLog":   loan_amount_log,
        "EMI":             emi,
        "BalanceIncome":   balance_income,
    }
    return raw

st.markdown('<div id="prediction-result"></div>', unsafe_allow_html=True)

if predict_btn:
    if not model_loaded:
        st.error("❌ Cannot predict — model files are missing. See the warning above.")
    else:
        raw = encode_inputs()

        # ALL 11 engineered features — exact order the SELECTOR was fitted on
        ALL_FEATURES = [
            "Gender", "Married", "Dependents", "Education", "Self_Employed",
            "Credit_History", "Property_Area",
            "TotalIncome", "LoanAmountLog", "EMI", "BalanceIncome"
        ]
        input_df_full = pd.DataFrame([raw])[ALL_FEATURES]  # 11 features

        # Step 1: SELECT — SelectKBest reduces 11 → 8 features
        input_selected_arr = selector.transform(input_df_full)

        # Step 2: Re-wrap with exact column names the scaler was fit on
        input_selected_df = pd.DataFrame(input_selected_arr, columns=feature_names)

        # Step 3: SCALE — scaler was fit AFTER selection, on these 8 columns
        input_scaled = scaler.transform(input_selected_df)

        prediction = model.predict(input_scaled)[0]
        proba      = model.predict_proba(input_scaled)[0]
        confidence = proba[1] if prediction == 1 else proba[0]

        if prediction == 1:
            st.markdown(f"""
            <div class="lp-result approved">
                <div class="lp-result-icon">✅</div>
                <div>
                    <p class="lp-result-title">Loan Approved</p>
                    <p class="lp-result-sub">This application is likely to be approved · Confidence: <b>{confidence*100:.1f}%</b></p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="lp-result rejected">
                <div class="lp-result-icon">❌</div>
                <div>
                    <p class="lp-result-title">Loan Rejected</p>
                    <p class="lp-result-sub">This application is likely to be rejected · Confidence: <b>{confidence*100:.1f}%</b></p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<p class="lp-slider-label" style="margin-top:6px;">Prediction Confidence</p>', unsafe_allow_html=True)
        st.progress(float(confidence))

        total_income   = applicant_income + coapplicant_income
        emi_est        = (loan_amount * 1000) / loan_term if loan_term > 0 else 0
        emi_income_pct = (emi_est / total_income * 100) if total_income > 0 else 0

        st.markdown(f"""
        <div class="lp-metric-row">
            <div class="lp-metric-card">
                <div class="lp-metric-val">₹{total_income:,.0f}</div>
                <div class="lp-metric-lbl">Total Monthly Income</div>
            </div>
            <div class="lp-metric-card">
                <div class="lp-metric-val">₹{emi_est:,.0f}</div>
                <div class="lp-metric-lbl">Est. Monthly EMI</div>
            </div>
            <div class="lp-metric-card">
                <div class="lp-metric-val">{emi_income_pct:.1f}%</div>
                <div class="lp-metric-lbl">EMI / Income Ratio</div>
            </div>
            <div class="lp-metric-card">
                <div class="lp-metric-val" style="color:{'#10B981' if credit_history==1 else '#ef4444'}">
                    {"Good ✅" if credit_history == 1 else "Poor ❌"}
                </div>
                <div class="lp-metric-lbl">Credit History</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        prob_df = pd.DataFrame({
            "Outcome":     ["Approved", "Rejected"],
            "Probability": [f"{proba[1]*100:.2f}%", f"{proba[0]*100:.2f}%"]
        })
        st.dataframe(prob_df, hide_index=True, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; font-size:0.78rem; color:{TEXT_FAINT}; margin-top:48px; padding-top:18px; border-top:1px solid {BORDER_SOFT};">
    SYVORA FINANCE · AIML Capstone 2026 · IIHMF, MNNIT Allahabad, Prayagraj
</div>
""", unsafe_allow_html=True)
