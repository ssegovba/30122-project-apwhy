# Pull data on crime from the Chicago data API
# Created by Andrew Dunn

import pandas as pd
from sodapy import Socrata

def pull_crime_data(year):
    '''
    Retrieves crime data from Chicago Data Portal for a specific year.
    For info on the data: https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2

    Inputs (int): year of data to pull

    Returns: None, writes the pulled data as a csv file in the provided path.
    '''

    APP_TOKEN = 'iVwn5D2iqqAipgU9FpV1K1nq7'

    client = Socrata("data.cityofchicago.org", APP_TOKEN)

    data = client.get("ijzp-q8t2", select = '*', where = 'Year = ' + str(year), limit = 1000000)

    # Convert to pd DataFrame and export the file
    results_df = pd.DataFrame.from_records(data)
    results_df.to_csv('data_bases/crime_data.csv')