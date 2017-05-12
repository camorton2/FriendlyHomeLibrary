# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from FHLBuilder.models import Song, Movie, Collection
from FHLBuilder import choices

from FriendlyHomeLibrary import settings

def my_preference(obj,me):
    """
    Given an object and a user return a triple
    indicating loves,likes,dislikes
    """
    if obj.loves.filter(username=me):
        return True,False,False
    if obj.likes.filter(username=me):
        return False,True,False
    if obj.dislikes.filter(username=me):
        return False,False,True
    return False,False,False

def my_preference_dict(obj,me):
    """
    Given an object and a user return a triple
    indicating loves,likes,dislikes
    """
    if obj.loves.filter(username=me):
        return { 'pref': choices.LOVE }
    if obj.likes.filter(username=me):
        return { 'pref': choices.LIKE }
    if obj.dislikes.filter(username=me):
        return { 'pref': choices.DISLIKE }
    return { 'pref': choices.INDIFFERENT }


def handle_pref(obj,pref,me):
    love,like,dislike = my_preference(obj,me)
    if pref == choices.LIKE:
        print('like')
        obj.likes.add(me)
        obj.loves.remove(me)
        obj.dislikes.remove(me)
    elif pref == choices.LOVE:
        print('love')
        obj.loves.add(me)
        obj.likes.remove(me)
        obj.dislikes.remove(me)
    elif pref == choices.DISLIKE:
        obj.dislikes.add(me)
        obj.loves.remove(me)
        obj.likes.remove(me)
    elif pref == choices.INDIFFERENT:
        obj.loves.remove(me)
        obj.likes.remove(me)
        obj.dislikes.remove(me)
    obj.save()


def handle_collection_kind(kind):
    """
    In queryset collections create a list of collections 
    containing files of kind
    """
    if kind in choices.SONG:
        return Collection.objects.exclude(songs=None)
    if kind in choices.PICTURE:
        return Collection.objects.exclude(pictures=None)
    if kind in choices.videos:
        return Collection.objects.all().filter(
            movies__fileKind__contains=kind).distinct()
    return []

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
