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

from FHLReader import forms

import FHLReader.cache_utility as cu
import FHLReader.query as rq

# Create your views here.

class UserDetail(View):
    """
    User main page mostly to select playlists
    """
    template_name = 'FHLReader/user_page.html'
    def get(self, request):
        # print("UserDetail GET")
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
            'myPictures': mycache.has_my_pictures(),
            'choices': choices.VIDEO_CHOICES
            }
        return render(request,self.template_name,context)


class UserSongList(View):
    """
    Selection of liked and loved songs by user
    """
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
    """
    Selection of liked loved videos by user
    """
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
    """ selection of liked loved pictures by user """
    def get(self,request, pref):
        me = User.objects.get(username=request.user)
        mycache = cu.MyCache(me)

        liked, loved = mycache.get_my_pictures()

        if pref == 'liked':
            pictures = liked
        elif pref == 'loved':
            pictures = loved
        else:
            pictures = []

        return vu.collection_view(request,
            [],pictures,[],[],'My Pictures', False)


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
    template_name = 'FHLReader/channel.html'
    form_class=forms.RandomForm

    def get(self, request):
        print("RandomList GET")
        context = {'form':self.form_class(),
            'title': 'Build a Random Channel'}
        return render(request,self.template_name,context)

    def post(self, request):
        print("RandomList POST")
        me = User.objects.get(username=request.user)
        mycache = cu.MyCache(me)

        if 'save-query' in request.POST:
            return redirect(reverse('cached_list'))

        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            print(' valid form ')
            count = bound_form.cleaned_data['count'];
            kind = bound_form.cleaned_data['kind'];
            tag = bound_form.cleaned_data['tag'];
            print( kind )
            rlist = rq.random_select(count,'',tag,kind)
            cu.cache_list_bykind(rlist,kind,'random_list',mycache)

        flist = slist = bu.link_file_list(rlist)
        # display the list as files with the form
        context = {'form':bound_form,'rlist':flist,
            'title': 'Build a Random Channel'
            }
        return render(request,self.template_name,context)


class RecentList(View):
    template_name = 'FHLReader/channel.html'
    form_class=forms.RecentForm

    def get(self, request):
        print("RecentList GET")
        context = {'form':self.form_class(),
            'title': 'Build a Recent Channel'}
        return render(request,self.template_name,context)

    def post(self, request):
        print("RecentList POST")
        me = User.objects.get(username=request.user)
        mycache = cu.MyCache(me)

        if 'save-query' in request.POST:
            return redirect(reverse('cached_list'))

        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            count = bound_form.cleaned_data['count'];
            kind = bound_form.cleaned_data['kind'];
            rlist = rq.recent_bykind(kind,count)
            cu.cache_list_bykind(rlist,kind,'random_list',mycache)

        # display the list as files with the form
        flist = slist = bu.link_file_list(rlist)
        context = {'form':bound_form,'rlist':flist,
            'title': 'Build a Recent Channel'}
        return render(request,self.template_name,context)


class SpecialChannel(View):
    """
    Special TV channels
    """
    template_name = 'FHLReader/channel.html'
    form_class=forms.CountForm

    def get(self, request, select):
        print("RandomList GET")
        title = ('Build a channel %s' % (select))
        context = {'form':self.form_class(),
            'title': title}
        return render(request,self.template_name,context)


    def post(self, request, select):
        print("RandomList POST")
        me = User.objects.get(username=request.user)
        mycache = cu.MyCache(me)

        if 'save-query' in request.POST:
            return redirect(reverse('cached_list'))

        rlist = []
        bound_form = self.form_class(request.POST)

        if bound_form.is_valid():
            count = bound_form.cleaned_data['count'];

            if select == 'saturday-morning':
                rlist = rq.saturday_select(count)
            elif select == 'sitcom':
                rlist = rq.sitcom_select(count)
            elif select == 'silly':
                rlist = rq.silly_select(count)
            elif select == 'scifi':
                rlist = rq.scifi_select(count)
            elif select == 'drama':
                rlist = rq.drama_select(count)
            elif select == 'scary':
                rlist = rq.scary_select(count)
            # cache the list
            cu.cache_list_bykind(rlist,choices.MOVIE,
                    'special_channel',mycache)


        # display the list as files with the form
        flist = slist = bu.link_file_list(rlist)
        title = ('Build a channel %s' % (select))
        context = {'form':bound_form,'rlist':flist,
            'title': title}
        return render(request,self.template_name,context)


class MovieChannel(View):
    """
    Channels based on movie kinds
    """
    template_name = 'FHLReader/channel.html'
    form_class=forms.MovieChannelForm

    def getKind(self,akind):
        for x in choices.VIDEO_CHOICES:
            if x[0] == akind:
                return x
        return (choices.TV_CARTOON, 'TV-Cartoon')


    def get(self, request, akind):

        title = ('Build a channel %s' % (akind))
        context = {'form':self.form_class(),
            'title': title}
        return render(request,self.template_name,context)


    def post(self, request, akind):
        me = User.objects.get(username=request.user)
        mycache = cu.MyCache(me)


        if 'save-query' in request.POST:
            return redirect(reverse('cached_list'))

        kind = akind #self.getKind(akind)
        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            count = bound_form.cleaned_data['count']
            title = bound_form.cleaned_data['atitle']
            tag = bound_form.cleaned_data['atag']
            print('Valid form count %d title %s tag %s' % (count,title,tag))
            rlist = rq.random_select(count,title,tag,kind)
            for a in rlist:
                print(a.title)
            cu.cache_list_bykind(rlist,kind,'random_list',mycache)

        flist = slist = bu.link_file_list(rlist)
        title = ('Build a channel %s' % (akind))
        # display the list as files with the form
        context = {'form':bound_form,'rlist':flist,
            'title': title}
        return render(request,self.template_name,context)


class RadioChannel(View):
    template_name = 'FHLReader/channel.html'
    form_class=forms.RadioForm

    def get(self, request):
        print("RandomList GET")
        context = {'form':self.form_class(),
            'title': 'Build a Radio Channel'}
        return render(request,self.template_name,context)


    def post(self, request):
        print("RandomList POST")
        me = User.objects.get(username=request.user)
        mycache = cu.MyCache(me)

        if 'save-query' in request.POST:
            return redirect(reverse('cached_list'))


        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            count = bound_form.cleaned_data['count']
            kind = bound_form.cleaned_data['kind']
            xmas = bound_form.cleaned_data['xmas']

            justme = False
            if kind == choices.ME:
                justme = True
            if xmas:
                rlist = rq.radio_select_christmas(count,justme,me)
            else:
                rlist = rq.radio_select(count,justme,me)
            cu.cache_list_bykind(rlist,choices.SONG,
                'special_channel',mycache)

        flist = slist = bu.link_file_list(rlist)
        # display the list as files with the form
        context = {'form':bound_form,'rlist':flist,
            'title': 'Build a  Channel'}
        return render(request,self.template_name,context)
