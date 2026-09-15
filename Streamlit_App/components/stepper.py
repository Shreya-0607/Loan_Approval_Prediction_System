"""Horizontal stepper component used at the top of the loan application form."""

import textwrap
import streamlit as st

STEPS = ["Personal", "Financial", "Property"]


def render_stepper(current_step: int):
    """current_step is 1-indexed (1, 2, or 3)."""
    parts = []
    for i, label in enumerate(STEPS, start=1):
        if i < current_step:
            circle_cls, label_cls, content = "done", "", "✓"
        elif i == current_step:
            circle_cls, label_cls, content = "current", "current", str(i)
        else:
            circle_cls, label_cls, content = "upcoming", "", str(i)

        parts.append(
            textwrap.dedent(f"""
            <div class="sf-stepper-step">
                <div class="sf-stepper-circle {circle_cls}">{content}</div>
                <div class="sf-stepper-label {label_cls}">{label}</div>
            </div>
            """).strip()
        )
        if i < len(STEPS):
            parts.append('<div class="sf-stepper-line"></div>')

    st.markdown(
        f'<div class="sf-stepper">{"".join(parts)}</div>',
        unsafe_allow_html=True,
    )
