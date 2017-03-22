# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from FHLBuilder.models import Tag, Song, Common
from FHLBuilder.forms import TagForm, SongForm
from django.template import RequestContext,loader
from django.shortcuts import get_object_or_404, render, redirect
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

# Tags
class TagDetailView(View):
    template_name = 'FHLBuilder/tag_detail.html'
    def get(self,request,slug):
        tag=get_object_or_404(Tag,slug__iexact=slug)
        return render(request, self.template_name, {'tag':tag})

class TagFormView(View):
    form_class=TagForm
    template_name = 'FHLBuilder/tag_form.html'
    def get(self, request):
        return render(request,self.template_name,
                      {'form':self.form_class()})
    def post(self,request):
        bound_form=self.form_class(request.POST)
        if bound_form.is_valid():
            new_tag=bound_form.save()
            return redirect(new_tag)
        else:
            return render(request,self.template_name,
                          {'form':bound_form})

class TagUpdate(View):
    form_class=TagForm
    model=Tag
    template_name='FHLBuilder/tag_update.html'
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
    def get(self,request,slug):
        tag = self.get_object(slug)
        context={
           'form': self.form_class(instance=tag),
           'tag': tag,
        }
        return render(request,self.template_name,context)

    def post(self,request,slug):
        tag = self.get_object(slug)
        bound_form = self.form_class(request.POST,instance=tag)
        if bound_form.is_valid():
            new_tag = bound_form.save()
            return redirect(new_tag)
        else:
            context={
                'form': bound_form,
                'tag': tag,
            }
            return render(request,self.template_name,context)

class TagDelete(View):
    form_class=TagForm
    model = Tag
    template_name='FHLBuilder/tag_confirm_delete.html'
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
    def get(self,request,slug):
        tag = self.get_object(slug)
        return render(request,self.template_name,{'tag': tag})
    def post(self,request,slug):
        tag = self.get_object(slug)
        tag.delete()
        return redirect('builder_tag_list')

# songs
class SongDetailView(View):
    template_name = 'FHLBuilder/song_detail.html'
    def get(self,request,slug):
        song=get_object_or_404(Song,slug__iexact=slug)
        return render(request, self.template_name, {'song':song})

class SongFormView(View):
    form_class=SongForm
    template_name = 'FHLBuilder/song_form.html'
    def get(self, request):
        return render(request,self.template_name,
                      {'form':self.form_class()})
    def post(self,request):
        bound_form=self.form_class(request.POST)
        if bound_form.is_valid():
            new_song=bound_form.save()
            return redirect(new_song)
        else:
            return render(request,self.template_name,
                          {'form':bound_form})

class SongUpdate(View):
    form_class=SongForm
    model=Song
    template_name='FHLBuilder/song_update.html'
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
    def get(self,request,slug):
        song = self.get_object(slug)
        context={
           'form': self.form_class(instance=song),
           'song': song,
        }
        return render(request,self.template_name,context)

    def post(self,request,slug):
        song = self.get_object(slug)
        bound_form = self.form_class(request.POST,instance=song)
        if bound_form.is_valid():
            new_song = bound_form.save()
            return redirect(new_song)
        else:
            context={
                'form': bound_form,
                'song': song,
            }
            return render(request,self.template_name,context)

class SongDelete(View):
    form_class=SongForm
    model = Song
    template_name='FHLBuilder/song_confirm_delete.html'
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
    def get(self,request,slug):
        song = self.get_object(slug)
        return render(request,self.template_name,{'song': song})
    def post(self,request,slug):
        song = self.get_object(slug)
        song.delete()
        return redirect('builder_song_list')



