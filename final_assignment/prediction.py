import file_save_load as fsl
import numpy as np
from sklearn.feature_extraction import DictVectorizer as DV
import pandas as pd
from pandas.tools import plotting

import csv, time, numpy, json
from collections import defaultdict
from itertools import count
from functools import partial
from sklearn import tree

import pandas as pd
import numpy as np

import statsmodels.formula.api as smf

movies = fsl.read_from_file_less('imdb_dataset_v6.0.2_3_actors_complete.tsv', 3)

movies_array = []

for title in movies:
    movies_array.append(movies[title])
# #
# # for entry in movies_array[:10]:
# #     print entry

data_df = pd.DataFrame.from_dict(movies)
data_df = data_df.transpose()

# print data_df.head()

# print data_df.head()

# print type(data_df)
# print "shape after transposing:\n", data_df.shape, "\n"
# # print "columns aft`er transposing:\n", data.columns
#
# print data_df.head()
#
# print data_df.describe()
#
# v = DV()
# X = v.fit_transform(movies_array)

data_df["actor1_ord"] = pd.Categorical(data_df.actor1).codes
data_df["actor2_ord"] = pd.Categorical(data_df.actor2).codes
data_df["actor3_ord"] = pd.Categorical(data_df.actor3).codes
data_df["genre_ord"] = pd.Categorical(data_df.genre).codes
data_df["gross_ord"] = pd.Categorical(data_df.gross).codes
data_df["budget_ord"] = pd.Categorical(data_df.budget).codes

import statsmodels.api as sm
# print data_df.head()
# print data_df.shape

y = data_df["gross_ord"]
X = data_df[["budget_ord","actor1_ord","actor2_ord","actor3_ord","genre_ord"]]

# est = smf.ols(formula="gross ~ budget", data=data_df).fit()

X = sm.add_constant(X)
est = sm.OLS(y.astype(float),X.astype(float)).fit()



print est.summary()

print max(data_df["actor1_ord"])
print max(data_df["actor2_ord"])
print max(data_df["actor3_ord"])
print max(data_df["genre_ord"])
print max(data_df["gross_ord"])
print max(data_df["budget_ord"])

# print v.get_feature_names()

import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import statsmodels.api as sm

# data_budget = []
# data_gross = []
# data_actor_1 = []
#
# for entry in movies:
#     data_gross.append(movies[entry]["gross"])
#     data_budget.append(movies[entry]["budget"])
#     data_actor_1.append(movies[entry]["actor1"])



# plt.scatter(data_budget, data_gross)
# plt.show()
#
# length = len(movies)
#
# trainingLength = int(float(length)/10*9)
#
#
# train_data_gross = data_gross[:trainingLength]
# train_data_budget = data_budget[:trainingLength]
# train_data_actor1 = data_actor_1[:trainingLength]
#
# test_data_gross = data_gross[trainingLength:]
# test_data_budget = data_budget[trainingLength:]
# test_data_actor1 = data_actor_1[trainingLength:]
#
# label_to_number1 = defaultdict(partial(next, count(1)))
# label_to_number2 = defaultdict(partial(next, count(1)))
# label_to_number3 = defaultdict(partial(next, count(1)))
# label_to_number4 = defaultdict(partial(next, count(1)))
# label_to_number5 = defaultdict(partial(next, count(1)))
# label_to_number6 = defaultdict(partial(next, count(1)))
#
# numbers_train_data_gross= [(label_to_number1[label]) for label in train_data_gross]
# numbers_train_data_budget= [(label_to_number2[label]) for label in train_data_budget]
# numbers_train_data_actor1= [(label_to_number3[label]) for label in train_data_actor1]
# numbers_test_data_gross= [(label_to_number4[label]) for label in test_data_gross]
# numbers_test_data_budget= [(label_to_number5[label]) for label in test_data_budget]
# numbers_test_data_actor1= [(label_to_number6[label]) for label in test_data_actor1]
#
# clf = tree.DecisionTreeClassifier()
#
# clf = clf.fit([[i] for i in numbers_train_data_gross],
#               [[i] for i in numbers_train_data_budget] )
#
# result = clf.predict([[i] for i in numbers_test_data_gross])
# print result
# bla = 0
# for i,e in enumerate(numbers_test_data_budget):
# #     print result[i]
#     if e == result[i]:
#         bla += 1
#
# print bla/float(len(result))

