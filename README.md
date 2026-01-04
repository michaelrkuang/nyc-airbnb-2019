# NYC Airbnb 2019 Listings - End-to-End Data Analysis (Python, MySQL, Tableau)

## An end-to-end analysis of the NYC Airbnb 2019 listings (`AB_NYC_2019.csv`): cleaned and profiled data in Python (Pandas), modeled it in MySQL (staging + window-function analytics view), then exported to Tableau for interactive dashboards.   

**Workflow:** EDA/cleaning using Python Pandas -> MySQL staging + analytics view -> export for Tableau -> Tableau data visualization

**Tech stack:** Python (Pandas + Matplotlib), MySQL (SQL + window functions), Tableau Public

## Tableau Dashboards (Tableau Public): 
- https://public.tableau.com/app/profile/michael.kuang/viz/AirbnbNYC2019-ListingsAnalysis/NYCAirbnbMarketOverview

**Author:** Michael Kuang

**LinkedIn:** https://www.linkedin.com/in/michael-kuang/

**Email:** michaelk8040@gmail.com

## Key insights:
- The market is highly concentrated: Manhatten (19,589, 44.1%) and Brooklyn (18,482, 41.6%) make up ~85.8% of all listings (44,398 total) with Queens a distant third (5,095, 11.5%).
- Median nightly price by borough: Manhattan $140, Brooklyn $95, Staten Island $80, Queens $79, Bronx $75.
- Benchmark-based pricing shows premiums/discounts: Median premium vs the citywide room-type benchmark is ~+8% in Manhatten, while other boroughs skew discounts (Brooklyn ~-22%, Queens/Bronx ~-27%, Staten Island ~-29%).
- Premiums are geographically clustered: Higher premium listings concentrate in southwest Manhatten and northwest Brooklyn based on the blue regions on the dot distribution map, while many outer-borough areas are discounted.
- There is a direct coorelation between the nightly price and reviews per month. Based on the nightly price vs reviews per month scatter plot diagram with trendline, listings with lower prices tend to have more reviews per month. 

# Repository Contents

### 1) eda_exploration.ipynb
Exploration analysis + documented observations/actions
### 2) data_clean.py
Clean the raw csv file containing the ~49K NYC 2019 Airbnb listings
### 3) load_to_mysql.py
Load cleaned data into MySQL staging table
### 4) airbnb.sql
MySQL schema + creation of analytics view using window functions
### 5) export_for_tableau.py
Export analytics view to CSV for Tableau
### 6) Airbnb NYC 2019 - Listings Analysis.twb
Create data visualizations using cleaned listing data

# Dataset

- Source: Kaggle - New York City Airbnb Open Data (2019)
> The raw CSV is not included in this repository, please download from Kaggle before running the pipeline.

# Project Workflow

## 1) Exploratory Data Analysis (EDA)
Notebook: `eda_exploration.ipynb`

The EDA notebook analyzes the dataset is the following aspects, influencing data cleansing and data visualization in the later steps:
1. dataset structure
2. data quality checks
3. distributions & outliers (e.g. `price`, `minimum_nights`)
4. segment breakdowns

## 2) Cleaning & Formatting
Script: `data_clean.py`

The get_cleaned_df() function supports with the following:
- Added logic guard rails to exclude rows with erroneous data (e.g. listings with minimum nights of > 365)
- Dropped listings with incomplete coordinates
- Handled null values and standardizing text fields such as host name and neighbourhood
- Converted data types to to allow for import to MySQL database

## 3) Loading cleaned data into MySQL (staging)
Script: `load_to_mysql.py`
Schema + view: `airbnb.sql`

Loaded the cleaned dataset into MySQL to create a reusable analytics layer. SQL allows me to standardize transformations, build window-function metrics, and keep business logic version controlled and reproducible across tools.

- `airbnb.sql` defines the staging table `listings_staging`.
- `load_to_mysql.py` reads the raw CSV `data/AB_NYC_2019.csv`, applies `get_cleaned_df()`, then inserts the cleaned records into `listings_staging` using Mysql.connector.

## 4) Analytics view for Tableau
SQL view: `listings_data` (created in `airbnb.sql`)

- Created new metrics via window functions including avg_price_group_roomtype that groups listings by each borough + room type combination and computes the average nightly price for each bucket.
- Applied final filters to remove outliers such as only selecting listings with nightly prices between $40 (5th percentile) and $355 (95th percentile) for the view

## 5) Tableau data visualization dashboards
File: Airbnb NYC 2019 - Listings Analysis.twb
- Built the BI dashboards by creating calculated measures such as `City Avg Price per Room Type` (aggregate), `Median Nightly Price` (aggregate), and `More Expensive Listings` (count based on string validation) using Tableau calculations.
- These dashboards provide a high level overview of the NYC Airbnb listings data including market composition, pricing vs demand signals, listing premiums vs market benchmarks, and listing-level details.
> Tableau Note: In a production setup, I would create a direct connection between the mySQL database and Tableau for a live data source. Tableau Public only supports file-based sources (e.g. CSV). For that reason, the project exports 'listings_data' to 'listings_tableau.csv' for Tableau import.

# Dashboards Created:

## - `Dashboard 1: NYC Airbnb Market Overview`
![NYC Airbnb Market Overview](images/NYC%20Airbnb%20Market%20Overview.png)
- Provides high-level overview of the NYC Airbnb market in 2019, summarizing market supply and pricing by borough. It visualizes (1) distribution of room types, (2) listings by borough, (3) median nightly price by borough, and (4) a color-coded map by borough zones, providing insight on listing concentration and pricing differences. 

## - `Dashboard 2: Pricing & Demand Signals`
![Pricing & Demand Signals](images/Pricing%20&%20Demand%20Signals.png)
- Showcases (1) the correlation between price and reviews per month (signals demand), (2) compares median prices per room type for the selected borough, and (3) the top 5 neighbourhoods by average availability within each Borough. It helps potential areas to stay by combining typical price levels with how frequently listings are available (days available out of 365).

## - `Dashboard 3: Price Premiums vs Room-Type Benchmarks`
![Price Premiums vs Room-Type Benchmarks](images/Price%20Premiums%20vs%20Room-Type%20Benchmarks.png)
- Analyzes price premiums/discounts relative to a citywide room-type benchmark for NYC Airbnb listings (2019). It visualises (1) the distribution of price premiums to show how listings deviate from the benchmark, (2) median price premium by borough to compare typical over/underpricing across boroughs, and (3) a map of price premiums by listing location to highlight where higher or lower pricing tends to cluster (orange = below city benchmark | blue = above city benchmark).

## - `Dashboard 4: Listing Explorer: Price vs Room-Type Benchmark`
![Listings Explorer](images/Listings%20Explorer.png)
-  Provides an interactive listing browser that lets users explore individual Airbnb listings and compare each listing's price to the citywide average for its room type (shows a calculated premium/discount). Users can filter by borough group, room type, reviews per month, and premium category (more expensive, near market, or cheaper). There is also a summary panel that counts listings by premium category which updates based on the selected parameters.

# How to run the pipeline

### 1) Create a database in MySQL
- Run `airbnb.sql` to create `listings_staging` table and `listings_data` view.
### 2) Load cleaned data into MySQL
- Run `load_to_mysql.py` file to insert the rows into `listings_staging`.
### 3) Export the analytics view
- Run `export_for_tableau.py` to create the `listings_tableau.csv` file which will be imported to Tableau public. If using Tableau Desktop, a direct connection can be made between the Mysql server and Tableau.
### 4) Build Tableau dashboards
- In Tableau Public: Connect -> Text file -> select `listings_tableau.csv` to start creating visuals using fields from `listings_tableau.csv`. Use geography (e.g. neighbourhood group, latitude/longitude), availability, and review counts alongside price to create calculated measures and identify patterns and trends.