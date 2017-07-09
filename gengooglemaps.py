# ############################################################################
# Copyright David Bodoh All Rights Reserved
# Author   : David Bodoh
# Created  : January 2016 (adapted from old perl script)
#
# Generates a webpage that displays a Google Map showing the current/latest
# Elton John tour path.  Also has a form selector to pick from a set of 
# past tours to display their paths on the map.  The map displays one path
# at a time. The map is zoom/panable, and each stop on the tour is onclickable
# to show the details of that date/venue/setlist.
#
# INPUT: latlon.xml - lat/lon positions of venues by city/country
# INPUT: concerts.xml - date/venue/city/country listing of all concerts
#
# OUTPUT: tours.js - javascript array matching location with descriptions
# OUTPUT: nolocation.js - javascript string listing concerts that had no
#           entry in the latlon set.
#
# %venue is a hash whose key is latlon and value is an array of v|c|c
# %venueloc is a hash whose key v|c|c and value is latlon
# both get populated from the latlon.txt database
# %appearances is a hash whose key is latlon and value is an array of date/tour
# ############################################################################

import location
import sys
from datetime import date
from collections import defaultdict
import xml.etree.ElementTree as ET

# ****************************************************************************
# Associates a name with a location so that two venues can be compared for
# proximity (for debugging).
# ****************************************************************************
class Venue:
  def __init__(self, node):
    (self.lat, self.lon) = map(float, venue.get('ll').split(','))
    alias = node.find('name')
    self.name = alias.text
  def closeTo(self,other):
    if abs(self.lat - other.lat) > tolerance: return False
    if abs(self.lon - other.lon) > tolerance: return False
    return True
  def __str__(self):
    return self.name

# ----------------------------------------------------------------------------
# STEP 1: load geocode values.
# ----------------------------------------------------------------------------
venueLocation = {}               # vcc -> ll
venues = defaultdict(list)       # ll -> (vcc,vcc...)
tolerance = 0.005                # degrees
near = {}                        # vcc -> vcc
    
# ----------------------------------------------------------------------------
# STEP 1: load the lat/lon data from XML file.  Meanwhile inspect the data
# for close-but-not-exact venue locations that might actually be the same
# place with different names.
# ----------------------------------------------------------------------------
pastvenues = []
vccs = []
locations = ET.parse(location.dbroot + 'latlon.xml').getroot()
for country in locations:
  for city in country:
    for venue in city:
      thisvenue = Venue(venue)
      for othervenue in pastvenues:
        if thisvenue.closeTo(othervenue):
          print ("%s: %s ~ %s" %(city.get('name'),thisvenue,othervenue))
      for vname in venue:
        vcc = "|".join([vname.text,city.get('name'),country.get('name')])
        vccs.append(vcc)
      pastvenues.append(thisvenue)

# ----------------------------------------------------------------------------
# STEP 2: open the full concerts list and cross-reference with the geocoded
# "vccs" list.  Complain if there's a concert with no latlon.  Store hits in
# the appearances hash.
# ----------------------------------------------------------------------------
totalMissing = 0
sameTourDayGap = 30   # how many days pass before starting a new "tour"
tourID = 0
prevdate = date(1960, 1 1)
appearances = defaultdict(list)  # ll -> (XMLconcert,...)
concerts = ET.parse(location.dbroot+'concerts.xml').getroot()
for concert in concerts:
  if concert.tag != "concert": continue         # skip introduction
  if concert.get('canceled') != None: continue  # skip canceled concerts
  if concert.get('country') != "USA": continue  # only USA tours for now
  # create a key for cross-referencing to latlon
  vcc = "|".join([concert.get('venue'),concert.get('city'),concert.get('country')])
  if vcc not in vccs:
    print ("missing location for '%s' at %s" %(vcc,concert.get('date')))
    totalMissing += 1
    continue
  (year,month,day) = map(int, concert.get('date').split("-"))
  thisdate = date(year,month,day)
  if thisdate - prevdate > sameTourGap:
    tourID += 1
  prevdate = thisdate
  
print ("total missing: %d" %totalMissing)
'''
# ----------------------------------------------------------------------------
# STEP 3
# use the appearances hash to populate locations in a javascript
# file.  Each location includes the venue(s) names at that lat/lon
# as well as all the dates played at that venue(s).
# ----------------------------------------------------------------------------
$googlejs = "tours.js";
$nolocation = "nolocation.js";
open (JS, ">$googlejs") or die "can't open $googlejs";
open (NL, ">$nolocation") or die "can't open $nolocation";
print JS "var geoconcerts = new Array()\;\n";
print NL "var nolocation = \'\n";
$index = 0;
foreach $latlon (keys %appearances) {
  $html = "";
  $title = "";
  $count = 0;
  foreach $datetour (@{$appearances{$latlon}}) {
    $html .= "$datetour<BR>";
    $count ++;
  }
  foreach $vcc (@{$venue{$latlon}}) {
    ($ven,$city,$country) = split (/\|/, $vcc);
    $title .= "$ven<BR>";
    if ($country eq "USA") {
      ($city,$state) = split(/\,/,$city);
      $location = "USA:$state";
      $location =~ s/ //g;
    } else {
      $location = $country;
    }
    if ($latlon eq "0,0") {
      print NL "$ven,$city,$country<BR>\n";
    }
  }
  $app = $count == 1 ? "appearance" : "appearances";
  $title .= "($count $app)";
  if ($latlon ne "0,0") {
    print JS "geoconcerts[$index] = new Array('$location',$latlon,\"$title\",\"$html\",$count)\;\n";
  }
  $index++;
}
print NL "\'\n";
close NL;
close JS;
'''

