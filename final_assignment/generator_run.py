import generator_mrjob as gmr
import datetime

old_time = datetime.datetime.now()

mr_job = gmr.map_movies_years(args=['IMDB_files_link/_filtered_data/big_movies_2'])
with mr_job.make_runner() as runner:
    runner.run()

print datetime.datetime.now() - old_time



# mr_job = gmr.map_genres(args=['IMDB_files_link/_filtered_data/genres.filtered'])
# with mr_job.make_runner() as runner:
#     runner.run()