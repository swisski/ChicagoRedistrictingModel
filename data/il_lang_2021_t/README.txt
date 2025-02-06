Illinois 2021 Select Language Data from the American Community Survey (2017-2021) at the Census Tract level

##Redistricting Data Hub (RDH) Retrieval Date
06/01/23

##Sources
ACS data retrieved using the Census API: https://api.census.gov/data/2021/acs/acs5
Boundary shapefile retrieved from the Census Cartographic Boundary File website: https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.2021.html

##Fields
Field Name Description                                                                   
GEOID      Unique Geographic Identifier                                                  
STATEFP    State FIPS                                                                    
STATE      State Name                                                                    
COUNTYFP   County FIPS                                                                   
COUNTY     County Name                                                                   
TOT_POP21  Total population (B06007_001E)                                                
ENG_ONLY21 Speak only English population (B06007_002E)                                   
SPANISH21  Speak Spanish total population (B06007_003E)                                  
SP_EN_VW21 Speak Spanish and speak English "very well" population (B06007_004E)          
SP_EN_LW21 Speak Spanish and speak English less than "very well" population (B06007_005E)
OTH_LANG21 Speak other languages total population (B06007_006E)                          
OT_EN_VW21 Speak other languages and speak English "very well" (B06007_007E)             
OT_EN_LW21 Speak other languages and speak English less than "very well" (B06007_008E)   

##Processing
ACS data for Illinois was retrieved with a Python script from the Census API.
The census tract data is available by county for all counties in Illinois. The script extracted the data for all counties in Illinois. 
Each field represents an estimate from the Census for a particular variable, as noted in the Fields section above.
The data were then merged on the GEOID with a corresponding TIGER shapefile.

##Additional Notes
For any questions about this dataset or if you would like additional related ACS data, please email info@redistrictingdatahub.org.