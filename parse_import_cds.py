#!/usr/local/bin/python2.7

# ----------------------------------------------------------------------------
# Copyright David Bodoh 2013
#
# This script loads an XML catalog of Elton John unauthorized CDs, and 
# distributes them across a handful of pages, ordered alphabetically. Each
# page contains N number of records.
# Dependencies:
#   - import_cds.xml
#   - songs.xml
# ----------------------------------------------------------------------------
import xml.etree.ElementTree as ET
import os.path
import re
import time
from getimageinfo import getImageInfo
import location
from html_tools import A, B, TD, TR, TABLE, IMG, BR, SPAN, DIV, OL, LI, U
from songLib import loadSongs, linkTrack
import templates

def textDate(ymd) :
  if len(ymd)==10: return time.strftime("%d %B %Y", time.strptime(ymd, "%Y-%m-%d"))
  if len(ymd)==7: return time.strftime("%B %Y", time.strptime(ymd, "%Y-%m"))
  return ymd[:4]

## ---------------------------------------------------------------------------
## Generate unauthorized CDs pages.
## ---------------------------------------------------------------------------
def parse_import_cds(per_page) :
  count = 0
  imports = ET.parse(location.dbroot + 'import_cds.xml').getroot()
  importpath = location.docroot+"albums/unauthorized/"
  picpath = importpath+"pix/"
  introduction = ""
  bubbles = []

  for cd in imports:
    if cd.tag == 'introduction':
      introduction = cd.text
      continue
    if cd.get('private'): continue

    count += 1
    # establish the left TD with a cover scan
    pic = cd.get('pic')
    if not pic: raise Exception("missing import pic for " + title)
    picfile = picpath+pic
    (type,width,height) = getImageInfo(picfile)
    img = IMG(dclass="sleeve", src="pix/"+pic, width=width, height=height, alt="scan of sleeve", title="scan of sleeve")
    picTD = TD(dclass="single_sleeve", content=img)

    # establish the right TD with all the text (as separate table rows)
    textRows = []
    textRows.append(TR(TD(dclass="left important", content=U(cd.get('title')))))
    textRows.append(TR(TD(dclass="left", content='label/catalog: ' + B(cd.get('catalog')))))
    if cd.get('year'): textRows.append(TR(TD(dclass="left", content='issued: ' + B(cd.get('year')))))
    if cd.get('venue'): textRows.append(TR(TD(dclass="left", content='venue: ' + B(cd.get('venue')))))
    if cd.get('date'): textRows.append(TR(TD(dclass="left", content='recorded live: ' + B(textDate(cd.get('date'))))))
    if cd.get('country'): textRows.append(TR(TD(dclass="left", content='country: ' + B(cd.get('country')))))
    tracks = []
    for element in cd:
      if element.tag == 'track': tracks.append(LI(dclass="left", content=linkTrack(element)))
      elif element.tag == 'note':
        textRows.append(TR(TD(dclass="left", content=element.text)))
    textRows.append (TR(TD(OL("\n".join(tracks)))))
    textTD = TD(TABLE("\n".join(textRows)))

    bubbles.append(DIV(dclass="bubble", content=TABLE(TR(picTD+textTD))))

  # figure out how many index pages we need to create
  total_index_pages = len(bubbles)/per_page               # first pages are maxed out
  if len(bubbles) % per_page > 0: total_index_pages += 1  # last page is partial set

  # chop away at the index_rows list, moving them into the current index page
  for ipage in range(total_index_pages) :
    my_rows = bubbles[:per_page]    # grab the rows that go into this index page
    del bubbles[:per_page]          # clean up as we go
    index_text = templates.getImportIndex().substitute(
      TITLE  = DIV(dclass="heading padded10", content="Elton John Unauthorized CDs"),
      DESCR  = DIV(dclass="description", content=introduction),
      ALBUMS = DIV(dclass="full_width", content="\n\n".join(my_rows)),
      NAVBAR = templates.getDotsDiv(ipage, total_index_pages),
    )
    suffix = str(ipage+1)
    if ipage == 0: suffix = ""
    with open(importpath+"index"+suffix+".html", "w") as indexfile:
      indexfile.write(index_text.encode('latin-1'))

  return count

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
if __name__=="__main__":
  loadSongs()
  r = parse_import_cds(20)
  print "total import CDs:",r
