#Luke Williams 18051086
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

#create function that builds the dropdownlist from list of tickers
def dropdownlist():
    list = []
    for ticker in sp500tickers:
        list.append({'label':ticker, 'value':ticker})
    return list

sp500tickers = ['MMM', 'ABT', 'ABBV', 'ABMD', 'ACN', 'ATVI', 'ADBE', 'AMD', 'AAP', 'AES', 'AFL', 'A', 'APD', 'AKAM',
                'ALK', 'ALB', 'ARE', 'ALXN', 'ALGN', 'ALLE', 'LNT', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AMCR', 'AEE',
                'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'ANTM',
                'AON', 'AOS', 'APA', 'AIV', 'AAPL', 'AMAT', 'APTV', 'ADM', 'ANET', 'AJG', 'AIZ', 'T', 'ATO', 'ADSK',
                'ADP', 'AZO', 'AVB', 'AVY', 'BKR', 'BLL', 'BAC', 'BK', 'BAX', 'BDX', 'BBY', 'BIO', 'BIIB',
                'BLK', 'BA', 'BKNG', 'BWA', 'BXP', 'BSX', 'BMY', 'AVGO', 'BR', 'CHRW', 'COG', 'CDNS', 'CPB',
                'COF', 'CAH', 'KMX', 'CCL', 'CARR', 'CTLT', 'CAT', 'CBOE', 'CBRE', 'CDW', 'CE', 'CNC', 'CNP', 'CERN',
                'CF', 'SCHW', 'CHTR', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CTXS',
                'CLX', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CAG', 'CXO', 'COP', 'ED', 'STZ', 'COO',
                'CPRT', 'GLW', 'CTVA', 'COST', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DAL',
                'XRAY', 'DVN', 'DXCM', 'FANG', 'DLR', 'DFS', 'DISCA', 'DISCK', 'DISH', 'DG', 'DLTR', 'D', 'DPZ', 'DOV',
                'DOW', 'DTE', 'DUK', 'DRE', 'DD', 'DXC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMR', 'ETR',
                'EOG', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ETSY', 'EVRG', 'ES', 'RE', 'EXC', 'EXPE', 'EXPD', 'EXR',
                'XOM', 'FFIV', 'FB', 'FAST', 'FRT', 'FDX', 'FIS', 'FITB', 'FE', 'FRC', 'FISV', 'FLT', 'FLIR', 'FLS',
                'FMC', 'F', 'FTNT', 'FTV', 'FBHS', 'FOXA', 'FOX', 'BEN', 'FCX', 'GPS', 'GRMN', 'IT', 'GD', 'GE', 'GIS',
                'GM', 'GPC', 'GILD', 'GL', 'GPN', 'GS', 'GWW', 'HAL', 'HBI', 'HIG', 'HAS', 'HCA', 'PEAK', 'HSIC', 'HSY',
                'HES', 'HPE', 'HLT', 'HFC', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HWM', 'HPQ', 'HUM', 'HBAN', 'HII',
                'IEX', 'IDXX', 'INFO', 'ITW', 'ILMN', 'INCY', 'IR', 'INTC', 'ICE', 'IBM', 'IP', 'IPG', 'IFF', 'INTU',
                'ISRG', 'IVZ', 'IPGP', 'IQV', 'IRM', 'JKHY', 'J', 'JBHT', 'SJM', 'JNJ', 'JCI', 'JPM', 'JNPR', 'KSU',
                'K', 'KEY', 'KEYS', 'KMB', 'KIM', 'KMI', 'KLAC', 'KHC', 'KR', 'LB', 'LHX', 'LH', 'LRCX', 'LW', 'LVS',
                'LEG', 'LDOS', 'LEN', 'LLY', 'LNC', 'LIN', 'LYV', 'LKQ', 'LMT', 'L', 'LOW', 'LUMN', 'LYB', 'MTB', 'MRO',
                'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MKC', 'MXIM', 'MCD', 'MCK', 'MDT', 'MRK', 'MET',
                'MTD', 'MGM', 'MCHP', 'MU', 'MSFT', 'MAA', 'MHK', 'TAP', 'MDLZ', 'MNST', 'MCO', 'MS', 'MOS', 'MSI',
                'MSCI', 'NDAQ', 'NOV', 'NTAP', 'NFLX', 'NWL', 'NEM', 'NWSA', 'NWS', 'NEE', 'NLSN', 'NKE', 'NI', 'NSC',
                'NTRS', 'NOC', 'NLOK', 'NCLH', 'NRG', 'NUE', 'NVDA', 'NVR', 'ORLY', 'OXY', 'ODFL', 'OMC', 'OKE', 'ORCL',
                'OTIS', 'PCAR', 'PKG', 'PH', 'PAYX', 'PAYC', 'PYPL', 'PNR', 'PBCT', 'PEP', 'PKI', 'PRGO', 'PFE', 'PM',
                'PSX', 'PNW', 'PXD', 'PNC', 'POOL', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM',
                'PVH', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RL', 'RJF', 'RTX', 'O', 'REG', 'REGN', 'RF', 'RSG', 'RMD', 'RHI',
                'ROK', 'ROL', 'ROP', 'ROST', 'RCL', 'SPGI', 'CRM', 'SBAC', 'SLB', 'STX', 'SEE', 'SRE', 'NOW', 'SHW',
                'SPG', 'SWKS', 'SLG', 'SNA', 'SO', 'LUV', 'SWK', 'SBUX', 'STT', 'STE', 'SYK', 'SIVB', 'SYF', 'SNPS',
                'SYY', 'TMUS', 'TROW', 'TTWO', 'TPR', 'TGT', 'TEL', 'FTI', 'TDY', 'TFX', 'TER', 'TXN', 'TXT', 'TMO',
                'TIF', 'TJX', 'TSCO', 'TT', 'TDG', 'TRV', 'TFC', 'TWTR', 'TYL', 'TSN', 'UDR', 'ULTA', 'USB', 'UAA',
                'UA', 'UNP', 'UAL', 'UNH', 'UPS', 'URI', 'UHS', 'UNM', 'VLO', 'VAR', 'VTR', 'VRSN', 'VRSK', 'VZ',
                'VRTX', 'VFC', 'VIAC', 'VTRS', 'V', 'VNT', 'VNO', 'VMC', 'WRB', 'WAB', 'WMT', 'WBA', 'DIS', 'WM', 'WAT',
                'WEC', 'WFC', 'WELL', 'WST', 'WDC', 'WU', 'WRK', 'WY', 'WHR', 'WMB', 'WLTW', 'WYNN', 'XEL', 'XRX',
                'XLNX', 'XYL', 'YUM', 'ZBRA', 'ZBH', 'ZION', 'ZTS']


#Initialize dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#Dash app layout consists of a navigation bar and 2 vertical columns in a row
app.layout = dbc.Container(fluid=True, children=[
    dbc.NavbarSimple(
            brand="Exoutia Finance Dash Visualisations",
            brand_href="#",
            color="primary",
            dark=True,
          ),
    html.Br(),
    html.H1('View current company price and % change during selected timeframe', style={'font-weight': 'bold'}),
    dbc.Row([
        dbc.Col(width=3,children=[
            dbc.FormGroup([
                html.H3('Select Company Ticker'),
                dcc.Dropdown(
                    id='tickerdropdown',
                    options=dropdownlist(),
                    value='NFLX')
                ]),
                html.H3('Select timeframe'),
                dcc.RadioItems(
                    id = 'datebox',
                    inputStyle={"margin-left": "20px", "margin-right": "3px"},
                    options=[
                        {'label': '1 Day   ', 'value': 1},
                        {'label': '1 Month   ', 'value': 2},
                        {'label': '6 Months   ', 'value': 3},
                        {'label': '1 Year   ', 'value': 4}
                    ],
                    labelStyle={'display': 'inline'
                                           ''},
                    value=2)
                ]),
        dbc.Col(width=9, children=[
            dcc.Graph(
                id='indicators',
                figure={})
            ]),
        ]),
])
#Dash app inputs & outputs
@app.callback(
    dash.dependencies.Output('indicators', 'figure'),
    dash.dependencies.Input('tickerdropdown', 'value'), dash.dependencies.Input('datebox','value'))

#Create indicator which updates whenever either of the 2 inputs are changed
def update_output(tickerdropdown, datebox):
    #connect to database
    conn = sqlite3.connect('../my_app/data/FinancialDatabase.db')
    #build 2 dataframes, one for historical data and one for fundamental data.
    SQL_Query = pd.read_sql_query("SELECT timestamp, open, high, low, close, adjusted_close FROM {}".format(tickerdropdown), conn)
    SQL_Query2 = pd.read_sql_query("SELECT Symbol, Name, Industry FROM FUNDAMENTALS", conn)

    #extract the fullname and industry from the dataframe using the user selected tickerdropdown
    fullname = SQL_Query2[SQL_Query2['Symbol']==tickerdropdown]['Name'].values[0]
    industry = SQL_Query2[SQL_Query2['Symbol']==tickerdropdown]['Industry'].values[0]

    #extract the historical data at specified intervals
    datapoints = []
    points = [0, 1, 30, 180, 365]
    for i in points:
        datapoints.append(SQL_Query['adjusted_close'].values[i])

    #subtitles based on date selected
    if datebox == 1:
        subtitle = 'Percentage change in 1 day'
    elif datebox == 2:
        subtitle = 'Percentage change in 1 month'
    elif datebox == 3:
        subtitle = 'Percentage change in 6 months'
    elif datebox == 4:
        subtitle = 'Percentage change in 1 year'

    #Initialise indicator figure
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=datapoints[0],
        title={
        "text": "{}<br><span style='font-size:0.8em;color:gray'>Industry: {}</span><br><span style='font-size:0.8em;color:gray'>{}</span>".format(fullname, industry, subtitle)},
        domain={'x': [0, 0.5], 'y': [0, 0.5]},
        delta={'reference': datapoints[datebox], 'relative': True, 'position': "top"}))

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=9010)

dropdownlist()
