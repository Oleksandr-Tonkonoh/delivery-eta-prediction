-- Active: 1790175058178@@127.0.0.1@5432@delivery_eta


-- Task 1. Table Size

-- Customers
SELECT COUNT(*) AS rows_count 
FROM customers;


-- Restaurants
SELECT COUNT(*) AS rows_count 
FROM restaurants;


-- Couriers
SELECT COUNT(*) AS rows_count 
FROM couriers;

-- Orders
SELECT COUNT(*) AS rows_count 
FROM orders;


-- Weather_daily
SELECT COUNT(*) AS rows_count 
FROM weather_daily;


-- Task 2. Primary key duplicates

-- Customers
SELECT COUNT(*) AS rows_count,
       COUNT(customer_id) AS non_null_id_count,
       COUNT(*) - COUNT(customer_id) AS null_id_count,
       COUNT(DISTINCT customer_id) AS distinct_id_count,
       COUNT(customer_id) - COUNT(DISTINCT customer_id) AS duplicate_id_count
FROM customers;


-- Restaurants
SELECT COUNT(*) AS rows_count,
       COUNT(restaurant_id) AS non_null_id_count,
       COUNT(*) - COUNT(restaurant_id) AS null_id_count,
       COUNT(DISTINCT restaurant_id) AS distinct_id_count,
       COUNT(restaurant_id) - COUNT(DISTINCT restaurant_id) AS duplicate_id_count
FROM restaurants;


-- Couriers
SELECT COUNT(*) AS rows_count,
       COUNT(courier_id) AS non_null_id_count,
       COUNT(*) - COUNT(courier_id) AS null_id_count,
       COUNT(DISTINCT courier_id) AS distinct_id_count,
       COUNT(courier_id) - COUNT(DISTINCT courier_id) AS duplicate_id_count
FROM couriers;


-- Orders
SELECT COUNT(*) AS rows_count,
       COUNT(order_id) AS non_null_id_count,
       COUNT(*) - COUNT(order_id) AS null_id_count,
       COUNT(DISTINCT order_id) AS distinct_id_count,
       COUNT(order_id) - COUNT(DISTINCT order_id) AS duplicate_id_count
FROM orders;


-- Weather_daily
SELECT COUNT(*) AS rows_count,
       COUNT(date) AS non_null_id_count,
       COUNT(*) - COUNT(date) AS null_id_count,
       COUNT(DISTINCT date) AS distinct_id_count,
       COUNT(date) - COUNT(DISTINCT date) AS duplicate_id_count
FROM weather_daily;


-- Task 3. NULL report

-- distance_km
SELECT 'distance_km' AS column_name,
       COUNT(*) AS all_rows_count,
       SUM(CASE WHEN distance_km IS NULL THEN 1 ELSE 0 END) AS null_count,
       ROUND(SUM(CASE WHEN distance_km IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS null_percentage
FROM orders;


-- items_count
SELECT 'items_count' AS column_name,
       COUNT(*) AS all_rows_count,
       SUM(CASE WHEN items_count IS NULL THEN 1 ELSE 0 END) AS null_count,
       ROUND(SUM(CASE WHEN items_count IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS null_percentage
FROM orders;


-- order_amount
SELECT 'order_amount' AS column_name,
       COUNT(*) AS all_rows_count,
       SUM(CASE WHEN order_amount IS NULL THEN 1 ELSE 0 END) AS null_count,
       ROUND(SUM(CASE WHEN order_amount IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS null_percentage
FROM orders;


-- weather
SELECT 'weather' AS column_name,
       COUNT(*) AS all_rows_count,
       SUM(CASE WHEN weather IS NULL THEN 1 ELSE 0 END) AS null_count,
       ROUND(SUM(CASE WHEN weather IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS null_percentage
FROM orders;


-- traffic_level
SELECT 'traffic_level' AS column_name,
       COUNT(*) AS all_rows_count,
       SUM(CASE WHEN traffic_level IS NULL THEN 1 ELSE 0 END) AS null_count,
       ROUND(SUM(CASE WHEN traffic_level IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS null_percentage
FROM orders;


-- delivery_minutes
SELECT 'delivery_minutes' AS column_name,
       COUNT(*) AS all_rows_count,
       SUM(CASE WHEN delivery_minutes IS NULL THEN 1 ELSE 0 END) AS null_count,
       ROUND(SUM(CASE WHEN delivery_minutes IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS null_percentage
FROM orders;


-- Task 4. invalid values


SELECT SUM(CASE WHEN distance_km <= 0 THEN 1 ELSE 0 END) AS distance_km_invalid_values_count,
       SUM(CASE WHEN items_count <= 0 THEN 1 ELSE 0 END) AS items_count_invalid_values_count,
       SUM(CASE WHEN order_amount <= 0 THEN 1 ELSE 0 END) AS order_amount_invalid_values_count,
       SUM(CASE WHEN delivery_minutes <= 0 THEN 1 ELSE 0 END) AS delivery_minutes_invalid_values_count
FROM orders;





