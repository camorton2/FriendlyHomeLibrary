# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import string

from django.contrib.auth.models import User
from django.db import models
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

from FHLReader import kodi


#from .utility import to_str, slugCompare, object_path, songList, get_drive
#from .query import findSongs, findMovies

# Views

class HomePage(View):
    template_name = 'FHLBuilder/base_fhlbuilder.html'
    def get(self, request):
        return render(request,self.template_name,)

# Tags
class TagList(View):
    template_name = 'FHLBuilder/tag_list.html'
    def get(self, request):
        tl = models.Tag.objects.all()
        context = {'tl': tl}
        return render(request,self.template_name,context)

class TagDetailView(View):
    template_name = 'FHLBuilder/tag_detail.html'
    def get(self,request,slug):
        tag=get_object_or_404(models.Tag,slug__iexact=slug)
        slist = songList(tag.song_tags.all())
        mlist = tag.movie_tags.all()
        context = {'tag':tag,'songlist':slist, 'movielist':mlist}
        if 'playlist' in request.GET:
            context = {'tag':tag,
                'songlist':slist, 'movielist':mlist,
                'asPlayList':True}
        return render(request, self.template_name,context)

@require_authenticated_permission('FHLBuilder.tag_reader')
class TagFormView(View):
    form_class=forms.TagForm
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
    form_class=forms.TagForm
    model=models.Tag
    template_name='FHLBuilder/tag_update.html'
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
        
    def get(self,request,slug):
        tag = self.get_object(slug)
        context={'form': self.form_class(instance=tag),'tag': tag}
        return render(request,self.template_name,context)

    def post(self,request,slug):
        tag = self.get_object(slug)
        bound_form = self.form_class(request.POST,instance=tag)
        if bound_form.is_valid():
            new_tag = bound_form.save()
            return redirect(new_tag)
        else:
            context={'form': bound_form,'tag': tag,}
            return render(request,self.template_name,context)


# songs
class SongList(View):
    template_name='FHLBuilder/song_list.html'
    def get(self,request):
        print("SongList GET")
        slist = songList(models.Song.objects.all())
        title = ('All Songs %d' % models.Song.objects.count())
        if 'playlist' in request.GET:
            context = {'listTitle': title, 'songlist': slist, 
                'asPlayList':True}
            return render(request,self.template_name,context)
        context = {'listTitle': title, 'songlist': slist, 
            'asPlayList':False }
        return render(request,self.template_name,context)
        
    def post(self,request):
        print("SongList POST")
        slist = songList(Song.objects.all())
        title = ('All Songs %d' % Song.objects.count())
        if 'kodi_lf' in request.POST:
            kodi.songs_to_kodi_lf(slist)
        elif 'kodi-bf' in request.POST:
            print("User pressed kodi bf -- to be setup")
            kodi.songs_to__bf_kodi_bf(slist)            
        context = {'listTitle': title, 'songlist': slist, 
            'asPlayList':False }
        return render(request,self.template_name,context)


class SongDetailView(View):
    template_name = 'FHLBuilder/song_detail.html'
    form_class=forms.SongForm
    def get(self,request,slug):
        song=get_object_or_404(Song,slug__iexact=slug)
        playit = object_path(song)        
        if 'tq' in request.GET and request.GET['tq']:
            tq = request.GET['tq']
            tqSlug = slugify(unicode(tq))
            new_tag = collection.add_tag(tq,tqSlug)
            song.tags.add(new_tag)
        context = {'song':song,'playit':playit,
            'objectForm':self.form_class(instance=song)}
        return render(request, self.template_name, coontext)
        
    def post(self,request,slug):
        print ("SONG POST slug %s" % (slug))
        song=get_object_or_404(models.Song,slug__iexact=slug)
        playit = object_path(song)
        bound_form = self.form_class(request.POST,instance=song)
        if 'UpdateObject' in request.POST:
            if bound_form.is_valid():
                new_song = bound_form.save()
                song.title=new_song.title
                song.year=new_song.year
                song.save()
                formContext = {'song':song,'playit':playit,
                    'objectForm':bound_form}
                return render(request,self.template_name, formContext)

        # Still to do, should remove from the other lists so its not in more than 1
        elif 'liked' in request.POST:
            print("LIKED by %s" % request.user)
            song.likes.add(request.user)
            song.save()
        elif 'loved' in request.POST:
            print("LOVED")
            song.loves.add(request.user)
            song.save()
        elif 'disliked' in request.POST:
            song.dislikes.add(request.user)
            song.save();
            print("DISLIKED")
        elif 'kodi_lf' in request.POST:
            kodi.send_to_kodi_lf(song)
        elif 'kodi-bf' in request.POST:
            print("User pressed kodi bf -- to be setup")
            kodi.send_to_kodi_bf(song)
        songContext = {'song':song,'playit':playit,
            'objectForm': self.form_class(instance=song)}
        return render(request,self.template_name, songContext)


@require_authenticated_permission('FHLBuilder.song_builder')
class SongFormView(View):
    form_class=forms.SongForm
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
    form_class=forms.SongForm
    model=models.Song
    template_name='FHLBuilder/song_update.html'
    
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
        
    def get(self,request,slug):
        song = self.get_object(slug)
        context={'form': self.form_class(instance=song),
            'song': song,}
        return render(request,self.template_name,context)

    def post(self,request,slug):
        song = self.get_object(slug)
        bound_form = self.form_class(request.POST,instance=song)
        if bound_form.is_valid():
            new_song = bound_form.save()
            return redirect(new_song)
        else:
            context={'form': bound_form,'song': song}
            return render(request,self.template_name,context)


#Collections
class CollectionList(View):
    template_name='FHLBuilder/collection_list.html'
    def get(self,request):
        print("CollectionList GET")
        context = {'tl': models.Collection.objects.all()}
        return render(request,self.template_name,context)


class CollectionMixins:
    def add_members(self,path,newCollection,formKind,formTag):
        # Still to do, log errors
        print("ADD_MEMBERS path %s" % (path))
        drive = get_drive(newCollection.drive)
        for root, dirs, files in os.walk(os.path.join(settings.MY_MEDIA_FILES_ROOT,drive,path)):
            for obj in files:
                try:
                    print("ADD_MEMBERS root %s obj %s" % (root,to_str(obj)))
                    collection.add_file(root,to_str(obj),path,newCollection,formKind,formTag)
                except UnicodeDecodeError:
                    print("ERROR unable to deal with filename- skipping in collection %s" % (newCollection.title))
                except IOError:
                    print("ERROR IOError with filename- skipping in collection %s" % (newCollection.title))
            for dobj in dirs:
                newPath = path + '/' + dobj
                print("ADD_MEMBERS subdir %s " % (to_str(dobj)))
                self.add_members(newPath, newCollection,formKind,formTag)


class CollectionDetailView(View, CollectionMixins):
    template_name = 'FHLBuilder/collection_detail.html'
    
    def get(self,request,slug):
        print("CollectionDetail GET %s" % slug)
        collection=get_object_or_404(Collection,slug__iexact=slug)
        if 'tq' in request.GET and request.GET['tq']:
            tq = request.GET['tq']
            tqSlug = slugify(unicode(tq))
            new_tag = collection.add_tag(tq,tqSlug)
            clist=collection.song_set.all()
            for obj in clist:
                obj.tags.add(new_tag)
        songObjects = collection.song_set.all()
        mySongList = songList(songObjects)
        if 'playlist' in request.GET:
            context = {'collection':collection,'songlist':mySongList, 
               'asPlayList':True}
            return render(request,self.template_name,context)
        context = {'collection':collection,'songlist':mySongList}
        return render(request, self.template_name, context)


@require_authenticated_permission('FHLBuilder.collection_builder')
class CollectionFormView(View,CollectionMixins):
    form_class=forms.CollectionForm
    template_name = 'FHLBuilder/collection_form.html'
    
    def get(self, request):
        print("CollectionFormView GET")
        return render(request,self.template_name,{'form':self.form_class()})
        
    def post(self,request):
        print("CollectionFormView POST")
        bound_form=self.form_class(request.POST)
        if bound_form.is_valid():
            cPath = bound_form.cleaned_data['filePath']
            # (first,second) where second is the rightmost name in path
            cTitle = cPath.rpartition('/')[2]
            cSlug = slugify(unicode(cTitle))
            cDrive = bound_form.drive
            collection = collection.add_collection(cTitle,cSlug,cPath,cDrive,False)
            
            self.add_members(cPath, collection, 
                bound_form.cleaned_data['kind'],
                bound_form.cleaned_data['tag'])
            if collection.song_set.count() or collection.movie_set.count():
                # mp3 files create their own collection leaving this one empty
                # so it is not saved unless it has been populated
                collection.save()
                return redirect(collection)
            else:
                musician_detail = 'FHLBuilder/musician_detail.html'
                for b in Musician.objects.all():
                    bSlug=b.slug[:-4]
                    if slugCompare(cSlug,bSlug):
                        return render(request, musician_detail, {'musician':b})
        return render(request,self.template_name,{'form':bound_form})


@require_authenticated_permission('FHLBuilder.collection_builder')
class CollectionUpdate(View,CollectionMixins):
    form_class=forms.BasicCollectionForm
    model=models.Collection
    template_name='FHLBuilder/collection_update.html'
    
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
        
    def get(self,request,slug):
        print("CollectionUpdate POST")
        collection = self.get_object(slug)
        context={'form': self.form_class(instance=collection),
           'collection': collection}
        formKind = choices.UNKNOWN
        formTag = ''
        bound_form=self.form_class(request.POST)
        if bound_form.is_valid():
            formKind=bound_form.cleaned_data['kind']
            formTag=bound_form.cleaned_data['tag']
        # rescan for additional files
        self.add_members(collection.filePath, collection,formKind,formTag)
        collection.save()
        return render(request,self.template_name,context)

    def post(self,request,slug):
        print("Collection update POST")
        collection = self.get_object(slug)
        bound_form = self.form_class(request.POST,instance=collection)
        formKind = choices.UNKNOWN
        formTag = ''
        bound_form=self.form_class(request.POST)
        if bound_form.is_valid():
            formKind=bound_form.cleaned_data['kind']
            formTag=bound_form.cleaned_data['tag']
        # rescan for additional files
        self.add_members(collection.filePath, collection,formKind,formTag)
        collection.save()
        return redirect(collection)


# Video Lists
class MovieList(View):
    template_name='FHLBuilder/movie_list.html'
    def get(self,request):
        title = ('All Movies')
        movielist = []
        for mv in models.Movie.objects.all():
            if mv.fileKind == 'MV':
                movielist.append(mv)
        context = {'listTitle': title, 'movielist': movielist}
        return render(request,self.template_name,context)


class ConcertList(View):
    template_name='FHLBuilder/movie_list.html'
    def get(self,request):
        title = ('All Concerts')
        movielist = []
        for mv in models.Movie.objects.all():
            if mv.fileKind == 'CC':
                movielist.append(mv)
        context = {'listTitle': title, 'movielist': movielist}
        return render(request,self.template_name,context)


class TVList(View):
    template_name='FHLBuilder/movie_list.html'
    def get(self,request):
        title = ('All TV Shows')
        movielist = []
        for mv in models.Movie.objects.all():
            if mv.fileKind == 'TV':
                movielist.append(mv)
        context = {'listTitle': title, 'movielist': movielist}
        return render(request,self.template_name,context)


class MiniSeriesList(View):
    template_name='FHLBuilder/movie_list.html'
    def get(self,request):
        title = ('All Mini Series')
        movielist = []
        for mv in models.Movie.objects.all():
            if mv.fileKind == 'MS':
                movielist.append(mv)
        context = {'listTitle': title, 'movielist': movielist}
        return render(request,self.template_name,context)


class MovieDetailView(View):
    template_name = 'FHLBuilder/movie_detail.html'
    form_class=forms.MovieForm

    def get(self,request,slug):
        print ("MovieDetail GET for %s" % slug)
        movie=get_object_or_404(Movie,slug__iexact=slug)
        if 'tq' in request.GET and request.GET['tq']:
            tq = request.GET['tq']
            tqSlug = slugify(unicode(tq))
            new_tag = collection.add_tag(tq,tqSlug)
            movie.tags.add(new_tag)
        if 'actor' in request.GET and request.GET['actor']:
            act = request.GET['actor']
            actSlug = slugify(unicode(act+'-act'))
            new_actor = collection.add_actor(act,actSlug)
            new_actor.movies.add(movie)
        if 'director' in request.GET and request.GET['director']:
            dtr = request.GET['director']
            dtrSlug = slugify(unicode(dtor+'-dtr'))
            new_dtr = collection.add_director(dtor,dtrSlug)
            new_dtr.movies.add(movie)
        if 'musician' in request.GET and request.GET['musician']:
            mus = request.GET['musician']
            mSlug = slugify(unicode(mus+'-mus'))
            new_mus = collection.add_musician(mus,mSlug)
            new_mus.concerts.add(movie)            
        playit = object_path(movie)
        context = {'movie':movie,'playit':playit,
            'objectForm':self.form_class(instance=movie)}
        return render(request, self.template_name,context)

    def post(self,request,slug):
        print ("MovieDetail POST for slug %s movie %s " % (slug,movie.title))
        movie=get_object_or_404(Movie,slug__iexact=slug)
        playit = object_path(movie)
        bound_form = self.form_class(request.POST,instance=movie)
        if 'UpdateObject' in request.POST:
            if bound_form.is_valid():
                new_movie = bound_form.save()
                movie.title=new_movie.title
                movie.year=new_movie.year
                movie.save()
                formContext = {'movie':movie,'playit':playit,'objectForm':bound_form}
                return render(request,self.template_name, formContext)
        # Still to do, should remove from the other lists so its not in more than 1
        if 'liked' in request.POST:
            movie.likes.add(request.user)
            movie.save()
        elif 'loved' in request.POST:
            movie.loves.add(request.user)
            movie.save()
        elif 'disliked' in request.POST:
            movie.dislikes.add(request.user)
            movie.save();
        elif 'StreamMovie' in request.POST:
            kodi.stream_to_vlc(movie,request)
        elif 'kodi_lf' in request.POST:
            kodi.send_to_kodi_lf(movie)
        elif 'kodi-bf' in request.POST:
            kodi.send_to_kodi_bf(movie)
        elif 'vlc_plugin' in request.POST:
            movieContext = {'movie':movie,'playit':playit,
                'objectForm': self.form_class(instance=movie),
                'vlcPlugin':True}
        movieContext = {'movie':movie,'playit':playit,
            'objectForm': self.form_class(instance=movie)}
        return render(request,self.template_name, movieContext)


@require_authenticated_permission('FHLBuilder.movie_builder')
class MovieFormView(View):
    form_class=forms.MovieForm
    template_name = 'FHLBuilder/movie_form.html'
    
    def get(self, request):
        context = {'form':self.form_class()}
        return render(request,self.template_name,context)
                      
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
    form_class=forms.MovieForm
    model=models.Movie
    template_name='FHLBuilder/movie_update.html'
    
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
        
    def get(self,request,slug):
        movie = self.get_object(slug)
        context={
           'form': self.form_class(instance=movie),
           'movie': movie}
        return render(request,self.template_name,context)

    def post(self,request,slug):
        movie = self.get_object(slug)
        bound_form = self.form_class(request.POST,instance=movie)
        if bound_form.is_valid():
            new_movie = bound_form.save()
            return redirect(new_movie)
        else:
            context={'form': bound_form,'movie': movie}
            return render(request,self.template_name,context)


# Actors
class ActorList(View):
    template_name = 'FHLBuilder/actor_list.html'
    
    def get(self, request):
        context = {'tl': models.Actor.objects.all()}
        return render(request,self.template_name,context)

class ActorDetailView(View):
    template_name = 'FHLBuilder/actor_detail.html'
    
    def get(self,request,slug):
        actor=get_object_or_404(Actor,slug__iexact=slug)
        return render(request, self.template_name, {'actor':actor})

@require_authenticated_permission('FHLBuilder.actor_reader')
class ActorFormView(View):
    form_class=forms.ActorForm
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
    form_class=forms.ActorForm
    model=models.Actor
    template_name='FHLBuilder/actor_update.html'
    
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
        
    def get(self,request,slug):
        actor = self.get_object(slug)
        context={'form': self.form_class(instance=tag), 'actor': actor}
        return render(request,self.template_name,context)

    def post(self,request,slug):
        actor = self.get_object(slug)
        bound_form = self.form_class(request.POST,instance=actor)
        if bound_form.is_valid():
            new_actor = bound_form.save()
            return redirect(new_actor)
        else:
            context={'form': bound_form,'actor': actor}
            return render(request,self.template_name,context)


# Directors
class DirectorList(View):
    template_name = 'FHLBuilder/director_list.html'
    
    def get(self, request):
        context = {'tl': models.Director.objects.all()}
        return render(request,self.template_name,context)


class DirectorDetailView(View):
    template_name = 'FHLBuilder/director_detail.html'
    def get(self,request,slug):
        director=get_object_or_404(Director,slug__iexact=slug)
        return render(request, self.template_name, {'director':director})


@require_authenticated_permission('FHLBuilder.director_reader')
class DirectorFormView(View):
    form_class=forms.DirectorForm
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
    form_class=forms.DirectorForm
    model=models.Director
    template_name='FHLBuilder/director_update.html'
    
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
        
    def get(self,request,slug):
        director = self.get_object(slug)
        context={'form': self.form_class(instance=tag),
           'director': director}
        return render(request,self.template_name,context)

    def post(self,request,slug):
        director = self.get_object(slug)
        bound_form = self.form_class(request.POST,instance=director)
        if bound_form.is_valid():
            new_director = bound_form.save()
            return redirect(new_director)
        else:
            context={'form': bound_form,'director': director}
            return render(request,self.template_name,context)


# Musicians
class MusicianList(View):
    template_name = 'FHLBuilder/musician_list.html'
    
    def get(self, request):
        context = {'tl': models.Musician.objects.all()}
        return render(request,self.template_name,context)


class MusicianDetailView(View):
    template_name = 'FHLBuilder/musician_detail.html'
    
    def get(self,request,slug):
        musician=get_object_or_404(Musician,slug__iexact=slug)
        slist = songList(musician.songs.all())
        if 'playlist' in request.GET:
            context = {'musician':musician,'songlist':slist, 'asPlayList':True}
            return render(request,self.template_name,context)
        return render(request, self.template_name,
            {'musician':musician,'songlist':slist})


@require_authenticated_permission('FHLBuilder.musician_reader')
class MusicianFormView(View):
    form_class=forms.MusicianForm
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
    form_class=forms.MusicianForm
    model=models.Musician
    template_name='FHLBuilder/musician_update.html'
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
        
    def get(self,request,slug):
        musician = self.get_object(slug)
        context={'form': self.form_class(instance=tag),
            'musician': musician}
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

