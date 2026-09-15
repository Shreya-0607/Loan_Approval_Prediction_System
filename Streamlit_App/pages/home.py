"""Home / Landing page — hero, 3-step process, footer."""

import textwrap
import streamlit as st
from components.navbar import render_navbar
from components.footer import render_footer


def render(go_to):
    render_navbar(active_link="Dashboard")

    st.markdown(
    textwrap.dedent("""
        <div class="sf-hero">
            <div class="sf-hero-badge">AI-POWERED PRECISION</div>
            <div class="sf-hero-title">
                Predict Your Loan Success with <span class="accent">Calm Precision.</span>
            </div>
            <div class="sf-hero-subtitle">
                SYVORA FINANCE utilizes advanced neural networks to provide institutional-grade
                loan approval predictions in seconds. Experience clarity before you apply.
            </div>
        </div>
        """).strip(),
    unsafe_allow_html=True,
)

    # Single centered CTA — rendered with native st.button so the click
    # handler works, styled via CSS to match .sf-btn-primary visually.
    spacer_l, c1, spacer_r = st.columns([2, 1, 2])
    with c1:
        if st.button("Start Prediction  →", key="btn_start_prediction", use_container_width=True):
            st.session_state.form_step = 1
            st.session_state.form_data = {}
            go_to("application")

    st.markdown(
    textwrap.dedent("""
        <div class="sf-section">
            <div class="sf-section-header">
                <div class="sf-section-title">A Simple 3-Step Process</div>
                <div class="sf-section-subtitle">
                    We've refined the complex world of credit risk into three effortless stages
                    to get you the answers you need.
                </div>
            </div>
            <div class="sf-card-grid">
                <div class="sf-step-card">
                    <div class="sf-step-icon blue">📄</div>
                    <div class="sf-step-title">1. Data Entry</div>
                    <div class="sf-step-desc">Input your basic financial parameters through our secure, encrypted portal.</div>
                </div>
                <div class="sf-step-card">
                    <div class="sf-step-icon light">🧠</div>
                    <div class="sf-step-title">2. AI Analysis</div>
                    <div class="sf-step-desc">Our neural network compares your profile against millions of historical data points.</div>
                </div>
                <div class="sf-step-card">
                    <div class="sf-step-icon teal">⚙️</div>
                    <div class="sf-step-title">3. Instant Result</div>
                    <div class="sf-step-desc">Receive a detailed probability report and actionable advice to improve your standing.</div>
                </div>
            </div>
        </div>
        """).strip(),
    unsafe_allow_html=True,
)

    render_footer()
