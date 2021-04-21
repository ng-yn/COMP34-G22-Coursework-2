# Richard Gao 18017045
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from Richard_LineChart import top10_price_movement

# Create the dash app for the top10_price_movement chart
dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create an initial figure
fig = top10_price_movement("Basic Materials")

# Define the layout with 1 row and two columns
dash_app.layout = dbc.Container(fluid=True, children=[
    html.Br(),
    html.H1('Exoutia Finance'),

    dbc.Row([
        # The first column contains a dropdown menu and slider
        dbc.Col(width=3, children=[
            dbc.FormGroup([
                html.H4("Select Sector"),
                # dash-core-components (dcc) provides a dropdown
                dcc.Dropdown(id="sector_select", options=[
                    {'label': 'Basic Materials', 'value': 'Basic Materials'},
                    {'label': 'Communication Services', 'value': 'Communication Services'},
                    {'label': 'Consumer Cyclical', 'value': 'Consumer Cyclical'},
                    {'label': 'Consumer Defensive', 'value': 'Consumer Defensive'},
                    {'label': 'Energy', 'value': 'Energy'},
                    {'label': 'Financial Services', 'value': 'Financial Services'},
                    {'label': 'Healthcare', 'value': 'Healthcare'},
                    {'label': 'Industrials', 'value': 'Industrials'},
                    {'label': 'Real Estate', 'value': 'Real Estate'},
                    {'label': 'Technology', 'value': 'Technology'},
                    {'label': 'Utilities', 'value': 'Utilities'}],
                             placeholder="Select Sector")
            ]),
        ]),
        # The second column contains the chart
        dbc.Col(width=9, children=[
            dcc.Graph(id="graph", figure=fig),
        ]),
    ]),
])


# Setup the callback function with the menu options and slider as input and the chart as output
@dash_app.callback(
    Output(component_id="graph", component_property="figure"),
    [Input(component_id="sector_select", component_property="value")]
)
def update_graph(sector_slctd):
    new_fig = top10_price_movement(sector_slctd)
    return new_fig


if __name__ == '__main__':
    dash_app.run_server(debug=False, port=8050)
