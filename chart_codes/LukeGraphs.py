#Luke Williams 18051086
import sqlite3
import pandas as pd
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

#Connect to database and create pandas dataframe sorted by market cap
conn = sqlite3.connect('../my_app/data/FinancialDatabase.db')
SQL_Query = pd.read_sql_query("SELECT Symbol, Name, Sector, FullTimeEmployees, MarketCapitalization, Industry FROM FUNDAMENTALS", conn)
df = pd.DataFrame(SQL_Query, columns = ['Symbol','Name','Sector','FullTimeEmployees','MarketCapitalization', 'Industry'])
df.sort_values(by=['MarketCapitalization'], inplace=True, ascending=False)

#Initialise dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#Dash app layout consists of a navigation bar and 2 vertical columns in a row
app.layout = dbc.Container(fluid=True, children=[
    dbc.NavbarSimple(
        brand="Exoutia Finance Dash Visualisations",
        brand_href="#",
        color="primary",
        dark=True,
    ),

    dbc.Row([
        dbc.Col(width=5,children=[
            dbc.FormGroup([
                html.Br(),
                html.H5(
                    'Use this slider to increase the number of companies shown in the sunburst graph. (Sorted by decreasing market cap)',
                    style={'text-align': 'center'}),
                dcc.Slider(
                    id='numcompanies',
                    min=1,
                    max=501,
                    step=1,
                    value=100,
                    marks={1: '1', 100: '100', 200: '200', 300: '300', 400: '400', 500: '500'})
                ]),
            ]),

        dbc.Col(width=7, children=[
            dcc.Graph(
                id='sunburstgraph',
                figure={})
            ]),
        ])
])
#Dash app inputs & outputs
@app.callback(
    dash.dependencies.Output('sunburstgraph', 'figure'),
    dash.dependencies.Input('numcompanies', 'value'))

#Create a sunburst diagram which updates when input changes
def update_graph(selectednumcompanies):
    fig = px.sunburst(df.head(selectednumcompanies), path=['Sector','Industry','Name'], values='MarketCapitalization')
    fig.update_layout(transition_duration=500)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
