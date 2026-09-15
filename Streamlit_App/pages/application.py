"""
Application Form page — 3-step wizard matching screen_2 mockup.

Step 1: Personal Information (Gender, Education, Marital Status, Dependents, Self Employed, Credit History)
Step 2: Financial Information (Applicant Income, Coapplicant Income, Loan Amount, Loan Term)
Step 3: Property (Property Area, confirmation)
"""

import textwrap
import streamlit as st
from components.navbar import render_navbar
from components.footer import render_footer
from components.stepper import render_stepper
from config import (
    GENDER_OPTIONS, MARITAL_OPTIONS, EDUCATION_OPTIONS,
    DEPENDENTS_OPTIONS, SELF_EMPLOYED_OPTIONS, CREDIT_HISTORY_OPTIONS,
    PROPERTY_AREA_OPTIONS,
)


def render(go_to):
    render_navbar(active_link="Applications")

    fd = st.session_state.form_data
    step = st.session_state.form_step

    with st.container(key="sfformpage"):
        # ---- Page header ----
        st.markdown(
    textwrap.dedent("""
            <div class="sf-form-title">New Loan Application</div>
            <div class="sf-form-subtitle">Complete the form below to get an instant precision credit assessment.</div>
            """).strip(),
    unsafe_allow_html=True,
)

        render_stepper(step)

        # ---- Form card ----
        with st.container(key="sfformcard"):
            if step == 1:
                _render_step1(fd, go_to)
            elif step == 2:
                _render_step2(fd, go_to)
            elif step == 3:
                _render_step3(fd, go_to)

    render_footer()


# ---------------------------------------------------------------------------
# Step 1 — Personal Information
# ---------------------------------------------------------------------------
def _render_step1(fd, go_to):
    st.markdown(
        '<div class="sf-form-card-header"><span class="icon">👤</span> Personal Information</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox(
            "Gender",
            GENDER_OPTIONS,
            index=GENDER_OPTIONS.index(fd.get("gender", GENDER_OPTIONS[0])),
            key="s1_gender",
        )
    with col2:
        education = st.selectbox(
            "Education",
            EDUCATION_OPTIONS,
            index=EDUCATION_OPTIONS.index(fd.get("education", EDUCATION_OPTIONS[0])),
            key="s1_education",
        )

    col3, col4 = st.columns(2)
    with col3:
        married = st.selectbox(
            "Marital Status",
            MARITAL_OPTIONS,
            index=MARITAL_OPTIONS.index(fd.get("married", MARITAL_OPTIONS[0])),
            key="s1_married",
        )
    with col4:
        dependents = st.selectbox(
            "Dependents",
            DEPENDENTS_OPTIONS,
            index=DEPENDENTS_OPTIONS.index(fd.get("dependents", DEPENDENTS_OPTIONS[0])),
            key="s1_dependents",
        )

    col5, col6 = st.columns(2)
    with col5:
        self_employed = st.selectbox(
            "Self Employed",
            SELF_EMPLOYED_OPTIONS,
            index=SELF_EMPLOYED_OPTIONS.index(fd.get("self_employed", SELF_EMPLOYED_OPTIONS[0])),
            key="s1_self_employed",
        )
    with col6:
        credit_history = st.selectbox(
            "Credit History",
            CREDIT_HISTORY_OPTIONS,
            index=CREDIT_HISTORY_OPTIONS.index(fd.get("credit_history_label", CREDIT_HISTORY_OPTIONS[0])),
            key="s1_credit_history",
        )

    st.markdown('<hr class="sf-form-divider"/>', unsafe_allow_html=True)

    # Validation
    _, btn_col = st.columns([3, 1])
    with btn_col:
        next_clicked = st.button("Next  →", key="s1_next", use_container_width=True)

    if next_clicked:
        errors = []
        if gender == GENDER_OPTIONS[0]:
            errors.append("Please select a Gender.")
        if education == EDUCATION_OPTIONS[0]:
            errors.append("Please select an Education level.")
        if married == MARITAL_OPTIONS[0]:
            errors.append("Please select a Marital Status.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            st.session_state.form_data.update({
                "gender": gender,
                "education": education,
                "married": married,
                "dependents": dependents,
                "self_employed": self_employed,
                "credit_history_label": credit_history,
                "credit_history": 1.0 if "1.0" in credit_history else 0.0,
            })
            st.session_state.form_step = 2
            st.rerun()


# ---------------------------------------------------------------------------
# Step 2 — Financial Information
# ---------------------------------------------------------------------------
def _render_step2(fd, go_to):
    st.markdown(
        '<div class="sf-form-card-header"><span class="icon">💰</span> Financial Information</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        applicant_income = st.number_input(
            "Applicant Income (₹ / month)",
            min_value=0,
            max_value=1_000_000,
            value=int(fd.get("applicant_income", 5000)),
            step=500,
            key="s2_applicant_income",
        )
    with col2:
        coapplicant_income = st.number_input(
            "Coapplicant Income (₹ / month)",
            min_value=0,
            max_value=1_000_000,
            value=int(fd.get("coapplicant_income", 0)),
            step=500,
            key="s2_coapplicant_income",
        )

    col3, col4 = st.columns(2)
    with col3:
        loan_amount = st.number_input(
            "Loan Amount (₹ thousands)",
            min_value=1,
            max_value=10_000,
            value=int(fd.get("loan_amount", 150)),
            step=10,
            key="s2_loan_amount",
        )
    with col4:
        loan_term = st.selectbox(
            "Loan Term (months)",
            [12, 36, 60, 84, 120, 180, 240, 300, 360, 480],
            index=[12, 36, 60, 84, 120, 180, 240, 300, 360, 480].index(
                int(fd.get("loan_term", 360))
            ),
            key="s2_loan_term",
        )

    st.markdown('<hr class="sf-form-divider"/>', unsafe_allow_html=True)

    back_col, spacer, next_col = st.columns([1, 2, 1])
    with back_col:
        if st.button("← Back", key="s2_back", use_container_width=True):
            st.session_state.form_step = 1
            st.rerun()
    with next_col:
        next_clicked = st.button("Next  →", key="s2_next", use_container_width=True)

    if next_clicked:
        if applicant_income <= 0:
            st.error("Please enter a valid Applicant Income.")
        elif loan_amount <= 0:
            st.error("Please enter a valid Loan Amount.")
        else:
            st.session_state.form_data.update({
                "applicant_income": applicant_income,
                "coapplicant_income": coapplicant_income,
                "loan_amount": loan_amount,
                "loan_term": loan_term,
            })
            st.session_state.form_step = 3
            st.rerun()


# ---------------------------------------------------------------------------
# Step 3 — Property Information
# ---------------------------------------------------------------------------
def _render_step3(fd, go_to):
    st.markdown(
        '<div class="sf-form-card-header"><span class="icon">🏠</span> Property Information</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        property_area = st.selectbox(
            "Property Area",
            PROPERTY_AREA_OPTIONS,
            index=PROPERTY_AREA_OPTIONS.index(fd.get("property_area", "Urban")),
            key="s3_property_area",
        )
    with col2:
        loan_purpose = st.selectbox(
            "Loan Purpose",
            ["Home Purchase", "Home Refinance", "Construction", "Plot Purchase"],
            key="s3_loan_purpose",
        )

    # Summary review block
    st.markdown(
    textwrap.dedent(f"""
        <div style="
            background: var(--surface-container-low);
            border: 1px solid var(--outline-variant);
            border-radius: var(--radius-lg);
            padding: 20px;
            margin-top: 16px;
        ">
            <div style="font-size:14px; font-weight:700; color:var(--on-surface); margin-bottom:12px;">
                Application Summary
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px 24px; font-size:13px; color:var(--on-surface-variant);">
                <div><strong>Gender:</strong> {fd.get('gender','—')}</div>
                <div><strong>Education:</strong> {fd.get('education','—')}</div>
                <div><strong>Married:</strong> {fd.get('married','—')}</div>
                <div><strong>Dependents:</strong> {fd.get('dependents','—')}</div>
                <div><strong>Self Employed:</strong> {fd.get('self_employed','—')}</div>
                <div><strong>Credit History:</strong> {fd.get('credit_history_label','—')}</div>
                <div><strong>Applicant Income:</strong> ₹{fd.get('applicant_income','—'):,}</div>
                <div><strong>Coapplicant Income:</strong> ₹{fd.get('coapplicant_income','—'):,}</div>
                <div><strong>Loan Amount:</strong> ₹{fd.get('loan_amount','—')}k</div>
                <div><strong>Loan Term:</strong> {fd.get('loan_term','—')} months</div>
            </div>
        </div>
        """).strip(),
    unsafe_allow_html=True,
)

    st.markdown('<hr class="sf-form-divider"/>', unsafe_allow_html=True)

    back_col, spacer, submit_col = st.columns([1, 2, 1])
    with back_col:
        if st.button("← Back", key="s3_back", use_container_width=True):
            st.session_state.form_step = 2
            st.rerun()
    with submit_col:
        if st.button("Submit  →", key="s3_submit", use_container_width=True):
            st.session_state.form_data.update({
                "property_area": property_area,
                "loan_purpose": loan_purpose,
            })
            go_to("processing")
