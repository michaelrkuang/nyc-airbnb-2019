"""
Clean raw Airbnb listing data and apply formatting to 
prepare records for database loading and analysis.
"""

import pandas as pd

def get_cleaned_df(path):

    df = pd.read_csv(path)

    # Add logic guard rails to exclude rows with irrational data
    df = df[(df["price"] > 0) & (df["minimum_nights"].between(1, 365))]

    # Drop missing coordinates
    df = df.dropna(subset=["latitude", "longitude"])

    # Clean and standardize text fields so values are treated consistently
    df["name"] = df["name"].fillna("Unknown").str.strip().str.title()
    df["host_name"] = df["host_name"].fillna("Unknown").str.strip().str.title()
    df["neighbourhood"] = df["neighbourhood"].fillna("Unknown").str.strip().str.title()
    df["neighbourhood_group"] = df["neighbourhood_group"].fillna("Unknown").str.strip().str.title()
    df["room_type"] = df["room_type"].fillna("Unknown").str.strip().str.title()

    # Convert last_review to datetime / invalid values become NaT so they are stored as NULL in SQL
    df["last_review"] = pd.to_datetime(df["last_review"], errors="coerce")

    # Replace missing review counts with 0
    df["reviews_per_month"] = df["reviews_per_month"].fillna(0)

    # Remove duplicate rows to avoid insert issues
    df = df.drop_duplicates()

    return df

# Execute cleaning and validate row count
cleaned_df = get_cleaned_df("Desktop/Airbnb Project/AB_NYC_2019.csv")
print(cleaned_df.shape)