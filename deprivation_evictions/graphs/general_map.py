# Creating the map of Chicago for evictions and dipravation index
# Written by: Stephania Tello Zamudio

import plotly.express as px

def general_map(df, ind_evic, geojson):
    
    df_map = df

    df_map = df_map.rename(columns={'eviction_filings_completed_scaled':'Evictions per capita',
    'g1_sum_scaled': 'Deprivation Index'})

    # if ind_evic == 'Evictions per capita':
    #     var = 'Evictions per capita'
    # else:
    #     var = 'Deprivation Index'
    
    fig = px.choropleth_mapbox(
        df_map,
        featureidkey="properties.zip",
        geojson=geojson,
        locations='zipcode',
        mapbox_style = 'carto-positron',
        center = {"lat": 41.8, "lon": -87.75},
        color=ind_evic,
        color_continuous_scale=px.colors.sequential.tempo,
        opacity=0.8,
        zoom=9,
        hover_name='zipcode',
        hover_data={ind_evic: ':.2f', 'zipcode': False},
    )

    fig.update_geos(fitbounds='locations', visible=False)

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                      coloraxis_showscale=True)

    return fig