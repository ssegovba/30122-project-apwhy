# make sure to install these packages before running:
# pip install pandas
# pip install geopy

import pandas as pd
import geopandas as gpd
import numpy as np
import geopy
import json

DATA_PATH = "../raw_data/"

def clean_db(lat_lon_dict = True):
    """
    Creates a clean database with all the relevant variables from the different
    data sources employed.

    Input:
        lat_lon_dict (boolean): True (default) if there is already a dictionary 
            containing a mapping for zipcodes and lat-lon coordinates.
            False to generate that dictionary using helper function.

    Output:
        - A .csv file that is stored in the current folder
    """

    # Defining initial arguments:
    zip = {'zip_code': ['60601', '60602', '60603', '60604',
                        '60605', '60606', '60607', '60608',
                        '60609', '60610', '60611', '60612',
                        '60613', '60614', '60615', '60616',
                        '60617', '60618', '60619', '60620',
                        '60621', '60622', '60623', '60624',
                        '60625', '60626', '60628', '60629',
                        '60630', '60631', '60632', '60633',
                        '60634', '60636', '60637', '60638',
                        '60639', '60640', '60641', '60642',
                        '60643', '60644', '60645', '60646',
                        '60647', '60649', '60651', '60652',
                        '60653', '60654', '60655', '60656',
                        '60657', '60659', '60660', '60661',
                        '60707', '60827']} #Removed 60666 (O'Hare)
    zipcodes = pd.DataFrame(data = zip)

    # ZILLOW DATA:
    # Filter by year (2019) and zip codes of Chicago:
    rent_data = pd.read_csv(DATA_PATH + "zillow_data.csv")
    rent_data = rent_data[rent_data["State"]=="IL"]
    date_cols = rent_data.filter(like='20', axis=1)
    rent_data = rent_data.melt(id_vars=["RegionName","State"],value_vars=date_cols,
                var_name="Date",value_name="RentPrice")
    rent_data['RegionName'] = rent_data['RegionName'].astype("string")
    rent_data = rent_data.rename(columns={"RegionName":"zip_code"})
    rent_data["Date"] = pd.to_datetime(rent_data["Date"], format = "%Y-%m-%d")
    rent_data = rent_data[rent_data["Date"].dt.year == 2019]

    # Calculate the mean rent in a zipcode:
    rent_data = rent_data[rent_data["zip_code"].isin(zipcodes["zip_code"])]
    mean_rent = rent_data.groupby("zip_code")["RentPrice"].mean().reset_index()

    # ACS DATA:
    # Filter by zipcodes from Chicago:
    acs_data = pd.read_csv(DATA_PATH + "acs_data.csv")
    acs_data = acs_data.drop(columns=["Unnamed: 0"])
    acs_data['zip_code'] = acs_data['zip_code'].astype("string")
    acs_data = acs_data[acs_data["zip_code"].isin(zipcodes["zip_code"])]

    # EVICTIONS DATA:
    # Filter by year and select specific columns:
    evic_data = pd.read_csv(DATA_PATH + "eviction_data.csv")
    evic_data = evic_data[evic_data["filing_year"] == 2019]
    cols_to_keep = ["filing_year","tract","eviction_filings_completed","back_rent_0",
                    "back_rent_1_to_999","back_rent_1000_to_2499","back_rent_2500_to_4999",
                    "back_rent_5000_or_more","back_rent_median","eviction_order_yes"]
    evic_data = evic_data[cols_to_keep]

    # Load censustract and zipcode boundary to find zipcodes:
    zipcodes_gdf = gpd.read_file(DATA_PATH + 'bound_zip_codes.geojson')
    census_tracts_gdf = gpd.read_file(DATA_PATH + 'bound_census_tracts.geojson')
    merged_gdf = gpd.sjoin(census_tracts_gdf, zipcodes_gdf, how='inner', predicate='intersects')
    merged_gdf = merged_gdf.rename(columns={"zip":"zip_code"})

    # Convert the 'Geoid10' column to str to ensure join match:
    census_tracts_gdf['Geoid10'] = census_tracts_gdf['geoid10'].astype(str)
    evic_data['tract'] = evic_data['tract'].astype(str)
    evic_data = evic_data.rename(columns={'tract': 'geoid10'})

    evic_data = pd.merge(evic_data,census_tracts_gdf["geoid10"],how="inner")
    evic_data = pd.merge(evic_data,merged_gdf[["geoid10","zip_code"]],how="inner")
    evic_data = evic_data[evic_data["zip_code"].isin(zipcodes["zip_code"])]

    # Aggregate data by zipcode:
    back_rent_cols = list(filter(lambda x:'back_rent_' in x, list(evic_data.columns)))
    cols_aggregate = ["eviction_filings_completed"] + back_rent_cols[0:len(back_rent_cols)-1]
    num_evics = evic_data.groupby("zip_code")[cols_aggregate].count().reset_index()
    mean_back_rent = evic_data.groupby("zip_code")["back_rent_median"].mean().reset_index()
    num_evics = pd.merge(num_evics,mean_back_rent)

    # CRIME DATA:
    # Define types of crimes that are going to be aggregated by zip code:
    crime_data = pd.read_csv(DATA_PATH + "crime_data.csv")
    violent_crime = ["ASSAULT","BATTERY","ROBBERY","CRIM SEXUAL ASSAULT",
                    "CRIMINAL SEXUAL ASSAULT","SEX OFFENSE","INTIMIDATION","HOMICIDE",
                    "KIDNAPPING","HUMAN TRAFFICKING"]
    non_offensive = ["OTHER OFFENSE","NARCOTICS","WEAPONS VIOLATION","MOTOR VEHICLE THEFT",
                    "LIQUOR LAW VIOLATION","GAMBLING"]
    cols_to_keep = ['id', 'date', 'primary_type','latitude','longitude']
    crime_data = crime_data[cols_to_keep]
    crime_data = crime_data[crime_data["latitude"].isna() == False] #2042 registers without coordinates

    crime_data["crime"] = 1
    crime_data["violent_crime"] = np.where(crime_data["primary_type"].isin(violent_crime),1,0)
    crime_data["non_offensive_crime"] = np.where(crime_data["primary_type"].isin(non_offensive),1,0)

    #Map coordinates to zip code:
    if lat_lon_dict:
        with open(DATA_PATH + "lat_lon_dict.txt", "r") as fp:
            lat_lon_dict = json.load(fp)
    else:
        mapping_coord_zip(crime_data)
    
    crime_data["key"] = crime_data["latitude"].astype(str) + "/" + crime_data["longitude"].astype(str)
    crime_data["zip_code"] = crime_data["key"].map(lat_lon_dict)
    crime_data = crime_data[crime_data["zip_code"].isin(zipcodes["zip_code"])]
    crime_data = crime_data[~crime_data["zip_code"].isnull()]

    #Aggregation by zip code:
    cols_aggregate = ["crime","violent_crime","non_offensive_crime"]
    num_crimes = crime_data.groupby("zip_code")[cols_aggregate].count().reset_index()

    #MERGING DATA:
    merged_db = pd.merge(acs_data,mean_rent,on="zip_code",how="outer")
    merged_db = pd.merge(merged_db,num_evics,on="zip_code",how="outer")
    merged_db = pd.merge(merged_db,num_crimes,on="zip_code",how="outer")

    #Some zipcodes don't have rent data, so the median rent price is assigned to them:
    median_price = mean_rent["RentPrice"].median()
    mean_rent["RentPrice"] = mean_rent["RentPrice"].fillna(median_price)
    
    #Exporting the database:
    merged_db.to_csv("clean_database.csv",index=False)

def mapping_coord_zip(df):
    """
    Helper function that based on some coordinates retrieve the associated zip codes.
    The task is split in part because there are a finite amount of calls allowed
    using the get_zipcode function.

    Input (DataFrame): Must contain the columns with the latitude and longitude
        thata are going to be used as inputs to calculate the zip code.
    
    Output: A .txt file that contains the information of a dictionary where its
        keys are latitude/longitude pairs and its values are zipcodes
    """
    #Initial arguments:
    num_rows = 5000
    num_splits = round(df.shape[0]/num_rows)

    #Function to get the zip codes (adapted from the following urls):
    #https://gis.stackexchange.com/questions/352961/converting-lat-lon-to-postal-code-using-python)
    #https://stackoverflow.com/questions/66227003/reverse-geocoding-getting-postal-code-with-geopy-nominatim

    def get_zipcode(geolocator, lat, lon):
        try:
            location = geolocator.reverse((lat, lon))
            return location.raw['address']['postcode']
        except KeyError:
            pass

    geolocator = geopy.Nominatim(user_agent='ssegovba@uchicago.edu')

    #Retrieving the indexes:  
    for s in range(num_splits+1):
        if s == 0:
            lat_lon_dict = {}
        else:
            with open(DATA_PATH + "lat_lon_dict_" + str(s-1) +".txt", "r") as fp:
                lat_lon_dict = json.load(fp)

        lower_idx = num_rows*s
        upper_idx = num_rows*(s+1)
        if s == num_splits:
            df_loop = df[lower_idx:].copy()
        else:
            df_loop = df[lower_idx:upper_idx].copy()

        df_loop = df_loop.reset_index()
        for _, row in df_loop.iterrows():
            key = str(row["latitude"]) + "/" + str(row["longitude"])
            if key not in lat_lon_dict:
                lat_lon_dict[key] = get_zipcode(geolocator,row["latitude"],row["longitude"])
        
        with open("lat_lon_dict_" + str(s) +".txt", "w") as fp:
            json.dump(lat_lon_dict, fp)
    
    #Creating the final dictionary:
    with open("lat_lon_dict_" + str(num_splits) +".txt", "r") as fp:
                lat_lon_dict = json.load(fp)
    with open("lat_lon_dict.txt", "w") as fp:
            json.dump(lat_lon_dict, fp)