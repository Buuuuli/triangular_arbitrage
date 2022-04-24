
import dash
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
from function import *


default_hostname = '127.0.0.1' # change it if needed
default_port = 7497   # change it if needed
default_client_id = 10645 # change it if needed


currencies = ['USD','EUR','GBP','JPY','AUD']

reqID_serial = 1

app = dash.Dash(__name__)





html.Div([

    html.H4('Acceptable Currency'),
    html.Img(src="asset/currency.jpeg"),
    html.Button('Arbitrage', id='check-button', n_clicks=0),
    html.Div(id="table1"),
    html.Div(
        id='optimal_route'
    )
])


@app.callback(
    # We're going to output the result to trade-output
    [Output(component_id='table1', component_property='children'),
     Output(component_id='my_output', component_property='children')],

    # Only run this callback function when the trade-button is pressed
    Input('check-button', 'n_clicks'),

    prevent_initial_call=True
)

def trade(n_clicks):

    if n_clicks >=1:
        exchange_datadrame = fetch_all(currencies)

        exchange_datadrame = fill_in_nan(exchange_datadrame)

        if not check_all_data(exchange_datadrame):
            print('Exchange Data Unavailable')
            exit(1)




        data = exchange_datadrame.to_dict('rows')
        columns = [{"name": i, "id": i, } for i in (exchange_datadrame.columns)]

        results = dict()

        results = [{'name': i,'id': i} for i in (exchange_datadrame)]

        optimal_route_str = max(results, key=results.get)

        # msg = html.Div(id='optimal route', children= # return of optimal_route_function
        # , style={'margin-bottom': '50px', 'text-align': 'center'}),


        return dash_table.DataTable(data=data, columns=columns), optimal_route_str

    else:
        return "please click the check button"




    #msg = html.Div(id='optimal route', children= # return of optimal_route_function
    #, style={'margin-bottom': '50px', 'text-align': 'center'}),

