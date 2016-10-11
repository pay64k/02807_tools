from mrjob.job import MRJob

class DetermineGraph(MRJob):

    def mapper(self, key, line):
        print line


    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    DetermineGraph.run()