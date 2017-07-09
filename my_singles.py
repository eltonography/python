#
# usage: python my_singles.py mine "South Africa"
#

import xml.etree.ElementTree as ET
import re
import sys
import os.path
import location
from collections import defaultdict

filter = sys.argv[1]  # mine | notmine | pete | all
target = sys.argv[2]  # country | all
format = sys.argv[3]  # 7 | 12 | CD | CS | FLEXI | all
summary = defaultdict(int)

root = ET.parse(location.dbroot+'/singles.xml').getroot()
mine = []
notmine = []
pete = []
for single in root:
  #if single.tag == 'single' : title = single.get('title')
  #if single.tag == 'miscellaneous': title = single.get('country')+" misc"
  for issue in single:
    if single.tag == 'miscellaneous':
      track = issue.find("track")
      title = track.get('title')
    else:
      title = single.get('title')
    country = issue.get('country')
    country = country.replace(" ","")  # in cases like "South Africa"
    if target != "all" and country != target: continue
    if (filter == 'mine') and (issue.get('own') != 'yes'): continue
    if (filter == 'notmine') and (issue.get('own') == 'yes'): continue
    if (filter == 'pete') and ( not issue.get('own').startswith('nope')): continue
    if (format != "all" and issue.get('format') != format): continue
    summary[format] += 1
    catalog = issue.get('catalog')
    tracks = 0
    own = " "
    if issue.get('own') == "yes": own = "X"
    if issue.get('own').startswith("nope"): own = "P"
    promo = ""
    if issue.get('promo'): promo = "(promo)"
    ps = ""
    if issue.get('ps'): ps = "(PS)"
    for track in issue : 
      if track.tag == 'track' : tracks += 1
    tracks = '('+str(tracks)+')'
    print " ".join([own, country, catalog, title, tracks, promo, ps])
for fmt in summary:
  print fmt,":",summary[fmt]