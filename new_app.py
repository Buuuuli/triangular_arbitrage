
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
import dash_table as dt




from function import *


from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from datetime import datetime

import threading
import time
import pandas
from pandas import DataFrame






default_hostname = '127.0.0.1' # change it if needed
default_port = 7497   # change it if needed
default_client_id = 10645 # change it if needed


reqId_serial = 1


currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD']



app = dash.Dash(__name__)





html.Div([

    html.H4('Acceptable Currency'),
    html.Img(src="asset/currency.jpeg"),
    html.Button('Arbitrage', id='check-button', n_clicks=0),
    html.Div(
        id='my_output1'
    ),
    html.Div(
            id='my_output2'
        )

])


@app.callback(
    # We're going to output the result to trade-output
    [Output(component_id='my_output1', component_property='children'),
     Output(component_id='my_output2', component_property='children')],


    # Only run this callback function when the trade-button is pressed
    Input('trade-button', 'n_clicks'),

    prevent_initial_call=True
)

def trade(n_clicks):

    if n_clicks >=1:

        exchange_dataframe = fetch_all(currencies)

        exchange_dataframe = fill_in_nan(exchange_dataframe)

        exchange_table = check_all_data(exchange_dataframe)

        data = exchange_table.to_dict('rows')
        columns =  [{"name": i, "id": i,} for i in (exchange_table.columns)]

        results = dict()
        results = check_all_arbitrage(results, exchange_table, currencies)

        optimal_route_str = max(results, key=results.get)





        currency1 = optimal_route_str.split(',')[0]
        currency2 = optimal_route_str.split(',')[1]
        currency3 = optimal_route_str.split(',')[2]



        contract1 = Contract()
        contract1.symbol = currency1
        contract1.secType = 'CASH'
        contract1.currency = currency2
        contract1.exchange = 'IDEALPRO'

        order1 = Order()
        order1.action = 'BUY'
        order1.orderType = 'MKT'
        order1.totalQuantity =  ibapi.wrapper.EWrapper.updateAccountValue('BuyingPower',currency1,default_client_id)

        c1 = place_order(contract1, order1)


        contract2 = Contract()
        contract2.symbol = currency2
        contract2.secType = 'CASH'
        contract2.currency = currency3
        contract2.exchange = 'IDEALPRO'

        order2 = Order()
        order2.action =  'BUY'
        order2.orderType =  'MKT'
        order2.totalQuantity =  ibapi.wrapper.EWrapper.updateAccountValue('BuyingPower',currency2,default_client_id)


        c2 = place_order(contract2, order2)


        contract3 = Contract()
        contract3.symbol = currency3
        contract3.secType = 'CASH'
        contract3.currency = currency1
        contract3.exchange = 'IDEALPRO'

        order3 = Order()
        order3.action =  'BUY'
        order3.orderType =  'MKT'
        order3.totalQuantity =  ibapi.wrapper.EWrapper.updateAccountValue('BuyingPower',currency3,default_client_id)



        c3 = place_order(contract3, order3)


        msg = html.Div(id='optimal route', children= optimal_route_str,
                       style={'margin-bottom': '50px', 'text-align': 'center'}),


        return dt.DataTable(data=data, columns=columns), msg

    else:
        return "please click the button"




    #msg = html.Div(id='optimal route', children= # return of optimal_route_function
    #, style={'margin-bottom': '50px', 'text-align': 'center'}),

