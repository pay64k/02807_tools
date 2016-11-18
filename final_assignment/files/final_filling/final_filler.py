import file_save_load_filler as fsl

movies_3_actors = fsl.read_from_file('imdb_dataset_v6.0.1_3_actors_complete_plots',3)
movies_6_actors = fsl.read_from_file('imdb_dataset_v7.1_6_actors_complete_no_plots',6)

for title in movies_6_actors:
    movies_6_actors[title]["plot"] = movies_3_actors[title]["plot"]

fsl.save_to_dataset(movies_6_actors,6)