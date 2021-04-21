#Luke Williams 18051086
import sqlite3
import pandas as pd
import plotly.graph_objects as go

#Connect to database and create dataframe using fundamental data
conn = sqlite3.connect('../my_app/data/FinancialDatabase.db')
SQL_Query = pd.read_sql_query("SELECT Sector, MarketCapitalization, FullTimeEmployees FROM FUNDAMENTALS", conn)

#loop through dataframe and create dictionary which calculates the sum of mktcap and employees for each sector
mktcap = {}
employees = {}
for index, row in SQL_Query.iterrows():
    if row['Sector'] not in mktcap:
        mktcap[row['Sector']] = row['MarketCapitalization']
        employees[row['Sector']] = row['FullTimeEmployees']
    else:
        mktcap[row['Sector']] += row['MarketCapitalization']
        employees[row['Sector']] += row['FullTimeEmployees']

#create 2 new dataframes of the sector market cap and sector employees data
df_mktcap = pd.DataFrame(mktcap.items(), columns = ['Sector', 'MarketCapitalization'])
df_employees = pd.DataFrame(employees.items(), columns = ['Sector', 'FullTimeEmployees'])

#sort dataframes by market cap and fulltime employees
df_mktcap.sort_values(by=['MarketCapitalization'], inplace=True, ascending=True)
df_employees.sort_values(by=['FullTimeEmployees'], inplace=True, ascending=True)

#Creating the 2 scatter plots
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=list(df_mktcap['Sector']),
    y=list(df_mktcap['MarketCapitalization']),
    name = 'Market Cap',
    mode = 'markers'
))
fig.add_trace(go.Scatter(
    x=list(df_mktcap['Sector']),
    y=list(df_employees['FullTimeEmployees']),
    name='Number of Employees',
    mode='markers',
    yaxis='y2'
))

#Updating layout to give 2 yaxis and keep the plot overlapped on the same figure
fig.update_layout(
    xaxis=dict(
        domain=[0.1, 1]
    ),
    yaxis=dict(
        title="Sector Market Cap (USD)",
        titlefont=dict(
            color="#1f77b4"
        ),
        tickfont=dict(
            color="#1f77b4"
        )
    ),
    yaxis2=dict(
        title="Sector Full time Employees",
        titlefont=dict(
            color="#ff7f0e"
        ),
        tickfont=dict(
            color="#ff7f0e"
        ),
        anchor="x",
        overlaying="y",
        side="right",
        position=0.15
    )
)
#Title and size of figure
fig.update_layout(
    title_text="Sector Market Cap & Full Time Employees - Double y-axis plot",
    width=1200,
)
fig.show()
