-- Task 16. previous restaurant delivery count
SELECT r.restaurant_id, o.order_id, o.order_ts, 
ROW_NUMBER() OVER(PARTITION BY o.restaurant_id ORDER BY o.order_ts, o.order_id) - 1 
    AS restaurant_previous_orders_count
FROM restaurants r JOIN orders o ON r.restaurant_id = o.restaurant_id;


-- Task 17. historical restaurant average
SELECT r.restaurant_id, o.order_id, o.order_ts, o.delivery_minutes, 
ROUND(AVG(o.delivery_minutes) OVER(PARTITION BY o.restaurant_id ORDER BY ORDER BY o.order_ts, o.order_id 
    ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING), 2)
    AS restaurant_historical_avg_delivery
FROM restaurants r JOIN orders o ON r.restaurant_id = o.restaurant_id;


-- Task 18. previous courier deliveries
SELECT c.courier_id, o.order_id, o.order_ts, 
ROW_NUMBER() OVER(PARTITION BY o.courier_id ORDER BY o.order_ts, o.order_id) - 1 
    AS courier_previous_orders_count
FROM couriers c JOIN orders o ON c.courier_id = o.courier_id;


-- Task 19. historical courier average
SELECT c.courier_id, o.order_id, o.order_ts, o.delivery_minutes, 
ROUND(AVG(o.delivery_minutes) 
OVER(PARTITION BY o.courier_id ORDER BY ORDER BY o.order_ts, o.order_id 
    ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING), 2)
    AS courier_historical_avg_delivery
FROM couriers c JOIN orders o ON c.courier_id = o.courier_id;