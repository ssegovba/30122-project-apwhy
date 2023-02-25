# make sure to install these packages before running:
# pip install pandas
# pip install geopy

import pandas as pd
import numpy as np
import geopy
import json
import time

def clean_db(lat_lon_dict):
    """
    Creates a clean database with all the relevant variables from the different
    data sources employed.

    Input:
        lat_lon_dict (boolean): True if a dictionary containing the zipcodes
            associated with 

    Output:
        - A .csv file that is stored in the 'data_path'
        - if lat_lon_dict a json file containing a coordinates dictionary
    """

    # Defining initial arguments:
    start_time = time.time()
    data_path = "../clean_data"

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
                        '60666', '60707', '60827']}
    zipcodes = pd.DataFrame(data = zip)

    # Zillow Data:
    # The data is filtered by state and year (2019). We focus only on zipcodes from 
    # the city of Chicago: 

    rent_data = pd.read_csv("zillow_data.csv")
    rent_data = rent_data[rent_data["State"]=="IL"]
    date_cols = rent_data.filter(like='20', axis=1)
    rent_data = rent_data.melt(id_vars=["RegionName","State"],value_vars=date_cols,
                var_name="Date",value_name="RentPrice")
    rent_data['RegionName'] = rent_data['RegionName'].astype("string")
    rent_data = rent_data.rename(columns={"RegionName":"zip_code"})
    rent_data["Date"] = pd.to_datetime(rent_data["Date"], format = "%Y-%m-%d")
    rent_data = rent_data[rent_data["Date"].dt.year == 2019]

    #We calculate the mean rent in a zipcode (problem: some zipcodes don't have data):
    rent_data = rent_data[rent_data["zip_code"].isin(zipcodes["zip_code"])]
    mean_rent = rent_data.groupby("zip_code")["RentPrice"].mean().reset_index()

    #Some zipcodes don't have rent data, so the median rent price is assigned to them:
    median_price = mean_rent["RentPrice"].median()
    mean_rent["RentPrice"] = mean_rent["RentPrice"].fillna(median_price)

    # ACS Data:
    # Select zipcodes from Chicago
    acs_data = pd.read_csv("acs_data.csv")
    acs_data = acs_data.drop(columns=["Unnamed: 0"])
    acs_data['zip_code'] = acs_data['zip_code'].astype("string")
    acs_data = acs_data[acs_data["zip_code"].isin(zipcodes["zip_code"])]

    # Evictions Data:
    # Filter by year, select specific columns and create zipcode variable:
    evic_data = pd.read_csv("eviction_data.csv")
    evic_data = evic_data[evic_data["filing_year"] == 2019]

    # 311 Data:
    # Define types of crimes that are going to be aggregated by zip code:
    crime_data = pd.read_csv("crime_data.csv")
    violent_crime = ["ASSAULT","BATTERY","ROBBERY","CRIM SEXUAL ASSAULT",
                    "CRIMINAL SEXUAL ASSAULT","SEX OFFENSE","INTIMIDATION","HOMICIDE",
                    "KIDNAPPING","HUMAN TRAFFICKING"]
    non_offensive = ["OTHER OFFENSE","NARCOTICS","WEAPONS VIOLATION","MOTOR VEHICLE THEFT",
                    "LIQUOR LAW VIOLATION","GAMBLING"]
    cols_to_keep = ['id', 'date', 'primary_type','description','location_description',
                    'arrest','latitude','longitude']
    cols_to_keep = ['id', 'date', 'primary_type','latitude','longitude']
    crime_data = crime_data[cols_to_keep]
    crime_data = crime_data[crime_data["latitude"].isna() == False] #2042 registers without coordinates

    crime_data["crime"] = 1
    crime_data["violent_crime"] = np.where(crime_data["primary_type"].isin(violent_crime),1,0)
    crime_data["non_offensive_crime"] = np.where(crime_data["primary_type"].isin(non_offensive),1,0)
    # crime_data = crime_data[0:50]

    if lat_lon_dict:
        mapping_coord_zip(crime_data)
    else:
        with open("lat_lon_dict.txt", "r") as fp:
            lat_lon_dict = json.load(fp)

    print("--- %s seconds ---" % (time.time() - start_time))

    #Merging the databases:
    # merged_db = pd.merge(acs_data,mean_rent,on="zip_code",how="outer")

def mapping_coord_zip(df):
    """
    Helper function that based on some coordinates retrieve the associated zip codes.

    Input (DataFrame): Must contain the columns with the latitude and longitude
        thata are going to be used as inputs to calculate the zip code.
    
    Output: A .txt file that contains the information of a dictionary where its
        keys are latitude/longitude pairs and its values are zipcodes
    """
    #Function to get the zip codes (taken from the following url):
    #https://gis.stackexchange.com/questions/352961/converting-lat-lon-to-postal-code-using-python)

    def get_zipcode(df, geolocator, lat_field, lon_field):
        location = geolocator.reverse((df[lat_field], df[lon_field]))
        return location.raw['address']['postcode']
    geolocator = geopy.Nominatim(user_agent='ssegovba@uchicago.edu')

    #Add zipcode to the df and then crete the dictionary:
    df["zip_code"] = df.apply(get_zipcode, geolocator=geolocator,
                            lat_field='latitude', lon_field='longitude', axis = 1)
    df["key"] = df["latitude"].astype(str) + "/" + df["longitude"].astype(str)
    lat_lon_dict = df.set_index('key').to_dict()['zip_code']

    #Export the dict as .txt file:
    with open("lat_lon_dict.txt", "w") as fp:
        json.dump(lat_lon_dict, fp)