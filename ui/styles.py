"""
Global Streamlit styles for Versandkosten-Kompass.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_01_BUILD_003"
PURPOSE = "Apply visual styling without business logic"
"""

import streamlit as st


GLOBAL_STYLE = """
<style>
:root {
    --bg-deep: #0b0d0f;
    --bg-panel: rgba(22, 25, 27, 0.94);
    --line: rgba(195, 168, 111, 0.30);
    --line-soft: rgba(195, 168, 111, 0.14);
    --text-main: #f1eee6;
    --text-muted: #b7ad9a;
    --accent: #c3a86f;
    --accent-soft: rgba(195, 168, 111, 0.11);
    --ok: #91aa7d;
    --warn: #d6b46f;
    --danger: #c98272;
}

.stApp {
    background: linear-gradient(135deg, #090b0d 0%, #111416 52%, #070809 100%);
    color: var(--text-main);
    font-family: "Segoe UI", "Inter", sans-serif;
}

[data-testid="stHeader"] { background: transparent; height: 0rem; }
[data-testid="stToolbar"] { display: none; }
footer { display: none; }

.main .block-container {
    padding-top: 0.38rem;
    padding-bottom: 0.28rem;
    max-width: 1600px;
}

.compact-header {
    display: grid;
    grid-template-columns: 0.92fr 1.28fr 0.88fr;
    align-items: center;
    gap: 1rem;
    padding: 0.72rem 0.92rem;
    border: 1px solid var(--line);
    border-radius: 15px;
    background:
        linear-gradient(180deg, rgba(195,168,111,0.08), rgba(0,0,0,0.10)),
        rgba(17, 20, 22, 0.96);
    margin-bottom: 0.52rem;
    box-shadow: 0 10px 28px rgba(0,0,0,0.28);
}

.brand-block {
    border-right: 1px solid rgba(195,168,111,0.18);
    padding-right: 1rem;
}

.brand-name {
    font-size: 2.08rem;
    line-height: 0.92;
    margin: 0;
    letter-spacing: 0.015em;
    font-weight: 950;
    color: #fff4d8;
}

.brand-sub {
    color: var(--text-muted);
    font-size: 0.66rem;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    margin-top: 0.28rem;
}

.title-block {
    text-align: left;
}

.title-row { display: flex; align-items: baseline; gap: 0.72rem; flex-wrap: wrap; }
.compact-header h1 {
    font-size: 1.42rem;
    line-height: 1;
    margin: 0;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    font-weight: 900;
}

.system-subtitle {
    color: var(--text-muted);
    font-size: 0.76rem;
    letter-spacing: 0.03em;
    margin-top: 0.32rem;
}

.version-badge {
    font-size: 0.66rem;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    color: var(--accent);
    border: 1px solid var(--line);
    border-radius: 999px;
    padding: 0.17rem 0.48rem;
    background: var(--accent-soft);
    white-space: nowrap;
}

.header-note {
    color: var(--text-muted);
    font-size: 0.68rem;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    line-height: 1.45;
    text-align: right;
    white-space: nowrap;
}

.header-note strong {
    color: var(--text-main);
    font-weight: 850;
}

.panel {
    border: 1px solid var(--line-soft);
    border-radius: 15px;
    padding: 0.64rem;
    background: linear-gradient(180deg, rgba(255,255,255,0.028), rgba(0,0,0,0.12)), var(--bg-panel);
    box-shadow: 0 10px 24px rgba(0,0,0,0.22), inset 0 1px 0 rgba(255,255,255,0.025);
    margin-bottom: 0.46rem;
}

.section-title {
    font-size: 0.68rem;
    font-weight: 850;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.38rem;
}

.hint-line {
    color: var(--text-muted);
    font-size: 0.72rem;
    line-height: 1.28;
    margin-top: 0.28rem;
}

.winner-card {
    border: 1px solid rgba(195,168,111,0.62);
    border-radius: 15px;
    padding: 0.78rem;
    background: linear-gradient(180deg, rgba(195,168,111,0.15), rgba(0,0,0,0.12)), rgba(18,21,23,0.96);
    min-height: 142px;
}

.recommendation {
    color: var(--accent);
    font-size: 0.66rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 850;
    margin-bottom: 0.28rem;
}

.winner-name { font-size: 1.28rem; font-weight: 850; margin: 0; }
.winner-price { font-size: 2.05rem; font-weight: 900; line-height: 1.02; color: #fff4d8; margin-top: 0.18rem; }
.winner-meta { color: var(--text-muted); font-size: 0.76rem; line-height: 1.32; margin-top: 0.34rem; }

.mini-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.38rem;
}

.mini-box {
    border: 1px solid var(--line-soft);
    border-radius: 12px;
    padding: 0.45rem 0.52rem;
    background: rgba(0,0,0,0.16);
}
.mini-label { color: var(--text-muted); font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.09em; }
.mini-value { color: var(--text-main); font-size: 0.90rem; font-weight: 830; margin-top: 0.10rem; }

.message-box {
    border: 1px solid rgba(195,168,111,0.18);
    border-radius: 12px;
    padding: 0.50rem 0.56rem;
    background: rgba(0,0,0,0.15);
    color: #d9d0be;
    font-size: 0.74rem;
    line-height: 1.32;
    min-height: 42px;
}

.warning-box {
    border-color: rgba(214,180,111,0.26);
    background: rgba(214,180,111,0.075);
    color: #e6d3a8;
}

.ok-box {
    border-color: rgba(145,170,125,0.24);
    background: rgba(145,170,125,0.07);
    color: #cdddba;
}

.provider-grid {
    display: grid;
    grid-template-columns: 0.34fr 1.55fr 0.78fr 1.16fr;
    width: 100%;
    border: 1px solid var(--line-soft);
    border-radius: 12px;
    overflow: hidden;
    font-size: 0.74rem;
    background: rgba(0,0,0,0.10);
}
.provider-head, .provider-cell {
    padding: 0.34rem 0.42rem;
    border-bottom: 1px solid rgba(195,168,111,0.08);
    border-right: 1px solid rgba(195,168,111,0.08);
    min-height: 1.95rem;
}
.provider-head {
    color: var(--accent);
    font-size: 0.61rem;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    font-weight: 850;
    background: rgba(0,0,0,0.18);
}
.provider-cell:nth-last-child(-n+4) { border-bottom: none; }
.provider-cell:nth-child(4n), .provider-head:nth-child(4n) { border-right: none; }
.provider-sub { color: var(--text-muted); font-size: 0.68rem; margin-top: 0.08rem; }
.rank { color: var(--accent); font-weight: 850; }
.price-cell { font-weight: 850; color: #fff4d8; white-space: nowrap; }
.status-ok { color: var(--ok); font-weight: 750; }
.status-bad { color: var(--danger); font-weight: 750; }

.booking-box {
    border: 1px solid rgba(195,168,111,0.38);
    border-radius: 12px;
    padding: 0.54rem 0.62rem;
    background: linear-gradient(180deg, rgba(195,168,111,0.11), rgba(0,0,0,0.15));
    font-size: 0.74rem;
    line-height: 1.36;
    color: #eee4d1;
}

.stNumberInput label, .stRadio label, .stCheckbox label, .stTextInput label, .stSelectbox label { font-size: 0.74rem !important; color: var(--text-muted) !important; }
.stNumberInput input, .stTextInput input {
    background-color: rgba(0,0,0,0.22) !important;
    border-radius: 10px !important;
    border-color: rgba(195,168,111,0.24) !important;
    color: #f2eee4 !important;
    min-height: 1.90rem !important;
}
div[data-baseweb="input"], div[data-baseweb="select"] { min-height: 1.90rem !important; }
.stSelectbox div[data-baseweb="select"] {
    background-color: rgba(0,0,0,0.22) !important;
    border-radius: 10px !important;
    border-color: rgba(195,168,111,0.24) !important;
    color: #f2eee4 !important;
}

.stButton button {
    border-radius: 12px;
    border: 1px solid rgba(195,168,111,0.50);
    background: linear-gradient(135deg, rgba(195,168,111,0.24), rgba(255,255,255,0.045));
    color: #f4eddd;
    font-weight: 850;
    width: 100%;
    min-height: 2.10rem;
    padding-top: 0.22rem;
    padding-bottom: 0.22rem;
}

.stButton button:hover {
    border-color: rgba(195,168,111,0.80);
    background: linear-gradient(135deg, rgba(195,168,111,0.34), rgba(255,255,255,0.065));
    color: #ffffff;
}

div[role="radiogroup"] { gap: 0.25rem !important; }


.trust-list {
    display: grid;
    grid-template-columns: 1fr;
    gap: 0.22rem;
    margin-top: 0.46rem;
    font-size: 0.74rem;
    color: #e7dcc7;
}

.trust-item {
    border: 1px solid rgba(145,170,125,0.18);
    border-radius: 10px;
    padding: 0.28rem 0.42rem;
    background: rgba(145,170,125,0.055);
}

.trust-percent {
    font-size: 2.35rem;
    line-height: 1;
    font-weight: 950;
    color: #fff4d8;
    letter-spacing: -0.04em;
}

.provider-reason {
    color: var(--text-muted);
    font-size: 0.66rem;
    line-height: 1.22;
    margin-top: 0.12rem;
}

.human-note {
    border: 1px solid rgba(195,168,111,0.34);
    border-radius: 12px;
    padding: 0.46rem 0.54rem;
    background: rgba(195,168,111,0.075);
    color: #eadfc9;
    font-size: 0.74rem;
    line-height: 1.34;
    margin-top: 0.46rem;
}

.footer-console {
    color: var(--text-muted);
    font-size: 0.62rem;
    opacity: 0.82;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    margin-top: 0.24rem;
}
</style>
"""


def apply_global_styles() -> None:
    """Apply the app-wide Streamlit CSS."""
    st.markdown(GLOBAL_STYLE, unsafe_allow_html=True)
