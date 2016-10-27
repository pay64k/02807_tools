import os
import re
import helpers
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import HashingVectorizer
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
    data_clean.append([w for w in words_list.lower().split()])
    if "earn" in entry["topics"]:
        topics_has_earn_word.append(1)
    else:
        topics_has_earn_word.append(0)

data_clean_train = []

for line in data_clean:
    data_clean_train.append(" ".join(line))  # glue all words together into a list of strings

# ------------------  'normal' BoW -----------------

vectorizer = CountVectorizer(analyzer = "word",
                             tokenizer = None,
                             preprocessor = None,
                             stop_words = None
                             )

train_data_features = vectorizer.fit_transform(data_clean_train)

train_data_features_array = train_data_features.toarray()
# print train_data_features_array.shape

old_time = datetime.now()

clf = RandomForestClassifier(n_estimators=50)
clf = clf.fit(train_data_features[0:8301],topics_has_earn_word[0:8301])
print "CountVecorizer BoW encoding \n" \
      "80% train data, 20% test data \n" \
      "Using 50 trees in RandomForestClassifier \n" \
      "Execution time: " , datetime.now() - old_time


score = clf.score(train_data_features[8301:],topics_has_earn_word[8301:])
print "Score:", score * 100, "\n"

# ------------------ BoW using feature hashing -----------------

# from http://scikit-learn.org/stable/auto_examples/text/document_classification_20newsgroups.html#sphx-glr-auto-examples-text-document-classification-20newsgroups-py

vectorizer = HashingVectorizer(stop_words='english', non_negative=True,
                                   n_features=1000)
X_train = vectorizer.transform(data_clean_train)

old_time = datetime.now()

clf = RandomForestClassifier(n_estimators=50)

clf.fit(X_train[0:8301], topics_has_earn_word[0:8301])

score = clf.score(X_train[8301:],topics_has_earn_word[8301:])

print "HashingVecorizer BoW encoding \n" \
      "80% train data, 20% test data \n" \
      "Using 50 trees in RandomForestClassifier \n" \
      "Execution time: " , datetime.now() - old_time, "\n"

print "Score:", score * 100



