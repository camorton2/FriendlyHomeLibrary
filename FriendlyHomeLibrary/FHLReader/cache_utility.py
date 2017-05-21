# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import string

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.cache import cache

from FriendlyHomeLibrary import settings

from FHLBuilder import models
from FHLBuilder import collection
from FHLBuilder import choices
from FHLBuilder import utility
from FHLBuilder import query


class MyCache:
    """
    class holds all interaction with the cache
    """
    def __init__(self,me):
        self.me = me.username
        self.songs = ('songs-%s' % self.me)
        self.videos = ('videos-%s' % self.me)
        self.pictures = ('pictures-%s' % self.me)
        self.channel = ('channel-%s' % self.me)
        

    def cache_query(self,songs,pictures,videos,channel):
        """
        cache the results of a given query
        """

        cache.set(self.songs, songs)
        cache.set(self.pictures, pictures)
        cache.set(self.videos, videos)
        cache.set(self.channel, channel)


    def get_query(self):
        """ get the cached result of the most recent query """
        songs = []
        videos = []
        pictures = []
        channel = None
        if self.songs in cache:
            songs = cache.get(self.songs)
        if self.videos in cache:
            videos = cache.get(self.videos)
        if self.pictures in cache:
            pictures = cache.get(self.pictures)
        if self.channel in cache:
            channel = cache.get(self.channel)
            
        print('cache get songs %s videos %d pictures %d' % (len(songs),len(videos),len(pictures)))
        return songs,pictures,videos,channel


    def clear_query(self):
        """ clear the currently cached query """
        cache.set(self.songs,[])
        cache.set(self.videos,[])
        cache.set(self.pictures,[])
        cache.set(self.channel,[])


def cache_list_bykind(rlist,kind,channel,mycache):
    """
    cache the given list according to its kind
    cache the channel that provided the list
    redirect to the cache-list display page
    """

    print('cache by kind %s' % kind)

    songs = []
    videos = []
    pictures = []

    if kind == choices.SONG:
        songs = rlist
    elif kind == choices.PICTURE:
        pictures = rlist
    elif kind in choices.videos:
        videos = rlist
    else:
        print('ERROR no kind selected %s' % kind)

    mycache.cache_query(songs,pictures,videos,channel)


def cache_list(rlist,channel,mycache):
    """
    cache the given list of objects
    cache the channel that provided the list
    redirect to the cache-list display page
    """

    songs = []
    pictures = []
    videos = []

    for obj in rlist:
        if obj.fileKind[0] == choices.SONG:
            songs.append(obj)
        elif obj.fileKind[0] == choices.PICTURE:
            pictures.append(obj)
        elif obj.fileKind in choices.videos:
            videos.append(obj)

    mycache.cache_query(songs,pictures,videos,channel)

