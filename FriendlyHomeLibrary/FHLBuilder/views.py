# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import string

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
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
        slist = utility.link_file_list(tag.song_tags.all())
        plist = utility.link_file_list(tag.picture_tags.all())
        mlist = tag.movie_tags.all()
        context = {'tag':tag,'songlist':slist, 'movielist':mlist}
        if 'playlist' in request.GET:
            context = {'tag':tag,
                'songlist':slist, 
                'movielist':mlist,
                'picturelist':plist,
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
        #print("SongList GET")
        slist = utility.link_file_list(models.Song.objects.all())
        title = ('All Songs %d' % models.Song.objects.count())
        if 'playlist' in request.GET:
            context = {'listTitle': title, 'songlist': slist,
                'asPlayList':True}
            return render(request,self.template_name,context)
        context = {'listTitle': title, 'songlist': slist,
            'asPlayList':False }
        return render(request,self.template_name,context)

    def post(self,request):
        #print("SongList POST")
        slist = utility.link_file_list(models.Song.objects.all())
        title = ('All Songs %d' % models.Song.objects.count())
        if 'kodi_lf' in request.POST:
            kodi.songs_to_kodi_lf(slist)
        elif 'kodi-bf' in request.POST:
            #print("User pressed kodi bf -- to be setup")
            kodi.songs_to__bf_kodi_bf(slist)
        context = {'listTitle': title, 'songlist': slist,
            'asPlayList':False }
        return render(request,self.template_name,context)


class SongDetailView(View):
    template_name = 'FHLBuilder/song_detail.html'
    form_class=forms.SongForm

    def get(self,request,slug):
        song=get_object_or_404(models.Song,slug__iexact=slug)
        playit = utility.object_path(song)
        if 'tq' in request.GET and request.GET['tq']:
            tq = request.GET['tq']
            tqSlug = slugify(unicode(tq))
            new_tag = collection.add_tag(tq,tqSlug)
            song.tags.add(new_tag)
        context = {'song':song,'playit':playit,
            'objectForm':self.form_class(instance=song)}
        return render(request, self.template_name, context)

    def post(self,request,slug):
        #print ("SONG POST slug %s" % (slug))
        song=get_object_or_404(models.Song,slug__iexact=slug)
        playit = utility.object_path(song)
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
            #print("LIKED by %s" % request.user)
            song.likes.add(request.user)
            song.save()
        elif 'loved' in request.POST:
            #print("LOVED")
            song.loves.add(request.user)
            song.save()
        elif 'disliked' in request.POST:
            song.dislikes.add(request.user)
            song.save();
            #print("DISLIKED")
        elif 'kodi_lf' in request.POST:
            kodi.send_to_kodi_lf(song)
        elif 'kodi-bf' in request.POST:
            #print("User pressed kodi bf -- to be setup")
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
        #print("CollectionList GET")
        allc = models.Collection.objects.all()
        songc,moviec,picturec,variousc = utility.collection_sets(allc)
        context = {
            'movies': moviec,
            'songs': songc,
            'pictures': picturec,
            'various': variousc
            }
        return render(request,self.template_name,context)


class CollectionMixins:
    def handle_collection(self,path,drive,kind,tag):
        spath = path.replace('/','-')
        slug = slugify( unicode( '%s' % (spath) ))
        title = path.replace('/','-')
        nc = collection.add_collection(title,slug,path,drive,False)
        return nc

    def add_members(self,path,drive,kind,tag):
        # Still to do, log errors
        #print("ADD_MEMBERS path %s" % (path))
        sDrive = utility.get_drive(drive)
        album = None
        artist = None
        setPath = os.path.join(settings.MY_MEDIA_FILES_ROOT,sDrive)
        for root, dirs, files in os.walk(os.path.join(setPath,path)):
            myroot = utility.to_str(root[len(setPath):])
            #print("LOOP myroot %s dirs %s files %s\n" % (myroot,dirs,files))
            album = self.handle_collection(myroot,drive,kind,tag)
            for obj in files:
                try:
                    #print("ADD_MEMBERS myroot %s obj %s" % (myroot,utility.to_str(obj)))
                    album,artist = collection.add_file(root,utility.to_str(obj),myroot,album,kind,tag)
                except UnicodeDecodeError:
                    print("ERROR unable to deal with filename- skipping in collection %s" % (album.title))
                except IOError:
                    print("ERROR IOError with filename- skipping in collection %s" % (album.title))
        return album,artist

class CollectionDetailView(View, CollectionMixins):
    template_name = 'FHLBuilder/collection_detail.html'

    def get(self,request,slug):
        #print("CollectionDetail GET %s" % slug)
        collection=get_object_or_404(models.Collection,slug__iexact=slug)
        if 'tq' in request.GET and request.GET['tq']:
            tq = request.GET['tq']
            tqSlug = slugify(unicode(tq))
            new_tag = collection.add_tag(tq,tqSlug)
            clist=collection.song_set.all()
            for obj in clist:
                obj.tags.add(new_tag)
        songObjects = collection.song_set.all()
        mySongList = utility.link_file_list(songObjects)
        pictureObjects = collection.picture_set.all()
        myPictureList = utility.link_file_list(pictureObjects)
        
        if 'playlist' in request.GET:
            context = {
                'collection':collection,
                'songlist':mySongList,
                'picturelist':myPictureList,
                'asPlayList':True}
            return render(request,self.template_name,context)
        context = {
            'collection':collection,
            'songlist':mySongList,
            'picturelist':myPictureList}
        return render(request, self.template_name, context)


@require_authenticated_permission('FHLBuilder.collection_builder')
class CollectionFormView(View,CollectionMixins):
    form_class=forms.CollectionForm
    template_name = 'FHLBuilder/collection_form.html'

    def get(self, request):
        #print("CollectionFormView GET")
        return render(request,self.template_name,{'form':self.form_class()})

    def post(self,request):
        #print("CollectionFormView POST")
        bound_form=self.form_class(request.POST)
        if bound_form.is_valid():
            album,artist = self.add_members(
                bound_form.cleaned_data['filePath'],
                bound_form.drive,
                bound_form.cleaned_data['kind'],
                bound_form.cleaned_data['tag'])

            if artist is not None:
                # display the page for the musician
                #return render(request, musician_detail, {'musician':artist})
                return redirect(artist)
            elif album.song_set.count() or album.movie_set.count():
                # new album is not empty, save and redirect
                album.save()
                return redirect(album)
                
        # otherwise display the list of all collections
        return redirect(reverse('builder_collection_list'))


@require_authenticated_permission('FHLBuilder.collection_builder')
class CollectionUpdate(View,CollectionMixins):
    form_class=forms.BasicCollectionForm
    model=models.Collection
    template_name='FHLBuilder/collection_update.html'

    def get_object(self,slug):
        return get_object_or_404(self.model,slug=slug)

    def get(self,request,slug):
        #print("CollectionUpdate POST")
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
        #print("Collection update POST")
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

class DocumentaryList(View):
    template_name='FHLBuilder/movie_list.html'
    def get(self,request):
        title = ('Documentary')
        movielist = []
        for mv in models.Movie.objects.all():
            if mv.fileKind == 'DD':
                movielist.append(mv)
        context = {'listTitle': title, 'movielist': movielist}
        return render(request,self.template_name,context)

class MiniMovieList(View):
    template_name='FHLBuilder/movie_list.html'
    def get(self,request):
        title = ('Mini-Movie')
        movielist = []
        for mv in models.Movie.objects.all():
            if mv.fileKind == 'MM':
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
        movie=get_object_or_404(models.Movie,slug__iexact=slug)
        if 'tq' in request.GET and request.GET['tq']:
            tq = request.GET['tq']
            tqSlug = slugify(unicode(tq))
            new_tag = collection.add_tag(tq,tqSlug)
            movie.tags.add(new_tag)
            movie.save()
        if 'actor' in request.GET and request.GET['actor']:
            act = request.GET['actor']
            actSlug = slugify(unicode(act+'-act'))
            new_actor = collection.add_actor(act,actSlug)
            new_actor.movies.add(movie)
            new_actor.save()
        if 'director' in request.GET and request.GET['director']:
            dtr = request.GET['director']
            dtrSlug = slugify(unicode(dtr+'-dtr'))
            new_dtr = collection.add_director(dtr,dtrSlug)
            new_dtr.movies.add(movie)
            new_dtr.save()
        if 'musician' in request.GET and request.GET['musician']:
            mus = request.GET['musician']
            mSlug = slugify(unicode(mus+'-mus'))
            new_mus = collection.add_musician(mus,mSlug)
            new_mus.concerts.add(movie)
            new_mus.save()
        playit = utility.object_path(movie)
        context = {'movie':movie,'playit':playit,
            'objectForm':self.form_class(instance=movie)}
        return render(request, self.template_name,context)

    def post(self,request,slug):
        movie=get_object_or_404(models.Movie,slug__iexact=slug)
        print ("MovieDetail POST for slug %s movie %s " % (slug,movie.title))
        playit = utility.object_path(movie)
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
        actor=get_object_or_404(models.Actor,slug__iexact=slug)
        return render(request, self.template_name, {'actor':actor})


# Directors
class DirectorList(View):
    template_name = 'FHLBuilder/director_list.html'

    def get(self, request):
        context = {'tl': models.Director.objects.all()}
        return render(request,self.template_name,context)


class DirectorDetailView(View):
    template_name = 'FHLBuilder/director_detail.html'
    def get(self,request,slug):
        director=get_object_or_404(models.Director,slug__iexact=slug)
        return render(request, self.template_name, {'director':director})


# Musicians
class MusicianList(View):
    template_name = 'FHLBuilder/musician_list.html'

    def get(self, request):
        context = {'tl': models.Musician.objects.all()}
        return render(request,self.template_name,context)


class MusicianDetailView(View):
    template_name = 'FHLBuilder/musician_detail.html'

    def get(self,request,slug):
        musician=get_object_or_404(models.Musician,slug__iexact=slug)
        slist = utility.link_file_list(musician.songs.all())
        if 'playlist' in request.GET:
            context = {'musician':musician,'songlist':slist, 'asPlayList':True}
            return render(request,self.template_name,context)
        return render(request, self.template_name,
            {'musician':musician,'songlist':slist})


# pictures
class PictureList(View):
    template_name='FHLBuilder/picture_list.html'
    def get(self,request):
        #print("PictureList GET")
        count = models.Picture.objects.count()
        plist = utility.link_file_list(models.Picture.objects.all())
        title = ('All Pictures %d' % count)
        context = {'listTitle': title, 'picturelist': plist, 
            'pictureCount':count}
        return render(request,self.template_name,context)

    def post(self,request):
        #print("PictureList POST")
        plist = utility.link_file_list(models.Picture.objects.all())
        title = ('All Pictures %d' % models.Picture.objects.count())
        context = {'listTitle': title, 'picturelist': plist,
            'pictureCount':count }
        return render(request,self.template_name,context)


class PictureDetailView(View):
    template_name = 'FHLBuilder/picture_detail.html'
    form_class=forms.PictureForm

    def get(self,request,slug):
        picture=get_object_or_404(models.Picture,slug__iexact=slug)
        playit = utility.object_path(picture)
        if 'tq' in request.GET and request.GET['tq']:
            tq = request.GET['tq']
            tqSlug = slugify(unicode(tq))
            new_tag = collection.add_tag(tq,tqSlug)
            picture.tags.add(new_tag)
        context = {'picture':picture,'playit':playit,
            'objectForm':self.form_class(instance=picture)}
        return render(request, self.template_name, context)

    def post(self,request,slug):
        #print ("PICTURE POST slug %s" % (slug))
        picture=get_object_or_404(models.Picture,slug__iexact=slug)
        playit = utility.object_path(picture)
        bound_form = self.form_class(request.POST,instance=picture)
        if 'UpdateObject' in request.POST:
            if bound_form.is_valid():
                new_picture = bound_form.save()
                picture.title=new_picture.title
                picture.year=new_picture.year
                picture.save()
                formContext = {'picture':picture,'playit':playit,
                    'objectForm':bound_form}
                return render(request,self.template_name, formContext)

        # Still to do, should remove from the other lists so its not in more than 1
        elif 'liked' in request.POST:
            #print("LIKED by %s" % request.user)
            picture.likes.add(request.user)
            picture.save()
        elif 'loved' in request.POST:
            #print("LOVED")
            picture.loves.add(request.user)
            picture.save()
        elif 'disliked' in request.POST:
            picture.dislikes.add(request.user)
            picture.save();
            #print("DISLIKED")
        pictureContext = {'picture':picture,'playit':playit,
            'objectForm': self.form_class(instance=picture)}
        return render(request,self.template_name, pictureContext)

