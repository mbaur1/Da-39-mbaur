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

# In the meantime, I fixed the issues that spilled over from Weeks 2-3

# Now its time to see what we will do with the missing values

# Here are the metrics that come in a yes/no answer

boolean_metrics = [
    'WaterfrontYN', 'BasementYN', 'PoolPrivateYN', 'ViewYN', 'FireplaceYN',
    'NewConstructionYN', 'AttachedGarageYN'
]

# for these, we will enter "no" if not available

for col in boolean_metrics:
    if col in sold_file.columns:
        sold_file[col] = sold_file[col].fillna('N')
    if col in listings_file.columns:
        listings_file[col] = listings_file[col].fillna('N')

# After we have done this for the boolean metrics, we can do so for
# the categorical metrics

categorical_metrics = [
    'City', 'CountyOrParish', 'PropertyType', 'PropertySubType',
    'ListOfficeName', 'BuyerOfficeName', 'MLSAreaMajor', 'SubdivisionName'
]

# We can do the same process with these
# Copy the old code, but instead of "N" we can
# just say "N/A" for not applicable

for col in categorical_metrics:
    if col in sold_file.columns:
        sold_file[col] = sold_file[col].fillna('N/A')
    if col in listings_file.columns:
        listings_file[col] = listings_file[col].fillna('N/A')

# Next step is to make sure that all numeric metrics are typed properly
# It is possible that they are read as strings (meant as numbers)

numeric_metrics = [
    'ClosePrice', 'LivingArea', 'DaysOnMarket', 'BedroomsTotal',
    'BathroomsTotalInteger,' 'ListPrice', 'OriginalListPrice'
]

# We can use the same conditionals as before, just with a little switch
# In the nested portion, we will just override the system and switch it manually to a number

for col in categorical_metrics:
    if col in sold_file.columns:
        sold_file[col] = pd.to_numeric(sold_file[col], errors = 'coerce')
    if col in listings_file.columns:
        listings_file[col] = pd.to_numeric(listings_file[col], errors = 'coerce')

# Once this is finished, we can remove numbers that are impossible to get
# For example, a close price/living area/day on market cannot be less than 0,
# So we will eliminate the chance that these metrics are negative in any way

# The following are the metrics that need to be greater than 0

sold_file = sold_file[
    (sold_file['ClosePrice'] > 0) &
    (sold_file['LivingArea'] > 0) &
    (sold_file['DaysOnMarket'] >= 0) &
    (sold_file['BedroomsTotal'] >= 0) &
    (sold_file['BathroomsTotalInteger'] >= 0)
]

# We can repeat the above for the listings files

listings_file = listings_file[
    (listings_file['ListPrice'] > 0) &
    (listings_file['LivingArea'] > 0) &
    (listings_file['DaysOnMarket'] >= 0) &
    (listings_file['BedroomsTotal'] >= 0) &
    (listings_file['BathroomsTotalInteger'] >= 0)
]

# Now as a check, we can print the total number of rows for each

print(f"Sold rows left: {len(sold_file):,}")
print(f"Listings rows left: {len(listings_file):,}")
