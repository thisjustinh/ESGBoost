import yfinance as yf
import pandas as pd
import csv
import requests

def outputZipandLongName():
    tickerList = None
    with open('sp500.csv', newline='') as csvfile:
        spReader = csv.reader(csvfile, delimiter=",")
        tickerList = [row[0] for row in spReader]

    zipList = []
    for ticker in tickerList:
        info = yf.Ticker(ticker).info
        if "zip" in info and "longName" in info and info != None:
            tickTuple = (info["zip"], info["longName"])
            zipList.append(tickTuple)

    df = pd.DataFrame(zipList, columns=["Zip", "Long Name"])
    df.to_csv("zip.csv", index=False)

def extractRegistryId():
    zips = []
    names = []
    with open('zip.csv', newline='') as csvfile:
        zipReader = csv.reader(csvfile, delimiter=",")
        data = [(row[0], row[1]) for row in zipReader]
    
    for point in data:
        apiLink = "https://ofmpub.epa.gov/frs_public2/frs_rest_services.get_facilities?facility_name=" + point[1] + "&zip_code=" + point[0] + "&program_output=yes&output=JSON"
        response = requests.get(apiLink)
        print(response.json())


outputZipandLongName()
extractRegistryId()


