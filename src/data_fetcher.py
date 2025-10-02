"""Module for fetching market data."""

from typing import Optional, List, Dict
import yfinance as yf


def fetch_candles(ticker: str, timeframe: str = '1h', periods: int = 100) -> Optional[List[Dict]]:
    """
    Fetches candle data for a ticker.
    
    Args:
        ticker: Ticker symbol
        timeframe: Timeframe (e.g., '5m', '15m', '1h', '4h', '1d', '1wk', '1mo')
        periods: Number of periods to fetch
        
    Returns:
        List of candle dictionaries with keys: timestamp, open, high, low, close, volume
        Returns None if data cannot be fetched
    """
    try:
        # Map timeframe to yfinance interval
        interval_map = {
            '5m': '5m',
            '15m': '15m',
            '1h': '1h',
            '4h': '1h',  # yfinance doesn't have 4h, we'll aggregate 1h
            '1d': '1d',
            '1wk': '1wk',
            '1mo': '1mo'
        }
        
        interval = interval_map.get(timeframe, '1h')
        
        # Determine period based on timeframe
        period_map = {
            '5m': '7d',
            '15m': '1mo',
            '1h': '2mo',
            '4h': '6mo',
            '1d': '1y',
            '1wk': '2y',
            '1mo': '5y'
        }
        
        period = period_map.get(timeframe, '1mo')
        
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        
        if df.empty:
            return None
        
        # Handle 4h aggregation from 1h data
        if timeframe == '4h':
            df = df.resample('4h').agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            }).dropna()
        
        # Convert to list of dictionaries
        candles = []
        for idx, row in df.iterrows():
            candles.append({
                'timestamp': idx,
                'open': row['Open'],
                'high': row['High'],
                'low': row['Low'],
                'close': row['Close'],
                'volume': row['Volume']
            })
        
        return candles[-periods:] if len(candles) > periods else candles
    
    except Exception as e:
        print(f"Error fetching data for {ticker} ({timeframe}): {e}")
        return None