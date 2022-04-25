import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from interactive_trader import *
import plotly.graph_objects as go
import base64

from interactive_trader.synchronous_functions import get_arbitrage
from yahoo import *
import plotly.graph_objects as go

reqId_serial = 1

currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD']

image = 'asset/currency.jpeg'
test_base64 = base64.b64encode(open(image, 'rb').read()).decode('ascii')

app = dash.Dash(__name__)
server = app.server

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

    html.H2("Section 3: Profits from each path of exchange"),  # store the path of triangular arbitrage
    html.Br(),
    html.Br(),
    html.Div(
        id='output_paths', style={'width': '50%'}),

    # additional variable graph
    html.H2("Section 4: USD Exchange rate Index (Additional Variable)"),
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
        exchange_rate_matrix, optimal_route_str, results = get_arbitrage()
        result_table = dash_table.DataTable(data=results.to_dict('rows'))
        return exchange_rate_matrix, optimal_route_str, result_table

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
