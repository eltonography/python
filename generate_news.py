import location
import templates

# ----------------------------------------------------------------------------
# Converts the concerts.txt file to an XML file, including songs from
# each of the dated sub-folder files.
# ----------------------------------------------------------------------------
def generate_news() :
  with open(location.docroot + "news/index.html", 'w') as newspage:
    newspage.write(templates.getFacebookPage())

## ---------------------------------------------------------------------------
## Main program.
## ---------------------------------------------------------------------------
if __name__=="__main__":
  generate_news()
