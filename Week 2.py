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
        plt.figure
        plt.hist(sold[column].dropna(), bins = 25, edgecolor = 'black')
        plt.title(f'{column} Distribution')
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.savefig(f'{column}_hist.png')
        plt.close()

        # Next a boxplot
        plt.figure
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