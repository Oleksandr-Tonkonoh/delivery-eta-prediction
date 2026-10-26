-- Task 12. delivery trend over time by hour
SELECT DATE_TRUNC('hour', order_ts) AS order_hour, 
       COUNT(*) AS orders_count,  
       ROUND(AVG(delivery_minutes), 2) AS avg_delivery_minutes
FROM orders
GROUP BY DATE_TRUNC('hour', order_ts)
ORDER BY DATE_TRUNC('hour', order_ts);


-- Task 13. weekday vs weekend
WITH CTE AS (SELECT order_id, delivery_minutes, EXTRACT(DOW FROM order_ts),
CASE 
    WHEN EXTRACT(DOW FROM order_ts) BETWEEN 1 AND 5 THEN 'weekday' 
    ELSE 'weekend' 
END AS day_type
FROM orders)

SELECT day_type,
       COUNT(order_id) AS orders_count, 
       ROUND(AVG(delivery_minutes), 0) AS avg_delivery_minutes
FROM CTE
GROUP BY day_type;


-- Task 14. monthly trend
SELECT DATE_TRUNC('month', order_ts) AS order_month,
       COUNT(order_id) AS orders_count,
       ROUND(AVG(delivery_minutes), 2) AS avg_delivery_minutes
FROM orders
GROUP BY DATE_TRUNC('month', order_ts)
ORDER BY DATE_TRUNC('month', order_ts);
