# Multi-Timeframe Trading Strategy Monitor

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

A real-time trading strategy monitor that identifies entry signals based on swing points and Fair Value Gaps (FVG) across multiple timeframes simultaneously. Built with Python and yfinance for automated market analysis.

## 📋 Table of Contents

- [Features](#-features)
- [Strategy Overview](#-strategy-overview)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Disclaimer](#-disclaimer)

## ✨ Features

- 🔄 **Multi-Timeframe Analysis**: Simultaneously monitors 7 timeframes (5m, 15m, 1h, 4h, Daily, Weekly, Monthly)
- ⚡ **Parallel Processing**: Uses ThreadPoolExecutor for fast concurrent scanning
- 🎯 **Smart Signal Detection**: Identifies swing points and Fair Value Gaps automatically
- 📊 **Real-Time Monitoring**: Continuous scanning at configurable intervals
- 🌐 **Multi-Asset Support**: Works with stocks, crypto, forex, and indices
- 📈 **Risk Management**: Automatic target and stop-loss calculation
- 🎨 **Clear Output**: Formatted signal display with all relevant trade parameters
- ⚙️ **Highly Configurable**: Easy customization of tickers, timeframes, and parameters

## 📖 Strategy Overview

This monitor implements a swing trading strategy based on:

1. **Swing Point Identification**: Detects swing highs and lows in price action
2. **Trend Analysis**: Determines bullish/bearish trend using 3 alternating swing points
3. **Fair Value Gap (FVG) Detection**: Identifies price imbalances between swing points
4. **Entry Signal Generation**: Combines all criteria to generate high-probability trade setups

### Entry Criteria

**Bullish Setup:**
- 3 swing points identified (alternating SH/SL/SH or SL/SH/SL)
- Bullish trend confirmed (price breaking above key levels)
- Bullish FVG found between 1st and 2nd swing points

**Bearish Setup:**
- 3 swing points identified (alternating SH/SL/SH or SL/SH/SL)
- Bearish trend confirmed (price breaking below key levels)
- Bearish FVG found between 1st and 2nd swing points

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/trading-strategy-monitor.git
cd trading-strategy-monitor
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install yfinance pandas
```

## ⚡ Quick Start

1. **Configure your settings** in `config.py`:
```python
TICKERS = ["AAPL", "MSFT", "GOOGL", "TSLA", "SPY"]
TIMEFRAMES = ['5m', '15m', '1h', '4h', '1d', '1wk', '1mo']
CHECK_INTERVAL = 300  # 5 minutes
```

2. **Run the monitor**:
```bash
python monitor.py
```

3. **Watch for signals**:
```
============================================================
🎯 ENTRY SIGNAL DETECTED: AAPL [1 Hour]
============================================================
Timeframe: 1 Hour
Trend: BULLISH
Time: 2025-10-01 14:30:00

Swing Points:
  1st (Recent): SH at 175.50
  2nd (Middle): SL at 172.30
  3rd (Oldest): SH at 174.20
...
```

## ⚙️ Configuration

### `config.py` Settings

#### 1. Tickers to Monitor
```python
TICKERS = [
    "AAPL",      # Apple Inc.
    "MSFT",      # Microsoft
    "GOOGL",     # Alphabet
    "TSLA",      # Tesla
    "SPY",       # S&P 500 ETF
    "BTC-USD",   # Bitcoin
    "EURUSD=X"   # EUR/USD Forex
]
```

#### 2. Timeframes
```python
TIMEFRAMES = [
    '5m',      # 5 minutes
    '15m',     # 15 minutes
    '1h',      # 1 hour
    '4h',      # 4 hours
    '1d',      # Daily
    '1wk',     # Weekly
    '1mo'      # Monthly
]
```

**Remove timeframes you don't need** to reduce scan time and API calls.

#### 3. Check Interval
```python
CHECK_INTERVAL = 300  # seconds (5 minutes)
```

Recommended intervals:
- **Day Trading**: 60-300 seconds (1-5 minutes)
- **Swing Trading**: 300-900 seconds (5-15 minutes)
- **Position Trading**: 1800-3600 seconds (30-60 minutes)

#### 4. Lookback Periods
```python
LOOKBACK_PERIODS = {
    '5m': 100,
    '15m': 100,
    '1h': 100,
    '4h': 100,
    '1d': 100,
    '1wk': 100,
    '1mo': 60
}
```

Adjust based on:
- More periods = Better pattern detection, slower scans
- Fewer periods = Faster scans, might miss patterns

## 📘 Usage

### Continuous Monitoring Mode

Run the monitor continuously:
```bash
python monitor.py
```

Stop with `Ctrl+C`

### Single Scan Test Mode

Edit `monitor.py` (line 165):
```python
if __name__ == "__main__":
    test_single_scan()  # Run once
```

Then:
```bash
python monitor.py
```

### Using Ticker Fetcher

Generate a comprehensive list of available tickers:

```bash
python ticker_fetcher.py
```

This creates a CSV file with tickers from:
- NASDAQ
- NYSE
- AMEX
- S&P 500
- NSE India
- Cryptocurrencies
- Forex pairs

Customize markets to fetch:
```python
save_tickers_to_csv(markets=['nasdaq', 'crypto', 'forex'])
```

## 📁 Project Structure

```
trading-strategy-monitor/
│
├── config.py              # Configuration settings
├── monitor.py             # Main monitoring script
├── data_fetcher.py        # Market data retrieval
├── strategy.py            # Trading strategy logic
├── swing_point.py         # Swing point identification
├── fvg.py                 # Fair Value Gap detection
├── ticker_fetcher.py      # Ticker list generator
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 How It Works

### 1. Data Fetching (`data_fetcher.py`)
- Fetches OHLCV data from yfinance
- Supports all major timeframes
- Aggregates 1h data into 4h candles
- Handles errors gracefully

### 2. Swing Point Detection (`swing_point.py`)
```python
def identify_swing_high(candles, index):
    # Swing High: Middle candle high > both neighbors
    return middle_high > prev_high and middle_high > next_high

def identify_swing_low(candles, index):
    # Swing Low: Middle candle low < both neighbors
    return middle_low < prev_low and middle_low < next_low
```

### 3. Fair Value Gap Detection (`fvg.py`)
```python
# Bullish FVG: Gap between candle 1 high and candle 3 low
if first_high < third_low:
    return {'type': 'bullish', 'top': third_low, 'bottom': first_high}

# Bearish FVG: Gap between candle 1 low and candle 3 high
if first_low > third_high:
    return {'type': 'bearish', 'top': first_low, 'bottom': third_high}
```

### 4. Trend Analysis (`strategy.py`)
- Finds 3 alternating swing points
- Checks if price breaks key levels
- Confirms bullish/bearish bias

### 5. Signal Generation
- Combines all criteria
- Calculates target (1st swing point)
- Calculates stop loss (2nd swing point)
- Returns complete trade setup

### 6. Parallel Monitoring (`monitor.py`)
- Uses ThreadPoolExecutor
- Scans all ticker-timeframe combinations concurrently
- Displays results in real-time

## 📊 Examples

### Example 1: Bullish Signal on AAPL (1 Hour)

```
============================================================
🎯 ENTRY SIGNAL DETECTED: AAPL [1 Hour]
============================================================
Timeframe: 1 Hour
Trend: BULLISH
Time: 2025-10-01 14:30:00

Swing Points:
  1st (Recent): SH at 175.50
  2nd (Middle): SL at 172.30
  3rd (Oldest): SH at 174.20

Fair Value Gap (BULLISH):
  Top: 173.80
  Bottom: 172.90

Trade Parameters:
  🎯 Target: 175.50
  🛑 Stop Loss: 172.30
  📊 Risk Range: 3.20
============================================================
```

**Interpretation:**
- Enter long when price enters the FVG (172.90-173.80)
- Target: 175.50 (recent swing high)
- Stop Loss: 172.30 (middle swing low)
- Risk: $3.20 per share

### Example 2: Multi-Timeframe Confirmation

```
[2025-10-01 15:00:00] Checking all tickers across all timeframes...
------------------------------------------------------------
  AAPL [5m]: No signal
  AAPL [15m]: No signal
🎯 AAPL [1h]: BULLISH SIGNAL (details above)
🎯 AAPL [4h]: BULLISH SIGNAL (details above)
  AAPL [1d]: No signal
  AAPL [1wk]: No signal
  AAPL [1mo]: No signal
------------------------------------------------------------
Scan complete: 35/35 checks
Signals found: 2
```

**Interpretation:**
- Signals on both 1h and 4h timeframes
- Higher confluence = Higher probability trade
- Consider entering with larger position size

## 🐛 Troubleshooting

### Problem: "No data available"

**Solutions:**
- Check internet connection
- Verify ticker symbol is correct
- Try a different timeframe
- Some assets may not have data for shorter timeframes

### Problem: Slow scans

**Solutions:**
- Reduce number of tickers in `config.py`
- Remove unnecessary timeframes
- Increase `max_workers` in `monitor.py` (line 107):
```python
with ThreadPoolExecutor(max_workers=20) as executor:
```
- Increase `CHECK_INTERVAL` to scan less frequently

### Problem: Too many API calls / Rate limiting

**Solutions:**
- Increase `CHECK_INTERVAL` (e.g., 600 seconds = 10 minutes)
- Monitor fewer tickers
- Remove high-frequency timeframes (5m, 15m)
- Add delays between scans

### Problem: No signals detected

**Solutions:**
- Increase `LOOKBACK_PERIODS` for more historical data
- Check if market is volatile enough (ranging markets produce fewer signals)
- Verify strategy logic matches your expectations
- Test with known volatile assets first (e.g., TSLA, BTC-USD)

### Problem: FutureWarning about 'H' frequency

**Solution:**
Already fixed in the latest version. If you still see it, update line 54 in `data_fetcher.py`:
```python
df = df.resample('4h').agg({  # lowercase 'h'
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contributions

- [ ] Add email/SMS notifications
- [ ] Create web dashboard with Flask/Django
- [ ] Implement backtesting module
- [ ] Add more technical indicators
- [ ] Database logging for historical signals
- [ ] Machine learning signal filtering
- [ ] Position sizing calculator
- [ ] Multi-broker integration
- [ ] Docker containerization
- [ ] Unit tests and CI/CD

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**IMPORTANT:** This software is for educational and research purposes only.

- This is NOT financial advice
- Past performance does not guarantee future results
- Trading involves substantial risk of loss
- Always do your own research
- Never trade with money you cannot afford to lose
- The authors are not responsible for any financial losses
- Test thoroughly with paper trading before using real money

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/trading-strategy-monitor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/trading-strategy-monitor/discussions)
- **Email**: your.email@example.com

## 🙏 Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) for market data
- Trading community for strategy insights
- All contributors to this project

## 📈 Roadmap

- [x] Multi-timeframe support
- [x] Parallel processing
- [x] FVG detection
- [ ] Backtesting module
- [ ] Web dashboard
- [ ] Alert notifications
- [ ] Database integration
- [ ] Risk management calculator
- [ ] Portfolio tracking
- [ ] Performance analytics

---

**Star ⭐ this repository if you find it helpful!**

Made with ❤️ by traders, for traders.