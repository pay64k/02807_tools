import cPickle as pickle
import scipy.sparse as ss
from matplotlib._path import point_in_path
from scipy import *
import numpy as np


filename = "data_10points_10dims.dat"

spr_matrix = pickle.load(open(filename, 'r'))
dense_matrix = ss.csr_matrix(spr_matrix).toarray()


def dist(set_1,set_2):
    intersection = (set_1 & set_2).tolist().count(1)
    union = (set_1 | set_2).tolist().count(1)
    return 1 - intersection / float(union)

# -------- --------------- --------

def regionQuery(data,one_point_data):
    neighbourhood = []

    for index in data:
        point_to_compare = points_info[index]['point_data']

        if dist(point_to_compare,one_point_data) <= eps:
            neighbourhood.append(index)

    return neighbourhood

# -------- --------------- --------

def expandCluster(point_info,neighborPts):

    # neighborPts_visited_indices = []

    for index in neighborPts:

        if index not in visited_indices:
            visited_indices.append(index)
            neighborPts_prime = regionQuery(neighborPts,point_info)

            if len(neighborPts_prime) >= minPts:
                neighborPts = neighborPts + neighborPts_prime

        if points_info[index]['cluster'] == 'NaN':
            points_info[index]['cluster'] = current_cluster_index

# -------- Prepare lookup point dictionary --------
points_info = dict()

for ind, matrix_entry in enumerate(dense_matrix):
    points_info[ind] = {'point_index': ind, 'point_data': matrix_entry, 'cluster': "NaN"}
print "-------- All points info: --------"
for point in points_info:
    print points_info[point]
print "-------- --------------- --------"

# -------- GLOBAL variables --------
visited_indices = []
noise_indices = []
clusters = dict()
current_cluster_index = 0

# -------- DBSCAN parameters --------
minPts = 2
eps = 0.4

# -------- DBSCAN main --------

for point_index in points_info:
    if point_index in visited_indices:
        continue

    visited_indices.append(point_index)

    neighborPts = regionQuery(range(0,len(points_info)),points_info[point_index]['point_data'])

    if len(neighborPts) < minPts:
        noise_indices.append(point_index)
    else:
        current_cluster_index += 1
        points_info[point_index]['cluster'] = current_cluster_index
        expandCluster(points_info[point_index]['point_data'],neighborPts)

print "-------- All noise indices: --------"
print noise_indices


print "-------- Updated points info: --------"
for point in points_info:
    print points_info[point]
print "-------- --------------- --------"

distinct_clusters = set()

for bla in points_info:
    distinct_clusters.add(points_info[bla]['cluster'])

print len(distinct_clusters)