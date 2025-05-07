SELECT
  sale_date,
  SUM(price * quantity) AS total_daily_sales,
  COUNT(*) AS sales_count
FROM sales
GROUP BY sale_date
ORDER BY sale_date;
