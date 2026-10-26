-- Task 21. final ml dataset
WITH CTE AS (SELECT EXTRACT(HOUR FROM order_ts) AS order_hour, COUNT(order_id) AS orders_count
FROM orders
GROUP BY EXTRACT(HOUR FROM order_ts)),

CTE2 AS (SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY orders_count)  AS p_75
FROM CTE),

CTE3 AS (SELECT CTE.order_hour, CTE.orders_count, CTE2.p_75
FROM CTE
CROSS JOIN CTE2)

SELECT o.order_id, o.distance_km, o.items_count, o.order_amount, o.weather, 
o.traffic_level, o.order_ts, o.delivery_minutes, DATE(o.order_ts) AS date,
r.restaurant_id, r.avg_prep_minutes, r.rating AS restaurant_rating, 
w.avg_temp_c, w.rain_mm, w.snow_cm,
c.courier_id, c.vehicle, c.experience_months, c.rating AS courier_rating,
EXTRACT(HOUR FROM o.order_ts) AS order_hour, 
EXTRACT(DOW FROM o.order_ts) AS day_of_week, 
CASE 
    WHEN EXTRACT(DOW FROM o.order_ts) BETWEEN 1 AND 5 THEN FALSE  
    ELSE TRUE
END AS is_weekend,

ROW_NUMBER() OVER(PARTITION BY r.restaurant_id ORDER BY o.order_ts, o.order_id) - 1 AS restaurant_previous_orders_count,
AVG(o.delivery_minutes) 
    OVER(PARTITION BY r.restaurant_id ORDER BY o.order_ts, o.order_id 
    ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)
    AS restaurant_historical_avg_delivery,

ROW_NUMBER() OVER(PARTITION BY c.courier_id ORDER BY o.order_ts, o.order_id) - 1 AS courier_previous_orders_count,
AVG(o.delivery_minutes) 
    OVER(PARTITION BY c.courier_id ORDER BY o.order_ts, o.order_id 
    ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) 
    AS courier_historical_avg_delivery,

CASE 
    WHEN CTE3.orders_count > CTE3.p_75 THEN TRUE
    ELSE FALSE
END AS is_peak_hour

FROM orders o 
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
JOIN couriers c ON o.courier_id = c.courier_id
LEFT JOIN weather_daily w ON DATE(o.order_ts) = w.date
JOIN CTE3 ON EXTRACT(HOUR FROM o.order_ts) = CTE3.order_hour;
