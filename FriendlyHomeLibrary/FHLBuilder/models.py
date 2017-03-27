# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

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
    def get_absolute_url(self):
        return reverse('builder_tag_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_tag_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_tag_delete',kwargs={'slug': self.slug})

class FHLUser(models.Model):
    BUILDER = 'B'
    READER = 'R'
    MODE_CHOICES = (
       (BUILDER, 'Builder'),
       (READER, 'Reader')
    )

    userMode = models.CharField(
       max_length=1,
       choices = MODE_CHOICES,
       default = READER)
    # no slug, name must be unique
    name = models.CharField(
       max_length=CHAR_LENGTH,
       unique=True)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

# not used right now
class Setup(models.Model):
    songsHead = models.CharField(max_length=CHAR_LENGTH)
    moviesHead = models.CharField(max_length=CHAR_LENGTH)
    booksHead = models.CharField(max_length=CHAR_LENGTH)

# holds the path, represents an Album (audio) or Series (video)
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


# the file itself
class CommonFile(models.Model):
    AUDIO = 'A'
    VIDEO = 'V'
    KIND_CHOICES = (
       (AUDIO, 'Audio'),
       (VIDEO, 'Video')
    )
    fileKind = models.CharField(
       max_length=1,
       choices = KIND_CHOICES,
       default = AUDIO)
    fileName = models.CharField(max_length=CHAR_LENGTH)
    year = models.IntegerField(default=0000)
    title = models.CharField(
       max_length=CHAR_LENGTH,
       unique=True)
    slug = models.SlugField(
       max_length=CHAR_LENGTH,
       unique=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

# any video is called a movie
class Movie(CommonFile):
    collection = models.ForeignKey(Collection,
      models.SET_NULL,
      blank=True,
      null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    def get_absolute_url(self):
        return reverse('builder_movie_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_movie_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_movie_delete',kwargs={'slug': self.slug})

class Song(CommonFile):
    collection = models.ForeignKey(Collection,
      models.SET_NULL,
      blank=True,
      null=True)
    track = models.IntegerField()
    tags = models.ManyToManyField(Tag, blank=True)
    def get_absolute_url(self):
        return reverse('builder_song_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_song_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_song_delete',kwargs={'slug': self.slug})

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

class Actor(Artist):
    movies = models.ManyToManyField(Movie, blank=True)
    def get_absolute_url(self):
        return reverse('builder_actor_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_actor_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_actor_delete',kwargs={'slug': self.slug})

class Director(Artist):
    movies = models.ManyToManyField(Movie, blank=True)
    def get_absolute_url(self):
        return reverse('builder_director_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_director_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_director_delete',kwargs={'slug': self.slug})

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

############# not implemented ############
##class Likes(models.Model):
##    liked = models.ManyToManyField(CommonFile)
##    likedBy = models.ManyToManyField(FHLUser)
##
##class Loves(models.Model):
##    loved = models.ManyToManyField(CommonFile)
##    lovedBy = models.ManyToManyField(FHLUser)
##
##class DisLikes(models.Model):
##    disLiked = models.ManyToManyField(CommonFile)
##    disLikedBy = models.ManyToManyField(FHLUser)
####################################################
