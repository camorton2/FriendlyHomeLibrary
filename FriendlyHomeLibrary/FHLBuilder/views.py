# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from FHLBuilder.models import Tag, Song
from django.template import Context,loader

# Create your views here.        

def poke(request):
    template = loader.get_template('FHLBuilder/test.html')
    test = {'x': 'George lives here'}
    tl = Tag.objects.all()
    test1 = {'tl': tl}
    output=template.render(test1)
    return HttpResponse(output)
    
    
