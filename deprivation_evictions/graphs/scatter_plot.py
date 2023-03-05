# Creates a scatter plot of zipcodes using two variables
# Written by Andrew Dunn

import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# to do:
# update graph axis titles
# round numbers in the hover

def make_scatter_plot(df, x_var_label):
    '''
    Creates a plotly scatter plot

    Inputs:
        df (pandas dataframe)
        x_var (object): the column for the x-axis
    
    Returns:
        fig (plotly figure): the scatter plot with OLS line
    '''

    # Define the x variables for different axis labels 
    if x_var_label == 'Violent Crime':
        x_var = 'violent_crime_scaled_norm' 
    elif x_var_label == 'All Crime':
        x_var = 'crime_scaled_norm' 
    elif x_var_label == 'Non-Violent Crime':
        x_var = 'non_offensive_crime_scaled_norm'
    elif x_var_label == 'Rent-to-Income Ratio':
        x_var = 'RTI_ratio_norm'
    elif x_var_label == 'Time to the Loop':
        x_var = 'time_to_CBD_norm'
    elif x_var_label == 'Distance to the Loop':
        x_var = 'distance_to_CBD_norm' 
        
    # Build the graph
    fig = px.scatter(df, x = x_var, 
                        y = 'eviction_filings_completed_scaled', 
                        labels={
                            x_var : x_var_label,
                            "eviction_filings_completed_scaled" : "Evictions (per capita)",
                        },
                        trendline = "ols", 
                        # Can we add in 'Zip code =' to the hover name?
                        hover_name = "zipcode", 
                        hover_data = [x_var, 'eviction_filings_completed_scaled'],
                        trendline_color_override = 'rgb(25, 137, 125)'
                    ).update_traces(
                        marker=dict(color='rgb(20, 29, 67)')
                    ).update_xaxes(showgrid=False
                    ).update_yaxes(showgrid=False)

    return fig