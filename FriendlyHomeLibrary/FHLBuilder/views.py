# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from FHLBuilder.models import Tag, Song, CommonFile, Collection, Movie
from FHLBuilder.models import Director,Actor,Musician
from FHLBuilder.forms import TagForm, SongForm, CollectionForm, MovieForm
from FHLBuilder.forms import ActorForm, DirectorForm, MusicianForm

from django.template import RequestContext,loader
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View

from FHLUser.decorators import require_authenticated_permission

import os

from collection import add_file



# Create your views here.

class HomePage(View):
    template_name = 'FHLBuilder/base_fhlbuilder.html'
    def get(self, request):
        return render(request,self.template_name,)

# Tags
class TagList(View):
    template_name = 'FHLBuilder/tag_list.html'
    def get(self, request):
        tl = Tag.objects.all()
        test1 = {'tl': tl}
        return render(request,self.template_name,test1)

class TagDetailView(View):
    template_name = 'FHLBuilder/tag_detail.html'
    def get(self,request,slug):
        tag=get_object_or_404(Tag,slug__iexact=slug)
        return render(request, self.template_name, {'tag':tag})

@require_authenticated_permission('FHLBuilder.tag_reader')
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

@require_authenticated_permission('FHLBuilder.tag_reader')
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

@require_authenticated_permission('FHLBuilder.tag_builder')
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
class SongList(View):
    template_name='FHLBuilder/song_list.html'
    def get(self,request):
        tl = Song.objects.all()
        test1 = {'tl': tl}

        return render(
          request,
          self.template_name,
          test1)

class SongDetailView(View):
    template_name = 'FHLBuilder/song_detail.html'
    def get(self,request,slug):
        song=get_object_or_404(Song,slug__iexact=slug)
        playit = "mediafiles/" + song.collection.filePath + '/' + song.fileName
        print("HERE HERE HERE HERE %s" % (playit))
        return render(request, self.template_name, {'song':song, 'playit':playit})
    def post(self,request,slug):
        print ("SONG POST ----- does nothing, added for experiment")
        print (slug)
        movie=get_object_or_404(Movie,slug__iexact=slug)
        playit = "/home/catherine/Media/" + movie.collection.filePath + '/' + movie.fileName
        os.system("vlc %s" % playit)        
        return render(request,self.template_name)


@require_authenticated_permission('FHLBuilder.song_builder')
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

@require_authenticated_permission('FHLBuilder.tag_reader')
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

@require_authenticated_permission('FHLBuilder.song_builder')
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

#Collections
class CollectionList(View):
    template_name='FHLBuilder/collection_list.html'
    def get(self,request):
        tl = Collection.objects.all()
        test1 = {'tl': tl}
        return render(
          request,
          self.template_name,
          test1)

class CollectionMixins:
    hardCodeHead = '/home/catherine/Media/'
    def add_members(self, path, newCollection):
        for root, dirs, files in os.walk(os.path.join(self.hardCodeHead,path)):
            for obj in files:
                print("root %s obj %s" % (root,obj))
                add_file(root,obj,path,newCollection)
            for dobj in dirs:
                newPath = path+'/'+dobj
                self.add_members(newPath, newCollection)


class CollectionDetailView(View, CollectionMixins):
    template_name = 'FHLBuilder/collection_detail.html'
    def get(self,request,slug):
        collection=get_object_or_404(Collection,slug__iexact=slug)
        return render(request, self.template_name, {'collection':collection})

@require_authenticated_permission('FHLBuilder.collection_builder')
class CollectionFormView(View,CollectionMixins):

    form_class=CollectionForm
    template_name = 'FHLBuilder/collection_form.html'
    def get(self, request):
        return render(request,self.template_name,
                      {'form':self.form_class()})
    def post(self,request):
        bound_form=self.form_class(request.POST)
        if bound_form.is_valid():
            new_collection=bound_form.save()
            self.add_members(new_collection.filePath, new_collection)
            new_collection.save()
            return redirect(new_collection)
        else:
            return render(request,self.template_name,
                          {'form':bound_form})

@require_authenticated_permission('FHLBuilder.collection_builder')
class CollectionUpdate(View,CollectionMixins):
    form_class=CollectionForm
    model=Collection
    template_name='FHLBuilder/collection_update.html'
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
    def get(self,request,slug):
        collection = self.get_object(slug)
        context={
           'form': self.form_class(instance=collection),
           'collection': collection,
        }
        # rescan for additional files
        self.add_members(collection.filePath, collection)
        collection.save()
        return render(request,self.template_name,context)

    def post(self,request,slug):
        collection = self.get_object(slug)
        bound_form = self.form_class(request.POST,instance=collection)
        if bound_form.is_valid():
            new_collection = bound_form.save()
            self.add_members(new_collection.filePath, new_collection)
            new_collection.save()
            return redirect(new_collection)
        else:
            context={
                'form': bound_form,
                'collection': collection,
            }
            return render(request,self.template_name,context)

@require_authenticated_permission('FHLBuilder.collection_builder')
class CollectionDelete(View,CollectionMixins):
    form_class=CollectionForm
    model = Collection
    template_name='FHLBuilder/collection_confirm_delete.html'
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
    def get(self,request,slug):
        collection = self.get_object(slug)
        return render(request,self.template_name,{'collection': collection})
    def post(self,request,slug):
        collection = self.get_object(slug)
        collection.delete()
        return redirect('builder_collection_list')


# movies
class MovieList(View):
    template_name='FHLBuilder/movie_list.html'
    def get(self,request):
        tl = Movie.objects.all()
        test1 = {'tl': tl}
        return render(
          request,
          self.template_name,
          test1)

class MovieDetailView(View):
    template_name = 'FHLBuilder/movie_detail.html'
    def get(self,request,slug):
        movie=get_object_or_404(Movie,slug__iexact=slug)

        playit = "mediafiles/" + movie.collection.filePath + '/' + movie.fileName
        print("HERE HERE HERE HERE %s" % (playit))

        return render(request, self.template_name, {'movie':movie, 'playit':playit})
    def post(self,request,slug):
        print ("MOVIE POST ----- does nothing, added for experiment")
        print (slug)
        movie=get_object_or_404(Movie,slug__iexact=slug)
        playit = "/home/catherine/Media/" + movie.collection.filePath + '/' + movie.fileName
        os.system("vlc %s" % playit)        
        return render(request,self.template_name)


@require_authenticated_permission('FHLBuilder.movie_builder')
class MovieFormView(View):
    form_class=MovieForm
    template_name = 'FHLBuilder/movie_form.html'
    def get(self, request):
        return render(request,self.template_name,
                      {'form':self.form_class()})
    def post(self,request):
        bound_form=self.form_class(request.POST)
        if bound_form.is_valid():
            new_movie=bound_form.save()
            return redirect(new_movie)
        else:
            return render(request,self.template_name,
                          {'form':bound_form})

@require_authenticated_permission('FHLBuilder.tag_reader')
class MovieUpdate(View):
    form_class=MovieForm
    model=Movie
    template_name='FHLBuilder/movie_update.html'
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
    def get(self,request,slug):
        movie = self.get_object(slug)
        context={
           'form': self.form_class(instance=movie),
           'movie': movie,
        }
        return render(request,self.template_name,context)

    def post(self,request,slug):
        movie = self.get_object(slug)
        bound_form = self.form_class(request.POST,instance=movie)
        if bound_form.is_valid():
            new_movie = bound_form.save()
            return redirect(new_movie)
        else:
            context={
                'form': bound_form,
                'movie': movie,
            }
            return render(request,self.template_name,context)

@require_authenticated_permission('FHLBuilder.movie_builder')
class MovieDelete(View):
    form_class=MovieForm
    model = Movie
    template_name='FHLBuilder/movie_confirm_delete.html'
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
    def get(self,request,slug):
        movie = self.get_object(slug)
        return render(request,self.template_name,{'movie': movie})
    def post(self,request,slug):
        movie = self.get_object(slug)
        movie.delete()
        return redirect('builder_movie_list')

# Actors
class ActorList(View):
    template_name = 'FHLBuilder/actor_list.html'
    def get(self, request):
        tl = Actor.objects.all()
        test1 = {'tl': tl}
        return render(
          request,
          self.template_name,
          test1)

class ActorDetailView(View):
    template_name = 'FHLBuilder/actor_detail.html'
    def get(self,request,slug):
        actor=get_object_or_404(Actor,slug__iexact=slug)
        return render(request, self.template_name, {'actor':actor})

@require_authenticated_permission('FHLBuilder.actor_reader')
class ActorFormView(View):
    form_class=ActorForm
    template_name = 'FHLBuilder/actor_form.html'
    def get(self, request):
        return render(request,self.template_name,
                      {'form':self.form_class()})
    def post(self,request):
        bound_form=self.form_class(request.POST)
        if bound_form.is_valid():
            new_actor=bound_form.save()
            return redirect(new_actor)
        else:
            return render(request,self.template_name,
                          {'form':bound_form})

@require_authenticated_permission('FHLBuilder.actor_reader')
class ActorUpdate(View):
    form_class=ActorForm
    model=Actor
    template_name='FHLBuilder/Actor_update.html'
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
    def get(self,request,slug):
        actor = self.get_object(slug)
        context={
           'form': self.form_class(instance=tag),
           'actor': actor,
        }
        return render(request,self.template_name,context)

    def post(self,request,slug):
        actor = self.get_object(slug)
        bound_form = self.form_class(request.POST,instance=actor)
        if bound_form.is_valid():
            new_actor = bound_form.save()
            return redirect(new_actor)
        else:
            context={
                'form': bound_form,
                'actor': actor,
            }
            return render(request,self.template_name,context)

@require_authenticated_permission('FHLBuilder.actor_builder')
class ActorDelete(View):
    form_class=ActorForm
    model = Actor
    template_name='FHLBuilder/actor_confirm_delete.html'
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
    def get(self,request,slug):
        actor = self.get_object(slug)
        return render(request,self.template_name,{'actor': actor})
    def post(self,request,slug):
        actor = self.get_object(slug)
        actor.delete()
        return redirect('builder_actor_list')

# Directors
class DirectorList(View):
    template_name = 'FHLBuilder/director_list.html'
    def get(self, request):
        tl = Director.objects.all()
        test1 = {'tl': tl}

        return render(
          request,
          self.template_name,
          test1)

class DirectorDetailView(View):
    template_name = 'FHLBuilder/director_detail.html'
    def get(self,request,slug):
        director=get_object_or_404(Director,slug__iexact=slug)
        return render(request, self.template_name, {'director':director})

@require_authenticated_permission('FHLBuilder.director_reader')
class DirectorFormView(View):
    form_class=DirectorForm
    template_name = 'FHLBuilder/director_form.html'
    def get(self, request):
        return render(request,self.template_name,
                      {'form':self.form_class()})
    def post(self,request):
        bound_form=self.form_class(request.POST)
        if bound_form.is_valid():
            new_director=bound_form.save()
            return redirect(new_director)
        else:
            return render(request,self.template_name,
                          {'form':bound_form})

@require_authenticated_permission('FHLBuilder.director_reader')
class DirectorUpdate(View):
    form_class=DirectorForm
    model=Director
    template_name='FHLBuilder/director_update.html'
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
    def get(self,request,slug):
        director = self.get_object(slug)
        context={
           'form': self.form_class(instance=tag),
           'director': director,
        }
        return render(request,self.template_name,context)

    def post(self,request,slug):
        director = self.get_object(slug)
        bound_form = self.form_class(request.POST,instance=director)
        if bound_form.is_valid():
            new_director = bound_form.save()
            return redirect(new_director)
        else:
            context={
                'form': bound_form,
                'director': director,
            }
            return render(request,self.template_name,context)

@require_authenticated_permission('FHLBuilder.director_builder')
class DirectorDelete(View):
    form_class=DirectorForm
    model = Director
    template_name='FHLBuilder/director_confirm_delete.html'
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
    def get(self,request,slug):
        director = self.get_object(slug)
        return render(request,self.template_name,{'director': director})
    def post(self,request,slug):
        director = self.get_object(slug)
        director.delete()
        return redirect('builder_director_list')

# Musicians
class MusicianList(View):
    template_name = 'FHLBuilder/musician_list.html'
    def get(self, request):
        tl = Musician.objects.all()
        test1 = {'tl': tl}

        return render(
          request,
          self.template_name,
          test1)

class MusicianDetailView(View):
    template_name = 'FHLBuilder/musician_detail.html'
    def get(self,request,slug):
        musician=get_object_or_404(Musician,slug__iexact=slug)
        return render(request, self.template_name, {'musician':musician})

@require_authenticated_permission('FHLBuilder.musician_reader')
class MusicianFormView(View):
    form_class=MusicianForm
    template_name = 'FHLBuilder/musician_form.html'
    def get(self, request):
        return render(request,self.template_name,
                      {'form':self.form_class()})
    def post(self,request):
        bound_form=self.form_class(request.POST)
        if bound_form.is_valid():
            new_musician=bound_form.save()
            return redirect(new_musician)
        else:
            return render(request,self.template_name,
                          {'form':bound_form})

@require_authenticated_permission('FHLBuilder.musician_reader')
class MusicianUpdate(View):
    form_class=MusicianForm
    model=Musician
    template_name='FHLBuilder/musician_update.html'
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
    def get(self,request,slug):
        musician = self.get_object(slug)
        context={
           'form': self.form_class(instance=tag),
           'musician': musician,
        }
        return render(request,self.template_name,context)

    def post(self,request,slug):
        musician = self.get_object(slug)
        bound_form = self.form_class(request.POST,instance=musician)
        if bound_form.is_valid():
            new_musician = bound_form.save()
            return redirect(new_musician)
        else:
            context={
                'form': bound_form,
                'musician': musician,
            }
            return render(request,self.template_name,context)

@require_authenticated_permission('FHLBuilder.musician_builder')
class MusicianDelete(View):
    form_class=MusicianForm
    model = Musician
    template_name='FHLBuilder/musician_confirm_delete.html'
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
    def get(self,request,slug):
        musician = self.get_object(slug)
        return render(request,self.template_name,{'musician': musician})
    def post(self,request,slug):
        musician = self.get_object(slug)
        musician.delete()
        return redirect('builder_musician_list')
