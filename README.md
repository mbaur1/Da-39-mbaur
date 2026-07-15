# DA-39-mbaur

Will be adding for for IDX Exchange (Summer 2026)


Week 1 Summary:

Combined monthly MLS files spanning from January 2024 to April 2026 into two clean datasets (sold and listings), filtered everything down to residential properties, and checked that the row counts made sense throughout the process.

Week 2 Summary:

Dug into the data to understand  data, got rid of 17 columns with a high amount of missing contents (>90% missing), and analyzed the distributions of key metrics such as price, living area, and days on market to spot any outliers.

Created boxplots and histograms for key metrics such as: 

ClosePrice, ListPrice, OriginalListPrice, LivingArea, LotSizeAcres, BedroomsTotal, BathroomsTotalInteger, DaysOnMarket, and YearBuilt

Week 3:

Pulled in national mortgage rate data from the Federal Reserve, converted it from weekly to monthly averages, and joined it onto both datasets to visualize how rates aligned with listing and sale activity.

