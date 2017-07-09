#!/usr/local/bin/python2.7

from songLib import loadSongs
from parse_standard_albums import parse_standard_albums
from parse_other_albums import parse_other_albums
from parse_guest_appearances import parse_guest_appearances
from parse_import_cds import parse_import_cds
from generate_sessions import generate_session_albums

## ---------------------------------------------------------------------------
## generate all sub-sections of the Albums page.
## ---------------------------------------------------------------------------
def generate_albums() :
  print "standard albums",parse_standard_albums()
  print "other albums", parse_other_albums()
  print "guest appearances", parse_guest_appearances()
  print "import CDs", parse_import_cds(20)
  print "session albums", generate_session_albums()

## ---------------------------------------------------------------------------
## Main program.
## ---------------------------------------------------------------------------
if __name__=="__main__":
  loadSongs()
  generate_albums()

