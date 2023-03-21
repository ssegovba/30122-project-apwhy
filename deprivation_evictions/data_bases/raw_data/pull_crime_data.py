# Pull data on crime from the Chicago data API
# Created by Andrew Dunn

import pandas as pd
from sodapy import Socrata

# From a non-public doc of API keys
from ...constants import API_TOKEN


def pull_crime_data(year):
    '''
    Retrieves crime data from Chicago Data Portal for a specific year.
    For info on the data: https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2

    Inputs (int): year of data to pull

    Returns: None, writes the pulled data as a csv file in the provided path.
    '''

    # The APP_TOKEN is saved in our local environment
    # To run this code, you will need to get your own API key info
    # See this page for more info https://dev.socrata.com/docs/app-tokens.html
    client = Socrata("data.cityofchicago.org", API_TOKEN)

    data = client.get("ijzp-q8t2", select = '*', where = 'Year = ' + str(year), limit = 1000000)

    # Convert to pd DataFrame and export the file
    results_df = pd.DataFrame.from_records(data)
    results_df.to_csv('deprivation_evictions/data_bases/raw_data/crime_data.csv')