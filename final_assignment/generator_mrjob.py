from mrjob.job import MRJob
from mrjob.step import MRStep

class map_movies_years(MRJob):
    def mapper_get_movies(self,_,line):
        parted = line.partition("\t")
        title = parted[0]
        # in the part_after_delimiter we delete all \t characters
        year = parted[2].replace("\t", "")
        # check year validity
        try:
            if year != "????" and int(year) >= 1986:
                yield title.decode('latin-1'), {"year": year}
        except:
            pass

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_movies)
        ]

class map_genres(MRJob):
    def mapper_get_genres(self,_,line):
        parted = line.partition("\t")
        title = parted[0]
        genre = parted[2].replace("\t", "")
        print "blaa"
        yield title.decode('latin-1'), genre

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_genres)
        ]

if __name__ == '__main__':
    map_movies_years.run()