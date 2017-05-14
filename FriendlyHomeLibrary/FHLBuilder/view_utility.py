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
from FHLBuilder import diagnostics

from FHLReader import kodi

def big_collection_view(request,mycache):
    """
    Given that a view has setup the generators in the cache
    experiment to see if I can iterate the big list without
    repeating the query
    If the generators are not setup, does nothing
    """
    template_name = 'FHLBuilder/collection_detail.html'

    picture = None
    filename = None

    if mycache.has_generator():
        print('Ok generator is setup')
        if 'cNext' in request.GET and request.GET.get('cNext'):
            print('next')
            picture,filename = mycache.cache_next()
        elif 'cPrev' in request.GET and request.GET.get('cPrev'):
            print('prev')
            picture,filename = mycache.cach_prev()
        else:
            print('start')
            picture,filename = mycache.cache_next()
        

    context = {
        'title':'still to do',
        'songlist':[],
        'picture':picture,
        'pictureCount':0,  # to do
        'filename': filename,
        'index': 0, # to do
        'asPlayList': False,
        'movielist':[],
        'update':False,
        'choices': choices.LIVE_CHOICES,
        'listkind':choices.PICTURE,
        'allowChoice': True,
        'artists': [],
        'message': ''
        }
    return render(request, template_name, context)


def collection_view(request, songs, pictures, movies, artists, title, 
    allowChoice=False, kind=choices.MOVIE,update=None):
        
    template_name = 'FHLBuilder/collection_detail.html'
    
    songList = utility.link_file_list(songs)
    
    asPlayList = False;
    if 'playlist' in request.GET:
        asPlayList = True

    # pictures, setup slideshow        
    
    print('pictures sent length %d' % (len(pictures)))
    count = len(pictures)
    pictureList = utility.link_file_list(pictures)
    
    current = 1
    if 'cNext' in request.GET and request.GET.get('cNext'):
        current = int(request.GET.get('cNext'))
        current = current+1
        if current > count:
            current = 1
        print('next %d count %d' % (current,count))
    if 'cPrev' in request.GET and request.GET.get('cPrev'):
        current = int(request.GET.get('cPrev'))
        if current == 1:
            current = count
        else:
            current=current-1

    picture = None
    filename = None
    
    if count:
        picture,filename = pictureList[current-1]

    # tags all objects
    if 'tq' in request.GET and request.GET['tq']:
        tq = request.GET['tq']
        tqSlug = slugify(unicode(tq))
        new_tag = collection.add_tag(tq,tqSlug)
            
        for obj in songs:
            obj.tags.add(new_tag)
        for obj in pictures:
            obj.tags.add(new_tag)
        for obj in movies:
            obj.tags.add(new_tag)

    # kodi playlist options
    # TODO collections with more than one?
    message = ''
    try:
        if movies and kodi.playlist_requests(movies,request):
            message = u'success - movies sent'
        elif songs and kodi.playlist_requests(songs,request):
            message = u'success - songs sent'
        elif pictures and kodi.playlist_requests(pictures,request):
            message = u'success - pictures sent'
        
    except kodi.MyException,ex:
        message = ex.message
        print('Caught %s' % ex.message)


    context = {
        'title':title,
        'songlist':songList,
        'picture':picture,
        'pictureCount':count,
        'filename': filename,
        'index': current,
        'asPlayList': asPlayList,
        'movielist':movies,
        'update':update,
        'choices': choices.LIVE_CHOICES,
        'listkind':kind,
        'allowChoice': allowChoice,
        'artists': artists,
        'message': message
        }
    return render(request, template_name, context)
    

def movies_bykind(kind):
    """
    Given a kind, select only matching movie objects
    """
    movies = models.Movie.objects.filter(fileKind=kind)
    count = movies.count()
    for x,y in choices.LIVE_CHOICES:
        if x == kind:
            desc = y
            break
    title = ('%s: %d' % (desc, count))
    return movies, title    


def view_list(request,alist,title,kind):
    template_name='FHLBuilder/collection_list.html'
    context = {
        'title':title,
        'clist': alist,
        'listkind':kind,
        'choices': choices.LIVE_CHOICES
        }
    return render(request,template_name,context)
    

def select_kind(request):
    """
    Given a GET request, select kind or default to movie
    """
    if 'kind' in request.GET and request.GET.get('kind'):
        kind = request.GET.get('kind')
    else:
        kind = choices.MOVIE
    return kind

