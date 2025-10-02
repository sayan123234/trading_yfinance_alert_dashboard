"""Module for identifying Fair Value Gaps (FVGs)."""

from typing import List, Dict, Optional


def find_fvgs_in_range(candles: List[Dict], start_idx: int, end_idx: int, fvg_type: str) -> List[Dict]:
    """
    Find all FVGs of a specific type in a given range.
    
    An FVG is identified using 3 consecutive candles:
    - Bullish FVG: first candle's high < third candle's low (must be a real gap)
    - Bearish FVG: first candle's low > third candle's high (must be a real gap)
    
    Args:
        candles: List of candle dictionaries
        start_idx: Starting index of the range (inclusive)
        end_idx: Ending index of the range (inclusive)
        fvg_type: 'bullish' or 'bearish'
        
    Returns:
        List of FVG dictionaries, each containing:
        - type: 'bullish' or 'bearish'
        - top: upper boundary of the gap
        - bottom: lower boundary of the gap
        - start_idx: index of first candle in the 3-candle pattern
        - end_idx: index of third candle in the 3-candle pattern
    """
    fvgs = []
    
    # Ensure we don't go out of bounds
    search_end = min(end_idx, len(candles) - 3)
    
    for i in range(start_idx, search_end + 1):
        if i + 2 >= len(candles):
            break

        if fvg_type == 'bullish':
            first_high = candles[i]['high']
            third_low = candles[i + 2]['low']
            
            # Bullish FVG: gap between first high and third low
            if third_low > first_high:  # must be a real gap
                fvg = {
                    'type': 'bullish',
                    'top': third_low,
                    'bottom': first_high,
                    'start_idx': i,
                    'end_idx': i + 2
                }
                if fvg['top'] > fvg['bottom']:  # safeguard
                    fvgs.append(fvg)

        elif fvg_type == 'bearish':
            first_low = candles[i]['low']
            third_high = candles[i + 2]['high']
            
            # Bearish FVG: gap between third high and first low
            if first_low > third_high:  # must be a real gap
                fvg = {
                    'type': 'bearish',
                    'top': first_low,
                    'bottom': third_high,
                    'start_idx': i,
                    'end_idx': i + 2
                }
                if fvg['top'] > fvg['bottom']:  # safeguard
                    fvgs.append(fvg)
    
    return fvgs


def select_optimal_fvg(fvgs: List[Dict], fvg_type: str) -> Optional[Dict]:
    """
    Select the optimal FVG from a list of FVGs.
    
    For bullish FVGs: selects the TOPMOST (highest bottom value)
    For bearish FVGs: selects the BOTTOMMOST (lowest top value)
    
    Args:
        fvgs: List of FVG dictionaries
        fvg_type: 'bullish' or 'bearish'
        
    Returns:
        The optimal FVG dictionary, or None if list is empty
    """
    if not fvgs:
        return None
    
    if fvg_type == 'bullish':
        return max(fvgs, key=lambda x: x['bottom'])
    else:
        return min(fvgs, key=lambda x: x['top'])
