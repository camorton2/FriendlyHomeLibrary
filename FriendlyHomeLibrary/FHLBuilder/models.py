# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class Tag(models.Model):
    name = models.CharField(
       max_length=31,
       unique=True)

    slug = models.SlugField(
       max_length=31,
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
    name = models.CharField(
       max_length=31,
       unique=True)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Setup(models.Model):
    songsHead = models.CharField(max_length=100)
    moviesHead = models.CharField(max_length=100)
    booksHead = models.CharField(max_length=100)

class Common(models.Model):
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
    filename = models.CharField(max_length=100)

    tag = models.ManyToManyField(Tag)
    title = models.CharField(
       max_length=31,
       unique=True)
    slug = models.SlugField(
       max_length=31,
       unique=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']
    year = models.IntegerField(default=0000)

# Directory which is also an album or an audio book
class Collection(models.Model):
    filepath = models.CharField(max_length=100)
    members = models.ForeignKey(Common,
      models.SET_NULL,
      blank=True,
      null=True)
    slug = models.SlugField(
       max_length=31,
       unique=True)
    def get_absolute_url(self):
        return reverse('builder_collection_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_collection_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_collection_delete',kwargs={'slug': self.slug})

class Movie(Common):
    def get_absolute_url(self):
        return reverse('builder_movie_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_movie_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_movie_delete',kwargs={'slug': self.slug})

class Concert(Movie):
    def get_absolute_url(self):
        return reverse('builder_concert_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_concert_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_concert_delete',kwargs={'slug': self.slug})


class Song(Common):
    track = models.IntegerField()
    def get_absolute_url(self):
        return reverse('builder_song_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_song_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_song_delete',kwargs={'slug': self.slug})

class Album(Collection):
    songs = models.ForeignKey(Song,
      models.SET_NULL,
      blank=True,
      null=True)
    def get_absolute_url(self):
        return reverse('builder_album_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_album_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_album_delete',kwargs={'slug': self.slug})


class Series(Collection):
    episodes = models.ForeignKey(Movie,
      models.SET_NULL,
      blank=True,
      null=True)
    def get_absolute_url(self):
        return reverse('builder_series_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_series_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_series_delete',kwargs={'slug': self.slug})


class Person(models.Model):
    firstName = models.CharField(max_length=63)
    lastName = models.CharField(max_length=63)
    def get_absolute_url(self):
        return reverse('builder_person_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_person_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_person_delete',kwargs={'slug': self.slug})

class Actor(Person):
    movies = models.ManyToManyField(Movie)
    def get_absolute_url(self):
        return reverse('builder_actor_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_actor_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_actor_delete',kwargs={'slug': self.slug})

class Director(Person):
    movies = models.ManyToManyField(Movie)
    def get_absolute_url(self):
        return reverse('builder_director_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_director_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_director_delete',kwargs={'slug': self.slug})

class Musician(Person):
    albums = models.ManyToManyField(Album)
    concerts = models.ManyToManyField(Concert)
    def get_absolute_url(self):
        return reverse('builder_musician_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_musician_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_misucian_delete',kwargs={'slug': self.slug})

class Band(models.Model):
    bandName = models.CharField(max_length=63)
    albums = models.ManyToManyField(Album)
    concerts = models.ManyToManyField(Concert)

############# not implemented ############
class Likes(models.Model):
    liked = models.ManyToManyField(Common)
    likedBy = models.ManyToManyField(FHLUser)

class Loves(models.Model):
    loved = models.ManyToManyField(Common)
    lovedBy = models.ManyToManyField(FHLUser)

class DisLikes(models.Model):
    disLiked = models.ManyToManyField(Common)
    disLikedBy = models.ManyToManyField(FHLUser)
