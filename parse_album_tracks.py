import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timedelta

songs = defaultdict(list)  # title -> (list of track lengths)

albumcount = 0
trackcount = 0
totalmins = 0
totalsecs = 0
anon = 0
known = 0
root = ET.parse('album_tracks.xml').getroot()
for collection in root:
  albumcount += 1
  id = collection.get('id')
  for track in collection:
    trackcount += 1
    length = track.get('length')
    for attrib in track.keys():
      if attrib == "title": continue
      if attrib == "length": continue
      if attrib == "artist": continue
      if attrib == "instrumental": continue
      if attrib == "live" : continue
      if attrib == "with" : continue
      if attrib == "version": continue
      if attrib == "remix"  : continue
      print "unexpected attribute",attrib
    title = track.get('title')
    if track.get('with'): title+=" [with "+track.get('with')+"]"
    if track.get('live'): title+=" [live]"
    elif collection.get('live'): title+=" [live]"
    if track.get('note'): print id,title,"has a note"
    songs[title].append(length)

for title,lengths in sorted(songs.iteritems()):
  #print title
  for length in lengths:
    #print "  ",length
    (min,sec) = length.split(':')
    if min != "#": totalmins += int(min); known += 1
    else: anon += 1
    if sec != "##": totalsecs += int(sec)

print "total collections",albumcount
print "total known tracks",known
print "total anon tracks",anon
print "total known mins", totalmins
print "total known secs", totalsecs
totalsecs += totalmins*60
print "total combined secs",totalsecs
average = totalsecs/known
print "average known track length seconds", average
print "estimated anon seconds",anon*average
totalsecs += anon*average
d = datetime(1,1,1) + timedelta(seconds=totalsecs)
print ("collection: %d DAYS %d HOURS %d MINUTES %d SECONDS" % (d.day-1, d.hour, d.minute, d.second))