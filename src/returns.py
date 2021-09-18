import numpy as np
import yfinance as yf
import pandas as pd

tickers = pd.read_csv('esg.csv')['Ticker'].tolist()
tickers.remove('BRK.B')
tickers.remove('BF.B')

yft = yf.download(tickers=' '.join(tickers[0:4]), period='1y', auto_adjust=True, group_by='ticker')

# TODO: Fix missing ticker prices
print(yft['ABMD'])

# Calculate returns per quarter: new price / original price
# returns = []
# for ticker in tickers:
#     lags = [ticker]

#     # If ticker actually has price info. If not, insert empty row
#     for i in range(4, 0, -1):
#         #try:
#             returns.append(yft[ticker]['Close'].iloc[[63*i-1]] / yft[ticker]['Close'].iloc[[63*(i-1)]])
#         #except KeyError:
#          #   lags.append('')

#     returns.append(lags)
#     print(ticker)

# print(returns)
    