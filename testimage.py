import getimageinfo

file = "C:/Users/david/Documents/elton/eltonography/albums/pix/LP/OZ/the_very_best.jpg"
imgdata = open(file,'rb').read(200)
(type,width,height) = getimageinfo.getImageInfo(imgdata)
print "width=",width,"height=",height