# Created by Joshua Ng
# This code is for the interactive bar chart (P/E Ratio)

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from Joshua_dash_chart import peratio, pe_mean, pe_median

size = 20 # Amount of companies displayed
fig1 = peratio(0,size,0) # Generating Initial State of the P/E Ratio Graph

# Generating Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container(fluid=True, children=[
    html.Br(),
    html.H1('Dashboard App', style={'font-weight': 'bold'}),
    html.Br(),
    html.H2('P/E Ratio Graphs'),
    # Elements in the First Row
    dbc.Row([
        dbc.Col(width=3, children=[
            # Selector for Sort Order (Ascending / Descending)
            dbc.FormGroup([
                html.H4('Sort Order'),
                dcc.Dropdown(id='sort_select', options=[
                    {'label': 'Ascending', 'value': 1},
                    {'label': 'Descending', 'value': 0}],
                             placeholder='Select Sort Type'
                             )
            ]),
            # Selector for Sector
            dbc.FormGroup([
                html.H4('Sector'),
                dcc.Dropdown(id='sector_select', options=[
                    {'label': 'All', 'value': 0},
                    {'label': 'Basic Materials', 'value': 1},
                    {'label': 'Communication Services', 'value': 2},
                    {'label': 'Consumer Cyclical', 'value': 3},
                    {'label': 'Consumer Defensive', 'value': 4},
                    {'label': 'Energy', 'value': 5},
                    {'label': 'Financial Services', 'value': 6},
                    {'label': 'Healthcare', 'value': 7},
                    {'label': 'Industrials', 'value': 8},
                    {'label': 'Real Estate', 'value': 9},
                    {'label': 'Technology', 'value': 10},
                    {'label': 'Utilities', 'value': 11}],
                             placeholder='Select Sector'
                             )
            ]),
            # Button to update chart
            html.Button(id='update1_button', n_clicks=0, children='Update Chart'),
            # Statistics Panel
            html.Div(id='stat_panel')
        ]),
        # P/E Ratio Bar Chart
        dbc.Col(width=9, children=[
            dcc.Graph(id='graph1',figure=fig1)
        ]),
    ]),
    # Second Row
    dbc.Row([

    ])
])
# Callback function to update the graph
@app.callback(
    Output('graph1','figure'),
    [Input('update1_button','n_clicks')],
    [State('sort_select','value'),
     State('sector_select','value')]
)
def update_graph_sort(n, val_sort, val_sec):
    fig = peratio(val_sort,size,val_sec)
    return fig

# Callback function to update the statistic panel
@app.callback(
    Output('stat_panel','children'),
    [Input('update1_button','n_clicks')],
    [State('sector_select','value')]
)
def update_panel(n, val_sec):
    mean = pe_mean(val_sec)
    median = pe_median(val_sec)
    panel = html.Div([
        html.Br(),
        dbc.Card(body=True, className='bg-dark text-light', children=[
            html.H5('Sector Mean:', className='card-title align-self-center'),
            html.H5('{:.2f}'.format(mean), className='card-text text-light align-self-center'),
            html.Br(),
            html.H5('Sector Median:', className='card-title align-self-center'),
            html.H5('{:.2f}'.format(median), className='card-text text-light align-self-center'),
        ])
    ])
    return panel


if __name__ == '__main__':
    app.run_server(debug=False, port=8050)
