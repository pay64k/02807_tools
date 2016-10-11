from mrjob.job import MRJob
import string


class MRWordCount(MRJob):

    def mapper(self, key, line):
        # yield "chars", len(line)
        # yield "words", len(line.split())
        # yield "lines", 1
        # yield line.split()
        for word in line.split():
            yield ''.join([x for x in word if x in string.ascii_letters]), 1
            # yield word, 1

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    MRWordCount.run()
