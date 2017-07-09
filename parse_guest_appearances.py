#!/usr/local/bin/python2.7

# ----------------------------------------------------------------------------
# Copyright David Bodoh 2013
#
# This script loads an XML catalog of Elton John guest appearances on other
# albums/compilations and renders a series of index pages each containing
# some finite set of records.  Each record contains a picture of the album,
# the title, artist, year and set of songs Elton appears on.
# Dependencies:
#   - guest.xml
#   - songs.xml
# ----------------------------------------------------------------------------
import xml.etree.ElementTree as ET
import os.path
import re
from getimageinfo import getImageInfo
import location
from html_tools import A, TD, TR, TABLE, IMG, BR, SPAN, DIV
from songLib import loadSongs, linkTrack
import templates

## ---------------------------------------------------------------------------
## Generate special guest appearance pages.
## ---------------------------------------------------------------------------
def parse_guest_appearances() :
  records = 0
  picpath = location.docroot+"albums/appearances/pix/"
  guestAlbums = ET.parse(location.dbroot+'guest.xml').getroot()
  index_rows = []
  for album in guestAlbums:
    if album.tag == 'description' :
      guest_description = ET.tostring(album)
      continue

    if album.get('private'): continue
    records += 1
    if album.tag == "single": title = SPAN(dclass="title", content="[single]")
    if album.tag == "album" : title = SPAN(dclass="title", content=album.get('title'))
    artist = SPAN(dclass="gartist", content="(" + album.get('artist') + ")")
    if not artist: print "missing artist for album",album.get('title')
    if not title: print "missing title for album by", artist
    year = "(" + album.get('year')[:4] + ")"
    if not year: year = "(unknown)"

    pic = album.get('pic')
    if not pic :
      picTD = TD(dclass="missing_sleeve", content="[photo not available]")
      print title,"missing guest pic",artist
      pic="NA"
    picfile = picpath+pic
    if os.path.isfile(picfile):
      (type,width,height) = getImageInfo(picfile)
      picTD = TD(dclass="single_sleeve",
          content=IMG(dclass="sleeve", src="pix/"+pic, width=width, height=height))
    else:
      picTD = TD(dclass="missing_sleeve", content="[photo not available]")
      print "ERROR: can't find guest picture:",title, album.get('artist')

    amazon = album.get('amazon')
    if amazon: amazon = templates.getAmazonButton(amazon)
    else: amazon = ""
    trackrows = []
    notes=[]

    for track in album:
      if track.tag == 'issue' : continue
      if track.tag == 'note' :
        notes.append(track.text)
        continue
      length = track.get('length') or "#:##"
      containsTD = TD(dclass="top", content="contains:")
      textTD = TD(dclass="track", content=linkTrack(track))
      trackrows.append(TR(containsTD + textTD))

    tracktable = TABLE("\n".join(trackrows))
    detailsText = " ".join([title,artist])
    detailsText +=  BR() + year + BR() + amazon + BR() + BR().join(notes)
    detailsTD = TD(dclass="guest_text", content=detailsText + BR() + tracktable)
    guest_entry = TABLE(TR(picTD + detailsTD))
    index_rows.append(DIV(dclass="bubble", content=guest_entry))

  # figure out how many index pages we need to create
  max_rows_per_index = 20;
  total_index_pages = len(index_rows)/max_rows_per_index
  if len(index_rows) % max_rows_per_index > 0: total_index_pages += 1

  # chop away at the index_rows list, moving them into the current index page
  guestroot = location.docroot + "albums/appearances/"
  for page in range(total_index_pages) :
    my_rows = index_rows[:max_rows_per_index]    # grab the rows that go into this index page
    del index_rows[:max_rows_per_index]          # clean up as we go
    guest_index_text = templates.getGuestIndex().substitute(
      TITLE  = DIV(dclass="heading padded10", content="Elton John Guest Appearances"),
      DESCR  = DIV(dclass="description", content=guest_description),
      ALBUMS = DIV(dclass="full_width", content="\n\n".join(my_rows)),
      #NAVBAR = DIV(content=DIV(content=" ".join(navDots))),
      NAVBAR = templates.getDotsDiv(page, total_index_pages),
    )
    suffix = str(page+1)
    if page == 0: suffix = ""
    with open(guestroot+"index"+suffix+".html", "w") as guestindex:
      guestindex.write(guest_index_text)
  return records

## ---------------------------------------------------------------------------
## Main program.
## ---------------------------------------------------------------------------
if __name__=="__main__":
  loadSongs()
  r = parse_guest_appearances()
  print "total guest records:",r