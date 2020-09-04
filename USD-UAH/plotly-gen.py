#! /usr/bin/env python3

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline

import numpy as np
import pandas as pd

data_raw = pd.read_excel('data/nbu_usd.xls')

data_raw['Дата-час'] = data_raw['Дата'] + ' ' + data_raw['Час'].map(str)
data_raw['Дата-час'] = pd.to_datetime(data_raw['Дата-час'], format='%d.%m.%Y %H.%M')

data = data_raw[data_raw['Кількість одиниць'] == 100]
data = data.drop(columns=['Дата', 'Час' ,'Назва валюти', 'Час', 'Кількість одиниць'])
data['Офіційний курс'] = data['Офіційний курс']/100

data = data.set_index(['Дата-час'])

data_2015 = data['2015-01-01':'2015-12-31']
data_2016 = data['2016-01-01':'2016-12-31']
data_2017 = data['2017-01-01':'2017-12-31']
data_2018 = data['2018-01-01':'2018-12-31']

graph = [go.Scatter(x=data_2018.index, y=data_2018['Офіційний курс'], name='USD')]
graph.append(go.Scatter(x=data_2018.index, y=data_2018['Офіційний курс'].rolling(20).mean(center=True), name='SMA~20'))
graph.append(go.Scatter(x=data_2018.index, y=data_2018['Офіційний курс'].ewm(com=1).mean(), name='EMA~1'))
graph.append(go.Scatter(x=data_2018.index, y=data_2018['Офіційний курс'].ewm(com=2).mean(), name='EMA~2'))
graph.append(go.Scatter(x=data_2018.index, y=data_2018['Офіційний курс'].ewm(com=10).mean(), name='EMA~10'))

plotly.offline.plot(graph, filename='reports/plotly-time-series.html')
