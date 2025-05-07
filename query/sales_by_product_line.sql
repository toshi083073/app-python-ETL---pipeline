SELECT
  product_line,
  COUNT(*) AS transaction_count,
  SUM(quantity) AS total_quantity,
  ROUND(AVG(unit_price), 2) AS avg_unit_price,
  SUM(sales_total) AS total_sales
FROM
  supermarket_sales
GROUP BY
  product_line
ORDER BY
  total_sales DESC;
