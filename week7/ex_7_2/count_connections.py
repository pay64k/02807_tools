from mrjob.job import MRJob


class CountConnections(MRJob):

    def mapper(self, _, line):
        for vertex in line.split():
            yield vertex, 1


    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    CountConnections.run()