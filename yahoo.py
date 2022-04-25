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

def get_arbitrage():
    currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD']
    exchange_dataframe = fetch_all(currencies)
    results = dict()
    results = check_all_arbitrage(results, exchange_dataframe, currencies)
    optimal_route_str = max(results, key=results.get)
    df_result = DataFrame.from_dict(results, orient='index').reset_index()
    df_result = df_result.rename(columns={'index': 'Paths', df_result.columns[1]: 'Profits'})
    return exchange_dataframe, optimal_route_str, df_result



# if __name__ == '__main__':


