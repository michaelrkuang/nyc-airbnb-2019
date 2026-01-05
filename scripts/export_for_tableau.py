"""
Export Airbnb listing data from MySQL to a CSV file for Tableau analysis
"""

import os
os.chdir("/Users/michaelkuang/Desktop/Airbnb Project")
import pandas as pd
import mysql.connector

# Creating the connection to the local MySQL database
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="DataAnalysis123",
    database="airbnb_nyc"
)

# Query listings data from MySQL into DataFrame, preview the results, and export the data into a CSV file for Tableau analysis
df_core = pd.read_sql("SELECT * FROM listings_data", conn)
print(df_core)
df_core.to_csv("listings_tableau.csv", index=False)