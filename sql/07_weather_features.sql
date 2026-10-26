-- Task 20. weather features
SELECT o.order_id, 
       DATE(o.order_ts) AS order_date, 
       w.avg_temp_c, w.rain_mm, w.snow_cm
FROM orders o 
LEFT JOIN weather_daily w ON DATE(o.order_ts) = w.date;
