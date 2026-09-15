"""Reusable footer component matching the Precision Fiscal mockups."""

import textwrap
import streamlit as st
from config import BRAND_NAME
from utils.branding import get_logo_data_uri


def render_footer():
    logo_uri = get_logo_data_uri()
    st.markdown(
    textwrap.dedent(f"""
        <div class="sf-footer">
            <div class="sf-footer-row">
                <div class="sf-footer-logo">
                    <img class="sf-footer-logo-img" src="{logo_uri}" alt="{BRAND_NAME} logo" />
                    {BRAND_NAME}
                </div>
                <div class="sf-footer-links">
                    <span>Privacy Policy</span>
                    <span>Terms of Service</span>
                    <span>Compliance</span>
                    <span>Contact Support</span>
                </div>
                <div class="sf-footer-copy">© 2026 {BRAND_NAME} Systems.<br/>All rights reserved.</div>
            </div>
        </div>
        """).strip(),
    unsafe_allow_html=True,
)
