-- Daily revenue with 7-day rolling average (window function)
WITH daily AS (
  SELECT order_date, SUM(amount) AS revenue
  FROM sales_orders
  GROUP BY order_date
)
SELECT
  order_date,
  revenue,
  AVG(revenue) OVER (ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS revenue_7d_avg
FROM daily
ORDER BY order_date;
