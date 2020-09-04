import numpy
import pandas
from pandas import Series, DataFrame
from matplotlib import pyplot

pyplot.rc('figure', figsize = (10,6))
pandas.set_option('display.max_column', 10)

data_raw = pandas.read_excel('data/nbu_usd.xls')
data_raw['Дата-час'] = data_raw['Дата'] + ' ' + data_raw['Час'].map(str)
data_raw['Дата-час'] = pandas.to_datetime(data_raw['Дата-час'], format = '%d.%m.%Y %H.%M')
data = data_raw[data_raw['Кількість одиниць'] == 100]
data['Офіційний курс'] = data['Офіційний курс']/100
data = data.drop(columns = ['Дата', 'Час', 'Кількість одиниць', 'Назва валюти'])
data = data.rename(columns = {'Офіційний курс':'Official course', 'Дата-час':'Date-time'})
print(data['Date-time'].is_unique)
data = data.set_index(['Date-time'])
print(data)

# visualization

data.plot(title = 'Official course USD to UAH')

# by years

data_2015 = data['2015-01-01':'2015-12-31']
data_2016 = data['2016-01-01':'2016-12-31']
data_2017 = data['2017-01-01':'2017-12-31']
data_2018 = data['2018-01-01':'2018-12-31']

fig, axs = pyplot.subplots(2,2)
fig.suptitle('Official course USD to UAH from 2015 to 2018')

axs[0][0].set_title('2015')
axs[0][0].plot(data_2015)
axs[0][0].axis('off')

axs[0][1].set_title('2016')
axs[0][1].plot(data_2016)
axs[0][1].axis('off')

axs[1][0].set_title('2017')
axs[1][0].plot(data_2017)
axs[1][0].axis('off')

axs[1][1].set_title('2018')
axs[1][1].plot(data_2018)
axs[1][1].axis('off')


# main stat characteristics

print(data_2018.describe())

# 2018 plot
quantile_2018_25 = data_2018['Official course'].quantile(0.25)
quantile_2018_mean = data_2018['Official course'].mean()
quantile_2018_75 = data_2018['Official course'].quantile(0.75)

data_2018.plot(title = '2018 - quantiles')
pyplot.axhline(y=quantile_2018_75, color = 'b', linestyle = ':', linewidth = 1)
pyplot.axhline(y=quantile_2018_mean, color = 'b', linestyle = ':', linewidth = 1)
pyplot.axhline(y=quantile_2018_25, color = 'b', linestyle = ':', linewidth = 1)

# simple moving average

data_2018.plot(title = 'simple moving average')
pyplot.plot(data_2018.rolling(15).mean(center = True), color = 'red', linewidth = 2)

# exponentially weighted moving average

data_2018.plot(title = 'exponentially weighted moving average')
pyplot.plot(data_2018.ewm(com = 2).mean(), color = 'purple', linewidth = 2)
 
pyplot.show()
# 