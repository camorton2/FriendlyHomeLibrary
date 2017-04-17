# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.views.generic import View

from FHLBuilder.models import Song, Movie
from FHLBuilder.utility import link_file_list 
from FHLBuilder.query import findSongs, findMovies

# Create your views here.

class UserDetail(View):
    template_name = 'FHLReader/user_page.html'
    def get(self, request):
        print("UserDetail GET")
        me = User.objects.get(username=request.user)
        context = {'me': me}
        return render(request,self.template_name,context)    

class UserSongList(View):
    template_name='FHLReader/user_songs.html'
    likedSongs = []
    lovedSongs = []

    def get(self,request):
        me = User.objects.get(username=request.user)
        playlist = True
        print("UserSongList GET")
        if 'filelist' in request.GET:
            playlist=False
        self.likedSongs,self.lovedSongs = findSongs(me)
        likedSongList = link_file_list(self.likedSongs)
        lovedSongList = link_file_list(self.lovedSongs)
            
        context = {
            'listTitle': "Songs I Love",
            'listTitle2': "Songs I Like",
            'songlist':lovedSongList,
            'songlist2':likedSongList,
            'asPlayList':playlist
            }            
            
        return render(request,self.template_name,context)

# movies
class UserMovieList(View):
    template_name='FHLReader/user_movies.html'
    def get(self,request):
        me = User.objects.get(username=request.user)
        likedMovies = []
        lovedMovies = []
        likedMovies,lovedMovies = findMovies(me)
        context = {
            'listTitle':"Movies I love",
            'movielist':lovedMovies,
            'listTitle2':"Movies I like",
            'movielist2':likedMovies
            }            
        return render(request,self.template_name,context)

