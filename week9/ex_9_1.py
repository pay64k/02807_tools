import json, os
import re
import helpers
import nltk
import numpy as np
from sklearn import linear_model, datasets
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime

# ------------- read in entries from all files -------------

data_raw = []
data_raw_filtered = []
data_directory = "data"

for file in os.listdir("data"):
    if file.endswith(".json"):
        data = helpers.read_file(data_directory + "/" + file)
        data_raw.append(data)

for file in data_raw:
    for entry in file:
        if ("topics" in entry) and ("body" in entry):
            data_raw_filtered.append(entry)

# ------------------ create bag of words -----------------

data_clean = []
topics_has_earn_word = []

for entry in data_raw_filtered:
    words_list = re.sub("[^a-zA-Z]", " ", entry['body'])
    # words_list = entry["body"]
    data_clean.append([w for w in words_list.lower().split()])
    if "earn" in entry["topics"]:
        topics_has_earn_word.append(1)
    else:
        topics_has_earn_word.append(0)

# print len(topics_has_earn_word)
# print topics_has_earn_word
data_clean_train = []

for line in data_clean:
    data_clean_train.append(" ".join(line))  # glue all words together into a list of strings

# ------------------ random forest -----------------

vectorizer = CountVectorizer(analyzer = "word",
                             tokenizer = None,
                             preprocessor = None,
                             stop_words = None
                             )
old_time = datetime.now()

train_data_features = vectorizer.fit_transform(data_clean_train)

train_data_features_array = train_data_features.toarray()
print train_data_features_array.shape

clf = RandomForestClassifier(n_estimators=50)
clf = clf.fit(train_data_features[0:8301],topics_has_earn_word[0:8301])
print "Execution time: " , datetime.now() - old_time

score = clf.score(train_data_features[8301:],topics_has_earn_word[8301:])
print "score", score * 100

# ------------------ feature hashing -----------------
