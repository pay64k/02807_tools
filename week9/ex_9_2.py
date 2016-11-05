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

print data_raw_filtered[0]
# ------------------ create bag of words -----------------

data_clean = []

# TODO: remove amount restriction
for entry in data_raw_filtered[:3]:
    words_list = re.sub("[^a-zA-Z]", " ", entry['body'])
    data_clean.append({"body": [w for w in words_list.lower().split()],
                               "topics": entry["topics"],
                               "id": entry["id"]})

print data_clean[0]

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
print train_data_features_array.shape

print train_data_features_array
# ----------------------------------------
# ----------------------------------------
# ----------------------------------------

minhashArray = np.transpose(train_data_features_array)
print minhashArray, "\n^ up there is minhashArray"

amount_of_permutations = 3

for hash in range(amount_of_permutations):
    np.take(minhashArray, np.random.permutation(minhashArray.shape[0]), axis=0, out=minhashArray)

# get the row and columns of arrray
r = np.shape(minhashArray)[0]
c = np.shape(minhashArray)[1]
# Result=np.zeros((r,c))

# Creating the phi size for permutation
phiSize = r
permutationArray = np.array(range(phiSize))
np.random.shuffle(permutationArray)

Result = np.zeros((r, c))
# for creat result I iterate trough rows and each time I shuffle permutationArrya and base of the array I create
# a result which obtain base of the first occurance of the 1 I checked with three articles and not changing permutationArray
# and the result was reasonable)
for rMinhash in range(r):
    np.random.shuffle(permutationArray)
    for Col in range(c):
        placeFinder = 0
        for Row in permutationArray:
            placeFinder += 1
            if minhashArray[Row][Col] == 1:
                Result[rMinhash][Col] = int(placeFinder)

# I show the result her to see how the matrix look like after permutation
# print Result

# now I make a bukket list with the similarity in thier columns
bucket = []
bucketList = []
WordColNr1 = -1
listOfTheWords = vectorizer.get_feature_names()
for word in listOfTheWords:
    WordColNr1 += 1
    WordColNr2 = -1
    bucket = []
    for word in listOfTheWords:
        WordColNr2 += 1
        if np.array_equal(Result[:, WordColNr1], Result[:, WordColNr2]):
            bucket.append(word)

    if bucket in bucketList:
        bucketList.remove(bucket)
    bucketList.append(bucket)

# print "\n\nBuckets:\n\n"
# for article in bucketList:
#     print article, "\n\n"
