# Created by Arinze David Nwanna

import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import matplotlib.dates as mdates
from models import Stock

# import data using models
AAPL = Stock('AAPL')
AMZN = Stock('AMZN')
QuarterlyAAPL = AAPL.income_statement_quarterly()
AnnualAAPL = AAPL.income_statement_annual()
QuarterlyAMZN = AMZN.income_statement_quarterly()
AnnualAMZN = AMZN.income_statement_annual()

QZGP = []

# Convert the income statement into integers via list

for i in QuarterlyAMZN.grossProfit:
    a = int(i)
    QZGP.append(int(a / 10 ** 6))  # USD millions

AAPL = pd.DataFrame()
AAPL['Date'] = QuarterlyAAPL.index
AAPL['Gross Profits US$millions'] = QZGP
AAPL.set_index('Date', inplace=True)

# time= pd.to_datetime(AAPL['Date'])

AAPL['date'] = mdates.date2num(dt)
Y = AAPL['Gross Profits US$millions']
X = AAPL['date']

# regression
reg = LinearRegression().fit(np.vstack(X), Y)
AAPL['Bestfit'] = reg.predict(np.vstack(X))

# plotly figure setup
fig = go.Figure()

fig.add_trace(go.Bar(name='Gross Profits US$millions', x=AAPL.index, y=Y.values))
fig.add_trace(go.Scatter(name='Linear Regression', x=AAPL.index, y=AAPL['Bestfit'], mode='lines'))

fig.update_layout(

    title={
        'text': 'Gross Profits in US$ (millions) of AAPL over 5 last years',
        'y': 0.85,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_tickfont_size=14,
    xaxis=dict(
        title='Date',
        titlefont_size=12,
        tickfont_size=12),
    yaxis=dict(
        title='Gross Profits US$ (millions)',
        titlefont_size=12,
        tickfont_size=12))

fig.write_image("BarChart3.png")
