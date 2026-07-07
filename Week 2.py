import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns

# To do's as comments throughout

sold = pd.read_csv('sold_combined.csv')

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

# Now look at the list we created and remove these columns
to_remove = high_missing_columns(sold, amount = 90)
print(f"Columns >90% missing: {to_remove}")

# Now we drop the columns
sold = sold.drop(columns = to_remove.index)

# This is our output
print(f"New table: {sold.shape}")

# Separate market analysis fields from metadata fields

# Calculate missing counts/percentages per column

# Decide which columns to drop/retain

# Analyze the following: ClosePrice, ListPrice, OriginalListPrice,
# LivingArea, LotSizeAcres, BedroomsTotal, BathroomsTotalInteger,
# DaysOnMarket, YearBuilt

# For each of above, make histograms, boxplots, percentile summaries
# Find outliers for each (for later use)

## From the handbook

# # Inspect structure
sold.columns
sold.head()
# Check property categories

sold['PropertyType'].unique()

# Filter residential

sold = sold[sold.PropertyType == 'Residential']

# Validate completeness

sold.isnull().sum()