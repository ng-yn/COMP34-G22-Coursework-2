# Created by Arinze David Nwanna

import pandas as pd
import sqlite3
import plotly.graph_objects as go
import os

# Create dataframe
con = sqlite3.connect("../my_app/data/FinancialDatabase.db")
AAPL = pd.read_sql_query("SELECT * from AAPL", con)
AAPL.set_index('timestamp', inplace=True)
AAPL = AAPL.head(50)

# Create figure
fig1 = go.Figure(data=[go.Candlestick(x=AAPL.index,
                                     open=AAPL['open'],
                                     high=AAPL['high'],
                                     low=AAPL['low'],
                                     close=AAPL['close'])])

fig1.update_layout(title="AAPL Candlestick Chart",
                  xaxis_title="Date",
                  yaxis_title="Price $",
                  font=dict(
                      family="Times New Roman, Times, serif",
                      size=14,
                      color="Black"))

# Save image to local disk
if not os.path.exists("/Users/arinze/PycharmProjects/Activity1COMP0034/Charts"):
    os.mkdir("/Users/arinze/PycharmProjects/Activity1COMP0034/Charts")

fig1.write_image("/Users/arinze/PycharmProjects/Activity1COMP0034/Charts/SingleStockCandlestick.png")
