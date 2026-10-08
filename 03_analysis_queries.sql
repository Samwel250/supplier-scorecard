-- Q1 Ranked scorecard
SELECT overall_rank, supplier_name, category, weighted_score, tier FROM v_supplier_scorecard ORDER BY overall_rank;
-- Q2 Suppliers needing review, with weakest dimension
SELECT supplier_name, weighted_score,
  CASE WHEN delivery_score<=MIN(quality_score,price_score) THEN 'Delivery'
       WHEN quality_score<=price_score THEN 'Quality' ELSE 'Price' END AS weakest_area
FROM v_supplier_scorecard WHERE tier='Under Review' ORDER BY weighted_score;
-- Q3 Monthly on-time trend
SELECT strftime('%Y-%m', order_date) AS month, ROUND(100.0*SUM(delivery_date<=promised_date)/COUNT(*),1) AS on_time_pct
FROM purchase_orders GROUP BY 1 ORDER BY 1;
-- Q4 Spend exposure by tier
SELECT tier, ROUND(SUM(total_spend)) AS spend, ROUND(100.0*SUM(total_spend)/(SELECT SUM(total_spend) FROM v_supplier_scorecard),1) AS pct_spend
FROM v_supplier_scorecard GROUP BY tier;
