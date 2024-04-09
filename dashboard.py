# TODO 1: Desing the Front-End
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context, no_update
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
import plotly.graph_objects as go
from helper import countries_df, ind_df, update_wb_data, indicators
import plotly.express as px
import numpy as np


# DF
DF = update_wb_data()


external_stylesheets = [dbc.themes.CYBORG]

app = Dash(__name__, 
           external_stylesheets=external_stylesheets)


# TODO2: Layout Structure
# Tab 1 Content
tab1_content = dbc.Card(
    dbc.CardBody(
        [
            # Tab Text
            html.H2(
                "Comparison of World Bank Country Data", 
                className="card-text"),
            # Insert the Graph
            dcc.Graph(
                id='my-choropleth',
                figure={}
            ),
            # Insert the radio items
            dbc.RadioItems(
                id = 'radio-indicator',
                options = [
                    {'label': ind, 
                     'value': ind}
                    for ind in indicators.values()
                ],
                value = list(indicators.values())[0],
            ),
            # Insert the slider
            dcc.RangeSlider(
                    id = 'years-range',
                    min = 2005,
                    max = 2021,
                    step = 1,
                    value = [2007, 2009],
                    marks = {
                        2005: "2005",
                        2006: "'06",
                        2007: "'07",
                        2008: "'08",
                        2009: "'09",
                        2010: "'10",
                        2011: "'11",
                        2012: "'12",
                        2013: "'13",
                        2014: "'14",
                        2015: "'15",
                        2016: "'16",
                        2017: "'17",
                        2018: "'18",
                        2019: "'19",
                        2020: "'20",
                        2021: "2021"
                            }
                ),
                dbc.Button(
                    # ID
                    id = 'my-button',
                    # Text on the Button
                    children = 'Submit',
                    # Number of clicks
                    n_clicks = 0,
                    # Color
                    color = 'primary',
                    # Margin top 4
                    class_name = 'mt-4'
            ),
        ]
    ),
    className="mt-3",
)

# Tab 2 content
tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.H2(
                "CO2 Emission Comparison", 
                className="card-text text-center"),
            # Insert multiple country options
            html.Div(
                dcc.Dropdown(
                    id='tab_2_drop_down',
                    multi=True,
                    options=[
                        {
                          'label': name,
                          'value': name
                        }
                        for name in sorted(DF['country'].unique())
                    ],
                    value = DF['country'].unique(),
                ), 
                className= 'mb-4' 
            ),
            # Insert the Graph
            dcc.Graph(
                id='tab_2_line_chart',
                figure={}
            ),
            # Insert an AgGrid for tab 2
            dbc.Row(
            dbc.Col(
            dag.AgGrid(
                # Insert ID
                id='tab_2_grid',
                rowData=DF[['country','year','CO2 emissions (kt)']].to_dict('records'),
                columnDefs=[{'field': i} for i in DF[['country','year','CO2 emissions (kt)']].columns],
                className="ag-theme-alpine-dark",
                columnSize="sizeToFit"), 
                width = 6), 
                justify="center", className='mt-4'),
        ]
    ),
    className="mt-3",
)

# Tab 3 Content
tab3_content = dbc.Card(
    dbc.CardBody(
        [
            html.H2(
                "GDP per capita growth Comparison", 
                className="card-text text-center"),
            # Insert multiple country options
            html.Div(
                dcc.Dropdown(
                    id='tab_3_drop_down',
                    multi=True,
                    options=[
                        {
                          'label': name,
                          'value': name
                        }
                        for name in sorted(DF['country'].unique())
                    ],
                    value = DF['country'].unique(),
                ), 
                className= 'mb-4' 
            ),
            # Insert the Graph
            dcc.Graph(
                id='tab_3_line_chart',
                figure={}
            ),
             # Insert an AgGrid for tab 3
            dbc.Row(
            dbc.Col(
            dag.AgGrid(
                # Insert ID
                id='tab_3_grid',
                rowData=DF[['country','year','GDP per capita growth (annual %)']].to_dict('records'),
                columnDefs=[{'field': i} for i in DF[['country','year','GDP per capita growth (annual %)']].columns],
                className="ag-theme-alpine-dark",
                columnSize="sizeToFit"), 
                width = 6), 
                justify="center", className='mt-4'),

        ]
    ),
    className="mt-3",
)


# Tab 4 Content
tab4_content = dbc.Card(
    dbc.CardBody(
        [
            html.H2(
                "Life Expectancy at Birth", 
                className="card-text text-center"),
            # Insert multiple country options
            html.Div(
                dcc.Dropdown(
                    id='tab_4_drop_down',
                    multi=True,
                    options=[
                        {
                          'label': name,
                          'value': name
                        }
                        for name in sorted(DF['country'].unique())
                    ],
                    value = DF['country'].unique(),
                ), 
                className= 'mb-4' 
            ),
            # Insert the Graph
            dcc.Graph(
                id='tab_4_line_chart',
                figure={}
            ),
            # Insert an AgGrid for tab 4
            dbc.Row(
            dbc.Col(
            dag.AgGrid(
                # Insert ID
                id='tab_4_grid',
                rowData=DF[['country','year','Life expectancy at birth, total (years)']].to_dict('records'),
                columnDefs=[{'field': i} for i in DF[['country','year','Life expectancy at birth, total (years)']].columns],
                className="ag-theme-alpine-dark",
                columnSize="sizeToFit"), 
                width = 6), 
                justify="center", className='mt-4'),

        ]
    ),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        # Tab 1
        dbc.Tab(
                tab1_content, 
                label="Country Comparision", 
                tab_id='tab_1',
        ),
        # Tab 4
        dbc.Tab(
                tab4_content, 
                label="Life expectancy at birth Comparison",
                tab_id='tab_4'),
        # Tab 2
        dbc.Tab(
                tab2_content, 
                label="CO2 Emissions Comparison",
                tab_id='tab_2',
        ),           
        # Tab 3
        dbc.Tab(
                tab3_content, 
                label="GDP per capita growth (annual %) Comparison",
                tab_id='tab_3'),

    ],
        # Tab id
        id = 'tabs',
        active_tab='tab_1'
)

# App Layout
app.layout = dbc.Container(
    [
        # Row 1
        dbc.Row(
            [
                # Heading
                dbc.Col(
                    html.H1(
                        "Covid vs Recession Impacts",
                        className="text-center bg-primary text-white p-2 mt-4",    
                    ),
                ),
            ]
        ),
        # Row 2
        dbc.Row(
            [
                dbc.Col(
                    # Insert Tabs
                    tabs,
                ),
            ]
        ),        
       # Store dashboard data in-memory
       dcc.Store(
                id='storage',
                storage_type='session',
                data = {}
       ),
       # Refresh the app
       dcc.Interval(
                id = 'timer',
                interval = 1000 * 60,
                n_intervals=0
       ), 
    ]
)





# TODO 2: Callback to get the data
@app.callback(
    # Output to the storage
    Output(component_id='storage',
           component_property='data'),
    # Input
    Input(component_id='timer',
         component_property='n_intervals')
)
# The update function
def update_data(n_time):
    df = update_wb_data()
    return df.to_dict('records')


# Create the Choropleth graph

@app.callback(
    # Tab 1 Ouput
    Output(component_id='my-choropleth', 
           component_property='figure'
          ),
    # Tab 2 Output Line Chart
    Output(
        component_id='tab_2_line_chart', 
        component_property='figure'
        ),
    # Tab 2 Output AgGrid
    Output(
        component_id='tab_2_grid',
        component_property='rowData',
    ),
    # Tab 3 Output
    Output(
        component_id='tab_3_line_chart', 
        component_property='figure'
        ),
    # Tab 3 Output AgGrid
    Output(
        component_id='tab_3_grid',
        component_property='rowData',
    ),
    # Tab 4 Output
    Output(
        component_id='tab_4_line_chart', 
        component_property='figure'
        ),
    # Tab 3 Output AgGrid
    Output(
        component_id='tab_4_grid',
        component_property='rowData',
    ),
    # Input 1- Button click
    Input(component_id='my-button',
         component_property='n_clicks'
         ),
    # Input - Data stored by the first callback
    Input(component_id='storage',
          component_property='data'),
    # Tab input
    Input(component_id='tabs',
         component_property='active_tab'),
    # Tab 2
    Input(
        component_id='tab_2_drop_down', 
        component_property='value'
    ),
    # Tab 3
    Input(
        component_id='tab_3_drop_down', 
        component_property='value'
    ),
    # Tab 4
    Input(
        component_id='tab_4_drop_down', 
        component_property='value'
    ),
    # Capture user input but only update when the button is clicked
    State('years-range','value'),
    State('radio-indicator','value')
)
# Update function
def update_graph(n_clicks, stored_df, active_tab, tab_2_options, 
                 tab_3_options, tab_4_options, years_chosen, 
                 indicator_chosen):
    # Get the stored_df from the browser
    df_ = pd.DataFrame(stored_df)
    # If there is an interval
    if active_tab == 'tab_1':
        if years_chosen[1] != years_chosen[0]:
            year_mask = df_['year'].between(int(years_chosen[0]), int(years_chosen[1]))
            df_ = (
                    # Select the chosen records
                    df_.loc[year_mask]
                    # Group by the iso3c and country
                    .groupby(
                        ['iso3c','country']
                    )
                    # Select the indictor chosen
                    [indicator_chosen]
                    # Get the mean
                    .mean()
                    # Reset the index
                    .reset_index()
                  )
            fig = px.choropleth(
                data_frame=df_,
                locations='iso3c',
                color=indicator_chosen,
                scope='world',
                hover_data={
                    'iso3c': False,
                    'country': True
                        },)
       
            fig.update_layout(
                geo={"projection": {"type": "natural earth"}},
                margin=dict(l=50, r=50, t=50, b=50),
            )
            # Update tab1 only
            return fig, no_update, no_update, no_update, no_update, no_update, no_update
    
        # If there is no interval
        if years_chosen[1] == years_chosen[0]:
            year_mask = df_['year'].isin(int(years_chosen))
            df_ = (
                    # Select the chosen records
                    df_.loc[year_mask]
                    # Group by the iso3c and country
                    .groupby(
                        ['iso3c','country']
                    )
                    # Select the indictor chosen
                    [indicator_chosen]
                    # Get the mean
                    .mean()
                    # Reset the index
                    .reset_index()
                  )
            fig = px.choropleth(
                data_frame=df_,
                locations='iso3c',
                color=indicator_chosen,
                scope='world',
                hover_data={
                    'iso3c': False,
                    'country': True
                        },)

            fig.update_layout(
                geo={"projection": {"type": "natural earth"}},
                margin=dict(l=50, r=50, t=50, b=50),
            )
            # Update tab 1 only
            return fig, no_update, no_update, no_update, no_update, no_update, no_update

    elif active_tab == 'tab_2':
        # Check drop_down options
        if not tab_2_options:
            # Return Empty Dict
            ag_grid_2_dict = (pd.DataFrame({
                                'country': [np.nan],
                                'year': [np.nan],
                                'CO2 emissions (kt)': [np.nan],
                            }).to_dict('records'))
            # Update tab 2 only
            return no_update, {}, ag_grid_2_dict, no_update, no_update, no_update, no_update

        # Get the drop_down options
        drop_down_mask_2 = df_['country'].isin(tab_2_options)
        # Grab the filtered df
        filtered_df_2 = df_.loc[drop_down_mask_2]
        # Get the dict for Ag Grid
        ag_grid_2_dict = filtered_df_2[['country', 'year', 'CO2 emissions (kt)']].to_dict('records')
        # print(ag_grid_2_dict)
        # Update the fig
        fig = px.line(
            data_frame = filtered_df_2,
            x = 'year',
            y = 'CO2 emissions (kt)',
            # log_y = True,
            color = 'country',
        )
        # Update tab 2 only
        return no_update, fig, ag_grid_2_dict, no_update, no_update, no_update, no_update


    elif active_tab == 'tab_3':
        # Check drop_down options
        if not tab_3_options:
            # Return Empty Dict
            ag_grid_3_dict = (pd.DataFrame({
                                'country': [np.nan],
                                'year': [np.nan],
                                'GDP per capita growth (annual %)': [np.nan],
                            }).to_dict('records'))
            # Update tab 3 only
            return no_update, no_update, no_update, {}, ag_grid_3_dict, no_update, no_update

        
        # Get the drop_down options
        drop_down_mask_3 = df_['country'].isin(tab_3_options)
        # Grab the filtered df
        filtered_df_3 = df_.loc[drop_down_mask_3]
        # Get the dict for Ag Grid
        ag_grid_3_dict = filtered_df_3[['country', 'year', 'GDP per capita growth (annual %)']].to_dict('records')
        # Update the fig
        fig = px.line(
            data_frame = filtered_df_3,
            x = 'year',
            y = 'GDP per capita growth (annual %)',
            # log_y = True,
            color = 'country',
        )
        # Update tab 3 only
        return no_update, no_update, no_update, fig, ag_grid_3_dict, no_update, no_update

    elif active_tab == 'tab_4':
        # Check drop_down options
        if not tab_4_options:
            # Return Empty Dict
            ag_grid_4_dict = (pd.DataFrame({
                                'country': [np.nan],
                                'year': [np.nan],
                                'Life expectancy at birth, total (years)': [np.nan],
                            }).to_dict('records'))
            # Update tab 4 only
            return no_update, no_update, no_update, no_update, no_update, {}, ag_grid_4_dict

        # Get the drop_down options
        drop_down_mask_4 = df_['country'].isin(tab_4_options)
        # Grab the filtered df
        filtered_df_4 = df_.loc[drop_down_mask_4]
        # Get the dict for Ag Grid
        ag_grid_4_dict = filtered_df_4[['country', 'year', 'Life expectancy at birth, total (years)']].to_dict('records')
        # Update the fig
        fig = px.line(
            data_frame = filtered_df_4,
            x = 'year',
            y = 'Life expectancy at birth, total (years)',
            # log_y = True,
            color = 'country',
        )
        # Update tab 4 only
        return no_update, no_update, no_update, no_update, no_update, fig, ag_grid_4_dict 




# Insert Main
if __name__ == '__main__':
    app.run_server(
        debug=True,
        host='127.0.0.1', 
        port='7090'
    )


