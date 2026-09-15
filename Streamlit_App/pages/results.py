"""
Results page — minimal, decision-first layout.

Shows only:
- Approval/denial banner with confidence
- Prediction confidence bar
- Four stat cards: Total Monthly Income, Est. Monthly EMI, EMI/Income Ratio, Credit History
- Outcome / probability table (Approved vs Rejected)
"""

import textwrap
import streamlit as st
from components.navbar import render_navbar
from components.footer import render_footer
from components.cards import stat_card


def render(go_to):
    render_navbar(active_link="Applications")

    result = st.session_state.get("prediction_result")
    fd = st.session_state.get("form_data", {})

    if not result:
        st.warning("No prediction result found. Please complete the application form.")
        if st.button("Start New Application"):
            go_to("application")
        return

    approved = result["approved"]
    confidence = result["confidence"]  # probability of the predicted class, 0-100
    credit_health = result["credit_health"]

    status_cls = "approved" if approved else "denied"
    status_word = "Loan Approved" if approved else "Loan Not Approved"
    status_icon = "✅" if approved else "❌"
    status_desc = "This application is likely to be approved" if approved else "This application is likely to be rejected"

    # ---- Derived display values (pure display-layer math on the same
    # figures predictor.py already computed for the DTI ratio — no model
    # or prediction logic touched here) ----
    income = result["income"]
    loan_amount_thousands = result["loan_amount"]
    loan_term = float(fd.get("loan_term", 360) or 360)
    monthly_emi = (loan_amount_thousands * 1000) / loan_term if loan_term else 0.0
    emi_income_ratio = result["dti"]  # already (monthly_emi / income * 100), capped at 100

    approved_prob = confidence if approved else (100 - confidence)
    rejected_prob = 100 - approved_prob

    credit_ok = credit_health == "Excellent"
    credit_icon = "✅" if credit_ok else "❌"

    with st.container(key="sfresultswrap"):
        # ---- Approval / denial banner ----
        st.markdown(
            textwrap.dedent(f"""
            <div class="sf-result-banner {status_cls}">
                <div class="sf-result-banner-icon {status_cls}">{status_icon}</div>
                <div>
                    <div class="sf-result-banner-title {status_cls}">{status_word}</div>
                    <div class="sf-result-banner-desc">{status_desc} · Confidence: <b>{confidence:.1f}%</b></div>
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True,
        )

        # ---- Prediction confidence bar ----
        st.markdown(
            textwrap.dedent(f"""
            <div class="sf-confidence-label">Prediction Confidence</div>
            <div class="sf-confidence-track">
                <div class="sf-confidence-fill {status_cls}" style="width:{confidence}%;"></div>
            </div>
            """).strip(),
            unsafe_allow_html=True,
        )

        # ---- Four stat cards ----
        stats_html = "".join([
            stat_card(f"₹{income:,.0f}", "TOTAL MONTHLY INCOME"),
            stat_card(f"₹{monthly_emi:,.0f}", "EST. MONTHLY EMI"),
            stat_card(f"{emi_income_ratio:.1f}%", "EMI / INCOME RATIO"),
            stat_card(f"{credit_health} {credit_icon}", "CREDIT HISTORY"),
        ])
        st.markdown(f'<div class="sf-stat-grid">{stats_html}</div>', unsafe_allow_html=True)

        # ---- Outcome / probability table ----
        st.markdown(
            textwrap.dedent(f"""
            <table class="sf-outcome-table">
                <thead>
                    <tr><th>Outcome</th><th>Probability</th></tr>
                </thead>
                <tbody>
                    <tr><td>Approved</td><td>{approved_prob:.2f}%</td></tr>
                    <tr><td>Rejected</td><td>{rejected_prob:.2f}%</td></tr>
                </tbody>
            </table>
            """).strip(),
            unsafe_allow_html=True,
        )

        # New Application button
        with st.container(key="sfresultsnewappbtn"):
            if st.button("🔄  Start New Application", key="btn_new_app"):
                st.session_state.form_step = 1
                st.session_state.form_data = {}
                st.session_state.prediction_result = None
                go_to("application")

    render_footer()
