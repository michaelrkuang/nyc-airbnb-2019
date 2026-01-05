-- Create database
DROP TABLE IF EXISTS listings_staging;
CREATE TABLE listings_staging (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    host_id INT,
    host_name VARCHAR(255),
    neighbourhood_group VARCHAR(100),
    neighbourhood VARCHAR(100),
    latitude DOUBLE,
    longitude DOUBLE,
    room_type VARCHAR(50),
    price INT,
    minimum_nights INT,
    number_of_reviews INT,
    last_review DATE,
    reviews_per_month DOUBLE,
    calculated_host_listings_count INT,
    availability_365 INT
);

-- Core analytics view used by Tableau dashboard
DROP VIEW IF EXISTS listings_data;
CREATE VIEW listings_data AS
SELECT
    *,
    AVG(price) OVER (
        PARTITION BY neighbourhood_group, room_type
    ) AS avg_price_group_roomtype,
    (
        (price - AVG(price) OVER (PARTITION BY neighbourhood_group, room_type))
        / AVG(price) OVER (PARTITION BY neighbourhood_group, room_type)
    ) * 100 AS price_vs_market_pct
FROM listings_staging
WHERE price BETWEEN 40 AND 355
  AND minimum_nights <= 365;