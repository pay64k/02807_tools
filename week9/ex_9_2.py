import os, re, helpers, sys
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from datetime import datetime
from sklearn.metrics import jaccard_similarity_score as jac_sim


def min_hash(perm, data, reference_data):
    print "#---------------------------------------#\n" \
          "Staring minHash with", perm, "permutations\n" \
          "#---------------------------------------#"
    original_array = np.transpose(data)

    amount_of_permutations = perm
    hash_functions_array = [[0 for i in range(original_array.shape[1])] for ii in range(amount_of_permutations)]

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
        print "Done with permutation #:", permutation + 1, "/", amount_of_permutations

    # each row corresponds to an article, each row index corresponds to article index in reference_data
    hash_functions_array = np.transpose(hash_functions_array)
    # print hash_functions_array

    print "Calculating..."

    all_similarities = {}
    amount_of_all_articles = len(hash_functions_array)

    # calculate similarities:
    for article_index, article in enumerate(hash_functions_array):
        similarities = {}
        for remaining_article in range(article_index + 1, amount_of_all_articles):
            similarity = jac_sim(hash_functions_array[article_index],
                                 hash_functions_array[remaining_article])
            current_article_id = reference_data[article_index]["id"]
            remaining_article_id = reference_data[remaining_article]["id"]
            if similarity > 0:
                similarities.update({"id": remaining_article_id,
                                     "similarity": similarity})
        if len(similarities) > 0:
            all_similarities[current_article_id] = {"similar_articles": similarities}
        if article_index % 11 == 0:
            sys.stdout.write("\rCompleted:" + str(article_index + 1) + "/" + str(amount_of_all_articles))
            sys.stdout.flush()
    print "\n"
    print "Amount of non-zero similarities:", len(all_similarities)

    for bucket_id in all_similarities:
        similarities_for_one_id = all_similarities[bucket_id]
        for sim in similarities_for_one_id:
            if similarities_for_one_id[sim]["similarity"] >= 0.8:
                print bucket_id, "is similar to:", similarities_for_one_id[sim]["id"]


        # for sim_id, sim in sims["similar_articles"].iteritems():
        #     print sim_id, sim
        #     if sim >= 0.8:
        #         print id, "is similar to:", sim_id
    print "#----------------- Done ----------------#"
    return all_similarities

# ------------- read in entries from all files -------------

if __name__ == '__main__':

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
    for entry in data_raw_filtered[:2000]:
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

    _features_array = _features.toarray()

    print "Got all features...", _features_array.shape

    # print train_data_features_array
    # ----------------------------------------
    # print data_clean
    min_hash(10, _features_array, data_clean)
