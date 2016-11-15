import csv, wikipedia, unicodedata, wptools
import time

movies = {}

with open('files/datasetV_20161115-124715') as csvfile:
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
wiki_no_budget = []
wiki_budget_ok = []
different_budget_keys = set()

for title in movies:
    if movies[title]["budget"] == "no_info":
        full_title = title
        title_no_year = title.partition("(")[0]
        movies_with_no_budget.append([title_no_year,full_title])

counter = 0
# TODO Remove limits
for title in movies_with_no_budget:

    title_no_year = title[0]
    full_title = title[1]
    try:
        search_results = wikipedia.search(title_no_year)
    except:
        print "Error on search_results"
        search_results =[]
        current_query = "no_results"

    search_results = [unicodedata.normalize('NFKD', x).encode('ascii','ignore') for x in search_results]

    # print "search_results for", title_no_year, search_results

    for result in search_results:
        if compute_jaccard_index(title_no_year,result) >= 0.9:
            current_query = result
            break
        if "film" in result:
            current_query = result
            break
        else:
            current_query = "no_results"

    # print "\tcurrent_query:", current_query , "/ for movie: ", full_title

    if current_query != "no_results":
        try:
            movie_page = wptools.page(current_query,silent=True).get_parse()
        except:
            print "error for:", current_query, " query"
            movie_page.infobox = None

        if movie_page.infobox is not None:
            # print "infobox for title:", title_no_year
            # print "\t", movie_page.infobox, "\n"

            if "budget" in movie_page.infobox:

                if movie_page.infobox["budget"] == "":
                    wiki_no_budget.append(["empty_info", full_title])

                else:
                    budget = movie_page.infobox["budget"]
                    wiki_budget_ok.append([budget, full_title])
                    different_budget_keys.add(budget)

            else:
                wiki_no_budget.append(["no_info", full_title])
        else:
            wiki_no_budget.append(["no_info_box", full_title])
        # getting the plot --------
        # try:
        #     movie_page = wikipedia.page(current_query)
        #     go_flag = True
        # except:
        #     print "PLOT------DisambiguationError for:", full_title
        #     go_flag = False
        #
        # if go_flag:
        #     section_results = [unicodedata.normalize('NFKD', x).encode('ascii','ignore') for x in movie_page.sections]
        #     print "sections for", full_title, section_results, "\n"

    else:
        wiki_no_budget.append(["no_info_query", full_title])

    counter += 1
    print "Done with:",counter,"/",len(movies_with_no_budget)

# for line in wiki_budget_ok:
#     print line

print "BUDGET:\tmovies with info:", len(wiki_budget_ok), "\tmovies no info:", len(wiki_no_budget), "\tall movies with no info:", len(movies_with_no_budget)

f = open('files/_additional_budget_from_wiki','w')
f.write(str(time.strftime("%c")) + "\n")
f.write("BUDGET:\tmovies with info:" + str(len(wiki_budget_ok)) + "\tmovies no info:" + str(len(wiki_no_budget)) + "\tall movies with no info:" + str(len(movies_with_no_budget)) + "\n")

for entry in wiki_budget_ok:
    f.write(str(entry)+"\n")

f.close()

# do the same with plots here: