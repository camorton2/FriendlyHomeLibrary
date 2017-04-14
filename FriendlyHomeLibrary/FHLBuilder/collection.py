# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import eyed3
import enzyme
from eyed3 import id3, mp3
from enzyme import MalformedMKVError
from .models import Collection, CommonFile, Musician, Artist, Song, Tag, Movie
from .models import Actor, Director
from django.utils.text import slugify
from django.db import models
from . import choices

from utility import to_str, get_drive

def setFileKind(obj,kind):
    fKind = kind[0]
    print("FileKind to %s %s" % (kind,fKind))
    if fKind == choices.UNKNOWN:
        print("unknown")
    else:
        obj.fileKind = fKind
        obj.save()


def add_collection(cAlbum, cSlug, cPath,cDrive,saveIt=True):
    print ("---> ADD Collection %s slug %s path %s" % (cAlbum,cSlug,cPath))
    try:
        dbobj = Collection.objects.get(slug=cSlug)
    except Collection.DoesNotExist:
        path = to_str(cPath)
        album = to_str(cAlbum)
        dbobj = Collection(filePath=path,title=album,slug=cSlug,drive=cDrive)
        if saveIt:
            dbobj.save()
    return dbobj

def add_song(sTrack, sTitle, sFileName, sSlug, sCollection):
    print ("---> ADD Song %s, track %s, filename %s, slug %s: " % (sTitle,sTrack,sFileName,sSlug))
    try:
        dbobj = Song.objects.get(slug=sSlug)
    except Song.DoesNotExist:
        sCollection.save()
        track = to_str(sTrack)
        title = to_str(sTitle)
        fileName=to_str(sFileName)
        dbobj = Song(track=track,title=title,slug=sSlug,fileName=fileName, collection=sCollection)
        dbobj.save()
    dbobj.fileKind = choices.SONG
    dbobj.save()
    return dbobj

def add_movie(mTitle, mFileName, mSlug, mCollection):
    print ("---> ADD Movie %s, filename %s, slug %s: " % (mTitle,mFileName,mSlug))
    try:
        dbobj = Movie.objects.get(slug=mSlug)
    except Movie.DoesNotExist:
        mCollection.save()
        title = to_str(mTitle)
        fileName = to_str(mFileName)
        dbobj = Movie(title=title,slug=mSlug,fileName=fileName, collection=mCollection)
        dbobj.save()
    dbobj.fileKind = choices.MOVIE
    dbobj.save()
    return dbobj

def add_musician(aName, aSlug):
    print("---> ADD Musician %s, slug %s" % (aName, aSlug))
    try:
        dbobj = Musician.objects.get(slug=aSlug)
    except Musician.DoesNotExist:
        name = to_str(aName)
        dbobj = Musician(fullName=name,slug=aSlug)
        dbobj.save()
    return dbobj

def add_actor(aName, aSlug):
    print("---> ADD Actor %s, slug %s" % (aName, aSlug))
    try:
        dbobj = Actor.objects.get(slug=aSlug)
    except Actor.DoesNotExist:
        name = to_str(aName)
        dbobj = Actor(fullName=name,slug=aSlug)
        dbobj.save()
    return dbobj

def add_director(aName, aSlug):
    print("---> ADD Director %s, slug %s" % (aName, aSlug))
    try:
        dbobj = Director.objects.get(slug=aSlug)
    except Director.DoesNotExist:
        name = to_str(aName)
        dbobj = Director(fullName=name,slug=aSlug)
        dbobj.save()
    return dbobj


def add_tag(tName, tSlug):
    print("---> ADD Tag %s, slug %s" % (tName, tSlug))
    try:
        dbobj = Tag.objects.get(slug=tSlug)
    except Tag.DoesNotExist:
        name = to_str(tName)
        dbobj = Tag(name=name,slug=tSlug)
        dbobj.save()
    return dbobj


def add_file(root,myfile,path,newCollection,formKind,formTag):
    print("ADD_FILE file %s, root %s, path %s formKind %s formTag %s" % (myfile,root,path,formKind,formTag))
    #drive = get_drive(newCollection.drive)
    theFile = os.path.join(root,myfile)
    if mp3.isMp3File(theFile):
        tag = id3.Tag()
        tag.parse(theFile)
        myArtist = tag.artist
        addC = False
        if myArtist is None :
            print("******************* mp3 file with no artist, skipping %s" % theFile)
        else:
            if tag.album is None:
                collection = newCollection
            else:
                addC = True
                # handle the collection (album) which only has a path and a name
                collectionSlug = slugify( unicode( '%s' % (tag.album) ))
                collection = add_collection(cAlbum=tag.album,cSlug=collectionSlug,cPath=path,cDrive=newCollection.drive)

            # song has track, title, filename, slug, collection
            songSlug = slugify( unicode('%s%s' % (tag.title,collection.slug)))
            t1, t2 = tag.track_num
            if t1 is None:
                t1=0
            song = add_song(sTrack=t1,sTitle=tag.title, sFileName=myfile, sSlug=songSlug, sCollection=collection)
            # musician has name, slug
            artistSlug = slugify( unicode('%s%s' % (myArtist,'-mus')))
            musician = add_musician(aName=myArtist, aSlug=artistSlug)
            setFileKind(song, formKind)
            if len(formTag):
                xSlug = slugify(unicode('%s' % (formTag)))
                xTag=add_tag(formTag,xSlug)
                song.tags.add(xTag)
            # when adding these, do I need to check if they are already there?
            if addC:
                musician.albums.add(collection)
            musician.songs.add(song)
            musician.save()

            genre = tag.genre
            if genre is not None:
                genreSlug = slugify(unicode('%s%s' % (genre.id,genre.name)))
                gen = add_tag(genre.name,genreSlug)
                song.tags.add(gen)
            song.save()
    else:
        # This section is for the info on mkv files, not being used
        #print("******* BOGUS NOT MP3"+theFile)
        # in this section new movies will be added to the passed collection
        ## try:
        ##    with open(theFile,'rb') as f:
        ##        mkv = enzyme.MKV(f)
        ##        print (mkv)
        ##        print (type(mkv))
        ##    f.close()
        ##except MalformedMKVError:
        ##    print("BOGUS MKV skip")

        # start 4 from the end and take the rest
        #extension = theFile[-4:]
        base = os.path.basename(theFile)
        mTitle, extension = os.path.splitext(base)
        #mTitle = os.path.splitext(base)[0]
        mSlug = slugify( unicode('%s' % (mTitle)))
        if extension == '.mkv':
            movie = add_movie(mTitle,base,mSlug,newCollection)
            setFileKind(movie,formKind)
            if len(formTag):
                xSlug = slugify(unicode('%s' % (formTag)))
                xTag=add_tag(formTag,xSlug)
                movie.tags.add(xTag)
                movie.save()
        else:
            print("UNKNOWN FILE SKIPPING %s extension %s " % (theFile,extension))


