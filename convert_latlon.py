# convert latlon.txt to latlon.xml
# <locations>
#   <country name="USA">
#     <city name="Los Angeles, CA">
#       <venue ll="34.323,-132.2342">
#         <name>vname1</name>
#         <name>vname2</name>
#       </venue>
#     </city>
#   </country>
# </locations>

import sys
import xml.etree.ElementTree as ET
import location

root = ET.Element('locations')

with open(location.dbroot+'latlon.txt') as LATLON:
  for line in LATLON:
    line = line.strip()
    if line.startswith('#'): continue
    if len(line.strip()) == 0: continue
    (venue,city,country,latlon) = line.split("|")
    note = None
    if " " in latlon:
      (latlon,note) = latlon.split(' ',1)
    countryTarget = "./country[@name='%s']" % country
    countryElement = root.find(countryTarget)
    if countryElement == None:
      countryElement = ET.SubElement(root,'country')
      countryElement.set('name',country)
      countryElement.text = '\n'
    cityTarget = "./city[@name='%s']" % city
    cityElement = countryElement.find(cityTarget)
    if cityElement == None:
      cityElement = ET.SubElement(countryElement,'city')
      cityElement.set('name',city)
      cityElement.text = '\n  '
      cityElement.tail = '\n'
    venueTarget = "./venue[@ll='%s']" % latlon
    venueElement = cityElement.find(venueTarget)
    if venueElement == None:
      venueElement = ET.SubElement(cityElement,'venue')
      venueElement.set('ll',latlon)
      venueElement.text = '\n    '
      venueElement.tail = '\n  '
    alias = ET.SubElement(venueElement,'name')
    alias.text = venue
    alias.tail = '\n  '
    if note != None:
      alias.set('note',note)
doc = ET.ElementTree(root)
doc.write("latlon.xml")
