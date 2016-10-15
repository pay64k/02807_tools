from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime
import collections


class CountTriangles(MRJob):

    def mapper(self, _, line):
        node_1, node_2 = line.split()
        yield int(node_1), int(node_2)
        yield int(node_2), int(node_1)

    def reducer(self, key_node, connected_nodes):
        # print "key", key_node
        # for bla in connected_nodes:
        #     print bla
        # print "------+"
        # values_copy = reduce(lambda x, y: x + [y], values, [])
        connected_nodes_copy = list(connected_nodes)
        for node in connected_nodes_copy:
            # print sorted([key_node,node]), connected_nodes_copy
            yield sorted([key_node,node]), connected_nodes_copy

    def reducer_2(self, key, values):

        # print "key",key
        # bla = list(values)
        # print bla

        list_of_nodes_sets = []
        for node_list in values:
            list_of_nodes_sets.append(set(node_list))
            # if key == [126,127]: print node_list
        # print "key",key, list_of_nodes_sets
        intersec = set.intersection(*list_of_nodes_sets)

        # if len(intersec)>1:
        #     print intersec;
        #     print key
        # print "----"
        # print "bla",list(intersec)
        # print "key", key, "intersection",list(intersec)
        yield key, list(intersec)



    def reducer_3(self, key, values):
        # print "key",key
        # bla = list(values)
        # print bla
        # pass
        # node_list = list(key)
        # for node in values:
        #     if node !=[]:
        #         node_list.append(node)
        # # flatten_list = [val for sublist in node_list for val in sublist]
        # maybe_a_triangle = sorted(self.flatten(node_list))
        # print maybe_a_triangle
        # if len(maybe_a_triangle)==3:
        #     yield maybe_a_triangle, 1
        # blabla = list(values)
        neighbour_nodes = sorted(self.flatten(values))
        # print neighbour_nodes
        # keys_list = list(key)

        if len(neighbour_nodes) > 0:
            for node in neighbour_nodes:
                triangle = []
                triangle += key
                triangle += [node]
                triangle = sorted(triangle)
                # print "key", key, "triangle",triangle, "neighbour_nodes", neighbour_nodes
                yield triangle, 1


    def reducer_4(self,key,val):
        # print key
        # for bla in val:
        #     print bla
        # print "----"
        yield "a triangle", 1

    def reducer_5(self,key,val):
        yield "amount", sum(val)

    def flatten(self,l):
        for el in l:
            if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
                for sub in self.flatten(el):
                    yield sub
            else:
                yield el

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer
                   ),
            MRStep(reducer=self.reducer_2
                   ),
            MRStep(reducer=self.reducer_3
                   ),
            MRStep(reducer=self.reducer_4
                   ),
            MRStep(reducer=self.reducer_5
                   )
        ]

if __name__ == '__main__':
    old_time = datetime.now()
    CountTriangles.run()
    print "run time:", datetime.now() - old_time