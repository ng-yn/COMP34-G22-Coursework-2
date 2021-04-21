# Created By Joshua Ng
# This code is for the bullet chart that displays the fundamental data of a company

import pandas as pd
import plotly.graph_objects as go
import sqlite3

# Importing fundamental data set
connection = sqlite3.connect('../my_app/data/FinancialDatabase.db')
sql_query = pd.read_sql_query('SELECT Symbol, PERatio, PEGRatio, PriceToBookRatio, EBITDA'
                              ' FROM FUNDAMENTALS', connection)
df = pd.DataFrame(sql_query, columns=['Symbol', 'PERatio', 'PEGRatio', 'PriceToBookRatio', 'EBITDA'])

# Calculating S&P 500 index means
mean_pe = round(df[df.PERatio != 'None'].PERatio.mean(), 2)
mean_peg = round(df[df.PEGRatio != 'None'].PEGRatio.mean(), 2)
mean_pb = round(df[df.PriceToBookRatio != 'None'].PriceToBookRatio.mean(), 2)
mean_ebitda = round(df[df.EBITDA != 'None'].EBITDA.mean())

# Creating dataframe for PYPL Stock
df_stock = df[df.Symbol == 'PYPL']
df_stock = df_stock.round(2)

# Creating empty figure and adding individual bullet charts
fig = go.Figure()

# For P/E Ratio
fig.add_trace(go.Indicator(
    mode='number+gauge+delta',
    gauge={'shape': 'bullet',
           'axis': {'range': [None, 100]},
           'threshold': {
               'line': {'color': 'red', 'width': 2},
               'thickness': 1,
               'value': mean_pe
           },
           'bgcolor': 'white',
           'bar': {'color': 'green'}
           },
    value=df_stock.iloc[0]['PERatio'],
    delta={'reference': mean_pe, 'position': 'top'},
    domain={'x': [0.15, 1], 'y': [0.75, 0.9]},
    title={'text': 'P/E Ratio'},
))

# For PEG Ratio
fig.add_trace(go.Indicator(
    mode='number+gauge+delta',
    gauge={'shape': 'bullet',
           'axis': {'range': [None, 10]},
           'threshold': {
               'line': {'color': 'red', 'width': 2},
               'thickness': 1,
               'value': mean_peg
           },
           'bgcolor': 'white',
           'bar': {'color': 'green'}
           },
    value=df_stock.iloc[0]['PEGRatio'],
    delta={'reference': mean_peg, 'position': 'top'},
    domain={'x': [0.15, 1], 'y': [0.5, 0.65]},
    title={'text': 'PEG Ratio'},
))

# For P/B Ratio
fig.add_trace(go.Indicator(
    mode='number+gauge+delta',
    gauge={'shape': 'bullet',
           'axis': {'range': [None, 20]},
           'threshold': {
               'line': {'color': 'red', 'width': 2},
               'thickness': 1,
               'value': mean_pb
           },
           'bgcolor': 'white',
           'bar': {'color': 'green'}
           },
    value=df_stock.iloc[0]['PriceToBookRatio'],
    delta={'reference': mean_pb, 'position': 'top'},
    domain={'x': [0.15, 1], 'y': [0.25, 0.4]},
    title={'text': 'P/B Ratio'},
))

# For EBITDA
fig.add_trace(go.Indicator(
    mode='number+gauge+delta',
    gauge={'shape': 'bullet',
           'axis': {'range': [None, 5000000000]},
           'threshold': {
               'line': {'color': 'red', 'width': 2},
               'thickness': 1,
               'value': mean_ebitda
           },
           'bgcolor': 'white',
           'bar': {'color': 'green'}
           },
    value=df_stock.iloc[0]['EBITDA'],
    delta={'reference': mean_ebitda, 'position': 'top'},
    domain={'x': [0.15, 1], 'y': [0, 0.15]},
    title={'text': 'EBITDA'},
))
fig.update_layout(height=800,
                  title='Fundamental Data of PYPL',
                  title_x=0.5,
                  font=dict(
                      size=18
                  ))

fig.show()


