from mrjob.job import MRJob


class CountConnections(MRJob):

    def mapper(self, _, line):
        for edge in line.split():
            for vertex in edge:
                yield vertex, 1


    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    CountConnections.run()