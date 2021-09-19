import numpy as np
import yfinance as yf
import pandas as pd

def calc_returns(tickers: list):
    yft = yf.download(tickers=' '.join(tickers), period='1y', auto_adjust=True, group_by='ticker')

    # Calculate returns per quarter: new price / original price
    returns = []
    for ticker in tickers:
        lags = [ticker]

        # If ticker actually has price info, calc lag returns. If not, insert empty row
        # returns calculated in order of current, lag1, lag2, lag3
        for i in range(4, 0, -1):
            try:
                prices = yft[ticker]
            except KeyError:
                returns.append([ticker, -1, -1, -1, -1])
                continue
            lags.append(prices['Close'].iloc[[63*i-1]].iloc[0] / prices['Close'].iloc[[63*(i-1)-1]].iloc[0])

        returns.append(lags)
    return returns


def calc_spy_returns():
    yft = yf.download('spy', period='1y', auto_adjust=True)
    lags = []
    for i in range(4, 0, -1):
        lags.append(yft['Close'].iloc[[63*i-1]].iloc[0] / yft['Close'].iloc[[63*(i-1)-1]].iloc[0])
    return lags


if __name__ == '__main__':
    tickers = pd.read_csv('esg.csv')['Ticker'].tolist()
    tickers.remove('BRK.B')
    tickers.remove('BF.B')

    spy_returns = calc_spy_returns()
    lagged_returns = calc_returns(tickers)

    df = pd.DataFrame(lagged_returns, columns=[
        'ticker',
        'lag0',
        'lag1',
        'lag2',
        'lag3',
    ])

    for i in range(0, 4):
        df[f'beat{i}'] = np.select([df[f'lag{i}'] > spy_returns[i], df[f'lag{i}'] <= spy_returns[i]], [1, 0])

    df.to_csv('returns.csv', index=False)
    