"""Reusable HTML card components for the SYVORA FINANCE design system.

These render static markup (no click handlers), so they're safe to compose
freely inside a single st.markdown() call — unlike st.container(), there's
no risk of the "unclosed div" containment bug here, since none of this
markup needs to wrap a native Streamlit widget.

Each function returns its fragment already dedented and stripped of
leading/trailing blank lines. This matters because Streamlit's markdown
renderer follows CommonMark: a line indented 4+ spaces starts an indented
*code* block (rendered as literal escaped text) unless it's already inside
an open HTML block — and a blank line ends that HTML block early. Since
these fragments get concatenated together (e.g. stat_grid joins several
stat_card() outputs), an untrimmed fragment would leave a blank line at
the join point and break HTML parsing for everything after it.
"""

import textwrap


def stat_card(value: str, label: str) -> str:
    """A single stat card, e.g. value='98.7%', label='Prediction Accuracy'."""
    return textwrap.dedent(f"""
    <div class="sf-stat-card sf-hover-lift">
        <div class="sf-stat-value">{value}</div>
        <div class="sf-stat-label">{label}</div>
    </div>
    """).strip()


def stat_grid(stats: list[tuple[str, str]]) -> str:
    """stats: list of (value, label) tuples."""
    cards = "".join(stat_card(v, l) for v, l in stats)
    return f'<div class="sf-stat-grid">{cards}</div>'


def feature_card(icon: str, title: str, desc: str, gold: bool = False) -> str:
    icon_cls = "sf-feature-icon gold" if gold else "sf-feature-icon"
    return textwrap.dedent(f"""
    <div class="sf-feature-card sf-hover-lift">
        <div class="{icon_cls}">{icon}</div>
        <div class="sf-feature-title">{title}</div>
        <div class="sf-feature-desc">{desc}</div>
    </div>
    """).strip()


def feature_grid(features: list[tuple[str, str, str]], gold_index: int | None = None) -> str:
    """features: list of (icon, title, desc) tuples."""
    cards = "".join(
        feature_card(icon, title, desc, gold=(i == gold_index))
        for i, (icon, title, desc) in enumerate(features)
    )
    return f'<div class="sf-feature-grid">{cards}</div>'


def badge(text: str, outline: bool = False) -> str:
    cls = "sf-badge-outline" if outline else "sf-badge"
    return f'<span class="{cls}">{text}</span>'
