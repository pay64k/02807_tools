import urllib2, time

for req in range(1,2001,50):

    response = urllib2.urlopen('http://www.imdb.com/search/name?gender=male,female&start='+str(req))
    # print response
    html = response.read()

    with open("imdb_scrap/"+str(req), "w") as text_file:
        text_file.write(html)
    print "file",req,"/",2001,"done"
    time.sleep(5)

