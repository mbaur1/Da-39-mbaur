import pandas as pd

# Some months are filled so we note them here
filled_months = [202405, 202406, 202407, 202501]

# Create an empty list
sold = []
for month in range(202401, 202606):
    if month in filled_months:
        file_name = f'CRMLSSold{month}_filled.csv'
    else:
        file_name = f'CRMLSSold{month}.csv'
    # We only have months 1-12, so numbers outside this within this range
    # we want to just pass on
    try:
        sold.append(pd.read_csv(file_name, low_memory=False))
    except FileNotFoundError:
        pass

# Concatenate the original list
sold_final = pd.concat(sold)

listings = []
for month in range(202401, 202606):
    file_name = f'CRMLSListing{month}.csv'
    try:
        listings.append(pd.read_csv(file_name, low_memory=False))
    except FileNotFoundError:
        pass

listings_final = pd.concat(listings)

# Now we are done with the first part and we have the concatenated lists

# We first want to count what the final counts are 
# before we filter out non residential listings
print(f"Sold rows before filter: {len(sold_final)}")
print(f"Listings rows before filter: {len(listings_final)}")

# Now we actually filter the listings to only residential properties
sold_final = sold_final[sold_final['PropertyType'] == 'Residential']
listings_final = listings_final[listings_final['PropertyType'] == 'Residential']

# We now count the number of rows after filtering
print(f"Sold rows after filter: {len(sold_final)}")
print(f"Listings rows after filter: {len(listings_final)}")

# We can now save the new datasets as new csvs
sold_final.to_csv('sold_combined.csv', index=False)
listings_final.to_csv('listings_combined.csv', index=False)

# I ran this code at got the following result
# Sold rows before filter: 639914
# Listings rows before filter: 929822
# Sold rows after filter: 430445
# Listings rows after filter: 591647

# It looks like we filtered out nearly a third of the 
# listings and sold properties during the span by just 
# filtering and counting the residential properties