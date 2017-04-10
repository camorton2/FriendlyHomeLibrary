# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import Song, Movie

def findSongs(me):
    #print("FindLikedSongs %s" % user)
    likedlist = []
    lovedlist = []
    for song in Song.objects.all():
        #print("checking song %s" % (song.title))
        if song.likes:
            list = song.likes.filter(username=me)
            if list:
                print("like song: %s" % song.title)
                likedlist.append(song)
            list1 = song.loves.filter(username=me)
            if list1:
                print("love song: %s" % song.title)
                lovedlist.append(song)
    #for a in lovedlist:
    #    print("loved found %s" % a.title)
    return likedlist,lovedlist

def findMovies(me):
    #print("FindLikedSongs %s" % user)
    likedlist = []
    lovedlist = []
    for movie in Movie.objects.all():
        #print("checking movie %s" % (movie.title))
        if movie.likes.count():
            list = movie.likes.filter(username=me)
            if list:
                print("like movie: %s" % movie.title)
                likedlist.append(movie)
            list1 = movie.loves.filter(username=me)
            if list1:
                print("love movie: %s" % movie.title)
                lovedlist.append(movie)
    return likedlist,lovedlist
