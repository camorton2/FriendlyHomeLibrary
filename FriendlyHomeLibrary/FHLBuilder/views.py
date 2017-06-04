# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.text import slugify

from django.views.generic import View

from FriendlyHomeLibrary import settings

from FHLUser.decorators import require_authenticated_permission

from FHLBuilder import models, forms
from FHLBuilder import collection
from FHLBuilder import utility
from FHLBuilder import query
from FHLBuilder import diagnostics
import FHLBuilder.view_utility as vu

from FHLReader import kodi, chromecast
from FHLReader import utility as rutils


class HomePage(View):
    """ main homepage """
    template_name = 'FHLBuilder/base_fhlbuilder.html'
    def get(self, request):
        return render(request,self.template_name,)


class TagList(View):
    """ list tags """
    template_name = 'FHLBuilder/tag_list.html'
    def get(self, request):
        context = {'tags': models.Tag.objects.all()}
        return render(request,self.template_name,context)


class TagDetailView(View):
    """ view all objects with this tag """
    def get(self,request,slug):
        """
        Given the slug, find the corresponding tag and
        collect object lists to pass to the collection view
        """
        #print("TagDetailView GET")
        tag=get_object_or_404(models.Tag,slug__iexact=slug)

        vargs = {
            'songs': tag.song_tags.all(),
            'pictures':tag.picture_tags.all(),
            'movies': tag.movie_tags.all(),
            'title': tag.name
            }
        return vu.generic_collection_view(request,**vargs)


class SongDetailView(View):
    template_name = 'FHLBuilder/song_detail.html'
    form_class=forms.SongForm

    def get(self,request,slug):
        """
        display form with initial values
        """
        song=get_object_or_404(models.Song,slug__iexact=slug)
        playit = utility.object_path(song)

        myform = self.form_class(instance=song,
            initial = query.my_preference_dict(song,request.user))

        context = {
            'song':song,
            'playit':playit,
            'objectForm':myform}
        return render(request, self.template_name, context)


    def post(self,request,slug):
        """
        Post handles updates from the SongForm
        as well as requests from kodi playback
        """
        song=get_object_or_404(models.Song,slug__iexact=slug)
        playit = utility.object_path(song)

        bound_form = self.form_class(request.POST,instance=song)
        if 'UpdateObject' in request.POST:
            if bound_form.is_valid():
                new_song = bound_form.save()
                song.title=new_song.title
                song.year=new_song.year

                # tag
                tq = bound_form.cleaned_data['tag']
                if len(tq):
                    tqSlug = slugify(unicode(tq))
                    new_tag = collection.add_tag(tq,tqSlug)
                    song.tags.add(new_tag)
                # new musician
                mus = bound_form.cleaned_data['musician']
                if len(mus):
                    mSlug = slugify(unicode(mus+'-mus'))
                    new_mus = collection.add_musician(mus,mSlug)
                    new_mus.songs.add(song)

                pref = bound_form.cleaned_data['pref']
                # user selected a preference
                if len(pref):
                    query.handle_pref(song,pref,request.user)

                song.save()
                bound_form = self.form_class(
                    instance=song,
                    initial = query.my_preference_dict(song,request.user)
                    )
                formContext = {
                    'song':song,'playit':playit,
                    'objectForm':bound_form}
                return render(request,self.template_name, formContext)
        _ = kodi.playback_requests(song,request)

        songContext = {
            'song':song,
            'playit':playit,
            'objectForm': bound_form}
        return render(request,self.template_name, songContext)


class CollectionList(View):
    """ collection list view from main menu """
    def get(self,request):
        """
        get simply sets up the list and passes it
        to the common collection list view
        """
        kind = vu.select_kind(request)
        clist = query.handle_collection_kind(kind)
        title = 'Library Collections'
        return vu.view_list(request,clist,title,kind)

class AllFilesView(View):
    """ form for all files view """
    template_name = 'FHLBuilder/all_files.html'
    form_class=forms.AllFilesForm

    def get(self, request):
        """ all files form get, setup form """
        context = {'form':self.form_class(),'title': 'List files'}
        return render(request,self.template_name,context)


    def post(self, request):
        """ all files request, process form """
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            kind = bound_form.cleaned_data['kind']
            order = bound_form.cleaned_data['order']
            return redirect(reverse('builder_file_list', args=(kind,order)))

        context = {'form':self.form_class(),'title': 'List files'}
        return render(request,self.template_name,context)


class FileList(View):
    """
    Handle the view of all files
    """
    def get(self,request,kind,myorder):
        """
        passes kind and ordering to the common collection view
        """
        vargs = {'kind': kind, 'myorder':myorder}
        return vu.generic_collection_view(request, **vargs)


class CollectionMixins:
    """
    utilities common to working with the creation of collections
    """
    def __init__(self):
        pass

    def handle_collection(self,path,drive):
        """
        handle the creation or selection of the appropriate collection
        """
        if path[0] == '/':
            path = path[1:]
        spath = path.replace('/','-')
        upath = unicode('%s' % (spath))
        slug = slugify(upath)
        title = upath
        #print('add collection slug %s spath %s upath %s path %s' % (slug,spath,upath,path))
        nc = collection.add_collection(title,slug,path,drive,False)
        return nc


    def add_members(self,path,drive,kind,tag, knownCollection = None):
        """
        walk the specified directory to populate the database
        handles (or should handle) all file type errors
        this is the main connection to the file system
        """
        #print("ADD_MEMBERS path %s" % (path))

        sDrive = utility.get_drive(drive)
        album = None
        artist = None
        setPath = os.path.join(settings.MY_MEDIA_FILES_ROOT,sDrive)
        scanPath = os.path.join(setPath,path)
        goodPath = os.path.exists(scanPath)

        if not goodPath:
            message = ('ERROR path does not exist check drive setup %s' % scanPath)
            utility.log(message)
            raise rutils.MyException(message)
        for root, _, files in os.walk(scanPath):
            try:
                myroot = unicode(root[len(setPath):])
                if knownCollection is None:
                    album = self.handle_collection(myroot,drive)
                else:
                    album = knownCollection
                for obj in files:
                    try:
                        artist = collection.add_file(
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


class CollectionDetailView(View):
    """
    view for a specific collection
    """
    def get(self,request,slug):
        """
        collect the information to pass to the common collection view
        """
        target=get_object_or_404(models.Collection,slug__iexact=slug)

        artists = target.album_musicians.all()
        if artists.count():
            songs = target.songs.all().order_by('track')
        else:
            songs = target.songs.all()

        vargs = {
            'songs': songs,
            'pictures': target.pictures.all(),
            'movies': target.movies.all(),
            'artists': artists,
            'title': target.title,
            'update': target
            }

        return vu.generic_collection_view(request, **vargs)


@require_authenticated_permission('FHLBuilder.collection_builder')
class CollectionFormView(View,CollectionMixins):
    """
    populating the database
    """
    form_class=forms.CollectionForm
    template_name = 'FHLBuilder/collection_form.html'

    def get(self, request):
        """
        """
        return render(request,self.template_name,{'form':self.form_class()})

    def post(self,request):
        """
        once the form is valid start walking files
        and populating the database
        """
        #print('CollectionFormView POST')
        bound_form=self.form_class(request.POST)
        if bound_form.is_valid():
            #print('valid create kind %s' % bound_form.cleaned_data['kind'])
            album,artist = self.add_members(
                bound_form.cleaned_data['filePath'],
                bound_form.drive,
                bound_form.cleaned_data['kind'],
                bound_form.cleaned_data['tag'])
            if artist is not None:
                # new collection matches an artist, redirect to artist
                return redirect(artist)
            elif album.songs.count() or album.movies.count() or album.pictures.count():
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

        # display all collections as a reasonable default if form
        # did not redirect with other options
        return redirect(reverse('builder_collection_list'))


@require_authenticated_permission('FHLBuilder.collection_builder')
class CollectionUpdate(View,CollectionMixins):
    """
    handle update, populating database for existing collection
    """
    form_class=forms.BasicCollectionForm
    model=models.Collection
    template_name='FHLBuilder/collection_update.html'

    def get_object(self,slug):
        """
        find collection matching slub
        """
        return get_object_or_404(self.model,slug=slug)

    def get(self,request,slug):
        """ setup form """
        #print("CollectionUpdate GET")
        target = self.get_object(slug)

        context={'form': self.form_class(instance=target)}
        return render(request,self.template_name,context)

    def post(self,request,slug):
        """ handle valid form and redirect """
        #print("CollectionUpdate POST")
        target = self.get_object(slug)
        bound_form = self.form_class(request.POST,instance=target)
        if bound_form.is_valid():
            try:
                #print('valid update tag %s' % bound_form.cleaned_data['tag'])
                album,artist = self.add_members(
                    target.filePath,
                    target.drive,
                    bound_form.cleaned_data['kind'],
                    bound_form.cleaned_data['tag'],
                    target
                    )
            except rutils.MyException,ex:
                message = ex.message
                context = {'form':bound_form,'message':message}
                return render(request,self.template_name,context)
            if artist is not None:
                # display the page for the artist
                return redirect(artist)
            elif album.songs.count() or album.movies.count() or album.pictures.count():
                # album is not empty, save and redirect
                album.save()
                return redirect(album)
        else:
            # in the case of an invalid form, redirect to the
            # bound form which has the ValidationError
            context = {
                'form':bound_form
                }
            return render(request,self.template_name,context)
        # otherwise redirect to target collection
        return redirect(target)


class MovieDetailView(View):
    """ movie details """
    template_name = 'FHLBuilder/movie_detail.html'
    form_class=forms.MovieForm

    def get(self,request,slug):
        """
        get responds to tags (actor, director, tag, musician,preferences)
        """
        movie=get_object_or_404(models.Movie,slug__iexact=slug)

        # real path required for playback
        playit = utility.object_path(movie)

        myform = self.form_class(instance=movie,
            initial = query.my_preference_dict(movie,request.user))
        context = {'movie':movie,
            'playit':playit,
            'objectForm':myform}
        return render(request, self.template_name,context)


    def post(self,request,slug):
        """
        post handles object update from the MovieForm
        """
        movie=get_object_or_404(models.Movie,slug__iexact=slug)

        #print ("MovieDetail POST for slug %s movie %s " % (slug,movie.title))
        playit = utility.object_path(movie)

        bound_form = self.form_class(request.POST,
            instance=movie,
            initial = query.my_preference_dict(movie,request.user))

        if 'UpdateObject' in request.POST:
            if bound_form.is_valid():
                new_movie = bound_form.save()
                movie.title=new_movie.title
                movie.year=new_movie.year

                cast = bound_form.cleaned_data['cast']
                if len(cast):
                    #print('cast %s' % cast)
                    try:
                        message = u'success'
                        #print('view calls cast_movie')
                        chromecast.cast_movie(cast,movie)
                    except rutils.MyException,ex:
                        message = ex.message
                        print('Caught %s' % ex.message)

                # tag
                tq = bound_form.cleaned_data['tag']
                if len(tq):
                    tqSlug = slugify(unicode(tq))
                    new_tag = collection.add_tag(tq,tqSlug)
                    movie.tags.add(new_tag)
                # new actor
                act = bound_form.cleaned_data['actor']
                if len(act):
                    actSlug = slugify(unicode(act+'-act'))
                    new_actor = collection.add_actor(act,actSlug)
                    new_actor.movies.add(movie)
                # new director
                dtr = bound_form.cleaned_data['director']
                if len(dtr):
                    dtrSlug = slugify(unicode(dtr+'-dtr'))
                    new_dtr = collection.add_director(dtr,dtrSlug)
                    new_dtr.movies.add(movie)
                # new musician - for concerts
                mus = bound_form.cleaned_data['musician']
                if len(mus):
                    mSlug = slugify(unicode(mus+'-mus'))
                    new_mus = collection.add_musician(mus,mSlug)
                    new_mus.concerts.add(movie)

                pref = bound_form.cleaned_data['pref']
                # user selected a preference
                if len(pref):
                    query.handle_pref(movie,pref,request.user)

                movie.save()
                bound_form = self.form_class(
                    instance=movie,
                    initial = query.my_preference_dict(movie,request.user)
                    )
                formContext = {
                    'movie':movie,
                    'playit':playit,
                    'objectForm':bound_form}
                return render(request,self.template_name, formContext)
        message = ''
        try:
            message = u'success'
            vlcPlugin = kodi.playback_requests(movie,request)
        except rutils.MyException,ex:
            message = ex.message
            print('Caught %s' % ex.message)
            vlcPlugin=False

        movieContext = {
            'movie':movie,
            'playit':playit,
            'objectForm': self.form_class(instance=movie),
            'vlcPlugin':vlcPlugin,
            'message':message}
        #print('render with message %s' % message)
        return render(request,self.template_name, movieContext)


class ArtistList(View):
    template_name = 'FHLBuilder/artist_list.html'
    def get(self, request, person):
        """
        Display list of artists as specified
        """
        title = ('Artists %s' % person)
        if person == 'actor':
            targetlist = models.Actor.objects.all()
        elif person == 'musician':
            targetlist = models.Musician.objects.all()
        elif person == 'director':
            targetlist = models.Director.objects.all()
        else:
            targetlist = []

        context = {'title': title,'targetlist': targetlist}
        return render(request,self.template_name,context)


class ActorDetailView(View):
    """  details for actor  """
    def get(self,request,slug):
        """ display movie list using common collection view """
        actor=get_object_or_404(models.Actor,slug__iexact=slug)

        vargs={
            'movies': actor.movies.all(),
            'title': ('Movies with actor %s' % actor.fullName)
            }
        return vu.generic_collection_view(request,**vargs)


class DirectorDetailView(View):
    """ details for director """
    def get(self,request,slug):
        """ display movie list using common collection view """
        director=get_object_or_404(models.Director,slug__iexact=slug)

        vargs={
            'movies': director.movies.all(),
            'title': ('Movies directed by %s' % director.fullName)
            }
        return vu.generic_collection_view(request,**vargs)


class MusicianDetailView(View):
    """
    Musician detail does not use the common display utility
    because the musician view displays albums and songs
    """
    template_name = 'FHLBuilder/musician_detail.html'

    def get(self,request,slug):
        """
        details of a musician as well as playlist for songs
        """
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
        except rutils.MyException,ex:
            message = ex.message
            print('Caught %s' % ex.message)

        context = {
            'musician':musician,
            'songlist':slist,
            'asPlayList':asPlayList,
            'message':message}
        return render(request,self.template_name,context)


class PictureShowView(View):
    """ slide show attempt details of a picture """
    template_name = 'FHLBuilder/picture_show.html'
    def get(self,request,
        slug='picturesbackup-scans-mortonfamily-provincialparksarchie1-pict',
        index='1',
        pictureCount='1'):
        picture=get_object_or_404(models.Picture,slug__iexact=slug)
        filename = utility.object_path(picture)
        context = {
            'index':index,'pictureCount':pictureCount,
            'filename':filename}
        return render(request, self.template_name,context)


class PictureDetailView(View):
    """ manage details of a picture """
    template_name = 'FHLBuilder/picture_detail.html'
    form_class=forms.PictureForm

    def get(self,request,slug):
        """ setup picture form   """

        picture=get_object_or_404(models.Picture,slug__iexact=slug)
        playit = utility.object_path(picture)

        myform = self.form_class(
            instance=picture,
            initial = query.my_preference_dict(picture,request.user)
            )

        context = {
            'picture':picture,'playit':playit,
            'objectForm':myform}
        return render(request, self.template_name, context)

    def post(self,request,slug):
        """ post request handles update from PictureForm """

        picture=get_object_or_404(models.Picture,slug__iexact=slug)
        playit = utility.object_path(picture)

        bound_form = self.form_class(request.POST,instance=picture,
            initial = query.my_preference_dict(picture,request.user))

        if 'UpdateObject' in request.POST:
            if bound_form.is_valid():
                new_picture = bound_form.save()
                picture.title=new_picture.title
                picture.year=new_picture.year

                cast = bound_form.cleaned_data['cast']
                if len(cast):
                    #print('cast %s' % cast)
                    try:
                        message = u'success'
                        #print('view calls cast_picture')
                        chromecast.cast_picture(cast,picture)
                    except rutils.MyException,ex:
                        message = ex.message
                        #print('Caught %s' % ex.message)

                # tag
                tq = bound_form.cleaned_data['tag']
                if len(tq):
                    tqSlug = slugify(unicode(tq))
                    new_tag = collection.add_tag(tq,tqSlug)
                    picture.tags.add(new_tag)

                pref = bound_form.cleaned_data['pref']
                # user selected a preference
                if len(pref):
                    query.handle_pref(picture,pref,request.user)

                picture.save()
                bound_form = self.form_class(
                    instance=picture,
                    initial = query.my_preference_dict(picture,request.user)
                    )

                formContext = {
                    'picture':picture,
                    'playit':playit,
                    'objectForm':bound_form,
                    'message':message}
                return render(request,self.template_name, formContext)

        pictureContext = {
            'picture':picture,'playit':playit,
            'objectForm': bound_form }
        return render(request,self.template_name, pictureContext)


@require_authenticated_permission('FHLBuilder.collection_builder')
class DiagnosticsView(View):
    """ diagnostics are for database verification/update """
    template_name = 'FHLBuilder/diagnostics.html'
    def get(self,request):
        message = ''
        blist = []
        title = 'diagnostics'
        if 'symlinks' in request.GET:
            diagnostics.play_with_links()
        elif 'verify-songs' in request.GET:
            title = 'missing songs'
            blist = diagnostics.verify_list(models.Song.objects.all())
        elif 'verify-movies' in request.GET:
            title = 'missing movies'
            blist = diagnostics.verify_list(models.Movie.objects.all())
        elif 'verify-pictures' in request.GET:
            title = 'missing pictures'
            blist = diagnostics.verify_list(models.Picture.objects.all())
        else:
            a = CollectionMixins()
            utility.rescan(request.GET,a)
        context = { 'message': message,
            'brokenList': blist,
            'title': title }
        return render(request,self.template_name, context)


@require_authenticated_permission('FHLBuilder.collection_builder')
class MusicianCleanupView(View):
    """
    Allow user to select musician(s) to remove from the database
    """
    template_name = 'FHLBuilder/remove.html'
    form_class=forms.MusicianCleanupForm

    def get(self, request):
        context = {'form':self.form_class(),
            'title': 'Remove a Musician'}
        return render(request,self.template_name,context)


    def post(self, request):

        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            artists = bound_form.cleaned_data['choices']
            for a in artists:
                #print('wants to remove %s' % (a.fullName))
                collection.remove_musician(a)                    

        context = {'form':bound_form,'title': 'Remove a Musician'}
        return render(request,self.template_name,context)


@require_authenticated_permission('FHLBuilder.collection_builder')
class CollectionCleanupView(View):
    """
    Allow user to select musician(s) to remove from the database
    """
    template_name = 'FHLBuilder/remove.html'
    form_class=forms.CollectionCleanupForm

    def get(self, request):
        context = {'form':self.form_class(),
            'title': 'Remove a Collection'}
        return render(request,self.template_name,context)


    def post(self, request):

        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            colls = bound_form.cleaned_data['choices']
            for collect in colls:
                #print('wants to remove %s' % (collect.title))
                collection.remove_collection(collect)                    

        context = {'form':bound_form,'title': 'Remove a Collection'}
        return render(request,self.template_name,context)


@require_authenticated_permission('FHLBuilder.collection_builder')
class DirectorCleanupView(View):
    """
    Allow user to select director(s) to remove from the database
    """
    template_name = 'FHLBuilder/remove.html'
    form_class=forms.DirectorCleanupForm

    def get(self, request):
        context = {'form':self.form_class(),
            'title': 'Remove a Director'}
        return render(request,self.template_name,context)


    def post(self, request):

        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            dtors = bound_form.cleaned_data['choices']
            for dtor in dtors:
                print('wants to remove %s' % (dtor.fullName))
                collection.remove_director(dtor)                    

        context = {'form':bound_form,'title': 'Remove a Director'}
        return render(request,self.template_name,context)


@require_authenticated_permission('FHLBuilder.collection_builder')
class ActorCleanupView(View):
    """
    Allow user to select director(s) to remove from the database
    """
    template_name = 'FHLBuilder/remove.html'
    form_class=forms.ActorCleanupForm

    def get(self, request):
        context = {'form':self.form_class(),
            'title': 'Remove an Actor'}
        return render(request,self.template_name,context)


    def post(self, request):

        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            acts = bound_form.cleaned_data['choices']
            for act in acts:
                print('wants to remove %s' % (act.fullName))
                collection.remove_actor(act)                    

        context = {'form':bound_form,'title': 'Remove an Actor'}
        return render(request,self.template_name,context)


@require_authenticated_permission('FHLBuilder.collection_builder')
class TagCleanupView(View):
    """
    Allow user to select tag(s) to remove from the database
    """
    template_name = 'FHLBuilder/remove.html'
    form_class=forms.TagCleanupForm

    def get(self, request):
        context = {'form':self.form_class(),
            'title': 'Remove a tag'}
        return render(request,self.template_name,context)


    def post(self, request):

        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            tags = bound_form.cleaned_data['choices']
            for tag in tags:
                print('wants to remove %s' % (tag.name))
                collection.remove_tag(tag)                    

        context = {'form':bound_form,'title': 'Remove a tag'}
        return render(request,self.template_name,context)


@require_authenticated_permission('FHLBuilder.collection_builder')
class PictureCleanupView(View):
    """
    Allow user to select picture(s) to remove from the database
    """
    template_name = 'FHLBuilder/remove.html'
    form_class=forms.PictureCleanupForm

    def get(self, request):
        context = {'form':self.form_class(),
            'title': 'Remove a picture'}
        return render(request,self.template_name,context)


    def post(self, request):

        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            picts = bound_form.cleaned_data['choices']
            for pict in picts:
                print('wants to remove %s' % (pict.title))
                collection.remove_picture(pict)                    

        context = {'form':bound_form,'title': 'Remove a picture'}
        return render(request,self.template_name,context)


@require_authenticated_permission('FHLBuilder.collection_builder')
class SongCleanupView(View):
    """
    Allow user to select picture(s) to remove from the database
    """
    template_name = 'FHLBuilder/remove.html'
    form_class=forms.SongCleanupForm

    def get(self, request):
        context = {'form':self.form_class(),
            'title': 'Remove a song'}
        return render(request,self.template_name,context)


    def post(self, request):

        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            songs = bound_form.cleaned_data['choices']
            for song in songs:
                print('wants to remove %s' % (song.title))
                collection.remove_song(song)                    

        context = {'form':bound_form,'title': 'Remove a song'}
        return render(request,self.template_name,context)


@require_authenticated_permission('FHLBuilder.collection_builder')
class MovieCleanupView(View):
    """
    Allow user to select movie(s) to remove from the database
    """
    template_name = 'FHLBuilder/remove.html'
    form_class=forms.MovieCleanupForm

    def get(self, request):
        context = {'form':self.form_class(),
            'title': 'Remove a movie'}
        return render(request,self.template_name,context)


    def post(self, request):

        rlist = []
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            movies = bound_form.cleaned_data['choices']
            for movie in movies:
                print('wants to remove %s' % (movie.title))
                collection.remove_movie(movie)                    

        context = {'form':bound_form,'title': 'Remove a movie'}
        return render(request,self.template_name,context)

