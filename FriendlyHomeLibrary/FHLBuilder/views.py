# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from FHLBuilder.models import Tag, Song, Common
from django.template import RequestContext,loader
from django.shortcuts import get_object_or_404, render
from django.views.generic import View

# Create your views here.

class HomePage(View):
    template_name = 'FHLBuilder/base_fhlbuilder.html'
    def get(self, request):

        return render(
          request,
          self.template_name,)

class TagList(View):
    template_name = 'FHLBuilder/tag_list.html'
    def get(self, request):
        tl = Tag.objects.all()
        test1 = {'tl': tl}

        return render(
          request,
          self.template_name,
          test1)

class CommonList(View):
    template_name='FHLBuilder/common_list.html'
    def get(self,request):
        tl = Common.objects.all()
        test1 = {'tl': tl}

        return render(
          request,
          self.template_name,
          test1)

class SongList(View):
    template_name='FHLBuilder/song_list.html'
    def get(self,request):
        tl = Song.objects.all()
        test1 = {'tl': tl}

        return render(
          request,
          self.template_name,
          test1)


def tag_detail(request,slug):
    tag = get_object_or_404(
       Tag,slug__iexact=slug)
    return render(
      request,
      'FHLBuilder/tag_detail.html',
      {'tag':tag})
