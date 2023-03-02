import pandas as pd
from urllib.request import urlopen
import json
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

#while waiting for final data
from graphs.make_dummy_viz_data import make_dummy_data
# temp data
df = make_dummy_data()

# import the graphs
from graphs.bivariate_map import bivariate_map, create_legend
from graphs.line_graphs import make_scatter_plot
from graphs.radar_graph import create_radar_graph

# Boundaries by Zip code - Chicago (Geojson)
boundaries_url = "https://data.cityofchicago.org/api/geospatial/gdcf-axmw?method=export&format=GeoJSON"

with urlopen(boundaries_url) as response:
    zipcodes = json.load(response)

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# ----------------- BIVARIATE MAP ---------------------

colors = ['#e8e8e8', '#b5c0da', '#6c83b5',
          '#b8d6be', '#90b2b3', '#567994',
          '#73ae80', '#5a9178', '#2a5a5b']

map_fig = bivariate_map(df, colors, zipcodes, 'disparity_index', 'num_evictions')
map_legend = create_legend(colors)


# ----------------- SCATTER PLOT ---------------------
indicator_dropdown = dcc.Dropdown(options = ['x1', 'x2', 'x3', 'x4'], value = 'x1')

scatter_fig = make_scatter_plot(df, 'disparity_index', 'num_evictions')

# ----------------- RADAR PLOT ---------------------

zip_dropdown = dcc.Dropdown(options = df['zipcode'].unique(), value = '60601')

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
                            style={"font-size": 16, "text-align": 'left', 'marginTop': 15})
                
            )
    
        ),
        dbc.Row(html.H3("How does neighborhood deprivation relate to evictions?",
                        style={'marginBottom': 10, 'marginTop': 20}),

        ),
        dbc.Row(
            [
            dbc.Col(
                dcc.Graph(id="map", figure=map_fig,
                          style={'width': '100%', 'marginBottom': 25, 'marginTop': 25}),
                width={"size":9}
            ),
            dbc.Col(
                dcc.Graph(id="legend", figure=map_legend, style={'width': '100%'}),
                width={"size":3}
            )
            ]
        ),
        dbc.Row(
            dbc.Col(
                #     dcc.Graph(id="radar_graph", figure=radar_fig,
                #               style={'width': '100%', 'marginBottom': 25, 'marginTop': 25}),
                # )
                html.Div(children=[
                    html.H3(children='Comparison of Zip Code Attributes to City Average',
                            style={'marginBottom': 10, 'marginTop': 20}),
                    zip_dropdown,
                    dcc.Graph(id="radar_graph", figure = radar_fig,)
                ])
            )
        ),
        dbc.Row(
            dbc.Col(
                html.H3("Comparison of Evictions to Key Deprivation Indicators",
                        style={'marginBottom': 10, 'marginTop': 20}),
            )
        ),
        dbc.Row(
            dbc.Col(
                # dcc.Graph(id="scatter_graph", figure=scatter_fig),

                html.Div(children=[
                    indicator_dropdown,
                    dcc.Graph(id="scatter_graph", figure = scatter_fig,)
                ])
            )
        ),
    ],
    className="mt-4",
)


# ---------------- APP INTERACTION ---------------------

# Dropdown for radar graph
# used this as general guide https://www.justintodata.com/python-interactive-dashboard-with-plotly-dash-tutorial/
@app.callback(
    Output(component_id = 'radar_graph', component_property = 'figure'),
    Input(component_id = zip_dropdown, component_property = 'value')
)
def update_graph(selected_zip):
    # updated_radar_fig = create_radar_graph(df, selected_zip, 'zipcode')
    # return updated_radar_fig
    return create_radar_graph(df, selected_zip, 'zipcode')

# Dropdown for scatter plot
@app.callback(
    Output(component_id = 'scatter_graph', component_property = 'figure'),
    Input(component_id = indicator_dropdown, component_property = 'value')
)
def update_graph(selected_x_var):
    # updated_scatter_plot = make_scatter_plot(df, selected_x_var, 'num_evictions')
    # return updated_scatter_plot
    return make_scatter_plot(df, selected_x_var, 'num_evictions')


if __name__ == '__main__':
    app.run_server(debug=True, port=8092)