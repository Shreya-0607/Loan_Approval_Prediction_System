"""
Prediction utility — loads the trained pipeline artifacts and exposes
a single predict_loan_approval(form_data) function.

Pipeline order at inference MUST mirror training exactly (see
Notebook/LoanApprovalPrediction.ipynb, Phase 5 "Feature Engineering"
and Cell 9 "Feature Selection"):

  1. Build the 11 engineered features, in training column order:
     Gender, Married, Dependents, Education, Self_Employed,
     Credit_History, Property_Area, TotalIncome, LoanAmountLog, EMI,
     BalanceIncome
     (categoricals are sklearn LabelEncoder-style codes: alphabetical
     order of the category strings, e.g. Female=0/Male=1,
     Rural=0/Semiurban=1/Urban=2)
  2. selector.transform(...)   -> the 8 chi2-selected columns
  3. scaler.transform(...)     -> standardized
  4. model.predict / predict_proba

NOTE: this previously built the *old* one-hot raw-feature row
(ApplicantIncome, Property_Area_Rural, ...), which doesn't match what
this Model/ folder's selector/scaler/model were actually fit on and
crashed with a sklearn feature-name ValueError. This file was
corrected to match the artifacts as trained -- no model, scaler, or
selector file was changed.
"""

import numpy as np
import joblib
import pandas as pd
import streamlit as st

from config import MODEL_PATH, SCALER_PATH, SELECTOR_PATH

# Column order the selector was fit on (11 engineered features, pre-selection).
# Falls back to this if the loaded selector doesn't expose feature_names_in_
# (e.g. it was fit on a plain ndarray rather than a DataFrame).
_ENGINEERED_FEATURE_ORDER = [
    "Gender", "Married", "Dependents", "Education", "Self_Employed",
    "Credit_History", "Property_Area", "TotalIncome", "LoanAmountLog",
    "EMI", "BalanceIncome",
]


@st.cache_resource(show_spinner=False)
def load_artifacts():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    selector = joblib.load(SELECTOR_PATH)
    return model, scaler, selector


def _build_feature_row(form_data: dict, column_order: list) -> pd.DataFrame:
    """Convert raw form inputs into the 11 engineered features used at
    training time (Phase 5 of the notebook), in the exact column order
    the selector was fit on."""

    applicant_income = float(form_data.get("applicant_income", 0) or 0)
    coapplicant_income = float(form_data.get("coapplicant_income", 0) or 0)
    loan_amount = float(form_data.get("loan_amount", 0) or 0)
    loan_term = float(form_data.get("loan_term", 360) or 360)

    total_income = applicant_income + coapplicant_income
    loan_amount_log = float(np.log1p(loan_amount))
    emi = loan_amount / loan_term if loan_term else 0.0
    balance_income = total_income - (emi * 1000)

    property_area_map = {"Rural": 0, "Semiurban": 1, "Urban": 2}
    education_map = {"Graduate": 0, "Not Graduate": 1}

    row = {
        "Gender": 1 if form_data.get("gender") == "Male" else 0,
        "Married": 1 if form_data.get("married") == "Yes" else 0,
        "Dependents": float(str(form_data.get("dependents", "0")).replace("3+", "3")),
        "Education": education_map.get(form_data.get("education"), 0),
        "Self_Employed": 1 if form_data.get("self_employed") == "Yes" else 0,
        "Credit_History": float(form_data.get("credit_history", 1.0)),
        "Property_Area": property_area_map.get(form_data.get("property_area", "Urban"), 2),
        "TotalIncome": total_income,
        "LoanAmountLog": loan_amount_log,
        "EMI": emi,
        "BalanceIncome": balance_income,
    }

    return pd.DataFrame([row], columns=column_order)


def predict_loan_approval(form_data: dict) -> dict:
    """
    Runs the full SelectKBest -> StandardScaler -> RandomForest pipeline.
    Returns a dict with approval decision, confidence, and supporting metrics.
    """
    model, scaler, selector = load_artifacts()

    column_order = list(getattr(selector, "feature_names_in_", _ENGINEERED_FEATURE_ORDER))
    X_row = _build_feature_row(form_data, column_order)

    X_selected = selector.transform(X_row)

    # Re-attach column names before scaling: selector.transform() returns a
    # plain ndarray, but scaler was fit on a DataFrame with named columns.
    # Passing a DataFrame back avoids a spurious sklearn UserWarning.
    scaler_columns = list(getattr(scaler, "feature_names_in_", []))
    if scaler_columns and len(scaler_columns) == X_selected.shape[1]:
        X_selected = pd.DataFrame(X_selected, columns=scaler_columns)

    X_scaled = scaler.transform(X_selected)

    prediction = model.predict(X_scaled)[0]
    proba = model.predict_proba(X_scaled)[0]
    confidence = float(proba[int(prediction)])

    approved = bool(prediction == 1)

    # ---- Derived metrics for the results page ----
    income = float(form_data.get("applicant_income", 0) or 0) + float(
        form_data.get("coapplicant_income", 0) or 0
    )
    loan_amount_thousands = float(form_data.get("loan_amount", 0) or 0)
    monthly_loan_payment = (loan_amount_thousands * 1000) / max(
        float(form_data.get("loan_term", 360) or 360), 1
    )
    dti = (monthly_loan_payment / income * 100) if income > 0 else 0
    dti = min(dti, 100)

    credit_history = float(form_data.get("credit_history", 1.0))
    credit_health = "Excellent" if credit_history == 1.0 else "Poor"
    credit_score_display = 812 if credit_history == 1.0 else 540

    risk_profile = "Minimal" if (approved and confidence > 0.8) else (
        "Low" if approved else ("Elevated" if confidence > 0.6 else "High")
    )

    base_apr = 5.25
    apr = base_apr if credit_history == 1.0 else base_apr + 3.5
    if dti > 36:
        apr += 0.75

    return {
        "approved": approved,
        "confidence": round(confidence * 100, 1),
        "risk_profile": risk_profile,
        "estimated_apr": round(apr, 2),
        "credit_health": credit_health,
        "credit_score": credit_score_display,
        "dti": round(dti, 1),
        "loan_amount": loan_amount_thousands,
        "income": income,
    }
