from bs4 import BeautifulSoup


file = open("IMDB_files_link/imdb_scrap/1")

soup = BeautifulSoup(file, 'html.parser')

# print(soup.prettify())
names = set()
for link in soup.find_all('a'):
    name = link.get('title')
    names.add(name)

good_names = set()
for bla in names:
    # print str(bla).join("")
    if "IMDb" not in str(bla).join(""):
        good_names.add(bla)

print len(names)