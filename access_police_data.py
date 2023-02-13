#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata

def pull_2022_crime_data():
    '''
    Retrieves 2022 crime data from Chicago Data Portal

    Inputs: none

    Returns (dataframe or csv): Chicago crime data, one crime per row
    '''

    APP_TOKEN = 'iVwn5D2iqqAipgU9FpV1K1nq7'

    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.cityofchicago.org", APP_TOKEN)

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(data.cityofchicago.org,
    #                  MyAppToken,
    #                  username="user@example.com",
    #                  password="AFakePassword")

    # webpage example:
    # https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2


    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    # results = client.get("ijzp-q8t2", limit=2000)

    data_2022 = client.get("ijzp-q8t2", select = '*', where = 'Year = 2022', limit = 1000000)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(data_2022)

    # if we want to convert to csv
    # results_df.to_csv('Chicago_2022_crime.csv')

    return results_df

