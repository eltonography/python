#!/usr/local/bin/python2.7

# ----------------------------------------------------------------------------
# Copyright David Bodoh 2013
#
# This script loads an XML catalog of Elton John session recordings.
# ----------------------------------------------------------------------------

from constants import monthAbbreviation
import location
import xml.etree.ElementTree as XML
import os.path
from getimageinfo import getImageInfo
import templates
from songLib import loadSongs, linkTrack
from collections import defaultdict
from html_tools import DIV, IMG, TD, TR, TABLE, BR, B, U, LI, OL

alltracks = defaultdict(list)  # id -> list of elements
# ----------------------------------------------------------------------------
# pre-load the referenced track listing for track collections.
# ----------------------------------------------------------------------------
def loadTracks(file) :
  tracksDoc = XML.parse(file).getroot()
  for collection in tracksDoc:
    id = collection.get('id')
    for track in collection:
      alltracks[id].append(track)

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def generate_session_albums() :
  totalAlbums = 0
  loadTracks(location.dbroot + "album_tracks.xml")
  sessionroot = location.docroot + "albums/sessions/"
  picroot = sessionroot + "pix/"
  root = XML.parse(location.dbroot+'sessionwork.xml').getroot()
  totalrecords = 0

  description = root.find('description')
  #description = description.text
  description = XML.tostring(description)
  index_rows = []
  songrows = []

  songrows.append(TR(TD(B(U("released")))+TD(B(U("title")))+TD(B(U("original artist")))))
  for song in root.findall('listing/song'):
    year = song.get('date')[:4]
    month = song.get('date')[5:7]
    month = monthAbbreviation[month]
    eltonvocals = song.get('elton', default="lead vocals")
    eltonvocals=" ["+eltonvocals+"]"
    songrow = TR(TD(month+" "+year) + TD(B(U(song.get('title')))+eltonvocals) + TD(song.get('artist')))
    songrows.append(songrow)
  songtable = DIV(dclass="bubble", content=TABLE(content="\n".join(songrows), dclass="left small"))
  description += songtable

  for category in root.findall('category'):
    if category.get('private'): continue
    format = category.get('format')
    categoryname = category.get('format')

    for issue in category :
      if issue.get('private') : continue
      #if issue.get('pic') == None: continue
      totalrecords += 1
      title = issue.get('title')
      if title == None: title = ""
      if format == "7": title="7-inch single"
      if format == "CD5": title="CD single"
      catalog = issue.get('catalog')
      if catalog == None: 
        print "no catalog for",title
        continue

      pic = issue.get('pic')
      if pic == None:
        picTD = TD(dclass="missing_sleeve", content="[no sleeve]")
      else:
        picfile = picroot+pic
        if os.path.isfile(picfile):
          (type,width,height) = getImageInfo(picfile)
          picTD = TD(dclass="single_sleeve",
              content=IMG(dclass="sleeve", src="pix/"+pic, width=width, height=height))
        else:
          picTD = TD(dclass="missing_sleeve", content="[photo not available]")
          print "ERROR: can't find session picture:",title, catalog

      year = issue.get('year', default="")
      if len(year): year = " (" + year[:4] + ")"
      trackrows = []
      for track in issue.findall('track'):
        if track.get('artist') == "anonymous":
          trackrows.append(LI(dclass="anonymous", content=track.get('title')))
        else :
          trackrows.append(LI(dclass="track", content=linkTrack(track)))

      reftracks = []
      for element in issue:
        if element.tag == 'tracks': reftracks = reftracks + alltracks[element.get('id')]
      for track in reftracks:
        trackrows.append(LI(dclass="track", content=linkTrack(track)))

      prefix = issue.get('discs',"")
      iconfile = "/pix/"+prefix+format+".gif"
      (type,width,height) = getImageInfo(location.docroot + iconfile)
      icon = IMG(dclass="padded10", src=iconfile, width=width, height=height)

      notes=""
      for note in issue.findall('note'):
        notes +=BR()+note.text

      tracktable = OL("\n".join(trackrows))
      title=DIV(dclass="large bold", content=title)
      detailsText = icon + title + catalog + year + notes
      detailsTD = TD(dclass="guest_text", content=detailsText + BR() + tracktable)
      session_issue = TABLE(TR(picTD + detailsTD))
      index_rows.append(DIV(dclass="bubble", content=session_issue))

    session_index_text = templates.getSessionIndex().substitute(
      TITLE  = DIV(dclass="heading padded10", content="Elton John as a Session Musician"),
      DESCR  = DIV(dclass="description", content=description),
      ALBUMS = DIV(dclass="full_width", content="\n\n".join(index_rows)),
    )
    with open(sessionroot+"index.html", "w") as sessionindex:
      sessionindex.write(session_index_text.encode('latin-1'))

  return totalrecords

## ---------------------------------------------------------------------------
## Main program.
## ---------------------------------------------------------------------------
if __name__=="__main__":
  loadSongs()
  r = generate_session_albums()
  print "total session albums:",r