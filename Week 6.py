import pandas as pd
import os
import geopandas as gpd
from shapely.geometry import Point


# From the handbook, we are to create a few metrics
# Price Ratio (ClosePrice/OriginalListPrice)
# Price Per SF (ClosePrice/LivingArea)
# Days on Market (DaysOnMarket)
# Year/Month/YrMo (from CloseDate)
# Close to Original Ratio (ClosePrice/OriginalListPrice)
# Listing to Contract Days (PurchaseContractDate - ListingContractDate)
# Contract to Close Days (CloseDate - PurchaseContractDate)

# all will have different purposes as outlined below

# First, we bring in the cleaned datasets from last week

sold_file = pd.read_csv("sold_new.csv", low_memory = False)
listings_file = pd.read_csv("listings_new.csv", low_memory = False)

# Being in a CSV loses the date/time that we converted to
# the previous weeks, so we have to redo this

dates = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate']
for col in dates:
    if col in sold_file.columns:
        sold_file[col] = pd.to_datetime(sold_file[col], errors = 'coerce')

# First metrics is the price ratio
# This measures negotiation strength

sold_file['price_ratio'] = sold_file['ClosePrice'] / sold_file['OriginalListPrice']

# Next up is price per SF
# This normalizes price across sizes

sold_file['price_per_sf'] = sold_file['ClosePrice'] / sold_file['LivingArea']

# Next is Days on Market
# This is an indicator of the time to sell
# But this is already done for us

sold_file['days_on_market'] = sold_file['DaysOnMarket']

# Next is the Year and the Month
# This allows us to do time series analysis

sold_file['year'] = sold_file['CloseDate'].dt.year
sold_file['month'] = sold_file['CloseDate'].dt.month
sold_file['yr_mo'] = sold_file['CloseDate'].dt.to_period('M')

# Next is the Listing to Contract Days
# This allows us to measure the time from listing
# to the time of the accepted offer

sold_file['listing_to_contract_days'] = (
    sold_file['PurchaseContractDate'] - sold_file['ListingContractDate']
).dt.days

# Finally we have Contract to Close Days
# This allows us to find the escrow and closing period duration

sold_file['contract_to_close_days'] = (
    sold_file['CloseDate'] - sold_file['PurchaseContractDate']
).dt.days

# Print the output to double check

print(sold_file[[
    'ClosePrice', 'OriginalListPrice', 'price_ratio',
    'price_per_sf', 'year', 'month', 'yr_mo',
    'listing_to_contract_days', 'contract_to_close_days'
]])

# Next, we will need to download geopandas for the
# data on the school districts

# Here is the plan for the updated data

# After creating your engineered metrics, group the analysis by key dimensions to uncover market patterns.
# Generate summary statistics for each segment:
# PropertyType and PropertySubType
# CountyOrParish and MLSAreaMajor
# ListOfficeName and BuyerOfficeName (for competitive intelligence)

# We pick back up and work on the school district join
# Every property has a lat/long to give us coordinates
# We can fidn a school district for each if we look hard enough

school_districts = gpd.read_file('DistrictAreas2425/DistrictAreas2425.shp')

# There are too many rows (not all have coordinates)
# So we will drop extraneous ones

sold_geo = sold_file.dropna(
    subset = ['Latitude', 'Longitude']
                            ).copy()

# We can turn the lat/long into a column at this point

sold_geo['geometry'] = sold_geo.apply(
    lambda row: Point(row['Longitude'], row ['Latitude']), axis = 1
)

# Next, we convert this to geodf
# and we can make a coordinate system

sold_geo = gpd.GeoDataFrame(sold_geo, geometry = 'geometry', crs = 'EPSG:4326')
districts = school_districts.to_crs('EPSG:4326')

# We want to match each property with the school district
# that its coordinates correspond to

sold_with_districts = gpd.sjoin(
    sold_geo, districts[['DistrictNa', 'geometry']], how='left', predicate='within'
    )

# Time to rename the columns 

sold_with_districts = sold_with_districts.rename(columns={'DistrictNa': 'school_district'})

# We can now merge back to the old columns

sold_file = sold_file.merge(
    sold_with_districts[['ListingKey', 'school_district']],
    on='ListingKey',
    how='left'
)

print(f"\nsold_file has {len(sold_file):,} rows and school_district column added")
sold_file.to_csv('sold_new.csv', index=False)
