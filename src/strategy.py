"""Core trading strategy logic."""

from typing import List, Dict, Optional
from swing_point import find_three_swing_points
from fvg import find_fvgs_in_range, select_optimal_fvg


def check_candles_close_above(candles: List[Dict], start_idx: int, end_idx: int, threshold: float) -> bool:
    """
    Check if any candle closes above threshold between indices.
    
    Args:
        candles: List of candle dictionaries
        start_idx: Starting index (inclusive)
        end_idx: Ending index (inclusive)
        threshold: Price threshold to check against
        
    Returns:
        True if any candle closes above threshold, False otherwise
    """
    for i in range(start_idx, end_idx + 1):
        if i >= len(candles):
            break
        if candles[i]['close'] > threshold:
            return True
    return False


def check_candles_close_below(candles: List[Dict], start_idx: int, end_idx: int, threshold: float) -> bool:
    """
    Check if any candle closes below threshold between indices.
    
    Args:
        candles: List of candle dictionaries
        start_idx: Starting index (inclusive)
        end_idx: Ending index (inclusive)
        threshold: Price threshold to check against
        
    Returns:
        True if any candle closes below threshold, False otherwise
    """
    for i in range(start_idx, end_idx + 1):
        if i >= len(candles):
            break
        if candles[i]['close'] < threshold:
            return True
    return False


def analyze_trend(candles: List[Dict], swing_points: List[tuple]) -> Optional[str]:
    """
    Analyzes trend based on 3 swing points.
    
    Uses a lenient approach - if we have the right swing pattern and the most recent
    swing point is higher/lower than the oldest, we consider it a valid trend.
    
    Args:
        candles: List of candle dictionaries
        swing_points: List of 3 swing points [(idx, type, value), ...]
        
    Returns:
        'bullish', 'bearish', or None
    """
    sp1_idx, sp1_type, sp1_value = swing_points[0]  # Most recent
    sp2_idx, sp2_type, sp2_value = swing_points[1]  # Middle
    sp3_idx, sp3_type, sp3_value = swing_points[2]  # Oldest (3rd)
    
    # Case 1: SH -> SL -> SH pattern (bullish potential)
    if sp3_type == 'SH' and sp1_type == 'SH':
        # Primary check: Has price broken above the oldest swing high?
        if check_candles_close_above(candles, sp3_idx, len(candles) - 1, sp3_value):
            return 'bullish'
        # Secondary check: Is the most recent SH higher than the oldest SH?
        # This indicates bullish structure even without a full breakout yet
        elif sp1_value > sp3_value:
            return 'bullish'
        # Check if price has moved below middle swing low, indicating bearish break
        elif check_candles_close_below(candles, sp2_idx, len(candles) - 1, sp2_value):
            return 'bearish'
    
    # Case 2: SL -> SH -> SL pattern (bearish potential)
    elif sp3_type == 'SL' and sp1_type == 'SL':
        # Primary check: Has price broken below the oldest swing low?
        if check_candles_close_below(candles, sp3_idx, len(candles) - 1, sp3_value):
            return 'bearish'
        # Secondary check: Is the most recent SL lower than the oldest SL?
        # This indicates bearish structure even without a full breakdown yet
        elif sp1_value < sp3_value:
            return 'bearish'
        # Check if price has moved above middle swing high, indicating bullish break
        elif check_candles_close_above(candles, sp2_idx, len(candles) - 1, sp2_value):
            return 'bullish'
    
    return None


def check_entry_criteria(candles: List[Dict]) -> Optional[Dict]:
    """
    Main function to check if entry criteria are met according to the technical specification.
    
    CORRECTED: Now only searches for FVGs between the 1st and 2nd swing points as per spec:
    "If a Bullish Fair Value Gap exists between the 1st and 2nd Swing Points"
    
    Args:
        candles: List of candle dictionaries
        
    Returns:
        Dictionary containing entry signal info with keys:
        - trend: 'bullish' or 'bearish'
        - swing_points: list of 3 swing points
        - fvg: Fair Value Gap information
        - target: price target (1st swing point)
        - stop_loss: stop loss level (2nd swing point)
        Returns None if no valid entry signal is found
    """
    # Step 1: Find 3 swing points
    swing_points = find_three_swing_points(candles)
    if not swing_points:
        return None
    
    # Step 2: Analyze trend
    trend = analyze_trend(candles, swing_points)
    if not trend:
        return None
    
    sp1_idx, sp1_type, sp1_value = swing_points[0]  # Most recent
    sp2_idx, sp2_type, sp2_value = swing_points[1]  # Middle
    sp3_idx, sp3_type, sp3_value = swing_points[2]  # Oldest
    
    # Step 3: Check for FVGs ONLY between 1st and 2nd swing points (as per spec)
    
    if trend == 'bullish' and sp3_type == 'SH' and sp1_type == 'SH':
        # Pattern: SH -> SL -> SH (bullish)
        # Per spec: Search for bullish FVGs ONLY between 1st and 2nd swing points
        fvgs = find_fvgs_in_range(candles, sp2_idx, sp1_idx, 'bullish')
        
        if fvgs:
            # Select the TOPMOST bullish FVG (highest bottom value)
            fvg = select_optimal_fvg(fvgs, 'bullish')
            return {
                'trend': trend,
                'swing_points': swing_points,
                'fvg': fvg,
                'target': sp1_value,
                'stop_loss': sp2_value
            }
            
    elif trend == 'bearish' and sp3_type == 'SL' and sp1_type == 'SL':
        # Pattern: SL -> SH -> SL (bearish)
        # Per spec: Search for bearish FVGs ONLY between 1st and 2nd swing points
        fvgs = find_fvgs_in_range(candles, sp2_idx, sp1_idx, 'bearish')
        
        if fvgs:
            # Select the BOTTOMMOST bearish FVG (lowest top value)
            fvg = select_optimal_fvg(fvgs, 'bearish')
            return {
                'trend': trend,
                'swing_points': swing_points,
                'fvg': fvg,
                'target': sp1_value,
                'stop_loss': sp2_value
            }
    
    return None