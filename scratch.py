from interactive_trader import *
from ibapi.order import Order

from function import *


# class IBapi(EWrapper, EClient):
#     def __init__(self):
#         EClient.__init__(self, self)
#         self.data = []  # Initialize variable to store candle
#
#     def historicalData(self, reqId, bar):
#         print(f'reqId: {reqId} Time: {bar.date} Close: {bar.close}')
#         self.data.append([reqId, bar.date, bar.close])


# app = IBapi()
# app.connect('127.0.0.1', 7497, 10645)
#
#
# def run_loop():
#     app.run()


# reqId_serial = 1
#
# api_thread = threading.Thread(target=run_loop, daemon=True)
# api_thread.start()
# time.sleep(1)

currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD']

exchange_dataframe = fetch_all(ibkr_app, currencies)

exchange_dataframe = fill_in_nan(exchange_dataframe)
if not check_all_data(exchange_dataframe):
    print('Exchange Data Unavailable')
    exit(1)

# data = exchange_dataframe.to_dict('rows')
# columns = [{"name": i, "id": i, } for i in (exchange_dataframe.columns)]

results = dict()
results = check_all_arbitrage(results, exchange_dataframe, currencies)

optimal_route_str = max(results, key=results.get)
print(optimal_route_str)
#
# currency1 = optimal_route_str.split('.')[0]
# currency2 = optimal_route_str.split('.')[1]
# currency3 = optimal_route_str.split('.')[2]
#
# contract1 = Contract()
# contract1.symbol = currency1
# contract1.secType = 'CASH'
# contract1.currency = currency2
# contract1.exchange = 'IDEALPRO'
#
# order1 = Order()
# order1.action = 'BUY'
# order1.orderType = 'MKT'
# order1.totalQuantity = 100000
#
# # c1 = place_order(contract1, order1)
#
# contract2 = Contract()
# contract2.symbol = currency2
# contract2.secType = 'CASH'
# contract2.currency = currency3
# contract2.exchange = 'IDEALPRO'
#
# order2 = Order()
# order2.action = 'BUY'
# order2.orderType = 'MKT'
# order2.totalQuantity = exchange_dataframe[currency1].loc[[currency2]].value[0] * 100000 * (1 - 0.00002)
# # c2 = place_order(contract2, order2)
#
# contract3 = Contract()
# contract3.symbol = currency3
# contract3.secType = 'CASH'
# contract3.currency = currency1
# contract3.exchange = 'IDEALPRO'
#
# order3 = Order()
# order3.action = 'BUY'
# order3.orderType = 'MKT'
# order3.totalQuantity = exchange_dataframe[currency2].loc[[currency3]].value[0] * \
#                        exchange_dataframe[currency1].loc[[currency2]].value[0] * 100000 * (1 - 0.00002) * (1 - 0.00002)

# c3 = place_order(contract3, order3)