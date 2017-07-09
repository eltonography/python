import location
import templates

# ----------------------------------------------------------------------------
# Converts the concerts.txt file to an XML file, including songs from
# each of the dated sub-folder files.
# ----------------------------------------------------------------------------
def generate_shop() :
  with open(location.docroot + "shop/index.html", 'w') as shoppage:
    shoppage.write(templates.getTictailPage())

## ---------------------------------------------------------------------------
## Main program.
## ---------------------------------------------------------------------------
if __name__=="__main__":
  generate_shop()
