# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import string

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
#from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.text import slugify
from django.template import RequestContext,loader
from django.views.generic import View

from FriendlyHomeLibrary import settings

from FHLUser.decorators import require_authenticated_permission

from FHLBuilder import models, forms
from FHLBuilder import collection
from FHLBuilder import choices
from FHLBuilder import utility
from FHLBuilder import query
from FHLBuilder import diagnostics

from FHLReader import kodi



def collection_view(request, songs, pictures, movies, title, 
    allowChoice=False, kind=choices.MOVIE,update=False):
    template_name = 'FHLBuilder/collection_detail.html'
    mySongList = utility.link_file_list(songs)
    asPlayList = False;
    if 'playlist' in request.GET:
        asPlayList = True

    # pictures, setup slideshow        
    count = len(pictures)
    current = 1
    if 'cNext' in request.GET and request.GET.get('cNext'):
        current = int(request.GET.get('cNext'))
        print("next with current %d" % current)
        current = current+1
        if current > count:
            current = 1
    if 'cPrev' in request.GET and request.GET.get('cPrev'):
        current = int(request.GET.get('cPrev'))
        print("prev with current %d" % current)
        if current == 1:
            current = count
        else:
            current=current-1
    picture = None
    filename = None
    if count:
       picture = pictures[current-1]
       filename = utility.object_path(picture)

    # movies, in future to setup playlist


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

    context = {
        'title':title,
        'songlist':mySongList,
        'picture':picture,
        'pictureCount':count,
        'filename': filename,
        'index': current,
        'asPlayList': asPlayList,
        'movielist':movies,
        'update':update,
        'choices': choices.KIND_CHOICES,
        'listkind':kind,
        'allowChoice': allowChoice,
        }
    return render(request, template_name, context)
    

def movies_bykind(kind):
    movies = models.Movie.objects.filter(fileKind=kind)
    count = movies.count()
    for x,y in choices.KIND_CHOICES:
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
        'choices': choices.KIND_CHOICES
        }
    return render(request,template_name,context)
    

def select_kind(request):
    if 'kind' in request.GET and request.GET.get('kind'):
        kind = request.GET.get('kind')
    else:
        kind = choices.MOVIE
    return kind
    
    