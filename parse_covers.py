import xml.etree.ElementTree as ET
import location
from collections import defaultdict

artists = defaultdict(int)      # songtitle => number of artists covering
languages = 0
mp3 = 0

root = ET.parse(location.dbroot + 'covers.xml').getroot()
for song in root:
  title = song.get('title')
  for artist in song:
    name = artist.get('name')
    artists[title] += 1
    if artist.get('language'): languages += 1
    if artist.get('mp3'): mp3 += 1

for song in sorted(artists) :
  print song,"("+str(artists[song])+" artists)"
print "languages",languages
print "mp3",mp3