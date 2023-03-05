import pandas as pd
from urllib.request import urlopen
import json
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

# Load the processed data
df = pd.read_csv('data_bases/final_data/processed_data.csv')

# Import the graphs
from graphs.bivariate_map import bivariate_map, create_legend
from graphs.scatter_plot import make_scatter_plot
from graphs.radar_graph import create_radar_graph

# Boundaries by Zip code - Chicago (Geojson)
boundaries_url = "https://data.cityofchicago.org/api/geospatial/gdcf-axmw?method=export&format=GeoJSON"

with urlopen(boundaries_url) as response:
    zipcodes = json.load(response)

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# ----------------- BIVARIATE MAP ---------------------

colors = ['rgb(222, 224, 210)', 'rgb(189, 206, 181)', 'rgb(153, 189, 156)', 
          'rgb(110, 173, 138)', 'rgb(65, 157, 129)', 'rgb(25, 137, 125)', 
          'rgb(18, 116, 117)', 'rgb(28, 72, 93)', 'rgb(20, 29, 67)']

map_fig = bivariate_map(df, colors, zipcodes, 'wdi_scaled', 'eviction_filings_completed_scaled')
map_legend = create_legend(colors)

# ----------------- SCATTER PLOT ---------------------
# need to create diplay names?
#  categories = ['Violent Crime','All Crime','Non-violent Crime', 'Rent-to-income Ratio', 
#                 'Time to Loop', 'Distance to Loop']

indicator_dropdown = dcc.Dropdown(options = ['violent_crime_scaled_y', 
                                             'crime_scaled_y', 
                                             'non_offensive_crime_scaled_y', 
                                             'RTI_ratio_y',
                                             'time_to_CBD_y',
                                             'distance_to_CBD_y',
                                             ], value = 'violent_crime_scaled_y')

scatter_fig = make_scatter_plot(df, 'violent_crime_scaled_y')


# ----------------- RADAR PLOT ---------------------

zip_dropdown = dcc.Dropdown(options = df['zipcode'].unique(), value = '60601')

radar_fig = create_radar_graph(df, 60615, 'zipcode')

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
                html.P("Evictions are one of the main consequences of the lack of affordable housing in the US. \
                        This project looks to understand what neighborhood characteristics are associated with eviction in \
                        the city of Chicago. In order to do that, we construct an index to measure neighborhood deprivation, \
                        using a similar approach as the Multi-dimensional poverty index.",
                            style={"font-size": 16, "text-align": 'left', 'marginTop': 15})
                
            )
    
        ),
        dbc.Row(dbc.RadioItems(id = 'ind_evic', 
                               options = ["Eviction rate", "Deprivation Index"],
                               value = "Eviction rate",
                               inline = True)
        ),
        dbc.Row(
        dcc.Graph(id="gen_map", figure={},
                  style={'width': '100%', 'marginBottom': 25, 'marginTop': 25})
        ),
        dbc.Row(html.H3("How does neighborhood deprivation relate to evictions?",
                        style={'marginBottom': 10, 'marginTop': 10}),

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
                html.Div(children=[
                    html.H3(children='Comparison of Zip Code Attributes to City Average',
                            style={'marginBottom': 10, 'marginTop': 20}),
                    zip_dropdown,
                    #dcc.Graph(id="radar_graph", figure = radar_fig,)
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

# Dropdown for general map
@app.callback(
        Output(component_id = 'gen_map', component_property='figure'),
        Input(component_id='ind_evic', component_property= 'value')
)

def general_map(ind_evic):
    
    df_map = df

    if ind_evic == 'Eviction rate':
        var = 'eviction_filings_completed_scaled'
    else:
        var = 'wdi_scaled'
    
    fig = px.choropleth_mapbox(
        df_map,
        featureidkey="properties.zip",
        geojson=zipcodes,
        locations='zipcode',
        mapbox_style = 'carto-positron',
        center = {"lat": 41.8, "lon": -87.75},
        color=var,
        color_continuous_scale=px.colors.sequential.tempo,
        opacity=0.8,
        zoom=9,
        hover_data={var: True},
    )

    fig.update_geos(fitbounds='locations', visible=False)

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                      coloraxis_showscale=True)

    return fig

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
    return make_scatter_plot(df, selected_x_var)


if __name__ == '__main__':
    app.run_server(debug=True, port=8092)