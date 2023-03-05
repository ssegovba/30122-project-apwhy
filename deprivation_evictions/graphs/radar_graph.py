# Creates a radar graph to compare kay variables of a zip code against the mean
# Written by Andrew Dunn

import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
import plotly.graph_objects as go

def create_radar_graph(df, zip_code, zipcode_col_name):
    '''
    Creates a plotly radar graph

    Inputs:
        df (pandas dataframe)
        zip_code (int): the zip code to use in the graph
        zipcode_col_name (str): the name of the relevant zip code col in the df
    
    Returns:
        fig (plotly figure): the radar plot of a zip vs the average
    '''

    # Format zip code column correctly
    #df[zipcode_col_name] = df[zipcode_col_name].apply(str)
    df = df.set_index(zipcode_col_name)

    # Get the data in the right format
    zip_dict = {}

    for index, rows in df.iterrows():
        zip_dict[index] = [rows.violent_crime_scaled_y, rows.crime_scaled_y, rows.non_offensive_crime_scaled_y, 
                            rows.RTI_ratio_y, rows.time_to_CBD_y, rows.distance_to_CBD_y]

    # update data categories upon final data
    categories = ['Violent Crime','All Crime','Non-violent Crime', 
                  'Rent-to-income Ratio', 'Time to Loop', 'Distance to Loop']

    fig = go.Figure()   

    # Graph the city averages
    fig.add_trace(go.Scatterpolar(
        r = [df['violent_crime_scaled_y'].mean(axis=0), 
                df['crime_scaled_y'].mean(axis=0), 
                df['non_offensive_crime_scaled_y'].mean(axis=0), 
                df['RTI_ratio_y'].mean(axis=0),
                df['time_to_CBD_y'].mean(axis=0),
                df['distance_to_CBD_y'].mean(axis=0)],
        theta = categories,
        fill = 'toself',
        name = 'City-wide mean'
    ))

    # Create the graph for a specific zip code
    #str_zip_code = str(zip_code)

    fig.add_trace(go.Scatterpolar(
        r = zip_dict[zip_code],
        theta = categories,
        fill = 'toself',
        name = zip_code
    ))

    # Get maximum value for the different axes
    maxes = df[['violent_crime_scaled_y', 'crime_scaled_y', 'non_offensive_crime_scaled_y', 'RTI_ratio_y', 
        'time_to_CBD_y', 'distance_to_CBD_y']].max(axis=0)

    # Add ranges to the graph
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, maxes.max()]
            )),
        showlegend=False
    )

    #fig.show()

    return fig