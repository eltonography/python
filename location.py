import platform

docroot = ""
if platform.system() == "Linux":
  homeroot = "/var/chroot/home/content/28/8910828/"
  docroot = homeroot+"html/"
  dbroot = homeroot+"db/"
else :  # assume windows on one of the home PCs