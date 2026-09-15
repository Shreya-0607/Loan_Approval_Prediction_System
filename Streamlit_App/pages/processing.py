"""
Processing page — animated checklist while the ML pipeline runs, then
auto-navigates to the results page.

Redesign notes: the previous version used a spinning square-border CSS
animation, which read as a broken/garbled scribble whenever a screenshot
caught it mid-rotation. It also rendered each checklist item in its own
separate st.empty() placeholder with no shared wrapper, so the items had
no gap between them (the .sf-checklist wrapper class existed in CSS but
was never actually applied) and appeared cramped/overlapping.

This version:
  - Replaces the spinner with a static-friendly SVG circular progress
    ring showing the live percentage in the center — reads correctly at
    any point in the animation, not just at rest.
  - Renders the whole checklist as ONE HTML block per update (wrapped in
    .sf-checklist) instead of four independent placeholders, so item
    spacing is consistent and there's no chance of items visually
    stacking on top of each other.
"""

import textwrap
import time
import streamlit as st

from components.navbar import render_navbar
from components.footer import render_footer
from utils.predictor import predict_loan_approval


def _progress_ring(pct: int, size: int = 96, stroke: int = 6) -> str:
    """Static-friendly SVG circular progress ring with the percentage in
    the center. Renders correctly whether captured mid-animation or at
    rest, unlike a CSS-spun border."""
    radius = (size - stroke) / 2
    circumference = 2 * 3.14159265 * radius
    offset = circumference * (1 - pct / 100)
    center = size / 2
    return textwrap.dedent(f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" class="sf-progress-ring">
        <circle cx="{center}" cy="{center}" r="{radius}"
                fill="none" stroke="var(--surface-container-high)" stroke-width="{stroke}"/>
        <circle cx="{center}" cy="{center}" r="{radius}"
                fill="none" stroke="var(--primary)" stroke-width="{stroke}"
                stroke-linecap="round" stroke-dasharray="{circumference:.2f}"
                stroke-dashoffset="{offset:.2f}"
                transform="rotate(-90 {center} {center})"/>
        <text x="{center}" y="{center}" text-anchor="middle" dominant-baseline="central"
              class="sf-progress-ring-text">{pct}%</text>
    </svg>
    """).strip()


def render(go_to):
    render_navbar(active_link="Applications")

    with st.container(key="sfprocessingwrap"):
        with st.container(key="sfprocessingcard"):
            placeholder_ring = st.empty()
            placeholder_title = st.empty()
            placeholder_sub = st.empty()
            placeholder_checklist = st.empty()

            checklist_items = [
                "Data integrity verification",
                "Credit risk assessment engine",
                "Regulatory compliance check",
                "Final eligibility synthesis",
            ]

            stages = [
                (25, "Analyzing…", "Scanning applicant data…"),
                (50, "Processing…", "Running credit risk engine…"),
                (75, "Verifying…", "Regulatory compliance check…"),
                (100, "Analysis Complete", "Complete. Redirecting to results…"),
            ]

            def _render_checklist(done_count: int, in_progress: bool) -> str:
                rows = []
                for j, label in enumerate(checklist_items):
                    if j < done_count:
                        icon, cls = "✅", "done"
                    elif j == done_count and in_progress:
                        icon, cls = "⏳", "active"
                    else:
                        icon, cls = "○", "pending"
                    rows.append(
                        f'<div class="sf-checklist-item {cls}">'
                        f'<span class="sf-checklist-icon">{icon}</span>'
                        f'<span>{label}</span>'
                        f'</div>'
                    )
                return f'<div class="sf-checklist">{"".join(rows)}</div>'

            for i, (pct, title, sub) in enumerate(stages):
                placeholder_ring.markdown(_progress_ring(pct), unsafe_allow_html=True)
                placeholder_title.markdown(
                    f'<div class="sf-processing-title">{title}</div>', unsafe_allow_html=True
                )
                placeholder_sub.markdown(
                    f'<div class="sf-processing-subtitle">{sub}</div>', unsafe_allow_html=True
                )
                done_count = i + 1 if pct == 100 else i
                placeholder_checklist.markdown(
                    _render_checklist(done_count=done_count, in_progress=(pct < 100)),
                    unsafe_allow_html=True,
                )
                time.sleep(0.6)

            # ---- Run prediction ----
            result = predict_loan_approval(st.session_state.form_data)
            st.session_state.prediction_result = result

            time.sleep(0.5)

        # Security note
        st.markdown(
    textwrap.dedent("""
            <div class="sf-security-note">
                🔒 Bank-level 256-bit encryption active
            </div>
            """).strip(),
    unsafe_allow_html=True,
)

    render_footer()

    # Auto-navigate to results
    time.sleep(0.4)
    go_to("results")
