"""pages/1_Market_Overview.py — MarketEdge"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.helpers import (
    GLOBAL_CSS, CHART_DEFAULTS, PALETTE,
    C_UP, C_DOWN, C_ACCENT, C_MUTED, C_TEXT, C_BG, C_BORDER, C_SURFACE2,
    lbl, fmt_currency, fmt_pct, fmt_large,
    chart_bar_h, chart_line_compare, sidebar_footer,
)
from utils.data_fetcher import fetch_info, fetch_history, data_source_banner

st.set_page_config(page_title="Market Overview · MarketEdge",
                   page_icon="💹", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 💹 Market Overview")
    st.divider()
    if st.button("🔄 Refresh", use_container_width=True):
        st.cache_data.clear(); st.rerun()
    sidebar_footer()

st.markdown("# 💹 Market Overview")
st.caption("Live prices · refreshed every 5 minutes")
st.divider()

WATCHLIST = {
    "Apple":"AAPL","Microsoft":"MSFT","Google":"GOOGL",
    "Amazon":"AMZN","Tesla":"TSLA","NVIDIA":"NVDA",
}

# ── Prices ─────────────────────────────────────────────
lbl("Live Prices")
cols = st.columns(3); any_live=False; cache={}
with st.spinner("Fetching prices…"):
    for idx,(name,tkr) in enumerate(WATCHLIST.items()):
        info,live = fetch_info(tkr); cache[name]=info
        if live: any_live=True
        cols[idx%3].metric(f"{name}  ·  {tkr}",
            fmt_currency(info.get("price",0)),
            fmt_pct(info.get("change_pct",0)))
data_source_banner(any_live)
st.divider()

# ── Row: 30d perf + Market cap ─────────────────────────
c1, c2 = st.columns(2)
with c1:
    lbl("30-Day Performance")
    perf=[]
    with st.spinner():
        for name,tkr in WATCHLIST.items():
            df,_=fetch_history(tkr,"1mo")
            if not df.empty and len(df)>=2:
                ret=((df["Close"].iloc[-1]-df["Close"].iloc[0])/df["Close"].iloc[0])*100
                perf.append({"Company":name,"Return (%)":round(ret,2)})
    if perf:
        pdf=pd.DataFrame(perf).set_index("Company").sort_values("Return (%)")
        st.plotly_chart(chart_bar_h(pdf["Return (%)"],
            [C_UP if v>=0 else C_DOWN for v in pdf["Return (%)"]],
            height=270, x_title="30-Day Return (%)"), use_container_width=True)

with c2:
    lbl("Market Cap Comparison")
    cap={n:cache[n].get("market_cap",0) for n in WATCHLIST if cache.get(n,{}).get("market_cap",0)>0}
    if cap:
        cs=pd.Series(cap).sort_values()
        fig=go.Figure(go.Bar(x=cs.values,y=cs.index,orientation="h",
            marker_color=PALETTE[:len(cs)],marker_line_width=0,
            text=[f"{v/1e12:.2f}T" if v>=1e12 else f"{v/1e9:.0f}B" for v in cs.values],
            textposition="outside",textfont=dict(size=11,color=C_TEXT)))
        fig.update_layout(**CHART_DEFAULTS,height=270,
            margin=dict(l=0,r=65,t=10,b=0),
            xaxis=dict(showgrid=True,gridcolor=C_BORDER,tickformat=".2s",tickfont=dict(size=10)),
            yaxis=dict(showgrid=False,tickfont=dict(size=11)))
        st.plotly_chart(fig,use_container_width=True)

st.divider()

# ── 1-year normalised comparison ───────────────────────
lbl("1-Year Trend Comparison")
st.caption("Normalised % return — compare stocks at different price levels fairly")
chosen=st.multiselect("Companies:",list(WATCHLIST.keys()),
    default=["Apple","Microsoft","NVIDIA"],label_visibility="collapsed")
if chosen:
    series={}
    with st.spinner("Loading…"):
        for n in chosen:
            df,_=fetch_history(WATCHLIST[n],"1y"); series[n]=df
    st.plotly_chart(chart_line_compare(series,height=360),use_container_width=True)
st.divider()

# ── Row: Volume + P/E ──────────────────────────────────
v1, v2 = st.columns(2)
with v1:
    lbl("Avg Daily Volume  ·  30 Days")
    vrows=[]
    with st.spinner():
        for name,tkr in WATCHLIST.items():
            df,_=fetch_history(tkr,"1mo")
            if not df.empty: vrows.append({"Company":name,"Avg Vol":int(df["Volume"].mean())})
    if vrows:
        vdf=pd.DataFrame(vrows).set_index("Company").sort_values("Avg Vol")
        fig=go.Figure(go.Bar(x=vdf["Avg Vol"],y=vdf.index,orientation="h",
            marker_color=PALETTE[:len(vdf)],marker_line_width=0,
            text=[f"{v/1e6:.1f}M" for v in vdf["Avg Vol"]],
            textposition="outside",textfont=dict(size=11,color=C_TEXT)))
        fig.update_layout(**CHART_DEFAULTS,height=260,
            margin=dict(l=0,r=65,t=10,b=0),
            xaxis=dict(showgrid=True,gridcolor=C_BORDER,tickformat=".2s",tickfont=dict(size=10)),
            yaxis=dict(showgrid=False,tickfont=dict(size=11)))
        st.plotly_chart(fig,use_container_width=True)

with v2:
    lbl("P/E Ratio Comparison")
    pe={n:cache[n].get("pe_ratio") for n in WATCHLIST if cache.get(n,{}).get("pe_ratio")}
    if pe:
        ps=pd.Series(pe).sort_values()
        fig=go.Figure(go.Bar(x=ps.values,y=ps.index,orientation="h",
            marker_color=C_ACCENT,marker_line_width=0,
            text=[f"{v:.1f}x" for v in ps.values],
            textposition="outside",textfont=dict(size=11,color=C_TEXT)))
        fig.update_layout(**CHART_DEFAULTS,height=260,
            margin=dict(l=0,r=60,t=10,b=0),
            xaxis=dict(showgrid=True,gridcolor=C_BORDER,tickfont=dict(size=10)),
            yaxis=dict(showgrid=False,tickfont=dict(size=11)))
        st.plotly_chart(fig,use_container_width=True)

st.divider()

# ── Key stats table ─────────────────────────────────────
lbl("Key Statistics Table")
rows=[]
for name,tkr in WATCHLIST.items():
    info=cache.get(name,{})
    rows.append({
        "Company":name,"Ticker":tkr,
        "Price":fmt_currency(info.get("price",0)),
        "Change":fmt_pct(info.get("change_pct",0)),
        "Mkt Cap":fmt_large(info.get("market_cap",0)),
        "P/E":f"{info.get('pe_ratio') or '—'}",
        "52W High":fmt_currency(info.get("high_52w",0)),
        "52W Low":fmt_currency(info.get("low_52w",0)),
        "Volume":fmt_large(info.get("volume",0),""),
    })
st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
