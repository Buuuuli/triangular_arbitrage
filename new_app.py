import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import base64
from interactive_trader.synchronous_functions import get_accoutsummary
from yahoo import *
import plotly.graph_objects as go

reqId_serial = 1

currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD']

image = 'asset/currency.jpeg'
test_base64 = base64.b64encode(open(image, 'rb').read()).decode('ascii')

app = dash.Dash(__name__)
server = app.server

global_balance = 1000000
global_currency = 'USD'
global_exchange_rate = None
global_optimal_path = None

app.layout = html.Div([
    html.Div([
        html.H1('Triangular Arbitrage')], style={'color': '#3258a8', 'fontSize': 14, 'textAlign': 'center',
                                                 'marginBottom': 50, 'marginTop': 25}),

    html.H2("Section 1: Asset Pool"),
    html.Div([
        html.Img(src='data:image/png;base64,{}'.format(test_base64))],
        style={'textAlign': 'center', 'height': '10%', 'width': '8%'}),
    html.Br(),
    html.Br(),
    html.Br(),

    html.H2("Section 2: Current Exchange Rate Matrix"),  # Store the current currency data table

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
    html.Br(),
    html.Div([
        html.H4("Please wait around 20 seconds to process the currency data")],
        style={'color': 'black', 'fontSize': 14, 'textAlign': 'center',
               'marginBottom': 50, 'marginTop': 25}),

    html.Div(
        id='my_output1',
        style={'width': '50%', 'align': 'center'}
    ),
    # TODO: 把UI改好看点
    html.Br(),
    html.Br(),
    html.Div(
        id='my_output2'),
    html.Br(),
    html.Br(),


    html.H2("Section 3: Profits from each path of exchange"),  # store the path of triangular arbitrage
    html.Br(),
    html.Br(),
    html.Div(
        id='output_paths', style={'width': '50%'}),
    html.Br(),
    html.Br(),
    html.H2('Section 4: Trades and profit'),
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
    html.H3(id='div_profit'),
    html.Br(),
    html.Br(),

    html.H2("Section 5: Account Balance"),
    html.Br(),
    html.Button(
        id='button_acc',
        children='Get Account Balance',
        n_clicks=0
    ),
    html.Div(
        id='account_summary'
    ),

    # additional variable graph
    html.H2("Section 6: USD Exchange rate Index (Additional Variable)"),
    html.Br(),

    html.Button(
        id='button',
        children='update graph',
        n_clicks=0
    ),
    dcc.Graph(id='candlestick-graph'),

    html.Br(),

])


@app.callback(
    # We're going to output the result to trade-output
    [Output(component_id='my_output1', component_property='children'),
     Output(component_id='my_output2', component_property='children'),
     Output(component_id='output_paths', component_property='children')],

    # Only run this callback function when the trade-button is pressed
    Input('check-button', 'n_clicks'),

    prevent_initial_call=True
)
def arbitrage(n_clicks):
    if n_clicks >= 1:
        exchange_dataframe, optimal_route_str, results = get_arbitrage()
        global global_exchange_rate
        global global_optimal_path
        global_exchange_rate = exchange_dataframe
        global_optimal_path = optimal_route_str
        exchange_dataframe = exchange_dataframe.reset_index()
        data = exchange_dataframe.to_dict('rows')
        columns = [{"name": i, "id": i, } for i in (exchange_dataframe.columns)]
        exchange_rate_matrix = dash_table.DataTable(data=data, columns=columns)
        result_table = dash_table.DataTable(data=results.to_dict('rows'))
        return exchange_rate_matrix, optimal_route_str, result_table

    else:
        return "please click the button"


@app.callback(
    Output(component_id='account_summary', component_property='children'),
    Input(component_id='button_acc', component_property='n_clicks'))
def clickaccount(n_clicks):
    if n_clicks >= 1:
        return f'Remaining Balance is {global_balance}'
    else:
        return "please click the button"


@app.callback(
    # We're going to output the result to trade-output
    Output(component_id='div_profit', component_property='children'),

    # Only run this callback function when the trade-button is pressed
    Input('trade-button', 'n_clicks'),

    prevent_initial_call=True
)
def trade(n_clicks):
    if n_clicks >= 1:
        if global_exchange_rate is None or global_optimal_path is None:
            return 'Exchange data unavailable, please click on arbitrage button first'
        else:
            global global_balance
            print(global_exchange_rate)
            print(global_optimal_path)
            profit, output_str = get_profit(global_balance,
                                                    global_currency,
                                                    global_exchange_rate,
                                                    global_optimal_path)
            global_balance += profit
            out_list = list()
            for line in output_str.split('\n'):
                out_list.append(line)
                out_list.append(html.Br())
            return out_list

    else:
        msg = 'order is not completed'
        return msg


# additional variable
@app.callback(
    Output(component_id='candlestick-graph', component_property='figure'),
    Input(component_id='button', component_property='n_clicks'))
def display_candlestick(n_clicks):
    df = fetch_index('DX-Y.NYB')
    df = df.reset_index()
    fig = go.Figure(
        data=[go.Candlestick(
            x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close']
        )
        ]
    )

    fig.update_layout(title='USD Exchange Rate Index')
    return fig


def get_profit(balance, currency, matrix, path):
    print(matrix)
    output = f'Start with {balance} {currency}\n'
    [curr1, curr2, curr3] = path.split('.')
    curr1_amt = balance
    rate_usd = 1
    if curr1 != 'USD':
        curr1_amt = balance * matrix['USD'][curr1]
        rate_usd = matrix['USD'][curr1]
        output += f'exchange for {curr1_amt}{curr1} at the rate of {rate_usd} {curr1}/USD\n'
    curr2_amt = curr1_amt * matrix[curr1][curr2]
    output += f'exchange for {curr2_amt}{curr2} at the rate of {matrix[curr1][curr2]} {curr2}/{curr1}\n'
    curr3_amt = curr2_amt * matrix[curr2][curr3]
    output += f'exchange for {curr3_amt}{curr3} at the rate of {matrix[curr2][curr3]} {curr3}/{curr2}\n'
    curr1_amt_new = curr3_amt * matrix[curr3][curr1]
    output += f'exchange for {curr1_amt_new}{curr1} at the rate of {matrix[curr3][curr1]} {curr1}/{curr3}\n'
    usd_amt = curr1_amt_new
    if curr1 != 'USD':
        usd_amt = curr1_amt_new * matrix[curr1]['USD']
        output += f'exchange for {usd_amt} USD at the rate of {1 / rate_usd} USD/{curr1}\n'
    profit = usd_amt - balance
    output += f'after the triangular trade, you earned ${profit}'
    print(output)
    return profit, output


if __name__ == '__main__':
    app.run_server(debug=True)
