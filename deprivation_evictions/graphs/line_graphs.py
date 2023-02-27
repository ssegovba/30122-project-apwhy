# app.py


from make_dummy_viz_data import make_dummy_data
import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

df = make_dummy_data()
df.sort_values('num_evictions')

# need to calculate averages for most of the columns

fig = px.line(df, x = 'num_evictions', y = 'disparity_index', title='Comparison of Deprivation Index to Evictions')
fig.show()


# app = Dash(__name__)

# if __name__ == "__main__":
#     app.run_server(debug=True)