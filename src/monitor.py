"""Main monitoring script for multiple timeframes with grouped alerts."""

import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
from typing import Dict, List, Tuple, Optional
import config
from data_fetcher import fetch_candles
from strategy import check_entry_criteria
import yfinance as yf


# Cache for security names to avoid repeated API calls
_security_name_cache = {}


def get_security_name(ticker: str) -> str:
    if ticker in _security_name_cache:
        return _security_name_cache[ticker]
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        name = info.get('longName') or info.get('shortName') or ticker
        _security_name_cache[ticker] = name
        return name
    except Exception:
        _security_name_cache[ticker] = ticker
        return ticker


def format_signal(ticker: str, timeframe: str, signal: Dict) -> str:
    trend = signal['trend'].upper()
    sp1_idx, sp1_type, sp1_value = signal['swing_points'][0]
    sp2_idx, sp2_type, sp2_value = signal['swing_points'][1]
    sp3_idx, sp3_type, sp3_value = signal['swing_points'][2]
    
    fvg = signal['fvg']
    
    tf_names = {
        '5m': '5 Minutes',
        '15m': '15 Minutes',
        '1h': '1 Hour',
        '4h': '4 Hours',
        '1d': 'Daily',
        '1wk': 'Weekly',
        '1mo': 'Monthly'
    }
    
    output = f"  📊 Timeframe: {tf_names.get(timeframe, timeframe)}\n"
    output += f"  Trend: {trend}\n"
    output += f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    output += f"  Swing Points:\n"
    output += f"    1st (Recent): {sp1_type} at {sp1_value}\n"
    output += f"    2nd (Middle): {sp2_type} at {sp2_value}\n"
    output += f"    3rd (Oldest): {sp3_type} at {sp3_value}\n\n"
    
    output += f"  Fair Value Gap ({fvg['type'].upper()}):\n"
    output += f"    Top: {fvg['top']}\n"
    output += f"    Bottom: {fvg['bottom']}\n\n"
    
    output += f"  Trade Parameters:\n"
    output += f"    🎯 Target: {signal['target']}\n"
    output += f"    🛑 Stop Loss: {signal['stop_loss']}\n"
    
    if trend == 'BULLISH':
        risk = abs(signal['target'] - signal['stop_loss'])
    else:
        risk = abs(signal['stop_loss'] - signal['target'])
    
    output += f"    📊 Risk Range: {risk}\n"
    
    return output


def format_grouped_signals(grouped_signals: Dict[str, List[Tuple[str, Dict]]]) -> str:
    if not grouped_signals:
        return ""
    
    timeframe_priority = {
        '1mo': 0,
        '1wk': 1,
        '1d': 2,
        '4h': 3,
        '1h': 4,
        '15m': 5,
        '5m': 6
    }
    
    output = f"\n{'='*70}\n"
    output += f"🎯 ENTRY SIGNALS DETECTED\n"
    output += f"{'='*70}\n\n"
    
    sorted_tickers = sorted(grouped_signals.keys(), 
                           key=lambda t: (-len(grouped_signals[t]), t))
    
    for ticker in sorted_tickers:
        security_name = get_security_name(ticker)
        
        signals = sorted(grouped_signals[ticker], 
                        key=lambda x: timeframe_priority.get(x[0], 999))
        
        if security_name != ticker:
            header_text = f"{ticker} - {security_name}"
        else:
            header_text = ticker
            
        if len(header_text) > 64:
            header_text = header_text[:61] + "..."
        
        output += f"┏{'━'*68}┓\n"
        output += f"┃ 📈 {header_text:<64} ┃\n"
        output += f"┃ {len(signals)} Signal(s) Found{'':<48} ┃\n"
        output += f"┗{'━'*68}┛\n\n"
        
        for i, (timeframe, signal) in enumerate(signals, 1):
            output += f"  Signal #{i}:\n"
            output += format_signal(ticker, timeframe, signal)
            if i < len(signals):
                output += f"  {'-'*66}\n"
        
        output += f"\n{'='*70}\n\n"
    
    return output


def check_ticker_timeframe(ticker: str, timeframe: str) -> Tuple[str, str, Optional[Dict], Optional[str]]:
    try:
        periods = config.LOOKBACK_PERIODS.get(timeframe, config.DEFAULT_LOOKBACK)
        candles = fetch_candles(ticker, timeframe, periods)
        
        if not candles:
            return (ticker, timeframe, None, "No data available")
        
        signal = check_entry_criteria(candles)
        return (ticker, timeframe, signal, None)
    
    except Exception as e:
        return (ticker, timeframe, None, str(e))


def monitor_tickers():
    print(f"\n{'='*70}")
    print(f"Multi-Timeframe Swing Point & FVG Monitor (Grouped by Ticker)")
    print(f"{'='*70}")
    print(f"Monitoring tickers: {', '.join(config.TICKERS)}")
    print(f"Timeframes: {', '.join(config.TIMEFRAMES)}")
    print(f"Check interval: {config.CHECK_INTERVAL} seconds")
    print(f"\nPress Ctrl+C to stop\n")
    
    try:
        while True:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n[{timestamp}] Checking all tickers across all timeframes...")
            print(f"{'-'*70}")
            
            grouped_signals = defaultdict(list)
            errors = []
            checks_completed = 0
            total_checks = len(config.TICKERS) * len(config.TIMEFRAMES)
            
            with ThreadPoolExecutor(max_workers=config.MAX_WORKERS) as executor:
                futures = {}
                for ticker in config.TICKERS:
                    for timeframe in config.TIMEFRAMES:
                        future = executor.submit(check_ticker_timeframe, ticker, timeframe)
                        futures[future] = (ticker, timeframe)
                
                for future in as_completed(futures):
                    try:
                        ticker, timeframe, signal, error = future.result()
                        checks_completed += 1
                        
                        if signal:
                            grouped_signals[ticker].append((timeframe, signal))
                        elif error:
                            errors.append((ticker, timeframe, error))
                    except Exception as e:
                        checks_completed += 1
                        ticker, timeframe = futures[future]
                        errors.append((ticker, timeframe, f"Task failed: {str(e)}"))
            
            if grouped_signals:
                print(format_grouped_signals(grouped_signals))
            
            if errors:
                print(f"\n⚠️  Errors encountered:")
                for ticker, timeframe, error in errors:
                    print(f"  {ticker} [{timeframe}]: {error}")
            
            print(f"\n{'-'*70}")
            print(f"Scan complete: {checks_completed}/{total_checks} checks")
            print(f"Tickers with signals: {len(grouped_signals)}")
            print(f"Total signals found: {sum(len(signals) for signals in grouped_signals.values())}")
            print(f"Next check in {config.CHECK_INTERVAL} seconds...")
            
            time.sleep(config.CHECK_INTERVAL)
    
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("Monitoring stopped by user")
        print("="*70)


def test_single_scan():
    print(f"\n{'='*70}")
    print(f"Running Single Scan Test (Grouped by Ticker)")
    print(f"{'='*70}\n")
    
    grouped_signals = defaultdict(list)
    errors = []
    
    with ThreadPoolExecutor(max_workers=config.MAX_WORKERS) as executor:
        futures = {}
        for ticker in config.TICKERS:
            for timeframe in config.TIMEFRAMES:
                future = executor.submit(check_ticker_timeframe, ticker, timeframe)
                futures[future] = (ticker, timeframe)
        
        for future in as_completed(futures):
            try:
                ticker, timeframe, signal, error = future.result()
                
                if signal:
                    grouped_signals[ticker].append((timeframe, signal))
                elif error:
                    errors.append((ticker, timeframe, error))
            except Exception as e:
                ticker, timeframe = futures[future]
                errors.append((ticker, timeframe, f"Task failed: {str(e)}"))
    
    if grouped_signals:
        print(format_grouped_signals(grouped_signals))
    
    if errors:
        print(f"\n⚠️  Errors encountered:")
        for ticker, timeframe, error in errors:
            print(f"  {ticker} [{timeframe}]: {error}")
    
    print(f"\n{'='*70}")
    print(f"Test complete.")
    print(f"Tickers with signals: {len(grouped_signals)}")
    print(f"Total signals found: {sum(len(signals) for signals in grouped_signals.values())}")
    print(f"{'='*70}")


if __name__ == "__main__":
    monitor_tickers()
    # Or run a single test scan:
    # test_single_scan()
