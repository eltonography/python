#!/usr/local/bin/python2.7

import xml.etree.ElementTree as ET
import location
import re
from collections import defaultdict
from constants import monthAbbreviation
from html_tools import TR, TD, B, DIV, TABLE, IMG, U, SELECT, A
import templates
from getimageinfo import getImageInfo
from os import listdir
from os.path import isfile, join
allPicFiles = []
allYears = []
magcount = defaultdict(int)

# ----------------------------------------------------------------------------
# Grab all the files in the pix folder; store in allPicFiles list.
# ----------------------------------------------------------------------------
def find_all_pix() :
  magpath = location.docroot + "magazines/pix/"
  global allPicFiles
  allPicFiles = [ f for f in listdir(magpath) if isfile(join(magpath,f)) ]

# ----------------------------------------------------------------------------
# Record the YYYY and add it to the allYears list.
# ----------------------------------------------------------------------------
def addYear(issuedate) :
  global allYears
  global magcount
  issuedate = re.sub('circa ','',issuedate)
  ymd = issuedate.split('-')
  if len(ymd) == 1:
    if ymd[0] not in allYears: allYears.append(ymd[0])
    magcount[ymd[0]] += 1
    return ymd[0]
  if len(ymd) == 2: 
    if ymd[0] not in allYears: allYears.append(ymd[0])
    magcount[ymd[0]] += 1
    return ymd[0]
  if len(ymd) == 3:
    if ymd[0] not in allYears: allYears.append(ymd[0])
    magcount[ymd[0]] += 1
    return ymd[0]
  print "UNKNOWN ISSUE YEAR", issuedate
  return issuedate

# ----------------------------------------------------------------------------
# create the html selection widget for all possible year values. with the 
# given year as already selected.
# ----------------------------------------------------------------------------
def yearSelector(selectedYear) :
  allOptions = []
  prevlink = ""
  nextlink = ""
  for y in allYears:
    selected = ""
    if y == selectedYear:
      selected = "selected"
      prevyear = int(selectedYear)-1
      if str(prevyear) in allYears:
        linkfile = "index.html" if str(prevyear) == allYears[0] else "index"+str(prevyear)+".html"
        prevlink = A(href=linkfile,content=str(prevyear)+"<<<")
      nextyear = int(selectedYear)+1
      if str(nextyear) in allYears:
        nextlink = A(href="index"+str(nextyear)+".html",content=">>>"+str(nextyear))
    allOptions.append("<option value='"+y+"'" + selected + ">"+y+" ("+str(magcount[y])+" magazines)</option>")
  left = TD(prevlink)
  middle = TD(content=SELECT(dclass="PX20", size=1, onChange="showYear(this,"+allYears[0]+")", content="\n".join(allOptions)))
  right = TD(nextlink)
  row = TR(content=left+middle+right)
  return TABLE(content=row, dclass="EVEN", width="100%")

  
def is_number(s) :
  try:
    int(s)
    return True
  except ValueError:
    return False
  
# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def generate_magazines() :
  totalMags = 0
  magspath = location.docroot + "magazines/"
  picpath = magspath + "pix/"
  bubbles = defaultdict(list)
  root = ET.parse(location.dbroot + 'magazines.xml').getroot()
  for mag in root:
    if mag.tag == "introduction":
      #introduction = mag.text
      introduction = ET.tostring(mag)
      continue
    if mag.get('private'): continue       # skip stuff not ready for publication
    if mag.get('own') == "no": continue   # skip stuff that I don't actually have
    if mag.get('nocover'): continue       # skip stuff if elton not on the cover page
    if mag.tag == "fanmagazine": continue # fan magazines will be done some other way
    pic = mag.get('pic')
    if pic == None: continue              # TBD: we should complain about missing pic
    totalMags += 1
    rows = []
    picfile = picpath + pic
    try:
      (type,width,height) = getImageInfo(picfile)
      allPicFiles.remove(pic)
      imageTD = TD(dclass="single_sleeve", content=IMG(dclass="sleeve", src="pix/"+pic, width=width, height=height))
      if width != 200: print "bad width for", pic
    except:
      try :
        print "cannot find picture for",mag.get('title'),mag.get('date'),":",pic
      except:
        print "cannot find picture for",mag.get('date')
    titletext = mag.get('title')
    rows.append(DIV(dclass="important left", content=U(B(titletext))))
    issuetext = mag.get('date')
    year = addYear(issuetext)
    date = issuetext.split('-');
    if len(date) > 1:
      if date[1] in monthAbbreviation:
        date[1] = monthAbbreviation[date[1]]
    if len(date) == 2:
      issuetext = date[1] + " " + date[0]
    if len(date) == 3:
      issuetext = date[1] + " " + date[2] + ", " + date[0]
    if (mag.get('issue') != None) :
      if is_number(mag.get('issue')) :
        issuetext = issuetext + ' (#' + mag.get('issue') + ')'
      else:
        issuetext = issuetext + ' ('+mag.get('issue')+')'
    rows.append(DIV(dclass="left", content="Issue Date: " + B(issuetext)))
    rows.append(DIV(dclass="left", content="Country: " + B(mag.get('country'))))

    color = "blue"
    #if mag.get('own') != None : color = "yellow"
      
    textTD = TD(dclass="top", content="".join(rows))
    bubbles[year].append(DIV(dclass="bubble "+color, content=TABLE(TR(imageTD + textTD))))

  # this javascript gets added to each mags html file
  # it is the response to load a new page when a selection is made
  yearScript = '''
<script type="text/javascript">
  function showYear(selector,firstyear) {
    year = selector.options[selector.selectedIndex].value
    if (year == firstyear) year = ""
    newurl = "index" + year + ".html";
    document.location=newurl;
  }
</script>
'''

  # divide all the magazines into sepatate index files sorted by year
  magroot = location.docroot + "magazines/"
  prevlink = None;
  for y in allYears :
    mag_index_text = templates.getMagazineIndex().substitute(
      EXTRA_HEADER = yearScript,
      DESCR  = DIV(dclass="description", content=introduction),
      BOOKS  = DIV(dclass="full_width", content="\n\n".join(bubbles[y])),
      NAVBAR = yearSelector(y),
    )
    suffix = str(y)
    if y == allYears[0]: suffix = ""
    with open(magroot+"index"+suffix+".html", "w") as magindex:
      magindex.write(mag_index_text.encode('UTF-8'))
  return totalMags


## ---------------------------------------------------------------------------
## Main program.
## ---------------------------------------------------------------------------
if __name__=="__main__":
  find_all_pix()                   # pre-load the available set of pix files
  b = generate_magazines()         # make HTML files
  print "total magazines:", b      # show summary
  for pic in allPicFiles:          # any pix left were not linked from the data
    print "unused pic file:", pic  # so we can investigate why
