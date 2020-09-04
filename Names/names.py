import numpy
import pandas
import matplotlib


# names1880 = pandas.read_csv('babynames/data/babynames/yob1880.txt', names = ['name', 'sex', 'births']) # read csv-format file and put it on table with index 
# print(names1880.groupby('sex').births.sum()) #quantity of by gender
# print(names1880.groupby('name').births.sum().nlargest(10)) #quantity of 10 most popular names

years = range(1880, 2018)
pieces = []
for year in years:
	path = 'babynames/data/babynames/yob{}.txt'.format(year)
	frame = pandas.read_csv(path, names = ['name', 'sex', 'births'])
	frame['year'] = year
	pieces.append(frame)

names = pandas.concat(pieces, ignore_index = True)

#print(names)
#%config InlineBackend.figure_format = 'svg'

print(names.pivot_table('births', index = 'year', columns = 'sex', aggfunc = sum)) #number of boys and girls by year

names.pivot_table('births', index = 'year', columns = 'sex', aggfunc = sum).plot(subplots = False, figsize = (8, 4), grid = False, title = 'number of boys and girls by year')
names.pivot_table('births', index = 'year', columns = 'sex', aggfunc = sum).plot(subplots = True, figsize = (8, 4), grid = False, title = 'number of boys and girls by year')
#matplotlib.pyplot.show()

names[names['name'] == 'John'].pivot_table('births', index = 'year', aggfunc = sum).plot(figsize = (8, 4), grid = False, title = 'number of names John by year')
names[names['name'] == 'John'].pivot_table('births', index = 'year', aggfunc = sum).plot(figsize = (8, 4), grid = True, title = 'number of names John by year')

