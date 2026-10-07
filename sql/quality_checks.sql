-- Nulls
SELECT COUNT(*) AS null_order_ids FROM sales_orders WHERE order_id IS NULL OR amount IS NULL;

-- Duplicates
SELECT order_id, COUNT(*) FROM sales_orders GROUP BY order_id HAVING COUNT(*) > 1;

-- Schema / range sanity
SELECT COUNT(*) AS negative_amounts FROM sales_orders WHERE amount < 0;
