"""
Load cleaned Airbnb listing data and insert into a MySQL staging table for analytics and SQL-based filtering.
"""

import pandas as pd
import numpy as np
import mysql.connector
from data_clean import get_cleaned_df

# Load and clean the raw NYC 2019 data CSV
csv_path = "data/AB_NYC_2019.csv"
df = get_cleaned_df(csv_path)

# Copy the cleaned DataFrame
df_sql = df[
    [
        "id",
        "name",
        "host_id",
        "host_name",
        "neighbourhood_group",
        "neighbourhood",
        "latitude",
        "longitude",
        "room_type",
        "price",
        "minimum_nights",
        "number_of_reviews",
        "last_review",
        "reviews_per_month",
        "calculated_host_listings_count",
        "availability_365",
    ]
].copy()

# Convert last_review to Python date for MySQL DATE compatability
df_sql["last_review"] = df_sql["last_review"].dt.date

# Replace NaN with None so they can be imported as NULLs to MySQL
df_sql = df_sql.where(pd.notnull(df_sql), None)

# Iterate and turn dataframe rows into list of tuples for insert
records = [tuple(row) for row in df_sql.itertuples(index=False, name=None)]

# Connect to MySQL on Docker
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="DataAnalysis123",
    database="airbnb_nyc"
)

# Create cursor object for SQL execution
cur = conn.cursor()

# bulk insert of rows
insert_sql = """
    INSERT INTO listings_staging
    (id, name, host_id, host_name,
     neighbourhood_group, neighbourhood,
     latitude, longitude, room_type,
     price, minimum_nights, number_of_reviews,
     last_review, reviews_per_month,
     calculated_host_listings_count, availability_365)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

cur.executemany(insert_sql, records)

# Commit and clean up
conn.commit()
cur.close()
conn.close()

print(f"inserted {len(records)} rows into listings_staging.")