# Created by Joshua Ng
# This code is used for defining multiple functions used in dash_app_joshua.py

import plotly.express as px
import pandas as pd
import sqlite3

def peratio(sort, size, sector):
    # Index in sector_list used as a reference for sector variable in the methods below
    sector_list = ['All',
                   'Basic Materials',
                   'Communication Services',
                   'Consumer Cyclical',
                   'Consumer Defensive',
                   'Energy',
                   'Financial Services',
                   'Healthcare',
                   'Industrials',
                   'Real Estate',
                   'Technology',
                   'Utilities'
                   ]
    # Connecting to sqlite3 to import data into dataframe
    connection = sqlite3.connect('../my_app/data/FinancialDatabase.db')
    sql_query = pd.read_sql_query('SELECT Symbol, Name, Sector, PERatio FROM FUNDAMENTALS', connection)
    df = pd.DataFrame(sql_query, columns=['Symbol', 'Name', 'Sector', 'PERatio'])
    df = df[df.PERatio != 'None']  # Removes 'None" strings in PERatio column
    # User can choose to either sort by ascending or descending order (Of the P/E Ratio)
    df = df.sort_values(by=['PERatio'], ascending=sort)

    if sector == 0:
        # Creating bar chart for all available companies
        df = df.head(n=size)
        fig1 = px.bar(df, x='Symbol', y='PERatio',
                      labels={'Symbol': 'Company', 'PERatio': 'P/E Ratio'},
                      color='Sector',
                      template='simple_white'
                      )
        fig1.update_layout(title_text='P/E Ratios of S&P 500 stocks', title_x=0.5)
    else:
        # Creating bar chart for selected sector
        chosen_sector = sector_list[sector]
        df = df[df.Sector.str.contains(chosen_sector)]
        df = df.head(n=size)
        fig1 = px.bar(df, x='Symbol', y='PERatio', title='P/E Ratios of S&P 500 stocks',
                      labels={'Symbol': 'Company', 'PERatio': 'P/E Ratio'},
                      template='simple_white'
                      )
        fig1.update_layout(title_text='P/E Ratios of S&P 500 stocks', title_x=0.5)
    return fig1


# Function used to calculate mean P/E ratio of a sector
def pe_mean(sector):
    sector_list = ['All',
                   'Basic Materials',
                   'Communication Services',
                   'Consumer Cyclical',
                   'Consumer Defensive',
                   'Energy',
                   'Financial Services',
                   'Healthcare',
                   'Industrials',
                   'Real Estate',
                   'Technology',
                   'Utilities'
                   ]
    connection = sqlite3.connect('../my_app/data/FinancialDatabase.db')
    sql_query = pd.read_sql_query('SELECT Symbol, Name, Sector, PERatio FROM FUNDAMENTALS', connection)
    df = pd.DataFrame(sql_query, columns=['Symbol', 'Name', 'Sector', 'PERatio'])
    df = df[df.PERatio != 'None']  # Removes 'None" strings in PERatio column
    if sector == 0:
        # Calculating mean for all available companies
        mean = df.PERatio.mean()

    else:
        # Calculating mean for selected sector
        chosen_sector = sector_list[sector]
        df = df[df.Sector.str.contains(chosen_sector)]
        mean = df.PERatio.mean()

    return mean


# Function used to calculate median P/E ratio of a sector
def pe_median(sector):
    sector_list = ['All',
                   'Basic Materials',
                   'Communication Services',
                   'Consumer Cyclical',
                   'Consumer Defensive',
                   'Energy',
                   'Financial Services',
                   'Healthcare',
                   'Industrials',
                   'Real Estate',
                   'Technology',
                   'Utilities'
                   ]
    connection = sqlite3.connect('../my_app/data/FinancialDatabase.db')
    sql_query = pd.read_sql_query('SELECT Symbol, Name, Sector, PERatio FROM FUNDAMENTALS', connection)
    df = pd.DataFrame(sql_query, columns=['Symbol', 'Name', 'Sector', 'PERatio'])
    df = df[df.PERatio != 'None']  # Removes 'None" strings in PERatio column
    if sector == 0:
        # Calculating median for all available companies
        median = df.PERatio.median()

    else:
        # Calculating median for selected sector
        chosen_sector = sector_list[sector]
        df = df[df.Sector.str.contains(chosen_sector)]
        median = df.PERatio.median()

    return median

