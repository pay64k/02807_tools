import json, os
import re
import helpers
import nltk
import numpy as np
from sklearn import linear_model, datasets
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer

# ------------- read in entries from all files -------------

data_raw = []
data_raw_filtered = []
data_directory = "data"

for file in os.listdir("data"):
    if file.endswith(".json"):
        data = helpers.read_file(data_directory + "/" + file)
        data_raw.append(data)

for bla in data_raw[0:1]:
    for lele in bla:
        print lele

for file in data_raw:
    for entry in file:
        if ("topics" in entry) and ("body" in entry):
            data_raw_filtered.append(entry)

print len(data_raw_filtered)
# print "data_raw_filtered",data_raw_filtered[0]

# ------------------ create bag of words -----------------

data_clean = []

for entry in data_raw_filtered:
    # words_list = re.sub("[^a-zA-Z]", " ", entry['body'])
    words_list = entry["body"]
    # print "words_list",words_list
    data_clean.append([w for w in words_list.lower().split()])

data_clean_train = []

for line in data_clean:
    data_clean_train.append(" ".join(line))  # glue all words together into a list of strings

# print data_clean[0]
# print data_clean_train[0:2]

vectorizer = CountVectorizer(analyzer = "word",
                             tokenizer = None,
                             preprocessor = None,
                             stop_words = None)

train_data_features = vectorizer.fit_transform(data_clean_train)

train_data_features_array = train_data_features.toarray()
print train_data_features_array.shape

# with open('valid_articles3+', 'w') as file_:
#     for line in data_clean:
#         file_.write(str(line))
#         file_.write("\n")