"""Module for identifying swing points in price data."""

from typing import List, Dict, Optional, Tuple


def identify_swing_high(candles: List[Dict], index: int) -> bool:
    """
    Identifies if the candle at given index is a swing high.
    
    A swing high occurs when the middle candle's high is greater than
    both the previous and next candle's high.
    
    Args:
        candles: List of candle dictionaries with 'high', 'low', 'close'
        index: Index of the middle candle to check
        
    Returns:
        True if swing high is identified, False otherwise
    """
    if index < 1 or index >= len(candles) - 1:
        return False
    
    middle_high = candles[index]['high']
    prev_high = candles[index - 1]['high']
    next_high = candles[index + 1]['high']
    
    return middle_high > prev_high and middle_high > next_high


def identify_swing_low(candles: List[Dict], index: int) -> bool:
    """
    Identifies if the candle at given index is a swing low.
    
    A swing low occurs when the middle candle's low is less than
    both the previous and next candle's low.
    
    Args:
        candles: List of candle dictionaries with 'high', 'low', 'close'
        index: Index of the middle candle to check
        
    Returns:
        True if swing low is identified, False otherwise
    """
    if index < 1 or index >= len(candles) - 1:
        return False
    
    middle_low = candles[index]['low']
    prev_low = candles[index - 1]['low']
    next_low = candles[index + 1]['low']
    
    return middle_low < prev_low and middle_low < next_low


def find_three_swing_points(candles: List[Dict]) -> Optional[List[Tuple[int, str, float]]]:
    """
    Finds 3 alternating swing points moving backwards from most recent closed candle.
    
    Searches backward from the second-to-last candle (most recent closed) to find
    3 swing points that alternate between highs and lows (e.g., SH->SL->SH or SL->SH->SL).
    
    Args:
        candles: List of candle dictionaries (oldest to newest)
        
    Returns:
        List of tuples [(index, type, value), ...] where:
        - index: position in candles array
        - type: 'SH' for Swing High or 'SL' for Swing Low
        - value: the high/low price value
        Returns None if 3 alternating swing points cannot be found
    """
    swing_points = []
    last_type = None
    
    # Start from second-to-last candle (most recent closed candle)
    # Go backwards to find swing points
    for i in range(len(candles) - 2, 0, -1):
        if len(swing_points) >= 3:
            break
            
        if identify_swing_high(candles, i):
            if last_type != 'SH':  # Ensure alternating
                swing_points.append((i, 'SH', candles[i]['high']))
                last_type = 'SH'
        elif identify_swing_low(candles, i):
            if last_type != 'SL':  # Ensure alternating
                swing_points.append((i, 'SL', candles[i]['low']))
                last_type = 'SL'
    
    if len(swing_points) == 3:
        return swing_points
    return None