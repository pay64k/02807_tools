import json


def read_file(filename):
    with open(filename) as data_file:
        return json.load(data_file)


for bucket_id in buckets:
    similarities_for_one_id = buckets[bucket_id]
    # print similarities_for_one_id
    for sim in similarities_for_one_id:
        if similarities_for_one_id[sim]["similarity"] >= 0.8:
            print bucket_id, "is similar to:", similarities_for_one_id[sim]["id"]

for bla in data_raw_filtered:
    if bla["id"]=="5556":
        print bla["body"]





