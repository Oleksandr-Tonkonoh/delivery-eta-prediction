-- Task 15. basic delivery dataset
SELECT c.customer_id, o.order_id, r.restaurant_id, co.courier_id,
       c.city, c.customer_segment,
       r.cuisine, r.avg_prep_minutes, r.rating,
       co.experience_months, co.vehicle, co.rating,
       o.distance_km, o.items_count, o.order_amount, o.weather, o.traffic_level, o.order_ts, o.delivery_minutes
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN restaurants r ON r.restaurant_id = o.restaurant_id
JOIN couriers co ON co.courier_id = o.courier_id;

