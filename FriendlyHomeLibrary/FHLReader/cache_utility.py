# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import string

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.text import slugify
from django.template import RequestContext,loader
from django.views.generic import View
from django.core.cache import cache

from FriendlyHomeLibrary import settings

from FHLUser.decorators import require_authenticated_permission

from FHLBuilder import models
from FHLBuilder import collection
from FHLBuilder import choices
from FHLBuilder import utility
from FHLBuilder import query


class MyCache:
    def __init__(self,me):
        self.me = me
        self.songs = ('songs-%s',me)
        self.videos = ('videos-%s',me)
        self.pictures = ('pictures-%s',me)
        self.channel = ('channel-%s',me)
        self.likedS = ('likedS-%s' % me)
        self.lovedS = ('lovedS-%s' % me)
        self.likedV = ('likedV-%s' % me)
        self.lovedV = ('lovedV-%s' % me)
        self.likedP = ('likedP-%s' % me)
        self.lovedP = ('lovedP-%s' % me)
        

    def cache_query(self,songs,pictures,videos,channel):
        cache.set(self.songs, songs)
        cache.set(self.pictures, pictures)
        cache.set(self.videos, videos)
        cache.set(self.channel, channel)

    def cache_my_songs(self,liked, loved):
        cache.set(self.likedS, liked)
        cache.set(self.lovedS, loved)

    def cache_my_videos(self,liked, loved):
        cache.set(self.likedV, liked)
        cache.set(self.lovedV, loved)

    def cache_my_pictures(self,liked, loved):
        cache.set(self.likedP, liked)
        cache.set(self.lovedP, loved)

    def has_my_songs(self):
        return self.likedS in cache or self.lovedS in cache

    def has_my_videos(self):
        return self.likedV in cache or self.lovedV in cache

    def has_my_pictures(self):
        return self.likedP in cache or self.lovedP in cache


    def get_my_songs(self):
        liked = []
        loved = []
        if self.likedS in cache:
            liked = cache.get(self.likedS)
        if self.lovedS in cache:
            loved = cache.get(self.lovedS)
        return liked,loved

    def get_my_videos(self):
        liked = []
        loved = []
        if self.likedV in cache:
            liked = cache.get(self.likedV)
        if self.lovedV in cache:
            loved = cache.get(self.lovedV)
        return liked,loved

    def get_my_pictures(self):
        liked = []
        loved = []
        if self.likedP in cache:
            liked = cache.get(self.likedP)
        if self.lovedP in cache:
            loved = cache.get(self.lovedP)
        return liked,loved

    def get_query(self):
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
        cache.set(self.songs,[])
        cache.set(self.videos,[])
        cache.set(self.pictures,[])
        cache.set(self.channel,[])

    def clear_me(self):
        cache.set(self.likedS,[])
        cache.set(self.lovedS,[])
        cache.set(self.likedV,[])
        cache.set(self.lovedV,[])



def cache_list_bykind(rlist,kind,channel,mycache):
    """
    cache the given list according to its kind
    cache the channel that provided the list
    redirect to the cache-list display page
    """

    songs = []
    videos = []
    pictures = []

    if kind[0] == choices.SONG:
        songs = rlist
    elif kind[0] == choices.PICTURE:
        pictures = rlist
    elif kind[0] in choices.videos:
        videos = rlist

    mycache.cache_query(songs,pictures,videos,channel)
    return redirect(reverse('cached_list'))


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
        elif kind[0] == choices.PICTURE:
            pictures.append(obj)
        elif kind[0] in choices.videos:
            videos.append(obj)

    mycache.cache_query(songs,pictures,videos,channel)
    return redirect(reverse('cached_list'))

