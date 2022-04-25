import yfinance as yf
from pandas import DataFrame


def fetch_exc_rate(base, quote):
    tic = base + quote + '=X'
    data = yf.download(tickers=tic, period='1d', interval='1d')
    if len(data) == 0:
        return float("nan")
    else:
        return data.iloc[0].Close


def fetch_all(curr_list):
    matrix = DataFrame(columns=curr_list, index=curr_list)
    for i in range(0, len(curr_list)):
        for j in range(0, len(curr_list)):
            if i == j:
                matrix[curr_list[i]][curr_list[j]] = 1
            else:
                matrix[curr_list[i]][curr_list[j]] = fetch_exc_rate(curr_list[i], curr_list[j])
    return matrix


def fetch_index(name):
    data = yf.download(tickers=name, period='60d', interval='1d')
    if len(data) == 0:
        return float("nan")
    else:
        return data


if __name__ == '__main__':
    # currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD']
    # exchange_rate = fetch_all(currencies)
    # print(exchange_rate)
    # fetch_exc_rate('PEN', 'ARS')
    ex_index = fetch_index('DX-Y.NYB')
    print(ex_index)
    # DX-Y.NYB
