"""Instantiate a Dash app."""
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import sqlite3
from dash.dependencies import Input, Output, State
import pandas as pd

app = dash.Dash(
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            dbc.themes.FLATLY,
        ]
    )

app.layout = html.Div(children=[
  dbc.NavbarSimple(
        brand="Exoutia Finance Dash Visualisations",
        brand_href="#",
        color="primary",
        dark=True,
      ),

html.H3('Basic Candlestick Charts'),
dbc.Row([
    dbc.Col(width=3, children=[
        html.Div(
            children='Select company:\n\n\n',
            style={'fontSize': 12}),
        dcc.Dropdown(
            id='demo-dropdown',
            options=[
                    {'label': 'American Airlines (AAL)', 'value': 'AAL'},
                    {'label': 'Apple (AAPL)', 'value': 'AAPL'},
                    {'label': 'Amazon (AMZN)', 'value': 'AMZN'},
                    {'label': 'Microsoft (MSFT', 'value': 'MSFT'},
                    {'label': 'ETSY (ETSY)', 'value': 'ETSY'},
                    {'label': 'Twitter (TWTR)', 'value': 'TWTR'}],
            value='AAL'),
        html.Br(),
        dcc.Checklist(
                id='toggle-rangeslider',
                options=[{'label': ' Include Rangeslider',
                          'value': 'slider'}],
                value=['slider'],
                style={'fontSize': 12}), ]),
        dbc.Col(width=9, children=[
        html.Br(),
        html.Div(' Select Number of data points to plot -  Min: 10, Max: 400',
                     style={'fontSize': 12}),
        dcc.Slider(
                id='points-slider',
                min=30,
                max=400,
                value=95,
                step=10,
                marks={i: 'Points {}'.format(i) for i in range(0, 400, 40)}),
        html.Br(),

        dcc.Graph(id="graph"),
        html.Div(children='Chart created by: Arinze David Nwanna',
                     style={'fontSize': 12}),
        ]),
    ])])

@app.callback(
    Output("graph", "figure"),
    [Input("toggle-rangeslider", "value"),
    Input('points-slider', "value"),
    Input('demo-dropdown', "value")])
    #define function for creating candlestick chart

def display_candlestick(value, points, ticker):
        #connect database
    con = sqlite3.connect("../my_app/data/FinancialDatabase.db")
    df = pd.read_sql_query(f"SELECT * from {ticker}", con)
    df.set_index('timestamp', inplace=True)
    df2 = df.head(points)
    fig1 = go.Figure(data=[go.Candlestick(x=df2.index,
                                            open=df2['open'],
                                            high=df2['high'],
                                            low=df2['low'],
                                            close=df2['close'])])

    fig1.update_layout(title=f"{ticker} Candlestick Chart",
                        xaxis_title="Date",
                        yaxis_title="Price $",
                        font=dict(
                            family="Times New Roman, Times, serif",
                            size=16,
                            color="Black"),
                        xaxis_rangeslider_visible='slider' in value,
                        xaxis = {'showgrid': True},
                        yaxis = {'showgrid': True},
                            )
    return fig1


if __name__ == '__main__':
    app.run_server(debug=True)
