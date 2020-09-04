import numpy
import pandas
from pandas import Series, DataFrame
from matplotlib import pyplot

Movies = pandas.read_csv('data/ml-latest-small/movies.csv', index_col = 'movieId')
Ratings = pandas.read_csv('data/ml-latest-small/ratings.csv', index_col = 'movieId')
Links = pandas.read_csv('data/ml-latest-small/links.csv', index_col = 'movieId')
Tags = pandas.read_csv('data/ml-latest-small/tags.csv', index_col = 'movieId')

print(Movies)
print(Ratings)
print(Links)
print(Tags)

#Rating of film

Ratings_mean = Ratings.pivot_table(values='rating', index = 'movieId', aggfunc = numpy.mean)
print(Ratings_mean)
Ratings_sum = Ratings.pivot_table(values='rating', index = 'movieId', aggfunc = numpy.sum)
print(Ratings_sum)
Ratings_count = Ratings.pivot_table(values = 'rating', index = 'movieId', aggfunc = numpy.count_nonzero)
print(Ratings_count)

#table merging

Movies_marks = pandas.merge(Movies, Ratings_mean, left_index = True, right_index = True)
Movies_marks = pandas.merge(Movies_marks, Ratings_sum, left_index = True, right_index = True)
Movies_marks = pandas.merge(Movies_marks, Ratings_count, left_index = True, right_index = True)
Movies_marks = Movies_marks.rename(index = str, columns = {'rating_x' : 'rating_mean', 'rating_y' : 'rating_sum', 'rating' : 'rating_count'})
print(Movies_marks)

#stst characters

print(Movies_marks.describe())
# print(Movies_marks.quantile(0.9))
# print(Movies_marks.quantile(0.1))
# print(Movies_marks.quantile(0.5))
#histograms

Movies_marks.hist(column = ['rating_mean', 'rating_sum', 'rating_count'], figsize = (8,6), histtype = 'bar', grid = False, rwidth = 0.8, log = True)
pyplot.show()

# masks, the best films

mask_count = Movies_marks['rating_count'] > Movies_marks['rating_count'].quantile(0.7)
mask_mean = Movies_marks['rating_mean'] > Movies_marks['rating_mean'].quantile(0.9)

print(Movies_marks[mask_count & mask_mean].sort_values('rating_mean').tail(10))
