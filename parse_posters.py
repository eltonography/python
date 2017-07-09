import xml.etree.ElementTree as ET
import location

postercount = 0
totalarea = 0
root = ET.parse(location.dbroot + 'posters.xml').getroot()
for category in root:
  for poster in category:
    if poster.get('own') == "no": continue
    totalarea += float(poster.get('w')) * float(poster.get('h'))
    postercount+=1

print "total posters:", postercount
print "total square feet: %0.2f" % (totalarea/144)
