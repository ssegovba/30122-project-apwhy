import numpy as np
import pandas as pd
import plotly.graph_objs as go
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
    #Calculating break points (percentile 33 and 66)
    x_bp = np.percentile(df[x], [33, 66])
    y_bp = np.percentile(df[y], [33, 66])

    #Assigning values of x and y to one of 3 bins
    x_bins = [set_interval_value(val_x, x_bp[0], x_bp[1]) for val_x in df[x]]
    y_bins = [set_interval_value(val_y, y_bp[0], y_bp[1]) for val_y in df[y]]

    #Calculating the position of each x and y pair in the 9 color matrix
    df['biv_bins'] = [int(val_x + 3 * val_y) for val_x, val_y in zip(x_bins, y_bins)]

    return df


#Creating the color square legend 
def create_legend(fig, colors):
    """
    Creates color square legend that contains 9-color matrix
        for bivariate map
    
    Inputs:
        fig (Figure object): map of Chicago
        colors (lst): list with 9 colors for legend

    Returns: (Figure object) map with added legend
    """
    #Setting the width and height of each color box
    width = 0.04
    height = 0.04 / 0.8 #box height / ratio of height to width

    #Calculating the coordinates of each rectangle in legend
    legend_colors = colors[:]
    legend_colors.reverse

    coordinates = []

    for row in range(1, 4):
        for col in range(1, 4):
            coordinates.append({
                'x0': round(1 - (col - 1)*width, 4),
                'y0': round(1 - (row - 1)*height, 4),
                'x1': round(1 - col*width, 4),
                'y1': round(1 - row*height, 4)
            })
    
    #Creating the boxes
    for i, value in enumerate(coordinates):
        # Add rectangle
        fig.add_shape(go.layout.Shape(
            type='rect',
            fillcolor=legend_colors[i],
            line=dict(
                color='#f8f8f8',
                width=0,
            ),
            xref='paper',
            yref='paper',
            xanchor='right',
            yanchor='top',
            x0=coordinates[i]['x0'],
            y0=coordinates[i]['y0'],
            x1=coordinates[i]['x1'],
            y1=coordinates[i]['y1'],
        ))

        #Text for x variable: Deprivation Index
        fig.add_annotation(
            xref='paper',
            yref='paper',
            xanchor='left',
            yanchor='top',
            x=coordinates[8]['x1'],
            y=coordinates[8]['y1'],
            showarrow=False,
            text="Deprivation Index" + ' 🠒',
            font=dict(
                color='#333',
                size=9,
            ),
            borderpad=0,
        )

        #Text for y variable: Evictions
        fig.add_annotation(
            xref='paper',
            yref='paper',
            xanchor='right',
            yanchor='bottom',
            x=coordinates[8]['x1'],
            y=coordinates[8]['y1'],
            showarrow=False,
            text="Evictions" + ' 🠒',
            font=dict(
                color='#333',
                size=9,
            ),
            textangle=270, #so it is vertical
            borderpad=0,
        )

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
    final_df['biv_bins'] = final_df['biv_bins'].apply(str)

    fig = px.choropleth_mapbox(
        final_df,
        featureidkey="properties.zip",
        geojson=geojson,
        locations='zipcode',
        mapbox_style = 'carto-positron',
        center = {"lat":41.8781, "lon":-87.6298},
        color='biv_bins',
        color_discrete_map={
            '0': colors[0],
            '1': colors[1],
            '2': colors[2],
            '3': colors[3],
            '4': colors[4],
            '5': colors[5],
            '6': colors[6],
            '7': colors[7],
            '8': colors[8],
        },
        opacity=0.7,
        zoom=9,
        hover_data=["num_evictions", "disparity_index"],
    )

    # fig = px.choropleth_mapbox(
    #     final_df,
    #     featureidkey="properties.zip",
    #     geojson=geojson,
    #     locations='zipcode',
    #     color='biv_bins',
    #     mapbox_style = 'carto-positron',
    #     center = {"lat":41.8781, "lon":-87.6298},
    #     color_discrete_map={
    #         '0': colors[0],
    #         '1': colors[1],
    #         '2': colors[2],
    #         '3': colors[3],
    #         '4': colors[4],
    #         '5': colors[5],
    #         '6': colors[6],
    #         '7': colors[7],
    #         '8': colors[8],
    #     },
    #     opacity=0.7,
    #     zoom=9,
    # )

    # fig = go.Figure(go.Choroplethmapbox(
    #     geojson=geojson,
    #     locations=final_df['zipcode'],
    #     z=final_df['biv_bins'],
    #     marker_line_width=.5,
    #     colorscale=[
    #         [0/8, colors[0]],
    #         [1/8, colors[1]],
    #         [2/8, colors[2]],
    #         [3/8, colors[3]],
    #         [4/8, colors[4]],
    #         [5/8, colors[5]],
    #         [6/8, colors[6]],
    #         [7/8, colors[7]],
    #         [8/8, colors[8]],
    #     ],
    #     featureidkey="properties.zip",
    # ))

    fig.update_geos(fitbounds='locations', visible=False)

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    #fig.update_traces(marker_line_width=0)
    #Adding the legend
    #fig = create_legend(fig, colors)

    return fig

    



