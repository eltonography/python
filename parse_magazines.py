import xml.etree.ElementTree as ET
import re
import sys
import location

chart = {}
countries = {}
records = skipped = counted = mine = pending = notmine = partialmine = 0
allmags = ET.parse(location.dbroot + 'magazines.xml').getroot()
for mag in allmags:
  if mag.tag == 'introduction': continue
  records += 1;
  if mag.tag == "fanmagazine": skipped+=1; continue
  if mag.get('nocover') != None: skipped+=1; continue
  own = mag.get('own')
  if (own == None): mine+=1
  elif (own == "no"): notmine+=1
  elif (own == "nope"): 
    pending+=1
    notmine+=1
  else: partialmine+=1
  date = mag.get('date')
  if date == None: print "no date for", mag.get('title')
  if date.startswith("circa "): date = date[6:]  # remove "circa "
  year = re.match("^\d\d\d\d", date)
  if (year == None): sys.stderr.write("ignoring bad date:"+date+"\n")
  else: chart[year.group(0)] = chart.setdefault(year.group(0),0) + 1
  counted+=1
  name = mag.get('title')
  if (name == None): sys.stderr.write("mag missing title\n")
  country = mag.get('country')
  if (country == None): sys.stderr.write("no country for " + name + "\n")
  else:
    country = country.rstrip("\?")
    countries[country] = countries.setdefault(country,0) + 1
  picname = re.sub('[ &!()\']','_',name) + "_" + date + ".jpg"   # remove odd characters
  picname = picname.lower()
  picname = re.sub('__','_',picname)  # squeeze underscores to one

for year in sorted (chart): print year, chart[year]

for country in sorted (countries): print country, countries[country]

print str(records),"records in file"
print str(counted)+" magazines counted"
print str(skipped)+" skipped mags for partial/no cover or fanmag"
print "mine:",mine,"(" + "{0:.0f}".format(100*mine/float(mine+notmine)) + "%)"
print "notmine:",notmine,"(pending:",pending,")"
print "partial:",partialmine