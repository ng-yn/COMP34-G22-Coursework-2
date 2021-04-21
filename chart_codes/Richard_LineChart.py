# Richard Gao 18017045
import plotly.graph_objects as go
import pandas as pd
import sqlite3

conn = sqlite3.connect('../my_app/data/FinancialDatabase.db', check_same_thread=False)


# Create a line chart showing the price movement of the top 10 companies by market cap in a selected sector
def top10_price_movement(sector):
    # Create a dataframe of the symbol, sector and market cap of all companies in the database and sort by market cap
    df = pd.read_sql_query("select Symbol, MarketCapitalization, Sector from Fundamentals", conn)
    df.sort_values(by=["MarketCapitalization"], inplace=True, ascending=False)
    df = df.reset_index(drop=True)

    # Loop through the dataframe to find the top 10 companies in the given sector
    top10 = []
    for i in range(len(df["Sector"])):
        if df["Sector"][i] == sector:
            if len(top10) < 10:
                top10.append(df["Symbol"][i])

    # Create a dictionary of dataframes of the top10 companies
    df_dict = {}
    for i in range(10):
        df = pd.read_sql_query("select timestamp, adjusted_close from {}".format(top10[i]), conn)
        df_dict[i] = df

    # Create a chart and loop through the dictionary to add the dataframes to it
    fig = go.Figure()
    for i in range(10):
        fig.add_trace(go.Scatter(x=df_dict[i]["timestamp"], y=df_dict[i]["adjusted_close"], mode="lines",
                                 name="{}".format(top10[i])))

    # Configure the layout of the chart
    fig.update_layout(title='Price Movement of the Top 10 Stocks in the {} Sector'.format(sector),
                      xaxis_title='Date (use the sliders to change the timeframe)',
                      yaxis_title='Price',
                      xaxis=dict(
                          rangeselector=dict(
                              buttons=list([
                                  dict(count=1,
                                       label="1m",
                                       step="month",
                                       stepmode="backward"),
                                  dict(count=6,
                                       label="6m",
                                       step="month",
                                       stepmode="backward"),
                                  dict(count=1,
                                       label="YTD",
                                       step="year",
                                       stepmode="todate"),
                                  dict(count=1,
                                       label="1y",
                                       step="year",
                                       stepmode="backward"),
                                  dict(step="all")
                              ])
                          ),
                          rangeslider=dict(
                              visible=True
                          ),
                          type="date"
                      )
                      )
    return fig
