#!/usr/local/bin/python2.7

import xml.etree.ElementTree as ET
import location
from html_tools import TR, TD, B, DIV, TABLE, IMG, U
import templates
from getimageinfo import getImageInfo

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def generate_books() :
  totalBooks = 0
  totalPages = 0
  bookspath = location.docroot + "books/"
  picpath = bookspath + "pix/"
  bubbles = []
  root = ET.parse(location.dbroot + 'books.xml').getroot()
  for book in root:
    if book.tag == "introduction":
      introduction = book.text
      continue
    pages = int(book.get('pages'))
    totalPages += pages
    totalBooks += 1
    if book.get('private'): continue

    rows = []
    pic = book.get('pic')
    picfile  = picpath + pic
    try:
      (type,width,height) = getImageInfo(picfile)
      imageTD = TD(dclass="single_sleeve", content=IMG(dclass="sleeve", src="pix/"+pic, width=width, height=height))
      if width != 200: print "bad width for",pic
    except IOError:
      print "cannot find picture for",book.get('title'),":",pic
    titletext = book.get('title')
    rows.append(DIV(dclass="important left", content="Title: " + U(B(titletext))))
    if book.get('author'):
      authortext = book.get('author')
      rows.append(DIV(dclass="left", content="Author: " + B(authortext)))
    rows.append(DIV(dclass="left", content="Year: " + B(book.get('year'))))
    if book.get('publisher'):
      pubtext = book.get('publisher')
      rows.append(DIV(dclass="left", content="publisher: " + B(pubtext)))
    if book.get('ISBN'): rows.append(DIV(dclass="left", content="ISBN: "+B(book.get('ISBN'))))
    if book.get('country'): rows.append(DIV(dclass="left", content="Country: " + B(book.get('country'))))
    rows.append(DIV(dclass="left", content="pages: " + B(str(pages))))
    rows.append(DIV(dclass="left", content="binding: " + B(book.get('format'))))
    if book.get('amazon'): rows.append(DIV(dclass="left", content=templates.getAmazonButton(book.get('amazon'))))

    d = book.find('description')
    if d is not None:
      if d.get('source'): rows.append(DIV(dclass="left small padded3 bold", content="[description text from " + d.get('source')+":]"))
      rows.append(DIV(dclass="left", content=ET.tostring(element=d)))
    textTD = TD(dclass="top", content="".join(rows))
    bubbles.append(DIV(dclass="bubble", content=TABLE(TR(imageTD + textTD))))

  #index_text = templates.getBooksIndex().substitute(
   # DESCR  = DIV(dclass="description", content=introduction),
   # BOOKS  = DIV(dclass="full_width", content="\n\n".join(bubbles)),
  #)

  # figure out how many index pages we need to create
  max_rows_per_index = 14;
  total_index_pages = len(bubbles)/max_rows_per_index
  if len(bubbles) % max_rows_per_index > 0: total_index_pages += 1

  # chop away at the bubbles list, moving them into the current index page
  bookroot = location.docroot + "books/"
  for page in range(total_index_pages) :
    my_rows = bubbles[:max_rows_per_index]       # grab the books that go into this index page
    del bubbles[:max_rows_per_index]             # clean up as we go
    book_index_text = templates.getBooksIndex().substitute(
      EXTRA_HEADER = "",
      DESCR  = DIV(dclass="description", content=introduction),
      BOOKS  = DIV(dclass="full_width", content="\n\n".join(my_rows)),
      #NAVBAR = DIV(content=DIV(content=" ".join(navDots))),
      NAVBAR = templates.getDotsDiv(page, total_index_pages),
    )
    suffix = str(page+1)
    if page == 0: suffix = ""
    with open(bookroot+"index"+suffix+".html", "w") as bookindex:
      bookindex.write(book_index_text.encode('UTF-8'))
  return totalBooks


## ---------------------------------------------------------------------------
## Main program.
## ---------------------------------------------------------------------------
if __name__=="__main__":
  b = generate_books()
  print "total books:", b
