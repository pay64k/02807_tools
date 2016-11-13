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
            language = parted[2].replace("\t", "")
            if language.startswith("English") and language != "English":
                # if "English" in language or "english" in language:
                english_variations.add(language)
                lets_say_its_english += 1

    for eng in english_variations:
        print eng
    print len(english_variations)
    print lets_say_its_english


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
# for line in directors_raw[:100]:
#     # each director is separated by new line character, in our case its an empty list of strings
#     if line != "":
#         # print "if", line
#         temp.append(line)
#     else:
#         # print "else"
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
#         if "(co-director)" in title:
#             title = title.replace("  (co-director)", "")
#         movie_and_its_director[title] = {"director": director}
#     else:
#         # for example: ["'t Hooft, Albert\tFallin' Floyd (2013)", '\t\tLittle Quentin (2010)',
#         #  '\t\tTrippel Trappel Dierensinterklaas (2014)']
#         first_line = line[0]
#         parted = first_line.partition("\t")
#         director = parted[0]
#         title_first = parted[2].replace("\t", "")
#         if "(co-director)" in title_first:
#             title_first = title_first.replace("  (co-director)", "")
#         all_dir_movies = [title_first]
#         for remaining_title in line[1:len(line)]:
#             remaining_title = remaining_title.replace("\t", "")
#             if "(co-director)" in remaining_title:
#                 remaining_title = remaining_title.replace("  (co-director)", "")
#             all_dir_movies.append(remaining_title)
#         for title in all_dir_movies:
#             movie_and_its_director[title] = {"director": director}
#
# print movie_and_its_director


import os
_proc_status = '/proc/%d/status' % os.getpid()

_scale = {'kB': 1024.0, 'mB': 1024.0*1024.0,
          'KB': 1024.0, 'MB': 1024.0*1024.0}

def _VmB(VmKey):
    '''Private.
    '''
    global _proc_status, _scale
     # get pseudo file  /proc/<pid>/status
    try:
        t = open(_proc_status)
        v = t.read()
        t.close()
    except:
        return 0.0  # non-Linux?
     # get VmKey line e.g. 'VmRSS:  9999  kB\n ...'
    i = v.index(VmKey)
    v = v[i:].split(None, 3)  # whitespace
    if len(v) < 3:
        return 0.0  # invalid format?
     # convert Vm value to bytes
    return float(v[1]) * _scale[v[2]]


def memory(since=0.0):
    '''Return memory usage in bytes.
    '''
    return _VmB('VmSize:') - since


def resident(since=0.0):
    '''Return resident memory usage in bytes.
    '''
    return _VmB('VmRSS:') - since


def stacksize(since=0.0):
    '''Return stack size in bytes.
    '''
    return _VmB('VmStk:') - since


# directors_raw = []
#
# with open("IMDB_files_link/_filtered_data/directors.filtered.new") as data_file:
#     reader = csv.reader(data_file, delimiter='\n')
#     for line in reader:
#         full_line = " ".join(line)
#         directors_raw.append(full_line)

# directors_less_raw = []
# temp = []
# for line in directors_raw:
#     # each director is separated by new line character, in our case its an empty list of strings
#     if line != "":
#         # print "if", line
#         temp.append(line)
#     else:
#         # print "else"
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
#         # if "(co-director)" in title:
#         #     title = title.replace("  (co-director)", "")
#         movie_and_its_director[title_parted] = {"director": director}
#     else:
#         # for example: ["'t Hooft, Albert\tFallin' Floyd (2013)", '\t\tLittle Quentin (2010)',
#         #  '\t\tTrippel Trappel Dierensinterklaas (2014)']
#         first_line = line[0]
#         parted = first_line.partition("\t")
#         director = parted[0]
#         title_first = parted[2].replace("\t", "")
#         title_parted = title_first.partition("  ")[0]
#         # if "(co-director)" in title_first:
#         #     title_first = title_first.replace("  (co-director)", "")
#         all_dir_movies = [title_parted]
#         for remaining_title in line[1:len(line)]:
#             remaining_title = remaining_title.replace("\t", "")
#             title_parted = remaining_title.partition("  ")[0]
#             # if "(co-director)" in remaining_title:
#             #     remaining_title = remaining_title.replace("  (co-director)", "")
#             all_dir_movies.append(title_parted)
#         for title in all_dir_movies:
#             movie_and_its_director[title] = {"director": director}
#
# print len(movie_and_its_director)

# business_raw = []
#
# with open("IMDB_files_link/_filtered_data/_test1") as data_file:
#     reader = csv.reader(data_file, delimiter='\n')
#     for line in reader:
#         full_line = " ".join(line)
#         business_raw.append(full_line)
#
# business_less_raw = []
# temp = []
# for line in business_raw:
#     if line != "----":
#         temp.append(line)
#     else:
#         business_less_raw.append(temp)
#         temp = []
#
# movies_with_values = []
# good_count = 0
# for movie in business_less_raw:
#     # print "movie", movie
#     for entry in movie:
#         # print "entry", entry
#         if "BT" in entry:
#             good_count +=1
#         if "GR" in entry:
#             good_count +=1
#     if good_count == 2:
#         movies_with_values.append(movie)
#     good_count = 0
#
# print movies_with_values


# business_raw = []
#
# with open("IMDB_files_link/_filtered_data/business.filtered") as data_file:
#     reader = csv.reader(data_file, delimiter='\n')
#     for line in reader:
#         full_line = " ".join(line)
#         business_raw.append(full_line)
#
# business_less_raw = []
# temp = []
# for line in business_raw:
#     if line != "----":
#         temp.append(line)
#     else:
#         business_less_raw.append(temp)
#         temp = []
#
# movies_with_values = []
# mandatory_count = 0
# gr_count = 0
# temp = []
# for movie in business_less_raw:
#     for entry in movie:
#         if "MV" in entry:
#             temp.append(entry)
#             mandatory_count += 1
#         if "BT" in entry:
#             temp.append(entry)
#             mandatory_count += 1
#         if "GR" in entry:
#             temp.append(entry)
#             gr_count += 1
#     if mandatory_count >= 2 and gr_count > 0:
#         movies_with_values.append(temp)
#     temp = []
#     mandatory_count = 0
#     gr_count = 0
#
# movie_business = {}
# budget_temp = []
# gross_temp = []
# for movie in movies_with_values:
#     for entry in movie:
#         if "MV" in entry:
#             title = entry.partition("MV: ")[2]
#         if "BT" in entry:
#             bt = entry.partition("BT: ")[2]
#             budget_temp.append(bt)
#         if "GR" in entry:
#             gr = entry.partition("GR: ")[2]
#             gross_temp.append(gr)
#
#     movie_business[title]={"budget":budget_temp, "gross": gross_temp}
#
#     budget_temp = []
#     gross_temp = []


# print len(movie_business), "amount of movies that have stated business values"

# all_actors = {}
#
# with open("IMDB_files_link/_filtered_data/top_1000.filtered") as data_file:
#     reader = csv.reader(data_file, delimiter=',')
#     for line in reader:
#         rank = line[0]
#         name = line[5]
#         print line
#         print rank, name
#         all_actors[name]=rank
# print all_actors
# print len(all_actors)

# top_actors = {}
#
# with open("IMDB_files_link/_filtered_data/actors.scrapped") as data_file:
#     reader = csv.reader(data_file, delimiter='\n')
#     for rank, name in enumerate(reader):
#         _name = name[0]
#         if _name not in top_actors:
#             top_actors[_name] = {"rank": rank}

# top_actors = {}
#
# with open("IMDB_files_link/_filtered_data/actors.scrapped") as data_file:
#     reader = csv.reader(data_file, delimiter='\n')
#     for rank, name in enumerate(reader):
#         _name = name[0]
#         if _name not in top_actors:
#             top_actors[_name] = {"rank": rank+1}


# print top_actors["Evan Rachel Wood"]
# print top_actors["Amy Adams"]
# print top_actors["Jana Kramer"]
# print top_actors["Nadine Garner"]
# print "\t", len(top_actors), "top actors found"

actors_raw = []
c=0
with open("IMDB_files_link/_filtered_data/actors.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for line in reader:
        c+=1
        full_line = " ".join(line)
        actors_raw.append(full_line)
        # if c >=100: break

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

for entry in actors_less_raw[:1000]:
    actor = entry[0]
    if "," in actor:
        parted = actor.partition(", ")
        # first name then surname
        actor = parted[2] + " " + parted[0]
    for role in entry[1:len(entry)]:
        movie_name = role.partition("  ")[0]
        if movie_name not in movie_and_roles:
            movie_and_roles[movie_name] = {"cast":[actor]}
        else:
            movie_and_roles[movie_name]["cast"].append(actor)

for line in movie_and_roles:
    print line, movie_and_roles[line]