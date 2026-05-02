"""pages/3_My_Portfolio.py — MarketEdge"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.helpers import (
    GLOBAL_CSS, CHART_DEFAULTS, PALETTE,
    C_UP, C_DOWN, C_ACCENT, C_MUTED, C_TEXT, C_BG, C_BORDER, C_SURFACE2,
    lbl, fmt_currency, fmt_pct, chart_pie, sidebar_footer,
)
from utils.portfolio import (
    init_portfolio, get_portfolio,
    add_position, remove_position, clear_portfolio,
    calculate_portfolio,
)
from utils.data_fetcher import fetch_history, POPULAR_STOCKS

st.set_page_config(page_title="My Portfolio · MarketEdge",
                   page_icon="💼", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
init_portfolio()

with st.sidebar:
    st.markdown("### 💼 My Portfolio")
    st.divider()
    st.markdown(
        "<div style='font-size:0.79rem;color:#5C7A99;line-height:1.85'>"
        "<b style='color:#E2EDF8'>How it works</b><br>"
        "1. Pick from dropdown or type ticker<br>"
        "2. Enter shares + buy price<br>"
        "3. Live gain/loss auto-calculated<br><br>"
        "<b style='color:#E2EDF8'>Note</b><br>"
        "Resets on app close (session only)</div>",
        unsafe_allow_html=True,
    )
    st.divider()
    if st.button("🔄 Refresh Prices", use_container_width=True):
        st.cache_data.clear(); st.rerun()
    sidebar_footer()

st.markdown("# 💼 My Portfolio")
st.caption("Track your personal holdings · live gain/loss calculated automatically")
st.divider()

# ── Add position ────────────────────────────────────────
lbl("Add a Position")
with st.form("add_form", clear_on_submit=True):
    f1, f2, f3, f4 = st.columns([2,2,1,1])

    with f1:
        dropdown = st.selectbox("Stock",list(POPULAR_STOCKS.keys()),
                                 index=0,label_visibility="collapsed")
        prefill  = POPULAR_STOCKS.get(dropdown,"")

    with f2:
        manual = st.text_input("Or type ticker",value=prefill,
            placeholder="e.g. AAPL",
            label_visibility="collapsed").upper().strip()

    with f3:
        new_qty = st.number_input("Shares",min_value=0.001,
            value=1.0,step=0.001,format="%.3f",
            label_visibility="collapsed")
    with f4:
        new_cost = st.number_input("Buy Price $",min_value=0.01,
            value=100.0,step=0.01,format="%.2f",
            label_visibility="collapsed")

    submitted = st.form_submit_button("Add to Portfolio", use_container_width=True)

if submitted:
    chosen_ticker = (manual or prefill or "").upper().strip()
    if not chosen_ticker or chosen_ticker.startswith("──"):
        st.error("Please select or type a ticker symbol.")
    else:
        with st.spinner(f"Validating {chosen_ticker}…"):
            ok, msg = add_position(chosen_ticker, new_qty, new_cost)
        if ok: st.success(msg); st.rerun()
        else:  st.error(msg)

portfolio = get_portfolio()
if not portfolio:
    st.divider()
    st.info("Your portfolio is empty. Add your first position above.")
    st.stop()

st.divider()

with st.spinner("Fetching live prices…"):
    rows_df, totals = calculate_portfolio()

# ── KPI strip ────────────────────────────────────────────
lbl("Summary")
k1,k2,k3,k4,k5 = st.columns(5)
k1.metric("Total Invested",    fmt_currency(totals["invested"]))
k2.metric("Current Value",     fmt_currency(totals["value"]))
k3.metric("Total Gain / Loss", fmt_currency(totals["gain_loss"]),
           fmt_pct(totals["gl_pct"]))
k4.metric("Positions",         str(totals["positions"]))
best = rows_df.loc[rows_df["Return (%)"].idxmax()] if not rows_df.empty else None
if best is not None:
    k5.metric("Best Performer", best["Ticker"],
               fmt_pct(best["Return (%)"]))

st.divider()

# ── Holdings table ──────────────────────────────────────
lbl("Holdings")
disp = rows_df[[
    "Ticker","Name","Shares","Buy Price","Current Price",
    "Invested ($)","Value ($)","Gain / Loss ($)","Return (%)","Live",
]].copy()

def _c(val):
    try:
        v=float(str(val).replace("$","").replace(",","").replace("%","").replace("+",""))
        return f"color:{C_UP};font-weight:600" if v>=0 else f"color:{C_DOWN};font-weight:600"
    except: return ""

st.dataframe(
    disp.style.applymap(_c,subset=["Return (%)","Gain / Loss ($)"]),
    use_container_width=True, hide_index=True,
)
st.divider()

# ── Allocation chart + legend ────────────────────────────
lbl("Allocation by Current Value")
pie_col, leg_col = st.columns([1,1])
with pie_col:
    st.plotly_chart(chart_pie(rows_df["Ticker"].tolist(),
        rows_df["Value ($)"].tolist()),use_container_width=True)
with leg_col:
    st.markdown("<div style='height:1rem'></div>",unsafe_allow_html=True)
    for i,row in rows_df.iterrows():
        color=C_UP if row["Return (%)"]>=0 else C_DOWN
        dot=PALETTE[i%len(PALETTE)]
        sign="+" if row["Return (%)"]>=0 else ""
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;"
            f"align-items:center;padding:0.42rem 0;border-bottom:1px solid {C_BORDER}'>"
            f"<div style='display:flex;align-items:center;gap:0.45rem'>"
            f"<div style='width:9px;height:9px;border-radius:50%;background:{dot}'></div>"
            f"<span style='color:#E2EDF8;font-size:0.83rem;font-weight:600'>{row['Ticker']}</span>"
            f"<span style='color:#5C7A99;font-size:0.74rem'>{str(row['Name'])[:20]}</span>"
            f"</div>"
            f"<div style='text-align:right'>"
            f"<div style='color:{color};font-size:0.83rem;font-weight:600'>"
            f"{sign}{row['Return (%)']:.2f}%</div>"
            f"<div style='color:#5C7A99;font-size:0.72rem'>${row['Value ($)']:,.2f}</div>"
            f"</div></div>",
            unsafe_allow_html=True,
        )

st.divider()

# ── 6-month trend overlay ────────────────────────────────
lbl("6-Month Price Trend  ·  All Holdings")
fig_trend=go.Figure()
with st.spinner("Loading trends…"):
    for i,item in enumerate(portfolio):
        df,_=fetch_history(item["ticker"],"6mo")
        if not df.empty:
            norm=((df["Close"]-df["Close"].iloc[0])/df["Close"].iloc[0])*100
            fig_trend.add_trace(go.Scatter(x=df.index,y=norm,
                name=item["ticker"],mode="lines",
                line=dict(color=PALETTE[i%len(PALETTE)],width=2),
                hovertemplate=f"<b>{item['ticker']}</b>  %{{y:+.2f}}%<extra></extra>"))

if fig_trend.data:
    fig_trend.update_layout(**CHART_DEFAULTS,height=300,
        margin=dict(l=0,r=0,t=10,b=0),yaxis_title="% Return",
        xaxis=dict(showgrid=False,tickfont=dict(size=10)),
        yaxis=dict(showgrid=True,gridcolor=C_BORDER,gridwidth=0.4,
                   tickfont=dict(size=10),zeroline=True,zerolinecolor=C_BORDER))
    st.plotly_chart(fig_trend,use_container_width=True)
else:
    st.info("Trend data unavailable for current holdings.")

st.divider()

# ── Risk metrics ─────────────────────────────────────────
lbl("Risk Metrics  ·  Based on 1-Year Daily Returns")
rk_rows=[]
with st.spinner("Calculating risk…"):
    for item in portfolio:
        df,_=fetch_history(item["ticker"],"1y")
        if not df.empty and len(df)>20:
            daily_ret=df["Close"].pct_change().dropna()
            vol=daily_ret.std()*100
            ann_vol=vol*(252**0.5)
            max_dd_val=((df["Close"]/df["Close"].cummax())-1).min()*100
            sharpe=(daily_ret.mean()/daily_ret.std())*(252**0.5) if daily_ret.std()>0 else 0
            rk_rows.append({"Ticker":item["ticker"],
                "Daily Volatility":f"{vol:.2f}%",
                "Annual Volatility":f"{ann_vol:.1f}%",
                "Max Drawdown":f"{max_dd_val:.1f}%",
                "Sharpe Ratio":f"{sharpe:.2f}"})

if rk_rows:
    st.dataframe(pd.DataFrame(rk_rows),use_container_width=True,hide_index=True)

st.divider()

# ── Manage ───────────────────────────────────────────────
lbl("Manage Positions")
r1,r2,r3=st.columns([2,1,1])
with r1:
    to_remove=st.selectbox("Select:",[p["ticker"] for p in portfolio],
        label_visibility="collapsed")
with r2:
    if st.button(f"Remove {to_remove}",type="secondary",use_container_width=True):
        remove_position(to_remove); st.rerun()
with r3:
    if st.button("Clear All",type="secondary",use_container_width=True):
        clear_portfolio(); st.rerun()

st.caption("⚠️ Portfolio resets when the app is closed — session storage only.")
