# Richard Gao 18017045
import plotly.graph_objects as go
import pandas as pd
import sqlite3

conn = sqlite3.connect('../my_app/data/FinancialDatabase.db')


# Creates a grouped bar chart showing the pe, pb and peg ratios of 5 selected companies
def key_ratios(ticker1, ticker2, ticker3, ticker4, ticker5):
    # Create a dataframe of the symbols and ratios of every company in the database using the "Fundamentals" table
    df = pd.read_sql_query("select Symbol, PERatio, PEGRatio, PriceToBookRatio from Fundamentals;", conn)

    # Loop through the dataframe to find the index of the selected companies
    tickers = [ticker1, ticker2, ticker3, ticker4, ticker5]
    index = []
    for i in range(len(tickers)):
        for j in range(len(df["Symbol"])):
            if df["Symbol"][j] == tickers[i]:
                index.append(j)

    # Make new dataframes of only the selected companies and their ratios
    x = [ticker1, ticker2, ticker3, ticker4, ticker5]
    pe = df["PERatio"][index[0:]]
    peg = df["PEGRatio"][index[0:]]
    pb = df["PriceToBookRatio"][index[0:]]

    # Use plotly graph objects to create the bar charts
    fig = go.Figure(data=[
        go.Bar(name="PEG", x=x, y=peg, text=peg, textposition="auto", marker_color="#6da7de"),
        go.Bar(name="P/B", x=x, y=pb, text=pb, textposition="auto", marker_color="#9e0059"),
        go.Bar(name="P/E", x=x, y=pe, text=pe, textposition="auto", marker_color="#dee000")
    ])
    fig.update_layout(barmode="group", title_text="Grouped Bar Chart Comparing Key Ratios of Selected Stocks",
                      xaxis={'categoryorder': 'category ascending'})
    fig.show()
