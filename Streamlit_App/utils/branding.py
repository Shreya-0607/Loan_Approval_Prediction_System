"""Small helper for embedding the SYVORA FINANCE logo as base64.

Streamlit apps served from localhost can't reference local file paths in
<img src="..."> tags directly, so the logo is base64-encoded and inlined as
a data URI. The encode is cached so the file is only read once per session.
"""

from functools import lru_cache
import base64

from config import LOGO_PATH


@lru_cache(maxsize=1)
def get_logo_data_uri() -> str:
    """Return the SYVORA FINANCE logo as a base64 data URI (PNG)."""
    with open(LOGO_PATH, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"
