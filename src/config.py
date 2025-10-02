"""Configuration settings for the trading strategy monitor."""

# List of tickers to monitor
TICKERS = [
    "EURUSD=X",
    "GBPUSD=X",
    "USDJPY=X",
    "AUDUSD=X",
    "USDCAD=X",
    "USDCHF=X",
    "NZDUSD=X",
    "EURGBP=X",
    "EURJPY=X",
    "GBPJPY=X",
    "GC=F",
    "SI=F",
    "^NDX",
    "^GSPC",
    "BTC-USD",
    "ETH-USD",
    "BNB-USD",
    "XRP-USD",
    "ADA-USD",
    "SOL-USD",
    "DOGE-USD",
    "DOT-USD",
    "AVAX-USD"
]

# TESTING ONLY
# TICKERS = ["BNB-USD"]

# Monitoring interval in seconds (300 = 5 minutes)
CHECK_INTERVAL = 300

# Multiple timeframes to monitor simultaneously
# Available: '5m', '15m', '1h', '4h', '1d', '1wk', '1mo'
TIMEFRAMES = [
    # '5m',      # 5 minutes
    # '15m',     # 15 minutes
    # '1h',      # 1 hour
    '4h',      # 4 hours
    '1d',      # Daily
    '1wk',     # Weekly
    '1mo'      # Monthly
]

# Number of candles to fetch for analysis per timeframe
LOOKBACK_PERIODS = {
    '5m': 100,
    '15m': 100,
    '1h': 100,
    '4h': 100,
    '1d': 100,
    '1wk': 100,
    '1mo': 60
}

# Default lookback if not specified
DEFAULT_LOOKBACK = 100

# Maximum number of parallel workers for concurrent processing
MAX_WORKERS = 10

# Cache duration for security names (in seconds)
SECURITY_NAME_CACHE_DURATION = 86400  # 24 hours

