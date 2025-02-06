2020 Census Redistricting Data (P.L. 94-171) Census Tract Shapefile for Illinois

##Redistricting Data Hub (RDH) Retrieval Date
02/25/2021

##Sources
Shapefiles for the 2020 Census Redistricting Data (P.L. 94-171) are available for download from https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
The Illinois Census Tract file direct download URL is https://www2.census.gov/geo/tiger/TIGER2020PL/LAYER/TRACT/2020/tl_2020_17_tract20.zip

##Fields
    Field Name                                                                                                                                                                   Description
0    STATEFP20                                                                                                                                                   2020 Census state FIPS code
1   COUNTYFP20                                                                                                                                                  2020 Census county FIPS code
2    TRACTCE20                                                                                                                                                        2020 Census tract code
3      GEOID20                                                              Census tract identifier; a concatenation of 2020 Census state FIPS code, county FIPS code, and census tract code
4       NAME20  2020 Census tract name, this is the census tract code converted to an integer or integer plus 2-character decimal if the last two characters of the code are not both zeros.
5   NAMELSAD20                                                                                           2020 Census translated legal/statistical area description and the census tract name
6      MTFCC20                                                                                                                                          MAF/TIGER feature class code (G5020)
7   FUNCSTAT20                                                                                                                                                 2020 Census functional status
8      ALAND20                                                                                                                                                         2020 Census land area
9     AWATER20                                                                                                                                                        2020 Census water area
10  INTPTLAT20                                                                                                                                    2020 Census latitude of the internal point
11  INTPTLON20                                                                                                                                   2020 Census longitude of the internal point

##Processing
The shapefile was retrieved from the download link (see sources above) and was renamed using RDH conventions with a python script.

##Additional Notes
For more information on the Decennial Census P.L. 94-171 Redistricting Data visit https://www.census.gov/programs-surveys/decennial-census/about/rdo/summary-files.html#P1
Please direct questions related to processing this dataset to info@redistrictingdatahub.org.