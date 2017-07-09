import xml.etree.ElementTree as XML
import location
import templates
from html_tools import DIV


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def generate_contact() :

  root = XML.parse(location.dbroot + 'contact.xml').getroot()
  text = XML.tostring(root)
  index_text = templates.getBaseTemplate(None).substitute(
    EXTRA_HEADER  = "",
    PAGE_TITLE   = "Eltonography Contact Me",
    PAGE_CONTENT = DIV(dclass="bubble", content=text),
  )
  with open(location.docroot + "contact/index.html", "w") as contactindex:
    contactindex.write(index_text)

## ---------------------------------------------------------------------------
## Main program.
## ---------------------------------------------------------------------------
if __name__=="__main__":
  generate_contact()
