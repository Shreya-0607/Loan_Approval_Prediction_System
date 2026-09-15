"""Styled button helper for the SYVORA FINANCE design system.

Native st.button is the only reliable way to get real click handling in
Streamlit — raw HTML buttons can't trigger a rerun. To still get distinct
visual variants (gradient navy, gold, secondary outline, ghost, dark), each
button is wrapped in st.container(key=...) using a variant-prefixed key.
Streamlit attaches a "st-key-<key>" class to that wrapper div, and
styles/buttons.css targets it via a `[class*="st-key-sfbtn<variant>"]`
substring selector. See styles/buttons.css for the variant rules.
"""

import streamlit as st

_VARIANT_PREFIX = {
    "primary": "sfbtnprimary",
    "gold": "sfbtngold",
    "secondary": "sfbtnsecondary",
    "ghost": "sfbtnghost",
    "dark": "sfbtndark",
}


def styled_button(
    label: str,
    key: str,
    variant: str = "primary",
    use_container_width: bool = False,
    disabled: bool = False,
) -> bool:
    """Render a native st.button styled with a design-system variant.

    Returns True on the run where the button was clicked, exactly like
    st.button — this is a drop-in replacement, not a new widget type.
    """
    if variant not in _VARIANT_PREFIX:
        raise ValueError(f"Unknown button variant: {variant!r}. Choose from {list(_VARIANT_PREFIX)}.")

    container_key = f"{_VARIANT_PREFIX[variant]}__{key}"
    with st.container(key=container_key):
        return st.button(
            label,
            key=key,
            use_container_width=use_container_width,
            disabled=disabled,
        )
