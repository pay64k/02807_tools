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


def regionQuery(data,one_point_data,epsilon):
    neighbourhood = []
    for index in data:
        point_to_compare = point_info[index]['point_data']
        if dist(point_to_compare,one_point_data) <= epsilon:
            neighbourhood.append(index)
    return neighbourhood

def expandCluster():
    0

# -------- Prepare lookup point dictionary --------
point_info = dict()

for ind, matrix_entry in enumerate(dense_matrix):
    point_info[ind] = {'point_index': ind, 'point_data': matrix_entry, 'cluster': "NaN"}
print "-------- All points info: --------"
for point in point_info:
    print point_info[point]
print "-------- --------------- --------"

# -------- GLOBAL variables --------
visited_indices = []
noise_indices = []
clusters = []
cluster_index = 0

# -------- DBSCAN parameters --------
minPts = 2
eps = 0.4

# -------- DBSCAN main --------

for point_index in point_info:
    if point_index in visited_indices:
        continue

        visited_indices.append(point_index)

    neighborPts = regionQuery(range(0,len(point_info)),point_info[point_index]['point_data'],eps)
    if len(neighborPts) < minPts:
        noise_indices.append(point_index)
    else:
        cluster_index += 1
        # expandCluster()

print noise_indices