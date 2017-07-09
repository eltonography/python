# ############################################################################
# Copyright David Bodoh All Rights Reserved
# Author   : David Bodoh
# Created  : February 2016
#
# Start with a concerts.xml data file that has "all" the tour data including
# dates, venues, notes and setlists, and divide into separate XML output
# files.  One file for all the "minimum" data (date,venue,city,country,tour,source)
# and then a separate XML file for each concert that has notes and/or setlist data.
# This is disposable - only need to work once - just before we go public with
# the changes permanently.
# ############################################################################

import location
import sys
from datetime import date
from collections import defaultdict
import xml.etree.ElementTree as ET
outputfolder = location.dbroot+'/tours/';

cdata = ET.ElementTree(file=location.dbroot+'concerts.xml')
concerts = cdata.getroot()
prevdate = "1960-01-01"
for concert in concerts:
  if concert.tag != 'concert': continue
  if concert.get('source') == "None": concert.attrib.pop('source')
  thisdate = concert.get('date')
  if thisdate < prevdate: print ("bad date order",prevdate,thisdate)
  prevdate = thisdate
  notes = concert.findall('note')
  songs = concert.findall('song')
  if len(notes) > 0 or len(songs) > 0 :
    for note in notes: concert.remove(note)
    for song in songs:
      concert.remove(song)
      if song.get('index') != None: song.attrib.pop('index')
    newroot = ET.Element('concert')
    newroot.set('date',concert.get('date'))
    newroot.extend(notes)
    newroot.extend(songs)
    newdata = ET.ElementTree(newroot)
    newdata.write(outputfolder+concert.get('date')+'.xml')
cdata.write(location.dbroot+'_UPDATED_CONCERTS.xml')
