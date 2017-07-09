from string import Template, uppercase
from datetime import date
from html_tools import DIV, HEAD, A, HTML, TITLE, BODY, B, TABLE, TR, TD, IMG, SPAN, BR


# ----------------------------------------------------------------------------
# This goes at bottom of every page.
# ----------------------------------------------------------------------------
def getBottomAdvertold() :
  return DIV(dclass="bold darkblue margin20", content=A(href="http://www.ebay.com/sch/captain_fantastic/m.html?_nkw=&_armrs=1&_ipg=&_from=", content="Elton John rarities for sale on Ebay"))

def getBottomAdvertxxx() :
  return """\
<script type="text/javascript" src="//www.auctionnudge.com/item_build/js/SellerID/captain_fantastic/siteid/0/theme/simple_list/MaxEntries/6/show_logo/1"></script><div id="auction-nudge-items" class="auction-nudge"><a href="http://www.auctionnudge.com/your-ebay-items">eBay on my website by Auction Nudge</a></div>"""

def getBottomAdvert() :
  ebaylink = "http://www.ebay.com/sch/captain_fantastic/m.html?_nkw=&_armrs=1&_ipg=&_from="
  ebaylogo = IMG(src="/pix/ebaylogo.png", width="120", height="48")
  ebaytext = "See my Elton John<br/>Auction Items on EBAY"
  ebaylayout = TABLE(TR(TD(ebaylogo)+TD(ebaytext)))
  ebaybox = TD(A(href=ebaylink, content=DIV(dclass="bubble", content=ebaylayout)))
  tictaillink = "http://eltonography.tictail.com"
  tictaillogo = IMG(src="/pix/shopping_cart.png", width="59", height="48")
  tictailtext = "Collectibles For Sale<br/>In Eltonography SHOP"
  tictaillayout = TABLE(TR(TD(tictaillogo) + TD(tictailtext)))
  tictailbox = TD(A(href=tictaillink, content=DIV(dclass="bubble", content=tictaillayout)))
  table = TABLE(dclass="center", content=TR(content=ebaybox+tictailbox))
  return table

# ----------------------------------------------------------------------------
# The javascript function that redirects browser to the file identified in
# the value of the currently selected option of the selector object sent as
# the argument to the function.
# ----------------------------------------------------------------------------
def tourFunctions() :
  return """\
<script type="text/javascript">
function showConcerts(selector) {
  str = selector.options[selector.selectedIndex].value;
  document.location=str;
}
function toggle(id) {
  var elem = document.getElementById(id);
  if(elem.style.display == "none") {
    elem.style.display = "";
  } else {
    elem.style.display = "none";
  }
}
</script>
"""

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def facebookHeader() :
  return """\
<div id="fb-root"></div>
<script>(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/all.js#xfbml=1";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));</script>
"""

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def facebookPlugin() :
  return """\
  <div style="background-color:#fff;" class="fb-like-box" data-href="http://www.facebook.com/eltonography"
       data-width="700" data-show-faces="false" data-stream="true" data-header="true"></div>
"""

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def tictailContent() :
  return """\
  <div class="sale">
  <img src="colored_vinyl.jpg">
  <p/>
  The Eltonography store offers a multitude of Elton John records, CDs, 
  books, magazines, clothing, posters, toys and other memorabilia from
  all over the world. All items will be carefully packaged and shipped
  after payment is complete. More items will be added over time, so
  remember to check back again!
  <p/>
  <a href="http://eltonography.tictail.com">Enter Store</a>
  </div>
"""

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def getGoogleAd() :
  google_ad       = """<div class="googlead">
  <script type="text/javascript"><!--
  google_ad_client = "pub-1622175966048288";
  google_ad_width = 468;
  google_ad_height = 60;
  google_ad_format = "468x60_as";
  google_ad_type = "text";
  google_ad_channel = "";
  google_color_border = "7CB9D1";
  google_color_bg = "99E1FF";
  google_color_link = "0000FF";
  google_color_text = "000000";
  google_color_url = "008000";
  //-->
  </script>
  <script type="text/javascript"
    src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
  </script>
  </div>"""
  return google_ad

#
#
#
def topad():
  ebaylink = "http://www.ebay.com/sch/captain_fantastic/m.html?item=161127422228&ssPageName=STRK%3AMESELX%3AIT&rt=nc&_trksid=p2047675.l2562"
  return DIV(dclass="banner",content=A(href=ebaylink,content="Rare items for sale on Ebay"))

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def goHome() :
  return """\
<script type="text/javascript">
function goHome() {document.location="/index.html";}
</script>
"""

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def getTabImg(tabName, front=False, alt=""):
  layer = "back"
  if front: layer = "front"
  return Template("""<img class="menu_button"
          src="/pix/${TNAME}_tab_${LAYER}.gif" alt="${ALT}"
          onmouseover="this.src='/pix/${TNAME}_tab_${LAYER}_over.gif';"
          onmouseout="this.src='/pix/${TNAME}_tab_${LAYER}.gif';"/>""").substitute(
    TNAME = tabName,
    ALT = alt,
    LAYER = layer,
    )

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def getTabs(fronttab=None) :
  bevel       = """<img class="menu_bevel", src="/pix/tab_bevel.gif"/>"""
  lyrics_tab  = A(href="/songs/index.html",   content=getTabImg("lyrics", front=fronttab=="lyrics", alt="Elton John lyrics"))
  albums_tab  = A(href="/albums/standard/index.html",  content=getTabImg("albums", front=fronttab=="albums", alt="Elton John Albums"))
  singles_tab = A(href="/singles/index.html", content=getTabImg("singles",front=fronttab=="singles",alt="Elton John singles"))
  tours_tab   = A(href="/tours/index.html",   content=getTabImg("tours",  front=fronttab=="tours",  alt="Elton John tours"))
  books_tab   = A(href="/books/index.html",   content=getTabImg("books",  front=fronttab=="books",  alt="Elton John books"))
  shop_tab    = A(href="/shop/index.html",    content=getTabImg("shop",   front=fronttab=="shop",   alt="Elton Items for Sale"))
  return DIV(content=bevel+lyrics_tab+albums_tab+singles_tab+tours_tab+books_tab+shop_tab, dclass="tabbed_menu")

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def getBaseTemplate(fronttab) :
  header_image    = DIV(dclass="header_image", content=IMG(src="/pix/arms.gif", width="800", height="240"))
  header_image = ""
  #home_button     = """<a href="/index.html"><img class="home_button" src="/pix/home_button.png" alt="eltonography.com home page" onmouseover="this.src='/pix/home_button_over.png';" onmouseout="this.src='/pix/home_button.png';"></a>"""
  #email_button    = """<a href="/contact.html"><img style="position:absolute;left:185px;top:75px" class="email_button" src="/pix/email_button.png" alt="contact the author" onmouseover="this.src='/pix/email_button_over.png';" onmouseout="this.src='/pix/email_button.png';"></a>"""
  #sale_button    = """<a href="TBD.html"><img style="position:absolute;left:265px;top:75px" class="sale_button" src="/pix/sale_button.png" alt="Elton John items for sale" onmouseover="this.src='/pix/sale_button_over.png';" onmouseout="this.src='/pix/sale_button.png';"></a>"""
  subtitle        = DIV(dclass="title_subtext", content="The online illustrated Elton John Discography<br/>by David Bodoh")
  blanktext       = """<a href="/index.html"><img src="/pix/blank.gif" style="position:absolute;left:10px;top:10px;width:780px;height:150px;z-index:3;" border="0"></a>"""
  header_template = DIV(dclass="header", onclick="location.href='/index.html';", style="cursor: pointer;", content=blanktext+subtitle)
  contactLink     = A(href="/contact/index.html", content="David Bodoh")
  copytext        = "Copyright &copy; " + str(date.today().year) + " " + contactLink
  trailer_div     = DIV(dclass="trailer", content=getBottomAdvert() + copytext)
  title           = TITLE(content="${PAGE_TITLE}")
  css             = """<link rel="stylesheet" type="text/css" href="/css/style3.css" />"""
  js              = goHome()
  head            = HEAD(content=title+css+js+"${EXTRA_HEADER}")
  mainbubble      = DIV(dclass="center_800", content=header_template+getTabs(fronttab)+'${PAGE_CONTENT}'+trailer_div)
  adbubble        = DIV(dclass="advert_800", content=getGoogleAd())
  body            = BODY(content=mainbubble + adbubble)
  html            = HTML(content=head+body)

  return Template(html)

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def getAlphaLinks() :
  letterlinks = []
  for letter in '0' + uppercase:
    shown = letter
    if shown == '0': shown = '#'
    letterlinks.append(A(dclass="song_letter",href="/songs/"+letter+"_index.html",content=shown))
  return DIV(dclass="lyrics_letters", content="".join(letterlinks))

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def getSearchBox() :
  searchform = """<form action="/cgi-bin/lyrics-search.cgi" METHOD=POST>
    Search Elton John song lyrics: <input type="TEXT" SIZE="45" name="query" maxsize=60>
  </form>"""
  return DIV(dclass="lyrics_search", content=searchform)

# ----------------------------------------------------------------------------
# The old address was http://wms.assoc-amazon.com/20070822/US/js/swfobject_1_5.js
# ----------------------------------------------------------------------------
def getAmazonWidget(asin, title):
  amazon_script = """
  <script type='text/javascript'>
  var amzn_wdgt={widget:'MP3Clips'};
  amzn_wdgt.tag='theillustrate-20';
  amzn_wdgt.widgetType='ASINList';
  amzn_wdgt.ASIN='${ASIN}';
  amzn_wdgt.title="${SONG_TITLE}";
  amzn_wdgt.width='234';
  amzn_wdgt.height='60';
  amzn_wdgt.shuffleTracks='False';
  amzn_wdgt.marketPlace='US';
   </script>
  <script type='text/javascript' src='http://ws-na.amazon-adsystem.com/20070822/US/js/swfobject_1_5.js'>
  </script>"""
  amazontemplate = Template(DIV(content=amazon_script))
  return amazontemplate.substitute(
    ASIN       = asin,
    SONG_TITLE = title,
  )

# ----------------------------------------------------------------------------
# Returns the Amazon button with link to the give ASIN.
# ----------------------------------------------------------------------------
def getAmazonButtonOld(asin):
  url = "".join(["http://www.amazon.com/gp/product/",
        asin,"/ref=as_li_qf_sp_asin_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=",
        asin,"&linkCode=as2&tag=theillustrate-20"])
  gif = "http://rcm-images.amazon.com/images/G/01/associates/remote-buy-box/buy2.gif"
  return A(href=url, target="amazon", content=IMG(dclass="amazon_button", src=gif, alt="Buy from Amazon.com"))

def getAmazonButton(asin):
  '''
  <a href="http://www.amazon.com/gp/product/1851498060/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=1851498060&linkCode=as2&tag=theillustrate-20&linkId=5FN7GSVXM5HOJJ3J">Two Days that Rocked the World: Elton John Live at Dodger Stadium: Photographs by Terry O'Neill</a>
  <img src="http://ir-na.amazon-adsystem.com/e/ir?t=theillustrate-20&l=as2&o=1&a=1851498060" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
  '''
  url = "".join(["http://www.amazon.com/gp/product/",
        asin,
        "/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=",
        asin,
        "&linkCode=as2&tag=theillustrate-20&linkId=Z4H4FKDBKDF74FJX"])
  gif = "http://rcm-images.amazon.com/images/G/01/associates/remote-buy-box/buy2.gif"
  link = A(href=url, target="amazon", content=IMG(dclass="amazon_button", src=gif, alt="Buy from Amazon.com"))
  extra = '''<img src="http://ir-na.amazon-adsystem.com/e/ir?t=theillustrate-20&l=as2&o=1&a=B00ISFZQ2Q" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />'''
  return link

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def getItunesLink(code):
  ituneslink = """<a href="http://click.linksynergy.com/fs-bin/stat?id=ven*WJHIINE&offerid=146261&type=3&subid=0&tmpid=1826&RD_PARM1=http%253A%252F%252Fitunes.apple.com%252Fus%252Falbum%252F${ITUNES}%2526uo%253D4%2526partnerId%253D30" target="itunes_store"><img src="http://ax.phobos.apple.com.edgesuite.net/images/web/linkmaker/badge_itunes-lrg.gif" alt="Download from itunes" style="border: 0;" /></a>"""
  template = Template(DIV(dclass="itunes_link", content=ituneslink))
  return template.substitute(
    ITUNES  = code,
  )

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def getDotsDiv(myindex, total) :
  navDots=[]
  for link in range(total) :
    suffix = str(link+1)
    if link == 0: suffix = ""
    if link == myindex:
      navDots.append(IMG(dclass="navdots", src="/pix/white_dot.gif"))
    else:
      navDots.append(A(href="index"+suffix+".html", alt="page "+suffix, content=IMG(dclass="noborder navdots", src="/pix/green_dot.gif")))
  return DIV("".join(navDots))

# ----------------------------------------------------------------------------
# LYRICS PAGE 
# ----------------------------------------------------------------------------
def getLyricPageTemplate() :
  songcredits = DIV(dclass="credits", content="${SONG_CREDITS}")
  songtitle = DIV(dclass="songtitle", content="${SONG_TITLE}")
  songnotes = DIV(dclass="songnotes", content="${SONG_NOTES}")
  songlyrics = DIV(dclass="lyrics", content="${SONG_LYRICS}")
  songcopy = DIV(dclass="copy", content="${SONG_COPYRIGHT}")
    
  prev_link = A(href="${PREVID}.html", content=IMG(dclass="arrow_link", src="/pix/left_arrow.gif", alt="previous song"))
  next_link = A(href="${NEXTID}.html", content=IMG(dclass="arrow_link", src="/pix/right_arrow.gif", alt="next song"))
  title_table = TABLE(content=TR(TD(prev_link, dclass="left_arrow") + TD(dclass="songtitle", content=songtitle) + TD(next_link, dclass="right_arrow")), dclass="song_title")

  pagecontent = DIV(dclass="lyric_page",content=getAlphaLinks()+getSearchBox()+title_table+songnotes+songcredits+songlyrics+songcopy+"${AMAZON}"+"${ITUNES}")

  return Template(getBaseTemplate("lyrics").substitute(
    EXTRA_HEADER  = "",
    PAGE_TITLE   = "Elton John Lyrics: ${SONG_TITLE}",
    PAGE_CONTENT = pagecontent,
  ))

# ----------------------------------------------------------------------------
# LYRICS INDEX
# ----------------------------------------------------------------------------
def getLyricsIndexTemplate(title) :
  pageheader=DIV(dclass="songtitle", content=title)
  indexcontent = DIV(dclass="lyric_page", content=getAlphaLinks()+getSearchBox()+pageheader+"${LISTING}")

  return Template(getBaseTemplate("lyrics").substitute(
    EXTRA_HEADER  = "${EXTRA_HEADER}",
    PAGE_TITLE   = title,
    PAGE_CONTENT = indexcontent,
  ))

def getSubAlbumBar(subcategory) :
  cells = []
  for subType in ["Standard","International","Appearances","Unauthorized","Sessions"] :
    if subType == subcategory:
      cells.append(TD(dclass="important padded10", content=A(href="/albums/"+subType.lower()+"/index.html",content=subType)))
    else :
      cells.append(TD(dclass="padded10", content=A(href="/albums/"+subType.lower()+"/index.html",content=subType)))
  return TABLE(dclass="center", content=TR(content="".join(cells)))


def getAlbumTemplate(subcategory) :
  return Template(getBaseTemplate("albums").substitute(
    EXTRA_HEADER    = "${EXTRA_HEADER}",                            # pass-thru
    PAGE_TITLE      = "${PAGE_TITLE}",                               # pass-thru
    PAGE_CONTENT    = getSubAlbumBar(subcategory) + "${PAGE_CONTENT}",  # prepend subindex bar
  ))


def getStandardAlbumTemplate(title) :
  title_bar = DIV(dclass="single_title", content=TABLE(dclass="single_title",
     content=TR(TD(content="${PREVICON}", dclass="left_arrow") + 
     TD(dclass="songtitle", content="${ALBUM_TITLE}<br/>${ALBUM_NOTES}") + 
     TD(content="${NEXTICON}", dclass="right_arrow"))))
  return Template(getAlbumTemplate("Standard").substitute(
    EXTRA_HEADER    = "",                           # no style needed
    PAGE_TITLE      = "Elton John Album: "+title,   # use album title here
    PAGE_CONTENT    = title_bar + "${VERSIONS}",
  ))


def getStandardIndexTemplate() :
  return Template(getAlbumTemplate("Standard").substitute(
    EXTRA_HEADER    = "${EXTRA_STYLE}",
    PAGE_TITLE      = "Elton John Album Discography",
    PAGE_CONTENT    = "${CONTENT}",
  ))


def getInternationalAlbumTemplate(country) :
  leftTD = TD(content="${PREVICON}", dclass="left_arrow")
  centerTD = TD(dclass="songtitle", content="${COUNTRY}")
  rightTD = TD(content="${NEXTICON}", dclass="right_arrow")
  row = TR(leftTD + centerTD + rightTD)
  table = TABLE(dclass="single_title",content=row)
  title_bar = DIV(dclass="single_title", content=table)
  return Template(getAlbumTemplate("International").substitute(
    EXTRA_HEADER    = "",
    PAGE_TITLE      = "Elton John Albums from "+country,
    PAGE_CONTENT    = title_bar + "${ALBUMS}" + title_bar,
  ))


def getInternationalIndexTemplate() :
  return Template(getAlbumTemplate("International").substitute(
    EXTRA_HEADER    = "",
    PAGE_TITLE      = "Elton John International Albums",
    PAGE_CONTENT    = "${PAGE_CONTENT}",
  ))


def getGuestIndex() :
  return Template(getAlbumTemplate("Appearances").substitute(
    EXTRA_HEADER = "",
    PAGE_TITLE   = "Elton John Guest Apperances",
    PAGE_CONTENT = BR().join(["${TITLE}","${DESCR}","${NAVBAR}","${ALBUMS}","${NAVBAR}"])
  ))


def getImportIndex() :
  return Template(getAlbumTemplate("Unauthorized").substitute(
    EXTRA_HEADER = "",
    PAGE_TITLE   = "Elton John Unauthorized CDs",
    PAGE_CONTENT = BR().join(["${TITLE}","${DESCR}","${NAVBAR}","${ALBUMS}","${NAVBAR}"])
  ))


def getSessionIndex() :
  return Template(getAlbumTemplate("Session").substitute(
    EXTRA_HEADER = "",
    PAGE_TITLE   = "Elton John as a Session Musician",
    PAGE_CONTENT = BR().join(["${TITLE}","${DESCR}","${ALBUMS}"])
  ))

  
def getBooksNavBar(subcategory) :
  cells = []
  for subType in ["Books","Magazines"] :
    if subType == subcategory:
      cells.append(TD(dclass="important padded10", content=A(href="/"+subType.lower()+"/index.html",content=subType)))
    else :
      cells.append(TD(dclass="padded10", content=A(href="/"+subType.lower()+"/index.html",content=subType)))
  return TABLE(dclass="center", content=TR(content="".join(cells)))

def getBooksIndex() :
  return Template(getBaseTemplate("books").substitute(
    EXTRA_HEADER    = "${EXTRA_HEADER}",
    PAGE_TITLE      = "Elton John Books and Biographies",
    PAGE_CONTENT    = getBooksNavBar("Books") + "${DESCR}\n${NAVBAR}\n${BOOKS}\n${NAVBAR}",
  ))
  
def getMagazineIndex() :
  return Template(getBaseTemplate("books").substitute(
    EXTRA_HEADER    = "${EXTRA_HEADER}",
    PAGE_TITLE      = "Elton John Magazine Covers",
    PAGE_CONTENT    = getBooksNavBar("Magazines") + "${DESCR}\n${NAVBAR}\n${BOOKS}\n${NAVBAR}",
  ))



# ----------------------------------------------------------------------------
# SINGLE PAGE
# ----------------------------------------------------------------------------
def getSingleTemplate() :
  single_span = SPAN(dclass="songtitle", content="${SINGLE_TITLE}") + BR() + SPAN(dclass="subtitle", content="${SINGLE_SUBTITLE}")
  prev_link = A(href="${PREVID}.html", content=IMG(src="/pix/left_arrow.gif", border="0", alt="previous single", title="previous single"))
  next_link = A(href="${NEXTID}.html", content=IMG(src="/pix/right_arrow.gif", border="0", alt="next single", title="next single"))
  title_bar = DIV(dclass="single_title", content=TABLE(dclass="single_title", content=TR(TD(content=prev_link, dclass="left_arrow") + 
     TD(dclass="songtitle", content=single_span) + 
     TD(content=next_link, dclass="right_arrow"))))
  issues = DIV(content="${ISSUES}")

  return Template(getBaseTemplate("singles").substitute(
    EXTRA_HEADER = "",
    PAGE_TITLE   = "Elton John Single: ${SINGLE_TITLE}",
    PAGE_CONTENT = title_bar + issues + title_bar,
  ))


def getSingleIndex() :
  return Template(getBaseTemplate("singles").substitute(
    EXTRA_HEADER  = "",
    PAGE_TITLE   = "Elton John Singles",
    PAGE_CONTENT = "${TITLE}"+"${DESCR}"+DIV("${NAVBAR}")+DIV("${ISSUES}")+DIV("${NAVBAR}"),
  ))


def getTourIndex() :
  return Template(getBaseTemplate("tours").substitute(
    EXTRA_HEADER = tourFunctions(),
    PAGE_TITLE   = "Elton John Concerts",
    PAGE_CONTENT = "${PAGE_CONTENT}",
  ))

def getFacebookPage() :
  return getBaseTemplate("news").substitute(
    EXTRA_HEADER = "",
    PAGE_TITLE   = "Eltonography News",
    PAGE_CONTENT = facebookHeader() + facebookPlugin(),
  )
  
def getTictailPage() :
  return getBaseTemplate("shop").substitute(
    EXTRA_HEADER = "",
    PAGE_TITLE   = "Eltonography Shop",
    PAGE_CONTENT = tictailContent(),
  )