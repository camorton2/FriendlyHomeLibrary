# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.core.cache import cache

from FHLBuilder import choices
from FHLBuilder.models import Song, Movie

import FHLBuilder.view_utility as vu
import FHLBuilder.query as bq
import FHLBuilder.utility as bu

from FHLReader import kodi
from FHLReader import forms
from FHLReader import query

import FHLReader.cache_utility as cu
import FHLReader.query as rq

# Create your views here.

class UserDetail(View):
    template_name = 'FHLReader/user_page.html'
    def get(self, request):
        print("UserDetail GET")
        me = User.objects.get(username=request.user)
        mycache = cu.MyCache(me)
                
        if 'my-songs' in request.GET:
            # Do the query, cache results
            likedS,lovedS = rq.findSongs(me)
            mycache.cache_my_songs(likedS,lovedS)
            mySongs = True
        if 'my-videos' in request.GET:
            # Do the query, cache results
            likedV,lovedV = rq.findVideos(me)
            mycache.cache_my_videos(likedV,lovedV)
            myMovies = True

        likedS,lovedS = mycache.get_my_songs()
        mySongs = likedS or lovedS
               
        likedV,lovedV = mycache.get_my_videos()
        myVideos = likedV or lovedV
        
        context = {
            'me': me,
            'mySongs': mySongs,
            'myVideos': myVideos
            }
        return render(request,self.template_name,context)    


class UserSongList(View):
    template_name='FHLReader/user_songs.html'

    def get(self,request):
        me = User.objects.get(username=request.user)
        mycache = cu.MyCache(me)
        
        # in this case chose playlist by default
        playlist = True
        # print("UserSongList GET")
        if 'filelist' in request.GET:
            playlist=False
        
        liked, loved = mycache.get_my_songs()
                                        
        likedList = bu.link_file_list(liked)
        lovedList = bu.link_file_list(loved)
            
        context = {
            'lovedList':lovedList,
            'likedList':likedList,
            'asPlayList':playlist
            }            
            
        return render(request,self.template_name,context)

# movies
class UserVideoList(View):
    template_name='FHLReader/user_videos.html'
    def get(self,request):
        me = User.objects.get(username=request.user)
        mycache = cu.MyCache(me)
        
        liked, loved = mycache.get_my_videos()
                        
        #likedList = bu.link_file_list(liked)
        #lovedList = bu.link_file_list(loved)
            
        context = {
            'lovedList': loved,
            'likedList': liked,
            }            
            
        return render(request,self.template_name,context)

class UserChannels(View):
    template_name = 'FHLReader/channels_page.html'
    def get(self, request):
        return render(request,self.template_name)

class CachedFileList(View):
    """
    CachedView will display the cached QuerySet from the
    view that requested this view
    the cached kind will hold the kind information for the QuerySet
    and the cached title will hold the title to describe the
    cached list
    """        
    def get(self,request):
        print("CachedFileList GET")
        me = User.objects.get(username=request.user)
        mycache = cu.MyCache(me)
                
        songs, pictures, videos,channel = mycache.get_query()
        
        return vu.collection_view(request,
            songs,pictures,videos,
            'Saved Collection',
            False)
             

class RandomList(View):
    template_name = 'FHLReader/random_select.html'
    form_class=forms.RandomForm
    
    def get(self, request):
        print("RandomList GET")
        context = {'form':self.form_class()}
        return render(request,self.template_name,context)                
        
    def post(self, request):
        print("RandomList POST")
        me = User.objects.get(username=request.user)
        mycache = cu.MyCache(me)
        
        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            count = bound_form.cleaned_data['count'];
            kind = bound_form.cleaned_data['kind'];
            tag = bound_form.cleaned_data['tag'];                
            print('Valid form count %d kind %s tag %s' % (count,kind,tag))
            rlist = rq.random_select(count,kind,tag)
            if 'save-query' in request.POST:
                # cache the query results and redirect to the cache-display
                return cu.cache_list_bykind(rlist,kind,'random_list',mycache)
        # display the list as files with the form    
        context = {'form':bound_form,'rlist':rlist}
        return render(request,self.template_name,context)
        
        
