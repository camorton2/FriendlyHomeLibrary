# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import eyed3
from eyed3 import id3, mp3
from .models import Collection, CommonFile, Musician, Artist, Song
from django.utils.text import slugify
from django.db import models

def add_collection(cAlbum, cSlug, cPath):
    print ("---> ADD Album %s slug %s path %s" % (cAlbum,cSlug,cPath))
    try:
        dbobj = Collection.objects.get(slug=cSlug)
    except Collection.DoesNotExist:
        dbobj = Collection(filePath=cPath,title=cAlbum,slug=cSlug)
        dbobj.save()
    return dbobj

def add_song(sTrack, sTitle, sFileName, sSlug, sCollection):
    print ("---> ADD Song %s, track %s, filename %s, slug %s: " % (sTitle,sTrack,sFileName,sSlug))
    try:
        dbobj = Song.objects.get(slug=sSlug)
    except Song.DoesNotExist:
        dbobj = Song(track=sTrack,title=sTitle,slug=sSlug,fileName=sFileName, collection=sCollection)
        dbobj.save()
    return dbobj

def add_musician(aName, aSlug):
    print("---> ADD Musician %s, slug %s" % (aName, aSlug))
    try:
        dbobj = Musician.objects.get(slug=aSlug)
    except Musician.DoesNotExist:
        dbobj = Musician(fullName=aName,slug=aSlug)
        dbobj.save()
    return dbobj

def add_file(root,myfile,path):
    print("file %s, root %s, path %s" % (myfile,root,path))
    theFile = os.path.join(root,myfile)
    if mp3.isMp3File(theFile):
        tag = id3.Tag()
        tag.parse(theFile)
        myArtist = tag.artist

        if myArtist is None :
            print("*******************  BOGUS - skipping")
        else:
            # handle the collection (album) which only has a path and a name
            collectionSlug = slugify( unicode( '%s%s' % (tag.album,myArtist) ))
            collection = add_collection(cAlbum=tag.album,cSlug=collectionSlug,cPath=path)

            # song has track, title, filename, slug, collection
            songSlug = slugify( unicode('%s%s' % (tag.title,myArtist)))
            t1, t2 = tag.track_num
            song = add_song(sTrack=t1,sTitle=tag.title, sFileName=myfile, sSlug=songSlug, sCollection=collection)

            # musician has name, slug
            artistSlug = slugify( unicode('%s' % (myArtist)))
            musician = add_musician(aName=myArtist, aSlug=artistSlug)
            # when adding these, do I need to check if they are already there?
            musician.albums.add(collection)
            musician.songs.add(song)
    else:
        print("******* BOGUS NOT MP3"+theFile)


