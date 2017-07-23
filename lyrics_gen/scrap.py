import urllib2, time, os, csv
from random import randint
from bs4 import BeautifulSoup
import unicodedata, string

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

base_url = 'http://www.tekstowo.pl'
base_path = 'songs/'

response = urllib2.urlopen(base_url+'/artysci_na,A,strona,1.html')
html = response.read()
soup = BeautifulSoup(html, 'html.parser')

artists_html_a = soup.find("div", class_="content").find_all("a", class_="title")

artist_names_and_links = {}

for ar in artists_html_a:
    artist_names_and_links[ar["title"]] = ar["href"]

print artist_names_and_links


response = urllib2.urlopen(base_url + artist_names_and_links['A'])
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
artist_song_html_a = soup.find("div", class_="ranking-lista").find_all("a", class_="title")
# print artist_song_html_a

songs_and_links = {}
for song in artist_song_html_a:
    songs_and_links[song["title"]] = song["href"]

response = urllib2.urlopen(base_url + songs_and_links['A - 2:59'])
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
text_html = soup.find("div", class_ = 'song-text')
text = text_html.get_text()
# print text
#
# for a in artist_names_and_links.keys():
#     # os.makedirs(base_path + a)
#     print a


def LOG(msg):
    print("------" + msg + "------")


def get_artist_list(letter, page, max):
    LOG("Scrap: letter " + letter + " page: " + page + '/' + max)
    try:
        response = urllib2.urlopen(base_url + '/artysci_na,' + letter + ',strona,' + page + '.html')
    except:
        print "ERROR, failed for:", letter, page
        return {}
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    artists_html_a = soup.find("div", class_="content").find_all("a", class_="title")
    artist_names_and_links = {}
    for ar in artists_html_a:
        artist_names_and_links[ar["title"]] = ar["href"]
    return artist_names_and_links


def find_max_page_number_per_letter(letter):
    response = urllib2.urlopen(base_url + '/artysci_na,' + letter + ',strona,1.html')
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    pages_a =  soup.find('div', class_ = "content").find_all('a',class_ = 'page')
    only_page_numbers = []
    for page in pages_a:
        only_page_numbers.append(int(page['title']))
    return max(only_page_numbers)


def find_max_page_per_artist(artist_link):
    response = urllib2.urlopen(base_url + artist_link)
    print base_url + artist_link
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    pages_a =  soup.find('div', class_ = "content").find_all('a',class_ = 'page')
    only_page_numbers = []
    for page in pages_a:
        only_page_numbers.append(int(page['title']))
    if len(only_page_numbers) == 0:
        return 1
    else:
        return max(only_page_numbers)

def init_get_all_artists():
    with open('artists_and_links.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)

        amount_pages_per_artist_letter = {}
        for letter in list(string.ascii_uppercase):
            amount_pages_per_artist_letter[letter] = find_max_page_number_per_letter(letter)

        all_artists = {}

        for letter in amount_pages_per_artist_letter.keys():
            max_page = int(amount_pages_per_artist_letter[letter]) + 1
            for page in range(1,max_page):
                # print get_artist_list(letter, str(page))
                artist_per_page = get_artist_list(letter, str(page), str(max_page))
                for e in artist_per_page.keys():
                    all_artists[e] = artist_per_page[e]
                    writer.writerow([e, artist_per_page[e]])

        # with open('artists_and_links.csv', 'wb') as csv_file:
        #     writer = csv.writer(csv_file)
        #     for key, value in all_artists.items():
        #         print key,value
        #         writer.writerow([key, value])


def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

# init_get_all_artists()
all_artists_with_links = {}
filename = 'artists_and_links_full.csv'
reader = unicode_csv_reader(open(filename))

for field1, field2 in reader:
    all_artists_with_links[field1] = field2

for a in all_artists_with_links.keys():
    print find_max_page_per_artist(all_artists_with_links[a])