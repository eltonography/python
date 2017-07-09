import xml.etree.ElementTree as XML
import location
import templates
from html_tools import DIV


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def generate_404() :

  root = XML.parse(location.dbroot + 'file_not_found.xml').getroot()
  text = XML.tostring(root)
  index_text = templates.getBaseTemplate(None).substitute(
    EXTRA_HEADER  = "",
    PAGE_TITLE   = "Eltonography: file not found",
    PAGE_CONTENT = DIV(dclass="bubble", content=text),
  )
  with open(location.docroot + "404.html", "w") as index:
    index.write(index_text)

## ---------------------------------------------------------------------------
## Main program.
## ---------------------------------------------------------------------------
if __name__=="__main__":
  generate_404()
