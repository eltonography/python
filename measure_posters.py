import xml.etree.ElementTree as ET
import location

postercount = 0
totalarea = 0
root = ET.parse(location.dbroot + 'posters.xml').getroot()
nofitA = nofitB = nofitC = 0
fitA = fitB = fitC = 0
for category in root:
  for poster in category:
    if poster.get('own') == "no": continue
    totalarea += float(poster.get('w')) * float(poster.get('h'))
    w = float(poster.get('w'))
    h = float(poster.get('h'))
    width = max(w,h)
    depth = min(w,h)
    if width > 44 or depth > 34: nofitA += 1
    else: fitA += 1
    if width > 45 or depth > 34: nofitB += 1
    else: fitB += 1
    if width > 52 or depth > 40: nofitC += 1
    else: fitC += 1


print "nofitA:",nofitA, fitA
print "nofitB:",nofitB, fitB
print "nofitC:",nofitC, fitC
