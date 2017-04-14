# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db import models

from FHLBuilder.models import Tag, Song, CommonFile, Collection, Movie
from FHLBuilder.models import Director,Actor,Musician
from FHLBuilder.forms import TagForm, SongForm, CollectionForm, MovieForm
from FHLBuilder.forms import ActorForm, DirectorForm, MusicianForm
from FHLBuilder.forms import BasicCollectionForm

from django.template import RequestContext,loader

from django.views.generic import View

from FHLUser.decorators import require_authenticated_permission
from FHLBuilder.collection import add_tag, add_actor, add_director, add_collection
from FriendlyHomeLibrary import settings

from FHLReader import kodi

import os
import string

from collection import add_file
from . import choices

from .utility import to_str, slugCompare, object_path, songList, get_drive
from .query import findSongs, findMovies

# Views


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
        #songlist = tag.song_tags.all()
        slist = songList(tag.song_tags.all())
        mlist = tag.movie_tags.all()
        context = {'tag':tag,'songlist':slist, 'movielist':mlist}
        if 'playlist' in request.GET:
            context = {'tag':tag,'songlist':slist, 'movielist':mlist,'asPlayList':True}
        return render(request, self.template_name,context)

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


# songs
class SongList(View):
    template_name='FHLBuilder/song_list.html'
    def get(self,request):
        print("SongList GET")
        slist = songList(Song.objects.all())
        
        if 'playlist' in request.GET:
            print("As PlayList")
            context = {'listTitle': 'All Songs', 'songlist': slist, 'asPlayList':True}
            return render(request,self.template_name,context)
        context = {'listTitle': 'All Songs', 'songlist': slist, 'asPlayList':False }
        return render(request,self.template_name,context)
    def post(self,request):
        print("SongList POST")
        slist = songList(Song.objects.all())
        if 'playlist' in request.GET:
            print("As PlayList")
            context = {'listTitle': 'All Songs', 'songlist': slist, 'asPlayList':True}
            return render(request,self.template_name,context)
        context = {'listTitle': 'All Songs', 'songlist': slist, 'asPlayList':False }
        return render(request,self.template_name,context)


class SongDetailView(View):
    template_name = 'FHLBuilder/song_detail.html'
    form_class=SongForm
    def get(self,request,slug):
        song=get_object_or_404(Song,slug__iexact=slug)
        playit = object_path(song)
        print("HERE HERE HERE HERE %s user %s" % (playit,request.user))
        kodi.send_to_kodi(song)
        if 'tq' in request.GET and request.GET['tq']:
            tq = request.GET['tq']
            tqSlug = slugify(unicode(tq))
            new_tag = add_tag(tq,tqSlug)
            song.tags.add(new_tag)
        return render(request,
            self.template_name, {'song':song,
                                 'playit':playit,
                                 'objectForm':self.form_class(instance=song)})
    def post(self,request,slug):
        print ("SONG POST slug %s" % (slug))
        song=get_object_or_404(Song,slug__iexact=slug)
        playit = object_path(song)
        bound_form = self.form_class(request.POST,instance=song)
        if 'UpdateObject' in request.POST:
            #bound_form = self.form_class(request.POST,instance=movie)
            print("User pressed UpdateObject")
            if bound_form.is_valid():
                print("UPDATE with valid form")
                new_song = bound_form.save()
                song.title=new_song.title
                song.year=new_song.year
                song.save()
                formContext = {'song':song,'playit':playit,'objectForm':bound_form}
                return render(request,self.template_name, formContext)
            else:
                print("form is NOT valid")
                # no change in context

        # Still to do, should remove from the other lists so its not in more than 1
        if 'liked' in request.POST:
            print("LIKED by %s" % request.user)
            song.likes.add(request.user)
            song.save()
        if 'loved' in request.POST:
            print("LOVED")
            song.loves.add(request.user)
            song.save()
        if 'disliked' in request.POST:
            song.dislikes.add(request.user)
            song.save();
            print("DISLIKED")

        songContext = {'song':song,'playit':playit,'objectForm': self.form_class(instance=song)}
        return render(request,self.template_name, songContext)


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


#Collections
class CollectionList(View):
    template_name='FHLBuilder/collection_list.html'
    def get(self,request):
        print("CollectionList GET")
        tl = Collection.objects.all()
        test1 = {'tl': tl}
        return render(
          request,
          self.template_name,
          test1)


class CollectionMixins:
    def add_members(self, path, newCollection, formKind,formTag):
        print("ADD_MEMBERS path %s" % (path))
        drive = get_drive(newCollection.drive)
        for root, dirs, files in os.walk(os.path.join(settings.MY_MEDIA_FILES_ROOT,drive,path)):
            for obj in files:
                try:
                    print("ADD_MEMBERS root %s obj %s" % (root,to_str(obj)))
                    add_file(root,to_str(obj),path,newCollection,formKind,formTag)
                except UnicodeDecodeError:
                    print("ERROR unable to deal with filename- skipping in collection %s" % (newCollection.title))
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
            new_tag = add_tag(tq,tqSlug)
            clist=collection.song_set.all()
            for obj in clist:
                print("obj %s" % (obj.title))
                obj.tags.add(new_tag)
        songObjects = collection.song_set.all()
        mySongList = songList(songObjects)
        if 'playlist' in request.GET:
            context = {'collection':collection,'songlist':mySongList, 'asPlayList':True}
            return render(request,self.template_name,context)
        return render(request, self.template_name, {'collection':collection,'songlist':mySongList})


@require_authenticated_permission('FHLBuilder.collection_builder')
class CollectionFormView(View,CollectionMixins):
    form_class=CollectionForm
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
            print("collection with title %s and slug %s and filePath %s drive %d" % (cTitle,cSlug,cPath,cDrive))
            collection = add_collection(cTitle,cSlug,cPath,cDrive,False)
            
            print("collection with title %s and slug %s and filePath %s " % (collection.title,collection.slug,collection.filePath))
            self.add_members(cPath, collection, bound_form.cleaned_data['kind'],bound_form.cleaned_data['tag'])
            if collection.song_set.count() or collection.movie_set.count():
                # mp3 files create their own collection leaving this one empty
                # so it is not saved unless it has been populated
                collection.save()
                return redirect(collection)
            else:
                print("In Special Case in progress slug %s" % cSlug)
                musician_detail = 'FHLBuilder/musician_detail.html'
                for b in Musician.objects.all():
                    print("musician found %s" % b.slug)
                    if slugCompare(cSlug,b.slug):
                        return render(request, musician_detail, {'musician':b})
        return render(request,self.template_name,{'form':bound_form})

@require_authenticated_permission('FHLBuilder.collection_builder')
class CollectionUpdate(View,CollectionMixins):
    form_class=BasicCollectionForm
    model=Collection
    template_name='FHLBuilder/collection_update.html'
    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)
    def get(self,request,slug):
        print("CollectionUpdate POST")
        collection = self.get_object(slug)
        context={
           'form': self.form_class(instance=collection),
           'collection': collection,
        }
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


# movies
class MovieList(View):
    template_name='FHLBuilder/movie_list.html'
    def get(self,request):
        test1 = {'listTitle': 'All Movies', 'movielist': Movie.objects.all()}
        return render(
          request,
          self.template_name,
          test1)

class MovieDetailView(View):
    template_name = 'FHLBuilder/movie_detail.html'
    form_class=MovieForm

    def get(self,request,slug):
        print ("MovieDetail GET for %s" % slug)
        movie=get_object_or_404(Movie,slug__iexact=slug)
        if 'tq' in request.GET and request.GET['tq']:
            tq = request.GET['tq']
            tqSlug = slugify(unicode(tq))
            new_tag = add_tag(tq,tqSlug)
            movie.tags.add(new_tag)
        if 'actor' in request.GET and request.GET['actor']:
            act = request.GET['actor']
            actSlug = slugify(unicode(act))
            actSlug = actSlug + to_str('-act')
            new_actor = add_actor(act,actSlug)
            new_actor.movies.add(movie)
        if 'director' in request.GET and request.GET['director']:
            dtor = request.GET['director']
            dtorSlug = slugify(unicode(dtor))
            dtorSlug = dtorSlug + to_str('-dtr')
            new_dtor = add_director(dtor,dtorSlug)
            new_dtor.movies.add(movie)
        #playit = "mediafiles/" + movie.collection.filePath + '/' + movie.fileName
        playit = object_path(movie)
        return render(request, self.template_name, {'movie':movie,
                                                    'playit':playit,
                                                    'objectForm':self.form_class(instance=movie)})

    def post(self,request,slug):
        movie=get_object_or_404(Movie,slug__iexact=slug)
        #playit = "mediafiles/" + movie.collection.filePath + '/' + movie.fileName
        playit = object_path(movie)
        bound_form = self.form_class(request.POST,instance=movie)
        print("POST playit %s" % (playit))
        print ("MovieDetail POST for slug %s movie %s " % (slug,movie.title))

        if 'UpdateObject' in request.POST:
            #bound_form = self.form_class(request.POST,instance=movie)
            print("User pressed UpdateObject")
            if bound_form.is_valid():
                print("UPDATe with valid form")
                new_movie = bound_form.save()
                movie.title=new_movie.title
                movie.year=new_movie.year
                movie.save()
                formContext = {'movie':movie,'playit':playit,'objectForm':bound_form}
                return render(request,self.template_name, formContext)
            else:
                print("form is NOT valid")
                # no change in context

        # Still to do, should remove from the other lists so its not in more than 1
        if 'liked' in request.POST:
            print("LIKED by %s" % request.user)
            movie.likes.add(request.user)
            movie.save()
        if 'loved' in request.POST:
            print("LOVED")
            movie.loves.add(request.user)
            movie.save()
        if 'disliked' in request.POST:
            movie.dislikes.add(request.user)
            movie.save();
            print("DISLIKED")

        if 'StreamMovie' in request.POST:
            print("User pressed StreamMovie")
            try:
                clientip = request.META['REMOTE_ADDR']
            except KeyError:
                clientip = 'unknown'
            hostip = request.get_host()

            #playit = "/home/catherine/FHL/FriendlyHomeLibrary/static/mediafiles/" + movie.collection.filePath + '/' + movie.fileName
            #sstr = ("vlc -vvv %s --sout \'#rtp{dst=%s,port=1234,sdp=rtsp://%s:8080/test.sdp}\'" % (playit,clientip,hostip[:-5]))
            #print(sstr)
            #os.system(sstr)
            kodi.send_to_kodi(movie)
        else:
            print("No StreamMovie")

        #formContext = {'movie':movie,'playit':playit,'objectForm':bound_form}
        movieContext = {'movie':movie,'playit':playit,'objectForm': self.form_class(instance=movie)}
        return render(request,self.template_name, movieContext)


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

# Actors
class ActorList(View):
    template_name = 'FHLBuilder/actor_list.html'
    def get(self, request):
        context = {'tl': Actor.objects.all()}
        return render(request,self.template_name,context)

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
        context = {'tl': Director.objects.all()}
        return render(request,self.template_name,context)

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
        slist = songList(musician.songs.all())
        if 'playlist' in request.GET:
            context = {'musician':musician,'songlist':slist, 'asPlayList':True}
            return render(request,self.template_name,context)
        return render(request, self.template_name,
            {'musician':musician,'songlist':slist})

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

