from mrjob.job import MRJob
from mrjob.step import MRStep

class CountTriangles(MRJob):

    def mapper_1(self, _, line):
        node_1, node_2 = line.split()
        yield int(node_1), int(node_2)
        yield int(node_2), int(node_1)

    def reducer_1(self, key, values):
        for node in values:
            yield key, map(lambda x: x,values)

    def mapper_2(self, key, neighbours):
        for vertex in neighbours:
            yield vertex, [key,neighbours]

    def reducer_2(self, key, values):
        print key, values

    def steps(self):
        return [
            MRStep(mapper=self.mapper_1,
                   reducer=self.reducer_1
                   ),
            MRStep(mapper=self.mapper_2,
                   reducer=self.reducer_2
                   )
        ]

if __name__ == '__main__':
    CountTriangles.run()