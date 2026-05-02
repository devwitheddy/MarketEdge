# 💹 MarketEdge — Live Financial Market Dashboard

> **A real-time financial data analysis dashboard built entirely in Python.**  
> Pulls live market data from the internet, analyzes it, and presents it through  
> an interactive, browser-based web application — with no HTML or JavaScript required.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?logo=streamlit&logoColor=white)
![yfinance](https://img.shields.io/badge/yfinance-0.2.40+-1D6FA4)
![Plotly](https://img.shields.io/badge/Plotly-5.22+-3F4F75?logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2+-150458?logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Overview

MarketEdge is a **live financial data analysis application** that fetches real-world market data directly from Yahoo Finance and transforms it into meaningful insights through interactive charts, tables, and metrics — all running in your browser.

The core goal of this project is **data analysis applied to real financial markets**:

- Loading and processing live data using **Pandas**
- Computing statistics such as returns, volatility, drawdowns, and Sharpe ratios
- Visualizing trends, distributions, and comparisons using **Plotly**
- Presenting everything in a clean, interactive dashboard using **Streamlit**

Unlike a static data analysis script, MarketEdge works with **live data from the internet** — meaning every number, chart, and insight you see reflects what is actually happening in the market right now. It covers stocks, cryptocurrencies, forex exchange rates, and financial news — all in one place.

---

## 🌟 Key Features at a Glance

| Feature | Description |
|---------|-------------|
| 📡 Live Data | Pulls real-time prices from Yahoo Finance — no manual CSV uploads needed |
| 📊 Interactive Charts | Zoomable, hoverable Plotly charts — candlestick, area, bar, pie, histogram |
| 🧮 Data Analysis | Returns, volatility, drawdowns, Sharpe ratio, P/E ratios, market cap comparisons |
| 💼 Portfolio Tracker | Add your own stocks and see live gain/loss calculated instantly |
| ₿ Crypto & Forex | Live cryptocurrency prices and currency converter including USD → KES |
| 📰 Market News | Live financial headlines from Reuters, Yahoo Finance, MarketWatch and CNBC |
| 🛡️ Fallback System | If live data fails, app loads from a local sample dataset automatically |
| ⚡ Smart Caching | All API calls cached for 5 minutes to keep the app fast and reliable |

---

## 🗂️ Application Pages

### 💹 1. Market Overview
The landing dashboard for global stock market data.

**What it shows:**
- Live prices for Apple, Microsoft, Google, Amazon, Tesla and NVIDIA — updated every 5 minutes
- **30-Day Performance Bar Chart** — see which stocks gained or lost the most this month
- **Market Cap Comparison** — visualise the size difference between companies
- **P/E Ratio Chart** — compare how expensive each stock is relative to earnings
- **Average Daily Volume Chart** — see how actively each stock is being traded
- **1-Year Normalised Trend Comparison** — compare stocks at different price levels fairly (shown as % return from the start of the period, not raw price)
- **Key Statistics Table** — price, change, market cap, P/E, 52-week high/low and volume in one place

---

### 🔍 2. Stock Tracker
Deep-dive analysis tool for any stock, index, crypto or commodity.

**What it shows:**
- **Dropdown** with 30+ popular stocks grouped by sector, plus a manual ticker input for any symbol worldwide
- **Candlestick Chart** — open, high, low, close for every trading day in the selected period
- **Area Chart** — alternative view showing price trend with colour-coded fill (green = up, red = down)
- **Moving Averages** — MA20 and MA50 overlay on the price chart to identify trends
- **Bollinger Bands** — upper and lower bands showing price volatility range
- **RSI Indicator** — Relative Strength Index (14-day) to identify overbought (>70) and oversold (<30) conditions
- **Trading Volume Chart** — daily volume bars coloured to match price direction
- **Closing Price Distribution** — histogram showing the frequency of different price levels
- **Period Statistics** — high, low, return, average volume and daily volatility for the selected period
- **Company Information** — sector, country, currency, exchange, employee count, website and business description
- **Raw OHLCV Data Table** — the actual numbers behind every chart, sortable and scrollable

**Supported ticker formats:**
- US Stocks: `AAPL`, `TSLA`, `NVDA`, `META`
- Indices: `^GSPC` (S&P 500), `^IXIC` (NASDAQ), `^DJI` (Dow Jones)
- Crypto: `BTC-USD`, `ETH-USD`, `SOL-USD`
- Commodities: `GC=F` (Gold), `CL=F` (Crude Oil), `SI=F` (Silver)
- Forex: `EURUSD=X`, `GBPUSD=X`

---

### 💼 3. My Portfolio
Personal investment tracker with live data.

**What it does:**
- Add stocks to your portfolio using the dropdown or by typing any ticker
- Enter how many shares you own and the price you paid per share
- The app fetches the current live price and calculates for each position:
  - Amount invested vs current value
  - Unrealised gain or loss (in dollars and as a percentage)
- **Summary KPI Cards** — total invested, current value, total gain/loss and number of positions
- **Portfolio Allocation Pie Chart** — see how your money is distributed across holdings
- **Holdings Breakdown Legend** — colour-coded list of every position with return percentage
- **6-Month Trend Overlay** — all your holdings normalised on one chart to compare performance
- **Risk Metrics Table** — daily volatility, annual volatility, maximum drawdown and Sharpe ratio for each holding
- Add and remove positions at any time during the session

> ⚠️ Portfolio data is stored in session memory — it resets when the app is closed. This is by design for privacy.

---

### ₿ 4. Crypto & Forex
Live cryptocurrency market data and currency exchange rates.

**What it shows:**
- **Live Crypto Prices** — Bitcoin, Ethereum, BNB, Solana and XRP with 24-hour change
- **Crypto Price Chart** — area chart for any coin across 1 month, 3 months, 6 months or 1 year
- **24-Hour Performance Bar** — side-by-side comparison of daily gains/losses across all coins
- **Crypto Statistics Table** — price, 24H change, market cap, 52-week high/low
- **Live Forex Rates** — USD→KES, EUR→KES, GBP→KES, USD→EUR, USD→GBP, USD→NGN
- **Currency Converter** — convert between any combination of: USD, KES, EUR, GBP, NGN, BTC, ETH, BNB, SOL, XRP
  - Uses live exchange rates when available
  - Falls back to recent hardcoded rates if Yahoo Finance is temporarily unavailable
  - Shows the reverse rate automatically (e.g. if you convert USD→KES it also shows KES→USD)

---

### 📰 5. Market News
Live financial news aggregated from multiple sources.

**What it shows:**
- Latest financial headlines fetched from RSS feeds (Yahoo Finance, Reuters, MarketWatch, CNBC)
- Organised into **6 category tabs**: All Markets · Stocks · Crypto · Forex/Macro · Finance · Energy
- Each article displays:
  - Headline title
  - Publisher name and logo
  - Time since publication (e.g. "2h ago")
  - Exact publication date
  - Thumbnail image when available
  - **Direct link** to the full article at the original publisher's website
- Adjustable article count (10, 20 or 30 per tab)
- Fully deduplicated — the same story never appears twice

> All articles open directly at their original source. MarketEdge does not host or store any news content.

---

## 🏗️ Project Structure

```
marketedge/
│
├── app.py                       ← Landing page, global config, market snapshot
│
├── pages/
│   ├── 1_Market_Overview.py     ← Live prices, performance charts, statistics table
│   ├── 2_Stock_Tracker.py       ← Deep-dive analysis for any stock or asset
│   ├── 3_My_Portfolio.py        ← Personal portfolio tracker with risk metrics
│   ├── 4_Crypto_Forex.py        ← Crypto prices and currency converter
│   └── 5_Market_News.py         ← Live news from financial RSS feeds
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py               ← Design system: colours, CSS, chart builders, formatters
│   ├── data_fetcher.py          ← All data fetching: yfinance, RSS, forex, caching, fallback
│   └── portfolio.py             ← Portfolio state management and P&L calculations
│
├── data/
│   └── sample_data.csv          ← Local fallback dataset (365 days × 8 tickers)
│
├── requirements.txt             ← Python dependencies
└── README.md                    ← This file
```

**Why this structure?**  
Each concern is separated into its own module. `helpers.py` owns all visual decisions. `data_fetcher.py` owns all external API calls. `portfolio.py` owns all financial calculations. Each page imports only what it needs. This makes the code easy to read, debug and extend.

---

## 🔧 Technologies Used

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.8+ | Core programming language |
| **Pandas** | 2.2+ | Data loading, cleaning, grouping, statistical calculations |
| **Streamlit** | 1.35+ | Multi-page web application framework — runs in the browser |
| **yfinance** | 0.2.40+ | Live stock, crypto and forex data from Yahoo Finance |
| **Plotly** | 5.22+ | Interactive, zoomable charts rendered in the browser |
| **urllib** | Built-in | Fetching RSS news feeds — no extra library needed |
| **xml.etree** | Built-in | Parsing RSS XML responses |

---

## ⚙️ Setup & Installation

### Requirements
- Python 3.8 or higher installed on your system
- An internet connection (required for live data)
- Compatible with Windows 10/11, macOS and Linux

---

### Step 1 — Clone or download the project

**Using Git:**
```bash
git clone https://github.com/YOUR_USERNAME/marketedge.git
cd marketedge
```

**Or** download the ZIP file, extract it, and open a terminal inside the `marketedge/` folder.

---

### Step 2 — Create a virtual environment

A virtual environment keeps the project's libraries separate from your system Python — this is best practice.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

You will see `(venv)` appear at the start of your terminal line — this confirms the environment is active.

---

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt --timeout 300
```

This installs: `streamlit`, `yfinance`, `pandas` and `plotly`.

> If the download times out (slow connection), re-run the same command — pip will resume from where it left off.

---

### Step 4 — Run the app

```bash
streamlit run app.py
```

Your default browser will open automatically at `http://localhost:8501`.  
Use the sidebar to navigate between pages.  
Press `Ctrl + C` in the terminal to stop the app.

---

## 🛡️ Reliability & Error Handling

MarketEdge is designed to **always work**, even when internet access is limited or Yahoo Finance is temporarily unavailable.

**Caching:** All API calls are cached for 5 minutes using `@st.cache_data(ttl=300)`. This means the app won't make a new network request every time you click something — it reuses the last fetched result, keeping the app fast.

**Fallback data:** If a live data fetch fails for any reason (rate limit, network issue, unsupported ticker), the app automatically loads data from `data/sample_data.csv` — a local dataset covering 365 days of price history for 8 tickers — and displays a clear warning banner so you always know which data source is being used.

**Forex fallback:** If live exchange rates are unavailable, the converter falls back to a table of recent hardcoded rates for all supported currency pairs. A 📁 icon next to a rate means it is from the fallback table rather than live.

**News fallback:** The news page uses RSS feeds (not just yfinance) as its primary source, meaning news loads reliably even when yfinance's news endpoint is unavailable.

---

## 🛠️ Common Issues & Fixes

| Issue | Likely Cause | Fix |
|-------|-------------|-----|
| `ModuleNotFoundError: No module named 'streamlit'` | Virtual environment not active | Run `venv\Scripts\activate` first, then `pip install -r requirements.txt` |
| Browser doesn't open automatically | Streamlit browser setting | Manually go to `http://localhost:8501` |
| Prices showing `$0.00` | Yahoo Finance temporarily unavailable | Click **🔄 Refresh** in the sidebar |
| `streamlit: command not found` | venv not activated | Run `venv\Scripts\activate` before `streamlit run app.py` |
| Stock shows "No data found" | Ticker not supported on Yahoo Finance | Try a different symbol — some regional tickers have limited coverage |
| Forex rate shows N/A | Currency pair not supported | App falls back to hardcoded rates automatically for common pairs |
| News tab shows no articles | RSS feed temporarily slow | Click **🔄 Refresh News** in the sidebar |
| `pip install` times out | Slow internet connection | Re-run with `--timeout 300` flag |
| Warnings during `git add` | Windows line-ending conversion | These are harmless — run `git config core.autocrlf true` to silence them |

---

## 📈 Data Analysis Capabilities

MarketEdge achieves its core data analysis goal through the following computations, all performed live on fetched data using Pandas:

- **Returns** — percentage price change over any selected period
- **Moving Averages** — 20-day and 50-day rolling mean of closing prices
- **Bollinger Bands** — 20-day rolling mean ± 2 standard deviations
- **RSI (Relative Strength Index)** — 14-day momentum oscillator
- **Daily Volatility** — standard deviation of daily percentage returns
- **Annual Volatility** — daily volatility scaled by √252 (trading days per year)
- **Maximum Drawdown** — largest peak-to-trough decline in the selected period
- **Sharpe Ratio** — risk-adjusted return (annualised mean return ÷ annualised volatility)
- **Market Cap Comparison** — absolute size of companies in USD
- **P/E Ratio Comparison** — relative valuation across companies
- **Volume Analysis** — average daily trading volume over 30-day windows
- **Portfolio P&L** — unrealised gain/loss per position and total portfolio

---

## 📦 Dependencies

```
streamlit>=1.35.0,<2.0.0
yfinance>=0.2.40,<1.0.0
pandas>=2.2.0,<3.0.0
plotly>=5.22.0,<6.0.0
```

All other libraries used (`urllib`, `xml.etree`, `datetime`, `os`, `sys`) are part of Python's standard library and require no installation.

---

## 👤 Author

**Mwanzia M. Edwin**  
GitHub: [github.com/YOUR_USERNAME](https://github.com/YOUR_USERNAME)
