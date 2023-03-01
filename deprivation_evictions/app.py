import pandas as pd
from urllib.request import urlopen
import json
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

#while waiting for final data
from graphs.make_dummy_viz_data import make_dummy_data

# import the graphs
from graphs.bivariate_map import bivariate_map
from graphs.line_graphs import make_scatter_plot
from graphs.radar_graph import create_radar_graph

# temp data
df = make_dummy_data()

# Boundaries by Zip code - Chicago (Geojson)
boundaries_url = "https://data.cityofchicago.org/api/geospatial/gdcf-axmw?method=export&format=GeoJSON"

with urlopen(boundaries_url) as response:
    zipcodes = json.load(response)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ----------------- BIVARIATE MAP ---------------------

colors = ['#73ae80', '#5a9178', '#2a5a5b',
          '#b8d6be', '#90b2b3', '#567994',
          '#e8e8e8', '#b5c0da', '#6c83b5']

map_fig = bivariate_map(df, colors, zipcodes, 'disparity_index', 'num_evictions')

# ----------------- SCATTER PLOT ---------------------
scatter_fig = make_scatter_plot(df, 'disparity_index', 'num_evictions')

# ----------------- RADAR PLOT ---------------------

zip_dropdown = dcc.Dropdown(options=df['zipcode'].unique(), value='60601')

radar_fig = create_radar_graph(df, '60615', 'zipcode')


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
        dbc.Row(
            dbc.Col(
                #     dcc.Graph(id="radar_graph", figure=radar_fig,
                #               style={'width': '100%', 'marginBottom': 25, 'marginTop': 25}),
                # )
                html.Div(children=[
                    html.H1(children='Comparison of Neighborhood Attributes to City Average'),
                    zip_dropdown,
                    dcc.Graph(id="radar_graph", figure=radar_fig,)
                ])
            )
        ),
        dbc.Row(
            dbc.Col(
                # dcc.Graph(id="scatter_graph", figure=scatter_fig),
                #           style={'width': '100%', 'marginBottom': 25, 'marginTop': 25}),
                dcc.Graph(id="scatter_graph", figure=scatter_fig),
            )
        ),



    ],
    className="mt-4",
)

# ---------------- APP INTERACTION ---------------------

# used this as general guide https://www.justintodata.com/python-interactive-dashboard-with-plotly-dash-tutorial/
@app.callback(
    Output(component_id = 'radar_graph', component_property = 'figure'),
    Input(component_id = zip_dropdown, component_property = 'value')
)
def update_graph(selected_zip):
    updated_radar_fig = create_radar_graph(df, selected_zip, 'zipcode')
    return updated_radar_fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8092)