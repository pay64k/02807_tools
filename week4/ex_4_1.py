import cPickle as pickle
import scipy.sparse as ss
from scipy import *
import distance

filename = "data_100points_100dims.dat"

spr_matrix = pickle.load(open(filename, 'r'))
dense_matrix = ss.csr_matrix(spr_matrix).toarray()


def dist(set_1,set_2):
    intersection = (set_1 & set_2).tolist().count(1)
    union = (set_1 | set_2).tolist().count(1)
    return 1 - intersection / float(union)


def region_query(data, point, eps):
    # neighborhood = []
    neighborhood = dict()
    # print "DATA: ", data
    for index in data:
        if dist(data[index]['point_data'],point['point_data']) <= eps:
            # neighborhood.append([point['point_index'], data[index]])
            neighborhood[index]=data[index]
    # print "neighborhood: " , neighborhood
    return neighborhood
    # for index,data_point in enumerate(data):
    #     if dist(data_point,point) <= eps:
    #         neighborhood.append([index,point])
    # # print "region_query for point index: ", point, neighborhood
    # return neighborhood


def expand_cluster(point__, neighPts, cluster_index, _eps, _minPt):

    local_points_info = dict()
    point_info[point__['point_index']]['cluster'] = cluster_index

    # print "neighPts: ", neighPts

    for point_index in neighPts:
        # bla = neighPts[point_index]
        neighPts[point_index]['is_visited'] = False

    for neigh_point in neighPts:

        if neighPts[neigh_point]['is_visited']:
            continue

        neighPts[neigh_point]['is_visited'] = True

        temp_points_data=[]
        # for i,point_ in neighPts:
        #     temp_points_data.append(point_['point_data'])

        local_neighPts = region_query(neighPts,neighPts[neigh_point],_eps)
        # print "local_neighPts: ", local_neighPts
        # print "len(local_neighPts): ", len(local_neighPts)
        if len(local_neighPts) >= _minPt:
            neighPts.update(local_neighPts)

        if neighPts[neigh_point]['cluster'] == 0:

            point_info[ neighPts[neigh_point]['point_index'] ]['cluster'] = cluster_index

point_info = dict()
minPts = 2
eps = 0.3
cluster_number = 0

for ind, matrix_entry in enumerate(dense_matrix):
    if ind not in point_info:
        # set point info:
        point_info[ind] = {'point_index': ind, 'point_data': matrix_entry, 'is_visited': False, 'is_noise': False, 'cluster': 0}

for index in point_info:

    # if index not in point_info:
    #     # set point info:
    #     point_info[index] = {'point_index': index, 'point_data': point, 'is_visited': False, 'is_noise': False, 'cluster': 0}

    if point_info[index]['is_visited']:
        continue

    point_info[index]['is_visited'] = True
    # neighborPts = region_query(dense_matrix, point_info[index], eps)
    neighborPts = region_query(point_info, point_info[index], eps)
    # print "point index: ", index,"neighbours: ", neighborPts

    if len(neighborPts) < minPts:
        point_info[index]['is_noise'] = True
        point_info[index]['cluster'] = -1
    else:
        cluster_number += 1
        expand_cluster(point_info[index],neighborPts,cluster_number,eps,minPts)

distinct_clusters = set()

for bla in point_info:
    # print bla,point_info[bla]
    distinct_clusters.add(point_info[bla]['cluster'])

# print point_info

print "distinct_clusters: ", distinct_clusters
print "amount of distinct_clusters: ", len(distinct_clusters)

# def dbScan(data, eps, minPts):
#     for index, point in enumerate(data):
#         if point not in point_info:
#             point_info[index]
