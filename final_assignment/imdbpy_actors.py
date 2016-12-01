from imdb import IMDb
import json, requests
import time
from random import randint
import file_save_load as fsl
ia = IMDb()

base_url = "http://www.omdbapi.com/?i=tt"

movies = fsl.read_from_file("imdb_dataset_v6.0.2_3_actors_complete.tsv", 3)
log_file = open('log_file.txt', 'a', 0)


def change_movie_data_3actors(title, new_list):
    movies[title]["actor1"] = new_list[0]
    movies[title]["actor2"] = new_list[1]
    movies[title]["actor3"] = new_list[2]


def logger(*args):
    msg = ""
    for a in args:
        msg += a
    log_file.write(msg +"\n")
    print msg


def format_title(t):
    if "/" in t:
        t = t.partition("/")[0]
        t += ")"
        return t
    return t


logger("------------LOG START ", str(time.strftime("%Y-%m-%d\t%H:%M:%S")), "------------")

movieID_list = ""
movieID = ""
movie_url = ""
response = ""

failed_movies = []

for title in movies:
    try:
        movieID_list = ia.search_movie(format_title(title))
        movieID = movieID_list[0].movieID
        ok = True
    except:
        logger("ERROR 1:\t", title, "\tnot found! The list returned:\t", movieID_list)
        failed_movies.append(title)
        ok = False

    if ok:
        try:
            movie_url = base_url + str(movieID)
            response = requests.get(movie_url)
            movie_info = json.loads(response.text)
            change_movie_data_3actors(title, [a for a in movie_info['Actors'].split(',')][:3])
            logger("OK\t", title, "\tactors:\t",movie_info['Actors'])
        except:
            logger("ERROR 2:\t", title, "\twhile getting movieID:\t", movieID, "\tURL:", movie_url, "\tresponse:\t", str(response))
            failed_movies.append(title)

    movieID_list = ""
    movieID = ""
    movie_url = ""
    response = ""
    time.sleep(randint(15, 30))


logger("----FAILED MOVIES----")
for title in failed_movies:
    logger(title)

fsl.save_to_dataset(movies, 3)