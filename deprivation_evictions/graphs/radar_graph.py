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
    df = df.set_index(zipcode_col_name)

    # Get the data in the right format
    zip_dict = {}

    for index, rows in df.iterrows():
        zip_dict[index] = [rows.violent_crime_scaled_norm,
                           rows.non_offensive_crime_scaled_norm, rows.RTI_ratio_norm, 
                           rows.time_to_CBD_norm, rows.distance_to_CBD_norm]

    # Define the data labels, in order
    categories = ['Violent Crime', 'Non-Violent Crime', 
                  'Rent-to-Income Ratio', 'Time to Loop', 'Distance to Loop']

    fig = go.Figure()   

    # Graph the city averages
    fig.add_trace(go.Scatterpolar(
        r = [df['violent_crime_scaled_norm'].mean(axis=0), 
                df['non_offensive_crime_scaled_norm'].mean(axis=0), 
                df['RTI_ratio_norm'].mean(axis=0),
                df['time_to_CBD_norm'].mean(axis=0),
                df['distance_to_CBD_norm'].mean(axis=0)],
        theta = categories,
        fill = 'toself',
        name = 'City-wide mean',
        fillcolor = 'rgb(222, 224, 210)',
        line_color = 'rgb(222, 224, 210)'
    ))

    # Create the graph for a specific zip code
    fig.add_trace(go.Scatterpolar(
        r = zip_dict[zip_code],
        theta = categories,
        fill = 'toself',
        name = "Zip code = {}".format(zip_code),
        fillcolor = 'rgb(153, 189, 156)',
        line_color = 'rgb(153, 189, 156)'
    ))

    # Get maximum value for the different axes

    indicators = ['violent_crime_scaled_norm', 
                'non_offensive_crime_scaled_norm', 'RTI_ratio_norm', 
                'time_to_CBD_norm', 'distance_to_CBD_norm']
    
    maxes = df[indicators].max(axis=0)
    
    mins = df[indicators].min(axis=0)

    # Add ranges to the graph
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[mins.min(), maxes.max()]
            #range=[mins.min(), 3]
            )),
        showlegend=True
    )
    fig.update_traces(opacity=0.5)
    fig.update_layout(
        autosize = False,
        height = 800)

    return fig