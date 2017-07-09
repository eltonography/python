#!/usr/local/bin/python2.7

import location
from html_tools import TR, TD, B, DIV, INPUT, FORM, TABLE, IMG, U, OPTION, SELECT
import templates
from collections import defaultdict
import constants
import xml.etree.ElementTree as XML

toursroot = location.docroot + "tours/"

# ----------------------------------------------------------------------------
# Convert an XML concert node
# ----------------------------------------------------------------------------
def getDetails(concert) :
  lines = []
  note = ""
  if concert.find('songs') != None: lines.append(B("Setlist from " + dmy(concert.get('date'))+":"))
  for elem in concert:
    if elem.tag == 'songs' :
      songs = elem.text.split("\n")
      for song in songs:
        lines.append(song)  # TBD: eventually link to lyrics
    if elem.tag == 'notes' :
      notes = elem.text.split("\n")
      for note in notes:
        lines.append(note)          # TBD: make sure notes really are separate sentences.
  return "<br/>".join(lines)

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def getLocation(city, country) :
  if country != "USA" : return country
  (city, state) = city.split(',')
  state = state.strip()
  return ":".join([country,constants.stateName[state]])

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def dmy(ymd) :
  (year, month, day) = ymd.split('-')
  return " ".join([day,constants.monthAbbreviation[month],year])

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def linkto(value) :
  value = value.lower()
  value = value.translate(None, ' :')
  return value + ".html"

# ----------------------------------------------------------------------------
# Converts the concerts.txt file to an XML file, including songs from
# each of the dated sub-folder files.
# ----------------------------------------------------------------------------
def generate_tours() :

  hiddenrowID = 0
  yearlist = defaultdict(list)
  locationlist = defaultdict(list)
  root = XML.parse(location.dbroot+"newconcerts.xml").getroot()
  for concert in root:
    if concert.tag == 'introduction':
      introduction = concert.text
      continue
    if concert.get('canceled'): continue
    if concert.get('postponed'): continue
    if concert.get('private'): continue
    ymd = concert.get('date')
    (year,month,day) = ymd.split('-')
    venue = concert.get('venue')
    city = concert.get('city')
    country = concert.get('country')
    tour = concert.get('tour')
    toggler = ""
    if len(list(concert)) == 0:  # if concert has any child elements
      row1 = (TR(TD(dmy(ymd))+TD(venue)+TD(city+", "+country)+TD(tour)+TD("")))
      row2 = ""
    else:
      hiddenrowID += 1
      elemID = "elem"+str(hiddenrowID)
      row1 = TR(TD(dmy(ymd))+TD(venue)+TD(city+", "+country)+TD(tour)+TD(onClick="toggle(\'"+elemID+"\')",style="cursor: pointer;",content=U("details")))
      row2 = TR(TD(dclass="left indent", style="display:none;", id=elemID, colspan=5,content=getDetails(concert)))
    yearlist[year].append(row1+row2)
    locationlist[getLocation(city,country)].append(row1+row2)

  year_opts = []
  year_opts.append(OPTION(value="index.html", content="Show Elton John Concerts By Year..."))
  for year in sorted(yearlist):
    year_opts.append(OPTION(value=str(year)+".html",content=str(year)+" ("+str(len(yearlist[year]))+") concerts"))
  yearSelector = SELECT(dclass="margin20 bold", size=1, onChange="showConcerts(this)", content="\n".join(year_opts))

  loc_opts = []
  loc_opts.append(OPTION(value="index.html", content="Show Elton John Concerts By Location..."))
  for loc in sorted(locationlist):
    loc_opts.append(OPTION(value=linkto(loc), content=loc+" ("+str(len(locationlist[loc]))+") concerts"))
  locSelector = SELECT(dclass="margin20 bold", size=1, onChange="showConcerts(this)", content="\n".join(loc_opts))

  headerRow = TR(dclass="bold underline large", content=TD("Date")+TD("Venue")+TD("City")+TD("Tour")+TD(""))  
  for year in sorted(yearlist):
    print year
    title = DIV(dclass="bold important padded10", content="Elton John " + year + " Concerts:")
    listing = TABLE(dclass="small center full_width", content=headerRow + "".join(yearlist[year]))
    tourtext = templates.getTourIndex().substitute(
      PAGE_CONTENT = yearSelector + locSelector + title + listing,
    )
    with open(toursroot + year + ".html","w") as yearfile:
      yearfile.write(tourtext.encode('UTF-8'))

  for loc in sorted(locationlist):
    title = DIV(dclass="bold important padded10", content="Elton John " + loc + " Concerts:")
    listing = TABLE(dclass="small center full_width", content=headerRow + "".join(locationlist[loc]))
    tourtext = templates.getTourIndex().substitute(
      PAGE_CONTENT = yearSelector + locSelector + title + listing,
    )
    with open(toursroot + linkto(loc),"w") as locfile:
      locfile.write(tourtext.encode('UTF-8'))

  indextext = templates.getTourIndex().substitute(
    PAGE_CONTENT = DIV(dclass="bubble description", content=introduction + "<br/>" + yearSelector + locSelector),
  )
  with open(toursroot + "index.html",'w') as indexfile:
    indexfile.write(indextext)

  return len(root)

## ---------------------------------------------------------------------------
## Main program.
## ---------------------------------------------------------------------------
if __name__=="__main__":
  r = generate_tours()
  print "total concerts:",r