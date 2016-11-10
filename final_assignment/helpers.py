import csv


def language_fun():
    english_variations = set()
    lets_say_its_english = 0

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
            if language.startswith("English") and language != "English":
            # if "English" in language or "english" in language:
                english_variations.add(language)
                lets_say_its_english +=1

    for eng in english_variations:
        print eng
    print len(english_variations)
    print lets_say_its_english


# with open("IMDB_files_link/directors.list") as data_file:
#     reader = csv.reader(data_file, delimiter='\n')
#     for line in reader:
#         print "line" ,line
#         print "--------------------------"

directors_raw = []

with open("IMDB_files_link/_filtered_data/directors.filtered.new") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for line in reader:
        full_line = " ".join(line)
        directors_raw.append(full_line)

directors_less_raw = []
temp = []
for line in directors_raw[:100]:
    # each director is separated by new line character, in our case its an empty list of strings
    if line != "":
        # print "if", line
        temp.append(line)
    else:
        # print "else"
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
        title = parted[2].replace("\t","")
        if "(co-director)" in title:
            title = title.replace("  (co-director)","")
        movie_and_its_director[title] = {"director": director}
    else:
        #for example: ["'t Hooft, Albert\tFallin' Floyd (2013)", '\t\tLittle Quentin (2010)', '\t\tTrippel Trappel Dierensinterklaas (2014)']
        # print line
        first_line = line[0]
        parted = first_line.partition("\t")
        director = parted[0]
        title_first = parted[2].replace("\t", "")
        if "(co-director)" in title_first:
            title_first = title_first.replace("  (co-director)", "")
        temp = [title_first]
        for remaining_title in line[1:len(line)]:
            remaining_title = remaining_title.replace("\t","")
            if "(co-director)" in remaining_title:
                remaining_title = remaining_title.replace("  (co-director)", "")
            temp.append(remaining_title)
        print director, temp

print movie_and_its_director
