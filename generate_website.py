from songLib import loadSongs
from generate_songs import generate_songs
from generate_albums import generate_albums
from generate_singles import generate_singles
from generate_tours import generate_tours
from generate_books import generate_books
from generate_news import generate_news
from generate_contact import generate_contact
from generate_404 import generate_404

loadSongs()
print ("total songs:"+ str(generate_songs()))
generate_albums()
print ("total singles:"+ str(generate_singles()))
print ("total concerts:"+ str(generate_tours()))
print ("total books:"+ str(generate_books()))
generate_news()
generate_contact()
generate_404()