# 💹 MarketEdge — Live Financial Market Dashboard

> A real-time, interactive financial dashboard built entirely in Python.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?logo=streamlit&logoColor=white)
![yfinance](https://img.shields.io/badge/yfinance-0.2.40+-blue)
![Plotly](https://img.shields.io/badge/Plotly-5.22+-3F4F75?logo=plotly&logoColor=white)

---

## 🌟 What is MarketEdge?

MarketEdge is a **live, multi-page financial web application** that pulls real-time data
from Yahoo Finance and presents it in an interactive, browser-based dashboard —
built entirely in Python with zero HTML or JavaScript required.

---

## 📺 Pages & Features

| Page | What it does |
|------|-------------|
| 💹 **Market Overview** | Live prices for Apple, Microsoft, NVIDIA, Tesla + 30-day performance · market cap comparison · P/E ratio chart · volume chart · 1-year trend comparison · key statistics table |
| 🔍 **Stock Tracker** | Search any ticker (e.g. `AAPL`, `TSLA`, `BTC-USD`, `GC=F`) from a dropdown or type manually · Candlestick or Area chart · MA20/50 · Bollinger Bands · RSI indicator · price distribution · company info |
| 💼 **My Portfolio** | Add stocks via dropdown or ticker · live gain/loss calculations · allocation pie chart · 6-month trend overlay · risk metrics (volatility, max drawdown, Sharpe ratio) |
| ₿ **Crypto & Forex** | Live Bitcoin, Ethereum, BNB, Solana, XRP prices · USD→KES live rate · multi-pair currency converter supporting crypto pairs |
| 📰 **Market News** | Latest financial headlines across 6 category tabs · direct links to original publisher · thumbnail images · time-ago display |

---

## 🏗️ Project Structure

```
marketedge/
├── app.py                      ← Landing page & global config
├── pages/
│   ├── 1_Market_Overview.py
│   ├── 2_Stock_Tracker.py
│   ├── 3_My_Portfolio.py
│   ├── 4_Crypto_Forex.py
│   └── 5_Market_News.py
├── utils/
│   ├── __init__.py
│   ├── helpers.py              ← Theme, formatters, chart builders
│   ├── data_fetcher.py         ← All yfinance calls + caching + fallback
│   └── portfolio.py            ← Portfolio state & calculations
├── data/
│   └── sample_data.csv         ← Fallback data when live data unavailable
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### Requirements
- Python 3.8 or higher
- Internet connection (for live data)
- Windows 10/11 · macOS · Linux

### Step 1 — Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/marketedge.git
cd marketedge
```

### Step 2 — Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the app
```bash
streamlit run app.py
```

Your browser opens at `http://localhost:8501` automatically. ✅

---

## 🛡️ Reliability

MarketEdge is built to **always work**, even when Yahoo Finance is unavailable:

- **Caching** — all API calls cached for 5 minutes (`ttl=300`)
- **Error handling** — every API call wrapped in `try-except`
- **Fallback** — if live data fails, app loads from `data/sample_data.csv` with a clear warning banner

---

## 🛠️ Common Issues & Fixes

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: No module named 'streamlit'` | Activate venv first, then `pip install -r requirements.txt` |
| Browser doesn't open | Go to `http://localhost:8501` manually |
| Prices showing `$0.00` | Click **🔄 Refresh** in the sidebar |
| `streamlit: command not found` | Make sure venv is activated |
| Regional stock shows no data | Some NSE/regional tickers have limited Yahoo Finance coverage |
| Forex pair unavailable | App falls back to hardcoded rates automatically |

---

## 📦 Dependencies

```
streamlit>=1.35.0
yfinance>=0.2.40
pandas>=2.2.0
plotly>=5.22.0
```
