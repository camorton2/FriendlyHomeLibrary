# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from eyed3 import mp3,id3
#import enzyme
import exifread
import time

from django.utils.text import slugify

from FHLBuilder import utility,choices
from FHLBuilder import models as bmodels
from FHLReader import utility as rutils

def setFileKind(obj,kind):
    
    if kind == choices.UNKNOWN:
        # don't modify to unknown
        pass
    else:
        obj.fileKind=kind
        obj.save()
        

def add_collection(cAlbum, cSlug, cPath,cDrive,saveIt=True):
    
    try:
        dbobj = bmodels.Collection.objects.get(slug__iexact=cSlug)
        if dbobj.filePath != cPath:
            # create a new slug by adding -1
            fslug = slugify( unicode( '%s-%d' % (cSlug,1) ))
            return add_collection(cAlbum, fslug, cPath, cDrive, saveIt)
    except bmodels.Collection.DoesNotExist:
        utility.log("---> ADD Collection %s slug %s path %s" % (cAlbum,cSlug,cPath))
        path = unicode(cPath)
        album = unicode(cAlbum)
        dbobj = bmodels.Collection(filePath=path,title=album,slug=cSlug,drive=cDrive)
        if saveIt:
            dbobj.save()
    return dbobj

def add_song(sTitle, sFileName, sSlug, sCollection):
    
    try:
        dbobj = bmodels.Song.objects.get(slug__iexact=sSlug)
    except bmodels.Song.DoesNotExist:
        utility.log("---> ADD Song slug %s: " % (sSlug))
        sCollection.save()
        title = unicode(sTitle)
        fileName = unicode(sFileName)
        dbobj = bmodels.Song(title=title,slug=sSlug,fileName=fileName, collection=sCollection)
        dbobj.save()
    dbobj.fileKind = choices.SONG
    dbobj.save()
    return dbobj

def add_movie(mTitle, mFileName, mSlug, mCollection, fKind=choices.MOVIE):
    try:
        dbobj = bmodels.Movie.objects.get(slug__iexact=mSlug)
    except bmodels.Movie.DoesNotExist:
        utility.log("---> ADD Movie slug %s: " % (mSlug))
        mCollection.save()
        title = unicode(mTitle)
        fileName = unicode(mFileName)
        dbobj = bmodels.Movie(title=title,slug=mSlug,fileName=fileName, collection=mCollection)
        dbobj.save()
    setFileKind(dbobj,fKind)
    dbobj.save()
    return dbobj

def add_picture(mTitle, mFileName, mSlug, mCollection):
    try:
        dbobj = bmodels.Picture.objects.get(slug__iexact=mSlug)
    except bmodels.Picture.DoesNotExist:
        utility.log("---> ADD Picture %s: " % (mSlug))
        mCollection.save()
        title = unicode(mTitle)
        fileName = unicode(mFileName)
        dbobj = bmodels.Picture(title=title,slug=mSlug,fileName=fileName, collection=mCollection)
        dbobj.save()
    dbobj.fileKind = choices.PICTURE
    dbobj.save()
    return dbobj

def add_musician(aName, aSlug):
    if aSlug == 'unknown-mus':
        raise rutils.MyException('No Way - no unknown musicians')
    if aSlug == 'unknown-artist-mus':
        raise rutils.MyException('No Way - no unknown-artist musicians')
        
    try:
        dbobj = bmodels.Musician.objects.get(slug__iexact=aSlug)
    except bmodels.Musician.DoesNotExist:
        utility.log("---> ADD Musician %s, slug %s" % (aName, aSlug))
        for b in bmodels.Musician.objects.all():
            if utility.slugCompare(aSlug,b.slug):
                return b
        name = unicode(aName)
        dbobj = bmodels.Musician(fullName=name,slug=aSlug)
        dbobj.save()
    return dbobj

def add_actor(aName, aSlug):
    try:
        dbobj = bmodels.Actor.objects.get(slug__iexact=aSlug)
    except bmodels.Actor.DoesNotExist:
        # print("---> ADD Actor %s, slug %s" % (aName, aSlug))
        name = unicode(aName)
        dbobj = bmodels.Actor(fullName=name,slug=aSlug)
        dbobj.save()
    return dbobj

def add_director(aName, aSlug):
    try:
        dbobj = bmodels.Director.objects.get(slug__iexact=aSlug)
    except bmodels.Director.DoesNotExist:
        # print("---> ADD Director %s, slug %s" % (aName, aSlug))
        name = unicode(aName)
        dbobj = bmodels.Director(fullName=name,slug=aSlug)
        dbobj.save()
    return dbobj

def add_tag(tName, tSlug):
    try:
        dbobj = bmodels.Tag.objects.get(slug__iexact=tSlug)
    except bmodels.Tag.DoesNotExist:
        # print("---> ADD Tag %s, slug %s" % (tName, tSlug))
        name = unicode(tName)
        dbobj = bmodels.Tag(name=name,slug=tSlug)
        dbobj.save()
    return dbobj


def as_picture(ext):
    if any(k == ext.lower() for k in choices.picts):
        return True
    return False

def as_movie(ext):
    if any(k == ext.lower() for k in choices.movs):
        return True
    return False


def pick_artist(path):
    # print('pick an artist from %s %s' % (path,path[:5]))
    first,_,album = path.rpartition('/')
    # print('first %s album %s' % (first,album))
    first,_,artist = first.rpartition('/')
    # print('first %s artist %s' % (first,artist))
    if artist:
        return artist
    # this will blow up
    return 'unknown'

def fix_song(song,theFile,collection):
    """
    Given a song, file and collection, attempt to get
    album,title,artist,genre information from the id3 tag
    to populate the database
    """
    tag = None
    try:
        tag = id3.Tag()
        tag.parse(theFile)
    except IOError:
        # id3 library has an issue with ? so just give up
        return None
    except Exception as ex:
        utility.log("ERROR (idetag) %s unhandled exception %s" % (theFile,type(ex).__name__))
        return None
            
    if tag is None:
        # pick some reasonable defaults
        myArtist = pick_artist(collection.filePath)
        title = song.title
    else:
        myArtist = unicode(tag.artist)
        if myArtist is None :
            #myArtist = u'various'
            myArtist = pick_artist(collection.filePath)
        elif myArtist == 'unknown':
            myArtist = pick_artist(collection.filePath)
        elif myArtist == 'Unknown':
            myArtist = pick_artist(collection.filePath)
        elif myArtist == 'Unknown Artist':
            myArtist = pick_artist(collection.filePath)
        
        title = unicode(tag.title)
        if title is None:
            title=song.title
        elif title == 'None':
            title=song.title
            
        album = tag.album
        if album is None:
            pass
        elif album == 'None':
            pass
        else:
            collection.title = album
            
    t1, _ = tag.track_num
    if t1 is None:
        t1=0
    song.track = t1
    
    # musician has name, slug
    artistSlug = slugify( unicode('%s%s' % (myArtist,'-mus')))
    
    musician = add_musician(aName=myArtist, aSlug=artistSlug)
    musician.albums.add(collection)
    musician.songs.add(song)
    musician.save()
    
    #print('musician %s collection %s' % (musician.fullName,collection.title))
    
    genre = tag.genre
    if genre is None:
        pass
    elif genre.name == 'None':
        pass
    elif genre.name == 'Unknown':
        pass
    elif genre.name == 'unknown':
        pass        
    elif genre.name == '<not-set>':
        pass                
    else:
        genreSlug = slugify(unicode('%s' % (genre.name)))
        gen = add_tag(unicode(genre.name),genreSlug)
        song.tags.add(gen)

    return musician

def add_file(root,myfile,path,newCollection,formKind,formTag):
    """
    passed the root, file, path from an os walk
    newCollection was created to hold the new database object
    formKind, formTag are from the create collections form
    returns musician (null unless it was found for a song) to allow redirect if appropriate
    """
    
    musician = None

    theFile = unicode(os.path.join(root,myfile))
    try:
        statinfo = os.stat(theFile)
    except Exception as ex:
        # in this case I want to see what the exception is, but the file is ok and
        # will not be ignored
        utility.log("SKIP (os.stat) %s unhandled exception %s" % (theFile,type(ex).__name__))
        return musician
    if not statinfo.st_size:
        utility.log("SKIP file with 0 size %s" % theFile)
        return musician
    base = unicode(os.path.basename(theFile))
    mTitle, extension = os.path.splitext(base)
    mTitle = unicode(mTitle)
    extension = unicode(extension)
    adate = time.gmtime(os.path.getmtime(theFile))
    fdate = time.strftime('%Y-%m-%d',adate)

    if mp3.isMp3File(theFile):
        nc = newCollection
        sSlug = slugify( unicode('%s%s-sg' % (nc.slug,mTitle)))            
        song = add_song(mTitle,base,sSlug,nc)
        song.date_added = fdate

        if len(formTag):
            xSlug = slugify(unicode('%s' % (formTag)))
            xTag=add_tag(formTag,xSlug)
            song.tags.add(xTag)

        # fill in extra details from the id3 tag on file if possible
        musician = fix_song(song,theFile,nc)
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
            mSlug = slugify( unicode('%s%s-mv' % (nc.slug,mTitle)))            
            movie = add_movie(mTitle,base,mSlug,nc,formKind)
            movie.date_added = fdate
            
            if len(formTag):
                xSlug = slugify(unicode('%s' % (formTag)))
                xTag=add_tag(formTag,xSlug)
                movie.tags.add(xTag)
                
            movie.save()
        elif as_picture(extension):
            mSlug = slugify( unicode('%s%s-pict' % (nc.slug,mTitle)))
            picture = add_picture(mTitle,base,mSlug,nc)
            picture.date_added = fdate
            picture.save()
            
            # supposed to be faster with details=False
            #itags = exifread.process_file(theFile, details=False)
            fname = unicode(theFile)
            try:
                #print("before open file open file %s" % fname)
                with open(fname,'r') as f:
                    #print("file open ok now get info")
                    itags = exifread.process_file(f,details=False)
                    #print("got info %s " % fname)
                    #print (itags)
                    #print tag['Image DateTime']
                    for tag in itags:
                        if tag in 'Image DateTime':
                            value = itags[tag]
                            picture.data1 = value
                            try:
                                picture.year = int(value[:4])
                            except ValueError:
                                # if its not a number just
                                # don't set the year
                                pass
                        if tag in 'EXIF DateTimeOriginal':
                            value = itags[tag]
                            picture.data2 = value
                            #print("2 %s" % value)
                        if tag in 'EXIF DateTimeDigitized':
                            value = itags[tag]
                            #print("3 %s" % value)
                            picture.data3 = value
                    picture.save()
            except NameError:
                #print("ERROR (opening for info) NameError file %s" % fname)
                # this is ok, file is OK just ignore the info
                pass
            except Exception as ex:
                # in this case I want to see what the exception is, but the file is ok and
                # will not be ignored
                utility.log("ERROR (opening for info) %s unhandled exception %s" % (fname,type(ex).__name__))

            if len(formTag):
                xSlug = slugify(unicode('%s' % (formTag)))
                xTag=add_tag(formTag,xSlug)
                picture.tags.add(xTag)
                
            picture.save()
        else:
            utility.log("SKIPPING - unhandled extension %s/%s" % (path,base))
    return musician


def remove_movie(target):
    # concert_musicians,movie_directors,movie_actors
    
    for mus in target.concert_musicians.all():
        target.concert_musicians.remove(mus)
    for dtor in target.movie_directors.all():
        target.movie_directors.remove(dtor)
    for act in target.movie_actors.all():
        target.movie_actors.remove(act)
    for lk in target.likes.all():
        target.likes.remove(lk)
    for lv in target.loves.all():
        target.loves.remove(lv)
    for tg in target.tags.all():
        target.tags.remove(tg)
    for dl in target.dislikes.all():
        target.dislikes.remove(dl)        
    target.delete()


def remove_picture(target):
    for lk in target.likes.all():
        target.likes.remove(lk)
    for lv in target.loves.all():
        target.loves.remove(lv)
    for tg in target.tags.all():
        target.tags.remove(tg)
    for dl in target.dislikes.all():
        target.dislikes.remove(dl)        
    target.delete()


def remove_song(target):
    #print('remove song %s' % (target.title))
    for m in target.song_musicians.all():
        target.song_musicians.remove(m)
    for lk in target.likes.all():
        target.likes.remove(lk)
    for lv in target.loves.all():
        target.loves.remove(lv)
    for dl in target.dislikes.all():
        target.dislikes.remove(dl)        
    for tg in target.tags.all():
        target.tags.remove(tg)
    target.delete()
    
    
def remove_collection(target):
    # movies, games,books,pictures,songs,chapters
    for mv in target.movies.all():
        remove_movie(mv)
    for pc in target.pictures.all():
        remove_picture(pc)
    for sg in target.songs.all():
        remove_song(sg)
    if target.games.all():
        raise rutils.MyException('No Way - games are not implemented')
    if target.books.all():
        raise rutils.MyException('No Way - books are not implemented')
    if target.chapters.all():
        raise rutils.MyException('No Way - chapters are not implemented')
    target.delete()


def remove_musician(target):
    #print('remove musician %s' % (target.fullName))
    for sg in target.songs.all():
        remove_song(sg)
    for con in target.concerts.all():
        # do not remove the concert, just remove the musician
        con.concert_musicians.remove(target)
    for col in target.albums.all():
        remove_collection(col)
    target.delete()
    

def remove_actor(target):
    for mv in target.movies.all():
        # do not remove the movie, just remove the actor
        mv.movie_actors.remove(target)
    target.delete()
    

def remove_director(target):
    for mv in target.movies.all():
        # do not remove the movie, just remove the director
        mv.movie_directors.remove(target)
    target.delete()
    

def remove_tag(target):
    for mv in target.movie_tags.all():
        # do not remove the movie, just remove the tag
        mv.tags.remove(target)
    for sg in target.song_tags.all():
        sg.tags.remove(target)
    for pt in target.picture_tags.all():
        pt.tags.remove(target)
    target.delete()

