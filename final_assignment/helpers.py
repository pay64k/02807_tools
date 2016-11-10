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

bla = []

with open("IMDB_files_link/directors.list") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for line in reader:
        full_line = " ".join(line)
        if len(full_line) != 0:
            bla.append(full_line)

# for a in bla[:100]:
#     print a

print bla[11]
print bla[12]
print bla[13]

# ok = []
# with open("IMDB_files_link/directors.list", "r") as data_file:
#     for line in data_file:
#         if line == " ":
#             print "bla"
