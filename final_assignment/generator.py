import csv, helpers

import time

import imdb_parser
import logging
logging.basicConfig(level=logging.ERROR)
movies ={}
movies_amount = 0

rejectes_movies = []

with open("IMDB_files_link/_filtered_data/movies.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\r')
    for line in reader:
        # line variable here is a list of strings, so we join it into one string
        full_line = " ".join(line)
        # partition returns 3-tuple: (part_before_delimiter, delimiter, part_after_delimiter)
        parted = full_line.partition("\t")
        title = parted[0]
        # in the part_after_delimiter we delete all \t characters
        year = parted[2].replace("\t","")
        # check year validity
        if year != "????" and int(year) >= 1986:
            movies[title]={"year": year}
        # else:
        #     rejectes_movies.append([title,"on_year"])
        movies_amount += 1

print movies_amount, "all movies"
print len(movies), "movies amount after year filter"

######################################################
#               language filtering
######################################################

movies_with_languages = {}

with open("IMDB_files_link/_filtered_data/language.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\r')
    for line in reader:
        # line variable here is a list of strings, so we join it into one string
        full_line = " ".join(line)
        # partition returns 3-tuple: (part_before_delimiter, delimiter, part_after_delimiter)
        parted = full_line.partition("\t")
        title = parted[0]
        # in the part_after_delimiter we delete all \t characters
        language = parted[2].replace("\t","")
        # this is because some movies like Avatar (2009) have more than one language
        if title not in movies_with_languages:
            movies_with_languages[title] = [language]
        else:
            movies_with_languages[title].append(language)

for title in movies_with_languages:
    languages = movies_with_languages[title]
    for language in languages:
        # if one of the languages of the movie is not english delete its entry from movies
        # there are different language descriptions in the language.list
        # like for example: English	(English Subtitles), English	(Original Version) etc
        if language == "English" \
                or language == "English	(English Subtitles)" \
                or language == "English(English subtitles)" \
                or language == "English	(Original Version)" \
                or language == "English(Original version)" \
                or language == "English(original version)" \
                or language == "English(US)" \
                or language == "English(United States)" \
                or language == "English(original text)" \
                or language == "English	(English Version)":
            break
        else:
            movies.pop(title, None)
            # rejectes_movies.append([title, "on_lang"])

print len(movies), "movies amount after language filter"

######################################################
#               ratings filtering
######################################################

with open("IMDB_files_link/_filtered_data/ratings.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\r')
    for line in reader:
        # line variable here is a list of strings, so we join it into one string
        full_line = " ".join(line)
        # We split the string back into list but double white space delimiter,
        # since column values have different lenghts.
        # Now we easily know which index element is what
        # This is how each entry will look after split:
        # ['', '2012000000', '72', '3.7', 'Ashbah (2014)']
        # ['', '0..0.12103', '23', '7.7', 'Ashbah Beyrouth (1998)']
        rating_data = full_line.split("  ")
        title = rating_data[4]
        rating = rating_data[3]
        votes = rating_data[2]
        if title not in movies:
            pass
        else:
            movies[title].update({  "votes": votes,
                                    "rating": rating})

for title in movies.keys():
    if "rating" not in movies[title]:
        movies.pop(title, None)
        # rejectes_movies.append([title, "on_rating"])

print len(movies), "amount of movies that have rating"

######################################################
#               director filtering
######################################################

# directors_raw = []
#
# with open("IMDB_files_link/_filtered_data/directors.filtered.new") as data_file:
#     reader = csv.reader(data_file, delimiter='\n')
#     for line in reader:
#         full_line = " ".join(line)
#         directors_raw.append(full_line)
#
# directors_less_raw = []
# temp = []
# for line in directors_raw:
#     # each director is separated by new line character, in our case its an empty list of strings
#     if line != "":
#         temp.append(line)
#     else:
#         directors_less_raw.append(temp)
#         temp = []
#
# movie_and_its_director = {}
#
# for line in directors_less_raw:
#     # first element is always director \t\t movie or director \t movie
#     # if a director has only one movie
#     if len(line) <= 1:
#         # for example: ["'Kid Niagara' Kallet, Harry\tDrug Demon Romance (2012)  (co-director)"]
#         full_line = " ".join(line)
#         parted = full_line.partition("\t")
#         director = parted[0]
#         title = parted[2].replace("\t", "")
#         title_parted = title.partition("  ")[0]
#         movie_and_its_director[title_parted] = {"director": director}
#     else:
#         # for example: ["'t Hooft, Albert\tFallin' Floyd (2013)", '\t\tLittle Quentin (2010)',
#         #  '\t\tTrippel Trappel Dierensinterklaas (2014)']
#         first_line = line[0]
#         parted = first_line.partition("\t")
#         director = parted[0]
#         title_first = parted[2].replace("\t", "")
#         # we want to separate the title from the rest because imdb tends to add
#         # extra info in the parathesis after the actual title
#         # for example: Electric Shades of Grey (2001) (V)  (uncredited)
#         # fortunately its separated by two white spaces after the actual title
#         title_parted = title_first.partition("  ")[0]
#         all_dir_movies = [title_parted]
#         for remaining_title in line[1:len(line)]:
#             remaining_title = remaining_title.replace("\t", "")
#             title_parted = remaining_title.partition("  ")[0]
#             all_dir_movies.append(title_parted)
#         for title in all_dir_movies:
#             movie_and_its_director[title] = {"director": director}

directors_raw = []
with open("IMDB_files_link/_filtered_data/directors.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for line in reader:
        full_line = " ".join(line)
        directors_raw.append(full_line)

directors_less_raw = []

temp = []
for line in directors_raw:
    if line != "":
        temp.append(line)
    else:
        # only add direcotrs that have movies listed
        if len(temp) > 1:
            directors_less_raw.append(temp)
        temp = []

movie_and_its_director = {}

for entry in directors_less_raw:
    director = entry[0]
    if "," in director:
        parted = director.partition(", ")
        # first name then surname
        director = parted[2] + " " + parted[0]
    for film in entry[1:len(entry)]:
        movie_name = film.partition("  ")[0]
        if movie_name not in movie_and_its_director:
            movie_and_its_director[movie_name] = {"director":[director]}
        else:
            movie_and_its_director[movie_name]["director"].append(director)

for title in movie_and_its_director:
    if title in movies:
        movies[title].update({"director": movie_and_its_director[title]["director"][0]})

for title in movies.keys():
    if "director" not in movies[title]:
        movies.pop(title, None)
        rejectes_movies.append([title,"on_dir"])

# print "memory then",helpers.memory()
# free up some memory
del movie_and_its_director, directors_raw, directors_less_raw, temp
# print "memory now",helpers.memory()

print len(movies), "amount of movies that have directors"

######################################################
#               genre filtering
######################################################

with open("IMDB_files_link/_filtered_data/genres.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\r')
    for line in reader:
        # line variable here is a list of strings, so we join it into one string
        full_line = " ".join(line)
        # partition returns 3-tuple: (part_before_delimiter, delimiter, part_after_delimiter)
        parted = full_line.partition("\t")
        title = parted[0]
        # in the part_after_delimiter we delete all \t characters
        genre = parted[2].replace("\t","")
        if title in movies:
            movies[title].update({"genre": genre})

for title in movies.keys():
    if "genre" not in movies[title]:
        movies.pop(title, None)
        rejectes_movies.append([title,"on_genre"])

print len(movies), "amount of movies that have genre"
# try:
#     print movies["Get Him to the Greek (2010)"]
# except:
#     print "HERE_bla2"
# c = 0
# for title in movies:
#     print title, movies[title]
#     c+=1
#     if c >=100: break

######################################################
#                business filtering
######################################################

business_raw = []

with open("IMDB_files_link/_filtered_data/business.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for line in reader:
        full_line = " ".join(line)
        business_raw.append(full_line)

business_less_raw = []
temp = []
for line in business_raw:
    if line != "----":
        temp.append(line)
    else:
        business_less_raw.append(temp)
        temp = []

movies_with_values = []
mandatory_count = 0
gr_count = 0
temp = []
for movie in business_less_raw:
    for entry in movie:
        if "MV" in entry:
            temp.append(entry)
            mandatory_count += 1
        if "BT" in entry:                     #uncomment to have movies with budget only
            temp.append(entry)                #comment to have movies without budget
            mandatory_count += 1              #
        if "GR" in entry:
            temp.append(entry)
            gr_count += 1
        # if "RT" in entry:
        #     temp.append(entry)
        #     mandatory_count += 1
    if mandatory_count >= 1 and gr_count > 0:   # change first condition to 2 if wanna have budget, 1 otherwise
        movies_with_values.append(temp)
    temp = []
    mandatory_count = 0
    gr_count = 0

budget_temp = []
gross_temp = []
title = ""

# print len(movies_with_values), "ALL movies that have stated at least budget and gross values"

for movie in movies_with_values:
    for entry in movie:
        if "MV" in entry:
            title = entry.partition("MV: ")[2]
        elif "BT" in entry:
            bt = entry.partition("BT: ")[2]
            budget_temp.append(bt)
        elif "GR" in entry:
            gr = entry.partition("GR: ")[2]
            gross_temp.append(gr)
    if title != "" and title in movies:
        if len(budget_temp) == 0 and movies[title]["rating"] >= 6:
            movies[title].update({"budget": "no_info", "gross": gross_temp})
        else:
            movies[title].update({"budget": budget_temp, "gross": gross_temp})
    title = ""
    budget_temp = []
    gross_temp = []

# for title in movies.keys():
#     if "budget" not in movies[title]:
#         if movies[title]["rating"] >= 6:
#             movies[title]["budget"] = "no_info"
#         else:
#             movies.pop(title, None)
#             rejectes_movies.append([title, "on_budg"])
#
for title in movies.keys():
    if "gross" not in movies[title]:
        movies.pop(title, None)

# try:
#     print movies["Get Him to the Greek (2010)"]
# except:
#     print "HERE_bla3"

small_wide_temp = []
big_wide_temp = []
usa_temp = []
other_temp = []

for title in movies:
    all_gross = movies[title]["gross"]
    for gross in all_gross:
        try:
            if "(worldwide)" in gross:
                gross_temp = gross.partition(" (worldwide)")[0]
                if "GBP" in gross_temp:
                    gross_temp = gross_temp.partition("GBP ")[2]
                    gross_temp = gross_temp.replace(",", "")
                    small_wide_temp.append(int(round(int(gross_temp)*1.25, 0)))
                elif "USD" in gross_temp:
                    gross_temp = gross_temp.partition("USD ")[2]
                    gross_temp = gross_temp.replace(",","")
                    small_wide_temp.append(int(gross_temp))
                else:
                    gross_temp = gross_temp.partition(" ")[2]
                    gross_temp = gross_temp.replace(",","")
                    small_wide_temp.append(int(gross_temp))
            elif "(Worldwide)" in gross:
                gross_temp = gross.partition(" (Worldwide)")[0]
                if "GBP" in gross_temp:
                    gross_temp = gross_temp.partition("GBP ")[2]
                    gross_temp = gross_temp.replace(",", "")
                    big_wide_temp.append(int(round(int(gross_temp)*1.25, 0)))
                elif "USD" in gross_temp:
                    gross_temp = gross_temp.partition("USD ")[2]
                    gross_temp = gross_temp.replace(",","")
                    big_wide_temp.append(int(gross_temp))
                else:
                    gross_temp = gross_temp.partition(" ")[2]
                    gross_temp = gross_temp.replace(",","")
                    big_wide_temp.append(int(gross_temp))
            elif "(USA)" in gross:
                gross_temp = gross.partition(" (USA)")[0]
                if "GBP" in gross_temp:
                    gross_temp = gross_temp.partition("GBP ")[2]
                    gross_temp = gross_temp.replace(",", "")
                    usa_temp.append(int(round(int(gross_temp)*1.25, 0)))
                elif "USD" in gross_temp:
                    gross_temp = gross_temp.partition("USD ")[2]
                    gross_temp = gross_temp.replace(",","")
                    usa_temp.append(int(gross_temp))
                else:
                    gross_temp = gross_temp.partition(" ")[2]
                    gross_temp = gross_temp.replace(",","")
                    usa_temp.append(int(gross_temp))
            else:
                gross_temp = gross.partition(" ")[2]
                gross_temp = gross_temp.partition(" ")[0]
                gross_temp = gross_temp.replace(",", "")
                other_temp.append(int(gross_temp))
        except:
            # print "ERROR\n", title, "\n", gross
            # logging.exception("logger")
            movies[title]["gross"] = "no_info"

    if len(small_wide_temp) > 0:
        movies[title]["gross"] = max(small_wide_temp)
    elif len(big_wide_temp) > 0:
        movies[title]["gross"] = max(big_wide_temp)
    elif len(usa_temp) > 0:
        movies[title]["gross"] = max(usa_temp)
    elif len(other_temp) > 0:
        movies[title]["gross"] = max(other_temp)
    else:
        movies[title]["gross"] = "no_info"

    small_wide_temp = []
    big_wide_temp = []
    usa_temp = []
    other_temp = []
# try:
#     print movies["Get Him to the Greek (2010)"]
# except:
#     print "HERE_bla"

budget_temp = []
for title in movies:
    budgetes = movies[title]["budget"]
    if budgetes == "no_info":
        rejectes_movies.append([title, "on_budg"])
        pass
    elif len(budgetes) >= 1:
        # print "UNCOORREC", title, budgetes
        for bud in budgetes:
            if bud != "":
                bud_temp = bud.partition(" ")[2]
                bud_temp = bud_temp.partition(" ")[0]
                bud_temp = bud_temp.replace(",","")
                bud_temp = bud_temp.replace(" ","")
                budget_temp.append(int(bud_temp))
        if len(budget_temp) <= 0:
            movies[title]["budget"] = "no_info"
        else:
            movies[title]["budget"] = max(budget_temp)
        # print "COORECTED", title, max(budget_temp)
        budget_temp = []

del business_raw, business_less_raw, movies_with_values, budget_temp, gross_temp, temp

print len(movies), "amount of movies that have stated business values"
######################################################
#                top actors filtering
######################################################

top_actors = {}

with open("IMDB_files_link/_filtered_data/actors.scrapped") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for rank, name in enumerate(reader):
        _name = name[0]
        if _name not in top_actors:
            top_actors[_name] = {"rank": rank + 1}

######################################################
#                actors filtering
######################################################

actors_raw = []
with open("IMDB_files_link/_filtered_data/actors.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for line in reader:
        full_line = " ".join(line)
        actors_raw.append(full_line)

actors_less_raw = []

temp = []
for line in actors_raw:
    if line != "":
        temp.append(line)
    else:
        # only add actors that have roles listed
        if len(temp) > 1:
            actors_less_raw.append(temp)
        temp = []

movie_and_roles = {}

for entry in actors_less_raw:
    actor = entry[0]
    if "," in actor:
        parted = actor.partition(", ")
        # first name then surname
        # if there is (I) or else in name - delete it
        name_with_paranth = parted[2]
        if "(" in name_with_paranth:
            clean_name = name_with_paranth.partition(" (")[0]
            actor = clean_name + " " + parted[0]
        else:
            actor = parted[2] + " " + parted[0]
    for role in entry[1:len(entry)]:
        movie_name = role.partition("  ")[0]
        if movie_name not in movie_and_roles:
            movie_and_roles[movie_name] = {"cast":[{"actor":actor,"sex": "M"}]}
        else:
            movie_and_roles[movie_name]["cast"].append({"actor":actor,"sex": "M"})

actors_raw = []
with open("IMDB_files_link/_filtered_data/actresses.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for line in reader:
        full_line = " ".join(line)
        actors_raw.append(full_line)

actors_less_raw = []

temp = []
for line in actors_raw:
    if line != "":
        temp.append(line)
    else:
        # only add actors that have roles listed
        if len(temp) > 1:
            actors_less_raw.append(temp)
        temp = []

for entry in actors_less_raw:
    actor = entry[0]
    if "," in actor:
        parted = actor.partition(", ")
        # first name then surname
        actor = parted[2] + " " + parted[0]
    for role in entry[1:len(entry)]:
        movie_name = role.partition("  ")[0]
        if movie_name not in movie_and_roles:
            movie_and_roles[movie_name] = {"cast":[{"actor":actor,"sex": "F"}]}
        else:
            movie_and_roles[movie_name]["cast"].append({"actor":actor,"sex": "F"})

del actors_less_raw, actors_raw, temp

######################################################
#            actors ranking and adding
######################################################

for title in movie_and_roles:
    if title in movies:
        movies[title].update({"cast": movie_and_roles[title]["cast"]})

print movies["Six-String Samurai (1998)"]

for title in movies.keys():
    if "cast" not in movies[title]:
        movies.pop(title, None)
        rejectes_movies.append([title,"on_cast_no_cast"])
    else:
        if len(movies[title]["cast"]) < 6:
            movies.pop(title, None)
            rejectes_movies.append([title, "on_cast_<_6"])

print len(movies), "amount of movies that have cast specified and with cast bigger then 6 actors"

top_cast = []

for title in movies:
    cast = movies[title]["cast"]
    if len(cast) >= 6:
        for actor_entry in cast:
            actor = actor_entry["actor"]
            if actor in top_actors:
                rank = top_actors[actor]["rank"]
                top_cast.append({"actor": actor, "rank": rank, "sex": actor_entry["sex"]})
        movies[title]["cast"] = top_cast
        top_cast=[]

for title in movies:
    cast = movies[title]["cast"]
    cast_sorted = sorted(cast, key=lambda k: k['rank'])
    cast_sorted = cast_sorted[:6]
    # if len(cast_sorted) == 0: print title
    # print cast_sorted
    movies[title]["cast"] = cast_sorted

print movies["Six-String Samurai (1998)"]

for title in movies.keys():
    if len(movies[title]["cast"]) < 6:
        movies.pop(title, None)
        rejectes_movies.append([title, "on_cast_<_6_2"])

print len(movies), "amount of movies after adding cast and with 6 actors listed in top list"

del top_cast, top_actors, movie_and_roles
######################################################
#                   plot adding
######################################################

plot_raw = []

with open("IMDB_files_link/_filtered_data/plot.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for line in reader:
        full_line = " ".join(line)
        plot_raw.append(full_line)

plot_less_raw = []
temp = []
for line in plot_raw:
    if line != "----":
        temp.append(line)
    else:
        temp.append("BY")
        plot_less_raw.append(temp)
        temp = []

movie_plots = {}
one_plot = []
for entry in plot_less_raw:
    for line in entry:
        if "MV" in line:
            title = line.partition("MV: ")[2]
        if "PL" in line:
            one_plot.append(line.partition("PL: ")[2])
        if "BY" in line:
            movie_plots[title] = {"plot": " ".join(one_plot)}
            one_plot = []
            break

for title in movies:
    if title in movie_plots:
        movies[title].update({"plot": movie_plots[title]["plot"]})
    else:
        # print "no plot for:", title
        movies[title].update({"plot": "no_info"})
        rejectes_movies.append([title, "on_plot"])

del movie_plots, one_plot, plot_less_raw, plot_raw

######################################################
#                   runtime adding
######################################################

runtimes = {}

with open("IMDB_files_link/_filtered_data/running-times.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\r')
    for line in reader:
        # line variable here is a list of strings, so we join it into one string
        full_line = " ".join(line)
        # partition returns 3-tuple: (part_before_delimiter, delimiter, part_after_delimiter)
        parted = full_line.partition("\t")
        title = parted[0]
        # in the part_after_delimiter we delete all \t characters
        runtime = parted[2].replace("\t","")
        if ":" in runtime:
            runtime = runtime.partition(":")[2]
        if "(" in runtime:
            runtime = runtime.partition("(")[0]
        runtimes[title] = {"runtime": runtime}

for title in movies:
    if title in runtimes:
        movies[title].update({"run-time": runtimes[title]["runtime"]})
    else:
        # print "no runtime for:", title
        movies[title].update({"run-time": "no_info"})

# add video game filtering - only CoD: Modern Warfare 2

for title in movies.keys():
    if "(VG)" in title:
        movies.pop(title, None)

print len(movies), "amount of movies after removing successful video games"

f = open('files/datasetV_' + str(time.strftime("%Y%m%d-%H%M%S")),'w')

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
        "actor4\t" +
        "actor4_rank\t" +
        "actor4_sex\t" +
        "actor5\t" +
        "actor5_rank\t" +
        "actor5_sex\t" +
        "actor6\t" +
        "actor6_rank\t" +
        "actor6_sex\t" +
        "plot" + "\n"
        )
for title in movies:
    entry = movies[title]
    f.write(title +"\t" +
            str(entry["director"])  + "\t" +
            str(entry["rating"])     + "\t" +
            str(entry["votes"])      + "\t" +
            str(entry["year"])       + "\t" +
            str(entry["genre"])      + "\t" +
            str(entry["gross"])      + "\t" +
            str(entry["budget"])     + "\t" +
            str(entry["run-time"])   + "\t" +
            str(entry["cast"][0]["actor"])   + "\t" +
            str(entry["cast"][0]["rank"]) + "\t" +
            str(entry["cast"][0]["sex"]) + "\t" +
            str(entry["cast"][1]["actor"])   + "\t" +
            str(entry["cast"][1]["rank"]) + "\t" +
            str(entry["cast"][1]["sex"]) + "\t" +
            str(entry["cast"][2]["actor"])   + "\t" +
            str(entry["cast"][2]["rank"]) + "\t" +
            str(entry["cast"][2]["sex"]) + "\t" +
            str(entry["cast"][3]["actor"]) + "\t" +
            str(entry["cast"][3]["rank"]) + "\t" +
            str(entry["cast"][3]["sex"]) + "\t" +
            str(entry["cast"][4]["actor"]) + "\t" +
            str(entry["cast"][4]["rank"]) + "\t" +
            str(entry["cast"][4]["sex"]) + "\t" +
            str(entry["cast"][5]["actor"]) + "\t" +
            str(entry["cast"][5]["rank"]) + "\t" +
            str(entry["cast"][5]["sex"]) + "\t" +
            str(entry["plot"]) + "\n")
f.close()
#
# print movies["Get Him to the Greek (2010)"]

f = open('files/_rejected.movies','w')
for entry in rejectes_movies:
    f.write(str(entry)+"\n")
f.close()