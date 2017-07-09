#!/usr/local/bin/python2.7

# ----------------------------------------------------------------------------
# Copyright David Bodoh 2013
#
# This script loads an XML catalog of Elton John singles, and generates a set
# of HTML files, with links to sleeve images. "Private" singles are skipped.
# Track titles are hyperlinked to lyrics pages. Each "single" page is linked
# to navigate forward/back to other singles chronologically.  Leftover
# miscellaneous singles are cataloged in their respective countries.
# ----------------------------------------------------------------------------
import xml.etree.ElementTree as ET
import re
import location
import os.path
import templates
from getimageinfo import getImageInfo
from songLib import loadSongs, linkTrack
from html_tools import DIV, HEAD, A, HTML, TITLE, BODY, B, TR, TD, IMG, TABLE, BR, SPAN

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def generate_singles():

  singles_root = location.docroot + "singles/"

  # ----------------------------------------------------------------------------
  # Collect href information for albums, to verify album linking. Dictionary is
  # fileID -> title_string
  # ----------------------------------------------------------------------------
  #album_ids = {}
  #albums = ET.parse(location.dbroot+'category_albums.xml').getroot()
  #for album in albums:
  #  album_ids[album.get('id')] = album.get('title')
  #albums = ET.parse(location.dbroot+'other_albums.xml').getroot()
  #for album in albums:
  #  album_ids[album.get('id')] = album.get('title')


  xmldoc = ET.parse(location.dbroot+'singles.xml').getroot()     # load singles from file

  # ----------------------------------------------------------------------------
  # Set the id/prev/next links as XML attributes.
  # ----------------------------------------------------------------------------
  prevsingle = None
  for single in xmldoc:
    if single.get('artist') : continue           # some other artist single
    if single.get('private') : continue          # not for public website
    if single.tag == 'description':
      description = single.text
      continue
    if single.tag == 'break' : continue
    if single.tag == 'single' :                  # get the id from the title
      id = re.sub(' ', '_', single.get('title')).lower()
      id = re.sub('\(', '', id)
      id = re.sub('\)', '', id)
      id = re.sub('\/',' ', id)
      id = re.sub('\'', "", id)
      single.set('id', re.sub(' ', '_', id))
    if single.tag == 'miscellaneous' :
      single.set('id', re.sub(' ','_',single.get('country').lower()))
    if prevsingle != None:
      prevsingle.set('nextid',single.get('id'))  # forward link
      single.set('previd',prevsingle.get('id'))  # backward link
    else :
      firstsingle = single                       # save first for linnking with last
    prevsingle = single
  single.set('nextid', firstsingle.get('id'))    # fully cycled double linked-list
  firstsingle.set('previd', single.get('id'))    # fully cycled double linked-list
 

  # ----------------------------------------------------------------------------
  # Store each single as its own HTML file with listing of issues.  Also
  # generate index pages.
  # ----------------------------------------------------------------------------
  picpath = singles_root + "pix/"
  flagpath = location.docroot + "/pix/flags/"
  index_rows = []                                # prepare list for index page
  total_issues = 0                               # prepare info for index page
  total_pages = 0
  for single in xmldoc:
    if single.tag == 'description': continue     # already got this
    if single.get('artist'): continue            # ignore singles by non-Elton artists
    if single.get('private'): continue           # ignore singles not intended for public
    total_pages += 1
    icon=None                                    # should be populated later
    if single.tag == 'single':
      title = single.get('title')
      subtitle = '('+single.get('release')[0:4] + ')'
      (type,width,height) = getImageInfo(picpath+'icons/'+single.get('icon'))
      single_icon=IMG(src="pix/icons/"+single.get('icon'), width=width, height=height, alt=title, dclass="single_icon")
    elif single.tag == 'break':
      index_rows.append(DIV(dclass="bubble description", content=single.text))
      continue
    elif single.tag == 'miscellaneous' :
      title = single.get('country')+" unique singles"
      subtitle = "(miscellaneous releases)"
      flag = re.sub(' ','_',single.get('country').lower()) + ".gif"
      if not os.path.isfile(flagpath+flag): print "ERROR missing flag for",country
      (type,width,height) = getImageInfo(flagpath+flag)
      single_icon = IMG(src="/pix/flags/"+flag, width=width, height=height, alt=title, dclass="single_icon")

    #print "parsing",title
    # TBD...
    #if single.get('album') :
    #  album_href = "/albums/"+single.get('album')+".html"
    #  album_title = album_ids.get(single.get('album'))
    #  albumlink = "From the album " + A(href=album_href, content=album_title)
    #  #subtitle += '<br/>('+albumlink+')'

    issues = []
    for issue in single:
      if issue.get('private'): continue          # not for website
      if issue.get('format') == "CS": continue   # not for website yet
      total_issues += 1                          # info for index page
      country = issue.get('country')
      if country == None: print "ERROR missing country"
      count = single.get('count')
      if count: count = int(count)+1
      else: count = 1
      single.set('count',str(count))

      # detect flag GIF based on country
      flag = re.sub(' ','_',country.lower()) + ".gif"
      if not os.path.isfile(flagpath+flag): print "ERROR missing flag for",country
      (type,width,height) = getImageInfo(flagpath+flag)
      flagpic = IMG(src="/pix/flags/"+flag, width=width, height=height, alt=country, title=country)
      if single.tag == 'miscellaneous': flagpic="" # flag for misc issues is redundant

      format = issue.get('format')
      if format == None: print "ERROR missing format"
      if format == 'postcard': continue  # ignore Polish cards for now
      year = issue.get('year')
      if year == 'unknown': year = ""
      if year == None: print "ERROR missing year"
      catalog = issue.get('catalog')
      if catalog == None: print "ERROR missing catalog"
      promo = ""
      if issue.get('promo'): promo = '[promo]'
      discs = ""
      if issue.get('discs'): discs = '[' + issue.get('discs') + ' discs]'
      note = ""
      if issue.get('note') : note = '[' + issue.get('note') + ']'
      if not issue.get('ps'):
        sleeve = ""
        picTD = TD(dclass="missing_sleeve", content="(no sleeve)")
      else:
        if issue.get('ps') == 'true' : sleeve = "[picture sleeve]"
        else : sleeve = '[' + issue.get('ps') + ']'
        pic = re.sub('/','',catalog).upper()
        pic = '/'.join([format,country,pic])
        if issue.get('pic'): pic = "/".join([format,issue.get('pic')])
        pic = re.sub(' ','_',pic)
        pic = re.sub('-','',pic)
        pic = re.sub('\.','',pic)
        if issue.get('pic') : pic = '/'.join([format,issue.get('pic')])
        picfile = None
        if os.path.isfile(picpath+pic+".jpg"): picfile = "pix/"+pic+".jpg"
        elif os.path.isfile(picpath+pic+".gif"): picfile = "pix/"+pic+".gif"

        if picfile:
          (type,width,height) = getImageInfo(singles_root + picfile)
          picTD = TD(dclass="single_sleeve",
              content=IMG(dclass="sleeve", src=picfile, width=width, height=height) + BR() + sleeve)
        else:
          picTD = TD(dclass="missing_sleeve", content="[sleeve photo not available]")
          if issue.get('pic') != "NA":
            print "ERROR: can't find picture:",issue.get('pic'), title, format, country, year, catalog

      if os.path.isfile(singles_root + "pix/"+format+".gif"):
        icon = IMG(src="pix/"+format+".gif")  # use graphical icon
      else: icon = format                     # use text name

      country = "("+country+")"
      if single.tag == 'miscellaneous': country = ""
      issueheader = TR(TD(dclass="single_details", colspan=2, content=" ".join([icon,year,catalog,country,discs,promo,note])))
      trackrows = []
      trackrows.append(issueheader)
      for track in issue:
        tracktime = TD(dclass="time", content=track.get('length'))
        tracktext = TD(dclass="track", content=linkTrack(track))
        trackrows.append(TR(tracktime + tracktext))
      tracktable = TABLE("\n".join(trackrows))
      detailsTD = TD(tracktable)
      issues.append(DIV(dclass="bubble", content=TABLE(dclass="single_issue", content=TR(picTD + detailsTD))))

    page_template = templates.getSingleTemplate()
    single_text = page_template.substitute(
      NEXTID          = single.get('nextid'),
      PREVID          = single.get('previd'),
      SINGLE_TITLE    = '"'+title+'"',
      SINGLE_SUBTITLE = subtitle,
      ISSUES          = "\n".join(issues)
    )

    target = single.get('id')+".html"
    with open(singles_root+target, "w") as singlefile:
      singlefile.write(single_text.encode('latin1'))
    count = single.get('count')
    suffix = ""
    if count > 1: suffix = "s"
    subtitle = SPAN(dclass="single_count",content=subtitle + BR()+'(' + count + '&nbsp;pressing'+suffix+')')
    iconTD = TD(dclass="single_icon", content=A(href=target, content=single_icon))
    textTD = TD(dclass="single_index", content=SPAN(dclass="single_index", content=A(href=target, content=title)) + subtitle)
    index_rows.append(DIV(dclass="bubble", content=TABLE(TR(iconTD + textTD))))

  #TBD index_rows.append(TR(TD("total worldwide pressings: " + str(total_issues))))

  # ----------------------------------------------------------------------------
  # Now write set of index pages that links to all the other single pages.
  # ----------------------------------------------------------------------------

  max_rows_per_index = 30;
  total_index_pages = len(index_rows)/max_rows_per_index
  if len(index_rows) % max_rows_per_index > 0: total_index_pages += 1

  for page in range(total_index_pages) :
    navDots=[]
    for link in range(total_index_pages) :
      suffix = str(link+1)
      if link == 0: suffix = ""
      if link == page:
        navDots.append(IMG(dclass="navdots", src="/pix/white_dot.gif"))
      else:
        navDots.append(A(href="index"+suffix+".html", alt="page "+suffix, content=IMG(dclass="noborder navdots", border="0", src="/pix/green_dot.gif")))

    my_rows = index_rows[:max_rows_per_index]
    del index_rows[:max_rows_per_index]
    single_index_text = templates.getSingleIndex().substitute(
      TITLE = DIV(dclass='heading padded10', content="Elton John Singles"),
      DESCR = DIV(dclass='description', content=description),
      ISSUES = "\n".join(my_rows),
      NAVBAR = DIV(content=DIV(content=" ".join(navDots))),
    )
    suffix = str(page+1)
    if page == 0: suffix = ""
    with open(singles_root+"index"+suffix+".html", "w") as singleindex:
      singleindex.write(single_index_text)

  return total_issues
  

## ---------------------------------------------------------------------------
## Main program.
## ---------------------------------------------------------------------------
if __name__=="__main__":
  loadSongs()
  s = generate_singles()
  print "total single issues:", s
