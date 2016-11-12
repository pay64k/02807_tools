import urllib2, time
from random import randint

for req in range(5401,10001,50):

    response = urllib2.urlopen('http://www.imdb.com/search/name?gender=male,female&start='+str(req))
    # print response
    html = response.read()

    with open("IMDB_files_link/imdb_scrap_more_raw/"+str((req-1)/50), "w") as text_file:
        text_file.write(html)
    print "file",(req-1)/50 ,"/199 done"
    time.sleep(randint(30,80))

