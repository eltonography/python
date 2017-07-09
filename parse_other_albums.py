#!/usr/local/bin/python2.7

# ----------------------------------------------------------------------------
# Copyright David Bodoh 2013
#
# This script loads an XML catalog of Elton John albums released only in
# specific countries, and generates an HTML page for each country, containing
# the set of that country's albums. Countries are ordered as they appear in
# the XML file, albums are ordered as they appear in the file. The single
# index page has a list of links to the countries, plus the number of albums
# expected to be found there.  Some countries will have just a few, others
# will have dozens of albums.
# ----------------------------------------------------------------------------

import location
import xml.etree.ElementTree as ET
import os.path
import re
from getimageinfo import getImageInfo
import templates
from songLib import loadSongs, linkTrack
from collections import defaultdict
from html_tools import A, DIV, IMG, STYLE, TD, TR, TABLE, B, SPAN, U

alltracks = defaultdict(list)  # id -> list of elements
# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def loadTracks(file) :
  tracksDoc = ET.parse(file).getroot()
  for collection in tracksDoc:
    id = collection.get('id')
    for track in collection:
      alltracks[id].append(track)

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def linkto(direction,country):
  target = country.get('id') + '.html'
  return A(href=target, content=IMG(src="/pix/"+direction+"_arrow.gif", border="0", title=country.get('name')))

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def parse_other_albums() :
  totalAlbums = 0
  loadTracks(location.dbroot + "album_tracks.xml")
  albumroot = location.docroot + "albums/international/"
  picroot = albumroot + "pix/"
  root = ET.parse(location.dbroot+'other_albums.xml').getroot()

  # establish next/prev links
  prevcountry = None
  for country in root:
    if country.tag == "description": continue
    if country.get('private'): continue
    country.set('previcon',"")
    country.set('nexticon',"")
    country.set('id',re.sub(' ','_',country.get('name')).lower())
    if prevcountry != None:
      prevcountry.set('nexticon',linkto("right",country))  # forward link
      country.set('previcon',linkto("left",prevcountry))  # backward link
    prevcountry = country

  indexrows = []
  for country in root:
    if country.tag == "description" :
      description = country.text
      continue
    if country.get('private'): continue
    count = 0
    name = country.get('name')
    bubbles = []

    for album in country:
      print album.get('title')
      if album.get('private'): continue
      count += 1
      totalAlbums += 1
      # TBD  id = album.get('id')
      picfile = country.get('id') + '/' + album.get('pic')
      picpath = picroot+picfile
      if not os.path.isfile(picpath): print "error no pic: "+picpath
      (type,width,height) = getImageInfo(picpath)
      image = IMG(dclass="sleeve", src="pix/"+picfile, width=width, height=height)
      picTD = TD(dclass="single_sleeve", content=image)

      discs = album.get('discs')
      if discs: prefix = discs
      else: prefix = ""
      iconfile = "/pix/"+prefix+album.tag+".gif"
      iconpath = location.docroot + iconfile
      (type,width,height) = getImageInfo(iconpath)
      iconTD = TD(IMG(dclass="padded10", src=iconfile, width=width, height=height))
      details = []
      details.append(DIV(dclass="left important", content=U(album.get('title'))))
      details.append(DIV(dclass="left", content="Year: "+B(album.get('year'))))
      details.append(DIV(dclass="left", content="Catalog: "+B(album.get('catalog'))))
      textTD = TD("\n".join(details))
      headerTable = TABLE(TR(iconTD + textTD))

      notes = []
      tracks = []
      for element in album:
        if element.tag == 'tracks': tracks = tracks + alltracks[element.get('id')]
        elif element.tag == 'note' : notes.append(element.text)
        elif element.tag == 'see': notes.append(element.text)
        else : print "bad tag",element.tag
      notesDiv = DIV(dclass="left padded3", content="<br/>".join(notes))
      trackrows = []
      for track in tracks:
        tracktime = TD(dclass="time", content=track.get('length'))
        tracktext = TD(dclass="track", content=linkTrack(track))
        trackrows.append(TR(tracktime + tracktext))
      tracksTable = TABLE("\n".join(trackrows))
      detailsTD = TD(headerTable + notesDiv + tracksTable)
      bubbles.append(DIV(dclass="bubble", content=TABLE(dclass="single_issue", content=TR(picTD + detailsTD))))

    page_template = templates.getInternationalAlbumTemplate(name)
    page_text = page_template.substitute(
      NEXTICON  = country.get('nexticon'),
      PREVICON  = country.get('previcon'),
      COUNTRY   = DIV(dclass="heading", content="select " + name + " pressings"),
      ALBUMS    = "\n".join(bubbles)
    )

    target = country.get('id')+".html"
    with open(albumroot+target, "w") as countryfile:
      countryfile.write(page_text.encode('UTF-8'))

    flagimg = A(href=target, content=IMG(dclass="hardleft20", src="/pix/flags/"+country.get('id')+".gif"))
    namespan = SPAN(dclass="important hardleft200", content=A(href=target, content=name))
    s = ""
    if count > 1 : s = "s"
    countspan = SPAN(dclass="important hardleft400", content=A(href=target, content=str(count)+" pressing"+s))
    indexrows.append(DIV(dclass="left bubble", content=flagimg+namespan+countspan))

  index_template = templates.getInternationalIndexTemplate()
  index_text = index_template.substitute(
    EXTRA_STYLE  = "",
    PAGE_TITLE   = "Elton John International Albums",
    PAGE_CONTENT = DIV(dclass="description", content=description) + "".join(indexrows),
  )

  with open(albumroot+"index.html","w") as indexfile:
    indexfile.write(index_text)

  return totalAlbums

## ---------------------------------------------------------------------------
## Main program.
## ---------------------------------------------------------------------------
if __name__=="__main__":
  loadSongs()
  r = parse_other_albums()
  print "total other albums:",r