import json
import re
import nltk

from nltk.corpus import stopwords

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
    words_list = re.sub("[^a-zA-Z]", " ", line['request_text'].encode('utf-8'))
    data_clean.append([w for w in words_list.lower().split() if not w in stops])
    for word in words_list.split():
        word_dict.add(word.lower())

meaningful_words = [w for w in word_dict if not w in stops]
# print len(meaningful_words)
# print meaningful_words
# print data_clean[0:1]


