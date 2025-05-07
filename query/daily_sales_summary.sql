-- query/daily_sales_summary.sql
SELECT
  sale_date,
  item_name,
  total_sales
FROM daily_sales_summary
WHERE sale_date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY sale_date DESC, item_name;
