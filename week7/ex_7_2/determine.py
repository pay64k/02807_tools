from mrjob.job import MRJob

class DetermineGraph(MRJob):

    def mapper(self, key, line):
        vertex = line.split()[0]
        degree = int(line.split()[1])
        if degree % 2 == 0:
            yield "even", 1
        else:
            yield "odd", 1


    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    DetermineGraph.run()