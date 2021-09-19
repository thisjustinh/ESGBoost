import yfinance as yf
import pandas as pd
import requests

def outputZipandLongName():
    tickers = pd.read_csv('sp500.csv')['Symbol'].tolist()

    zipList = []
    yf_out = yf.Tickers(' '.join(tickers))
    i = 0

    for ticker in tickers:
        info = yf_out.tickers[ticker].info
        if "zip" in info and "longName" in info and info is not None:
            tickNest = [ticker, info['longName'], info['zip']]
            if 'logo_url' in info:
                tickNest.append(info["logo_url"])
            if 'regularMarketPrice' in info:
                tickNest.append(info['regularMarketPrice'])
            zipList.append(tickNest)
        i += 1
        print(ticker, f'{i}/505')

    df = pd.DataFrame(zipList, columns=["ticker","longName", "zip", "logo_url", "close_price"])
    df.to_csv("zip-copy.csv", index=False)

outputZipandLongName()


