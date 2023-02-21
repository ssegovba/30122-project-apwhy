import pandas as pd
# import geopandas as gpd
# import shapely.geometry as geometry
import geopy
import numpy as np

# Defining initial arguments:
data_path = "data_bases/"

chi_zipcodes = np.array(['60601', '60602', '60603', '60604',
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
                               '60666', '60707', '60827'])

# Zillow Data:
rent_data = pd.read_csv(data_path + "zillow_data.csv")
rent_data = rent_data[rent_data["State"]=="IL"]
date_cols = rent_data.filter(like='20', axis=1)
rent_data = rent_data.melt(id_vars=["RegionName","State"],value_vars=date_cols,
            var_name="Date",value_name="RentPrice")
rent_data["Date"] = pd.to_datetime(rent_data["Date"], format = "%Y-%m-%d")
rent_data = rent_data[rent_data["Date"].dt.year == 2019]

# 311 Data:
# df = pd.read_csv(data_path + "crime_data.csv")
# df = df["date"].str.slice(0,10)
# cols_to_keep = ['id', 'date', 'primary_type','description','location_description',
#                 'arrest','latitude','longitude']
# df = df[cols_to_keep]
# df = df[df["latitude"].isna() == False] #2042 registers without coordinates

# #Getting zip codes from latitude and longitude:
# #(taken from https://gis.stackexchange.com/questions/352961/converting-lat-lon-to-postal-code-using-python)

# def get_zipcode(df, geolocator, lat_field, lon_field):
#     location = geolocator.reverse((df[lat_field], df[lon_field]))
#     return location.raw['address']['postcode']

# geolocator = geopy.Nominatim(user_agent='ssegovba@uchicago.edu')
# df["zipcode"] = df.apply(get_zipcode, geolocator=geolocator, lat_field='latitude', lon_field='longitude', axis = 1)

# ACS Data:
acs_data = pd.read_csv(data_path + "acs_data.csv")

acs_data["date"] = 2019

#Merging the databases:

