"""
SYVORA FINANCE — Streamlit App Configuration
Central place for design tokens (mirrors DESIGN.md "Precision Fiscal") and paths.
"""

import os

# ---------- Paths ----------
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_ROOT)

MODEL_DIR = os.path.join(PROJECT_ROOT, "Model")
MODEL_PATH = os.path.join(MODEL_DIR, "loan_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
SELECTOR_PATH = os.path.join(MODEL_DIR, "selector.pkl")
FEATURE_COLUMNS_PATH = os.path.join(MODEL_DIR, "feature_columns.pkl")

STYLES_DIR = os.path.join(APP_ROOT, "styles")
ASSETS_DIR = os.path.join(APP_ROOT, "assets")
LOGO_PATH = os.path.join(ASSETS_DIR, "images", "logo.png")

# ---------- Brand ----------
BRAND_NAME = "SYVORA FINANCE"
NAV_LINKS = ["Dashboard", "Applications", "Reports", "Settings"]

# ---------- Design Tokens ----------
# Source of truth for rendering is styles/global.css — these mirror it for
# any Python code (e.g. chart color scales) that needs the brand palette.
COLORS = {
    "navy-900": "#051730",
    "navy-800": "#071E3D",
    "navy-700": "#0A2A57",  # primary brand navy (sampled from logo)
    "navy-600": "#123A6E",
    "navy-500": "#1B4C8C",
    "gold-600": "#B88437",
    "gold-500": "#C49442",  # accent gold (sampled from logo)
    "gold-400": "#D9AE5F",
    "gold-300": "#E8C57F",
    "surface": "#F7F8FB",
    "surface-container-lowest": "#FFFFFF",
    "surface-container-low": "#F2F4F9",
    "surface-container": "#E9EDF5",
    "surface-container-high": "#DEE4F0",
    "on-surface": "#0E1B2E",
    "on-surface-variant": "#47536B",
    "outline": "#7A869C",
    "outline-variant": "#D6DCE8",
    "inverse-surface": "#0A1830",
    "inverse-on-surface": "#EEF2FB",
    "primary": "#0A2A57",
    "on-primary": "#FFFFFF",
    "accent": "#C49442",
    "on-accent": "#1A1206",
    "success": "#0F9D6B",
    "warning": "#C77F13",
    "error": "#C13A3A",
    "background": "#F7F8FB",
    "on-background": "#0E1B2E",
}

SPACING = {
    "base": "4px",
    "xs": "8px",
    "sm": "16px",
    "md": "24px",
    "lg": "40px",
    "xl": "64px",
    "container-max": "1200px",
    "gutter": "24px",
}

RADIUS = {
    "sm": "8px",
    "DEFAULT": "12px",
    "md": "14px",
    "lg": "18px",
    "xl": "24px",
    "full": "9999px",
}

# ---------- Form option sets ----------
GENDER_OPTIONS = ["Select gender", "Male", "Female"]
MARITAL_OPTIONS = ["Select status", "Yes", "No"]
EDUCATION_OPTIONS = ["Select level", "Graduate", "Not Graduate"]
DEPENDENTS_OPTIONS = ["0", "1", "2", "3+"]
SELF_EMPLOYED_OPTIONS = ["No", "Yes"]
CREDIT_HISTORY_OPTIONS = ["Good (1.0)", "Poor (0.0)"]
PROPERTY_AREA_OPTIONS = ["Urban", "Semiurban", "Rural"]
