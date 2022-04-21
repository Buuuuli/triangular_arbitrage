from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time
import pandas


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []  # Initialize variable to store candle

    def historicalData(self, reqId, bar):
        print(f'Time: {bar.date} Close: {bar.close}')
        self.data.append([bar.date, bar.close])


def run_loop():
    app.run()


app = IBapi()
app.connect('127.0.0.1', 7497, 10645)

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


EUR_USD_contract = create_contract('EUR', 'USD')


def request_and_append_data(contract):
    app.reqHistoricalData(reqId=1, contract=contract, endDateTime='', durationStr='1 D', barSizeSetting='1 day',
                          whatToShow='MIDPOINT', useRTH=0, formatDate=1, keepUpToDate=False, chartOptions=[])


# Request historical candles


time.sleep(3)  # sleep to allow enough time for data to be returned

df = pandas.DataFrame(app.data, columns=['DateTime', 'Close'])
df['DateTime'] = pandas.to_datetime(df['DateTime'], format='%y%m%d')

print(df)

app.disconnect()
