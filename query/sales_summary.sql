WITH base_sales AS (
  SELECT
    item_name,
    price * quantity AS total_price,
    sale_date
  FROM sales
),
aggregated AS (
  SELECT
    item_name,
    SUM(total_price) AS total_sales,
    SUM(CASE WHEN sale_date < '2024-07-01' THEN total_price ELSE 0 END) AS first_half_sales,
    SUM(CASE WHEN sale_date >= '2024-07-01' THEN total_price ELSE 0 END) AS second_half_sales
  FROM base_sales
  GROUP BY item_name
),
ranked AS (
  SELECT
    item_name,
    total_sales,
    first_half_sales,
    second_half_sales,
    second_half_sales - first_half_sales AS diff,
    RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
  FROM aggregated
)
SELECT *
FROM ranked
WHERE sales_rank <= 10
ORDER BY sales_rank;
