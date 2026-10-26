CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    signup_date DATE,
    city VARCHAR(50),
    customer_segment VARCHAR(50)
);


CREATE TABLE restaurants (
    restaurant_id INT PRIMARY KEY,
    city VARCHAR(50),
    cuisine VARCHAR(50),
    avg_prep_minutes DECIMAL(5, 2),
    rating DECIMAL(3, 2)
);


CREATE TABLE couriers (
    courier_id INT PRIMARY KEY,
    experience_months INT,
    vehicle VARCHAR(100),
    rating DECIMAL(3, 2)
);


CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),
    restaurant_id INT,
    FOREIGN KEY (restaurant_id)
        REFERENCES restaurants(restaurant_id),
    courier_id INT,
    FOREIGN KEY (courier_id)
        REFERENCES couriers(courier_id),
    order_ts TIMESTAMP,
    distance_km DECIMAL(5, 2),
    items_count INT,
    order_amount DECIMAL(5, 2),
    weather VARCHAR(50),
    traffic_level VARCHAR(50),
    delivery_minutes DECIMAL(5, 2)
);


CREATE TABLE weather_daily (
    date DATE PRIMARY KEY,
    avg_temp_c DECIMAL(5, 2),
    rain_mm DECIMAL(5, 2),
    snow_cm DECIMAL(5, 2)
);


CREATE TABLE flourmills_sales (
    sales_id INT PRIMARY KEY,
    sale_date DATE,
    region VARCHAR(100),
    state VARCHAR(100),
    product_category VARCHAR(100),
    product_name VARCHAR(150),
    customer_type VARCHAR(100),
    customer_id INT,
    quantity_sold INT,
    unit_price DECIMAL(10, 2),
    discount_rate INT,
    payment_method VARCHAR(100),
    sales_rep VARCHAR(150),
    warehouse VARCHAR(100),
    delivery_status VARCHAR(100),
    order_channel VARCHAR(100),
    batch_number INT,
    production_date DATE,
    total_amount DECIMAL(10, 2)
);