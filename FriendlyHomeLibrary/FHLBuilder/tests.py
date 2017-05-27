# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

from FHLBuilder.models import Song, Collection, Movie, Picture
from FHLBuilder.views import CollectionMixins
from FHLBuilder import choices

class SongCollection(TestCase):
    
    def setUp(self):
        a = CollectionMixins()
        kind = choices.SONG
        tag = 'abc'
        path = 'mp3s/Duffy'
        album, artist = a.add_members(path,2,kind,tag)
        
    def test1(self):
        rf = Collection.objects.get(title__icontains='rockferry')
        self.assertEqual(rf.title, 'Rockferry')
        
    def test2(self):
        rf = Song.objects.get(title__icontains='mercy')
        self.assertEqual(rf.track,7)
    
    def test3(self):
        self.assertEqual(Song.objects.count(),10)
        
        

class MovieCollection(TestCase):
    
    def setUp(self):
        a = CollectionMixins()
        kind = choices.MOVIE
        tag = 'xxx'
        path = 'Videos/movies-x'
        album, artist = a.add_members(path,1,kind,tag)
                
    def test1(self):
        rf = Movie.objects.filter(title__icontains='x-men')
        self.assertEqual(rf.count(),8)
    
    def test2(self):
        self.assertEqual(Movie.objects.count(),11)
        

class PictureCollection(TestCase):
    
    def setUp(self):
        a = CollectionMixins()
        kind = choices.MOVIE
        tag = 'xxx'
        path = 'picturesbackup/win2001'
        album, artist = a.add_members(path,2,kind,tag)
                
    def test1(self):
        rf = Picture.objects.get(title__icontains='capture')
        self.assertEqual(rf.title,'Capture_00001')
    
    def test2(self):
        self.assertEqual(Picture.objects.count(),9)


