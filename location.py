import platformimport os

docroot = ""
if platform.system() == "Linux":
  homeroot = "/var/chroot/home/content/28/8910828/"
  docroot = homeroot+"html/"
  dbroot = homeroot+"db/"
else :  # assume windows on one of the home PCs  if platform.platform().startswith("Windows-7"):    homeroot = "c:/eltonography/"    docroot = homeroot    dbroot = "c:/users/david/google drive/elton/db/"  else:    homeroot = "c:/Documents and Settings/David/My Documents/eltonography/"    docroot = homeroot+"html/"    dbroot = "c:/Documents and Settings/David/My Documents/Google Drive/Elton/db/"
