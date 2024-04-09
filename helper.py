"""
    This Python File shows how to download data from the World Bank databse with Pandas
"""
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from pandas_datareader import wb

# Get the Countries
countries_df = wb.get_countries()


# Grab the countries with associated country codes
count_codes_df = (
    countries_df
    .assign(
        # Replace Empty capital cities
        capitalCity = lambda df_: df_['capitalCity'].replace({'': None}),
    )
    # Drop null capital city values
    .loc[lambda df_: ~(df_['capitalCity'].isna())]
    # Take out Kosovo
    .loc[lambda df_: df_['capitalCity'].ne('Kosovo')]
    # Select the name and iso3c cols
    [['name','iso3c']]
    # Rename the cols
    .rename(columns={
        'name': 'country'
    })
)



# Getting the WB indicators
ind_df = wb.get_indicators()


indicators = {
    'IT.NET.USER.ZS': 'Individuals using the Internet (% of population)',
    'SG.GEN.PARL.ZS':'Proportion of seats held by women in national parliaments (%)',
    'EN.ATM.CO2E.KT':'CO2 emissions (kt)',
    'SH.STA.MMRT':'Maternal mortality ratio (modeled estimate, per 100,000 live births)',
    # 'HF.DYN.AIDS.ZS':'Prevalence of HIV, total (% of population ages 15-49)',
    'SH.DYN.MORT':'Mortality rate, under-5 (per 1,000 live births)',
    'NY.GDP.PCAP.KD.ZG':'GDP per capita growth (annual %)',
    'SP.DYN.LE00.IN':'Life expectancy at birth, total (years)',    
}

select_countries = ['GHA', 'MYS', 'DEU', 'USA', 'NGA', 'CAN']

def update_wb_data():
    # Retrieve specific World Bank data from API
    df = wb.download(
        indicator = list(indicators),
        country = count_codes_df['iso3c'],
        start = 2004,
        end = 2021
    )
    # DF Reset index
    df = df.reset_index()
    # Add the country
    merged_df = (
                    # Merge the DF
                    pd.merge(df, count_codes_df, on='country')
                    .assign(
                        # Convert the year to int
                        year = lambda df_: df_['year'].astype('int'),
                    )
                    # Select the countries of choice
                    .loc[ lambda df_: df_['iso3c'].isin(select_countries) ]
    )
    # Rename the indicators
    merged_df = (
                    merged_df.rename(
                        columns=indicators
                                )
                # Round the entire DS to 2DP
                .round(decimals=2)
                )
    
    return merged_df