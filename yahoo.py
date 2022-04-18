import yfinance as yf
from pandas import DataFrame

currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD']


def fetch_exc_rate(base, quote):
    tic = base + quote + '=X'
    data = yf.download(tickers=tic, period='1d', interval='1d')
    return data.iloc[0].Close


def fetch_all(curr_list):
    exchange_rate = DataFrame(columns=currencies, index=currencies)
    for i in range(0, len(curr_list)):
        for j in range(0, len(curr_list)):
            if i == j:
                exchange_rate[curr_list[i]][curr_list[j]] = 1
            else:
                exchange_rate[curr_list[i]][curr_list[j]] = fetch_exc_rate(curr_list[i], curr_list[j])
    return exchange_rate


if __name__ == '__main__':
    exchange_rate = fetch_all(currencies)
    print(exchange_rate)
