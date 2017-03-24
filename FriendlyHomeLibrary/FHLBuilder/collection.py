import os
import eyed3
from eyed3 import id3, mp3
from .models import Common, Song, Artist
from django.utils.text import slugify

def add_file(root,myfile):
    theFile = os.path.join(root,myfile)
    if mp3.isMp3File(theFile):
        tag = id3.Tag()
        tag.parse(theFile)
        myArtist = tag.artist

        if myArtist is None :
            print("*******************  BOGUS - skipping")
        else:
            print(myArtist)
            artistSlug = slugify( unicode('%s' % (myArtist)))
            print("SLUG (artist): " + artistSlug)
            try:
                dbArtist = Artist.objects.get(fullName=myArtist,slug=artistSlug)
            except Artist.DoesNotExist:
                dbArtist = Artist(fullName=myArtist,slug=artistSlug)
                dbArtist.save()
                
            print(tag.track_num)
            print(tag.album)
            print(tag.album_artist)
            songSlug = slugify( unicode('%s %s' % (tag.title,myArtist)))
            print("SLUG (song): " + songSlug)
            print(tag.title)
            #dbArtist = Song.objects.get_or_create(
            #   
            #)
            print(tag.genre)
            print(type(tag.genre))
    else:
        print("******* BOGUS NOT MP3"+theFile)


