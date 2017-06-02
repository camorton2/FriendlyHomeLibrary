# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.timezone import now

from FHLBuilder import choices


# Create your models here.

CHAR_LENGTH=1000

class Tag(models.Model):
    name = models.CharField(max_length=CHAR_LENGTH,unique=True)
    slug = models.SlugField(max_length=CHAR_LENGTH, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        permissions=(("tag_builder", "tag builder"),
                     ("tag_reader", "tag reader"))
    def get_absolute_url(self):
        return reverse('builder_tag_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_tag_update',kwargs={'slug': self.slug})

# holds the path, represents an Album/audioBook (audio) or Series (video)
class Collection(models.Model):
    filePath = models.CharField(max_length=CHAR_LENGTH)
    drive = models.IntegerField()
    title = models.CharField(max_length=CHAR_LENGTH)
    slug = models.SlugField(max_length=CHAR_LENGTH,unique=True)

    def get_absolute_url(self):
        return reverse('builder_collection_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_collection_update',kwargs={'slug': self.slug})
    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        permissions=(("collection_builder", "collection builder"),
                     ("collection_reader", "collection reader"))

# the file itself
class CommonFile(models.Model):
    fileKind = models.CharField(
       max_length=10,
       choices = choices.KIND_CHOICES,
       default = choices.UNKNOWN)
    fileName = models.CharField(max_length=CHAR_LENGTH)
    year = models.IntegerField(default=0000)
    title = models.CharField(max_length=CHAR_LENGTH)
    slug = models.SlugField(max_length=CHAR_LENGTH,unique=True)
    date_added = models.DateField(default = now)
    
    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ['title']
        permissions=(("common_builder", "common builder"),
                     ("common_reader", "common reader"))


class TV_Manager(models.Manager):
    def get_queryset(self):
        q1 = Q(fileKind__exact=choices.TV)
        q2 = Q(fileKind__exact=choices.TV_CARTOON)
        q3 = Q(fileKind__exact=choices.TV_SITCOM)
        return super(TV_Manager,self).get_queryset().filter(q1|q2|q3)


# any video is called a movie
class Movie(CommonFile):
    collection = models.ForeignKey(Collection,
      models.SET_NULL,
      blank=True,
      null=True,related_name='movies')
    tags = models.ManyToManyField(Tag, blank=True, related_name='movie_tags')
    likes = models.ManyToManyField(User, blank=True, related_name='movie_likes')
    loves = models.ManyToManyField(User, blank=True, related_name='movie_loves')
    dislikes = models.ManyToManyField(User, blank=True, related_name='movie_dislikes')
    
    # default manager
    objects = models.Manager() 
    # just finds TV shows
    tv_objects = TV_Manager()
    
    def get_absolute_url(self):
        return reverse('builder_movie_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_movie_update',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("movie_builder", "movie builder"),
                     ("movie_reader", "movie reader"))


class Game(CommonFile):
    collection = models.ForeignKey(Collection,
      models.SET_NULL,
      blank=True,
      null=True,related_name='games')
    tags = models.ManyToManyField(Tag, blank=True, related_name='game_tags')
    likes = models.ManyToManyField(User, blank=True, related_name='game_likes')
    loves = models.ManyToManyField(User, blank=True, related_name='game_loves')
    dislikes = models.ManyToManyField(User, blank=True, related_name='game_dislikes')

    def get_absolute_url(self):
        return reverse('builder_game_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_game_update',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("game_builder", "game builder"),
                     ("game_reader", "game reader"))


# ebook
class Book(CommonFile):
    collection = models.ForeignKey(Collection,
      models.SET_NULL,
      blank=True,
      null=True,related_name='books')
    tags = models.ManyToManyField(Tag, blank=True, related_name='book_tags')
    likes = models.ManyToManyField(User, blank=True, related_name='book_likes')
    loves = models.ManyToManyField(User, blank=True, related_name='book_loves')
    dislikes = models.ManyToManyField(User, blank=True, related_name='book_dislikes')

    def get_absolute_url(self):
        return reverse('builder_book_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_book_update',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("book_builder", "book builder"),
                     ("book_reader", "book reader"))


class Slide_Manager(models.Manager):
    def get_queryset(self):
        q1 = Q(fileName__iendswith=choices.picts[7])
        q2 = Q(collection__filePath__icontains='smut')
        return super(Slide_Manager,self).get_queryset().exclude(q1 | q2)


class Picture(CommonFile):
    collection = models.ForeignKey(Collection,
      models.SET_NULL,
      blank=True,
      null=True,related_name='pictures')
    tags = models.ManyToManyField(Tag, blank=True, related_name='picture_tags')
    likes = models.ManyToManyField(User, blank=True, related_name='picture_likes')
    loves = models.ManyToManyField(User, blank=True, related_name='picture_loves')
    dislikes = models.ManyToManyField(User, blank=True, related_name='picture_dislikes')
    
    data1 = models.CharField(max_length=CHAR_LENGTH,blank=True)
    data2 = models.CharField(max_length=CHAR_LENGTH,blank=True)
    data3 = models.CharField(max_length=CHAR_LENGTH,blank=True)
    data4 = models.CharField(max_length=CHAR_LENGTH,blank=True)
    data5 = models.CharField(max_length=CHAR_LENGTH,blank=True)

    # default manager
    objects = models.Manager() 
    # excludes extensions not wanted in slide shows
    slide_objects = Slide_Manager()

    def friendly_name(self):
        """ strip first directory from path """
        fpath = self.collection.filePath
        if '/' in fpath:
            bg = fpath.index('/')+1
            return fpath[bg:]+ '/' + self.fileName
        return fpath+'/'+self.fileName
    
    def get_absolute_url(self):
        return reverse('builder_picture_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_picture_update',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("picture_builder", "picture builder"),
                     ("picture_reader", "picture reader"))


class Newest_Song_Manager(models.Manager):
    def get_queryset(self):
        return super(Newest_Song_Manager,self). \
            get_queryset(). \
            order_by('-date_added','collection','track')


class Oldest_Song_Manager(models.Manager):
    def get_queryset(self):
        return super(Oldest_Song_Manager,self). \
            get_queryset(). \
            order_by('date_added','collection','track')


class Random_Song_Manager(models.Manager):
    def get_queryset(self):
        return super(Random_Song_Manager,self).get_queryset().order_by('?')


class Song(CommonFile):
    collection = models.ForeignKey(Collection,
      models.SET_NULL,
      blank=True,
      null=True, related_name='songs')
    track = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True, related_name='song_tags')
    likes = models.ManyToManyField(User, blank=True, related_name='song_likes')
    loves = models.ManyToManyField(User, blank=True, related_name='song_loves')
    dislikes = models.ManyToManyField(User, blank=True, related_name='song_dislikes')

    # default manager
    objects = models.Manager() 
    # sets up order for recent
    newest_objects = Newest_Song_Manager()
    # sets up order for old
    oldest_objects = Oldest_Song_Manager()    
    # setups up order for random
    random_objects = Random_Song_Manager()

    def get_absolute_url(self):
        return reverse('builder_song_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_song_update',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("song_builder", "song builder"),
                     ("song_reader", "song reader"))


# Chapter of an audio-book, should not be viewed or modified
class Chapter(CommonFile):
    collection = models.ForeignKey(Collection,
      models.SET_NULL,
      blank=True,
      null=True,related_name='chapters')
    def get_absolute_url(self):
        return reverse('builder_chapter_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_chapter_update',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("chapter_builder", "chapter builder"),
                     ("chapter_reader", "chapter reader"))

class Artist(models.Model):
    fullName = models.CharField(max_length=CHAR_LENGTH)
    slug = models.SlugField(max_length=CHAR_LENGTH, unique=True)
    def get_absolute_url(self):
        return reverse('builder_artist_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_artist_update',kwargs={'slug': self.slug})
        
    def __unicode__(self):
        return self.fullName
        
        
    class Meta:
        ordering = ['fullName']
        permissions=(("artist_builder", "artist builder"),
                     ("artist_reader", "artist reader"))


class Actor(Artist):
    movies = models.ManyToManyField(Movie, blank=True, related_name='movie_actors')
    def get_absolute_url(self):
        return reverse('builder_actor_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_actor_update',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("actor_builder", "actor builder"),
                     ("actor_reader", "actor reader"))


class Director(Artist):
    movies = models.ManyToManyField(Movie, blank=True, related_name='movie_directors')
    def get_absolute_url(self):
        return reverse('builder_director_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_director_update',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("director_builder", "director builder"),
                     ("director_reader", "director reader"))


class Musician(Artist):
    albums = models.ManyToManyField(Collection, blank=True, related_name='album_musicians')
    concerts = models.ManyToManyField(Movie, blank=True, related_name='concert_musicians')
    songs = models.ManyToManyField(Song, blank=True, related_name='song_musicians')
    def get_absolute_url(self):
        return reverse('builder_musician_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_musician_update',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("musician_builder", "musician builder"),
                     ("musician_reader", "musician reader"))


