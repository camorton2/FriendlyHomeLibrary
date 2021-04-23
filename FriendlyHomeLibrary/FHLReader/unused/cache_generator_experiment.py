# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import string

from django.contrib.auth.models import User
from django.urls import reverse
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
        self.likedS = ('likedS-%s' % self.me)
        self.lovedS = ('lovedS-%s' % self.me)
        self.likedV = ('likedV-%s' % self.me)
        self.lovedV = ('lovedV-%s' % self.me)
        self.likedP = ('likedP-%s' % self.me)
        self.lovedP = ('lovedP-%s' % self.me)
        
        self.pnext = ('pnext-%s' % self.me)
        self.pprev = ('pprev-%s' % self.me)
        self.pindex = ('pindex-%s' % self.me)
        self.pgenset = ('pgenset-%s' % self.me)


    def setup_generator(self,pictures):
        """
        setup foward/backwards generator pictures
        """
        cache.set(self.pnext,self.forwards_generator(pictures))
        cache.set(self.pprev,self.backwards_generator(pictures))
        cache.set(self.pindex,len(pictures))
        cache.set(self.pgenset,True)


    def clear_generator(self):
        """
        reset
        """
        cache.set(self.pgenset,False)

    def has_generator(self):
        return cache.get(self.pgenset)
        
    def cache_next(self):
        cache.get(self.pnext).next()
        
    def cach_prev(self):
        cache.get(self.pprev).next()

    def backwards_generator(self,pictures):
        """
        move fowards or backwards through pictures
        using the cached index
        """
        while True:
            count = len(pictures)
            if self.pindex == 1:
                self.pindex = count
            else:
                self.pindex = self.pindex-1
            pictureList = utility.link_file_list(pictures)
            yield pictureList[self.pindex]
        

    def forwards_generator(self,pictures):
        """
        move fowards or backwards through pictures
        using the cached index
        """
        while True:
            count = len(pictures)        
            if self.pindex==count:
                self.pindex = 1
            else:
                self.pindex = self.pindex+1
            pictureList = utility.link_file_list(pictures)
            yield pictureList[self.pindex]


    def cache_query(self,songs,pictures,videos,channel):
        """
        cache the results of a given query
        """
        cache.set(self.songs, songs)
        cache.set(self.pictures, pictures)
        cache.set(self.videos, videos)
        cache.set(self.channel, channel)


    def cache_my_songs(self,liked, loved):
        """ cache the results of the liked/loved songs query """
        cache.set(self.likedS, liked)
        cache.set(self.lovedS, loved)


    def cache_my_videos(self,liked, loved):
        """ cache the results of the liked/loved videos query """
        cache.set(self.likedV, liked)
        cache.set(self.lovedV, loved)


    def cache_my_pictures(self,liked, loved):
        """ cache the results of the liked/loved pictures query """
        cache.set(self.likedP, liked)
        cache.set(self.lovedP, loved)

    def has_my_songs(self):
        """ determine if the liked/loved songs query is in cache """
        return self.likedS in cache or self.lovedS in cache

    def has_my_videos(self):
        """ determine if the liked/loved videos query is in the cache """
        return self.likedV in cache or self.lovedV in cache

    def has_my_pictures(self):
        """ determine if the liked/loved pictures query is in the cache """
        return self.likedP in cache or self.lovedP in cache


    def get_my_songs(self):
        """ return the cached result from the liked/loved songs query """
        liked = []
        loved = []
        if self.likedS in cache:
            liked = cache.get(self.likedS)
        if self.lovedS in cache:
            loved = cache.get(self.lovedS)
        return liked,loved

    def get_my_videos(self):
        """ return the cached result of the liked/loved videos query """
        liked = []
        loved = []
        if self.likedV in cache:
            liked = cache.get(self.likedV)
        if self.lovedV in cache:
            loved = cache.get(self.lovedV)
        return liked,loved

    def get_my_pictures(self):
        """ return the cached result of the liked/loved pictures query """
        liked = []
        loved = []
        if self.likedP in cache:
            liked = cache.get(self.likedP)
        if self.lovedP in cache:
            loved = cache.get(self.lovedP)
        return liked,loved

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
        return songs,pictures,videos,channel


    def clear_query(self):
        """ clear the currently cached query """
        cache.set(self.songs,[])
        cache.set(self.videos,[])
        cache.set(self.pictures,[])
        cache.set(self.channel,[])


    def clear_me(self):
        """ clear the liked/loved queries from the cache """
        cache.set(self.likedS,[])
        cache.set(self.lovedS,[])
        cache.set(self.likedV,[])
        cache.set(self.lovedV,[])
        cache.set(self.lovedP,[])
        cache.set(self.likedP,[])


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
    #return redirect(reverse('cached_list'))


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
    #return redirect(reverse('cached_list'))

