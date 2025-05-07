SELECT
  sale_date AS date,
  SUM(price * quantity) AS total_sales
FROM sales
GROUP BY sale_date
ORDER BY sale_date;
