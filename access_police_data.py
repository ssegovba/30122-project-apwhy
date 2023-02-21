#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata

def pull_crime_data(year):
    '''
    Retrieves crime data from Chicago Data Portal for a specific year.

    Inputs (int): Year for which the data wants to be pulled

    Returns: None, writes the pulled data as a csv file in the provided path.
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

    data = client.get("ijzp-q8t2", select = '*', where = 'Year = ' + str(year), limit = 1000000)

    # Convert to pd DataFrame an exports the file
    results_df = pd.DataFrame.from_records(data)
    results_df.to_csv('data_bases/crime_data.csv')