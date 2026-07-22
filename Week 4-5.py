import pandas as pd
import os

# we start this by taking the datasets that we built last week
sold_file = pd.read_csv("sold_with_mortgage_rates.csv", low_memory = False)
listings_file = pd.read_csv("listings_with_mortgage_rates.csv", low_memory = False)


# First, we take note of the current length of both the 
# sold and the listings in their original form
sold_rows = len(sold_file)
listings_rows = len(listings_file)

print(f"Starting rows (sold): {sold_rows}")
print(f"Starting rows (listings): {listings_rows}")

# After noting our starting position, we can just make the date fields

# Our first task is to do this: Convert date fields to datetime format 
# (CloseDate, PurchaseContractDate, ListingContractDate, ContractStatusChangeDate)

date_fields = [
    'CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate'
]

# We then want to check what we currently have and make sure that
# if the columns we are looking for are in the dataset, then we will
# successfully change them to the date and time format we want
for col in date_fields:
    if col in sold_file.columns:
        sold_file[col] = pd.to_datetime(sold_file[col], errors = 'coerce')
    if col in listings_file.columns:
        listings_file[col] = pd.to_datetime(listings_file[col], errors = 'coerce')

print(f"After conversion:")

# We can now print the data type of the resulting columns
# We do this to check our work and make sure that our process works
# as intended (print to double check)
for col in date_fields:
    if col in sold_file.columns:
        print(f"Sold_file.{col}: {sold_file[col].dtype}")
    if col in listings_file.columns:
        print(f"Listings_file.{col}: {listings_file[col].dtype}")

# By putting the information in the datetime format, we can now
# compare two different dates because they are registered under
# date/time instead of being input as just values

# Before proceeding, I wanted a list of which columns were a part of each
print("SOLD columns:")
print(sold_file.columns.tolist())

print("\nLISTINGS columns:")
print(listings_file.columns.tolist())

# I ran the code from weeks 2-3 and cross referenced the output
# that I got here with the columns that had greater than 90% of
# its data missing from the report back in week 2
# Here are the columns that appeared in both: FireplacesTotal', 'AboveGradeFinishedArea', 'TaxAnnualAmount', 'BuilderName',
#    'TaxYear', 'BuildingAreaTotal', 'ElementarySchoolDistrict', 'CoBuyerAgentFirstName',
#   'BelowGradeFinishedArea', 'BusinessType', 'CoveredSpaces', 'LotSizeDimensions',
#    'MiddleOrJuniorSchoolDistrict'

# so we can go ahead and do this

missing_in_listings  = [
    'FireplacesTotal', 'AboveGradeFinishedArea', 'TaxAnnualAmount', 'BuilderName',
    'TaxYear', 'BuildingAreaTotal', 'ElementarySchoolDistrict', 'CoBuyerAgentFirstName',
    'BelowGradeFinishedArea', 'BusinessType', 'CoveredSpaces', 'LotSizeDimensions',
    'MiddleOrJuniorSchoolDistrict'
]

# I also noticed that there were a bunch of duplicate columns as well
# particularly these ones: 'PropertyType.1', 'DaysOnMarket.1', 'LivingArea.1', 'Longitude.1', 'Latitude.1',
#   'ListPrice.1', 'CloseDate.1', 'BuyerOfficeName.1', 'UnparsedAddress.1',
#    'ListAgentFirstName.1', 'ListAgentLastName.1'

# we can take care of those as well by doing this

repeated_columns = [
    'PropertyType.1', 'DaysOnMarket.1', 'LivingArea.1', 'Longitude.1', 'Latitude.1',
    'ListPrice.1', 'CloseDate.1', 'BuyerOfficeName.1', 'UnparsedAddress.1',
    'ListAgentFirstName.1', 'ListAgentLastName.1'
]

drop_from_listings = missing_in_listings + repeated_columns

# if listings contains these columns, then we are to drop them
listings_file.drop(columns = [c for c in drop_from_listings if c in listings_file.columns], inplace = True)

print(f"Listings columns post drop: {len(listings_file.columns)}")
# The sold columns looked alright
print(f"Sold columns: {len(sold_file.columns)}")
