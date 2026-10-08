# Supplier Performance Scorecard

A small analytics project that ranks suppliers on delivery, quality and price using SQL, plus a simple web dashboard of the results.

**Data note:** all data is simulated (12 suppliers, 1,320 purchase orders, Jan 2025 to Jun 2026). It is not from a real company.

## How the score works
| Measure | How it is calculated | Weight |
|---|---|---|
| Delivery | % of orders delivered on or before the promised date | 40% |
| Quality | 100 minus (defect rate x 1000), floored at 0 (10% defects = 0) | 35% |
| Price | Unit price / market price, scaled so 0.90x = 100 and 1.30x = 0 | 25% |

Tiers: Preferred (85+), Acceptable (75 to 84.9), Under Review (below 75).

## Folder guide
- `01_schema.sql`, `02_supplier_scorecard.sql`, `03_analysis_queries.sql`: schema, the scorecard view, and the analysis queries
- the `.csv` files: simulated tables and exported results
- `POWER_BI_BUILD_GUIDE.md`: DAX measures and steps to rebuild the report in Power BI Desktop
- `index.html` the dashboard (open in any browser)
- `generate_data.py`, `make_dashboard.py` scripts that rebuild the data and the page

## Rebuild
```
python3 generate_data.py
python3 make_dashboard.py
```
Requires Python 3 only (SQLite is built in).

## Limitations
Simulated data, subjective weights and scoring thresholds, no seasonality or lead-time analysis, and no real market price feed.
