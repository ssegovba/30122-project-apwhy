import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# to do:
# update graph axis titles
# round numbers in the hover

def make_scatter_plot(df, x_var, y_var):
    fig = px.scatter(df, x = x_var, 
                        y = y_var, 
                        trendline = "ols", 
                        #title='Comparison of Deprivation Index to Evictions',
                        hover_name = "zipcode", 
                        hover_data = [x_var, y_var])

    return fig