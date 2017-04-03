# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


# Create your models here.

CHAR_LENGTH=100

class Tag(models.Model):
    name = models.CharField(
       max_length=CHAR_LENGTH,
       unique=True)
    slug = models.SlugField(
       max_length=CHAR_LENGTH,
       unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        permissions=(("tag_builder", "tag builder"),
                     ("tag_reader", "tag reader"))
    def get_absolute_url(self):
        return reverse('builder_tag_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_tag_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_tag_delete',kwargs={'slug': self.slug})

## not used right now
##class Setup(models.Model):
##    songsHead = models.CharField(max_length=CHAR_LENGTH)
##    moviesHead = models.CharField(max_length=CHAR_LENGTH)
##    booksHead = models.CharField(max_length=CHAR_LENGTH)

# holds the path, represents an Album/audioBook (audio) or Series (video)
class Collection(models.Model):
    filePath = models.CharField(max_length=CHAR_LENGTH)
    title = models.CharField(
       max_length=CHAR_LENGTH,
       unique=True)
    slug = models.SlugField(
       max_length=CHAR_LENGTH,
       unique=True)

    def get_absolute_url(self):
        return reverse('builder_collection_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_collection_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_collection_delete',kwargs={'slug': self.slug})
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        permissions=(("collection_builder", "collection builder"),
                     ("collection_reader", "collection reader"))

# the file itself
class CommonFile(models.Model):
    MOVIE = 'MV'
    MINI_MOVIE = 'MM'
    CONCERT = 'CC'
    DOCUMENTARY = 'DD'
    GAME = "GG"
    TV = "TV"
    MINISERIES = "MS"
    AUDIO_BOOK = "AB"
    EBOOK = "EB"
    SONG = "SG"
    PICTURE = "PT"
    UNKNOWN = "UN"
    KIND_CHOICES = (
        (MOVIE, 'Movie'),
        (MINI_MOVIE, 'Mini-movie'),
        (CONCERT, 'Concert'),
        (DOCUMENTARY,'Documentary'),
        (GAME, 'Game'),
        (TV, 'TV-show'),
        (MINISERIES, 'Mini-series'),
        (AUDIO_BOOK, 'audio-book'),
        (EBOOK, 'e-book'),
        (SONG, 'song'),
        (PICTURE, 'picture'),
        (UNKNOWN, 'unknown')
    )
    fileKind = models.CharField(
       max_length=2,
       choices = KIND_CHOICES,
       default = UNKNOWN)
    fileName = models.CharField(max_length=CHAR_LENGTH)
    year = models.IntegerField(default=0000)
    title = models.CharField(max_length=CHAR_LENGTH)
    slug = models.SlugField(max_length=CHAR_LENGTH,unique=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']
        permissions=(("common_builder", "common builder"),
                     ("common_reader", "common reader"))



# any video is called a movie
class Movie(CommonFile):
    collection = models.ForeignKey(Collection,
      models.SET_NULL,
      blank=True,
      null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='movie_tags')
    likes = models.ManyToManyField(User, blank=True, related_name='movie_likes')
    loves = models.ManyToManyField(User, blank=True, related_name='movie_loves')
    dislikes = models.ManyToManyField(User, blank=True, related_name='movie_dislikes')
    def get_absolute_url(self):
        return reverse('builder_movie_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_movie_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_movie_delete',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("movie_builder", "movie builder"),
                     ("movie_reader", "movie reader"))


class Game(CommonFile):
    collection = models.ForeignKey(Collection,
      models.SET_NULL,
      blank=True,
      null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='game_tags')
    likes = models.ManyToManyField(User, blank=True, related_name='game_likes')
    loves = models.ManyToManyField(User, blank=True, related_name='game_loves')
    dislikes = models.ManyToManyField(User, blank=True, related_name='game_dislikes')

    def get_absolute_url(self):
        return reverse('builder_game_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_game_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_game_delete',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("game_builder", "game builder"),
                     ("game_reader", "game reader"))



# ebook
class Book(CommonFile):
    collection = models.ForeignKey(Collection,
      models.SET_NULL,
      blank=True,
      null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='book_tags')
    likes = models.ManyToManyField(User, blank=True, related_name='book_likes')
    loves = models.ManyToManyField(User, blank=True, related_name='book_loves')
    dislikes = models.ManyToManyField(User, blank=True, related_name='book_dislikes')

    def get_absolute_url(self):
        return reverse('builder_book_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_book_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_book_delete',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("book_builder", "book builder"),
                     ("book_reader", "book reader"))


class Picture(CommonFile):
    collection = models.ForeignKey(Collection,
      models.SET_NULL,
      blank=True,
      null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='picture_tags')
    likes = models.ManyToManyField(User, blank=True, related_name='picture_likes')
    loves = models.ManyToManyField(User, blank=True, related_name='picture_loves')
    dislikes = models.ManyToManyField(User, blank=True, related_name='picture_dislikes')

    def get_absolute_url(self):
        return reverse('builder_picture_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_picture_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_picture_delete',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("picture_builder", "picture builder"),
                     ("picture_reader", "picture reader"))


class Song(CommonFile):
    collection = models.ForeignKey(Collection,
      models.SET_NULL,
      blank=True,
      null=True)
    track = models.IntegerField()
    tags = models.ManyToManyField(Tag, blank=True, related_name='song_tags')
    likes = models.ManyToManyField(User, blank=True, related_name='song_likes')
    loves = models.ManyToManyField(User, blank=True, related_name='song_loves')
    dislikes = models.ManyToManyField(User, blank=True, related_name='song_dislikes')

    def get_absolute_url(self):
        return reverse('builder_song_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_song_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_song_delete',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("song_builder", "song builder"),
                     ("song_reader", "song reader"))


# Chapter of an audio-book, should not be viewed or modified
class Chapter(CommonFile):
    collection = models.ForeignKey(Collection,
      models.SET_NULL,
      blank=True,
      null=True)
    def get_absolute_url(self):
        return reverse('builder_chapter_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_chapter_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_chapter_delete',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("chapter_builder", "chapter builder"),
                     ("chapter_reader", "chapter reader"))

class Artist(models.Model):
    fullName = models.CharField(max_length=CHAR_LENGTH)
    slug = models.SlugField(
       max_length=CHAR_LENGTH,
       unique=True)
    def get_absolute_url(self):
        return reverse('builder_artist_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_artist_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_artist_delete',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("artist_builder", "artist builder"),
                     ("artist_reader", "artist reader"))


class Actor(Artist):
    movies = models.ManyToManyField(Movie, blank=True, related_name='movie_actors')
    def get_absolute_url(self):
        return reverse('builder_actor_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_actor_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_actor_delete',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("actor_builder", "actor builder"),
                     ("actor_reader", "actor reader"))



class Director(Artist):
    movies = models.ManyToManyField(Movie, blank=True, related_name='movie_directors')
    def get_absolute_url(self):
        return reverse('builder_director_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_director_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_director_delete',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("director_builder", "director builder"),
                     ("director_reader", "director reader"))


class Musician(Artist):
    albums = models.ManyToManyField(Collection, blank=True)
    concerts = models.ManyToManyField(Movie, blank=True)
    songs = models.ManyToManyField(Song, blank=True)
    def get_absolute_url(self):
        return reverse('builder_musician_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_musician_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_musician_delete',kwargs={'slug': self.slug})
    class Meta:
        permissions=(("musician_builder", "musician builder"),
                     ("musician_reader", "musician reader"))


###################################################################
## Anonymous: query and play
## Reader: create: tag, actor, director, musician
##         modify: everything except filename, path, slug
## Builder: modify: filename, path, slug
##          create: common
## Superuser: delete
###################################################################
