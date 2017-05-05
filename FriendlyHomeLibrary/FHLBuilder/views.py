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
import FHLBuilder.view_utility as vu

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
        #print("TagList GET")
        context = {'tags': models.Tag.objects.all()}
        return render(request,self.template_name,context)


class TagDetailView(View):
    template_name = 'FHLBuilder/tag_detail.html'
    def get(self,request,slug):
        #print("TagDetailView GET")
        tag=get_object_or_404(models.Tag,slug__iexact=slug)
        songs = tag.song_tags.all()
        pictures = tag.picture_tags.all()
        movies = tag.movie_tags.all()
        return vu.collection_view(request,songs,pictures,movies,[],tag.name)

# songs
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
        elif 'musician' in request.GET and request.GET['musician']:
            mus = request.GET['musician']
            mSlug = slugify(unicode(mus+'-mus'))
            new_mus = collection.add_musician(mus,mSlug)
            new_mus.songs.add(song)
            new_mus.save()
        elif 'pref' in request.GET and request.GET.get('pref'):
            #print("preference selection")
            query.handle_pref(song, request.GET.get('pref'),request.user)

        love,like,dislike = query.my_preference(song,request.user)

        context = {
            'song':song,
            'playit':playit,
            'love':love,'like':like,'dislike':dislike,
            'objectForm':self.form_class(instance=song)}
        return render(request, self.template_name, context)

    def post(self,request,slug):
        #print ("SONG POST slug %s" % (slug))
        song=get_object_or_404(models.Song,slug__iexact=slug)
        playit = utility.object_path(song)
        love,like,dislike = query.my_preference(song,request.user)

        bound_form = self.form_class(request.POST,instance=song)
        if 'UpdateObject' in request.POST:
            if bound_form.is_valid():
                new_song = bound_form.save()
                song.title=new_song.title
                song.year=new_song.year
                song.save()
                formContext = {
                    'song':song,'playit':playit,
                    'love':love,'like':like,'dislike':dislike,
                    'objectForm':bound_form}
                return render(request,self.template_name, formContext)
        _ = kodi.playback_requests(song,request)

        songContext = {
            'song':song,
            'playit':playit,
            'love':love,'like':like,'dislike':dislike,
            'objectForm': self.form_class(instance=song)}
        return render(request,self.template_name, songContext)


# LISTS
class CollectionList(View):
    def get(self,request):
        #print("CollectionList GET")
        kind = vu.select_kind(request)
        clist = query.handle_collection_kind(
            models.Collection.objects.all(), kind)
        title = 'Library Collections'
        return vu.view_list(request,clist,title,kind)


class FileList(View):
    def get(self,request):
        #print("CollectionList GET")
        kind = vu.select_kind(request)
        olist = []
        if kind == choices.SONG:
            olist = models.Song.objects.all()
            title = ('All Songs %d' % olist.count())
            return vu.collection_view(request, olist, [], [],[], title, True, kind)
        elif kind == choices.PICTURE:
            olist = models.Picture.objects.all()
            title = ('All Pictures %d' % olist.count())
            return vu.collection_view(request, [], olist, [],[], title, True, kind)
        # Videos
        else:
            olist,title =  vu.movies_bykind(kind)
        #return vu.view_list(request,olist,title,kind)
        return vu.collection_view(request, [], [], olist, [], title,True, kind)

# Collections

class CollectionMixins:
    def handle_collection(self,path,drive,kind,tag):
        spath = path.replace('/','-')
        upath = unicode('%s' % (spath))
        slug = slugify(upath)
        title = upath
        nc = collection.add_collection(title,slug,path,drive,False)
        return nc

    def add_members(self,path,drive,kind,tag, knownCollection = None):
        # Still to do, log errors
        #print("ADD_MEMBERS path %s" % (path))
        sDrive = utility.get_drive(drive)
        album = None
        artist = None
        setPath = os.path.join(settings.MY_MEDIA_FILES_ROOT,sDrive)
        scanPath = os.path.join(setPath,path)
        goodPath = os.path.exists(scanPath)
        #print('setPath %s exists %s' % (scanPath,goodPath))
        if not goodPath:
            message = ('ERROR path does not exist check drive setup %s' % scanPath)
            utility.log(message)
            raise kodi.MyException(message)
        for root, dirs, files in os.walk(scanPath):
            try:
                #myroot = utility.to_str(root[len(setPath):])
                myroot = unicode(root[len(setPath):])
                utility.log("START myroot %s dirs %s files %s\n" % (myroot,dirs,files))
                if knownCollection is None:
                    album = self.handle_collection(myroot,drive,kind,tag)
                else:
                    album = knownCollection
                for obj in files:
                    try:
                        #print("ADD_MEMBERS myroot %s obj %s" % (myroot,utility.to_str(obj)))
                        album,artist = collection.add_file(
                            unicode(root),
                            unicode(obj),
                            myroot,
                            album,
                            kind,
                            tag)
                    except UnicodeDecodeError:
                        print("UnicodeDecodeError file in collection %s" % (album.title))
                    except IOError:
                        print("IOError file in collection %s file %s" % (album.title,obj))
            except UnicodeDecodeError:
                print("UnicodeDecodeError collection")
        return album,artist

class CollectionDetailView(View, CollectionMixins):


    def get(self,request,slug):
        # print("CollectionDetail GET %s" % slug)
        target=get_object_or_404(models.Collection,slug__iexact=slug)

        songs = target.song_set.all()
        pictures = target.picture_set.all()
        movies = target.movie_set.all()
        artists = target.album_musicians.all()

        return vu.collection_view(request, songs, pictures, movies,
            artists,target.title, False, choices.MOVIE, True)


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
        else:
            # in the case of an invalid form, redirect to the
            # bound form which has the ValidationError
            context = {
                'form':bound_form
                }
            return render(request,self.template_name,context)
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
        print("CollectionUpdate GET")
        target = self.get_object(slug)

        context={'form': self.form_class(instance=target),
           'collection': collection}
        return render(request,self.template_name,context)

    def post(self,request,slug):
        print("CollectionUpdate POST")
        target = self.get_object(slug)
        bound_form = self.form_class(request.POST,instance=target)
        if bound_form.is_valid():
            #print("form valid rescan")
            try:
                album,artist = self.add_members(
                    target.filePath,
                    target.drive,
                    bound_form.cleaned_data['kind'],
                    bound_form.cleaned_data['tag'],
                    target
                    )
            except kodi.MyException,ex:
                message = ex.message
                print('caught %s' % message)
                context = {'form':bound_form,'message':message}
                return render(request,self.template_name,context)
            if artist is not None:
                print("redirect artist")
                # display the page for the musician
                #return render(request, musician_detail, {'musician':artist})
                return redirect(artist)
            elif album.song_set.count() or album.movie_set.count():
                print("redirect album")
                # new album is not empty, save and redirect
                album.save()
                return redirect(album)
        else:
            print("form not valid")
            # in the case of an invalid form, redirect to the
            # bound form which has the ValidationError
            context = {
                'form':bound_form
                }
            return render(request,self.template_name,context)
        # otherwise redirect to target collection
        return redirect(target)


# Movies
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
        elif 'actor' in request.GET and request.GET['actor']:
            act = request.GET['actor']
            actSlug = slugify(unicode(act+'-act'))
            new_actor = collection.add_actor(act,actSlug)
            new_actor.movies.add(movie)
            new_actor.save()
        elif 'director' in request.GET and request.GET['director']:
            dtr = request.GET['director']
            dtrSlug = slugify(unicode(dtr+'-dtr'))
            new_dtr = collection.add_director(dtr,dtrSlug)
            new_dtr.movies.add(movie)
            new_dtr.save()
        elif 'musician' in request.GET and request.GET['musician']:
            mus = request.GET['musician']
            mSlug = slugify(unicode(mus+'-mus'))
            new_mus = collection.add_musician(mus,mSlug)
            new_mus.concerts.add(movie)
            new_mus.save()
        elif 'pref' in request.GET and request.GET.get('pref'):
            print("preference selection")
            query.handle_pref(movie, request.GET.get('pref'),request.user)
        playit = utility.object_path(movie)
        print(playit)
        love,like,dislike = query.my_preference(movie,request.user)
        context = {'movie':movie,
            'playit':playit,
            'love':love,'like':like,'dislike':dislike,
            'objectForm':self.form_class(instance=movie)}
        return render(request, self.template_name,context)

    def post(self,request,slug):
        movie=get_object_or_404(models.Movie,slug__iexact=slug)
        love,like,dislike = query.my_preference(movie,request.user)
        print ("MovieDetail POST for slug %s movie %s " % (slug,movie.title))
        playit = utility.object_path(movie)
        bound_form = self.form_class(request.POST,instance=movie)
        if 'UpdateObject' in request.POST:
            if bound_form.is_valid():
                new_movie = bound_form.save()
                movie.title=new_movie.title
                movie.year=new_movie.year
                movie.save()
                formContext = {
                    'movie':movie,
                    'playit':playit,
                    'love':love,'like':like,'dislike':dislike,
                    'objectForm':bound_form}
                return render(request,self.template_name, formContext)
        message = ''
        try:
            message = u'success'
            vlcPlugin = kodi.playback_requests(movie,request)
        except kodi.MyException,ex:
            message = ex.message
            print('Caught %s' % ex.message)
            vlcPlugin=False

        movieContext = {
            'movie':movie,
            'playit':playit,
            'love':love,'like':like,'dislike':dislike,
            'objectForm': self.form_class(instance=movie),
            'vlcPlugin':vlcPlugin,
            'message':message}
        print('render with message %s' % message)
        return render(request,self.template_name, movieContext)


# Artists:   Actors,Directors,Musicians
class ActorList(View):
    template_name = 'FHLBuilder/actor_list.html'
    def get(self, request):
        context = {'tl': models.Actor.objects.all()}
        return render(request,self.template_name,context)


class DirectorList(View):
    template_name = 'FHLBuilder/director_list.html'
    def get(self, request):
        context = {'tl': models.Director.objects.all()}
        return render(request,self.template_name,context)


class MusicianList(View):
    template_name = 'FHLBuilder/musician_list.html'
    def get(self, request):
        context = {'tl': models.Musician.objects.all()}
        return render(request,self.template_name,context)


class ActorDetailView(View):
    def get(self,request,slug):
        actor=get_object_or_404(models.Actor,slug__iexact=slug)
        movies = actor.movies.all()
        title = ('Movies with actor %s' % actor.fullName)
        return vu.collection_view(request, [], [], movies,[],title)
    

class DirectorDetailView(View):
    def get(self,request,slug):
        director=get_object_or_404(models.Director,slug__iexact=slug)
        movies = director.movies.all()
        title = ('Movies directed by %s' % director.fullName)
        return vu.collection_view(request, [], [], movies,[],title)


class MusicianDetailView(View):
    """
    Musician detail does not use the common display utility
    because the musician view displays albums and songs
    """
    template_name = 'FHLBuilder/musician_detail.html'

    def get(self,request,slug):
        musician=get_object_or_404(models.Musician,slug__iexact=slug)
        songs = musician.songs.all()
        slist = utility.link_file_list(songs)
        asPlayList = False
        if 'playlist' in request.GET:
            asPlayList = True
        message = ''
        try:
            if songs and kodi.playlist_requests(songs,request):
                message = u'success - songs sent'
        except kodi.MyException,ex:
            message = ex.message
            print('Caught %s' % ex.message)            
            
        context = {
            'musician':musician,
            'songlist':slist, 
            'asPlayList':asPlayList,
            'message':message}
        return render(request,self.template_name,context)


# pictures
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
        elif 'pref' in request.GET and request.GET.get('pref'):
            query.handle_pref(picture, request.GET.get('pref'),request.user)
        love,like,dislike = query.my_preference(picture,request.user)

        context = {
            'picture':picture,'playit':playit,
            'love':love,'like':like,'dislike':dislike,
            'objectForm':self.form_class(instance=picture)}
        return render(request, self.template_name, context)

    def post(self,request,slug):
        #print ("PICTURE POST slug %s" % (slug))
        picture=get_object_or_404(models.Picture,slug__iexact=slug)
        playit = utility.object_path(picture)
        love,like,dislike = query.my_preference(picture,request.user)
        bound_form = self.form_class(request.POST,instance=picture)
        if 'UpdateObject' in request.POST:
            if bound_form.is_valid():
                new_picture = bound_form.save()
                picture.title=new_picture.title
                picture.year=new_picture.year
                picture.save()
                formContext = {
                    'picture':picture,
                    'playit':playit,
                    'love':love,'like':like,'dislike':dislike,
                    'objectForm':bound_form}
                return render(request,self.template_name, formContext)

        pictureContext = {
            'picture':picture,'playit':playit,
            'love':love,'like':like,'dislike':dislike,
            'objectForm': self.form_class(instance=picture)}
        return render(request,self.template_name, pictureContext)

# Diagnostics, for playing around, updating database etc
class DiagnosticsView(View):
    template_name = 'FHLBuilder/diagnostics.html'
    def get(self,request):
        message = ''
        blist = []
        title = 'diagnostics'
        if 'symlinks' in request.GET:
            diagnostics.play_with_links()
        if 'verify-songs' in request.GET:
            title = 'missing songs'
            blist = diagnostics.verify_list(models.Song.objects.all())
        if 'verify-movies' in request.GET:
            title = 'missing movies'
            blist = diagnostics.verify_list(models.Movie.objects.all())
        if 'verify-pictures' in request.GET:
            title = 'missing pictures'
            blist = diagnostics.verify_list(models.Picture.objects.all())
            
        context = { 'message': message,
            'brokenList': blist,
            'title': title }
        return render(request,self.template_name, context)


