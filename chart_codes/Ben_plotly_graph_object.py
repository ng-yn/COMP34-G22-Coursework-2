# COMP0034 CW1 Group 22
# Code create by Yu-Hsiang Chen
# STN : 18035617

import pandas as pd
import plotly.graph_objects as go
import sqlite3

def plotly_graph_object(label,value):
    conn = sqlite3.connect('../my_app/data/FinancialDatabase.db')
    df = pd.read_sql_query("SELECT * from {}".format(label), conn)
    df_plot = df[['timestamp', 'open', 'high', 'low', 'close', 'adjusted_close']]
    # Since the database includes more than 10 year of data, I only use the latest 200 days' data
    df_plot = df_plot.head(value)
    # using candlestick chart with plotly graph object to plot the stock price
    fig = go.Figure(go.Candlestick(x=df_plot['timestamp'], open=df_plot['open'],
                           high=df_plot['high'], low=df_plot['low'],
                           close=df_plot['close'], name = 'Stock Price'))
    # adding the moving average line with two different period
    ma_10 = df_plot['close'].rolling(10, min_periods=1).mean()
    ma_50 = df_plot['close'].rolling(50, min_periods=1).mean()
    fig.add_trace(go.Scatter(x = df_plot['timestamp'], y = ma_10, line=dict(color='royalblue')
                             , name = 'Moving Average 10'))
    fig.add_trace(go.Scatter(x = df_plot['timestamp'], y = ma_50, line=dict(color='chocolate')
                             , name = 'Moving Average 50'))
    # set the chart title and axis label to the chart
    fig.update_layout(
        title="{} Stock Price".format(label),
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        legend_title="Technical Data",
        font=dict( size=18, color="Black")
    )
    fig.show()
    return fig

plotly_graph_object("MMM",200)
