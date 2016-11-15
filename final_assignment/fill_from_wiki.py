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
    set_1 = set(list_1.split())
    set_2 = set(list_2.split())
    return len(set_1.intersection(set_2)) / float(len(set_1.union(set_2)))

movies_with_no_budget = []
wiki_no_info_movies = []
wiki_ok = []


for title in movies:
    if movies[title]["budget"] == "no_info":
        full_title = title
        title_no_year = title.partition("(")[0]
        movies_with_no_budget.append([title_no_year,full_title])

for title in movies_with_no_budget[:20]:

    title_no_year = title[0]
    full_title = title[1]

    search_results = wikipedia.search(title_no_year)

    search_results = [unicodedata.normalize('NFKD', x).encode('ascii','ignore') for x in search_results]

    print "search_results for", title_no_year, search_results

    for result in search_results:
        if compute_jaccard_index(title_no_year,result) >= 0.9:
            current_query = result
            break
        if "film" in result:
            current_query = result
            break
        else:
            current_query = "no_results"

    print "\tcurrent_query:", current_query , "/ for movie: ", title_no_year, "\n"

    if current_query != "no_results":
        movie_page = wptools.page(current_query,silent=True).get_parse()

        if movie_page.infobox is not None:
            print "infobox for title:", title_no_year
            print "\t", movie_page.infobox, "\n"

            if "budget" in movie_page.infobox:

                if movie_page.infobox["budget"] == "":
                    wiki_no_info_movies.append(["empty_info", full_title])
                else:
                    budget = movie_page.infobox["budget"]
                    wiki_ok.append([budget, full_title])

            else:
                wiki_no_info_movies.append(["no_info", full_title])

        else:
            wiki_no_info_movies.append(["no_info_box", full_title])
    else:
        wiki_no_info_movies.append(["no_info_query", full_title])

for line in wiki_no_info_movies:
    print line