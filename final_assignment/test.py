import csv

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

# print movies
print movies_amount, "all movies"
print len(movies), "movies amount after year filter"
# count =0
# for line in movies:
#     print line, movies[line]
#     count+=1
#     if(count>100):break

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
        # if the language of the movie is not english delete its entry from movies
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
            pass
        else:
            movies.pop(title, None)

print len(movies), "movies amount after language filter"

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

print len(movies), "amount of movies that has rating"

count =0
for line in movies:
    print line, movies[line]
    count+=1
    if(count>100):break