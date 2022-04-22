from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from datetime import datetime
from math import isnan
import threading
import time
import pandas
from pandas import DataFrame


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


def create_contract(curr1, curr2):
    # Create contract object
    contract = Contract()
    contract.symbol = curr1
    contract.secType = 'CASH'
    contract.exchange = 'IDEALPRO'
    contract.currency = curr2
    return contract

def request_data(contract):
    global reqId_serial
    reqId_serial += 1
    app.reqHistoricalData(reqId=reqId_serial, contract=contract, endDateTime='', durationStr='1 D',
                          barSizeSetting='1 day',
                          whatToShow='MIDPOINT', useRTH=0, formatDate=1, keepUpToDate=False, chartOptions=[])
    time.sleep(0.5)
    if app.data[len(app.data) - 1][0] != reqId_serial:
        return float('NaN')
    else:
        return app.data[len(app.data) - 1][2]

def fetch_exc_rate(base, quote):
    contract = create_contract(base, quote)
    return request_data(contract)


def fetch_all(curr_list):
    matrix = DataFrame(columns=curr_list, index=curr_list)
    for i in range(0, len(curr_list)):
        for j in range(0, len(curr_list)):
            if i == j:
                matrix[curr_list[i]][curr_list[j]] = 1
            else:
                matrix[curr_list[i]][curr_list[j]] = fetch_exc_rate(curr_list[i], curr_list[j])
    return matrix


def fill_in_nan(matrix):
    for col in matrix.columns:
        for row in matrix.index:
            if isnan(matrix[col][row]) & (not isnan(matrix[row][col])):
                matrix[col][row] = 1 / matrix[row][col]
    return matrix



def check_all_data(matrix):
    return not matrix.isnull().values.any()

