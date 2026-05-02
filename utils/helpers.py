"""utils/helpers.py — MarketEdge design system"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ── Colours ────────────────────────────────────────────
C_BG       = "#060D1A"
C_SURFACE  = "#0B1526"
C_SURFACE2 = "#0F1D33"
C_SIDEBAR  = "#070E1C"
C_BORDER   = "#162236"
C_BORDER2  = "#1E3050"
C_ACCENT   = "#1C8EF9"
C_ACCENT2  = "#0D6EFD"
C_UP       = "#00C896"
C_DOWN     = "#FF4560"
C_WARN     = "#F59E0B"
C_TEXT     = "#E2EDF8"
C_MUTED    = "#5C7A99"
C_CAPTION  = "#344D66"
PALETTE    = [C_ACCENT,"#00C896","#F59E0B","#A78BFA",
              "#F472B6","#34D399","#FB923C","#60A5FA"]

CHART_DEFAULTS = dict(
    template      = "plotly_dark",
    paper_bgcolor = C_BG,
    plot_bgcolor  = C_SURFACE,
    font          = dict(color=C_TEXT, family="Inter, system-ui, sans-serif", size=12),
    hoverlabel    = dict(bgcolor=C_SURFACE2, bordercolor=C_BORDER2,
                         font_size=12, font_color=C_TEXT),
    legend        = dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)",
                         orientation="h", yanchor="bottom", y=1.02,
                         xanchor="left", x=0, font=dict(size=11, color=C_MUTED)),
)

GLOBAL_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] {{ font-family: 'Inter', system-ui, sans-serif !important; }}

/* ── Scaffold ── */
[data-testid="stAppViewContainer"] {{ background: {C_BG} !important; }}
[data-testid="stHeader"] {{ background: {C_BG} !important;
    border-bottom: 1px solid {C_BORDER} !important; }}
.main .block-container {{ padding: 1.6rem 2.2rem 2rem !important;
    max-width: 1320px !important; }}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{ background: {C_SIDEBAR} !important;
    border-right: 1px solid {C_BORDER} !important; }}
[data-testid="stSidebar"] > div {{ padding: 1.1rem 0.9rem !important; }}
section[data-testid="stSidebar"] * {{ color: {C_TEXT} !important; }}
[data-testid="stSidebarNav"] a {{ border-radius: 6px !important;
    padding: 0.3rem 0.6rem !important; }}
[data-testid="stSidebarNav"] a:hover {{ background: {C_SURFACE} !important; }}

/* ── Type ── */
h1 {{ font-size:1.55rem !important; font-weight:700 !important;
     color:{C_TEXT} !important; letter-spacing:-0.3px !important;
     line-height:1.2 !important; margin-bottom:0.05rem !important; }}
h2 {{ font-size:1.05rem !important; font-weight:600 !important;
     color:{C_TEXT} !important; margin-bottom:0.05rem !important; }}
h3 {{ font-size:0.88rem !important; font-weight:500 !important;
     color:{C_MUTED} !important; }}
p, li {{ color:{C_MUTED} !important; font-size:0.87rem !important;
         line-height:1.6 !important; }}
[data-testid="stCaptionContainer"] p {{ color:{C_CAPTION} !important;
    font-size:0.75rem !important; }}

/* ── Section label ── */
.me-label {{ display:block; font-size:0.67rem; font-weight:700;
    letter-spacing:0.09em; text-transform:uppercase; color:{C_MUTED};
    border-left:3px solid {C_ACCENT}; padding-left:0.5rem;
    margin:0 0 0.7rem 0; }}

/* ── Metrics ── */
[data-testid="stMetric"] {{ background:{C_SURFACE}; border:1px solid {C_BORDER};
    border-radius:8px; padding:0.85rem 1.05rem !important; min-height:86px;
    transition:border-color 0.15s, background 0.15s; }}
[data-testid="stMetric"]:hover {{ border-color:{C_ACCENT}; background:{C_SURFACE2}; }}
[data-testid="stMetricLabel"] > div {{ font-size:0.67rem !important;
    font-weight:700 !important; letter-spacing:0.07em !important;
    text-transform:uppercase !important; color:{C_MUTED} !important; }}
[data-testid="stMetricValue"] {{ font-size:1.3rem !important; font-weight:700 !important;
    color:{C_TEXT} !important; line-height:1.2 !important; }}
[data-testid="stMetricDelta"] svg {{ display:none !important; }}
[data-testid="stMetricDelta"] > div {{ font-size:0.75rem !important;
    font-weight:600 !important; margin-top:0.1rem !important; }}

/* ── Divider ── */
hr {{ border:none !important; border-top:1px solid {C_BORDER} !important;
     margin:1rem 0 !important; }}

/* ── Buttons ── */
.stButton > button {{ background:{C_ACCENT}; color:#fff; border:none;
    border-radius:6px; font-size:0.81rem; font-weight:600;
    padding:0.4rem 0.95rem; transition:background 0.15s, box-shadow 0.15s;
    box-shadow:0 1px 4px rgba(0,0,0,.45); }}
.stButton > button:hover {{ background:#3A9FFF;
    box-shadow:0 0 0 3px rgba(28,142,249,.2); }}
.stButton > button[kind="secondary"] {{ background:transparent;
    color:{C_MUTED} !important; border:1px solid {C_BORDER} !important;
    box-shadow:none; }}
.stButton > button[kind="secondary"]:hover {{ border-color:{C_BORDER2} !important;
    color:{C_TEXT} !important; }}

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {{ background:{C_SURFACE} !important;
    color:{C_TEXT} !important; border:1px solid {C_BORDER} !important;
    border-radius:6px !important; font-size:0.87rem !important; }}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {{ border-color:{C_ACCENT} !important;
    box-shadow:0 0 0 2px rgba(28,142,249,.15) !important; outline:none !important; }}
[data-baseweb="select"] > div {{ background:{C_SURFACE} !important;
    border:1px solid {C_BORDER} !important; border-radius:6px !important;
    color:{C_TEXT} !important; }}
[data-baseweb="menu"] {{ background:{C_SURFACE2} !important;
    border:1px solid {C_BORDER} !important; border-radius:6px !important; }}
[data-baseweb="option"] {{ background:{C_SURFACE2} !important;
    color:{C_TEXT} !important; font-size:0.85rem !important; }}
[data-baseweb="option"]:hover {{ background:{C_SURFACE} !important; }}
[data-baseweb="tag"] {{ background:{C_ACCENT} !important;
    border-radius:4px !important; }}
[data-testid="stCheckbox"] label p,
[data-testid="stRadio"] label p {{ color:{C_MUTED} !important;
    font-size:0.83rem !important; }}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {{ border:1px solid {C_BORDER};
    border-radius:8px; overflow:hidden; }}
[data-testid="stDataFrame"] th {{ background:{C_SURFACE2} !important;
    color:{C_MUTED} !important; font-size:0.69rem !important;
    font-weight:700 !important; letter-spacing:0.06em !important;
    text-transform:uppercase !important; padding:0.5rem 0.7rem !important;
    border-bottom:1px solid {C_BORDER} !important; }}
[data-testid="stDataFrame"] td {{ color:{C_TEXT} !important;
    font-size:0.83rem !important; padding:0.44rem 0.7rem !important;
    border-bottom:1px solid {C_BORDER} !important; }}

/* ── Alerts ── */
[data-testid="stAlert"] {{ border-radius:6px !important;
    font-size:0.83rem !important; padding:0.55rem 0.85rem !important;
    border-left-width:3px !important; }}
.stSuccess {{ background:rgba(0,200,150,.07) !important;
    border-color:{C_UP} !important; }}
.stError   {{ background:rgba(255,69,96,.07) !important;
    border-color:{C_DOWN} !important; }}
.stInfo    {{ background:rgba(28,142,249,.07) !important;
    border-color:{C_ACCENT} !important; }}
.stWarning {{ background:rgba(245,158,11,.07) !important;
    border-color:{C_WARN} !important; }}
.stSuccess p,.stError p,.stInfo p,.stWarning p {{ color:{C_TEXT} !important; }}

/* ── Expander ── */
[data-testid="stExpander"] {{ background:{C_SURFACE};
    border:1px solid {C_BORDER}; border-radius:8px; }}
[data-testid="stExpander"] summary {{ font-size:0.83rem;
    font-weight:600; color:{C_MUTED} !important; }}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{ background:{C_SURFACE};
    border-radius:7px; padding:3px; gap:2px; border:1px solid {C_BORDER}; }}
.stTabs [data-baseweb="tab"] {{ border-radius:5px; font-size:0.81rem;
    font-weight:500; color:{C_MUTED} !important; padding:0.3rem 0.8rem; }}
.stTabs [aria-selected="true"] {{ background:{C_ACCENT} !important;
    color:#fff !important; }}

/* ── Form ── */
[data-testid="stForm"] {{ background:{C_SURFACE};
    border:1px solid {C_BORDER}; border-radius:10px;
    padding:1rem 1.3rem !important; }}

/* ── Page link cards ── */
[data-testid="stPageLink"] a {{ background:{C_SURFACE} !important;
    border:1px solid {C_BORDER} !important; border-radius:10px !important;
    padding:1.2rem 1.3rem !important; text-decoration:none !important;
    display:block !important; transition:border-color .18s, background .18s,
    transform .15s !important; }}
[data-testid="stPageLink"] a:hover {{ border-color:{C_ACCENT} !important;
    background:{C_SURFACE2} !important; transform:translateY(-2px) !important; }}
[data-testid="stPageLink"] p {{ color:{C_TEXT} !important;
    font-size:0.9rem !important; font-weight:600 !important; }}

/* ── Columns equal padding ── */
[data-testid="column"] {{ padding:0 0.3rem !important; }}
[data-testid="column"]:first-child {{ padding-left:0 !important; }}
[data-testid="column"]:last-child  {{ padding-right:0 !important; }}

/* ── News card ── */
.news-card {{ background:{C_SURFACE}; border:1px solid {C_BORDER};
    border-radius:8px; padding:0.9rem 1.1rem; margin-bottom:0.6rem;
    transition:border-color .15s; }}
.news-card:hover {{ border-color:{C_BORDER2}; }}
.news-title {{ font-size:0.9rem; font-weight:600; color:{C_TEXT};
    line-height:1.4; margin-bottom:0.3rem; }}
.news-meta  {{ font-size:0.72rem; color:{C_CAPTION}; margin-bottom:0.4rem; }}
.news-link  {{ font-size:0.77rem; color:{C_ACCENT}; text-decoration:none; font-weight:500; }}
.news-link:hover {{ text-decoration:underline; }}

/* ── Stat strip ── */
.stat-box {{ background:{C_SURFACE}; border:1px solid {C_BORDER};
    border-radius:8px; padding:0.7rem 1rem; text-align:center; }}
.stat-val {{ font-size:1.05rem; font-weight:700; color:{C_TEXT}; }}
.stat-lbl {{ font-size:0.67rem; color:{C_MUTED}; margin-top:0.12rem;
    text-transform:uppercase; letter-spacing:0.06em; }}
</style>
"""

# ── Helpers ────────────────────────────────────────────
def lbl(text):
    st.markdown(f'<span class="me-label">{text}</span>', unsafe_allow_html=True)

def fmt_currency(v, prefix="$", d=2):
    return "N/A" if v is None else f"{prefix}{v:,.{d}f}"

def fmt_large(v, prefix="$"):
    if not v: return "N/A"
    if v>=1e12: return f"{prefix}{v/1e12:.2f}T"
    if v>=1e9:  return f"{prefix}{v/1e9:.2f}B"
    if v>=1e6:  return f"{prefix}{v/1e6:.2f}M"
    return f"{prefix}{v:,.2f}"

def fmt_pct(v, sign=True):
    if v is None: return "N/A"
    s = "+" if sign and v>=0 else ""
    return f"{s}{v:.2f}%"

def sidebar_footer():
    st.sidebar.divider()
    st.sidebar.caption("📡  Yahoo Finance · 5-min cache")

# ── Charts ─────────────────────────────────────────────
def chart_candle(df, ticker, show_ma=True, show_bb=False, height=450):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"],
        low=df["Low"], close=df["Close"], name=ticker,
        increasing=dict(line=dict(color=C_UP,   width=1), fillcolor=C_UP),
        decreasing=dict(line=dict(color=C_DOWN, width=1), fillcolor=C_DOWN),
    ))
    if show_ma and len(df)>=20:
        fig.add_trace(go.Scatter(x=df.index,
            y=df["Close"].rolling(20).mean(), name="MA20", mode="lines",
            line=dict(color=C_WARN, width=1.3, dash="dot")))
    if show_ma and len(df)>=50:
        fig.add_trace(go.Scatter(x=df.index,
            y=df["Close"].rolling(50).mean(), name="MA50", mode="lines",
            line=dict(color=C_ACCENT, width=1.3, dash="dot")))
    if show_bb and len(df)>=20:
        mid  = df["Close"].rolling(20).mean()
        std  = df["Close"].rolling(20).std()
        fig.add_trace(go.Scatter(x=df.index, y=mid+2*std, name="BB Upper",
            mode="lines", line=dict(color="#A78BFA", width=1, dash="dash"), opacity=0.6))
        fig.add_trace(go.Scatter(x=df.index, y=mid-2*std, name="BB Lower",
            mode="lines", line=dict(color="#A78BFA", width=1, dash="dash"),
            fill="tonexty", fillcolor="rgba(167,139,250,0.05)", opacity=0.6))
    fig.update_layout(**CHART_DEFAULTS, height=height,
        margin=dict(l=0,r=0,t=10,b=0),
        xaxis_rangeslider_visible=False,
        xaxis=dict(showgrid=False, tickfont=dict(size=10), linecolor=C_BORDER),
        yaxis=dict(showgrid=True, gridcolor=C_BORDER, gridwidth=0.4,
                   tickfont=dict(size=10), side="right"))
    return fig

def chart_volume(df, height=130):
    colors = [C_UP if c>=o else C_DOWN for c,o in zip(df["Close"],df["Open"])]
    fig = go.Figure(go.Bar(x=df.index, y=df["Volume"],
        marker_color=colors, opacity=0.75, name="Volume"))
    fig.update_layout(**CHART_DEFAULTS, height=height,
        margin=dict(l=0,r=0,t=4,b=0), showlegend=False,
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor=C_BORDER, gridwidth=0.4,
                   tickfont=dict(size=10), side="right"))
    return fig

def chart_area(df, label, height=320):
    is_up    = df["Close"].iloc[-1] >= df["Close"].iloc[0]
    lc       = C_UP if is_up else C_DOWN
    fc       = "rgba(0,200,150,0.07)" if is_up else "rgba(255,69,96,0.07)"
    fig = go.Figure(go.Scatter(x=df.index, y=df["Close"], name=label,
        mode="lines", fill="tozeroy", fillcolor=fc,
        line=dict(color=lc, width=2)))
    fig.update_layout(**CHART_DEFAULTS, height=height,
        margin=dict(l=0,r=0,t=10,b=0), showlegend=False,
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor=C_BORDER, gridwidth=0.4,
                   tickfont=dict(size=10), side="right"))
    return fig

def chart_bar_h(values, colors=None, height=290, x_title=""):
    if colors is None:
        colors = [C_UP if v>=0 else C_DOWN for v in values]
    fig = go.Figure(go.Bar(x=values.values, y=values.index,
        orientation="h", marker_color=colors, marker_line_width=0,
        text=[f"{v:+.2f}%" for v in values], textposition="outside",
        textfont=dict(size=11, color=C_TEXT)))
    fig.update_layout(**CHART_DEFAULTS, height=height,
        margin=dict(l=0,r=72,t=10,b=0), xaxis_title=x_title,
        xaxis=dict(showgrid=True, gridcolor=C_BORDER,
                   zeroline=True, zerolinecolor=C_BORDER2, tickfont=dict(size=10)),
        yaxis=dict(showgrid=False, tickfont=dict(size=11)))
    return fig

def chart_pie(labels, values, height=340):
    fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.55,
        marker=dict(colors=PALETTE, line=dict(color=C_BG, width=2)),
        textinfo="label+percent", textfont=dict(size=11),
        hovertemplate="<b>%{label}</b><br>$%{value:,.2f}<extra></extra>"))
    fig.update_layout(**CHART_DEFAULTS, height=height,
        margin=dict(l=0,r=0,t=10,b=0), showlegend=False)
    return fig

def chart_line_compare(series_dict, height=380):
    fig = go.Figure()
    for i,(name,df) in enumerate(series_dict.items()):
        if df.empty: continue
        norm = ((df["Close"]-df["Close"].iloc[0])/df["Close"].iloc[0])*100
        fig.add_trace(go.Scatter(x=df.index, y=norm, name=name, mode="lines",
            line=dict(color=PALETTE[i%len(PALETTE)], width=2),
            hovertemplate=f"<b>{name}</b>  %{{y:+.2f}}%<extra></extra>"))
    fig.update_layout(**CHART_DEFAULTS, height=height,
        margin=dict(l=0,r=0,t=10,b=0), yaxis_title="% Return",
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor=C_BORDER, gridwidth=0.4,
                   tickfont=dict(size=10), zeroline=True, zerolinecolor=C_BORDER2))
    return fig

def chart_rsi(df, height=160):
    delta  = df["Close"].diff()
    gain   = delta.clip(lower=0).rolling(14).mean()
    loss   = (-delta.clip(upper=0)).rolling(14).mean()
    rs     = gain / loss.replace(0, 1e-10)
    rsi    = 100 - (100 / (1 + rs))
    color  = [C_DOWN if v>=70 else (C_UP if v<=30 else C_ACCENT) for v in rsi]
    fig = go.Figure()
    fig.add_hline(y=70, line_color=C_DOWN, line_dash="dash", line_width=1, opacity=0.5)
    fig.add_hline(y=30, line_color=C_UP,   line_dash="dash", line_width=1, opacity=0.5)
    fig.add_hline(y=50, line_color=C_MUTED, line_dash="dot", line_width=1, opacity=0.4)
    fig.add_trace(go.Scatter(x=df.index, y=rsi, name="RSI(14)", mode="lines",
        line=dict(color=C_ACCENT, width=1.8)))
    fig.update_layout(**CHART_DEFAULTS, height=height,
        margin=dict(l=0,r=0,t=10,b=0),
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=False, range=[0,100], tickfont=dict(size=10),
                   side="right", tickvals=[0,30,50,70,100]))
    return fig
