"""pages/5_Market_News.py — MarketEdge"""

import streamlit as st
from datetime import datetime
from utils.helpers import (
    GLOBAL_CSS, C_ACCENT, C_MUTED, C_TEXT, C_BORDER, C_CAPTION,
    lbl, sidebar_footer,
)
from utils.data_fetcher import fetch_news

st.set_page_config(page_title="Market News · MarketEdge",
                   page_icon="📰", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 📰 Market News")
    st.divider()
    st.markdown(
        f"<div style='font-size:0.79rem;color:{C_MUTED};line-height:1.85'>"
        f"<b style='color:{C_TEXT}'>Sourced from</b><br>"
        f"Reuters · Bloomberg · CNBC<br>"
        f"Yahoo Finance · MarketWatch<br>"
        f"Financial Times · and more<br><br>"
        f"<b style='color:{C_TEXT}'>Coverage</b><br>"
        f"Stocks · Crypto · Forex<br>"
        f"Macro · Earnings · IPOs</div>",
        unsafe_allow_html=True,
    )
    st.divider()
    if st.button("🔄 Refresh News", use_container_width=True):
        st.cache_data.clear(); st.rerun()
    sidebar_footer()

st.markdown("# 📰 Market News")
st.caption("Latest financial headlines · click any article to read the full story")
st.divider()

# ── Category tabs ────────────────────────────────────────
CATEGORIES = {
    "🌍 All Markets":   ["SPY","QQQ","^GSPC","BTC-USD","GC=F","^DJI"],
    "📈 Stocks":        ["SPY","QQQ","AAPL","MSFT","NVDA","TSLA","AMZN"],
    "₿ Crypto":         ["BTC-USD","ETH-USD","BNB-USD","SOL-USD"],
    "💱 Forex/Macro":   ["EURUSD=X","GC=F","CL=F","^TNX","DX-Y.NYB"],
    "🏦 Finance":       ["JPM","GS","BAC","V","MA"],
    "⚡ Energy":        ["CL=F","XOM","CVX","NG=F"],
}

tab_names = list(CATEGORIES.keys())
tabs = st.tabs(tab_names)

for tab, (cat, tickers) in zip(tabs, CATEGORIES.items()):
    with tab:
        hd_col, cnt_col = st.columns([4,1])
        with cnt_col:
            max_news = st.selectbox(
                "Show", [10,20,30], index=1,
                key=f"cnt_{cat}", label_visibility="collapsed",
            )

        with st.spinner(f"Loading {cat} news…"):
            articles = fetch_news(tickers, max_per_ticker=6)

        if not articles:
            st.warning(
                "No articles found right now. "
                "Click **Refresh News** in the sidebar to retry."
            )
            continue

        # Deduplicate
        seen, filtered = set(), []
        for a in articles:
            t = a["title"].strip().lower()
            if t not in seen:
                seen.add(t); filtered.append(a)
            if len(filtered) >= max_news:
                break

        hd_col.markdown(
            f'<span class="me-label">{len(filtered)} articles</span>',
            unsafe_allow_html=True,
        )

        for article in filtered:
            title   = article.get("title","No title")
            link    = article.get("link","#")
            pub     = article.get("publisher","")
            pub_dt  = article.get("published", datetime.utcnow())
            ticker  = article.get("ticker","")
            thumb   = article.get("thumbnail","")

            # Time ago
            now = datetime.utcnow()
            pub_naive = pub_dt.replace(tzinfo=None) if pub_dt.tzinfo else pub_dt
            diff = now - pub_naive
            mins = int(diff.total_seconds()/60)
            if   mins < 60:   time_ago = f"{mins}m ago"
            elif mins < 1440: time_ago = f"{mins//60}h ago"
            else:             time_ago = f"{mins//1440}d ago"
            date_str = pub_naive.strftime("%d %b %Y")

            badge = (
                f"<span style='background:{C_ACCENT};color:#fff;"
                f"font-size:0.64rem;font-weight:700;"
                f"padding:1px 6px;border-radius:3px;margin-right:5px'>"
                f"{ticker}</span>"
            )
            meta = (
                f"<div class='news-meta'>{badge}"
                f"{pub}  ·  {time_ago}  ·  {date_str}</div>"
            )
            card_body = (
                f"<div class='news-title'>{title}</div>"
                f"{meta}"
                f"<a class='news-link' href='{link}' target='_blank'>"
                f"Read full article →</a>"
            )

            if thumb:
                ic, tc = st.columns([1, 5])
                with ic:
                    try: st.image(thumb, use_column_width=True)
                    except: pass
                with tc:
                    st.markdown(f"<div class='news-card'>{card_body}</div>",
                                unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='news-card'>{card_body}</div>",
                            unsafe_allow_html=True)

        st.divider()
        st.caption(
            "News sourced from Yahoo Finance via yfinance. "
            "All articles link directly to their original publishers."
        )
