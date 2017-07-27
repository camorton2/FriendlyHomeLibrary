# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import calendar, datetime

from django.forms.widgets import HiddenInput
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import FormView

from FHLBuilder import choices
from FHLBuilder.models import Song, Movie, Picture

import FHLBuilder.view_utility as vu

from FHLReader import forms, kodi

import FHLReader.cache_utility as cu
import FHLReader.query as rq
import FHLReader.utility as rutils

# Create your views here.


class UserDetail(View):
    """
    User main page mostly to select playlists
    """
    template_name = 'FHLReader/user_page.html'
    def get(self, request):
        # print("UserDetail GET")
        me = rq.get_me(True,request)
            
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
        me = rq.get_me(False,request)
            
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
        me = rq.get_me(False,request)
            
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
        me = rq.get_me(False,request)
        lk = Q(likes__username=me)
        lv = Q(loves__username=me)

        if pref == 'liked':
            pictures = Picture.slide_objects.filter(lk)
            title = 'Pictures I Like'
        elif pref == 'loved':
            pictures = Picture.slide_objects.filter(lv)
            title = 'Pictures I Love'
        elif pref == 'both':
            pictures = Picture.slide_objects.filter(lk|lv)
            title = 'All My Pictures'
        elif pref == 'random':
            pictures = Picture.slide_objects.filter(lk|lv).order_by('?')
            title = 'All My Pictures'
            
        else:
            # should not happen
            pictures = []
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
        #print("CachedFileList GET")
        
        mycache = cu.MyCache(request)

        songs, pictures, videos,_ = mycache.get_query()

        vargs = {
            'songs': songs,
            'pictures': pictures,
            'movies': videos,
            'title': 'Saved Collection'
            }
        return vu.generic_collection_view(request,**vargs)


class RandomList(View):
    template_name = 'FHLReader/channel.html'
    form_class=forms.RandomForm

    def get(self, request):
        #print("RandomList GET")
        context = {'form':self.form_class(),
            'title': 'Build a Random Channel'}
        return render(request,self.template_name,context)

    def post(self, request):
        #print("RandomList POST")
        mycache = cu.MyCache(request)

        if 'save-query' in request.POST:
            return redirect(reverse('cached_list'))

        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            #print(' valid form ')
            count = bound_form.cleaned_data['count']
            kind = bound_form.cleaned_data['kind']
            tag = bound_form.cleaned_data['tag']
            title = bound_form.cleaned_data['atitle']
            #print( kind )
            rlist = rq.random_select(count,title,tag,kind)
            cu.cache_list_bykind(rlist,kind,'random_list',mycache)

        # display the list as files with the form
        context = {'form':bound_form,'rlist':rlist,
            'title': 'Build a Random Channel'
            }
        return render(request,self.template_name,context)


class RecentList(View):
    template_name = 'FHLReader/channel.html'
    form_class=forms.RecentForm

    def get(self, request):
        #print("RecentList GET")
        context = {'form':self.form_class(),
            'title': 'Build a Recent Channel'}
        return render(request,self.template_name,context)

    def post(self, request):
        #print("RecentList POST")
        mycache = cu.MyCache(request)

        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            count = bound_form.cleaned_data['count']
            kind = bound_form.cleaned_data['kind']
            rlist = rq.recent_bykind(kind,count)
            cu.cache_list_bykind(rlist,kind,'random_list',mycache)
            return redirect(reverse('cached_list'))
        # display the list as files with the form
        context = {'form':bound_form,'rlist':rlist,
            'title': 'Build a Recent Channel'}
        return render(request,self.template_name,context)


class SpecialChannel(View):
    """
    Special TV channels
    """
    template_name = 'FHLReader/channel.html'
    form_class=forms.CountForm

    def get(self, request, select):
        #print("RandomList GET")
        title = ('Build a channel %s' % (select))
        context = {'form':self.form_class(),
            'title': title}
        return render(request,self.template_name,context)


    def post(self, request, select):
        #print("RandomList POST")
        mycache = cu.MyCache(request)

        if 'save-query' in request.POST:
            return redirect(reverse('cached_list'))

        rlist = []
        bound_form = self.form_class(request.POST)

        if bound_form.is_valid():
            count = bound_form.cleaned_data['count']

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
        title = ('Build a channel %s' % (select))
        context = {'form':bound_form,'rlist':rlist,
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
        mycache = cu.MyCache(request)

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

        title = ('Build a channel %s' % (akind))
        # display the list as files with the form
        context = {'form':bound_form,'rlist':rlist,'title': title}
        return render(request,self.template_name,context)


class RadioChannel(View):
    """
    Allow the user to create a radio channel based on form
    """
    template_name = 'FHLReader/channel.html'
    form_class=forms.RadioForm

    def get(self, request):
        #print("RandomList GET")        
        rform = self.form_class()
        me = rq.get_me(True,request)
        if me is None:
            # hide field from anonymous user
            rform.fields['kind'].widget = HiddenInput()
        
        context = {'form':rform,
            'title': 'Build a Radio Channel'}
        return render(request,self.template_name,context)


    def post(self, request):
        #print("RadioChannel POST")
        me = rq.get_me(True,request)
        mycache = cu.MyCache(request)

        if 'save-query' in request.POST:
            return redirect(reverse('cached_list'))

        rlist = []
        bound_form = self.form_class(request.POST)
        if me is None:
            # hide field from anonymous user
            bound_form.fields['kind'].widget = HiddenInput()
            
        if bound_form.is_valid():
            count = bound_form.cleaned_data['count']
            kind = bound_form.cleaned_data['kind']
            xmas = bound_form.cleaned_data['xmas']
            recent = bound_form.cleaned_data['recent']
            cl = bound_form.cleaned_data['classic']

            justme = False
            if kind == choices.ME:
                justme = True

            if recent:
                rlist = rq.radio_recent(justme,me,cl,xmas,count)
            else:
                target = rq.radio_all(justme,me,cl,xmas)
                rlist = target[:count]
                                
            cu.cache_list_bykind(rlist,choices.SONG,'special_channel',
                mycache)
            if recent:
                # recent case simply move to cached list
                return redirect(reverse('cached_list'))

        # display the list as files with the form
        context = {'form':bound_form,'rlist':rlist,
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
        #print("RandomList GET")
        context = {'form':self.form_class(),
            'title': 'Build a Musician Radio Channel'}
        return render(request,self.template_name,context)


    def post(self, request):
        #print("RandomList POST")
        mycache = cu.MyCache(request)

        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            xmas = bound_form.cleaned_data['xmas']
            artists = bound_form.cleaned_data['choices']
            rlist = rq.artist_radio_select(artists,xmas)
            cu.cache_list_bykind(rlist,choices.SONG,'special_channel',mycache)
            return redirect(reverse('cached_list'))

        # display the list as files with the form
        context = {'form':bound_form,'rlist':rlist,
            'title': 'Build a  Channel'}
        return render(request,self.template_name,context)



class CollectionRadioChannel(View):
    """
    Allow user to select a radio channel based on the form
    in this case by selection collections
    """
    template_name = 'FHLReader/channel.html'
    form_class=forms.CollectionRadioForm

    def get(self, request):
        context = {'form':self.form_class(),
            'title': 'Build a Collection Radio Channel'}
        return render(request,self.template_name,context)


    def post(self, request):
        mycache = cu.MyCache(request)

        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            xmas = bound_form.cleaned_data['xmas']
            colls = bound_form.cleaned_data['choices']
            rlist = rq.collection_radio_select(colls,xmas)
            cu.cache_list_bykind(rlist,choices.SONG,'special_channel',mycache)
            return redirect(reverse('cached_list'))

        # display the list as files with the form
        context = {'form':bound_form,'rlist':rlist,
            'title': 'Build a  Channel'}
        return render(request,self.template_name,context)


class SongRadioChannel(View):
    """
    Allow user to select a radio channel based on the form
    in this case by selecting songs
    """
    template_name = 'FHLReader/channel.html'
    form_class=forms.SongRadioForm

    def get(self, request):
        context = {'form':self.form_class(),
            'title': 'Build a Song Radio Channel'}
        return render(request,self.template_name,context)


    def post(self, request):
        mycache = cu.MyCache(request)

        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            rlist = bound_form.cleaned_data['choices']
            cu.cache_list_bykind(rlist,choices.SONG,'special_channel',mycache)
            return redirect(reverse('cached_list'))

        # display the list as files with the form
        context = {'form':bound_form,'rlist':rlist,
            'title': 'Build a  Channel'}
        return render(request,self.template_name,context)


class DateRadioChannel(FormView):
    template_name = 'FHLReader/channel_basic.html'
    form_class = forms.DateAddedRadioForm
    success_url = ''
    random = False
    
    def form_valid(self,form):
        random = form.cleaned_data['random']
        playback = form.cleaned_data['playback']
        christmas = form.cleaned_data['xmas']
        print('form with playback %s' % playback)
        #print('form with random %s' % random)
        try:
            ya=int(form.cleaned_data['yearA'])
            yb=int(form.cleaned_data['yearB'])
            ma=int(form.cleaned_data['monthA'])
            mb=int(form.cleaned_data['monthB'])
        except ValueError:
            return redirect(reverse('date_radio_channel'))

        my_options = u'?playback=' + playback        
        if random:
            my_options = my_options + u'&random=True'
        if christmas:
            my_options = my_options + u'&christmas=True'

        if ya and yb:
            if ma and mb:
                context = {
                    'yearA': ya,
                    'yearB': yb,
                    'monthA': ma,
                    'monthB': mb
                }
            elif ma:
                context = {'yearA': ya,'yearB': yb,'monthA': ma}
            elif mb:
                context = {'yearA': ya,'yearB': yb,'monthB': mb}
            else:
                context = {'yearA': ya,'yearB': yb}
            reverse_value = reverse('range_added_radio_channel',
                kwargs=context)
            reverse_value = reverse_value + my_options
            return redirect(reverse_value)
            
        if ya and ma:
            context = {'yearA': ya,'monthA': ma}
        else:
            context = {'yearA': ya}
        reverse_value = reverse('date_added_radio_channel',
            kwargs = context)
        reverse_value = reverse_value + my_options        
            
        #print(reverse_value)
        return redirect(reverse_value)


def send_to_playlist(songs,request):

    # default values to be replaced if option is in request
    christmas = False
    playback = choices.WEB
    random = False
    
    if request.method == 'POST':
        if 'random' in request.POST:
            random = request.POST.get('random')
        if 'playback' in request.POST:
            playback = request.POST.get('playback')
        if 'christmas' in request.POST:
            christmas = request.POST.get('christmas')
    if request.method == 'GET':
        if 'random' in request.GET:
            random = request.GET.get('random')
        if 'playback' in request.GET:
            playback = request.GET.get('playback')
        if 'christmas' in request.GET:
            christmas = request.GET.get('christmas')
    print('options xmas %s random %s playback %s' % (christmas,random,playback))            
    
    message = u''
    if random:
        songs = songs.order_by('?')
    if not christmas:
        songs = rq.exclude_xmas(songs)

    
    if playback == choices.WEB:
        asPlayList = True
    elif playback == choices.FLIST:
        asPlayList = False
    else:
        asPlayList = False
        try:
            if kodi.playlist_select(songs,playback,request):
                message = u'success - songs sent to Kodi' 
        except rutils.MyException,ex:
            message = ex.message
            print('Caught %s' % ex.message)
        
    context = {
        'songlist':songs,
        'asPlayList':asPlayList,
        'listTitle':'Date added radio',
        'message':message}
    template_name = 'FHLReader/song_list.html'    
    return render(request,template_name,context)


def date_added_radio_channel(request,yearA,monthA=None):    
    songs = Song.newest_objects.filter(date_added__year=yearA)
    if monthA:
        songs = songs.filter(date_added__month=monthA)
        
    return send_to_playlist(songs,request)


def range_added_radio_channel(request,yearA,yearB,monthA=None,
    monthB=None):

    valid = yearB >= yearA
    if monthA and monthB:
        pass
    elif monthA:
        valid = False
    elif monthB:
        valid = False
                
    if valid and monthA:
        try:
            # first day of monthA
            yA = int(yearA)
            mA = int(monthA)
            yB = int(yearB)
            mB = int(monthB)
            dA = datetime.date(yA,mA,1)            
            rangeB = calendar.monthrange(yB,mB)[1]
            # last day of monthA
            dB = datetime.date(yB,mB,rangeB)
            q1 = Q(date_added__gte=dA)
            q2 = Q(date_added__lte=dB)
            songs = Song.newest_objects.filter(q1).filter(q2)
        except ValueError:
            songs = []
    elif valid:
        q1 = Q(date_added__year__gte=yearA)
        q2 = Q(date_added__year__lte=yearB)
        songs = Song.newest_objects.filter(q1).filter(q2)
    else:
        # likely better to have an error condition, but
        # plan is to disallow this in the form
        songs=[]
        
    return send_to_playlist(songs,request)
