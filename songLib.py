import xml.etree.ElementTree as ET
from html_tools import A, B
import re
import location

unlinkablesongs = []    # list of titles that don't get HREF treatment
songs = {}              # title => fileID

# ----------------------------------------------------------------------------
# Load songs from XML into songs{} and unlinkablesongs[]
# ----------------------------------------------------------------------------
def loadSongs() :
  root = ET.parse(location.dbroot+'songs.xml').getroot()
  for song in root:
    if song.tag == "copyright": continue
    if song.tag == "introduction": continue
    if song.tag == "metadata": continue
    title = song.get('title')
    if title == None: raise Exception("error: missing title for song ",song.get('fileID'))
    if title in songs: raise Exception("error: repeat song:",title)
    if song.get('nolink'):
      unlinkablesongs.append(title)
      continue
    songs[title] = song.get('fileID')
    if (song.get('alias')): songs[song.get('alias')] = song.get('fileID')


# ----------------------------------------------------------------------------
# Convert a XML track element to a web-ready passage with links to song(s).
# ----------------------------------------------------------------------------
def linkTrack(track):
  notes=[]
  title = track.get('title')
  if (title == None): raise Exception("missing title in track")
  for attribute in track.keys():
    if attribute   == 'title'   : pass
    elif attribute == 'length'  : pass
    elif attribute == 'index'   : pass
    elif attribute == 'elton'   : notes.append('[Elton: ' + track.get('elton') + ']')
    elif attribute == 'artist'  : notes.append('['+ track.get('artist') + ']')
    elif attribute == 'live'    : notes.append('[live]')
    elif attribute == 'with'    : notes.append('[with ' + track.get('with') + ']')
    elif attribute == 'version' : notes.append('[' + track.get('version') + ']')
    else: print "UNKNOWN attribute",attribute,"in",track.get('title')
  links = []
  title = track.get('title')
  if track.get('artist'): links.append(B(title))
  elif track.get('elton'): links.append(B(title))
  else:
    for subtitle in title.split('/'):
      if subtitle in unlinkablesongs: links.append(B(subtitle)); continue
      if subtitle not in songs: print "bad song reference:\""+subtitle+"\""
      #href = subtitle.lower()
      #href = re.sub(' ','_',href)
      #href = re.sub('\(','',href)
      #href = re.sub('\)','',href)
      #href = re.sub('\'','',href)
      #href = re.sub('#','',href)
      #href = href+'.html'
      href = songs[subtitle] + '.html'
      links.append(A(href="/songs/"+href, content=B(subtitle)))
  linkstring = "/".join(links)
  notestring = " ".join(notes)
  return " ".join([linkstring,notestring])

