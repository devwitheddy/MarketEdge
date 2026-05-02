"""utils/data_fetcher.py — MarketEdge"""

import os, time
from datetime import datetime
import pandas as pd
import streamlit as st
import yfinance as yf

_SAMPLE_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "sample_data.csv")

# ── NSE / regional ticker aliases ─────────────────────
# Some regional tickers need remapping for yfinance
TICKER_ALIASES = {
    "SCOM.NR":   "SCOM.NR",   # Safaricom — may or may not work; we handle gracefully
    "SAFCOM.NR": "SCOM.NR",
}

# ── Fallback rates ─────────────────────────────────────
_FB: dict = {
    ("USD","KES"):129.50, ("USD","EUR"):0.923, ("USD","GBP"):0.787,
    ("USD","NGN"):1540.0, ("USD","ZAR"):18.7,  ("USD","JPY"):154.2,
    ("EUR","KES"):140.20, ("EUR","USD"):1.084, ("EUR","GBP"):0.853,
    ("GBP","KES"):164.80, ("GBP","USD"):1.270, ("GBP","EUR"):1.172,
    ("KES","USD"):1/129.50, ("KES","EUR"):1/140.20, ("KES","GBP"):1/164.80,
    ("BTC","USD"):67000., ("ETH","USD"):3500., ("BNB","USD"):580.,
    ("SOL","USD"):175.,   ("XRP","USD"):0.52,
    ("BTC","KES"):67000.*129.50, ("ETH","KES"):3500.*129.50,
    ("BNB","KES"):580.*129.50,   ("SOL","KES"):175.*129.50,
    ("XRP","KES"):0.52*129.50,
    ("BTC","EUR"):67000.*0.923,  ("ETH","EUR"):3500.*0.923,
    ("BTC","GBP"):67000.*0.787,  ("ETH","GBP"):3500.*0.787,
}

_CRYPTO_TICKERS = {
    "BTC":"BTC-USD","ETH":"ETH-USD","BNB":"BNB-USD",
    "SOL":"SOL-USD","XRP":"XRP-USD",
}

# Popular stocks for dropdown
POPULAR_STOCKS: dict = {
    "── US Technology ──":         "",
    "Apple (AAPL)":                "AAPL",
    "Microsoft (MSFT)":            "MSFT",
    "Google (GOOGL)":              "GOOGL",
    "Amazon (AMZN)":               "AMZN",
    "Tesla (TSLA)":                "TSLA",
    "NVIDIA (NVDA)":               "NVDA",
    "Meta (META)":                 "META",
    "Netflix (NFLX)":              "NFLX",
    "AMD (AMD)":                   "AMD",
    "Intel (INTC)":                "INTC",
    "── US Finance ──":            "",
    "JPMorgan Chase (JPM)":        "JPM",
    "Goldman Sachs (GS)":          "GS",
    "Visa (V)":                    "V",
    "Mastercard (MA)":             "MA",
    "Bank of America (BAC)":       "BAC",
    "── US Consumer ──":           "",
    "Coca-Cola (KO)":              "KO",
    "McDonald's (MCD)":            "MCD",
    "Nike (NKE)":                  "NKE",
    "Walt Disney (DIS)":           "DIS",
    "── Healthcare ──":            "",
    "Johnson & Johnson (JNJ)":     "JNJ",
    "Pfizer (PFE)":                "PFE",
    "── Indices ──":               "",
    "S&P 500 (^GSPC)":             "^GSPC",
    "NASDAQ 100 (^IXIC)":          "^IXIC",
    "Dow Jones (^DJI)":            "^DJI",
    "── Africa / Emerging ──":     "",
    "Safaricom NSE (SCOM.NR)":     "SCOM.NR",
    "── Crypto ──":                "",
    "Bitcoin (BTC-USD)":           "BTC-USD",
    "Ethereum (ETH-USD)":          "ETH-USD",
    "Solana (SOL-USD)":            "SOL-USD",
    "── Commodities ──":           "",
    "Gold (GC=F)":                 "GC=F",
    "Crude Oil (CL=F)":            "CL=F",
    "Silver (SI=F)":               "SI=F",
}

# ── Internal helpers ───────────────────────────────────
def _load_sample(ticker):
    try:
        df  = pd.read_csv(_SAMPLE_CSV, parse_dates=["Date"])
        sub = df[df["Ticker"]==ticker].copy().set_index("Date").sort_index()
        sub.index = pd.DatetimeIndex(sub.index)
        return sub[["Open","High","Low","Close","Volume"]]
    except Exception:
        return pd.DataFrame()

def _sample_info(ticker):
    df = _load_sample(ticker)
    if df.empty: return {}
    last = df.iloc[-1]; prev = df.iloc[-2] if len(df)>1 else last
    chg  = ((last["Close"]-prev["Close"])/prev["Close"])*100
    return {"name":ticker,"price":round(last["Close"],2),
            "change_pct":round(chg,2),"market_cap":0,"pe_ratio":None,
            "high_52w":round(df["High"].max(),2),"low_52w":round(df["Low"].min(),2),
            "volume":int(last["Volume"]),"currency":"USD","sector":"N/A","country":"N/A",
            "description":""}

def _raw_price(info_dict):
    return (info_dict.get("currentPrice")
            or info_dict.get("regularMarketPrice")
            or info_dict.get("previousClose")
            or info_dict.get("regularMarketPreviousClose")
            or 0)

def _fiat_direct(fc, tc):
    try:
        raw  = yf.Ticker(f"{fc}{tc}=X").info
        rate = _raw_price(raw)
        return float(rate) if rate else 0.0
    except Exception:
        return 0.0

def _crypto_usd(symbol):
    tkr = _CRYPTO_TICKERS.get(symbol, f"{symbol}-USD")
    try:
        raw   = yf.Ticker(tkr).info
        price = _raw_price(raw)
        return float(price) if price else 0.0
    except Exception:
        return 0.0

# ── Public API ─────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def fetch_history(ticker: str, period: str = "1y"):
    """Returns (DataFrame, is_live)."""
    try:
        df = yf.Ticker(ticker).history(period=period)
        if df.empty:
            raise ValueError("empty")
        df.index = pd.DatetimeIndex(df.index.date)
        return df[["Open","High","Low","Close","Volume"]], True
    except Exception:
        return _load_sample(ticker), False


@st.cache_data(ttl=60, show_spinner=False)
def fetch_info(ticker: str):
    """Returns (info_dict, is_live)."""
    try:
        raw   = yf.Ticker(ticker).info
        price = _raw_price(raw)
        if not price:
            raise ValueError("no price")
        return {
            "name":        raw.get("longName") or raw.get("shortName", ticker),
            "price":       round(float(price), 4),
            "change_pct":  round(float(raw.get("regularMarketChangePercent") or 0), 4),
            "market_cap":  raw.get("marketCap") or 0,
            "pe_ratio":    raw.get("trailingPE"),
            "high_52w":    raw.get("fiftyTwoWeekHigh") or 0,
            "low_52w":     raw.get("fiftyTwoWeekLow")  or 0,
            "volume":      raw.get("regularMarketVolume") or 0,
            "currency":    raw.get("currency", "USD"),
            "sector":      raw.get("sector", "—"),
            "country":     raw.get("country", "—"),
            "description": raw.get("longBusinessSummary", ""),
            "exchange":    raw.get("exchange", ""),
            "employees":   raw.get("fullTimeEmployees"),
            "website":     raw.get("website", ""),
        }, True
    except Exception:
        return _sample_info(ticker), False


@st.cache_data(ttl=60, show_spinner=False)
def fetch_forex_rate(fc: str, tc: str):
    """Returns (rate, is_live). Handles crypto chaining correctly."""
    if fc == tc:
        return 1.0, True

    # Crypto origin
    if fc in _CRYPTO_TICKERS:
        usd_price = _crypto_usd(fc)
        if usd_price:
            if tc == "USD":
                return round(usd_price, 4), True
            usd_to_tc = _fiat_direct("USD", tc)
            if not usd_to_tc:
                usd_to_tc = _FB.get(("USD", tc), 0.0)
            if usd_to_tc:
                return round(usd_price * usd_to_tc, 4), True
        fb = _FB.get((fc, tc), 0.0)
        return (fb, False) if fb else (0.0, False)

    # Fiat → fiat
    rate = _fiat_direct(fc, tc)
    if rate:
        return round(rate, 6), True
    fb = _FB.get((fc, tc), 0.0)
    if fb:
        return round(fb, 6), False
    rev = _FB.get((tc, fc), 0.0)
    if rev:
        return round(1/rev, 6), False
    return 0.0, False


@st.cache_data(ttl=180, show_spinner=False)
def fetch_news(tickers: list, max_per_ticker: int = 8):
    """
    Fetch financial news from yfinance .news property.
    Returns a deduplicated list of news dicts sorted by date (newest first).
    Each dict: {title, link, publisher, published, thumbnail}
    """
    seen   = set()
    result = []
    for tkr in tickers:
        try:
            articles = yf.Ticker(tkr).news or []
            for a in articles[:max_per_ticker]:
                link = a.get("link","")
                if not link or link in seen:
                    continue
                seen.add(link)

                # Handle both old and new yfinance news schemas
                title  = (a.get("title") or
                          a.get("content",{}).get("title","No title"))
                pub    = (a.get("publisher") or
                          a.get("content",{}).get("provider",{}).get("displayName",""))
                ts     = (a.get("providerPublishTime") or
                          a.get("content",{}).get("pubDate"))
                thumb  = ""
                if a.get("thumbnail"):
                    resolutions = a["thumbnail"].get("resolutions",[])
                    if resolutions:
                        thumb = resolutions[0].get("url","")

                try:
                    if isinstance(ts, int):
                        pub_dt = datetime.utcfromtimestamp(ts)
                    elif isinstance(ts, str):
                        pub_dt = datetime.fromisoformat(ts.replace("Z","+00:00"))
                    else:
                        pub_dt = datetime.utcnow()
                except Exception:
                    pub_dt = datetime.utcnow()

                result.append({
                    "title":     title,
                    "link":      link,
                    "publisher": pub or "Financial News",
                    "published": pub_dt,
                    "thumbnail": thumb,
                    "ticker":    tkr,
                })
        except Exception:
            continue

    result.sort(key=lambda x: x["published"], reverse=True)
    return result


def data_source_banner(is_live: bool):
    if is_live:
        st.success("📡  Live data — Yahoo Finance")
    else:
        st.warning("⚠️  Live data unavailable — showing sample data. "
                   "Click **Refresh** in the sidebar to retry.")
