# 📈 FinPulse — Live Financial Market Dashboard

> A real-time, interactive financial dashboard built entirely in Python.  
> **Moringa School · AIDV-PT10 AI Access Program · Capstone Project**

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?logo=streamlit&logoColor=white)
![yfinance](https://img.shields.io/badge/yfinance-0.2.40+-blue)
![Plotly](https://img.shields.io/badge/Plotly-5.22+-3F4F75?logo=plotly&logoColor=white)

---

## 🌟 What is FinPulse?

FinPulse is a **live, multi-page financial web application** that pulls real-time data
from Yahoo Finance and presents it in an interactive, browser-based dashboard —
built entirely in Python with zero HTML or JavaScript.

It is designed for anyone who wants to:
- Track global stock prices and trends
- Research any stock in the world using its ticker
- Monitor their personal investment portfolio live
- Check cryptocurrency prices and convert currencies

---

## 📺 Features

| Page | What it does |
|------|-------------|
| 🌍 **Market Overview** | Live tiles for Apple, Microsoft, NVIDIA, Tesla + 30-day performance bar chart + interactive 1-year normalised trend comparison |
| 🔍 **Stock Tracker** | Type any stock ticker (e.g. `AAPL`, `TSLA`, `BTC-USD`, `SCOM.NR`) → candlestick chart + volume + key statistics |
| 💼 **My Portfolio** | Enter your own holdings (ticker + shares + buy price) → live gain/loss calculations + allocation pie chart |
| ₿ **Crypto & Forex** | Live Bitcoin, Ethereum, Solana prices + USD→KES live rate + built-in two-way currency converter |

---

## 🏗️ Project Structure

```
finpulse/
├── app.py                      ← Landing page & global config
├── pages/
│   ├── 1_Market_Overview.py    ← Page 1
│   ├── 2_Stock_Tracker.py      ← Page 2
│   ├── 3_My_Portfolio.py       ← Page 3
│   └── 4_Crypto_Forex.py       ← Page 4
├── utils/
│   ├── __init__.py
│   ├── helpers.py              ← Theme, formatters, chart builders
│   ├── data_fetcher.py         ← All yfinance calls + caching + fallback
│   └── portfolio.py            ← Portfolio state & calculations
├── data/
│   └── sample_data.csv         ← Fallback data (365 days × 8 tickers)
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
git clone https://github.com/YOUR_USERNAME/finpulse.git
cd finpulse
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

FinPulse is built to **always work**, even when Yahoo Finance is unavailable:

- **Caching** — all API calls are cached for 5 minutes (`ttl=300`) to reduce request frequency
- **Error handling** — every API call is wrapped in `try-except`
- **Fallback** — if live data fails, the app seamlessly loads from `data/sample_data.csv` and shows a clear warning banner

---

## 🛠️ Common Issues & Fixes

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: No module named 'streamlit'` | Activate venv first, then `pip install -r requirements.txt` |
| Browser doesn't open automatically | Go to `http://localhost:8501` manually |
| Prices showing `$0.00` | Click **🔄 Refresh** in the sidebar |
| `streamlit: command not found` | Make sure venv is activated |
| Forex pair shows "Unavailable" | Try a different pair; not all pairs are supported |

---

## 👤 Author

**Gamaliel**  
Moringa School · AIDV-PT10 · 2025  
*Built with heavy AI assistance (Claude by Anthropic)*
