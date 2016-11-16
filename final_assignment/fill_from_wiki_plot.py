import csv, wikipedia, unicodedata, wptools
import time

movies = {}

with open('files/datasetV_20161116-203716') as csvfile:
    reader = csv.DictReader(csvfile, delimiter = "\t")
    for entry in reader:
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
        "actor1_sex":   entry["actor1_sex"],
        "actor2":       entry["actor2"],
        "actor2_rank":  entry["actor2_rank"],
        "actor2_sex":   entry["actor2_sex"],
        "actor3":       entry["actor3"],
        "actor3_rank":  entry["actor3_rank"],
        "actor3_sex":   entry["actor3_sex"],
        "actor4":       entry["actor4"],
        "actor4_rank":  entry["actor4_rank"],
        "actor4_sex":   entry["actor4_sex"],
        "actor5":       entry["actor5"],
        "actor5_rank":  entry["actor5_rank"],
        "actor5_sex":   entry["actor5_sex"],
        "actor6":       entry["actor6"],
        "actor6_rank":  entry["actor6_rank"],
        "actor6_sex":   entry["actor6_sex"],
        "plot":         entry["plot"]
        }
# print movies["Get Him to the Greek (2010)"]


def compute_jaccard_index(list_1, list_2):
    list_1 = list_1.replace("(","").replace(")","")
    list_2 = list_2.replace("(","").replace(")","")
    set_1 = set(list_1.split())
    set_2 = set(list_2.split())
    return len(set_1.intersection(set_2)) / float(len(set_1.union(set_2)))

movies_with_no_plot = []
wiki_no_plot = []
wiki_plot_ok = []

for title in movies:
    if movies[title]["plot"] == "no_info":
        full_title = title
        title_no_year = title.partition("(")[0]
        movies_with_no_plot.append([title_no_year, full_title])
print "movies with no plot:" , len(movies_with_no_plot)
counter = 0
# TODO Remove limits
f = open('files/_additional_plot_from_wiki','a',0)

for title in movies_with_no_plot:

    title_no_year = title[0]
    full_title = title[1]
    title_film = str(title_no_year + "(film)")
    year = title[1].partition("(")[2]
    year = year.replace("(","")
    year = year.replace(")","")
    try:
        search_results = wikipedia.search(title_film)
    except:
        print "Error on search_results"
        search_results =[]
        current_query = "no_results"

    search_results = [unicodedata.normalize('NFKD', x).encode('ascii','ignore') for x in search_results]

    print "search_results for\t", title_film, "\t\t" ,search_results

    for result in search_results:
        if compute_jaccard_index(title_film,result) >= 1:
            # print "\n-----1-----\n"
            current_query = result
            break
        elif compute_jaccard_index(title_no_year,result) >=1:
            # print "\n-----2-----\n"
            current_query = result
            break
        elif compute_jaccard_index(title_no_year,result) >=1:
            # print "\n-----3-----\n"
            current_query = result
            break
        elif compute_jaccard_index(str(title_no_year + " (" + year + " film" + ")"),result) >=1:
            # print "\n-----4-----\n"
            current_query = result
            break
        # elif "film" in result:
        #     current_query = result
        #     break
        else:
            current_query = "no_results"

    print "current_query:\t\t", current_query , "/ for movie: ", full_title

    if current_query != "no_results":
        try:
            movie_page = wikipedia.page(current_query)
            go_flag = True
        except:
            print "PLOT------DisambiguationError for:", full_title
            go_flag = False

        if go_flag:
            section_results = [unicodedata.normalize('NFKD', x).encode('ascii','ignore') for x in movie_page.sections]
            f.write(str(full_title + "\t" + current_query + "\t" + str(search_results) + "\n"))
            print "sections for\t\t", current_query, section_results, "\n"

    else:
        wiki_no_plot.append(["no_info_query", full_title])

    counter += 1
    print "Done with:",counter,"/",len(movies_with_no_plot)

f.close()

#
# print "BUDGET:\tmovies with info:", len(wiki_budget_ok), "\tmovies no info:", len(wiki_no_budget), "\tall movies with no info:", len(movies_with_no_budget)
#
# f = open('files/_additional_budget_from_wiki_corrected','w')
# f.write(str(time.strftime("%c")) + "\n")
# f.write("BUDGET:\tmovies with info:" + str(len(wiki_budget_ok)) + "\tmovies no info:" + str(len(wiki_no_budget)) + "\tall movies with no info:" + str(len(movies_with_no_budget)) + "\n")
#
# for entry in wiki_budget_ok:
#     f.write(str(entry)+"\n")
#
# f.close()

