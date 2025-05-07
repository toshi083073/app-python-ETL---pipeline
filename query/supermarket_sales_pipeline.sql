SELECT
  date AS sale_date,
  SUM(sales_total) AS daily_sales
FROM
  supermarket_sales
GROUP BY
  date
ORDER BY
  date;
