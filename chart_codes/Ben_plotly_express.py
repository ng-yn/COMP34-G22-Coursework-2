# COMP0034 CW1 Group 22
# Code create by Yu-Hsiang Chen
# STN : 18035617

import pandas as pd
import plotly.express as px
import sqlite3

#connect to the database
conn = sqlite3.connect('../my_app/data/FinancialDatabase.db')


def plotly_express():
    SQL_Query = pd.read_sql_query("SELECT Symbol, Name, Sector, MarketCapitalization FROM FUNDAMENTALS", conn)
    df1 = pd.DataFrame(SQL_Query, columns=['Symbol', 'Name', 'Sector', 'MarketCapitalization'])
    df1_plot = df1.copy()
    # make the market cap unit to trillion for better visualization
    df1_plot['MarketCapitalization (Trillion USD)'] = df1_plot['MarketCapitalization'] / 10e11
    size = df1_plot['MarketCapitalization (Trillion USD)']
    label = df1_plot['Symbol']
    # plot the treemap showing ranking of the market cap with different industry sector
    fig = px.treemap(df1_plot,
                     path=['Sector', 'Symbol'],
                     values='MarketCapitalization (Trillion USD)',
                     color='MarketCapitalization (Trillion USD)',
                     color_continuous_scale='Aggrnyl')
    fig.update_layout(
        title="S&P 500 Companies Market Cap",
        font=dict(size=14, color="Black")
    )
    fig.show()

plotly_express()
