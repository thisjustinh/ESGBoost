import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

def preprocess(df):
    returns = df[['beat0', 'beat1', 'beat2', 'beat3']].copy()
    tickers = df[['ticker']].copy()
    df = df.drop(columns=['ticker', "longName", "logo_url", "close_price", 'beat0', 'beat1', 'beat2', 'beat3'])

    # standardize to mean 0, sd 1
    std = (df-df.mean()) / df.std()
    df = pd.concat([tickers, std, returns], axis=1)
    df = df.dropna()
    return df


def supervised_split(df, ratio):
    train = df.sample(frac=ratio)
    test = df.drop(train.index)
    train.to_csv('data/train.csv')
    test.to_csv('data/test.csv')
    return train, test
    

if __name__ == '__main__':
    master = pd.read_csv('data/master.csv')
    preprocessed = preprocess(master)
    tickers = preprocessed['ticker'].copy()
    preprocessed = preprocessed.drop(columns={'ticker'})

    # to be used with Tangram!
    train, test = supervised_split(preprocessed, 0.7)

    kmeans = KMeans(n_clusters=10).fit(preprocessed)
    clusters = pd.DataFrame({'cluster': kmeans.labels_})
    pd.concat([tickers, clusters], axis=1).to_csv('data/clusters.csv', index=False)
