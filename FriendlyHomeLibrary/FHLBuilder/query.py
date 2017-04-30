# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from FHLBuilder.models import Song, Movie
from FHLBuilder import choices

from FriendlyHomeLibrary import settings

def my_preference(obj,me):
    if obj.loves.filter(username=me):
        print("select love")
        return True,False,False
    if obj.likes.filter(username=me):
        print("select like")
        return False,True,False
    if obj.dislikes.filter(username=me):
        print("select dislike")
        return False,False,True
    return False,False,False


def handle_pref(obj,pref,me):
    love,like,dislike = my_preference(obj,me)
    if pref == 'liked':
        obj.likes.add(me)
        obj.loves.remove(me)
        obj.dislikes.remove(me)
    elif pref == 'loved':
        obj.loves.add(me)
        obj.likes.remove(me)
        obj.dislikes.remove(me)
    elif pref == 'disliked':
        obj.dislikes.add(me)
        obj.loves.remove(me)
        obj.likes.remove(me)
    obj.save()


def handle_collection_kind(collections, kind):
    """
    In queryset collections create a list of collections 
    containing files of kind
    """
    clist = []    
    vt = kind in choices.videos
    st = kind == choices.SONG
    pt = kind == choices.PICTURE
    for current in collections:
        if vt and current.movie_set.filter(fileKind=kind):
            clist.append(current)
        elif st and current.song_set.count():
            clist.append(current)
        elif pt and current.picture_set.count():
            clist.append(current)
    return clist


def next_group(pictures):
    """
    My first generator will iterate through a picture list in
    sections according to the length in settings
    """
    first = 0
    last = 0
    limit = len(pictures)
    for ctr in range(limit):
        con = ctr % settings.PHOTO_LIST_LENGTH
        if ctr and not con:
            last = ctr
            yield pictures[first:last]
            first = ctr
    yield pictures[first:limit]
