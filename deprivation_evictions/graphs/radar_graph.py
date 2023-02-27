# app.py

from make_dummy_viz_data import make_dummy_data
import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
import plotly.graph_objects as go

df = make_dummy_data()

# calc city averages

# Reformat data for viz
df = df.set_index('zipcode')
# zip_dict = df.to_dict('index')

zip_dict = {}

for index, rows in df.iterrows():
    zip_dict[index] = [rows.x1, rows.x2, rows.x3, rows.x4]


# update data categories upon final data
# Display names for the fields of data
categories = ['data field 1','data field 2','data field 3', 'data field 4']

fig = go.Figure()

# City average
df['x1':'x4'].mean(axis=0)

fig.add_trace(go.Scatterpolar(
      r=[df['x1'].mean(axis=0), 
            df['x2'].mean(axis=0), 
            df['x3'].mean(axis=0), 
            df['x4'].mean(axis=0)],
      theta=categories,
      fill='toself',
      name='City-wide mean'
))

# Specific zip code
fig.add_trace(go.Scatterpolar(
      r=zip_dict['60615'],
      theta=categories,
      fill='toself',
      name='60615'
))

fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[df['x1'].min(axis=0), df['x1'].max(axis=0)]
    )),
  showlegend=False
)

fig.show()