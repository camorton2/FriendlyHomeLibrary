# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.views.generic import View

from FHLBuilder.models import Song, Movie
from FHLBuilder.utility import link_file_list 
from FHLBuilder.query import findSongs, findMovies

from FHLReader import kodi
from FHLReader import forms
from FHLReader import query

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

class UserChannels(View):
    template_name = 'FHLReader/channels_page.html'
    def get(self, request):
        return render(request,self.template_name)


class RandomList(View):
    template_name = 'FHLReader/random_select.html'
    form_class=forms.RandomForm
    def get(self, request):
        context = {'form':self.form_class()}
        return render(request,self.template_name,context)
    
    def post(self,request):
        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            count = bound_form.cleaned_data['count'];
            kind = bound_form.cleaned_data['kind'];
            tag = bound_form.cleaned_data['tag'];                
            print('Valid form count %d kind %s tag %s' % (count,kind,tag))
            rlist = query.random_select(count,kind,tag)
        context = {'form':bound_form,'rlist':rlist}
        
        return render(request,self.template_name,context)
        
        
