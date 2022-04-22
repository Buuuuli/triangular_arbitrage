
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



        #return1 = optimal_function1
        #return2 = optimal_function2
        #return3 = optimal_function3


        #contract1 = Contract()
        #contract1.symbol = #optimal_Contract_Symbol1
        #contract1.secType = #SecType
        #contract1.currency = #currency
        #contract1.exchange = #exchange
        #contract1.primaryExchange = #primaryExchange

        #contract2 = Contract()
        #contract2.symbol = #optimal_Contract_Symbol2
        #contract2.secType = #SecType
        #contract2.currency = #currency
        #contract2.exchange = #exchange
        #contract2.primaryExchange = #primaryExchange

        #contract3 = Contract()
        #contract3.symbol = #optimal_Contract_Symbol3
        #contract3.secType = #SecType
        #contract3.currency = #currency
        #contract3.exchange = #exchange
        #contract3.primaryExchange = #primaryExchange


        #order1 = Order()
        #order1.action = #buy_or_sell
        #order1.orderType = #'MKT'
        #order1.totalQuantity = #trade_amt
        #order1.lmtPrice = #mktPrice

        #order2 = Order()
        #order2.action =  # buy_or_sell
        #order2.orderType =  # 'MKT'
        #order2.totalQuantity =  # trade_amt
        #order2.lmtPrice =  # mktPrice

        #order3 = Order()
        #order3.action =  # buy_or_sell
        #order3.orderType =  # 'MKT'
        #order3.totalQuantity =  # trade_amt
        #order3.lmtPrice =  # mktPrice


        #c1 = place_order(contract1, order1)
        #c2 = place_order(contract2, order2)
        #c3 = place_order(contract3, order3)


        # msg = html.Div(id='optimal route', children= # return of optimal_route_function
        # , style={'margin-bottom': '50px', 'text-align': 'center'}),


        return dt.DataTable(data=data, columns=columns), msg

    else:
        return "please click the button"




    #msg = html.Div(id='optimal route', children= # return of optimal_route_function
    #, style={'margin-bottom': '50px', 'text-align': 'center'}),

