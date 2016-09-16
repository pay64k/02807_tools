import numpy as np
from numpy.random import randn
import pandas as pd
from pandas import Series, DataFrame, Index
from collections import defaultdict
import operator
import matplotlib.pyplot as plt

# 3083::All About My Mother (Todo Sobre Mi Madre) (1999)::Comedy|Drama line has been removed

movies_table = pd.read_table('ml-1m/movies.dat',
                             engine='python',
                             delimiter="::",
                             names=['movie_id', 'title', 'genre'])

users_table = pd.read_table('ml-1m/users.dat',
                            engine='python',
                            delimiter="::",
                            names=['user_id', 'gender', 'age', 'occupation', 'zip'])

ratings_table = pd.read_table('ml-1m/ratings.dat',
                              engine='python',
                              delimiter="::",
                              names=['user_id', 'movie_id', 'rating', 'timestamp'])

movies_data = pd.merge(movies_table, ratings_table)
movies_data = pd.merge(movies_data, users_table)
# print movies_data.head()

# ------- Point 1 -------
# amount_of_ratings = defaultdict(int)
#
# for entry in movies_data.title:
#     amount_of_ratings[entry] += 1
#
# sorted_amount_of_ratings = sorted(amount_of_ratings.items(), key=operator.itemgetter(1), reverse=True)
#
# for movie in sorted_amount_of_ratings[0:5]:
#     print movie

# faster, better way:
rating_counts = movies_data['title'].value_counts()[:5]
print rating_counts
# ------- Point 2 -------

over250 = movies_data.title.value_counts() >= 250 #this is a Series object

over250_df = pd.DataFrame(over250).reset_index()
over250_df.columns = ['title','is_active']

active_titles = over250_df[over250_df.is_active == True]

print active_titles



