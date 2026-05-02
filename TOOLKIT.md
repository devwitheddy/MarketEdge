# FinPulse — Getting Started with Python, Pandas & Streamlit for Live Financial Data Analysis
### Moringa School · AIDV-PT10 AI Access Program · Capstone Toolkit

**Author:** Gamaliel  
**Email:** mwanziaedwin5@gmail.com  
**Date:** 2025

---

## 1. Title & Objective

**Title:** FinPulse — A Live Financial Market Dashboard with Python, Pandas & Streamlit

**Technologies Used:**

| Technology | Role |
|-----------|------|
| **Python 3** | Core programming language |
| **Pandas** | All data processing, cleaning, and calculations behind the scenes |
| **Streamlit** | Turns Python scripts into interactive web pages in the browser |
| **yfinance** | Fetches live stock, crypto, and forex data from Yahoo Finance |
| **Plotly** | Interactive charts — candlestick, line, bar, pie |

**Why I chose this:**
My career goal is AI and Data Science. Finance is one of the most data-rich fields in the world, and Python dominates it. This project gave me real hands-on experience with live data APIs, interactive dashboards, and professional code architecture — all skills directly relevant to AI and data careers.

**End Goal:**
Build a fully interactive, 4-page financial web app that fetches real-time data from the internet, displays it with professional charts, tracks a personal investment portfolio with live gain/loss calculations, and converts currencies using live rates. The app runs entirely in the browser from a single `streamlit run app.py` command.

---

## 2. Quick Summary of the Technologies

### Python
Python is a high-level general-purpose programming language, first released in 1991. It is the #1 language in data science, machine learning, and AI due to its readable syntax and enormous library ecosystem.

### Pandas
Pandas is Python's premier data manipulation library. Every piece of data in FinPulse — whether it's a DataFrame of 365 days of stock prices or a table of portfolio holdings — is handled by pandas. It provides the `DataFrame` structure that makes sorting, filtering, grouping, and computing on tabular data trivial.

### Streamlit
Streamlit is a Python library that renders web applications directly from Python scripts. You write Python; Streamlit handles all the HTML, CSS, and JavaScript behind the scenes. Data scientists use it to share dashboards, demos, and ML models without needing frontend development skills. FinPulse is a multi-page Streamlit app using the official `pages/` folder pattern.

### yfinance
yfinance is an open-source library that wraps Yahoo Finance's data API. It provides free access to historical and near-real-time stock prices, cryptocurrency values, forex rates, and company metadata — no API key required. FinPulse uses `yf.Ticker().history()` for OHLCV data and `yf.Ticker().info` for live price and company stats.

### Plotly
Plotly is an interactive charting library. Unlike matplotlib (static images), Plotly charts are zoomable, hoverable, and pannable — and they embed directly in Streamlit pages as live web elements.

### Real-World Example
Bloomberg Terminal — used by professional traders and analysts globally — does essentially what FinPulse does at a beginner level: live market data, interactive charts, and portfolio tracking. FinPulse is the Python developer's minimal recreation of that concept.

---

## 3. System Requirements

| Item | Requirement |
|------|-------------|
| Operating System | Windows 10/11 |
| Python Version | 3.8 or higher |
| Internet Connection | Required for live data fetching |
| Code Editor | VS Code (recommended) |
| Terminal | Command Prompt or PowerShell |
| Disk Space | ~350 MB (Python + packages) |

---

## 4. Installation & Setup

### Step 1 — Verify Python

```bash
python --version
```
Expected output: `Python 3.x.x`

---

### Step 2 — Clone the project

```bash
git clone https://github.com/YOUR_USERNAME/finpulse.git
cd finpulse
```

Or download the ZIP, extract it, then open CMD inside the `finpulse/` folder.

---

### Step 3 — Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

✅ `(venv)` appears in your terminal — you're isolated from global Python packages.

---

### Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

This installs: `streamlit`, `yfinance`, `pandas`, `plotly`

---

### Step 5 — Run the app

```bash
streamlit run app.py
```

Your default browser opens at `http://localhost:8501`.
Navigate the 4 pages using the **sidebar menu**. Press `Ctrl+C` to stop.

---

## 5. Minimal Working Example

### What FinPulse Does

FinPulse is a 4-page live financial dashboard:

**Page 1 — Market Overview:**
Fetches and displays live prices for Apple, Microsoft, Google, Amazon, Tesla, and NVIDIA in styled metric cards. Computes 30-day percentage returns and renders them as a horizontal bar chart (green for gains, red for losses). Provides an interactive multi-select comparison chart showing normalised 1-year returns so stocks of different price levels can be compared fairly.

**Page 2 — Stock Tracker:**
User types any stock ticker (e.g. `AAPL`, `TSLA`, `BTC-USD`, `SCOM.NR` for Safaricom on the Nairobi Stock Exchange) and selects a time period. The app fetches OHLCV history and renders an interactive candlestick chart with optional 20-day and 50-day moving averages, plus a volume bar chart and five key metric tiles (live price, market cap, P/E ratio, 52-week high/low). A collapsible table shows the raw data.

**Page 3 — My Portfolio:**
User enters their own holdings: ticker, number of shares, and the price they paid. The app fetches current live prices and calculates for each position: invested amount, current value, unrealised gain/loss in dollars, and percentage return. A donut pie chart shows portfolio allocation by current value. Add and remove positions at any time.

**Page 4 — Crypto & Forex:**
Live prices for Bitcoin, Ethereum, BNB, Solana, and XRP in metric tiles. A chart that lets the user pick any coin and time period to view its price history as an area chart. Live forex tiles for six currency pairs (USD→KES, EUR→KES, GBP→KES, etc.). A two-way currency converter that uses live exchange rates with hardcoded fallbacks for common pairs.

---

### Core Code Explained

**Fetching live data with 5-minute caching:**
```python
import yfinance as yf
import streamlit as st

@st.cache_data(ttl=300, show_spinner=False)
def fetch_history(ticker: str, period: str = "1y") -> tuple:
    """
    Returns (DataFrame, is_live).
    Falls back to local CSV if Yahoo Finance is unavailable.
    """
    try:
        df = yf.Ticker(ticker).history(period=period)
        if df.empty:
            raise ValueError("Empty response")
        return df[["Open","High","Low","Close","Volume"]], True
    except Exception:
        return load_from_csv(ticker), False   # graceful fallback
```

**Displaying a live metric card:**
```python
info, is_live = fetch_info("AAPL")

st.metric(
    label = "Apple  `AAPL`",
    value = f"${info['price']:,.2f}",
    delta = f"{info['change_pct']:+.2f}%",   # auto green/red
)
```

**Interactive candlestick chart with Plotly:**
```python
import plotly.graph_objects as go

fig = go.Figure(go.Candlestick(
    x     = df.index,
    open  = df["Open"],  high  = df["High"],
    low   = df["Low"],   close = df["Close"],
    increasing = dict(line=dict(color="#2EA043"), fillcolor="#2EA043"),
    decreasing = dict(line=dict(color="#F85149"), fillcolor="#F85149"),
))
st.plotly_chart(fig, use_container_width=True)
```

**Portfolio gain/loss with session state:**
```python
# Persist across reruns
if "portfolio" not in st.session_state:
    st.session_state["portfolio"] = []

# Add position
st.session_state["portfolio"].append({
    "ticker": "AAPL", "quantity": 10, "buy_price": 150.0
})

# Calculate live P&L
for item in st.session_state["portfolio"]:
    info, _   = fetch_info(item["ticker"])
    cur_price = info.get("price") or item["buy_price"]   # safe fallback
    gain_loss = (cur_price - item["buy_price"]) * item["quantity"]
```

**Live forex rate with hardcoded fallback:**
```python
def fetch_forex_rate(from_cur, to_cur):
    FALLBACK = {("USD","KES"): 129.50, ("EUR","KES"): 140.20}
    try:
        rate = yf.Ticker(f"{from_cur}{to_cur}=X").info.get("currentPrice")
        if not rate:
            raise ValueError("No rate")
        return rate, True
    except Exception:
        return FALLBACK.get((from_cur, to_cur), 0.0), False
```

---

### Expected Output

Running `streamlit run app.py` opens a dark-themed web dashboard at `http://localhost:8501` with:
- A branded landing page with navigation cards
- Sidebar with page links, refresh button, and timestamp
- Live price tiles that turn green (up) or red (down)
- Zoomable, hoverable Plotly charts
- A portfolio table with colour-coded return column
- A currency converter that responds immediately to input

---

## 6. AI Prompt Journal

### Prompt 1 — Understanding the Multi-Page App Structure
**Prompt:** *"How do I create a multi-page Streamlit app using the pages/ folder? How does page ordering and naming work?"*

**AI Response Summary:**
The AI explained that Streamlit automatically discovers Python files in a `pages/` folder and adds them to the sidebar navigation. Files are ordered by their numeric prefix (e.g. `1_Market_Overview.py` comes before `2_Stock_Tracker.py`). The underscore acts as a space in the display name.

**Evaluation:** Essential — without this I would have tried building navigation manually. Rated 5/5.

---

### Prompt 2 — Caching yfinance Data in Streamlit
**Prompt:** *"What is the best way to cache yfinance data in Streamlit with a TTL so I don't make too many API calls? Show me with a real example."*

**AI Response Summary:**
The AI introduced `@st.cache_data(ttl=300)` — a decorator that stores function results for 300 seconds. It warned that yfinance is scraping-based and can be rate-limited, so caching is critical for reliability. It also showed how to call `st.cache_data.clear()` manually from a refresh button.

**Evaluation:** Without caching, the app would make a new API call on every user interaction. This single pattern makes the app reliable. Rated 5/5.

---

### Prompt 3 — Error Handling for yfinance Failures
**Prompt:** *"How should I handle yfinance failures gracefully in a Streamlit app so the app doesn't crash when Yahoo Finance is unavailable or rate-limits me?"*

**AI Response Summary:**
The AI recommended wrapping every `yf.Ticker()` call in a `try-except Exception` block, returning a fallback value on failure, and displaying a `st.warning()` banner to tell the user the data source. It also suggested keeping a local CSV as a fallback dataset.

**Evaluation:** This was the most important architectural decision. The fallback CSV means the app always works, even completely offline. Rated 5/5.

---

### Prompt 4 — Persistent Portfolio with Session State
**Prompt:** *"How do I build a persistent portfolio tracker in Streamlit using st.session_state? I want users to add/remove stocks and have them persist across page reruns."*

**AI Response Summary:**
The AI explained that `st.session_state` is Streamlit's built-in key-value store that survives page reruns within the same browser session. It showed the pattern of checking `if "portfolio" not in st.session_state` on first load and appending/removing from the list on user action, followed by `st.rerun()` to refresh the display.

**Evaluation:** Without session state, every button click would wipe the portfolio. This pattern is the backbone of Page 3. Rated 5/5.

---

### Prompt 5 — Building the Candlestick Chart
**Prompt:** *"How do I build a professional interactive candlestick chart in Plotly with green up-candles and red down-candles, 20-day and 50-day moving averages, and dark theme? Display it in Streamlit."*

**AI Response Summary:**
The AI provided the full `go.Candlestick()` code with `increasing` and `decreasing` colour configs, showed how to compute rolling averages with `df["Close"].rolling(20).mean()` and overlay them as `go.Scatter` traces, and demonstrated the `template="plotly_dark"` config for dark mode.

**Evaluation:** This is the most visually impressive feature of the app. The moving averages are genuinely useful for financial analysis. Rated 5/5.

---

### Prompt 6 — Separating Code into Utility Modules
**Prompt:** *"How should I structure a Streamlit project with multiple pages that all share the same data-fetching logic and chart-building functions? I don't want to repeat code in every file."*

**AI Response Summary:**
The AI recommended a `utils/` folder with separate modules: `data_fetcher.py` for all API calls, `helpers.py` for shared formatters and chart builders, and `portfolio.py` for business logic. Each page imports only what it needs. This is the standard pattern used in professional Python projects.

**Evaluation:** This is what separates a school project from a professional codebase. The separation made every page cleaner and easier to debug. Rated 5/5.

---

### Prompt 7 — Consistent Dark Theme Across All Pages
**Prompt:** *"How do I apply a consistent custom dark theme CSS to all pages in a multi-page Streamlit app without repeating the CSS in every file?"*

**AI Response Summary:**
The AI showed that each page calls `st.set_page_config()` independently, so CSS must be injected on each page via `st.markdown(css, unsafe_allow_html=True)`. The solution is to store the CSS string in `helpers.py` as a constant (`GLOBAL_CSS`) and import and inject it at the top of every page file.

**Evaluation:** Keeping the CSS in one place means changing one variable updates the entire app's theme. Rated 5/5.

---

### Prompt 8 — Debugging a TypeError in Portfolio
**Prompt:** *"I'm getting TypeError: unsupported operand type 'NoneType' * float in my portfolio calculator. What does this mean and how do I fix it safely?"*

**AI Response Summary:**
The AI explained that `yf.Ticker().info` sometimes returns `None` for price fields when data is momentarily unavailable, and multiplying `None` by a float raises this error. The fix is the `or` fallback pattern: `cur_price = info.get("price") or item["buy_price"]` — which uses the user's buy price as a safe default.

**Evaluation:** This exact bug appeared during development. The `or` fallback is now applied everywhere a price is fetched. Rated 5/5.

---

## 7. Common Issues & Fixes

| # | Error | Cause | Fix |
|---|-------|-------|-----|
| 1 | `ModuleNotFoundError: No module named 'streamlit'` | venv not active | Activate venv then `pip install -r requirements.txt` |
| 2 | Browser doesn't open | Streamlit browser setting | Go to `http://localhost:8501` manually |
| 3 | Price tiles show `$0.00` | Yahoo Finance temporarily unavailable | Click **🔄 Refresh** in sidebar; app uses fallback data |
| 4 | `TypeError: NoneType * float` | yfinance returned None for price | Use `info.get("price") or fallback` pattern |
| 5 | `streamlit: command not found` | venv not activated | Run `venv\Scripts\activate` first |
| 6 | Forex pair shows "Unavailable" | Pair not supported by Yahoo Finance | Try USD→KES, EUR→KES instead |
| 7 | App is slow on first load | No cached data yet | Normal — second load is fast |
| 8 | `KeyError: 'Close'` | Empty DataFrame from yfinance | Always check `if not df.empty:` before accessing columns |
| 9 | Portfolio disappears on refresh | Session state reset | This is expected — session state persists per browser session |
| 10 | `ModuleNotFoundError: No module named 'utils'` | Running script from wrong folder | Always `cd finpulse` first, then `streamlit run app.py` |

---

## 8. References

| Resource | Link |
|---------|------|
| Streamlit Official Docs | https://docs.streamlit.io |
| Streamlit Multi-Page Apps | https://docs.streamlit.io/library/get-started/multipage-apps |
| Streamlit Session State | https://docs.streamlit.io/library/api-reference/session-state |
| yfinance GitHub | https://github.com/ranaroussi/yfinance |
| Plotly Python Charts | https://plotly.com/python/ |
| Plotly Candlestick | https://plotly.com/python/candlestick-charts/ |
| pandas Documentation | https://pandas.pydata.org/docs/ |
| Python Official Docs | https://docs.python.org/3/ |
| Yahoo Finance | https://finance.yahoo.com |

---

*This toolkit was created as part of the Moringa School AIDV-PT10 AI Access Program Capstone.*  
*Built with heavy AI assistance — Claude (Anthropic) was used for code architecture, all utility functions, debugging support, and documentation drafting. This project is an honest demonstration of how AI can accelerate a beginner's learning.*
