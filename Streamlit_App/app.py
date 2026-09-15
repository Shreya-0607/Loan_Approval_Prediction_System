"""
SYVORA FINANCE — Loan Approval Prediction
Main Streamlit entrypoint.

Routing note: navigation between Home / Application / Processing / Results is
handled via st.session_state rather than Streamlit's native multipage file-based
routing or any HTML/JS-based links. This avoids the JS-sandboxing and query-param
conflicts that broke navigation in earlier iterations of this app, and keeps the
whole flow inside a single page (st.rerun() driven) so the custom navbar/footer
stay visually identical across every screen.
"""

import textwrap
import streamlit as st
import os
from config import LOGO_PATH

st.set_page_config(
    page_title="SYVORA FINANCE | Loan Approval Prediction",
    page_icon=LOGO_PATH,
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
STYLES_DIR = os.path.join(APP_DIR, "styles")

# ---------- Load design-system CSS (cascade order matters: tokens/reset first,
# then shared components, then page-specific styles not yet migrated) ----------
CSS_FILES = [
    "global.css",
    "navbar.css",
    "footer.css",
    "buttons.css",
    "cards.css",
    "results.css",
    "pages-legacy.css",
]
css_blob = ""
for fname in CSS_FILES:
    with open(os.path.join(STYLES_DIR, fname)) as f:
        css_blob += f.read() + "\n"
st.markdown(f"<style>{css_blob}</style>", unsafe_allow_html=True)

# Hide the default Streamlit sidebar nav (we don't use multipage file routing)
st.markdown(
    textwrap.dedent("""
    <style>
    div[data-testid="stSidebarNav"] { display: none; }
    section[data-testid="stSidebar"] { display: none; }
    </style>
    """).strip(),
    unsafe_allow_html=True,
)

# ---------- Session state defaults ----------
if "route" not in st.session_state:
    st.session_state.route = "home"
if "form_step" not in st.session_state:
    st.session_state.form_step = 1
if "form_data" not in st.session_state:
    st.session_state.form_data = {}
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None


def go_to(route: str):
    st.session_state.route = route
    st.rerun()


# ---------- Route to the correct page module ----------
from pages import home, application, processing, results

route = st.session_state.route

if route == "home":
    home.render(go_to)
elif route == "application":
    application.render(go_to)
elif route == "processing":
    processing.render(go_to)
elif route == "results":
    results.render(go_to)
else:
    home.render(go_to)
