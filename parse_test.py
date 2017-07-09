# coding: latin1

import xml.etree.ElementTree as ET

root = ET.parse('test.xml').getroot()
title = root.get('title')
print title
with open("testout.html", "w") as newfile:
  newfile.write('hello')
  decodedtitle = title.encode('latin1')
  newfile.write(decodedtitle)
#title =  decodedtitle.decode('latin1')
title = title.replace("&", "&amp;").encode("latin-1")
print title