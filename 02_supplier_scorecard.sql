-- Weighted supplier scorecard (SQLite syntax; for SQL Server use DATEDIFF, GREATEST/LEAST or CASE)
-- Weights: Delivery 40% | Quality 35% | Price 25%
CREATE VIEW v_supplier_scorecard AS
WITH base AS (
  SELECT s.supplier_id, s.supplier_name, s.category, s.country,
    COUNT(*) AS total_orders,
    SUM(p.qty_ordered * p.unit_price) AS total_spend,
    1.0 * SUM(CASE WHEN p.delivery_date <= p.promised_date THEN 1 ELSE 0 END) / COUNT(*) AS on_time_rate,
    AVG(MAX(julianday(p.delivery_date) - julianday(p.promised_date), 0)) AS avg_days_late,
    1.0 * SUM(p.qty_defective) / SUM(p.qty_received) AS defect_rate,
    AVG(p.unit_price / p.market_price) AS price_index
  FROM purchase_orders p JOIN suppliers s ON s.supplier_id = p.supplier_id
  GROUP BY s.supplier_id, s.supplier_name, s.category, s.country
), scored AS (
  SELECT *,
    ROUND(on_time_rate * 100, 1) AS delivery_score,
    ROUND(MAX(0, 100 - defect_rate * 1000), 1) AS quality_score,
    ROUND(MAX(0, MIN(100, 100 - (price_index - 0.90) * 250)), 1) AS price_score
  FROM base)
SELECT *,
  ROUND(0.40*delivery_score + 0.35*quality_score + 0.25*price_score, 1) AS weighted_score,
  RANK() OVER (ORDER BY 0.40*delivery_score + 0.35*quality_score + 0.25*price_score DESC) AS overall_rank,
  CASE WHEN 0.40*delivery_score + 0.35*quality_score + 0.25*price_score >= 85 THEN 'Preferred'
       WHEN 0.40*delivery_score + 0.35*quality_score + 0.25*price_score >= 75 THEN 'Acceptable'
       ELSE 'Under Review' END AS tier
FROM scored;
