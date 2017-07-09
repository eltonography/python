import xml.etree.ElementTree as ET
import os.path
import getimageinfo

picpath = "c:/users/david/documents/elton/eltonography/albums/pix/guest/"

### LOAD SONGS
unlinkablesongs = []
songs = {}  # title => fileID
root = ET.parse('songs.xml').getroot()
for song in root:
  title = song.get('title')
  if title == None: print "error: missing title for ",song.get('fileID')
  if title in songs: print "error: repeat song:",title
  if song.get('nolink'):
    unlinkablesongs.append(title)
    continue
  songs[title] = song.get('fileID')
  if (song.get('alias')): songs[song.get('alias')] = song.get('fileID')


## LOAD GUEST APPERANCES
root = ET.parse('guest.xml').getroot()
for release in root:
  if release.get('private') != None: continue
  if release.tag == 'album':
    if release.get('title') == None: print "error: appearances album missing title tag"
    title = release.get('title')
    if release.get('pic') == None : print "error: no pic for",title
    if release.get('year') == None: print "error: no year for", title
    if release.get('artist') == None: print "error: no artist for",title
  elif release.tag == 'single':
    if release.get('artist') == None: print "error: no artist for single"
  if release.get('pic') == None: continue
  pic = release.get('pic')
  if not os.path.isfile(picpath+pic): print "error: can't find picture", pic
  else:
    print "getting dimensions for",pic
    imgdata = open(picpath+pic,'rb').read()
    (type,width,height) = getimageinfo.getImageInfo(imgdata)


  for element in release:
    if element.tag != 'track': continue # skip notes and issues
    if element.get('artist'): continue  # skip other artist songs
    if element.get('elton'): continue   # elton not on vocals
    if element.get('title') == None: print "error no title for",title
    for subtitle in element.get('title').split('/'):
      if subtitle in unlinkablesongs: continue
      if subtitle not in songs: print "bad song reference:",subtitle