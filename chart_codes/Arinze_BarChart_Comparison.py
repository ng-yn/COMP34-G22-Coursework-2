# Created by Arinze David Nwanna

from Model import Stock
import plotly.graph_objects as go

AAPL = Stock('AAPL')
AMZN = Stock('AMZN')

QuarterlyAAPL = AAPL.income_statement_quarterly()
AnnualAAPL = AAPL.income_statement_quarterly()
QuarterlyAMZN = AMZN.income_statement_quarterly()
AnnualAMZN = AMZN.income_statement_quarterly()

years = QuarterlyAAPL.index

totalRevAAPL = QuarterlyAAPL['totalRevenue']
totalRevAMZN = QuarterlyAMZN['totalRevenue']

totalRevAAPL_rev = []
totalRevAMZN_rev = []

for revs in totalRevAAPL:
    totalRevAAPL_rev.append(totalRevAAPL[-1])

for revs in totalRevAMZN:
    totalRevAAPL_rev.append(totalRevAMZN[-1])

A = list(totalRevAAPL)
AZ = list(totalRevAMZN)
year = list(QuarterlyAAPL.index)


fig = go.Figure()
fig.add_trace(go.Bar(x=years,
                y=A,
                name='AAPL Total Revenue',
                marker_color='rgb(55, 83, 100)'
                ))
fig.add_trace(go.Bar(x=years,
                y=AZ,
                name='AMZN Total Revenue',
                marker_color='rgb(26, 118, 255)'
                ))

fig.update_layout(
    title='Total Revenue',
    xaxis_tickfont_size=14,
    xaxis=dict(
        title='Date (years)',
        titlefont_size=16,
    ),
    yaxis=dict(
        title='USD (millions)',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig.show()
