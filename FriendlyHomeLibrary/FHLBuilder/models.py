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
    filename = models.FileField()
    filepath = models.FilePathField()
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

class Likes(models.Model):
    liked = models.ManyToManyField(Common)
    likedBy = models.ManyToManyField(FHLUser)

class Loves(models.Model):
    loved = models.ManyToManyField(Common)
    lovedBy = models.ManyToManyField(FHLUser)

class DisLikes(models.Model):
    disLiked = models.ManyToManyField(Common)
    disLikedBy = models.ManyToManyField(FHLUser)



# Audio book chapter
class Chapter(Common):
    author = models.CharField(max_length=63)
    chapterNumber = models.IntegerField()

class Actor(models.Model):
    firstName = models.CharField(max_length=63)
    lastName = models.CharField(max_length=63)

class Director(models.Model):
    firstName = models.CharField(max_length=63)
    lastName = models.CharField(max_length=63)

class Musician(models.Model):
    firstName = models.CharField(max_length=63)
    lastName = models.CharField(max_length=63)

class Band(models.Model):
    bandName = models.CharField(max_length=63)

class AudioBook(Common):
    chapters = models.ForeignKey(Chapter,
      models.SET_NULL,
      blank=True,
      null=True)

class Song(Common):
    musician = models.ForeignKey(Musician,
      models.SET_NULL,
      blank=True,
      null=True)
    band = models.ForeignKey(Band,
      models.SET_NULL,
      blank=True,
      null=True)
    track = models.IntegerField()
    def get_absolute_url(self):
        return reverse('builder_song_detail',kwargs={'slug': self.slug})
    def get_update_url(self):
        return reverse('builder_song_update',kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('builder_song_delete',kwargs={'slug': self.slug})


class Album(Common):
    songs = models.ForeignKey(Song,
      models.SET_NULL,
      blank=True,
      null=True)

class Movie(Common):
    director = models.ForeignKey(Director,
      models.SET_NULL,
      blank=True,
      null=True)

    actor = models.ForeignKey(Actor,
      models.SET_NULL,
      blank=True,
      null=True)

