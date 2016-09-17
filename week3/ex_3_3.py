import numpy as np
from numpy.random import randn
import pandas as pd
from pandas import Series, DataFrame, Index, pivot_table
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
print movies_data.shape
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

active_titles = active_titles.merge(movies_data)

# ------- Point 2.1 -------

top3 = active_titles.groupby(['gender','title'],as_index = False)['rating'].mean()
top3_female = top3[top3.gender == 'F'].sort_values(by = 'rating',ascending = False)[:3]
top3_male = top3[top3.gender == 'M'].sort_values(by = 'rating',ascending = False)[:3]

print top3_female
print top3_male

# ------- Point 2.2 -------
# general calculations:
only_females = active_titles[active_titles.gender == 'F']
only_females = only_females.groupby(['title'], as_index = False)['rating'].mean()

only_males = active_titles[active_titles.gender == 'M']
only_males = only_males.groupby(['title'], as_index = False)['rating'].mean()

# top 10 males liked more then females:
diff_df_males = (only_males.rating - only_females.rating).to_frame()
diff_df_males.columns = ['diff']

diff_df_males_sorted = diff_df_males.sort_values(by='diff',ascending = False)

print only_males.ix[diff_df_males_sorted.index[:10]]

# to 10 females liked more then males:
diff_df_females = (only_females.rating - only_males.rating).to_frame()
diff_df_females.columns = ['diff']

diff_df_females_sorted = diff_df_females.sort_values(by='diff',ascending = False)

print only_males.ix[diff_df_females_sorted.index[:10]]

# ------- Point 2.3 -------
active_titles.groupby(by='title',as_index=False).mean()