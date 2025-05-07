SELECT
  product_line,
  COUNT(*) AS sales_count,
  ROUND(AVG(unit_price), 2) AS avg_unit_price,
  ROUND(SUM(sales_total), 2) AS total_sales
FROM
  supermarket_sales
GROUP BY
  product_line
ORDER BY
  total_sales DESC;
