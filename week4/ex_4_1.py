import cPickle as pickle
import scipy.sparse as ss
from scipy import *


filename = "data_10points_10dims.dat"

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
        if dist(point['point_data'],data[index]['point_data']) <= eps:
            # neighborhood.append([point['point_index'], data[index]])
            neighborhood[index]=dict(data[index])
    # print "point: ", point['point_index'] ," neighborhood: " , neighborhood
    return neighborhood



def expand_cluster(point__, _neighPts, cluster_index, _eps, _minPt):


    point_info[point__['point_index']]['cluster'] = cluster_index

    # print "neighPts: ", neighPts
    neighPts = dict(_neighPts)
    for point_index in neighPts:
        neighPts[point_index]['is_visited'] = False
        print "tuu" , neighPts[point_index]

    for neigh_point in neighPts.keys():
        # print "LENNNN: ", len(neighPts)
        if neighPts[neigh_point]['is_visited']:
            continue

        neighPts[neigh_point]['is_visited'] = True
        print neighPts[neigh_point]
        # print point_info[neighPts[neigh_point]['point_index']]['is_visited']
        temp_points_data=[]
        # for i,point_ in neighPts:
        #     temp_points_data.append(point_['point_data'])

        local_neighPts = dict(region_query(neighPts,neighPts[neigh_point],_eps))
        # print "neighPts: ", neighPts
        # print "local_neighPts: ", local_neighPts

        # print "len(local_neighPts): ", len(local_neighPts)
        if len(local_neighPts) >= _minPt:
            # neighPts.update(local_neighPts)
            for ind in local_neighPts:
                neighPts[rand()] = local_neighPts[ind]
        # print "neighPts(updated): ", neighPts

        if neighPts[neigh_point]['cluster'] == "NaN":

            point_info[ neighPts[neigh_point]['point_index'] ]['cluster'] = cluster_index

point_info = dict()
minPts = 2
eps = 0.4
cluster_number = 0

for ind, matrix_entry in enumerate(dense_matrix):
    if ind not in point_info:
        # set point info:
        point_info[ind] = {'point_index': ind, 'point_data': matrix_entry, 'is_visited': False, 'is_noise': False, 'cluster': "NaN"}


for index in point_info:
    print point_info[index]

    # if index not in point_info:
    #     # set point info:
    #     point_info[index] = {'point_index': index, 'point_data': point, 'is_visited': False, 'is_noise': False, 'cluster': 0}

    print "point nr " , point_info[index]['point_index']," is visited ", point_info[index]['is_visited']

    if point_info[index]['is_visited']:
        print "continue",index
        continue

    point_info[index]['is_visited'] = True
    # neighborPts = region_query(dense_matrix, point_info[index], eps)
    print "current point:", point_info[index]['point_index']
    neighborPts = dict(region_query(point_info, point_info[index], eps))
    # print "point index: ", index,"neighbours: ", neighborPts

    if len(neighborPts) < minPts:
        point_info[index]['is_noise'] = True
        point_info[index]['cluster'] = -1
    else:
        cluster_number += 1
        expand_cluster(point_info[index],neighborPts,cluster_number,eps,minPts)

distinct_clusters = set()

for bla in point_info:
    print bla,point_info[bla]
    distinct_clusters.add(point_info[bla]['cluster'])

# print point_info

print "distinct_clusters: ", distinct_clusters
print "amount of distinct_clusters: ", len(distinct_clusters)

# def dbScan(data, eps, minPts):
#     for index, point in enumerate(data):
#         if point not in point_info:
#             point_info[index]
