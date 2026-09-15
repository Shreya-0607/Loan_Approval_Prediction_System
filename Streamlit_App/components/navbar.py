"""Reusable navbar component matching the Precision Fiscal mockups."""

import textwrap
import streamlit as st
from config import BRAND_NAME, NAV_LINKS
from utils.branding import get_logo_data_uri


def render_navbar(active_link: str = "Dashboard"):
    links_html = ""
    for link in NAV_LINKS:
        cls = "sf-navbar-link active" if link == active_link else "sf-navbar-link"
        links_html += f'<span class="{cls}">{link}</span>'

    logo_uri = get_logo_data_uri()

    st.markdown(
    textwrap.dedent(f"""
        <div class="sf-navbar">
            <div class="sf-navbar-left">
                <img class="sf-navbar-logo-img" src="{logo_uri}" alt="{BRAND_NAME} logo" />
                <span class="sf-navbar-logo">{BRAND_NAME}</span>
            </div>
            <div class="sf-navbar-links">
                {links_html}
            </div>
            <div class="sf-navbar-right">
                <span class="sf-navbar-icon">🌙</span>
                <span class="sf-navbar-icon">🔔</span>
                <div class="sf-navbar-avatar">SG</div>
            </div>
        </div>
        """).strip(),
    unsafe_allow_html=True,
)
