import requests
import pandas as pd
from bs4 import BeautifulSoup

def esg_scrape(ticker):
    # Define scraping parameters
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    url = f"https://finance.yahoo.com/quote/{ticker}/sustainability?p={ticker}"
    soup = BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser')

    total = soup.find('div', {'class': 'Fz(36px) Fw(600) D(ib) Mend(5px)'})
    # Return None if sustainability page doesn't exist for ticker
    if total is None:
        return None

    total = total.text # Total ESG score

    # Get individual E, S, G scores
    individual = []
    scores = soup.find_all('div', {'class': 'D(ib) Fz(23px) smartphone_Fz(22px) Fw(600)'})
    for score in scores:
        individual.append(score.text)

    # Get controversy scores
    controversy = soup.find('div', {'class': 'D(ib) Fz(36px) Fw(500)'})
    controversy = controversy.text

    # Store scraped values into list
    esg = [ticker, total, individual[0], individual[1], individual[2], controversy]
    return esg

if __name__ == '__main__':
    # Get S&P500 tickers to run esg_scrape
    sp500 = pd.read_csv('sp500.csv')
    tickers = sp500['Symbol'].tolist()
    esg = []

    for ticker in tickers:
        data = esg_scrape(ticker)

        if data is None:
            print(f"Skipped {ticker}")
            # add blank entry if ticker doesn't exist
            esg.append([ticker,'','','','',''])
            continue

        esg.append(data)
        print(f"Finished {ticker}")

    # Convert list to DataFrame and export as CSV
    df = pd.DataFrame(esg, columns=['Ticker',
                                    'Total', 
                                    'Environmental', 
                                    'Social', 
                                    'Governance', 
                                    'Controversy'])
    df.to_csv('esg.csv', index=False)
