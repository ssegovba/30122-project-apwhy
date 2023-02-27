import pandas as pd
from urllib.request import urlopen
import json
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

#while waiting for final data
from graphs.make_dummy_viz_data import make_dummy_data
from graphs.bivariate_map import bivariate_map

# Boundaries by Zip code - Chicago (Geojson)
boundaries_url = "https://data.cityofchicago.org/api/geospatial/gdcf-axmw?method=export&format=GeoJSON"

with urlopen(boundaries_url) as response:
    zipcodes = json.load(response)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ----------------- BIVARIATE MAP ---------------------

colors = ['#73ae80', '#5a9178', '#2a5a5b',
          '#b8d6be', '#90b2b3', '#567994',
          '#e8e8e8', '#b5c0da', '#6c83b5']

map_fig = bivariate_map(make_dummy_data(), colors, zipcodes, 'disparity_index', 'num_evictions')


# ----------------- APP LAYOUT ------------------------

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Neighborhood Deprivation and Evictions in Chicago", className="text-center mb-4"),
            )
        ),
        dbc.Row(
            dbc.Col(
                html.H1("Andrew Dunn, Gregory Ho, Santiago Segovia, Stephania Tello Zamudio",
                            style={"font-style": "italic", "font-size": 16, "text-align": 'center'})
                
            )
    
        ),
        dbc.Row(
            dbc.Col(
                html.H1("Evictions are one of the main consequences of the lack of affordable housing in the US. \
                        This project looks to understand what neighborhood characteristics are associated with eviction in \
                        the city of Chicago. This will allow us to construct an index to measure neighborhood deprivation, \
                        using a similar approach as the Multi-dimensional poverty index.",
                            style={"font-size": 14, "text-align": 'left', 'marginTop': 15})
                
            )
    
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id="map", figure=map_fig,
                          style={'width': '100%', 'marginBottom': 25, 'marginTop': 25}),
            )
        ),
    ],
    className="mt-4",
)

# ---------------- APP INTERACTION ---------------------

# @app.callback(


if __name__ == '__main__':
    app.run_server(debug=True, port=8092)