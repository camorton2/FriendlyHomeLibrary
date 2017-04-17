# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from eyed3 import mp3,id3
import enzyme
import exifread

from django.utils.text import slugify
from django.db import models

from FHLBuilder import utility,choices
from FHLBuilder import models as bmodels

def setFileKind(obj,kind):
    fKind = kind[0]
    #print("FileKind to %s %s" % (kind,fKind))
    if fKind == choices.UNKNOWN:
        # print("unknown")
        pass
    else:
        obj.fileKind = fKind
        obj.save()

def add_collection(cAlbum, cSlug, cPath,cDrive,saveIt=True):
    #print ("---> ADD Collection %s slug %s path %s" % (cAlbum,cSlug,cPath))
    try:
        dbobj = bmodels.Collection.objects.get(slug__iexact=cSlug)
    except bmodels.Collection.DoesNotExist:
        path = utility.to_str(cPath)
        album = utility.to_str(cAlbum)
        dbobj = bmodels.Collection(filePath=path,title=album,slug=cSlug,drive=cDrive)
        if saveIt:
            dbobj.save()
    return dbobj

def add_song(sTrack, sTitle, sFileName, sSlug, sCollection):
    #print ("---> ADD Song %s, track %s, filename %s, slug %s: " % (sTitle,sTrack,sFileName,sSlug))
    try:
        dbobj = bmodels.Song.objects.get(slug__iexact=sSlug)
    except bmodels.Song.DoesNotExist:
        sCollection.save()
        track = utility.to_str(sTrack)
        title = utility.to_str(sTitle)
        fileName = utility.to_str(sFileName)
        dbobj = bmodels.Song(track=track,title=title,slug=sSlug,fileName=fileName, collection=sCollection)
        dbobj.save()
    dbobj.fileKind = choices.SONG
    dbobj.save()
    return dbobj

def add_movie(mTitle, mFileName, mSlug, mCollection):
    #print ("---> ADD Movie %s, filename %s, slug %s: " % (mTitle,mFileName,mSlug))
    try:
        dbobj = bmodels.Movie.objects.get(slug__iexact=mSlug)
        #print ("SKIPPING - duplicate %s" % mSlug)
    except bmodels.Movie.DoesNotExist:
        mCollection.save()
        title = utility.to_str(mTitle)
        fileName = utility.to_str(mFileName)
        #print("CATH add movie %s to collection %s" % (mSlug,mCollection.slug))
        dbobj = bmodels.Movie(title=title,slug=mSlug,fileName=fileName, collection=mCollection)
        dbobj.save()
    dbobj.fileKind = choices.MOVIE
    dbobj.save()
    return dbobj

def add_picture(mTitle, mFileName, mSlug, mCollection):
    try:
        dbobj = bmodels.Picture.objects.get(slug__iexact=mSlug)
    except bmodels.Picture.DoesNotExist:
        mCollection.save()
        title = utility.to_str(mTitle)
        fileName = utility.to_str(mFileName)
        dbobj = bmodels.Picture(title=title,slug=mSlug,fileName=fileName, collection=mCollection)
        dbobj.save()
    dbobj.fileKind = choices.PICTURE
    dbobj.save()
    return dbobj

def add_musician(aName, aSlug):
    #print("---> ADD Musician %s, slug %s" % (aName, aSlug))
    try:
        dbobj = bmodels.Musician.objects.get(slug__iexact=aSlug)
    except bmodels.Musician.DoesNotExist:
        for b in bmodels.Musician.objects.all():
            if utility.slugCompare(aSlug,b.slug):
                return b
        name = utility.to_str(aName)
        dbobj = bmodels.Musician(fullName=name,slug=aSlug)
        dbobj.save()
    return dbobj

def add_actor(aName, aSlug):
    #print("---> ADD Actor %s, slug %s" % (aName, aSlug))
    try:
        dbobj = bmodels.Actor.objects.get(slug__iexact=aSlug)
    except bmodels.Actor.DoesNotExist:
        name = utility.to_str(aName)
        dbobj = bmodels.Actor(fullName=name,slug=aSlug)
        dbobj.save()
    return dbobj

def add_director(aName, aSlug):
    #print("---> ADD Director %s, slug %s" % (aName, aSlug))
    try:
        dbobj = bmodels.Director.objects.get(slug__iexact=aSlug)
    except bmodels.Director.DoesNotExist:
        name = utility.to_str(aName)
        dbobj = bmodels.Director(fullName=name,slug=aSlug)
        dbobj.save()
    return dbobj

def add_tag(tName, tSlug):
    print("---> ADD Tag %s, slug %s" % (tName, tSlug))
    try:
        dbobj = bmodels.Tag.objects.get(slug__iexact=tSlug)
    except bmodels.Tag.DoesNotExist:
        name = utility.to_str(tName)
        dbobj = bmodels.Tag(name=name,slug=tSlug)
        dbobj.save()
    return dbobj

def as_picture(ext):
    if ext == '.jpg':
        return True
    if ext == '.JPG':
        return True
    if ext == '.img':
        return True
    if ext == '.IMG':
        return True
    if ext == '.png':
        return True
    if ext == '.PNG':
        return True
    if ext == '.THM':
        return True
    if ext == '.thm':
        return True
    if ext == '.tiff':
        return True
    if ext == '.tif':
        return True
    return False

def as_movie(ext):
    if ext == '.mkv':
        return True
    if ext == '.mov':
        return True
    if ext == '.MOV':
        return True
    if ext == '.mp4':
        return True
    if ext == '.avi':
        return True
    if ext == '.AVI':
        return True
    if ext == '.flv':
        return True
    if ext == '.wmv':
        return True
    if ext == '.mpg':
        return True
    if ext == '.VOB':
        return True
    return False

def add_file(root,myfile,path,newCollection,formKind,formTag):
    album = newCollection
    musician = None
    # Still to do: log messages
    theFile = os.path.join(root,myfile)
    try:
        statinfo = os.stat(theFile)
    except:
        print("SKIP error getting file stats %s" % theFile)
        return album, musician
    if not statinfo.st_size:
        print("SKIP file with 0 size %s" % theFile)
        return album, musician
    base = os.path.basename(theFile)
    mTitle, extension = os.path.splitext(base)

    if mp3.isMp3File(theFile):
        tag = id3.Tag()
        tag.parse(theFile)
        myArtist = tag.artist
        addC = False

        if myArtist is None :
            myArtist = 'various'
        title = tag.title
        if title is None:
            title=mTitle
        if tag.album is None:
            collection = newCollection
        else:
            addC = True
            # handle the collection (album) which only has a path and a name
            collectionSlug = slugify( unicode( '%s' % (tag.album) ))
            collection = add_collection(cAlbum=tag.album,
                cSlug=collectionSlug,cPath=path,
                cDrive=newCollection.drive)
            album = collection
            newCollection = collection
        # song has track, title, filename, slug, collection
        songSlug = slugify( unicode('%s%s' % (title,collection.slug)))
        t1, t2 = tag.track_num
        if t1 is None:
            t1=0
        song = add_song(sTrack=t1,sTitle=title, sFileName=myfile,
            sSlug=songSlug, sCollection=collection)
        # musician has name, slug
        artistSlug = slugify( unicode('%s%s' % (myArtist,'-mus')))

        musician = add_musician(aName=myArtist, aSlug=artistSlug)
        setFileKind(song, formKind)
        if len(formTag):
            xSlug = slugify(unicode('%s' % (formTag)))
            xTag=add_tag(formTag,xSlug)
            song.tags.add(xTag)

        if addC:
            musician.albums.add(collection)
        musician.songs.add(song)
        musician.save()

        genre = tag.genre
        if genre is not None:
            genreSlug = slugify(unicode('%s' % (genre.name)))
            gen = add_tag(genre.name,genreSlug)
            song.tags.add(gen)
        song.save()
    else:
        # This section is for the info on mkv files
        # currently not being used, but may be in future
        # in this section new movies will be added to the passed collection
        ## try:
        ##    with open(theFile,'rb') as f:
        ##        mkv = enzyme.MKV(f)
        ##        print (mkv)
        ##        print (type(mkv))
        ##    f.close()
        ##except enzyme.MalformedMKVError:
        ##    print("BOGUS MKV skip")

        nc = newCollection
        if as_movie(extension):
            mSlug = slugify( unicode('%s%s' % (nc.slug,mTitle)))
            movie = add_movie(mTitle,base,mSlug,nc)
            setFileKind(movie,formKind)
            if len(formTag):
                xSlug = slugify(unicode('%s' % (formTag)))
                xTag=add_tag(formTag,xSlug)
                movie.tags.add(xTag)
                movie.save()
        elif as_picture(extension):
            mSlug = slugify( unicode('%s%s-pict' % (nc.slug,mTitle)))
            #print("PICTURE %s album %s" % (mSlug,nc.slug))
            picture = add_picture(mTitle,base,mSlug,nc)
            # supposed to be faster with details=False
            #itags = exifread.process_file(theFile, details=False)
            itags = exifread.process_file(theFile)
            if len(formTag):
                xSlug = slugify(unicode('%s' % (formTag)))
                xTag=add_tag(formTag,xSlug)
                picture.tags.add(xTag)
                picture.save()
        else:
            print ("SKIPPING - unhandled extension %s/%s" % (path,base))

    return album,musician

