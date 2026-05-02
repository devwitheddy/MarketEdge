"""pages/2_Stock_Tracker.py — MarketEdge"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.helpers import (
    GLOBAL_CSS, CHART_DEFAULTS, PALETTE,
    C_UP, C_DOWN, C_ACCENT, C_MUTED, C_TEXT, C_BORDER,
    lbl, fmt_currency, fmt_large, fmt_pct,
    chart_candle, chart_volume, chart_area, chart_rsi, sidebar_footer,
)
from utils.data_fetcher import (
    fetch_info, fetch_history, data_source_banner, POPULAR_STOCKS,
)

st.set_page_config(page_title="Stock Tracker · MarketEdge",
                   page_icon="🔍", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🔍 Stock Tracker")
    st.divider()
    st.markdown(
        f"<div style='font-size:0.79rem;color:#5C7A99;line-height:1.85'>"
        f"<b style='color:#E2EDF8'>Tips</b><br>"
        f"Use dropdown for popular stocks<br>"
        f"Or type any ticker manually<br>"
        f"Manual input overrides dropdown<br><br>"
        f"<b style='color:#E2EDF8'>Unsupported tickers</b><br>"
        f"Some regional stocks (e.g. NSE)<br>"
        f"may have limited data on Yahoo</div>",
        unsafe_allow_html=True,
    )
    st.divider()
    if st.button("🔄 Refresh", use_container_width=True):
        st.cache_data.clear(); st.rerun()
    sidebar_footer()

st.markdown("# 🔍 Stock Tracker")
st.caption("Search any stock on global exchanges · NYSE · NASDAQ · NSE · LSE")
st.divider()

PERIOD_MAP = {"1W":"5d","1M":"1mo","3M":"3mo","6M":"6mo","1Y":"1y","5Y":"5y"}

# ── Search controls ─────────────────────────────────────
sc1, sc2 = st.columns([3,2])
with sc1:
    lbl("Select from popular stocks")
    dropdown = st.selectbox("Stock", list(POPULAR_STOCKS.keys()),
                             index=0, label_visibility="collapsed")
    prefill  = POPULAR_STOCKS.get(dropdown,"")

with sc2:
    lbl("Or type any ticker manually")
    manual = st.text_input("Ticker",value=prefill,
        placeholder="e.g. AAPL · BTC-USD · ^GSPC",
        label_visibility="collapsed").upper().strip()

ticker = manual or prefill

# ── Chart options ───────────────────────────────────────
op1,op2,op3,op4 = st.columns(4)
with op1: period_lbl=st.selectbox("Period",list(PERIOD_MAP.keys()),index=4,
              label_visibility="collapsed"); period=PERIOD_MAP[period_lbl]
with op2: chart_type=st.radio("Chart",["Candlestick","Area"],
              horizontal=True,label_visibility="collapsed")
with op3: show_ma=st.checkbox("Moving Avg (MA20/50)",value=True)
with op4: show_bb=st.checkbox("Bollinger Bands",value=False)

st.divider()

if not ticker or ticker.startswith("──"):
    st.info("👆 Select a stock from the dropdown or type a ticker above.")
    st.stop()

# ── Fetch ───────────────────────────────────────────────
with st.spinner(f"Loading {ticker}…"):
    info, info_live = fetch_info(ticker)
    df,   hist_live = fetch_history(ticker, period)

# ── Safaricom / regional stock handling ─────────────────
if df.empty and not info.get("price"):
    st.error(
        f"**No data found for `{ticker}`.**\n\n"
        "Possible reasons:\n"
        "- This ticker is not available on Yahoo Finance\n"
        "- Regional stocks (e.g. NSE Safaricom `SCOM.NR`) have very limited "
        "coverage on Yahoo Finance and may return no data\n"
        "- Check the exact symbol at [finance.yahoo.com](https://finance.yahoo.com)\n\n"
        "**Try:** `AAPL` · `TSLA` · `BTC-USD` · `GC=F` (Gold) · `^GSPC` (S&P 500)"
    )
    st.stop()

# If we have partial data (info but no history, or vice versa)
if df.empty:
    st.warning(
        f"⚠️ Price history unavailable for `{ticker}` — "
        "showing available metadata only."
    )

data_source_banner(info_live and hist_live)

# ── Stock header ────────────────────────────────────────
price  = info.get("price",0)
change = info.get("change_pct",0)
col_h  = C_UP if change>=0 else C_DOWN
st.markdown(
    f"<div style='margin-bottom:0.4rem'>"
    f"<span style='font-size:1.45rem;font-weight:700;color:#E2EDF8'>"
    f"{info.get('name',ticker)}</span>"
    f"<code style='font-size:0.8rem;margin-left:0.55rem;color:#5C7A99;"
    f"background:#0B1526;padding:2px 7px;border-radius:4px'>{ticker}</code>"
    f"</div>"
    f"<div style='font-size:0.82rem;color:#5C7A99;margin-bottom:0.3rem'>"
    f"{info.get('sector','—')}  ·  {info.get('country','—')}  ·  "
    f"Currency: {info.get('currency','USD')}  ·  "
    f"Exchange: {info.get('exchange','—')}</div>",
    unsafe_allow_html=True,
)

# ── Metric strip ─────────────────────────────────────────
m1,m2,m3,m4,m5,m6 = st.columns(6)
m1.metric("Live Price",    fmt_currency(price),           fmt_pct(change))
m2.metric("Market Cap",    fmt_large(info.get("market_cap",0)))
m3.metric("P/E Ratio",     f"{info.get('pe_ratio') or '—'}")
m4.metric("52W High",      fmt_currency(info.get("high_52w",0)))
m5.metric("52W Low",       fmt_currency(info.get("low_52w",0)))
m6.metric("Volume",        fmt_large(info.get("volume",0),""))

st.divider()

if not df.empty:
    # ── Price chart ─────────────────────────────────────
    lbl(f"Price Chart  ·  {period_lbl}")
    if chart_type == "Candlestick":
        st.plotly_chart(chart_candle(df,ticker,show_ma,show_bb),
                        use_container_width=True)
    else:
        st.plotly_chart(chart_area(df,ticker),use_container_width=True)

    # ── Volume ───────────────────────────────────────────
    lbl("Trading Volume")
    st.plotly_chart(chart_volume(df),use_container_width=True)

    # ── RSI ──────────────────────────────────────────────
    lbl("RSI  ·  Relative Strength Index (14)")
    st.caption("Above 70 = overbought (red)  ·  Below 30 = oversold (green)  ·  50 = neutral")
    st.plotly_chart(chart_rsi(df),use_container_width=True)

    st.divider()

    # ── Period stats ─────────────────────────────────────
    lbl(f"Period Statistics  ·  {period_lbl}")
    ps1,ps2,ps3,ps4,ps5 = st.columns(5)
    ph   = df["High"].max()
    pl   = df["Low"].min()
    pret = ((df["Close"].iloc[-1]-df["Close"].iloc[0])/df["Close"].iloc[0])*100
    ps1.metric("Period High",  fmt_currency(ph))
    ps2.metric("Period Low",   fmt_currency(pl))
    ps3.metric("Return",       fmt_pct(pret))
    ps4.metric("Avg Volume",   f"{df['Volume'].mean()/1e6:.2f}M")
    ps5.metric("Volatility",   f"{df['Close'].pct_change().std()*100:.2f}% daily")

    st.divider()

    # ── Price distribution ────────────────────────────────
    lbl("Closing Price Distribution")
    fig_hist=go.Figure(go.Histogram(x=df["Close"],nbinsx=30,
        marker_color=C_ACCENT,marker_line_width=0,opacity=0.8))
    fig_hist.update_layout(**CHART_DEFAULTS,height=200,
        margin=dict(l=0,r=0,t=10,b=0),bargap=0.04,showlegend=False,
        xaxis=dict(showgrid=False,tickfont=dict(size=10)),
        yaxis=dict(showgrid=True,gridcolor=C_BORDER,gridwidth=0.4,
                   tickfont=dict(size=10)))
    st.plotly_chart(fig_hist,use_container_width=True)

# ── Company info ──────────────────────────────────────
desc    = info.get("description","")
website = info.get("website","")
emp     = info.get("employees")

if desc or website or emp:
    with st.expander("Company Information"):
        if emp:
            st.markdown(f"**Employees:** {emp:,}")
        if website:
            st.markdown(f"**Website:** [{website}]({website})")
        if desc:
            st.markdown(
                f"<p style='font-size:0.83rem;color:#5C7A99;line-height:1.65'>"
                f"{desc[:900]}{'…' if len(desc)>900 else ''}</p>",
                unsafe_allow_html=True,
            )

if not df.empty:
    with st.expander("Raw OHLCV Data"):
        show=df[["Open","High","Low","Close","Volume"]].copy().round(4)
        try: show.index=show.index.strftime("%Y-%m-%d")
        except: pass
        st.dataframe(show.sort_index(ascending=False),use_container_width=True)
