import cPickle as pickle
import scipy.sparse as ss
from scipy import *
import distance

filename = "data_10points_10dims.dat"

spr_matrix = pickle.load(open(filename, 'r'))
dense_matrix = ss.csr_matrix(spr_matrix).toarray()


point_info = dict()


def dist(set_1,set_2):
    intersection = (set_1 & set_2).tolist().count(1)
    union = (set_1 | set_2).tolist().count(1)
    return 1 - intersection / float(union)


def region_query(data, point, eps):
    neighborhood = []
    for index,data_point in enumerate(data):
        if dist(data_point,point) <= eps:
            neighborhood.append([index,point])
    return neighborhood

def expand_cluster(point, point_index, neighPts, cluster, eps, minPt):
    local_points_info = dict()
    cluster.append(point_index)
    for index,point in enumerate(neighPts):
        if index in local_points_info:
            continue
        local_points_info[index]={'point_data':point, 'is_visited':True, 'is_noise':False}
        local_neighPts = region_query(neighPts,point,eps)
        if len(local_neighPts) >= minPt:
            neighPts.append(local_neighPts)
        if

minPts = 2
for index,point in enumerate(dense_matrix):
    cluster = []
    cluster_index = 1
    if index in point_info:
        continue
    point_info[index]={'point_data':point, 'is_visited':True, 'is_noise':False, 'cluster': 0}
    neighborPts = region_query(dense_matrix,point,0.4)
    if len(neighborPts) < minPts:
        point_info[index]['is_noise'] = True
    else:


print point_info
# def dbScan(data, eps, minPts):
#     for index, point in enumerate(data):
#         if point not in point_info:
#             point_info[index]
