-- Task 5. orphan customers
SELECT COUNT(*) AS orders_with_missing_customer_count
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;


-- Task 6. orphan restaurants
SELECT COUNT(*) AS orders_with_missing_restaurant_count
FROM orders o
LEFT JOIN restaurants r ON o.restaurant_id = r.restaurant_id
WHERE r.restaurant_id IS NULL;


-- Task 7. orphan couriers
SELECT COUNT(*) AS orders_with_missing_courier_count
FROM orders o 
LEFT JOIN couriers c ON o.courier_id = c.courier_id
WHERE c.courier_id IS NULL;