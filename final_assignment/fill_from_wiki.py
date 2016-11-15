import csv, wikipedia, unicodedata, wptools
from sklearn.metrics import jaccard_similarity_score

movies = {}

with open('imdb_dataset_v6.empty_for_wiki') as csvfile:
    reader = csv.DictReader(csvfile, delimiter = "\t")
    for entry in reader:
        # print(row['first_name'], row['last_name'])
        movies[
            entry["title"]
        ] = {
        "director":     entry["director"],
        "rating":       entry["rating"],
        "votes":        entry["votes"],
        "year":         entry["year"],
        "genre":        entry["genre"],
        "gross":        entry["gross"],
        "budget":       entry["budget"],
        "run-time":     entry["run-time"] ,
        "actor1":       entry["actor1"],
        "actor1_rank":  entry["actor1_rank"],
        "actor2":       entry["actor2"],
        "actor2_rank":  entry["actor2_rank"],
        "actor3":       entry["actor3"],
        "actor3_rank":  entry["actor3_rank"],
        "plot":  entry["plot"]
        }
# print movies["Get Him to the Greek (2010)"]


def compute_jaccard_index(list_1, list_2):
    set_1 = set(list_1)
    set_2 = set(list_2)
    return len(set_1.intersection(set_2)) / float(len(set_1.union(set_2)))

movies_with_no_budget = []

for title in movies:
    if movies[title]["budget"] == "no_info":
        title_no_year = title.partition("(")[0]
        movies_with_no_budget.append(title_no_year)

for title in movies_with_no_budget[11:12]:
    search_results = wikipedia.search(title)

    search_results = [unicodedata.normalize('NFKD', x).encode('ascii','ignore') for x in search_results]

    for result in search_results:
        if compute_jaccard_index(title,result) >= 1.0:
            current_query = result
            break
        if "film" in result:
            current_query = result
            break
        else:
            current_query = "no_results"

    print "----current_query:", current_query , "/ for movie: ", title

    if current_query != "no_results":
        movie_page = wikipedia.page(current_query)
        print movie_page
        print movie_page.sections
    # print line,"found:",wikipedia.search(line)

# first look if there is exact title
#     if yes then look in that article
#     if not look for search that returned 'film' in article name