import dash
import ibapi.wrapper
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from page_1 import page_1
from order_page import order_page
from error_page import error_page
from navbar import navbar
from sidebar import sidebar, SIDEBAR_HIDDEN, SIDEBAR_STYLE
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from interactive_trader import *
from datetime import datetime
from ibapi.contract import Contract
from ibapi.order import Order
import time
import threading
from dash import dash_table
import base64

from function import *

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from datetime import datetime

import threading
import time
import pandas
from pandas import DataFrame

reqId_serial = 1

currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD']

image = 'asset/currency.jpeg'
test_base64 = base64.b64encode(open(image, 'rb').read()).decode('ascii')

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([

    html.Div([html.H1('Acceptable Currency')], style={'color': 'blue', 'fontSize': 14, 'textAlign': 'center',
                                                      'marginBottom': 50, 'marginTop': 25}),

    html.Div([
        html.Img(src='data:image/png;base64,{}'.format(test_base64))],
        style={'textAlign': 'center', 'height': '10%', 'width': '10%'}),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Button('Arbitrage', id='check-button', n_clicks=0,
                style={
                    'marginRight': '50px',
                    'textAlign': 'center',
                    'position': 'absolute',
                    'left': '50%',
                    'transform': 'translateX(-50%)',
                    'display': 'inline-block',
                    'width': '50%',

                }),
    html.Div(
        id='my_output1'
    ),
    html.Br(),
    html.Br(),
    html.Div(
        id='my_output2'),
    html.Br(),
    html.Br(),
    html.Button('trade', id='trade-button', n_clicks=0,
                style={
                    'marginRight': '50px',
                    'textAlign': 'center',
                    'position': 'absolute',
                    'left': '50%',
                    'transform': 'translateX(-50%)',
                    'display': 'inline-block',
                    'width': '50%',

                }),
    html.Br(),
    html.Br(),
    html.Div(
        id='my_output3')





   ])


@app.callback(
    # We're going to output the result to trade-output
    [Output(component_id='my_output1', component_property='children'),
     Output(component_id='my_output2', component_property='children')],


    # Only run this callback function when the trade-button is pressed
    Input('check-button', 'n_clicks'),

    prevent_initial_call=True
)

def arbitrage(n_clicks):

    if n_clicks >=1:

        class IBapi(EWrapper, EClient):
            def __init__(self):
                EClient.__init__(self, self)
                self.data = []  # Initialize variable to store candle

            def historicalData(self, reqId, bar):
                print(f'reqId: {reqId} Time: {bar.date} Close: {bar.close}')
                self.data.append([reqId, bar.date, bar.close])

        app = IBapi()
        app.connect('127.0.0.1', 7497, 10645)

        def run_loop():
            app.run()

        reqId_serial = 1

        # Start the socket in a thread
        api_thread = threading.Thread(target=run_loop, daemon=True)
        api_thread.start()
        time.sleep(1)  # Sleep interval to allow time for connection to server

        exchange_dataframe = fetch_all(currencies)

        exchange_dataframe = fill_in_nan(exchange_dataframe)

        if not check_all_data(exchange_dataframe):
            print('Exchange Data Unavailable')
            exit(1)

        #exchange_table = check_all_data(exchange_dataframe)

        data = exchange_dataframe.to_dict('rows')
        columns =  [{"name": i, "id": i,} for i in (exchange_dataframe.columns)]

        results = dict()
        results = check_all_arbitrage(results, exchange_dataframe, currencies)

        optimal_route_str = max(results, key=results.get)

        return dash_table.DataTable(data=data, columns=columns), optimal_route_str

    else:
        return "please click the button"

@app.callback(
    # We're going to output the result to trade-output
    Output(component_id='my_output3', component_property='children'),

    # Only run this callback function when the trade-button is pressed
    Input('trade-button', 'n_clicks'),

    prevent_initial_call=True
)

def trade(n_clicks):
    if n_clicks>=1:
        return

    else:
        msg = 'order is not completed'
        return msg


if __name__ == '__main__':
    app.run_server(debug=True)