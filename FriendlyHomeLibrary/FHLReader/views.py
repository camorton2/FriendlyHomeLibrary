# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View

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

        context = {
            'me': me,
            'choices': choices.VIDEO_CHOICES
            }
        return render(request,self.template_name,context)


class UserSongList(View):
    """
    Selection of liked and loved songs by user
    """
    def get(self,request,pref):
        me = User.objects.get(username=request.user)

        lk = Q(likes__username=me)
        lv = Q(loves__username=me)

        if pref == 'liked':
            songs = Song.objects.filter(lk)
            title = 'Songs I like'
        elif pref == 'loved':
            songs = Song.objects.filter(lv)
            title = 'Songs I love'
        elif pref == 'both':
            songs = Song.objects.filter(lv|lk)
            title = 'All my Songs'
        elif pref == 'random':
            songs = Song.objects.filter(lv|lk).order_by('?')
            title = 'My Songs Radio'            
        else:
            # should not happen
            songs = []
            title = 'Error - no song preference'
            
        vargs = {'songs':songs,'title':title}
        return vu.generic_collection_view(request,**vargs)


class UserVideoList(View):
    """
    Selection of liked loved videos by user
    """
    def get(self,request,pref):
        me = User.objects.get(username=request.user)
        lk = Q(likes__username=me)
        lv = Q(loves__username=me)

        if pref == 'liked':
            videos = Movie.objects.filter(lk)
            title = 'Videos I like'
        elif pref == 'loved':
            videos = Movie.objects.filter(lv)
            title = 'Videos I love'
        elif pref == 'both':
            videos = Movie.objects.filter(lk|lv)
            title = 'All My Videos'
        elif pref == 'random':
            videos = Movie.objects.filter(lk|lv).order_by('?')
            title = 'All My Videos'            
        else:
            # should not happen
            videos = []
            title = 'Error - no video preference'
            
        vargs = {'movies': videos, 'title': title}
        return vu.generic_collection_view(request,**vargs)


class UserPictureList(View):
    """ selection of liked loved pictures by user """
    def get(self,request, pref):
        me = User.objects.get(username=request.user)
        lk = Q(likes__username=me)
        lv = Q(loves__username=me)

        if pref == 'liked':
            pictures = Picture.objects.filter(lk)
            title = 'Pictures I Like'
        elif pref == 'loved':
            pictures = Picture.objects.filter(lv)
            title = 'Pictures I Love'
        elif pref == 'both':
            pictures = Picture.objects.filter(lk|lv)
            title = 'All My Pictures'
        elif pref == 'random':
            pictures = Picture.objects.filter(lk|lv).order_by('?')
            title = 'All My Pictures'
            
        else:
            # should not happen
            videos = []
            title = 'Error - no picture preference'

        vargs = {'pictures':pictures,'title':title}
        return vu.generic_collection_view(request,**vargs)


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

        vargs = {
            'songs': songs,
            'pictures': pictures,
            'videos': videos,
            'title': 'Saved Collection'
            }
        return vu.generic_collection_view(request,**vargs)


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
            count = bound_form.cleaned_data['count']
            kind = bound_form.cleaned_data['kind']
            tag = bound_form.cleaned_data['tag']
            title = bound_form.cleaned_data['atitle']
            print( kind )
            rlist = rq.random_select(count,title,tag,kind)
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

        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            count = bound_form.cleaned_data['count'];
            kind = bound_form.cleaned_data['kind'];
            rlist = rq.recent_bykind(kind,count)
            cu.cache_list_bykind(rlist,kind,'random_list',mycache)
            return redirect(reverse('cached_list'))
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
            random = bound_form.cleaned_data['random']

            rlist = rq.random_select(count,title,tag,kind,random)
            cu.cache_list_bykind(rlist,kind,'random_list',mycache)

        flist = slist = bu.link_file_list(rlist)
        title = ('Build a channel %s' % (akind))
        # display the list as files with the form
        context = {'form':bound_form,'rlist':flist,
            'title': title}
        return render(request,self.template_name,context)


class RadioChannel(View):
    """
    Allow the user to create a radio channel based on form
    """
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
            recent = bound_form.cleaned_data['recent']

            justme = False
            if kind == choices.ME:
                justme = True

            if recent:
                target = Song.newest_objects.all()
            else:
                target = Song.random_objects.all()
                
            if xmas:
                alist = rq.radio_select_christmas(justme,me,target)
            else:
                alist = rq.radio_select(justme,me,target)
            
            rlist = alist[:count]
            if recent:
                rlist = rq.random_count(rlist,count)
                
            cu.cache_list_bykind(rlist,choices.SONG,'special_channel',
                mycache)
            if recent:
                # recent case simply move to cached list
                return redirect(reverse('cached_list'))

        flist = slist = bu.link_file_list(rlist)
        # display the list as files with the form
        context = {'form':bound_form,'rlist':flist,
            'title': 'Build a  Channel'}
        return render(request,self.template_name,context)


class MusicianRadioChannel(View):
    """
    Allow user to select a radio channel based on the form
    in this case selecting by artist
    """
    template_name = 'FHLReader/channel.html'
    form_class=forms.MusicianRadioForm

    def get(self, request):
        print("RandomList GET")
        context = {'form':self.form_class(),
            'title': 'Build a Musician Radio Channel'}
        return render(request,self.template_name,context)


    def post(self, request):
        print("RandomList POST")
        me = User.objects.get(username=request.user)
        mycache = cu.MyCache(me)

        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            xmas = bound_form.cleaned_data['xmas']
            artists = bound_form.cleaned_data['choices']
            rlist = rq.artist_radio_select(artists,xmas)
            cu.cache_list_bykind(rlist,choices.SONG,'special_channel',mycache)
            return redirect(reverse('cached_list'))

        flist = slist = bu.link_file_list(rlist)
        # display the list as files with the form
        context = {'form':bound_form,'rlist':flist,
            'title': 'Build a  Channel'}
        return render(request,self.template_name,context)
