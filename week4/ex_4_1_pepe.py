import cPickle as pickle
import scipy.sparse as ss
from scipy import *
from datetime import datetime

# -------- GLOBAL variables --------
visited_indices = []
noise_indices = []
clusters = dict()
current_cluster_index = 0
added_to_any_cluster = []
points_info = dict()
# -------- --------------- --------

def clean_variables():
    global visited_indices
    global noise_indices
    global clusters
    global current_cluster_index
    global added_to_any_cluster
    global points_info
    visited_indices = []

    noise_indices = []
    clusters = dict()
    current_cluster_index = 0
    added_to_any_cluster = []
    points_info = dict()

def dist(set_1,set_2):
    intersection = (set_1 & set_2).tolist().count(1)
    union = (set_1 | set_2).tolist().count(1)
    return 1 - intersection / float(union)

# -------- --------------- --------


def regionQuery(one_point_data):
    neighbourhood = []

    for index in points_info:
        point_to_compare = points_info[index]['point_data']

        if dist(point_to_compare,one_point_data) <= eps:
            neighbourhood.append(index)

    return neighbourhood

# -------- --------------- --------


def expandCluster(point_info,neighborPts):

    for index in neighborPts:

        if index not in visited_indices:
            visited_indices.append(index)
            neighborPts_prime = regionQuery(points_info[index]['point_data'])

            if len(neighborPts_prime) >= minPts:
                neighborPts += neighborPts_prime

        if index not in added_to_any_cluster:
            clusters[current_cluster_index].append(index)
            added_to_any_cluster.append(index)


# -------- DBSCAN parameters --------
minPts = 2
eps = 0.3

# -------- DBSCAN main --------


def dbscan(filename,_eps):
    global eps
    eps = _eps
    global current_cluster_index

    spr_matrix = pickle.load(open(filename, 'r'))
    dense_matrix = ss.csr_matrix(spr_matrix).toarray()

    # -------- Prepare lookup point dictionary --------

    for ind, matrix_entry in enumerate(dense_matrix):
        points_info[ind] = {'point_index': ind, 'point_data': matrix_entry, 'cluster': "NaN"}

    # -------- --------------- --------

    for point_index in points_info:
        if point_index in visited_indices:
            continue

        visited_indices.append(point_index) # mark P as visited

        neighborPts = regionQuery(points_info[point_index]['point_data']) # NeighborPts = regionQuery(P, eps)

        if len(neighborPts) < minPts: # if sizeof(NeighborPts) < MinPts
            noise_indices.append(point_index)  # mark P as NOISE
        else:
            current_cluster_index += 1
            clusters[current_cluster_index] = []
            clusters[current_cluster_index].append(point_index)
            added_to_any_cluster.append(point_index)
            expandCluster(points_info[point_index]['point_data'],neighborPts)

# -------- --------------- --------

filename1 = "data_10points_10dims.dat"
filename2 = "data_100points_100dims.dat"
filename3 = "data_1000points_1000dims.dat"
filename4 = "data_10000points_10000dims.dat"
filename5 = "data_100000points_100000dims.dat"

old_time = datetime.now()
dbscan(filename1, 0.4)
print filename1 , "-----------"
print "Amount of different clusters: ", len(clusters)
max_nodes = 0
for cluster in clusters:
    print "Amount of nodes in cluster nr.", cluster, ":", len(clusters[cluster])
    cur_max = len(clusters[cluster])
    if cur_max > max_nodes:
        max_nodes = cur_max
print "Amount of noise nodes: " , len(noise_indices)
print "Amount of nodes in the biggest cluster: ", max_nodes
print "Execution time: " , datetime.now() - old_time
clean_variables()
print "-----------"

old_time = datetime.now()
dbscan(filename2, 0.3)
print filename2 , "-----------"
print "Amount of different clusters: ", len(clusters)
max_nodes = 0
for cluster in clusters:
    print "Amount of nodes in cluster nr.", cluster, ":", len(clusters[cluster])
    cur_max = len(clusters[cluster])
    if cur_max > max_nodes:
        max_nodes = cur_max
print "Amount of noise nodes: " , len(noise_indices)
print "Amount of nodes in the biggest cluster: ", max_nodes
print "Execution time: " , datetime.now() - old_time
clean_variables()
print "-----------"

old_time = datetime.now()
dbscan(filename3, 0.15)
print filename3 , "-----------"
print "Amount of different clusters: ", len(clusters)
max_nodes = 0
for cluster in clusters:
    print "Amount of nodes in cluster nr.", cluster, ":", len(clusters[cluster])
    cur_max = len(clusters[cluster])
    if cur_max > max_nodes:
        max_nodes = cur_max
print "Amount of noise nodes: " , len(noise_indices)
print "Amount of nodes in the biggest cluster: ", max_nodes
print "Execution time: " , datetime.now() - old_time
clean_variables()
print "-----------"

old_time = datetime.now()
dbscan(filename4, 0.15)
print filename4 , "-----------"
print "Amount of different clusters: ", len(clusters)
max_nodes = 0
for cluster in clusters:
    print "Amount of nodes in cluster nr.", cluster, ":", len(clusters[cluster])
    cur_max = len(clusters[cluster])
    if cur_max > max_nodes:
        max_nodes = cur_max
print "Amount of noise nodes: " , len(noise_indices)
print "Amount of nodes in the biggest cluster: ", max_nodes
print "Execution time: " , datetime.now() - old_time
clean_variables()
print "-----------"

old_time = datetime.now()
dbscan(filename5, 0.15)
print filename5 , "-----------"
print "Amount of different clusters: ", len(clusters)
max_nodes = 0
for cluster in clusters:
    print "Amount of nodes in cluster nr.", cluster, ":", len(clusters[cluster])
    cur_max = len(clusters[cluster])
    if cur_max > max_nodes:
        max_nodes = cur_max
print "Amount of noise nodes: " , len(noise_indices)
print "Amount of nodes in the biggest cluster: ", max_nodes
print "Execution time: " , datetime.now() - old_time
clean_variables()
print "-----------"