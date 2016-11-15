import csv, wikipedia, unicodedata, wptools
import time
import ast

######################################################
#               adding new budgets
######################################################

movies = {}

with open('files/datasetV_20161115-181058') as csvfile:
    reader = csv.DictReader(csvfile, delimiter="\t")
    for entry in reader:
        movies[
            entry["title"]
        ] = {
            "director": entry["director"],
            "rating": entry["rating"],
            "votes": entry["votes"],
            "year": entry["year"],
            "genre": entry["genre"],
            "gross": entry["gross"],
            "budget": entry["budget"],
            "run-time": entry["run-time"],
            "actor1": entry["actor1"],
            "actor1_rank": entry["actor1_rank"],
            "actor1_sex": entry["actor1_sex"],
            "actor2": entry["actor2"],
            "actor2_rank": entry["actor2_rank"],
            "actor2_sex": entry["actor2_sex"],
            "actor3": entry["actor3"],
            "actor3_rank": entry["actor3_rank"],
            "actor3_sex": entry["actor3_sex"],
            "plot": entry["plot"]
        }

new_budgets = {}

with open('files/_additional_budget_from_wiki_corrected') as file:
    # reader = csv.DictReader(csvfile, delimiter = "\n")
    for entry in file:
        temp = ast.literal_eval(entry)
        title = temp[1]
        budget = temp[0]
        no_dollar = budget.partition("$")[2]
        no_comma = no_dollar.replace(",", "")
        no_space = no_comma.replace(" ", "")
        if "million" in no_comma:
            only_number = no_space.partition("million")[0]
            budget = int(round(float(only_number) * 1000000, 0))
        else:
            budget = no_space
        new_budgets[title] = budget
# 294 new budgets found
# for bla in new_budgets:
#     print new_budgets[bla], bla
c = 0
for title in movies:
    if title in new_budgets:
        movies[title]["budget"] = new_budgets[title]
        c += 1
print c

for title in movies.keys():
    if movies[title]["budget"] == "no_info":
        movies.pop(title, None)

print len(movies)

f = open('files/datasetV_' + str(time.strftime("%Y%m%d-%H%M%S")), 'w')

f.write("title\t" +
        "director\t" +
        "rating\t" +
        "votes\t" +
        "year\t" +
        "genre\t" +
        "gross\t" +
        "budget\t" +
        "run-time\t" +
        "actor1\t" +
        "actor1_rank\t"
        "actor1_sex\t"
        "actor2\t" +
        "actor2_rank\t" +
        "actor2_sex\t" +
        "actor3\t" +
        "actor3_rank\t" +
        "actor3_sex\t" +
        "plot" + "\n"
        )
for title in movies:
    entry = movies[title]
    f.write(title + "\t" +
            str(entry["director"]) + "\t" +
            str(entry["rating"]) + "\t" +
            str(entry["votes"]) + "\t" +
            str(entry["year"]) + "\t" +
            str(entry["genre"]) + "\t" +
            str(entry["gross"]) + "\t" +
            str(entry["budget"]) + "\t" +
            str(entry["run-time"]) + "\t" +
            str(entry["actor1"]) + "\t" +
            str(entry["actor1_rank"]) + "\t" +
            str(entry["actor1_sex"]) + "\t" +
            str(entry["actor2"]) + "\t" +
            str(entry["actor2_rank"]) + "\t" +
            str(entry["actor2_sex"]) + "\t" +
            str(entry["actor3"]) + "\t" +
            str(entry["actor3_rank"]) + "\t" +
            str(entry["actor2_sex"]) + "\t" +
            str(entry["plot"]) + "\n")
f.close()
