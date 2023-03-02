#from make_dummy_viz_data import make_dummy_data
import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
import plotly.graph_objects as go

#df = make_dummy_data()

def create_radar_graph(df, zip_code, zipcode_col_name):

  # Reformat data for viz
  df = df.set_index(zipcode_col_name)

  # Get the data in the right format
  zip_dict = {}

  for index, rows in df.iterrows():
      zip_dict[index] = [rows.x1, rows.x2, rows.x3, rows.x4]


  # update data categories upon final data
  # Create display names for the fields of data
  categories = ['data field 1','data field 2','data field 3', 'data field 4']

  fig = go.Figure()

  # Graph the city averages
  df['x1':'x4'].mean(axis=0)

  fig.add_trace(go.Scatterpolar(
        r = [df['x1'].mean(axis=0), 
              df['x2'].mean(axis=0), 
              df['x3'].mean(axis=0), 
              df['x4'].mean(axis=0)],
        theta = categories,
        fill = 'toself',
        name = 'City-wide mean'
  ))

  # Create the graph for a specific zip code
  fig.add_trace(go.Scatterpolar(
        r = zip_dict[zip_code],
        theta = categories,
        fill = 'toself',
        name = zip_code
  ))

  fig.update_layout(
    polar=dict(
      radialaxis=dict(
        visible=True,
        range=[df['x1'].min(axis=0), df['x1'].max(axis=0)]
      )),
    showlegend=False
  )

  #fig.show()

  return fig