# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from django.utils.text import slugify

from FHLBuilder import models as bmod
from FHLBuilder import choices

from FriendlyHomeLibrary import settings

def findSongs(me):
    #print("FindLikedSongs %s" % user)
    likedlist = []
    lovedlist = []
    for song in bmod.Song.objects.all():
        #print("checking song %s" % (song.title))
        if song.likes:
            list = song.likes.filter(username=me)
            if list:
                #print("like song: %s" % song.title)
                likedlist.append(song)
        if song.loves:
            list1 = song.loves.filter(username=me)
            if list1:
                #print("love song: %s" % song.title)
                lovedlist.append(song)
    #for a in lovedlist:
    #    print("loved found %s" % a.title)
    return likedlist,lovedlist

def findVideos(me):
    #print("FindLikedSongs %s" % user)
    likedlist = []
    lovedlist = []
    for movie in bmod.Movie.objects.all():
        #print("checking movie %s" % (movie.title))
        if movie.likes:
            list = movie.likes.filter(username=me)
            if list:
                print("like movie: %s" % movie.title)
                likedlist.append(movie)
        if movie.loves:
            list1 = movie.loves.filter(username=me)
            if list1:
                print("love movie: %s" % movie.title)
                lovedlist.append(movie)
    return likedlist,lovedlist


def kind_from_tag(akind, tagobj):
    """
    given a tag, find all objects matching kind
    """
    kind = akind[0]
    if kind in choices.videos:
        return tagobj.movie_tags.filter(fileKind=kind)
    if kind == choices.SONG:
        return tagobj.song_tags.all()
    if kind == choices.PICTURE:
        return tagobj.picture_tags.all()
    return CommonFile.objects.none()
    
    
def kind_from_all(akind):
    """
    given a kind, find all objects in the database matching that kind
    """
    kind = akind[0]
    if kind in choices.videos:
        return models.Movie.objects.filter(fileKind=kind)
    if kind == choices.SONG:
        return models.Song.objects.all()
    if kind == choices.PICTURE:
        return models.Picture.objects.all()
    return CommonFile.objects.none()
    

def random_select(count, kind, tag):
    """
    Find a list of count random objects (or all if there are less than count)
    with matching kind and tag
    """
    # begin empty
    mylist = models.CommonFile.objects.none()
    if len(tag):
        # get this tag
        tSlug = slugify(unicode('%s' % (tag)))
        try:
            target = models.Tag.objects.get(slug__iexact=tSlug)
            mylist = kind_from_tag(kind,target)
        except models.Tag.DoesNotExist:
            return mylist
    else:
        mylist = kind_from_all(kind)
        
    mysize = mylist.count()
    if mysize <= count:
        return mylist
    
    rand_entities = random.sample( range(mysize), count)
    print(mysize)
    print(rand_entities)
    flist = []
    for ind in rand_entities:
        flist.append(mylist[ind])
    return flist
    
    
    
