# a proper solution utilizing steps, but still needs to be ran for every graph (just like in ex_7_2.sh),
# but without the first step
from mrjob.job import MRJob
from mrjob.step import MRStep


class EulerStepsJob(MRJob):
    def mapper_get_degree(self, _, line):
        for vertex in line.split():
            yield vertex, 1

    def reducer_count_degree(self, key, values):
        yield key, sum(values)

    def mapper_determine(self, key, degree):
        if degree % 2 == 0:
            yield "even", 1
        else:
            yield "odd", 1

    def reducer_count_determine(self, key, values):
        yield key, sum(values)

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_degree,
                   reducer=self.reducer_count_degree),
            MRStep(mapper=self.mapper_determine,
                   reducer=self.reducer_count_determine)
        ]

if __name__ == '__main__':
    EulerStepsJob.run()
