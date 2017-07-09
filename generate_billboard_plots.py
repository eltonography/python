#!/usr/local/bin/python2.7

# ----------------------------------------------------------------------------
# Copyright David Bodoh 2013
#
# This script loads an XML file of billboard chart information for songs
# and albums, and generates PNG plot files.
# ----------------------------------------------------------------------------
import xml.etree.ElementTree as XML
import location
import templates
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def generate_billboard_plots():
  chart = XML.parse(location.dbroot+'billboard_hot_100.xml').getroot()
  for single in chart:
    labels = []
    positions = []
    for week in single:
      positions.append(week.get('position'))
      labels.append(week.get('date'))
    x = range(1,len(positions)+1)
    plt.plot(x, positions, 'ro')               # create a plot with red dots
    x1,x2,y1,y2 = plt.axis()                   # get the preferred axes range
    plt.axis((x1-1,x2+1,100,0))                # reverse the Y-axis to show better positions higher
    plt.xticks(x, labels, rotation='vertical') # set the X labels to be rotated dates
    plt.margins(0.2)                           # Pad margins so that markers don't get clipped by the axes
    plt.subplots_adjust(bottom=0.25)           # Tweak spacing to prevent clipping of tick-labels
    plt.show()

## ---------------------------------------------------------------------------
## Main program.
## ---------------------------------------------------------------------------
if __name__=="__main__":
  generate_billboard_plots()
