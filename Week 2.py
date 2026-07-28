import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns

# To do's as comments throughout

sold = pd.read_csv('sold_combined.csv')
listings = pd.read_csv('listings_combined.csv')

# Identify number of rows/columns

column_num = sold.columns
row_num = len(sold)

print(f"Number of Rows: {row_num}")
print(f"Number of Columns: {len(column_num)}")

# Review column data types

print(sold.dtypes)

# Identify high missing columns

print(sold.head(10))

def high_missing_columns(df, amount = 90):
    # We want to eliminate columns with >90% missing columns
    missing_percent = (df.isnull().sum() / len(df)) * 100
    # We filter by checking if missing > 90%
    qualified = missing_percent[missing_percent > amount]
    return qualified

# There are some columns that we will want to keep no matter what
to_keep = [
    'ClosePrice', 'ListPrice', 'OriginalListPrice', 'LivingArea', 'LotSizeAcres',
    'BedroomsTotal', 'BathroomsTotalInteger', 'DaysOnMarket', 'YearBuilt',
    'City', 'CountyOrParish', 'PostalCode', 'PropertyType', 'PropertySubType',
    'ListOfficeName', 'BuyerOfficeName', 'ListAgentFullName', 'BuyerAgentFirstName',
    'BuyerAgentLastName', 'CloseDate', 'ListingContractDate', 'PurchaseContractDate',
    'WaterfrontYN', 'BasementYN', 'PoolPrivateYN', 'ViewYN'
]
# Now look at the list we created and remove these columns
should_remove = high_missing_columns(sold, amount = 90)
# Now just remove the ones that don't overlap
to_remove = [col for col in should_remove.index if col not in to_keep]
print(f"Columns >90% missing: {should_remove}")

# Now we drop the columns
sold = sold.drop(columns = to_remove)

# This is our output
print(f"New table: {sold.shape}")

# Lets track the missing values for the columns that we keep

print("Missing Values")
missing_values = pd.DataFrame({
    'Column': sold.columns,
    'MissingCount': sold.isnull().sum(),
    'MissingPct': (sold.isnull().sum() / len(sold)) * 100
})
missing_values = missing_values[missing_values['MissingCount'] > 0].sort_values('MissingPct')
print(missing_values)

# We see that some columns have almost all the values and some are missing
# a significant amount, but we are keeping columns that have at least 
# 10% of values available

# Analyze the following: ClosePrice, ListPrice, OriginalListPrice,
# LivingArea, LotSizeAcres, BedroomsTotal, BathroomsTotalInteger,
# DaysOnMarket, YearBuilt

important_columns = ['ClosePrice', 'ListPrice', 'OriginalListPrice', 'LivingArea', 'LotSizeAcres', 'BedroomsTotal', 'BathroomsTotalInteger', 'DaysOnMarket', 'YearBuilt']

for column in important_columns:
    if column in sold.columns:
        print(f"{column}")
        # Describe will give us min/max/quartiles/std/mean
        print(sold[column].describe())

        # We can first make a histogram
        plt.figure()
        plt.hist(sold[column].dropna(), bins = 25, edgecolor = 'black')
        plt.title(f'{column} Distribution')
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.savefig(f'{column}_hist.png')
        plt.close()

        # Next a boxplot
        plt.figure()
        sns.boxplot(y = sold[column])
        plt.title(f'{column} Boxplot')
        plt.savefig(f'{column}_boxplot.png')
        plt.close()

        # Lastly, we calculate the IQR for outliers
        q1 = sold[column].quantile(.25)
        q3 = sold[column].quantile(.75)
        iqr = q3 - q1
        # we take our lower/upper bounds for valid inputs
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        # if anything isn't in this region, we can 
        # mark it as a statistical outlier
        outliers = sold[(sold[column] < lower_bound) | (sold[column] > upper_bound)]
        print(f'Lower bound: {lower_bound}')
        print(f'Upper bound: {upper_bound}')
    
print("Histograms and boxplots complete")

# Finally we can save this to a new csv

sold.to_csv('sold_week2.csv', index = False)

# This gets the mortgage data from fred
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates = ['observation_date'])
# We only take the columns that we want to use
mortgage.columns = ['date', 'rate_30yr_fixed']

# We now want to get the monthly average
mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = (
    mortgage.groupby('year_month')['rate_30yr_fixed']
    .mean()
    .reset_index()
)

# We now make a matching year_month key on the current dataset
sold['year_month'] = pd.to_datetime(sold['CloseDate']).dt.to_period('M')

listings['year_month'] = pd.to_datetime(
    listings['ListingContractDate']
).dt.to_period('M')

# Now we merge for both datasets
sold_with_rates = sold.merge(mortgage_monthly, on = 'year_month', how = 'left')
listings_with_rates = listings.merge(mortgage_monthly, on = 'year_month', how = 'left')

# Print everything to ensure that we get the desired results

sold_nulls = sold_with_rates['rate_30yr_fixed'].isnull().sum()
listings_nulls = listings_with_rates['rate_30yr_fixed'].isnull().sum()

# Only print if there is a null
if sold_nulls > 0:
    print(sold_nulls)

if listings_nulls > 0:
    print(listings_nulls)

# If none, then we did correctly and we can show that
if sold_nulls == 0 and listings_nulls == 0:
    print("Success")

print(
    sold_with_rates[
        ['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']
    ].head()
)

# Finally we can just save the data as a csv
sold_with_rates.to_csv('sold_with_mortgage_rates.csv', index = False)
listings_with_rates.to_csv('listings_with_mortgage_rates.csv', index = False)

print("Saved")

# Done with weeks 2-3