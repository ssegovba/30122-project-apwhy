# Created by Gregory Ho

import geopandas as gpd
import random
import shapely.geometry as geometry
import pandas as pd
import requests
from random import randint
from time import sleep

# From a non-public doc of API keys
from ...constants import GOOGLE_TOKEN

#Google token for calling its API
API_KEY = GOOGLE_TOKEN

#Path to Geojson file, from which zip code boundaries are stored
ZIPCODE_PATH = "deprivation_evictions/data_bases/raw_data/bound_zip_codes.geojson"

DESTINATION = "41.875556,-87.6244014" # coordinates of the center of "The Loop, Chicago"
NUM_ORIGIN = 13 # number of random points
SEED = 20220224

def define_origin_coor(NUM_ORIGIN):
    '''
    Opens zipcode shapefile, generates 'num_origin' random coordinates as origin
    points. As zip code boundaries come in different sizes, it is more appropriate 
    to use a set of random coordinates to generate more representative travel 
    statistics.

    Helper function: 
    --used in update_travel_data

    Inputs: 
    NUM_ORIGIN: number of random origin points in a zipcode boundary

    Function:
    Appends (zipcode, latitude, longitude) into a Pandas dataframe
    '''
    # Open geojson shapefile
    zipcodes = gpd.read_file(ZIPCODE_PATH)

    # Instantiate Pandas DF to store data
    points_df = pd.DataFrame(columns=['latitude', 'longitude', 'zipcode'])

    # Loop through each zipcode and generate n. random coordinates representing origin
    for _, zipcode in zipcodes.iterrows():
        for _ in range(NUM_ORIGIN):
            # If random point is not within zipcode boundary, randomize again
            point = None
            while not point:
                point = geometry.Point(random.uniform(zipcode.geometry.bounds[0], 
                                                        zipcode.geometry.bounds[2]),
                                    random.uniform(zipcode.geometry.bounds[1], 
                                                    zipcode.geometry.bounds[3]))
                if zipcode.geometry.contains(point):
                    points_df = points_df.append({'latitude': point.y, 
                                                    'longitude': point.x, 
                                                    'zipcode': zipcode.zip}, 
                                                    ignore_index=True)
    
    return points_df


def get_time_distance(origin, DESTINATION):
    '''
    API Call to obtain travel data from Google Distance Matrix API.

    Helper function: 
    --used in update_travel_data

    Inputs: 
    origin: starting coordinates
    DESTINATION: ending coordinates

    Returns:
    time: travel time
    distance: travel distance 
    '''
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={origin}&destinations={DESTINATION}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Key Error Handling: If API returns nothing, 
    # record time, distance as 0 representing missing values
    try:
        time = data['rows'][0]['elements'][0]['duration']['value']
        distance = data['rows'][0]['elements'][0]['distance']['value']
    except KeyError:
        time, distance = 0, 0

    return time, distance

def update_travel_data(DESTINATION, NUM_ORIGIN):
    '''
    Updates each observation in pandas df for DESTINATION (CBD)

    Inputs: 
    DESTINATION: destination either in text, or in (lat, lng)

    Function:
    Appends travel data (time_to_cbd, distance_to_cbd) into the Pandas dataframe
    '''
    random.seed(SEED)
    points_df = define_origin_coor(NUM_ORIGIN)

    points_df['time_to_CBD'] = None
    points_df['distance_to_CBD'] = None
    
    for i, row in points_df.iterrows():
        origin = f"{row['latitude']},{row['longitude']}"
        time, distance = get_time_distance(origin, DESTINATION)
        points_df.at[i, 'time_to_CBD'] = time
        points_df.at[i, 'distance_to_CBD'] = distance
        sleep(randint(1,4))

    points_df.to_csv("deprivation_evictions/data_bases/raw_data/google_distancematrix.csv")

