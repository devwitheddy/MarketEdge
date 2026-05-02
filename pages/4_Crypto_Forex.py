"""pages/4_Crypto_Forex.py — MarketEdge"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.helpers import (
    GLOBAL_CSS, CHART_DEFAULTS, PALETTE,
    C_UP, C_DOWN, C_ACCENT, C_MUTED, C_TEXT, C_BORDER,
    lbl, fmt_currency, fmt_pct, fmt_large,
    chart_area, sidebar_footer,
)
from utils.data_fetcher import (
    fetch_info, fetch_history, fetch_forex_rate, data_source_banner,
)

st.set_page_config(page_title="Crypto & Forex · MarketEdge",
                   page_icon="₿", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ₿ Crypto & Forex")
    st.divider()
    if st.button("🔄 Refresh", use_container_width=True):
        st.cache_data.clear(); st.rerun()
    sidebar_footer()

st.markdown("# ₿  Crypto & Forex")
st.caption("Live cryptocurrency prices and currency exchange rates")
st.divider()

CRYPTOS = {"Bitcoin":"BTC-USD","Ethereum":"ETH-USD","BNB":"BNB-USD",
           "Solana":"SOL-USD","XRP":"XRP-USD"}

# ── Crypto prices ───────────────────────────────────────
lbl("Live Crypto Prices")
c_cols=st.columns(5); any_live=False; c_info={}
with st.spinner("Fetching…"):
    for i,(name,tkr) in enumerate(CRYPTOS.items()):
        info,live=fetch_info(tkr); c_info[name]=info
        if live: any_live=True
        c_cols[i].metric(name,fmt_currency(info.get("price",0)),
                          fmt_pct(info.get("change_pct",0)))
data_source_banner(any_live)
st.divider()

# ── Crypto chart + 24H bar ──────────────────────────────
ch1,ch2=st.columns([3,2])
with ch1:
    lbl("Price Chart")
    cx1,cx2=st.columns(2)
    sel_coin=cx1.selectbox("Coin",list(CRYPTOS.keys()),label_visibility="collapsed")
    sel_per =cx2.radio("Period",["1mo","3mo","6mo","1y"],horizontal=True,
                label_visibility="collapsed",
                format_func=lambda x:x.replace("mo","M").replace("y","Y"))
    with st.spinner(f"Loading {sel_coin}…"):
        c_df,_=fetch_history(CRYPTOS[sel_coin],sel_per)
    if not c_df.empty:
        st.plotly_chart(chart_area(c_df,sel_coin,height=290),use_container_width=True)

with ch2:
    lbl("24H Performance")
    perf_s=pd.Series({n:c_info[n].get("change_pct",0) for n in CRYPTOS}).sort_values()
    fig=go.Figure(go.Bar(x=perf_s.values,y=perf_s.index,orientation="h",
        marker_color=[C_UP if v>=0 else C_DOWN for v in perf_s.values],
        marker_line_width=0,
        text=[f"{v:+.2f}%" for v in perf_s.values],
        textposition="outside",textfont=dict(size=11,color=C_TEXT)))
    fig.update_layout(**CHART_DEFAULTS,height=290,
        margin=dict(l=0,r=70,t=10,b=0),
        xaxis=dict(showgrid=True,gridcolor=C_BORDER,
                   zeroline=True,zerolinecolor=C_BORDER,tickfont=dict(size=10)),
        yaxis=dict(showgrid=False,tickfont=dict(size=11)))
    st.plotly_chart(fig,use_container_width=True)

st.divider()

# ── Crypto stats table ──────────────────────────────────
lbl("Key Statistics")
st.dataframe(pd.DataFrame([{
    "Coin":name,"Price":fmt_currency(info.get("price",0)),
    "24H Change":fmt_pct(info.get("change_pct",0)),
    "Market Cap":fmt_large(info.get("market_cap",0)),
    "52W High":fmt_currency(info.get("high_52w",0)),
    "52W Low":fmt_currency(info.get("low_52w",0)),
} for name,info in c_info.items()]),use_container_width=True,hide_index=True)

st.divider()

# ── Forex rates ─────────────────────────────────────────
lbl("Live Exchange Rates  ·  1 base → target")
FOREX_PAIRS=[("USD","KES"),("EUR","KES"),("GBP","KES"),
             ("USD","EUR"),("USD","GBP"),("USD","NGN")]
fx_cols=st.columns(3); any_fx=False
with st.spinner("Fetching rates…"):
    for i,(fc,tc) in enumerate(FOREX_PAIRS):
        rate,live=fetch_forex_rate(fc,tc)
        if live: any_fx=True
        src="📡" if live else "📁"
        if rate: fx_cols[i%3].metric(f"{src}  {fc} → {tc}",f"{rate:,.4f} {tc}")
        else: fx_cols[i%3].metric(f"{fc} → {tc}","N/A")
if not any_fx:
    st.warning("Showing fallback rates — live forex temporarily unavailable.")

st.divider()

# ── Currency converter ──────────────────────────────────
lbl("Currency Converter")
st.caption("Supports: USD · KES · EUR · GBP · NGN · BTC · ETH · BNB · SOL · XRP")
CURRENCIES=["USD","KES","EUR","GBP","NGN","BTC","ETH","BNB","SOL","XRP"]
cv1,cv2,cv3=st.columns([2,1,1])
amount  =cv1.number_input("Amount",min_value=0.000001,value=100.0,
              step=1.0,format="%.4f",label_visibility="collapsed")
from_cur=cv2.selectbox("From",CURRENCIES,index=0,label_visibility="collapsed")
to_cur  =cv3.selectbox("To",  CURRENCIES,index=1,label_visibility="collapsed")

if from_cur==to_cur:
    st.info(f"**{amount:,.4f} {from_cur}** = **{amount:,.4f} {to_cur}**")
else:
    with st.spinner("Fetching rate…"):
        rate,live=fetch_forex_rate(from_cur,to_cur)
    if rate:
        converted=amount*rate
        src="📡 Live" if live else "📁 Fallback"
        st.success(
            f"**{amount:,.4f} {from_cur}**  →  **{converted:,.4f} {to_cur}**  \n"
            f"{src} rate:  1 {from_cur} = {rate:,.6f} {to_cur}"
        )
        rev,_=fetch_forex_rate(to_cur,from_cur)
        if rev: st.caption(f"↩ Reverse: 1 {to_cur} = {rev:,.6f} {from_cur}")
    else:
        st.error(
            f"Rate unavailable for **{from_cur} → {to_cur}**.  \n"
            "Try USD → KES, BTC → USD, or ETH → KES."
        )
