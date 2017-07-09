#!/usr/local/bin/python2.7

# ----------------------------------------------------------------------------
# Copyright David Bodoh 2013
#
# This script loads an XML catalog of Elton John standard albums and generates
# an HTML page for each title.  Titles are categorized by type, and each
# title may have alternate versions. Also generate a single main index page
# that links to the separate categories.  All the thumbnail images for
# the standard albums are rendered via sprites (windows that only show one
# block of a larger album collage image).
# ----------------------------------------------------------------------------

import location
import xml.etree.ElementTree as ET
import os.path
from getimageinfo import getImageInfo
import templates
from songLib import loadSongs, linkTrack
from collections import defaultdict
from html_tools import A, DIV, IMG, STYLE, TD, TR, TABLE, U

alltracks = defaultdict(list)  # id -> list of elements
# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def loadTracks(file) :
  tracksDoc = ET.parse(file).getroot()
  for collection in tracksDoc:
    id = collection.get('id')
    for track in collection:
      alltracks[id].append(track)

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def minilink(album) :
  link = album.get('id') + ".html"
  year = album.find('version').get('year')[:4]
  year = "(" + year + ")"
  return A(href=link, content=IMG(dclass="margin3 sleeve", alt=album.get('title'),
    title=" ".join([album.get('title'),year]), id=album.get('id'), src="/pix/trans.gif", width=1, height=1))

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def parse_standard_albums() :
  totalAlbums = 0
  loadTracks(location.dbroot + "album_tracks.xml")
  albumroot = location.docroot + "albums/standard/"
  picroot = albumroot + "pix/"
  root = ET.parse(location.dbroot+'category_albums.xml').getroot()
  ##decodedroot = ET.tostring(root)
  ##root2 = ET.fromstring(decodedroot)

  ### establish prev/next icons
  for category in root:
    if category.tag == 'description':
      pageDescription = DIV(dclass="description", content=category.text)
      continue
    prevalbum = None
    for album in category:
      album.set('previcon',"")
      album.set('nexticon',"")
      if prevalbum != None:
        prevpic = IMG(src="/pix/left_arrow.gif", border="0", title=prevalbum.get('title'))
        nextpic = IMG(src="/pix/right_arrow.gif", border="0", title=album.get('title'))
        prevalbum.set('nexticon',A(href=album.get('id')+".html",content=nextpic))  # forward link
        album.set('previcon',A(href=prevalbum.get('id')+".html",content=prevpic))  # backward link
      prevalbum = album

  styles = []
  catThumbs = {}
  categories = []
  for category in root:
    if category.tag == 'description': continue
    ### create the CSS style & index matrix for all the sprites in this category
    thumbs = []
    for album in category:
      id = album.get('id')
      XY = '-'+album.get('spriteX')+'px '+'-'+album.get('spriteY')+'px'
      imagecss = "img#"+id+"{ width:50px; height:50px; background:url(sprite.jpg) "+XY+";}"
      styles.append(imagecss)  # each album gets an icon in their category
      thumbs.append(minilink(album))
    categories.append(category.get('name'))
    catThumbs[category.get('name')] = DIV(dclass="thumbnails", content=" ".join(thumbs))

    ### create an HMTL page for each album
    for album in category:
      totalAlbums += 1
      albumnotes = []
      versions = []
      title = album.get('title')
      for element in album:
        if element.tag == 'see': continue
        if element.tag == 'note':
          albumnotes.append(element.text)
          continue

        # otherwise it's a version
        tracks = []
        versionNotes = []
        version = element
        name = version.get('name')
        if name == None: name = ""
        year = '('+version.get('year')[:4]+')'
        amazonID = version.get('amazon')
        if amazonID: amazon = templates.getAmazonButton(amazonID)
        else: amazon = ""

        picname = version.get('pic')
        if not os.path.isfile(picroot+picname): print "error no pic",picname
        (type,width,height) = getImageInfo(picroot + picname)
        image = IMG(dclass="sleeve", src="pix/"+picname, width=width, height=height)
        picTD = TD(dclass="single_sleeve", content=image)

        for element in version:
          if element.tag == 'tracks': tracks = tracks + alltracks[element.get('id')]
          elif element.tag == 'section': tracks = tracks + [element]
          elif element.tag == 'note' : versionNotes.append(element.text)
          else : print "bad tag",element.tag
        trackrows = []
        trackrows.append(TR(TD(dclass="single_details", colspan=2, content=" ".join([name,year]))))
        for note in versionNotes:
          trackrows.append(TR(TD(dclass="note", colspan=2, content=note)))
        trackrows.append(TR(TD(dclass="amazon", colspan=2, content=amazon)))
        for track in tracks:
          if track.tag == 'section':
            trackrows.append(TR(TD(colspan=2, dclass="tracksection", content=track.get('title'))))
            continue
          tracktime = TD(dclass="time", content=track.get('length'))
          tracktext = TD(dclass="track", content=linkTrack(track))
          trackrows.append(TR(tracktime + tracktext))
        tracktable = TABLE("\n".join(trackrows))
        detailsTD = TD(tracktable)
        versiontable = TABLE(dclass="single_issue", content=TR(picTD + detailsTD))
        versions.append(DIV(dclass="bubble", content=versiontable))
      page_template = templates.getStandardAlbumTemplate(title)
      album_text = page_template.substitute(
        NEXTICON        = album.get('nexticon'),
        PREVICON        = album.get('previcon'),
        ALBUM_TITLE     = DIV(dclass="heading",content=U(title)),
        ALBUM_NOTES     = DIV(dclass="subheading",content="<br/>".join(albumnotes)),
        VERSIONS        = "\n".join(versions)
      )
      target = album.get('id')+".html"
      with open(albumroot+target, "w") as albumfile:
        albumfile.write(album_text.encode('UTF-8'))
    # end album
  #end category

  catDivs = []
  for category in categories:
    catDivs.append(DIV(dclass="bubble", content = DIV(dclass="heading",content=category+':') +
        catThumbs[category]))

  albumCSS = STYLE(content="\n".join(styles))
  index_template = templates.getStandardIndexTemplate()
  index_text = index_template.substitute(
    EXTRA_STYLE = albumCSS,
    CONTENT     = pageDescription + "".join(catDivs),
  )
  with open(albumroot+"index.html", "w") as indexfile:
    indexfile.write(index_text.encode('UTF-8'))

  return totalAlbums

## ---------------------------------------------------------------------------
## Main program.
## ---------------------------------------------------------------------------
if __name__=="__main__":
  loadSongs()
  r = parse_standard_albums()
  print "total standard albums:",r