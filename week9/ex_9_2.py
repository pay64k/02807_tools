import os, re, helpers

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import HashingVectorizer
from datetime import datetime

# ------------- read in entries from all files -------------

data_raw = []
data_raw_filtered = []
data_directory = "data"
data_topics = []

for file in os.listdir(data_directory):
    if file.endswith(".json"):
        data = helpers.read_file(data_directory + "/" + file)
        data_raw.append(data)

for file in data_raw:
    for entry in file:
        if ("topics" in entry) and ("body" in entry):
            data_raw_filtered.append(entry)

print "All articles loaded..."
# print data_raw_filtered[0]
# ------------------ create bag of words -----------------

data_clean = []

# TODO: remove amount restriction
for entry in data_raw_filtered[:5]:
    words_list = re.sub("[^a-zA-Z]", " ", entry['body'])
    data_clean.append({"body": [w for w in words_list.lower().split()],
                       "topics": entry["topics"],
                       "id": entry["id"]})

# print data_clean[0]

data_words_only = []

for article in data_clean:
    data_words_only.append(" ".join(article["body"]))  # glue all words together into a list of strings

vectorizer = CountVectorizer(analyzer="word",
                             tokenizer=None,
                             preprocessor=None,
                             stop_words='english'
                             )

_features = vectorizer.fit_transform(data_words_only)

train_data_features_array = _features.toarray()

print "Got all features...", train_data_features_array.shape

# print train_data_features_array
# ----------------------------------------

original_array = np.transpose(train_data_features_array)

# TODO: remove amount restriction
amount_of_permutations = 3
hash_functions_array = [[0 for i in range(original_array.shape[1])] for ii in range(amount_of_permutations)]

print "Starting minHash for", amount_of_permutations, "permutations..."

for permutation in range(amount_of_permutations):
    permuted_array = np.copy(original_array)
    np.random.shuffle(permuted_array)
    permuted_array = np.transpose(permuted_array)
    row_index = 0
    for row in permuted_array:
        column_index = 0
        for number in row:
            if number > 0:
                hash_functions_array[permutation][row_index] = column_index
                break
            column_index += 1
        row_index += 1
    print "Done with permutation #:", permutation, "/", amount_of_permutations

# each row corresponds to an article
hash_functions_array = np.transpose(hash_functions_array)


def jaccard_dist(set_1,set_2):
    intersection = len(set_1 & set_2)
    union = len(set_1 | set_2)
    return 1 - intersection / float(union)

print "Creating buckets based on Jaccard distance..."

