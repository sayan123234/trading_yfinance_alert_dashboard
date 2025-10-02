"""Script to fetch all available tickers from various markets and save to CSV."""

import pandas as pd
import requests
from datetime import datetime
import time


def fetch_nasdaq_tickers():
    """Fetch all NASDAQ listed tickers."""
    print("Fetching NASDAQ tickers...")
    try:
        # NASDAQ trader API
        url = "ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt"
        df = pd.read_csv(url, sep='|')
        df = df[df['Symbol'].str.contains(r'^[A-Z]+$', na=False)]
        df = df[['Symbol', 'Security Name']]
        df['Exchange'] = 'NASDAQ'
        print(f"  Found {len(df)} NASDAQ tickers")
        return df
    except Exception as e:
        print(f"  Error fetching NASDAQ tickers: {e}")
        return pd.DataFrame()


def fetch_nyse_tickers():
    """Fetch all NYSE listed tickers."""
    print("Fetching NYSE tickers...")
    try:
        # NYSE listed from NASDAQ trader
        url = "ftp://ftp.nasdaqtrader.com/symboldirectory/otherlisted.txt"
        df = pd.read_csv(url, sep='|')
        df = df[df['Exchange'] == 'N']  # N = NYSE
        df = df[df['ACT Symbol'].str.contains(r'^[A-Z]+$', na=False)]
        df = df[['ACT Symbol', 'Security Name']]
        df.columns = ['Symbol', 'Security Name']
        df['Exchange'] = 'NYSE'
        print(f"  Found {len(df)} NYSE tickers")
        return df
    except Exception as e:
        print(f"  Error fetching NYSE tickers: {e}")
        return pd.DataFrame()


def fetch_amex_tickers():
    """Fetch all AMEX listed tickers."""
    print("Fetching AMEX tickers...")
    try:
        url = "ftp://ftp.nasdaqtrader.com/symboldirectory/otherlisted.txt"
        df = pd.read_csv(url, sep='|')
        df = df[df['Exchange'] == 'A']  # A = AMEX
        df = df[df['ACT Symbol'].str.contains(r'^[A-Z]+$', na=False)]
        df = df[['ACT Symbol', 'Security Name']]
        df.columns = ['Symbol', 'Security Name']
        df['Exchange'] = 'AMEX'
        print(f"  Found {len(df)} AMEX tickers")
        return df
    except Exception as e:
        print(f"  Error fetching AMEX tickers: {e}")
        return pd.DataFrame()


def fetch_sp500_tickers():
    """Fetch S&P 500 component tickers from Wikipedia."""
    print("Fetching S&P 500 tickers...")
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        tables = pd.read_html(url)
        df = tables[0]
        df = df[['Symbol', 'Security', 'GICS Sector']]
        df.columns = ['Symbol', 'Security Name', 'Sector']
        df['Exchange'] = 'S&P500'
        print(f"  Found {len(df)} S&P 500 tickers")
        return df
    except Exception as e:
        print(f"  Error fetching S&P 500 tickers: {e}")
        return pd.DataFrame()


def fetch_nse_india_tickers():
    """Fetch NSE India tickers."""
    print("Fetching NSE India tickers...")
    try:
        # NSE Equity List
        url = "https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O"
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        # Create session and get cookies
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers)
        time.sleep(1)
        
        response = session.get(url, headers=headers)
        data = response.json()
        
        tickers = []
        if 'data' in data:
            for item in data['data']:
                tickers.append({
                    'Symbol': item['symbol'] + '.NS',
                    'Security Name': item.get('meta', {}).get('companyName', item['symbol']),
                    'Exchange': 'NSE'
                })
        
        df = pd.DataFrame(tickers)
        print(f"  Found {len(df)} NSE tickers")
        return df
    except Exception as e:
        print(f"  Error fetching NSE tickers: {e}")
        return pd.DataFrame()


def fetch_bse_india_tickers():
    """Fetch BSE India tickers (using popular BSE 500 components)."""
    print("Fetching BSE India tickers...")
    try:
        # Alternative: Fetch from a known list or API
        # For now, we'll create a sample structure
        # You may need to find a reliable BSE ticker source
        
        # This is a placeholder - you'll need a proper BSE data source
        df = pd.DataFrame()
        print(f"  BSE ticker fetching not fully implemented")
        return df
    except Exception as e:
        print(f"  Error fetching BSE tickers: {e}")
        return pd.DataFrame()


def fetch_crypto_tickers():
    """Fetch popular cryptocurrency tickers."""
    print("Fetching Crypto tickers...")
    try:
        # Popular cryptocurrencies with their yfinance symbols
        cryptos = [
            ('BTC-USD', 'Bitcoin', 'CRYPTO'),
            ('ETH-USD', 'Ethereum', 'CRYPTO'),
            ('BNB-USD', 'Binance Coin', 'CRYPTO'),
            ('XRP-USD', 'Ripple', 'CRYPTO'),
            ('ADA-USD', 'Cardano', 'CRYPTO'),
            ('SOL-USD', 'Solana', 'CRYPTO'),
            ('DOGE-USD', 'Dogecoin', 'CRYPTO'),
            ('DOT-USD', 'Polkadot', 'CRYPTO'),
            ('MATIC-USD', 'Polygon', 'CRYPTO'),
            ('AVAX-USD', 'Avalanche', 'CRYPTO'),
        ]
        
        df = pd.DataFrame(cryptos, columns=['Symbol', 'Security Name', 'Exchange'])
        print(f"  Found {len(df)} Crypto tickers")
        return df
    except Exception as e:
        print(f"  Error fetching Crypto tickers: {e}")
        return pd.DataFrame()


def fetch_forex_pairs():
    """Fetch popular forex pairs."""
    print("Fetching Forex pairs...")
    try:
        forex_pairs = [
            ('EURUSD=X', 'EUR/USD', 'FOREX'),
            ('GBPUSD=X', 'GBP/USD', 'FOREX'),
            ('USDJPY=X', 'USD/JPY', 'FOREX'),
            ('AUDUSD=X', 'AUD/USD', 'FOREX'),
            ('USDCAD=X', 'USD/CAD', 'FOREX'),
            ('USDCHF=X', 'USD/CHF', 'FOREX'),
            ('NZDUSD=X', 'NZD/USD', 'FOREX'),
            ('EURGBP=X', 'EUR/GBP', 'FOREX'),
            ('EURJPY=X', 'EUR/JPY', 'FOREX'),
            ('GBPJPY=X', 'GBP/JPY', 'FOREX'),
        ]
        
        df = pd.DataFrame(forex_pairs, columns=['Symbol', 'Security Name', 'Exchange'])
        print(f"  Found {len(df)} Forex pairs")
        return df
    except Exception as e:
        print(f"  Error fetching Forex pairs: {e}")
        return pd.DataFrame()


def fetch_all_tickers(markets=None):
    """
    Fetch tickers from multiple markets.
    
    Args:
        markets: List of markets to fetch. If None, fetches all.
                Options: 'nasdaq', 'nyse', 'amex', 'sp500', 'nse', 'bse', 'crypto', 'forex'
    
    Returns:
        pd.DataFrame: Combined DataFrame of all tickers
    """
    if markets is None:
        markets = ['nasdaq', 'nyse', 'amex', 'sp500', 'nse', 'crypto', 'forex']
    
    all_dfs = []
    
    market_functions = {
        'nasdaq': fetch_nasdaq_tickers,
        'nyse': fetch_nyse_tickers,
        'amex': fetch_amex_tickers,
        'sp500': fetch_sp500_tickers,
        'nse': fetch_nse_india_tickers,
        'bse': fetch_bse_india_tickers,
        'crypto': fetch_crypto_tickers,
        'forex': fetch_forex_pairs,
    }
    
    for market in markets:
        if market in market_functions:
            df = market_functions[market]()
            if not df.empty:
                all_dfs.append(df)
            time.sleep(0.5)  # Rate limiting
    
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        
        # Remove duplicates
        combined_df = combined_df.drop_duplicates(subset=['Symbol'])
        
        # Add timestamp
        combined_df['Last Updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return combined_df
    
    return pd.DataFrame()


def get_tickers_list(markets=None):
    """
    Get tickers as a simple list of symbols.

    Args:
        markets: List of markets to include. Available options:
            'nasdaq', 'nyse', 'amex', 'sp500', 'nse', 'bse', 'crypto', 'forex'

    Returns:
        list: List of ticker symbols as strings
    """
    df = fetch_all_tickers(markets)
    if df.empty:
        return []
    return df['Symbol'].tolist()

def save_tickers_to_csv(markets=None, filename=None):
    """
    Main function to fetch and save tickers to CSV.
    
    Args:
        markets: List of markets to include. Available options:
            'nasdaq', 'nyse', 'amex', 'sp500', 'nse', 'bse', 'crypto', 'forex'
        filename: Output filename. If None, generates timestamp-based name
    """
    print("\n" + "="*60)
    print("Ticker Fetcher - Market Data Retrieval")
    print("="*60 + "\n")
    
    # Fetch all tickers
    df = fetch_all_tickers(markets)
    
    if df.empty:
        print("\n❌ No tickers fetched. Please check your connection.")
        return
    
    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'tickers_{timestamp}.csv'
    
    # Save to CSV
    df.to_csv(filename, index=False)
    
    print("\n" + "="*60)
    print(f"✅ Successfully saved {len(df)} tickers to '{filename}'")
    print("="*60)
    
    # Print summary by exchange
    print("\nSummary by Exchange:")
    print("-" * 60)
    exchange_counts = df['Exchange'].value_counts()
    for exchange, count in exchange_counts.items():
        print(f"  {exchange:15s}: {count:5d} tickers")
    print("-" * 60)
    
    return filename

if __name__ == "__main__":
    # Example usage:
    # 1. Fetch specific markets
    save_tickers_to_csv(markets=['forex', 'crypto'])