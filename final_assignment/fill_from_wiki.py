import csv, wikipedia, unicodedata


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

movies_with_no_budget = []

for title in movies:
    if movies[title]["budget"] == "no_info":
        title_no_year = title.partition("(")[0]
        movies_with_no_budget.append(title_no_year)

for title in movies_with_no_budget[:10]:
    search_results = wikipedia.search(title)
    for result in search_results:
        if result == title:
            current_query = result
            break
        if "film" in result:
            current_query = result
            break
        else:
            current_query = "no_results"

    # print line,"found:",wikipedia.search(line)

# first look if there is exact title
#     if yes then look in that article
#     if not look for search that returned 'film' in article name