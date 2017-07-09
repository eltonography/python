import xml.etree.ElementTree as ET
import location

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def generate_books() :

  root = ET.parse(location.dbroot + 'books.xml').getroot()
  for book in root:
    if book.tag == "introduction": continue
    if book.get('pic') != "inaki_berrio.jpg": continue
    print book.get('author')


## ---------------------------------------------------------------------------
## Main program.
## ---------------------------------------------------------------------------
if __name__=="__main__":
  b = generate_books()

