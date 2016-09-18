import json
import re
import nltk
import numpy as np
from sklearn import linear_model, datasets
from sklearn.metrics import accuracy_score

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

# nltk.download() #must do once; download stopwords
# print stopwords.words("english")

stops = set(stopwords.words("english"))

# http://stackoverflow.com/questions/1059559/python-split-strings-with-multiple-delimiters
# https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-1-for-beginners-bag-of-words

with open('pizza-train.json') as data_file:
    data = json.load(data_file)

word_dict = set()
data_clean = []

for line in data:
    # words_list = line['request_text'].encode('utf-8').split()
    # words_list = re.findall(r"[\w']+", line['request_text'].encode('utf-8'))
    # if line['request_text'] != '':
    words_list = re.sub("[^a-zA-Z]", " ", line['request_text'])
    data_clean.append([w for w in words_list.lower().split() if not w in stops])
    for word in words_list.split():
        word_dict.add(word.lower())

meaningful_words = [w for w in word_dict if not w in stops]

vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 200000)
data_clean_train = []

for line in data_clean:
    data_clean_train.append(" ".join(line))
# -------
req_received_pizza = []
for line in data:
    req_received_pizza.append(line['requester_received_pizza'])
# -------
train_data_features = vectorizer.fit_transform(data_clean_train,req_received_pizza)

train_data_features_array = train_data_features.toarray()
print train_data_features_array.shape

# ------- EX 3.4 classification -------

model = linear_model.LogisticRegression()
model = model.fit(
    train_data_features_array[0:3636],
    req_received_pizza[0:3636]
)

print model.score(
    train_data_features_array[3636:],
    req_received_pizza[3636:]
)

# -------
# vocab = vectorizer.get_feature_names()
# print vocab
# -------
# dist = np.sum(train_data_features, axis=0)
#
# for tag, count in zip(vocab, dist):
#     print count, tag
# -------

with open('features', 'w') as file_:
    for line in train_data_features:
        file_.write(str(line))
        file_.write("\n")

