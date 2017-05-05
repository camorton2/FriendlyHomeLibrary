# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.core.cache import cache

from FHLBuilder import choices
from FHLBuilder.models import Song, Movie, Picture

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
            likedS,lovedS = rq.find_objects(me, Song.objects.all())
            mycache.cache_my_songs(likedS,lovedS)
        if 'my-videos' in request.GET:
            likedV,lovedV = rq.find_objects(me, Movie.objects.all())
            mycache.cache_my_videos(likedV,lovedV)
        if 'my-pictures' in request.GET:
            likedP,lovedP = rq.find_objects(me, Picture.objects.all())
            mycache.cache_my_pictures(likedP,lovedP)
        
        context = {
            'me': me,
            'mySongs': mycache.has_my_songs(),
            'myVideos': mycache.has_my_videos(),
            'myPictures': mycache.has_my_pictures()
            }
        return render(request,self.template_name,context)    


class UserSongList(View):
    def get(self,request,pref):
        me = User.objects.get(username=request.user)
        mycache = cu.MyCache(me)
        
        liked, loved = mycache.get_my_songs()
                                        
        if pref == 'liked':
            songs = liked
        elif pref == 'loved':
            songs = loved
        else:
            songs = []
            
        return vu.collection_view(request,
            songs,[],[],[],'My Songs', False)

class UserVideoList(View):
    def get(self,request,pref):
        me = User.objects.get(username=request.user)
        mycache = cu.MyCache(me)
        
        liked, loved = mycache.get_my_videos()
        
        if pref == 'liked':
            videos = liked
        elif pref == 'loved':
            videos = loved
        else:
            videos = []
            
        return vu.collection_view(request,
            [],[],videos,[],'My Videos', False)

class UserPictureList(View):
    
    def get(self,request, pref):
        me = User.objects.get(username=request.user)
        mycache = cu.MyCache(me)
        
        liked, loved = mycache.get_my_pictures()
        
        # join the pictures for a single slideshow
        #pictures = loved
        #pictures.append(liked)
        
        if pref == 'liked':
            pictures = liked
        elif pref == 'loved':
            pictures = loved
        else:
            pictures = []
            
        return vu.collection_view(request,
            [],pictures,[],[],'My Pictures', False)



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
            songs,pictures,videos,[],
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
        
        
