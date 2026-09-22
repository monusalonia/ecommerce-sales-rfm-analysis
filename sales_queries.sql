-- E-Commerce Sales & RFM Segmentation Queries
-- PostgreSQL / MySQL Compatible

-- 1. Monthly Revenue & Average Order Value (AOV) Trend
SELECT 
    TO_CHAR(order_date, 'YYYY-MM') AS sales_month,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(total_amount), 2) AS gross_revenue,
    ROUND(AVG(total_amount), 2) AS average_order_value
FROM orders
WHERE total_amount > 0
GROUP BY sales_month
ORDER BY sales_month ASC;

-- 2. Top Revenue-Generating Product Categories
SELECT 
    category,
    COUNT(order_id) AS order_volume,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(SUM(total_amount) * 100.0 / SUM(SUM(total_amount)) OVER (), 2) AS revenue_share_pct
FROM orders
WHERE category IS NOT NULL
GROUP BY category
ORDER BY total_revenue DESC;

-- 3. High-Value Customer Identification (Repeat Buyers Spend > 15,000)
SELECT 
    customer_id,
    COUNT(order_id) AS lifetime_orders,
    ROUND(SUM(total_amount), 2) AS total_lifetime_spend,
    MAX(order_date) AS last_order_date
FROM orders
GROUP BY customer_id
HAVING COUNT(order_id) >= 5 AND SUM(total_amount) >= 15000
ORDER BY total_lifetime_spend DESC;
