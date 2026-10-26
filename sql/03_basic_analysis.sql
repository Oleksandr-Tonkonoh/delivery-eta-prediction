-- Task 8. deliveries by city
SELECT r.city, 
       COUNT(o.order_id) AS orders_count,
       ROUND(AVG(o.delivery_minutes), 2) AS avg_delivery_minutes,
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY o.delivery_minutes)  AS median_delivery_minutes
FROM restaurants r 
INNER JOIN orders o ON r.restaurant_id = o.restaurant_id
GROUP BY r.city;


-- Task 9. delivery by traffic
SELECT traffic_level, COUNT(order_id) AS orders_count, ROUND(AVG(delivery_minutes), 2) AS avg_delivery_minutes 
FROM orders
GROUP BY traffic_level; 


-- Task 10. delivery by weather
SELECT weather, COUNT(order_id) AS orders_count, ROUND(AVG(delivery_minutes), 2) AS avg_delivery_minutes 
FROM orders
GROUP BY weather;


-- Task 11 — delivery by vehicle
SELECT c.vehicle, COUNT(o.order_id) AS orders_count,
                   ROUND(AVG(o.delivery_minutes), 2) AS avg_delivery_minutes
FROM couriers c 
JOIN orders o ON c.courier_id = o.courier_id
GROUP BY c.vehicle;