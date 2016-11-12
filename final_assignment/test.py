import csv, helpers
import imdb_parser

movies ={}
movies_amount = 0

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

print len(movies), "amount of movies that have rating"

######################################################
#               director filtering
######################################################

directors_raw = []

with open("IMDB_files_link/_filtered_data/directors.filtered.new") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for line in reader:
        full_line = " ".join(line)
        directors_raw.append(full_line)

directors_less_raw = []
temp = []
for line in directors_raw:
    # each director is separated by new line character, in our case its an empty list of strings
    if line != "":
        temp.append(line)
    else:
        directors_less_raw.append(temp)
        temp = []

movie_and_its_director = {}

for line in directors_less_raw:
    # first element is always director \t\t movie or director \t movie
    # if a director has only one movie
    if len(line) <= 1:
        # for example: ["'Kid Niagara' Kallet, Harry\tDrug Demon Romance (2012)  (co-director)"]
        full_line = " ".join(line)
        parted = full_line.partition("\t")
        director = parted[0]
        title = parted[2].replace("\t", "")
        title_parted = title.partition("  ")[0]
        movie_and_its_director[title_parted] = {"director": director}
    else:
        # for example: ["'t Hooft, Albert\tFallin' Floyd (2013)", '\t\tLittle Quentin (2010)',
        #  '\t\tTrippel Trappel Dierensinterklaas (2014)']
        first_line = line[0]
        parted = first_line.partition("\t")
        director = parted[0]
        title_first = parted[2].replace("\t", "")
        # we want to separate the title from the rest because imdb tends to add
        # extra info in the parathesis after the actual title
        # for example: Electric Shades of Grey (2001) (V)  (uncredited)
        # fortunately its separated by two white spaces after the actual title
        title_parted = title_first.partition("  ")[0]
        all_dir_movies = [title_parted]
        for remaining_title in line[1:len(line)]:
            remaining_title = remaining_title.replace("\t", "")
            title_parted = remaining_title.partition("  ")[0]
            all_dir_movies.append(title_parted)
        for title in all_dir_movies:
            movie_and_its_director[title] = {"director": director}

for title in movie_and_its_director:
    if title in movies:
        movies[title].update({"director": movie_and_its_director[title]["director"]})

for title in movies.keys():
    if "director" not in movies[title]:
        movies.pop(title, None)

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

print len(movies), "amount of movies that have genre"

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
    if mandatory_count >= 2 and gr_count > 0:   # change first condition to 2 if wanna have budget, 1 otherwise
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
        if "BT" in entry:
            bt = entry.partition("BT: ")[2]
            budget_temp.append(bt)
        if "GR" in entry:
            gr = entry.partition("GR: ")[2]
            gross_temp.append(gr)
    if title != "" and title in movies:
        movies[title].update({"budget": budget_temp, "gross": gross_temp})
    title = ""
    budget_temp = []
    gross_temp = []

for title in movies.keys():
    if "budget" not in movies[title]:
        movies.pop(title, None)

del business_raw, business_less_raw, movies_with_values, budget_temp, gross_temp, temp

print len(movies), "amount of movies that have stated business values"
######################################################
#                actors filtering
######################################################

top_actors = {}

with open("IMDB_files_link/_filtered_data/actors.scrapped") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for rank, name in enumerate(reader):
        _name = name[0]
        if _name not in top_actors:
            top_actors[_name] = {"rank": rank}

print "\t", len(top_actors), "top actors found"



