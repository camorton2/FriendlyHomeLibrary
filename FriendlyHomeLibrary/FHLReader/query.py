# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from django.utils.text import slugify

from FHLBuilder import models as bmod
from FHLBuilder import choices

from FriendlyHomeLibrary import settings


def find_objects(me, targetList):
    """
    find all members of list marked as liked or loved by me
    """
    likedlist = []
    lovedlist = []
    for obj in targetList:
        if obj.likes and obj.likes.filter(username=me):
            likedlist.append(obj)
        if obj.loves and obj.loves.filter(username=me):
            lovedlist.append(obj)
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
        return bmod.Movie.objects.filter(fileKind=kind)
    if kind == choices.SONG:
        return bmod.Song.objects.all()
    if kind == choices.PICTURE:
        return bmod.Picture.objects.all()
    return CommonFile.objects.none()
    

def random_select(count, kind, tag):
    """
    Find a list of count random objects (or all if there are less than count)
    with matching kind and tag
    """
    # begin empty
    mylist = bmod.CommonFile.objects.none()
    if len(tag):
        # get this tag
        tSlug = slugify(unicode('%s' % (tag)))
        try:
            target = bmod.Tag.objects.get(slug__iexact=tSlug)
            mylist = kind_from_tag(kind,target)
        except bmod.Tag.DoesNotExist:
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
    
    
    
