# make sure to install these packages before running:
# pip install pandas
# pip install geopy

import pandas as pd
import numpy as np
import geopy

# Defining initial arguments:
data_path = "data_bases/"
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
# 
rent_data = pd.read_csv(data_path + "zillow_data.csv")
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

# 311 Data:
# Define types of crimes that are going to be aggregated by zip code:
crime_data = pd.read_csv(data_path + "crime_data.csv")
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

# crime_data["coord"] = crime_data["latitude"].astype(str) + "/" + crime_data["longitude"].astype(str)
# crime_count = crime_data.groupby("coord")["crime","violent_crime","non_offensive_crime"].count().reset_index()
# new_crime_data = pd.merge(crime_count,crime_data[["coord","latitude","longitude"]].drop_duplicates(),how="left",on="coord")

#Getting zip codes from latitude and longitude:
#(taken from https://gis.stackexchange.com/questions/352961/converting-lat-lon-to-postal-code-using-python)

def get_zipcode(df, geolocator, lat_field, lon_field):
    location = geolocator.reverse((df[lat_field], df[lon_field]))
    return location.raw['address']['postcode']

geolocator = geopy.Nominatim(user_agent='ssegovba@uchicago.edu')

crime_data["zip_code"] = crime_data.apply(get_zipcode, geolocator=geolocator,
                        lat_field='latitude', lon_field='longitude', axis = 1)

temp = crime_data[0:100]
temp.apply(get_zipcode, geolocator=geolocator,
                        lat_field='latitude', lon_field='longitude', axis = 1)

crime_data[crime_data["violent_crime"]==1].shape

# ACS Data:
# Select zipcodes from Chcicago
acs_data = pd.read_csv(data_path + "acs_data.csv")
acs_data = acs_data.drop(columns=["Unnamed: 0"])
acs_data['zip_code'] = acs_data['zip_code'].astype("string")
acs_data = acs_data[acs_data["zip_code"].isin(zipcodes["zip_code"])]

#Merging the databases:
merged_db = pd.merge(acs_data,mean_rent,on="zip_code",how="outer")