# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

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


class Movie(Common):
    director = models.CharField(max_length=63)
    actors = models.ManyToManyField(Tag)

# Audio book chapter
class Chapter(Common):
    author = models.CharField(max_length=63)
    chapterNumber = models.IntegerField()

class AudioBook(Common):
    chapters = models.ForeignKey(Chapter, 
      models.SET_NULL,
      blank=True,
      null=True)

class Song(Common):
    artist = models.CharField(max_length=63)
    track = models.IntegerField()

class Album(Common):
    songs = models.ForeignKey(Song,
      models.SET_NULL,
      blank=True,
      null=True)       
    

