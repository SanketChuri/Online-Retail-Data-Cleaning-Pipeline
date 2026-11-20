-- name: Overall summary
SELECT
    COUNT(DISTINCT invoice_no)   AS total_orders,
    COUNT(DISTINCT customer_id)  AS total_customers,
    COUNT(DISTINCT stock_code)   AS total_products,
    ROUND(SUM(line_total), 2)    AS total_revenue_gbp
FROM sales;

-- name: Revenue by month
SELECT invoice_month,
       COUNT(DISTINCT invoice_no) AS orders,
       ROUND(SUM(line_total), 2)  AS revenue_gbp
FROM sales
GROUP BY invoice_month
ORDER BY invoice_month;

-- name: Top 10 products by revenue
SELECT stock_code, description,
       SUM(quantity)             AS units_sold,
       ROUND(SUM(line_total), 2) AS revenue_gbp
FROM sales
GROUP BY stock_code, description
ORDER BY revenue_gbp DESC
LIMIT 10;

-- name: Top 10 countries by revenue (excluding UK)
SELECT country,
       COUNT(DISTINCT invoice_no) AS orders,
       ROUND(SUM(line_total), 2)  AS revenue_gbp
FROM sales
WHERE country <> 'United Kingdom'
GROUP BY country
ORDER BY revenue_gbp DESC
LIMIT 10;

-- name: Average order value by month
SELECT invoice_month,
       ROUND(AVG(order_total), 2) AS avg_order_value_gbp
FROM (
    SELECT invoice_no, invoice_month, SUM(line_total) AS order_total
    FROM sales
    GROUP BY invoice_no, invoice_month
)
GROUP BY invoice_month
ORDER BY invoice_month;

-- name: Top 10 customers by spend
SELECT customer_id, country,
       COUNT(DISTINCT invoice_no) AS orders,
       ROUND(SUM(line_total), 2)  AS total_spent_gbp
FROM sales
WHERE has_customer_id = 1
GROUP BY customer_id, country
ORDER BY total_spent_gbp DESC
LIMIT 10;

-- name: Busiest days of the week
SELECT day_of_week,
       COUNT(DISTINCT invoice_no) AS orders,
       ROUND(SUM(line_total), 2)  AS revenue_gbp
FROM sales
GROUP BY day_of_week
ORDER BY orders DESC;

-- name: Repeat vs one-time customers
SELECT CASE WHEN orders = 1 THEN 'One-time' ELSE 'Repeat' END AS customer_type,
       COUNT(*)             AS customers,
       ROUND(SUM(spent), 2) AS revenue_gbp
FROM (
    SELECT customer_id,
           COUNT(DISTINCT invoice_no) AS orders,
           SUM(line_total)            AS spent
    FROM sales
    WHERE has_customer_id = 1
    GROUP BY customer_id
)
GROUP BY customer_type;

-- name: Why rows were rejected
SELECT reject_reason, COUNT(*) AS rows_rejected
FROM rejected_rows
GROUP BY reject_reason
ORDER BY rows_rejected DESC;