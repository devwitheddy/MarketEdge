"""
utils/portfolio.py
────────────────────────────────────────────────────────
Portfolio data management and calculation logic.
All state is stored in st.session_state["portfolio"].
────────────────────────────────────────────────────────
"""

import streamlit as st
import pandas as pd
from utils.data_fetcher import fetch_info


# ══════════════════════════════════════════════════════
# SESSION STATE INIT
# ══════════════════════════════════════════════════════

def init_portfolio():
    """Call once at the top of the Portfolio page."""
    if "portfolio" not in st.session_state:
        st.session_state["portfolio"] = []


def get_portfolio() -> list:
    return st.session_state.get("portfolio", [])


def add_position(ticker: str, quantity: float, buy_price: float) -> tuple[bool, str]:
    """
    Validate and add a new position.
    Returns (success, message).
    """
    ticker = ticker.upper().strip()
    if not ticker:
        return False, "Ticker symbol cannot be empty."
    if quantity <= 0:
        return False, "Number of shares must be greater than zero."
    if buy_price <= 0:
        return False, "Buy price must be greater than zero."

    # Validate ticker against live/sample data
    info, _ = fetch_info(ticker)
    if not info or info.get("price", 0) == 0:
        return False, f"'{ticker}' doesn't look like a valid ticker. Check and try again."

    # Check for duplicate
    for item in st.session_state["portfolio"]:
        if item["ticker"] == ticker:
            return False, f"'{ticker}' is already in your portfolio. Remove it first to re-add."

    st.session_state["portfolio"].append({
        "ticker":    ticker,
        "quantity":  quantity,
        "buy_price": buy_price,
        "name":      info.get("name", ticker),
    })
    return True, f"Added {quantity} share(s) of {ticker} at ${buy_price:,.2f} each."


def remove_position(ticker: str):
    """Remove a position by ticker."""
    st.session_state["portfolio"] = [
        p for p in st.session_state["portfolio"]
        if p["ticker"] != ticker
    ]


def clear_portfolio():
    """Remove all positions."""
    st.session_state["portfolio"] = []


# ══════════════════════════════════════════════════════
# CALCULATIONS
# ══════════════════════════════════════════════════════

def calculate_portfolio() -> tuple[pd.DataFrame, dict]:
    """
    Fetch live prices for every position and compute P&L.

    Returns
    -------
    (rows_df, totals)
        rows_df  : DataFrame with one row per position
        totals   : dict with portfolio-level aggregates
    """
    portfolio = get_portfolio()
    if not portfolio:
        return pd.DataFrame(), {}

    rows           = []
    total_invested = 0.0
    total_value    = 0.0

    for item in portfolio:
        info, is_live = fetch_info(item["ticker"])
        cur_price     = info.get("price") or item["buy_price"]

        invested   = item["buy_price"] * item["quantity"]
        value      = cur_price         * item["quantity"]
        gain_loss  = value - invested
        gl_pct     = (gain_loss / invested * 100) if invested else 0.0

        total_invested += invested
        total_value    += value

        rows.append({
            "Ticker":          item["ticker"],
            "Name":            item.get("name", item["ticker"]),
            "Shares":          item["quantity"],
            "Buy Price":       item["buy_price"],
            "Current Price":   round(cur_price, 2),
            "Invested ($)":    round(invested, 2),
            "Value ($)":       round(value, 2),
            "Gain / Loss ($)": round(gain_loss, 2),
            "Return (%)":      round(gl_pct, 2),
            "Live":            "✅" if is_live else "⚠️",
        })

    total_gl     = total_value - total_invested
    total_gl_pct = (total_gl / total_invested * 100) if total_invested else 0.0

    totals = {
        "invested":   total_invested,
        "value":      total_value,
        "gain_loss":  total_gl,
        "gl_pct":     total_gl_pct,
        "positions":  len(portfolio),
    }
    return pd.DataFrame(rows), totals
