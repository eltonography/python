#!/usr/local/bin/python2.7

import location
import string
from collections import defaultdict
import xml.etree.ElementTree as ET
from string import Template
from html_tools import DIV, B, TABLE, TR, TD, A, META
import re
from templates import getLyricPageTemplate, getLyricsIndexTemplate, getAmazonWidget, getItunesLink

# ----------------------------------------------------------------------------
# Load the XML file with songs and write each song as its own HTML file.
# Also generate 26 index pages for each alphabet letter for manageable
# browsing.  Also generate a single intro index page.
# ----------------------------------------------------------------------------
def generate_songs() :
  root = ET.parse(location.dbroot+"songs.xml").getroot()

  # STEP 1: set the alphabetizable id for each song
  alphaIndex = defaultdict(list)     # letter -> list of alphatitles starting with letter
  alphaElements = {}                 # alpha-ranked_title -> XML_song
  for song in root:
    if song.tag == 'introduction' :
      introduction = ET.tostring(song)
      continue
    if song.tag == 'copyright':
      warning = ET.tostring(song)
      continue
    if song.tag == 'metadata' :
      metadata = song.text
      continue
    if song.get('nolink'): continue
    alphatitle = song.get('title')
    alphatitle = re.sub('\)','',alphatitle)
    alphatitle = re.sub('\(','',alphatitle)
    alphatitle = re.sub('^A ','',alphatitle)
    alphatitle = re.sub('^The ','',alphatitle)
    if alphatitle[0].isdigit(): alphatitle = "0" + alphatitle
    alphaIndex[alphatitle[0]].append(alphatitle)
    alphaElements[alphatitle] = song

  # STEP 2: set the alphabetized prev/next IDs for each song
  prevsong = None
  for aid in sorted(alphaElements) :
    if prevsong != None:
      prevsong.set('nextid',alphaElements[aid].get('fileID'))
      alphaElements[aid].set('previd',prevsong.get('fileID'))
    prevsong = alphaElements[aid]

  # STEP 3: run each song through template and write to file
  totalsongs = 0
  searchable = []
  for song in root.findall('song'):
    if song.get('nolink'): continue
    totalsongs += 1
    title = song.get('title')
    asin = song.get('amazon')
    if asin: amazonWidget = getAmazonWidget(asin, title)
    else:    amazonWidget=""
    #itunesCode = song.get('itunes')
    #if itunesCode: itunesButton = getItunesLink(itunesCode)
    #else: itunesButton=""
    itunesButton = ""   # TBD: need new affiliate links

    copyright = ""
    lyrics = []
    notes = []
    creditrows = []
    searchtext = ""
    for element in song:
      if element.tag == 'copyright': copyright = " ".join(["&copy;",element.get('year'),element.get('owner')])
      if element.tag == 'credit'   :
        creditType = re.sub(' ','&nbsp;',element.get('type'))
        creditrows.append(TR(TD(dclass="credit_type", content=creditType+":")+TD(dclass="credit_name", content=B(element.text))))
      if element.tag == 'note':
        notes.append(element.text)
      if element.tag == 'lyrics':
        for verse in element:
          if verse.text : searchtext += re.sub('\n',' ',verse.text)
          if verse.tag == 'verse'  :
            versecontent = re.sub('\n','<br/>\n', verse.text[1:])
            lyrics.append(DIV(dclass="verse", content=versecontent))
          if verse.tag == 'chorus' :
            versecontent = re.sub('\n','<br/>\n', verse.text[1:])
            lyrics.append(DIV(dclass="chorustag", content="chorus:")+DIV(dclass="chorus", content=versecontent))
          if verse.tag == 'repeat' :
            if verse.get('chorus') : lyrics.append(DIV(dclass="chorusrepeat", content="(repeat chorus "+verse.get('chorus')+')'))
            else                   : lyrics.append(DIV(dclass="chorusrepeat", content="(repeat chorus)"))

    if len(searchtext): searchable.append('|'.join([song.get('fileID'),song.get('title'),song.get('title').lower() + ' ' + searchtext.lower()]))
    credittable = TABLE(dclass="credits", content="\n".join(creditrows))
    if lyrics : alllyrics = "".join(lyrics)
    else: alllyrics = "(instrumental)"
    allnotes = "<br/>".join(notes)
    nextlink = ""
    if song.get('nextid'): nextlink = song.get('nextid')
    prevlink = ""
    if song.get('previd'): prevlink = song.get('previd')

    song_text = getLyricPageTemplate().substitute(
      NEXTID         = nextlink,
      PREVID         = prevlink,
      SONG_TITLE     = title,
      SONG_CREDITS   = credittable,
      SONG_NOTES     = allnotes,
      SONG_LYRICS    = DIV(dclass="bubble large",content=alllyrics),
      AMAZON         = amazonWidget,
      ITUNES         = itunesButton,
      SONG_COPYRIGHT = copyright
    )

    songsroot = location.docroot + "songs/"
    with open(songsroot+song.get('fileID')+".html", "w") as songfile:
      print "generating",title
      songfile.write(song_text.encode('UTF-8'))


  # STEP 4: generate an index page for each alphabet letter
  for letter in '0' + string.uppercase :
    songRows = []
    for title in sorted(alphaIndex[letter]) :
      song = alphaElements[title]
      songRows.append(DIV(dclass="padded3", content=A(href=song.get('fileID')+".html", content=song.get('title'))))

    index_text = getLyricsIndexTemplate("Elton John \""+letter+"\" Songs").substitute(
      EXTRA_HEADER = "",
      LISTING = DIV(dclass="bubble important padded3", content="\n".join(songRows))
    )
    with open(songsroot+letter+"_index.html","w") as indexfile:
      indexfile.write(index_text.encode('UTF-8'))


  # STEP 5: generate a single introduction index page for all lyrics
  index_text = getLyricsIndexTemplate("Elton John Song Lyrics").substitute(
    EXTRA_HEADER   = META(name="description", content=metadata),
    LISTING = DIV(dclass="margin20 important", content=introduction) + DIV(dclass="bubble small", content=warning),
  )
  with open(songsroot+"index.html","w") as indexfile:
    indexfile.write(index_text.encode('UTF-8'))


  # STEP 6: generate a data file that the CGI script uses to search lyrics
  with open(location.dbroot+"searchable_lyrics.txt","w") as searchfile:
    searchfile.write("\n".join(searchable).encode('UTF-8'))

  return totalsongs


## ---------------------------------------------------------------------------
## Main program.
## ---------------------------------------------------------------------------
if __name__=="__main__":
  s = generate_songs()
  print "total song pages:", s
