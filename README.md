# Author: Michael Kuang
# Contact Info: michaelk8040@gmail.com | https://www.linkedin.com/in/michael-kuang/
# NYC Airbnb 2019 Listings - End-to_End Data Analysis (Python, MySQL, Tableau)

An end-to-end analysis of the NYC Airbnb 2019 listings dataset (`AB_NYC_2019.csv`) using:

EDA/cleaning using Python Pandas -> MySQL staging + analytics view -> export for Tableau -> Tableau data visualization

Tableau Dashboards (Tableau Public):
https://public.tableau.com/app/profile/michael.kuang/viz/AirbnbNYC2019-ListingsAnalysis/NYCAirbnbMarketOverview

Tableau Dashboards (Screenshots):
![NYC Airbnb Market Overview](images/NYC%20Airbnb%20Market%20Overview.png)
![Pricing & Demand Signals](images/Pricing%20&%20Demand%20Signals.png)
![Price Premiums vs Room-Type Benchmarks](images/Price%20Premiums%20vs%20Room-Type%20Benchmarks.png)
![Listings Explorer](images/Listings%20Explorer.png)

# Repository contents

1) eda_exploration.ipynb
    - Exploration analysis + documented observations/actions
2) data_clean.py
    - Clearning the raw csv file containing the ~49K NYC 2019 Airbnb listings
3) load_to_mysql.py
    - Load cleaned data into MySQL staging table
4) airbnb.sql
    - MySQL schema + creation of analytics view using window functions
5) export_for_tableau.py
    - Export analytics view to CSV for Tableau
6) Airbnb NYC 2019 - Listings Analysis.twb
    - Creating data visualizations using cleaned listing data

# Dataset

- Source: Kaggle - New York City Airbnb Open Data (2019)
> The raw CSV is not included in this repository, please download from Kaggle before running the pipeline.

# Project workflow

1) Exploratory Data Analysis (EDA)
Notebook: `eda_exploration.ipynb`

The EDA notebook analyzes the dataset is the following aspects, influencing data cleansing and data visualization in the later steps:
- dataset structure
- data quality checks
- distributions & outliers (e.g. `price`, `minimum_nights`)
- segment breakdowns

2) Cleaning & Formatting
Script: `data_cleaning.py`

The get_cleaned_df() function supports with the following:
- Added logic guard rails to exclude rows with erroneous data (e.g. listings with minimum nights of > 365)
- Droped listings with incomplete coordinates
- Handled null values and standardizing text fields such as host name and neighbourhood
- Converted data types to to allow for import to MySQL databse

3) Loading cleaned data into MySQL (staging)
Script: `load_to_mysql.py`
Schema + view: `airbnb.sql`

Loaded the cleaned dataset into MySQL to create a reusable analytics layer. SQL allows me to standardize transformations, build window-function metrics, and keep business logic version controlled and reproducible across tools.

- `airbnb.sql` defines the staging table `listings_staging`.
- `load_to_mysql.py` reads the raw CSV `data/AB_NYC_2019.csv`, applies `get_cleaned_df()`, then inserts the cleaned records into `listings_staging` using mysql.connector.

4) Analytics view for Tableau
SQL view: `listings_data` (created in `airbnb.sql`)

- Created new metrics via window function
- Applied final filters to remove outliers such as only selecting listings with nightly prices between $40 (5th percentile) and $355 (95th percentile) for the view

# Tableau note: In a production setup I would create a direct connection between the mySQL database and Tableau for a live data source Tableau Public only supports file-based sources (e.g. CSV). For that reason, the project exports 'listings_data' to 'listings_tableau.csv' for Tableau import.

5) Tableau data visualization dashboards
File: Airbnb NYC 2019 - Listings Analysis.twb
> To create the BI dashboards, I created calculated measures such as `City Avg Price per Room Type` and ``
> These dashboards provide a high level overview of the NYC Airbnb listings data including market composition, pricing vs demand signals, listing premiums vs market benchmarks, and listing-level details.

Dashboards included:

- `Dashboard 1 - NYC Airbnb Market Overview`
![NYC Airbnb Market Overview](images/NYC%20Airbnb%20Market%20Overview.png)
    - Provides high-level overview of the NYC Airbnb market in 2019, summarizing market supply and pricing by borough. It visualizes (1) distribution of room types, (2) listings by borough, (3) median nightly price by borough, and (4) a color-coded map by borough zones, providing insight on listing concentration and pricing differences. 

- `Dashboard 2 - Pricing & Demand Signals`
![Pricing & Demand Signals](images/Pricing%20&%20Demand%20Signals.png)
    - Showcases (1) the correlation between price and reviews per month (signals demand), (2) compares median prices per room type for the selected borough, and (3) the top 5 neighbourhoods by average availability within each Borough. It helps potential areas to stay by combining typical price levels with how frequently listings are available (days available out of 365).

- `Dashboard 3 - Price Premiums vs Room-Type Benchmarks`
![Price Premiums vs Room-Type Benchmarks](images/Price%20Premiums%20vs%20Room-Type%20Benchmarks.png)
    - Analyzes price premiums/discounts relative to a citywide room-type benchmark for NYC Airbnb listings (2019). It visualises (1) the distribution of price premiums to show how listings deviate from the benchmark, (2) median price premium by borough to compare typical over/underpricing across boroughs, and (3) a map of price premiums by listing location to highlight where higher or lower pricing tends to cluster (orange = below city benchmark | blue = above city benchmark).

- `Dashboard 4 - Listing Explorer: Price vs Room-Type Benchmark`
![Listings Explorer](images/Listings%20Explorer.png)
    -  Provides an interactive listing browser that lets users explore individual Airbnb listings and compare each listings's price to the citywide average for its room type (shows a calculated premium/discount). Users can filter by borough group, room type, reviews per month, and premium category (more expensive, near market, or cheaper). There is also a summary panel that counts listings by premium category which updates based on the selected parameters.

# How to run the pipeline

1) Create a database in MYSQL
- Run `airbnb.sql` to create `listings_staging` table and `listings_data` view.

2) Load cleaned data into MySQL
- Run `load_to_mysql.py` file to insert the rows into `listings_staging`.

3) Export the analytics view
- Run `export_for_tableau.py` to create the `listings_tableau.csv` file which will be imported to Tableau public. If using Tableau Desktop, a direct connection can be made between the Mysql server and Tableau.

4) Tableau dashboards
- In Tableau Public: Connect -> Text file -> select `listings_tableau.csv` to start creating visuals using fields from `listings_tableau.csv`.
