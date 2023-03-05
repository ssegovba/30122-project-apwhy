# Creates a scatter plot of zipcodes using two variables
# Written by Andrew Dunn

import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# to do:
# update graph axis titles
# round numbers in the hover

def make_scatter_plot(df, x_var):
    '''
    Creates a plotly scatter plot

    Inputs:
        df (pandas dataframe)
        x_var (object): the column for the x-axis
    
    Returns:
        fig (plotly figure): the scatter plot with OLS line
    '''

    # Define axis labels for differentx inputs
    x_var_label = 'test label'



    fig = px.scatter(df, x = x_var, 
                        y = 'eviction_filings_completed_scaled', 
                        labels={
                            "x_var" : x_var_label,
                            "eviction_filings_completed_scaled" : "Evictions (per 10,000 residents)",
                        },
                        trendline = "ols", 
                        #title='Comparison of Deprivation Index to Evictions',
                        hover_name = "zipcode", 
                        hover_data = [x_var, 'eviction_filings_completed_scaled'])

    #fig.show()

    return fig