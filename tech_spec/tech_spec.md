# Technical Specification: Swing Point and Fair Value Gap Strategy

## 1. Swing Point Identification
- Start **moving backwards** from the most recent *closed* candle.  
  *(Ignore the current candle if it has not closed yet.)*  
- Identify **3 alternating Swing Points** (High → Low → High, or Low → High → Low).  

### Rules
- **No consecutive swing point type**:  
  - Two Swing Highs or two Swing Lows cannot be considered in sequence.  

---

## 2. Third Swing Point Logic
The **third Swing Point** plays a crucial role in determining the trend bias.  

- If the **3rd Swing Point** is a **Swing High** and the **1st Swing Point** is also a **Swing High**:  
  1. Check if any candle *between* these three swing points **closes above the 3rd Swing High**.  
     - ✅ If yes → Potential **Bullish Trend**.  
     - ❌ If no → Check if any candle *between* the 2nd Swing Point closes **below it**.  
       - ✅ If yes → Potential **Bearish Trend**.  

- The same logic applies **in reverse** if the 3rd Swing Point is a **Swing Low**.  

**Illustrations**  
![Bullish Scenario](Bullish%20Scenario.png)  
![Bearish Scenario](Bearish%20Scenario.png)  
![Bearish Scenario 2](Bearish%20Scenario%202.png)  

---

## 3. Fair Value Gap (FVG) Entry Confirmation
- In a **bullish case (as per Step 2)**:  
  - If a **Bullish Fair Value Gap** exists *between the 1st and 2nd Swing Points*, this zone may serve as a **potential entry area** in a **Lower Time Frame (LTF)**.  
  - Monitor price action on the LTF when price returns into this FVG.  

- In this setup:  
  - 🎯 **Target** = First Swing Point.  
  - 🛑 **Stop Loss** = Second Swing Point.  

- The same applies **vice versa** for bearish cases.  

---

## 4. Definitions

### Swing Point
- Requires **3 consecutive closed candles**.  
- If the **middle candle’s high** is higher than both the first and third → **Swing High**.  
- If the **middle candle’s low** is lower than both the first and third → **Swing Low**.  

### Fair Value Gap (FVG)
- Requires **3 consecutive closed candles**.  
- **Bullish FVG**: If the **first candle’s high** is lower than the **third candle’s low**.  
- **Bearish FVG**: If the **first candle’s low** is higher than the **third candle’s high**.  
