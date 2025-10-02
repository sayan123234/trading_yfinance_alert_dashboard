"""
Test verification script to validate the fixed codebase.
Run this after replacing the files to ensure everything works correctly.
"""

from typing import List, Dict
from typing import List, Dict, Optional
from swing_point import find_three_swing_points, identify_swing_high, identify_swing_low
from fvg import find_fvgs_in_range, select_optimal_fvg
from strategy import check_entry_criteria, analyze_trend


def create_test_candles() -> List[Dict]:
    """Create test candle data for verification."""
    # Create a bullish pattern: SH -> SL -> SH with bullish FVG
    candles = [
        {'open': 100, 'high': 105, 'low': 95, 'close': 102, 'volume': 1000},   # 0
        {'open': 102, 'high': 110, 'low': 100, 'close': 108, 'volume': 1000},  # 1 - will be SH (oldest)
        {'open': 108, 'high': 109, 'low': 103, 'close': 105, 'volume': 1000},  # 2
        {'open': 105, 'high': 106, 'low': 98, 'close': 100, 'volume': 1000},   # 3 - will be SL (middle)
        {'open': 100, 'high': 101, 'low': 99, 'close': 100, 'volume': 1000},   # 4
        {'open': 100, 'high': 107, 'low': 102, 'close': 105, 'volume': 1000},  # 5 - FVG candidate (high=107)
        {'open': 105, 'high': 108, 'low': 104, 'close': 106, 'volume': 1000},  # 6 - middle of FVG
        {'open': 106, 'high': 115, 'low': 111, 'close': 113, 'volume': 1000},  # 7 - FVG candidate (low=111)
        {'open': 113, 'high': 120, 'low': 112, 'close': 118, 'volume': 1000},  # 8 - will be SH (recent)
        {'open': 118, 'high': 119, 'low': 115, 'close': 117, 'volume': 1000},  # 9 - most recent (checking from 8)
    ]
    return candles


def test_swing_point_identification():
    """Test swing point identification."""
    print("\n" + "="*70)
    print("TEST 1: Swing Point Identification")
    print("="*70)
    
    candles = create_test_candles()
    
    # Test individual swing points
    print("\nChecking individual candles for swing points:")
    for i in range(len(candles)):
        is_sh = identify_swing_high(candles, i)
        is_sl = identify_swing_low(candles, i)
        if is_sh or is_sl:
            sp_type = "SH" if is_sh else "SL"
            value = candles[i]['high'] if is_sh else candles[i]['low']
            print(f"  Index {i}: {sp_type} at {value}")
    
    # Test finding 3 swing points
    swing_points = find_three_swing_points(candles)
    print(f"\nFound 3 swing points: {swing_points is not None}")
    
    if swing_points:
        print("Swing points (recent to oldest):")
        for i, (idx, sp_type, value) in enumerate(swing_points, 1):
            print(f"  {i}. Index {idx}: {sp_type} at {value}")
        
        # Verify pattern
        sp1_type = swing_points[0][1]
        sp3_type = swing_points[2][1]
        if sp1_type == sp3_type:
            print(f"✅ Valid pattern: {sp3_type} -> {swing_points[1][1]} -> {sp1_type}")
        else:
            print(f"❌ Invalid pattern")
    else:
        print("❌ Failed to find 3 swing points")
    
    return swing_points


def test_fvg_identification(swing_points):
    """Test FVG identification."""
    print("\n" + "="*70)
    print("TEST 2: FVG Identification")
    print("="*70)
    
    candles = create_test_candles()
    
    if not swing_points:
        print("❌ Cannot test FVGs without swing points")
        return None
    
    sp1_idx = swing_points[0][0]  # Recent swing
    sp2_idx = swing_points[1][0]  # Middle swing
    sp3_idx = swing_points[2][0]  # Oldest swing
    
    print(f"\nSearching for FVGs between SP2 (idx {sp2_idx}) and SP1 (idx {sp1_idx}):")
    
    # Search for bullish FVGs in the correct range
    fvgs = find_fvgs_in_range(candles, sp2_idx, sp1_idx, 'bullish')
    
    print(f"Found {len(fvgs)} bullish FVG(s)")
    
    for i, fvg in enumerate(fvgs, 1):
        print(f"\n  FVG #{i}:")
        print(f"    Type: {fvg['type']}")
        print(f"    Top: {fvg['top']}")
        print(f"    Bottom: {fvg['bottom']}")
        print(f"    Indices: {fvg['start_idx']} to {fvg['end_idx']}")
        
        # Verify it's within the correct range
        if sp2_idx <= fvg['start_idx'] <= sp1_idx:
            print(f"    ✅ FVG is within SP2→SP1 range")
        else:
            print(f"    ❌ FVG is OUTSIDE SP2→SP1 range!")
    
    # Test FVG selection
    if fvgs:
        optimal_fvg = select_optimal_fvg(fvgs, 'bullish')
        if optimal_fvg:
            print(f"\n✅ Optimal bullish FVG selected: bottom at {optimal_fvg['bottom']}")
            return optimal_fvg
        else:
            print("\n❌ Failed to select optimal FVG")
            return None
    else:
        print("\n❌ No FVGs found in the specified range")
        return None


def test_trend_analysis(swing_points):
    """Test trend analysis."""
    print("\n" + "="*70)
    print("TEST 3: Trend Analysis")
    print("="*70)
    
    candles = create_test_candles()
    
    if not swing_points:
        print("❌ Cannot test trend without swing points")
        return None
    
    trend = analyze_trend(candles, swing_points)
    
    print(f"\nDetected trend: {trend}")
    
    sp1_type = swing_points[0][1]
    sp3_type = swing_points[2][1]
    
    if sp3_type == 'SH' and sp1_type == 'SH':
        print("Pattern: SH -> SL -> SH")
        if trend == 'bullish':
            print("✅ Correctly identified as bullish")
        else:
            print(f"❌ Expected bullish, got {trend}")
    elif sp3_type == 'SL' and sp1_type == 'SL':
        print("Pattern: SL -> SH -> SL")
        if trend == 'bearish':
            print("✅ Correctly identified as bearish")
        else:
            print(f"❌ Expected bearish, got {trend}")
    
    return trend


def test_full_strategy():
    """Test complete strategy logic."""
    print("\n" + "="*70)
    print("TEST 4: Full Strategy (Entry Criteria)")
    print("="*70)
    
    candles = create_test_candles()
    
    signal = check_entry_criteria(candles)
    
    if signal:
        print("\n✅ Entry signal detected!")
        print(f"\nSignal details:")
        print(f"  Trend: {signal['trend']}")
        print(f"  Target: {signal['target']}")
        print(f"  Stop Loss: {signal['stop_loss']}")
        print(f"\n  Swing Points:")
        for i, (idx, sp_type, value) in enumerate(signal['swing_points'], 1):
            print(f"    {i}. Index {idx}: {sp_type} at {value}")
        print(f"\n  FVG:")
        print(f"    Type: {signal['fvg']['type']}")
        print(f"    Top: {signal['fvg']['top']}")
        print(f"    Bottom: {signal['fvg']['bottom']}")
        print(f"    Range: indices {signal['fvg']['start_idx']} to {signal['fvg']['end_idx']}")
        
        # Verify FVG is in correct range
        sp1_idx = signal['swing_points'][0][0]
        sp2_idx = signal['swing_points'][1][0]
        fvg_start = signal['fvg']['start_idx']
        
        if sp2_idx <= fvg_start <= sp1_idx:
            print(f"\n✅ FVG is correctly located between SP2 and SP1")
        else:
            print(f"\n❌ ERROR: FVG is NOT between SP2 and SP1!")
            print(f"   SP2 index: {sp2_idx}")
            print(f"   FVG start: {fvg_start}")
            print(f"   SP1 index: {sp1_idx}")
    else:
        print("\n❌ No entry signal detected")
        print("This might be expected if test data doesn't meet all criteria")
    
    return signal


def test_fvg_range_verification():
    """Specific test to verify FVG search range fix."""
    print("\n" + "="*70)
    print("TEST 5: FVG Range Fix Verification (CRITICAL)")
    print("="*70)
    
    # Create candles with FVGs in different locations
    candles = [
        {'open': 100, 'high': 105, 'low': 95, 'close': 102, 'volume': 1000},   # 0
        {'open': 102, 'high': 110, 'low': 100, 'close': 108, 'volume': 1000},  # 1 - SH (3rd/oldest)
        {'open': 108, 'high': 109, 'low': 103, 'close': 105, 'volume': 1000},  # 2
        # FVG between 3rd and 2nd (should NOT be detected after fix)
        {'open': 105, 'high': 106, 'low': 90, 'close': 92, 'volume': 1000},    # 3 - FVG start (high=106)
        {'open': 92, 'high': 95, 'low': 88, 'close': 90, 'volume': 1000},      # 4 - middle
        {'open': 90, 'high': 93, 'low': 110, 'close': 92, 'volume': 1000},     # 5 - FVG end (low=110) INVALID FVG
        {'open': 92, 'high': 94, 'low': 85, 'close': 88, 'volume': 1000},      # 6 - SL (2nd/middle)
        {'open': 88, 'high': 90, 'low': 87, 'close': 89, 'volume': 1000},      # 7
        # FVG between 2nd and 1st (SHOULD be detected)
        {'open': 89, 'high': 91, 'low': 88, 'close': 90, 'volume': 1000},      # 8 - FVG start (high=91)
        {'open': 90, 'high': 95, 'low': 89, 'close': 93, 'volume': 1000},      # 9 - middle
        {'open': 93, 'high': 100, 'low': 98, 'close': 99, 'volume': 1000},     # 10 - FVG end (low=98)
        {'open': 99, 'high': 115, 'low': 98, 'close': 112, 'volume': 1000},    # 11 - SH (1st/recent)
        {'open': 112, 'high': 113, 'low': 108, 'close': 110, 'volume': 1000},  # 12
    ]
    
    swing_points = find_three_swing_points(candles)
    
    if not swing_points:
        print("❌ Could not find swing points in test data")
        return False
    
    sp1_idx = swing_points[0][0]
    sp2_idx = swing_points[1][0]
    sp3_idx = swing_points[2][0]
    
    print(f"\nSwing points found:")
    print(f"  SP1 (recent): index {sp1_idx}")
    print(f"  SP2 (middle): index {sp2_idx}")
    print(f"  SP3 (oldest): index {sp3_idx}")
    
    # Search in the CORRECT range (SP2 to SP1)
    correct_range_fvgs = find_fvgs_in_range(candles, sp2_idx, sp1_idx, 'bullish')
    print(f"\nFVGs found between SP2 and SP1: {len(correct_range_fvgs)}")
    
    # Search in the WRONG range (SP3 to SP2) - this should NOT be included
    wrong_range_fvgs = find_fvgs_in_range(candles, sp3_idx, sp2_idx, 'bullish')
    print(f"FVGs found between SP3 and SP2: {len(wrong_range_fvgs)}")
    
    # Now test the full strategy
    signal = check_entry_criteria(candles)
    
    if signal and signal['fvg']:
        fvg_start = signal['fvg']['start_idx']
        print(f"\nStrategy selected FVG starting at index: {fvg_start}")
        
        if sp2_idx <= fvg_start <= sp1_idx:
            print(f"✅ PASS: FVG is correctly in SP2→SP1 range")
            print(f"   The fix is working correctly!")
            return True
        else:
            print(f"❌ FAIL: FVG is in SP3→SP2 range")
            print(f"   The fix is NOT working!")
            print(f"   Expected range: {sp2_idx} to {sp1_idx}")
            print(f"   FVG location: {fvg_start}")
            return False
    else:
        print("\n⚠️  No signal generated (might be expected depending on test data)")
        return None


def run_all_tests():
    """Run all verification tests."""
    print("\n" + "="*70)
    print("CODEBASE VERIFICATION TEST SUITE")
    print("="*70)
    print("\nThis will verify that all fixes are working correctly.")
    print("Pay special attention to TEST 5 - this verifies the critical fix.")
    
    try:
        # Run tests in sequence
        swing_points = test_swing_point_identification()
        fvg = test_fvg_identification(swing_points)
        trend = test_trend_analysis(swing_points)
        signal = test_full_strategy()
        critical_test = test_fvg_range_verification()
        
        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"Swing Point Detection: {'✅ PASS' if swing_points else '❌ FAIL'}")
        print(f"FVG Identification: {'✅ PASS' if fvg else '⚠️  CHECK'}")
        print(f"Trend Analysis: {'✅ PASS' if trend else '⚠️  CHECK'}")
        print(f"Full Strategy: {'✅ PASS' if signal else '⚠️  CHECK'}")
        print(f"FVG Range Fix: {'✅ PASS' if critical_test else '❌ FAIL' if critical_test is False else '⚠️  CHECK'}")
        
        if critical_test is True:
            print("\n🎉 All critical tests passed! The codebase is working correctly.")
        elif critical_test is False:
            print("\n⚠️  CRITICAL TEST FAILED! The FVG range fix is not working.")
        else:
            print("\n⚠️  Some tests need manual verification.")
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()