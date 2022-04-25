from math import isnan

from ibapi.contract import Contract
from dash import dash_table
from pandas import DataFrame

from interactive_trader.ibkr_app import ibkr_app
import threading
import time
from datetime import datetime

# If you want different default values, configure it here.
default_hostname = '127.0.0.1'
default_port = 7497
default_client_id = 10645  # can set and use your Master Client ID
timeout_sec = 5
reqId_serial = 1


def fetch_managed_accounts(hostname=default_hostname, port=default_port,
                           client_id=default_client_id):
    app = ibkr_app()
    app.connect(hostname, int(port), int(client_id))

    start_time = datetime.now()
    while not app.isConnected():
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_managed_accounts",
                "timeout",
                "couldn't connect to IBKR"
            )

    def run_loop():
        app.run()

    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()
    while app.next_valid_id is None:
        time.sleep(0.01)
    app.disconnect()
    return app.managed_accounts


def fetch_current_time(hostname=default_hostname,
                       port=default_port, client_id=default_client_id):
    app = ibkr_app()
    app.connect(hostname, int(port), int(client_id))
    start_time = datetime.now()
    while not app.isConnected():
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_current_time",
                "timeout",
                "couldn't connect to IBKR"
            )

    def run_loop():
        app.run()

    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()
    start_time = datetime.now()
    while app.next_valid_id is None:
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_current_time",
                "timeout",
                "next_valid_id not received"
            )

    app.reqCurrentTime()
    start_time = datetime.now()
    while app.current_time is None:
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_current_time",
                "timeout",
                "current_time not received"
            )
    app.disconnect()
    return app.current_time


def fetch_historical_data(contract, endDateTime='', durationStr='30 D',
                          barSizeSetting='1 hour', whatToShow='MIDPOINT',
                          useRTH=True, hostname=default_hostname,
                          port=default_port, client_id=default_client_id):
    app = ibkr_app()
    app.connect(hostname, int(port), int(client_id))
    start_time = datetime.now()
    while not app.isConnected():
        time.sleep(0.01)
    if (datetime.now() - start_time).seconds > timeout_sec:
        app.disconnect()
        raise Exception(
            "fetch_historical_data",
            "timeout",
            "couldn't connect to IBKR"
        )

    def run_loop():
        app.run()
        print('api_thread ended')

    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()
    start_time = datetime.now()
    while app.next_valid_id is None:
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            print('time out #1')
            raise Exception(
                "fetch_historical_data",
                "timeout",
                "next_valid_id not received"
            )
    tickerId = app.next_valid_id
    print('tickerId = ' + str(tickerId))
    app.reqHistoricalData(
        tickerId, contract, endDateTime, durationStr, barSizeSetting,
        whatToShow, useRTH, formatDate=1, keepUpToDate=False, chartOptions=[])
    start_time = datetime.now()
    while app.historical_data_end != tickerId:
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            print('time out #2')
            raise Exception(
                "fetch_historical_data",
                "timeout",
                "historical_data not received"
            )
    app.disconnect()
    api_thread.join()
    return app.historical_data


def fetch_contract_details(contract, hostname=default_hostname,
                           port=default_port, client_id=default_client_id):
    app = ibkr_app()
    app.connect(hostname, int(port), int(client_id))
    start_time = datetime.now()
    while not app.isConnected():
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_contract_details",
                "timeout",
                "couldn't connect to IBKR"
            )

    def run_loop():
        app.run()

    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()
    start_time = datetime.now()
    while app.next_valid_id is None:
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_contract_details",
                "timeout",
                "next_valid_id not received"
            )

    tickerId = app.next_valid_id
    app.reqContractDetails(tickerId, contract)

    start_time = datetime.now()
    while app.contract_details_end != tickerId:
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_contract_details",
                "timeout",
                "contract_details not received"
            )

    app.disconnect()

    return app.contract_details


def fetch_matching_symbols(pattern, hostname=default_hostname,
                           port=default_port, client_id=default_client_id):
    app = ibkr_app()
    app.connect(hostname, int(port), int(client_id))
    start_time = datetime.now()
    while not app.isConnected():
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_contract_details",
                "timeout",
                "couldn't connect to IBKR"
            )

    def run_loop():
        app.run()

    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()
    start_time = datetime.now()
    while app.next_valid_id is None:
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_contract_details",
                "timeout",
                "next_valid_id not received"
            )

    req_id = app.next_valid_id
    app.reqMatchingSymbols(req_id, pattern)

    start_time = datetime.now()
    while app.matching_symbols is None:
        time.sleep(0.01)
        if (datetime.now() - start_time).seconds > timeout_sec:
            app.disconnect()
            raise Exception(
                "fetch_contract_details",
                "timeout",
                "contract_details not received"
            )

    app.disconnect()

    return app.matching_symbols


def place_order(contract, order, hostname=default_hostname,
                port=default_port, client_id=default_client_id):
    app = ibkr_app()
    app.connect(hostname, port, client_id)
    while not app.isConnected():
        time.sleep(0.01)

    def run_loop():
        app.run()

    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()

    while app.next_valid_id is None:
        time.sleep(0.01)

    app.placeOrder(app.next_valid_id, contract, order)
    while not ('Submitted' in set(app.order_status['status'])):
        time.sleep(0.25)

    app.disconnect()

    return app.order_status


def get_arbitrage(hostname=default_hostname, port=default_port, client_id=default_client_id):

    currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD']
    app = ibkr_app()
    app.connect(hostname, port, client_id)
    time.sleep(0.5)

    def run_loop():
        app.run()

    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()

    time.sleep(0.5)
    reqId_serial = 1

    def create_contract(curr1, curr2):
        # Create contract object
        contract = Contract()
        contract.symbol = curr1
        contract.secType = 'CASH'
        contract.exchange = 'IDEALPRO'
        contract.currency = curr2
        return contract

    def request_data(app, contract):
        global reqId_serial
        reqId_serial += 1
        app.reqHistoricalData(reqId=reqId_serial, contract=contract, endDateTime='', durationStr='1 D',
                              barSizeSetting='1 day',
                              whatToShow='MIDPOINT', useRTH=0, formatDate=1, keepUpToDate=False, chartOptions=[])
        time.sleep(0.5)
        if len(app.data) == 0:
            return float('NaN')
        elif app.data[len(app.data) - 1][0] != reqId_serial:
            return float('NaN')
        else:
            return app.data[len(app.data) - 1][2]

    def fetch_exc_rate(app, base, quote):
        contract = create_contract(base, quote)
        return request_data(app, contract)

    def fetch_all(app, curr_list):
        matrix = DataFrame(columns=curr_list, index=curr_list)
        for i in range(0, len(curr_list)):
            for j in range(0, len(curr_list)):
                if i == j:
                    matrix[curr_list[i]][curr_list[j]] = 1
                else:
                    matrix[curr_list[i]][curr_list[j]] = fetch_exc_rate(app, curr_list[i], curr_list[j])
        return matrix

    def fill_in_nan(matrix):
        for col in matrix.columns:
            for row in matrix.index:
                if isnan(matrix[col][row]) & (not isnan(matrix[row][col])):
                    matrix[col][row] = 1 / matrix[row][col]
        return matrix

    def check_arbitrage(result_dict, matrix, curr1, curr2, curr3):
        arbitrage_amount = matrix[curr1][curr2] * matrix[curr2][curr3] * matrix[curr3][curr1] - 1
        result_dict[curr1 + '.' + curr2 + '.' + curr3] = arbitrage_amount
        arbitrage_amount_rev = matrix[curr1][curr3] * matrix[curr3][curr2] * matrix[curr2][curr1] - 1
        result_dict[curr1 + '.' + curr3 + '.' + curr2] = arbitrage_amount_rev
        print(curr1 + '->' + curr2 + '->' + curr3 + '->' + curr1 + ': ' + "{:.6f}".format(arbitrage_amount))
        print(curr1 + '->' + curr3 + '->' + curr2 + '->' + curr1 + ': ' + "{:.6f}".format(arbitrage_amount_rev))
        return arbitrage_amount

    def check_all_arbitrage(result_dict, matrix, currency_list):
        for i in range(0, len(currency_list)):
            for j in range(i + 1, len(currency_list)):
                for k in range(j + 1, len(currency_list)):
                    check_arbitrage(result_dict, matrix, currency_list[i], currency_list[j], currency_list[k])
        return result_dict

    def check_all_data(matrix):
        return not matrix.isnull().values.any()

    # ============== main =============
    exchange_dataframe = fetch_all(app, currencies)
    print('fetch success')
    exchange_dataframe = fill_in_nan(exchange_dataframe)

    if not check_all_data(exchange_dataframe):
        print('Exchange Data Unavailable')
        exit(1)

    data = exchange_dataframe.to_dict('rows')
    columns = [{"name": i, "id": i, } for i in (exchange_dataframe.columns)]

    results = dict()
    results = check_all_arbitrage(results, exchange_dataframe, currencies)

    optimal_route_str = max(results, key=results.get)

    return dash_table.DataTable(data=data, columns=columns), optimal_route_str