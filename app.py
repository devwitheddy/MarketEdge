"""MarketEdge — app.py  |  streamlit run app.py"""

import streamlit as st
from datetime import datetime
from utils.helpers import GLOBAL_CSS, C_ACCENT, C_UP, C_DOWN, C_SURFACE, C_BORDER, C_MUTED, C_TEXT, C_CAPTION

st.set_page_config(
    page_title = "MarketEdge",
    page_icon  = "💹",
    layout     = "wide",
    initial_sidebar_state = "expanded",
)
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💹 MarketEdge")
    st.caption("Live Financial Intelligence")
    st.divider()
    if st.button("🔄  Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.caption(f"🕐  {datetime.now().strftime('%d %b %Y  %H:%M')}")

# ── Hero ───────────────────────────────────────────────
st.markdown("# 💹 MarketEdge")
st.markdown(
    f"<p style='font-size:0.95rem;color:{C_MUTED};margin-top:-0.3rem'>"
    "Real-time financial intelligence — live market data, interactive charts, "
    "portfolio tracking, news and currency conversion.</p>",
    unsafe_allow_html=True,
)
st.divider()

# ── Nav cards (fully clickable via st.page_link) ───────
st.markdown('<span class="me-label">Navigate</span>', unsafe_allow_html=True)

PAGES = [
    ("💹",  "pages/1_Market_Overview.py", "Market Overview",
     "Live prices · 30-day returns · trend charts"),
    ("🔍", "pages/2_Stock_Tracker.py",   "Stock Tracker",
     "Any ticker · Candlestick · RSI · Bollinger"),
    ("💼", "pages/3_My_Portfolio.py",    "My Portfolio",
     "Live gain/loss · allocation · risk metrics"),
    ("₿",  "pages/4_Crypto_Forex.py",    "Crypto & Forex",
     "Crypto prices · USD→KES · converter"),
    ("📰", "pages/5_Market_News.py",     "Market News",
     "Live headlines · 6 categories · source links"),
]

cols = st.columns(5)
for col, (icon, path, title, desc) in zip(cols, PAGES):
    with col:
        # Visual card (not clickable — just for display)
        st.markdown(
            f"<div style='"
            f"background:#0B1526;border:1px solid #162236;"
            f"border-radius:10px;padding:1rem 1rem 0.7rem 1rem;"
            f"margin-bottom:0.4rem;min-height:100px'>"
            f"<div style='font-size:1.4rem;margin-bottom:0.3rem'>{icon}</div>"
            f"<div style='font-size:0.88rem;font-weight:700;"
            f"color:#E2EDF8;margin-bottom:0.25rem'>{title}</div>"
            f"<div style='font-size:0.75rem;color:#5C7A99;"
            f"line-height:1.45'>{desc}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
        # Clickable link button below the card
        st.page_link(path, label="Open →", use_container_width=True)

st.divider()

# ── Live market snapshot ───────────────────────────────
st.markdown('<span class="me-label">Live Market Snapshot</span>', unsafe_allow_html=True)

from utils.data_fetcher import fetch_info

SNAP = [
    ("S&P 500",  "^GSPC"),
    ("NASDAQ",   "^IXIC"),
    ("Dow Jones","^DJI"),
    ("Bitcoin",  "BTC-USD"),
    ("Gold",     "GC=F"),
    ("Crude Oil","CL=F"),
]

snap_cols = st.columns(6)
with st.spinner("Loading…"):
    for i, (name, tkr) in enumerate(SNAP):
        info, _ = fetch_info(tkr)
        price   = info.get("price", 0)
        change  = info.get("change_pct", 0)
        color   = C_UP if change >= 0 else C_DOWN
        arrow   = "▲" if change >= 0 else "▼"
        snap_cols[i].markdown(
            f"<div class='stat-box'>"
            f"<div class='stat-val'>${price:,.2f}</div>"
            f"<div style='color:{color};font-size:0.76rem;font-weight:600;margin:0.1rem 0'>"
            f"{arrow} {abs(change):.2f}%</div>"
            f"<div class='stat-lbl'>{name}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

st.divider()

# ── Quick stats row ────────────────────────────────────
st.markdown('<span class="me-label">Quick Currency Rates</span>', unsafe_allow_html=True)
from utils.data_fetcher import fetch_forex_rate

FX_QUICK = [
    ("USD","KES"), ("EUR","KES"), ("GBP","KES"),
    ("USD","EUR"), ("USD","GBP"), ("USD","NGN"),
]
fx_cols = st.columns(6)
with st.spinner("Loading rates…"):
    for i,(fc,tc) in enumerate(FX_QUICK):
        rate, live = fetch_forex_rate(fc,tc)
        src = "📡" if live else "📁"
        if rate:
            fx_cols[i].markdown(
                f"<div class='stat-box'>"
                f"<div class='stat-val'>{rate:,.4f}</div>"
                f"<div style='font-size:0.68rem;color:{C_MUTED};margin:0.1rem 0'>{src}</div>"
                f"<div class='stat-lbl'>{fc} → {tc}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

st.divider()
st.markdown(
    f"<p style='font-size:0.77rem;color:{C_CAPTION}'>"
    "Data: Yahoo Finance · Prices refresh every 5 min · "
    "Falls back to sample data when live data is unavailable.</p>",
    unsafe_allow_html=True,
)
