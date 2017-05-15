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


def generic_collection_view(request, **kwargs):
    print('generic_collection_view')
    
    template_name = 'FHLBuilder/collection_detail.html'
    
    # respond to slide show
    current = 1
    if 'cNext' in request.GET and request.GET.get('cNext'):
        current = int(request.GET.get('cNext'))
        current = current+1
        if current > count:
            current = 1
    if 'cPrev' in request.GET and request.GET.get('cPrev'):
        current = int(request.GET.get('cPrev'))
        if current == 1:
            current = count
        else:
            current=current-1

    # respond to playlist
    asPlayList = False;
    if 'playlist' in request.GET:
        asPlayList = True

    songs=kwargs.get('songs',[])
    movies=kwargs.get('movies',[])
    pictures=kwargs.get('pictures',[])
    artists=kwargs.get('artists',[])
    title=kwargs.get('title','Collection View')
    allowChoice = kwargs.get('allowChoice',False)
    kind=kwargs.get('kind',choices.MOVIE)
    update=kwargs.get('update',None)
    
    songList = utility.link_file_list(songs)
    count = len(pictures)
    pictureList = utility.link_file_list(pictures)
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

