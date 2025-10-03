import streamlit as st
import pandas as pd
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import config
from monitor import check_ticker_timeframe
import yfinance as yf
from streamlit_autorefresh import st_autorefresh


st.set_page_config(page_title="Trading Monitor", layout="wide")

# Auto-refresh every CHECK_INTERVAL seconds
st_autorefresh(interval=config.CHECK_INTERVAL * 1000, key="refresh")

st.title("📊 Trading Entry Scanner")

# Sidebar controls
st.sidebar.header("Settings")
tickers = st.sidebar.multiselect("Select Tickers", config.TICKERS, default=config.TICKERS[:5])
timeframes = st.sidebar.multiselect("Select Timeframes", config.TIMEFRAMES, default=config.TIMEFRAMES)

def get_security_name(ticker: str) -> str:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return info.get("longName") or info.get("shortName") or ticker
    except Exception:
        return ticker

def run_scan(tickers, timeframes):
    grouped_signals = defaultdict(list)
    errors = []

    with ThreadPoolExecutor(max_workers=config.MAX_WORKERS) as executor:
        futures = {
            executor.submit(check_ticker_timeframe, ticker, timeframe): (ticker, timeframe)
            for ticker in tickers for timeframe in timeframes
        }
        for future in as_completed(futures):
            ticker, timeframe = futures[future]
            try:
                ticker, timeframe, signal, error = future.result()
                if signal:
                    grouped_signals[ticker].append((timeframe, signal))
                elif error:
                    errors.append((ticker, timeframe, error))
            except Exception as e:
                errors.append((ticker, timeframe, str(e)))
    return grouped_signals, errors


# Run scan automatically every refresh
grouped_signals, errors = run_scan(tickers, timeframes)

# 🕒 Show last updated time
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (refreshes every {config.CHECK_INTERVAL // 60} min)")

# Display results
st.subheader("✅ Signals Found")
if grouped_signals:
    for ticker, signals in grouped_signals.items():
        with st.expander(f"{ticker} - {get_security_name(ticker)} ({len(signals)} signal(s))"):
            for timeframe, signal in signals:
                trend = signal["trend"].upper()
                fvg = signal["fvg"]

                df = pd.DataFrame({
                    "Swing Point": ["1st (Recent)", "2nd (Middle)", "3rd (Oldest)"],
                    "Type": [sp[1] for sp in signal["swing_points"]],
                    "Value": ["{:.5f}".format(sp[2]) for sp in signal["swing_points"]],
                })

                st.markdown(f"**Timeframe:** {timeframe} | **Trend:** {trend}")
                st.dataframe(df, hide_index=True, width='stretch')

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🎯 Target", "{:.5f}".format(signal["target"]))
                with col2:
                    st.metric("🛑 Stop Loss", "{:.5f}".format(signal["stop_loss"]))
                with col3:
                    st.metric("Risk Range", "{:.5f}".format(abs(signal["target"] - signal["stop_loss"])))

                st.markdown(
                    f"**Fair Value Gap ({fvg['type'].upper()}):** Top: {fvg['top']:.5f}, Bottom: {fvg['bottom']:.5f}"
                )
else:
    st.info("No signals detected.")

# Display errors if any
if errors:
    st.subheader("⚠️ Errors")
    for ticker, timeframe, error in errors:
        st.error(f"{ticker} [{timeframe}]: {error}")
