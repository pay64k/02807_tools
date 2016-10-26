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

for file in data_raw:
    for entry in file:
        if ("topics" in entry) and ("body" in entry):
            data_raw_filtered.append(entry)

print len(data_raw_filtered)
# print "data_raw_filtered",data_raw_filtered[0]

# ------------------ create bag of words -----------------

data_clean = []
data_topics_list = []

for entry in data_raw_filtered:
    words_list = re.sub("[^a-zA-Z]", " ", entry['body'])
    # words_list = entry["body"]
    data_clean.append([w for w in words_list.lower().split()])
    data_topics_list.append(entry["topics"])

data_clean_train = []

for line in data_clean:
    data_clean_train.append(" ".join(line))  # glue all words together into a list of strings

vectorizer = CountVectorizer(analyzer = "word",
                             tokenizer = None,
                             preprocessor = None,
                             stop_words = None
                             )

train_data_features = vectorizer.fit_transform(data_clean_train)

train_data_features_array = train_data_features.toarray()
print train_data_features_array.shape

