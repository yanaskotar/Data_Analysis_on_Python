#! /usr/bin/env python3

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mpl_finance import candlestick2_ohlc
from tqdm import tqdm, trange
import time

apikey = 'XXXXXXXXXXXXXXX'
symbols = ['SPY', 'INTC', 'AMD', 'AMZN', 'GOOGL', 'FB', 'AAPL']
crypt_symbols = ['BTC', 'ETH', 'LTC', 'BCH', 'XMR', 'ZEC']

def get_alpha_vantage(
        apikey, symbol,
        function='TIME_SERIES_DAILY',
        outputsize='compact',
        datatype='csv',
        **kwargs):

    '''Makes a request with Alpha Vantage API and returns a pandas Dataframe. 

    Usage:
    apple = get_alpha_vantage(apikey, 'AAPL')
    intel = get_alpha_vantage(apikey, 'INTC', outputsize='full')
    bitcoin = get_alpha_vantage(
        apikey, 'BTC', function='DIGITAL_CURRENCY_DAILY',
        outputsize='compact', market='USD')
    
    '''

    base_url = 'https://www.alphavantage.co/query?'
    request_url = base_url + '&'.join\
        (['function=' + function,
          'outputsize=' + outputsize,
          'datatype=' + datatype,
          'symbol=' + symbol,
          'apikey=' + apikey])
    
    for key, val in kwargs.items():
        request_url += '&' + str(key) + '=' + val

    data = pd.read_csv(request_url, index_col='timestamp', parse_dates=True)    
    return data.iloc[::-1]


def bollinger_bands(series, MA=20, k=2):

    '''Takas a pandas timeseries and returns lower_band, sma, upper_band
    as timeseries with the same timestamps.

    Usage:
    lower_band, sma, upper_band = bollinger_bands(intel['close'])
    lower_band, sma, upper_band = bollinger_bands(apple['close'], MA=30, k=3)

    '''

    sma =  series.rolling(window=MA).mean()
    rstd = series.rolling(window=MA).std()
    lower_band = sma - k * rstd
    upper_band = sma + k * rstd
    return lower_band, sma, upper_band


def plot_with_bollinger_bands(series, color='#0066FF', symbol=''):

    lower_band, sma, upper_band = bollinger_bands(series)

    ax = plt.axes()

    ax.set_title('{} Price and Bollinger Bands'.format(symbol))
    ax.set_xlabel('Date')
    ax.set_ylabel('SMA and Bollinger Bands')

    ax.plot(series.index, series, color=color)

    ax.fill_between(
            series.index, lower_band, upper_band,
            color=color, alpha=0.1)
    ax.plot(
            series.index, lower_band, upper_band,
            color=color, linewidth=1, alpha=0.4)
    ax.plot(series.index, sma,
            color=color, linewidth=1, alpha=0.4)
    plt.show()


def plot_candlestick(data):

    '''Takes a Dataframe with required columns 'open', 'close', 'high','low',
    and makes a candlestick plot.

    '''
    
    ax = plt.axes()
    candlestick2_ohlc(
            ax,
            data['open'], data['high'], data['low'], data['close'],
            width=0.5)
    plt.show()

intel = get_alpha_vantage(apikey, 'INTC')

bitcoin = get_alpha_vantage(
    apikey, 'BTC', function='DIGITAL_CURRENCY_DAILY',
    outputsize='compact', market='USD')

bitcoin = bitcoin.drop(columns=['open (USD).1', 'high (USD).1', 'low (USD).1', 'close (USD).1'])
bitcoin = bitcoin.rename(index=str, columns={
        'open (USD)': 'open',
        'high (USD)': 'high',
        'low (USD)': 'low',
        'close (USD)': 'close'})

data_stocks = {}
for symbol in symbols:
    print(symbol)
    time.sleep(15)
    data_stocks[symbol] = get_alpha_vantage(apikey, symbol)


crypto_currencies = {}
for symbol in crypt_symbols:
    print(symbol + ':')
    time.sleep(15)
    crypto_currencies[symbol] = get_alpha_vantage(
            apikey, symbol,
            function='DIGITAL_CURRENCY_DAILY',
            outputsize='compact', market='USD')
    
    crypto_currencies[symbol] = crypto_currencies[symbol].drop(
            columns=[
                'open (USD).1',
                'high (USD).1',
                'low (USD).1',
                'close (USD).1'])

    crypto_currencies[symbol] = crypto_currencies[symbol].rename(
        index=str, columns={
            'open (USD)': 'open',
            'high (USD)': 'high',
            'low (USD)': 'low',
            'close (USD)': 'close'})


# AAPL splits:
# Apple’s stock has split four times since the company went public.
# 2014-06-09 x7
# 2005-02-28 x2
# 2000-06-21 x2
# 1987-06-16 x2

apple = apple.drop(columns=['volume'])
splits = {'2014-06-09': 7, '2005-02-28': 2, '2000-06-21': 2, '1987-06-16': 2}

for date, k in splits.items():
    apple[apple.index < date] /= k

