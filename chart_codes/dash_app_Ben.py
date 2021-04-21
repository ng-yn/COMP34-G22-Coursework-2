import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import sqlite3
import pandas as pd

def plotly_graph_object(label,label1,value):
    conn = sqlite3.connect('../my_app/data/FinancialDatabase.db')
    df = pd.read_sql_query("SELECT * from {}".format(label), conn)
    df_plot = df[['timestamp', 'open', 'high', 'low', 'close', 'adjusted_close']]
    # Since the database includes more than 10 year of data, I only use the latest 200 days' data
    df_plot = df_plot.head(value)
    df1 = pd.read_sql_query("SELECT * from {}".format(label1), conn)
    df1_plot = df1[['timestamp', 'open', 'high', 'low', 'close', 'adjusted_close']]
    # Since the database includes more than 10 year of data, I only use the latest 200 days' data
    df1_plot = df1_plot.head(value)
    # using candlestick chart with plotly graph object to plot the stock price
    fig = go.Figure(go.Candlestick(x=df_plot['timestamp'], open=df_plot['open'],
                                   high=df_plot['high'], low=df_plot['low'],
                                   close=df_plot['close'], name='{} Stock Price'.format(label)))
    fig.add_trace(go.Scatter(x = df1_plot['timestamp'], y = df1_plot['adjusted_close'], line=dict(color='royalblue')
                             , name = '{} stock price'.format(label1)))
    # set the chart title and axis label to the chart
    fig.update_layout(
        title="Stock Compare",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        legend_title="Company",
        font=dict( size=18, color="Black")
    )
    return fig

fig = plotly_graph_object("AMD","MMM",200)

dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

dash_app.layout = dbc.Container(fluid=True, children=[
        html.Br(),
        html.H1('S&P 500 Dashboard'),
        html.P('Learn how to invest in stock market',
               className='lead'),

        # Add the first row here
        dbc.Row([
            # Add the first column here. This is for the area selector and the statistics panel.
            dbc.Col(width=3, children=[
                dbc.FormGroup([
                    html.H4("Select first company"),
                    # dash-core-components (dcc) provides a dropdown
                    dcc.Dropdown(id="company_select1", options=[{"label": 'Apple (AAPL)', "value": 'AAPL'}, {"label": '3M Company (MMM)', "value": 'MMM'},
                                                                {"label": 'Advanced Micro Device (AMD)', "value": 'AMD'}, {"label": 'eBay (EBAY)', "value": 'EBAY'},
                                                                {"label": 'Facebook (FB)', "value": 'FB'}],
                                 value="AMD"),
                    html.H4("Select second company"),
                    # dash-core-components (dcc) provides a dropdown
                    dcc.Dropdown(id="company_select2", options=[{"label": 'Apple (AAPL)', "value": 'AAPL'}, {"label": '3M Company (MMM)', "value": 'MMM'},
                                                                {"label": 'Advanced Micro Device (AMD)', "value": 'AMD'},{"label": 'eBay (EBAY)', "value": 'EBAY'},
                                                                {"label": 'Facebook (FB)', "value": 'FB'}],
                                 value="MMM")
                ]),
            ]),
            # Add the second column here. This is for the figure.
            dbc.Col(width=9, children=[
                html.H2('Stock Data'),
                dcc.Graph(id = "fig", figure=fig),
                dcc.Slider(
                id='slider',
                min=1,
                max=500,
                step=1,
                marks={i: 'Day Range {}'.format(i) for i in range(0, 500, 50)}
                )

            ]),
        ]),
    ])

@dash_app.callback(
    Output(component_id="fig", component_property="figure"),
     [Input(component_id="company_select1", component_property="value"),
      Input(component_id="company_select2", component_property="value"),
      Input(component_id="slider", component_property="value")]
)

def plotly_graph_object(label,label1,value):
    conn = sqlite3.connect('../my_app/data/FinancialDatabase.db')
    df = pd.read_sql_query("SELECT * from {}".format(label), conn)
    df_plot = df[['timestamp', 'open', 'high', 'low', 'close', 'adjusted_close']]
    # Since the database includes more than 10 year of data, I only use the latest 200 days' data
    df_plot = df_plot.head(value)
    df1 = pd.read_sql_query("SELECT * from {}".format(label1), conn)
    df1_plot = df1[['timestamp', 'open', 'high', 'low', 'close', 'adjusted_close']]
    # Since the database includes more than 10 year of data, I only use the latest 200 days' data
    df1_plot = df1_plot.head(value)
    # using candlestick chart with plotly graph object to plot the stock price
    fig = go.Figure(go.Candlestick(x=df_plot['timestamp'], open=df_plot['open'],
                                   high=df_plot['high'], low=df_plot['low'],
                                   close=df_plot['close'], name='{} Stock Price'.format(label)))

    fig.add_trace(go.Scatter(x = df1_plot['timestamp'], y = df1_plot['adjusted_close'], line=dict(color='royalblue')
                             , name = '{} stock price'.format(label1)))
    # set the chart title and axis label to the chart
    fig.update_layout(
        title="Stock Compare",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        legend_title="Company",
        font=dict( size=18, color="Black")
    )
    return fig



if __name__ == '__main__':
    dash_app.run_server(debug=False, port=8050)
