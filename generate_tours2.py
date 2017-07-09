#!/usr/local/bin/python2.7

import location
import xml.etree.ElementTree as XML


# ----------------------------------------------------------------------------
# Converts the concerts.txt file to an XML file, including songs from
# each of the dated sub-folder files.
# ----------------------------------------------------------------------------
def generate_tours() :

  root = XML.parse(location.dbroot+"concerts.xml").getroot()
  for concert in root:
    if concert.tag == 'introduction': continue
    if concert.get('canceled'): continue
    if concert.get('postponed'): continue
    if concert.get('private'): continue
    ymd = concert.get('date')
    if ymd != '2014-07-20': continue # TEMPORARY
    #if concert.get('pic') != "inaki_berrio.jpg": continue
    #print concert.get('author')
    print concert.get('city')

## ---------------------------------------------------------------------------
## Main program.
## ---------------------------------------------------------------------------
if __name__=="__main__":
  r = generate_tours()
