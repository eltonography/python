#!/usr/local/bin/python2.7

# ****************************************************************************
# Copyright 2016 David Bodoh
#
# This disposable script converts a single XML file of all cancert data into
# separate XML files with details for each concert.  It still keeps a main
# xml index of all concerts, but without setlist information.
# ****************************************************************************
import location
import xml.etree.ElementTree as XML

# ----------------------------------------------------------------------------
# Convert the tours XML file to a set of separate files.  One main file with
# concert records with date, venue, city, country, tour, source, [canceled], [postponed]
# and a set of separate detail xml files with notes and setlists.
# ----------------------------------------------------------------------------
def convert_tours() :

  xmlfile = XML.parse(location.dbroot+"concerts.xml")
  root = xmlfile.getroot()
  for concert in root:
    if concert.tag == 'introduction':
      introduction = concert.text
      continue
    notes = concert.findall("note")
    notestext = "\n".join(map(lambda x: x.text, notes))
    for note in notes:
      concert.remove(note)
    setlist = concert.findall("song")
    songtext = "\n".join(map(lambda x: x.get('title'), setlist))
    for song in setlist:
      concert.remove(song)
    if len(list(concert)) > 0:   # count the child elements
      print("concert has something", concert.get("date"))
    concert.text = None     # make sure there's no whitespace
    if len(notes) > 0:
      noteElement = XML.Element("notes")
      noteElement.text = notestext
      concert.append(noteElement)
    if len(setlist) > 0:
      songsElement = XML.Element("songs")
      songsElement.text = songtext
      concert.append(songsElement)
  xmlfile.write("newconcerts.xml", encoding="UTF-8", xml_declaration=True)
  
## ---------------------------------------------------------------------------
## Main program.
## ---------------------------------------------------------------------------
if __name__=="__main__":
  convert_tours()