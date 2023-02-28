# app.py


from make_dummy_viz_data import make_dummy_data
import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# had to do 
# pip3 install statsmodels
# pip3 install -U psutil

df = make_dummy_data()

# is this necessary?
df = df.sort_values('num_evictions')

# Need to include other factors in the hover-over, like zip code


fig = px.scatter(df, x="num_evictions", 
                    y="disparity_index", 
                    trendline="ols", 
                    title='Comparison of Deprivation Index to Evictions')
fig.show()


# get the regression equation
results = px.get_trendline_results(fig)
results = results.iloc[0]["px_fit_results"].summary()
# print(results)

# correlation coefficient
df['num_evictions'].corr(df['disparity_index'])

# app = Dash(__name__)

# if __name__ == "__main__":
#     app.run_server(debug=True)