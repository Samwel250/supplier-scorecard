# Power BI Build Guide
1. **Get Data** → Text/CSV: import `data/suppliers.csv` and `data/purchase_orders.csv` (or connect to your SQL database and import `v_supplier_scorecard`).
2. **Model**: relationship `suppliers[supplier_id]` 1 → * `purchase_orders[supplier_id]`. Add a Date table (`Calendar = CALENDAR(DATE(2025,1,1), DATE(2026,12,31))`) related to `order_date`.
3. **Measures (DAX)**
```
Total Spend = SUMX(purchase_orders, purchase_orders[qty_ordered] * purchase_orders[unit_price])
On-Time Rate = DIVIDE(CALCULATE(COUNTROWS(purchase_orders), FILTER(purchase_orders, purchase_orders[delivery_date] <= purchase_orders[promised_date])), COUNTROWS(purchase_orders))
Defect Rate = DIVIDE(SUM(purchase_orders[qty_defective]), SUM(purchase_orders[qty_received]))
Price Index = AVERAGEX(purchase_orders, DIVIDE(purchase_orders[unit_price], purchase_orders[market_price]))
Delivery Score = [On-Time Rate] * 100
Quality Score = MAX(0, 100 - [Defect Rate] * 1000)
Price Score = MAX(0, MIN(100, 100 - ([Price Index] - 0.90) * 250))
Weighted Score = 0.40*[Delivery Score] + 0.35*[Quality Score] + 0.25*[Price Score]
Supplier Rank = RANKX(ALL(suppliers[supplier_name]), [Weighted Score], , DESC)
Tier = SWITCH(TRUE(), [Weighted Score] >= 85, "Preferred", [Weighted Score] >= 75, "Acceptable", "Under Review")
```
4. **Visuals**: KPI cards (On-Time Rate, Defect Rate, Total Spend, # Under Review); ranked table/bar of Weighted Score by supplier with conditional formatting by Tier; scatter (X = Price Index, Y = On-Time Rate, size = Total Spend); line chart of On-Time Rate by month; slicers for Category, Country, Date.
5. **Optional**: weight what-if parameters (Modeling → New Parameter) so viewers can adjust the 40/35/25 weights.
