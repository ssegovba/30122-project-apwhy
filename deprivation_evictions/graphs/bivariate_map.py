# Creating the bivariate map for Deprivation and Evictions data
# Written by: Stephania Tello Zamudio

import numpy as np
import plotly.express as px

#Code adapted from Bivariate choropleth map using Plotly 
# (https://www.kaggle.com/code/yotkadata/bivariate-choropleth-map-using-plotly)

#Defining bins for Deprivation Index and Evictions data
def set_interval_value(val, break1, break2):
    '''
    Assigns value (val) to one of the three bins (0, 1, 2)
        according to break points define by break1 and break2

    Inputs:
        val (float): value of variable
        break1 (float): threshold for first bin
        break2 (float): threshold for second bin

    Returns:
        (int):  one of the three bins (0, 1, 2) 
    '''
    if val <= break1:
        return 0
    elif val > break1 and val <= break2:
        return 1
    else:
        return 2

#Adding column to df with the bin value
def prepare_df(df, x, y):
    '''
    Add a column to dataframe with the position of x and y
        in the 9-color matrix of the map.
    
    Inputs:
        df (DataFrame): final project DataFrame
        x (str): name of variable in x-axis
        y (str): name of variable in y-axis
    
    Returns: (DataFrame) df with an additional column
    '''
    prep_df = df
    
    prep_df = prep_df.rename(columns={'eviction_filings_completed_scaled':'Evictions per capita',
                             'wdi_scaled': 'Deprivation Index'})
    
    #Calculating break points (percentile 33 and 66)
    x_bp = np.percentile(prep_df[x], [33, 66])
    y_bp = np.percentile(prep_df[y], [33, 66])

    #Assigning values of x and y to one of 3 bins
    x_bins = [set_interval_value(val_x, x_bp[0], x_bp[1]) for val_x in prep_df[x]]
    y_bins = [set_interval_value(val_y, y_bp[0], y_bp[1]) for val_y in prep_df[y]]

    #Calculating the position of each x and y pair in the 9 color matrix
    prep_df['biv_bins'] = [int(val_x + 3 * val_y) for val_x, val_y in zip(x_bins, y_bins)]

    return prep_df


#Creating the color square legend 
def create_legend(colors):
    """
    Creates color square legend that contains 9-color matrix
        for bivariate map
    
    Inputs:
        fig (Figure object): map of Chicago
        colors (lst): list with 9 colors for legend

    Returns: (Figure object) 9-color legend matrix
    """
    data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    legend_colors = colors[6:] + colors[3:6] + colors[:3]

    fig = px.imshow(
        data,
        labels=dict(x = "Deprivation Index", y = "Evictions per capita"),
        x=["< 0.33", "< 0.66", "< 1.0"],
        y=["High", "Medium", "Low"],
        color_continuous_scale=legend_colors,
                                )

    fig.update_layout(coloraxis_showscale=False)
    
    return fig


#Creating bivariate map
def bivariate_map(df, colors, geojson, x, y):
    """
    Creates a bivariate choropleth map

    Inputs:
        df (DataFrame): final project dataset
        colors (lst): list of colors for map legend
        geojson (geojson): file of Zip Code boundaries in Chicago
        x (str): name of variable in x-axis
        y (str): name of variable in y-axis

    Returns:
        (fig) Bivariate choropleth map of Chicago relating
            evictions and neighborhood deprivation
    """
    
    #Checking that colors list has 9 elements
    assert 9 == len(colors), "List of colors has to contain 9 elements"

    final_df = prepare_df(df, x, y)

    # final_df.rename(columns={'eviction_filings_completed_scaled':'Evictions per capita',
    #                          'wdi_scaled': 'Deprivation Index'}, inplace=True)

    fig = px.choropleth_mapbox(
        final_df,
        featureidkey="properties.zip",
        geojson=geojson,
        locations='zipcode',
        mapbox_style = 'carto-positron',
        center = {"lat": 41.8, "lon": -87.75},
        color='biv_bins',
        color_continuous_scale=colors,
        opacity=0.8,
        zoom=9,
        hover_name='zipcode',
        hover_data={"Evictions per capita": ':.2f', "Deprivation Index": ':.2f',
                    'biv_bins': False, 'zipcode': False},
    )

    fig.update_geos(fitbounds='locations', visible=False)

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                      coloraxis_showscale=False)

    #fig.update_coloraxes() --- to change style of coloraxes


    return fig

    



