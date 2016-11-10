import csv

movies ={}

with open("IMDB_files_link/_filtered_data/movies.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\r')
    for line in reader:
        full_line = " ".join(line)
        # partition returns 3-tuple: (part_before_delimiter, delimiter, part_after_delimiter)
        parted = full_line.partition("\t")
        title = parted[0]
        # in the part_after_delimiter we delete all \t characters
        year = parted[2].replace("\t","")
        # check year validity
        if year != "????" and int(year) >= 1986:
            movies[title]={"year": year}

# print movies

# print len(movies)
# count =0
# for line in movies:
#     print line, movies[line]
#     count+=1
#     if(count>100):break



