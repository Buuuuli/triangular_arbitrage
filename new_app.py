import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from interactive_trader import *
import base64
from function import *
from yahoo import *

reqId_serial = 1

currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD']

image = 'asset/currency.jpeg'
test_base64 = base64.b64encode(open(image, 'rb').read()).decode('ascii')

# ==========================================
exchange_dataframe = fetch_all(ibkr_app, currencies)
exchange_dataframe = fill_in_nan(exchange_dataframe)
if not check_all_data(exchange_dataframe):
    print('Exchange Data Unavailable')
    exit(1)
# exchange_table = check_all_data(exchange_dataframe)
data = exchange_dataframe.to_dict('rows')
columns = [{"name": i, "id": i, } for i in exchange_dataframe.columns]
results = dict()
results = check_all_arbitrage(results, exchange_dataframe, currencies)
optimal_route_str = max(results, key=results.get)
print(results)
print(optimal_route_str)
# ===========================

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
        id='my_output3'),

    # additional variable graph
    html.H3("Section 2: USD Exchange rate Index"),
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
     Output(component_id='my_output2', component_property='children')],

    # Only run this callback function when the trade-button is pressed
    Input('check-button', 'n_clicks'),

    prevent_initial_call=True
)
def arbitrage(n_clicks):
    if n_clicks >= 1:

        exchange_dataframe = fetch_all(currencies)
        print('fetch success')

        exchange_dataframe = fill_in_nan(exchange_dataframe)

        if not check_all_data(exchange_dataframe):
            print('Exchange Data Unavailable')
            exit(1)

        # exchange_table = check_all_data(exchange_dataframe)

        data = exchange_dataframe.to_dict('rows')
        columns = [{"name": i, "id": i, } for i in (exchange_dataframe.columns)]

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
    if n_clicks >= 1:
        return

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


if __name__ == '__main__':
    app.run_server(debug=True)
