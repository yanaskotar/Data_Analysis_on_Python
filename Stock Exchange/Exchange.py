import numpy
import pandas
from pandas import Series, DataFrame
from matplotlib import pyplot
from mpl_finance import candlestick2_ohlc
import time

apikey = 'FQCTAP98UEYW3KFY' # for AlphaVintage
symbols = ['SPY', 'INTC', 'AMD', 'AMZN', 'GOOGL', 'FB', 'AAPL']
#crypt_symbols = ['BTC', 'ETH', 'LTC', 'BCH', 'XMR', 'ZEC']

# apple = get_alpha_vantage(apikey, 'AAPL')
# intel = get_alpha_vantage(apikey, 'INTC', outputsize='full')

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

    data = pandas.read_csv(request_url, index_col='timestamp', parse_dates=True)    
    return data.iloc[::-1]


intel = data = get_alpha_vantage(apikey, 'INTC', outputsize='full')
print(intel)

# intel['close'].plot(title = '{} price'.format('INTC'))


# Basic characteristics
print('----------------------------------------------')
print(intel['close'].describe())


# intel['close']['2018':].plot()
# intel['close'].rolling(window=20).mean()['2018':].plot()

# Technical Analysis and Indicators
# Bollinger bands
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

    ax = pyplot.axes()

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

plot_with_bollinger_bands(intel['close']['2018':], symbol='INTC', color='#0066FF')
pyplot.show()

# CandlStick
def plot_candlestick(data):

    '''Takes a Dataframe with required columns 'open', 'close', 'high', 'low',
    and makes a candlestick plot.

    '''
    
    ax = pyplot.axes()
    candlestick2_ohlc(
            ax,
            data['open'], data['high'], data['low'], data['close'],
            width=0.5)

plot_candlestick(intel['2019':])
pyplot.show()

# Adjusted cost
intel = get_alpha_vantage(apikey, 'INTC', outputsize='full')
intel['close'].plot()

intel = intel.drop(columns=['volume'])
splits = {'2014-06-09': 7, '2005-02-28': 2, '2000-06-21': 2, '1987-06-16': 2}

for date, k in splits.items():
    intel[intel.index < date] /= k

intel['close'].plot()
pyplot.show()

# another method
intel_adj = get_alpha_vantage(apikey, 'INTC', function='TIME_SERIES_DAILY_ADJUSTED', outputsize='full')
print(intel_adj)

intel_adj_nonzero = intel_adj[intel_adj['dividend_amount'] != 0]
print(intel_adj_nonzero)

intel_adj_split = intel_adj[intel_adj['split_coefficient'] != 1]
print(intel_adj_split)

