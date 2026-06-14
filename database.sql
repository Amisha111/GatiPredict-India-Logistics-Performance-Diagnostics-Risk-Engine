DROP TABLE IF EXISTS india_logistics_warehouse;

CREATE TABLE india_logistics_warehouse (
    delivery_id REAL,
    delivery_partner VARCHAR(50),
    package_type VARCHAR(50),
    vehicle_type VARCHAR(50),
    delivery_mode VARCHAR(30),
    region VARCHAR(20),
    weather_condition VARCHAR(30),
    distance_km NUMERIC,
    package_weight_kg NUMERIC,
    delivery_time_hours_clean INT,
    expected_time_hours_clean INT,
    delayed VARCHAR(5),
    delivery_status VARCHAR(30),
    delivery_rating INT,
    delivery_cost NUMERIC,
    target_delayed INT
);
