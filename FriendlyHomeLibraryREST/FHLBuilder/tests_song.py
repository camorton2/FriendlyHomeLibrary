# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from rest_framework import status

from django.test import TestCase, Client
from django.urls import reverse

from FHLBuilder import models as db
from FHLBuilder import serializers as ss
from FHLBuilder import collection, choices

# Create your tests here.

class SongTestAdd(TestCase):
    
    def setUp(self):
        a = collection.CollectionMixins()
        kind = choices.SONG
        tag = 'abc'
        path = 'mp3s/Duffy'
        album, artist = a.add_members(path,2,kind,tag)
    
    def test1(self):
        rf = db.Collection.objects.get(title__icontains='rockferry')
        self.assertEqual(rf.title, 'Rockferry')
        
    def test2(self):
        rf = db.Song.objects.get(title__icontains='mercy')
        self.assertEqual(rf.track,7)
    
    def test3(self):
        self.assertEqual(db.Song.objects.count(),10)

# initialize the APIClient app
client = Client()

class SongTestViews(TestCase):
    
    def setUp(self):
        a = collection.CollectionMixins()
        kind = choices.SONG
        tag = 'abc'
        path = 'mp3s/Duffy'
        album, artist = a.add_members(path,2,kind,tag)
    
    def test_get_all_songs(self):
        response = client.get(reverse('get_post_songs'))
        # get data from db
        songs = db.Song.objects.all()
        serializer = ss.SongSerializer(songs,many=True)
        self.assertEqual(response.data,serializer.data)        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_valid_single_song(self):
        rf = db.Song.objects.get(title__icontains='mercy')
        self.assertEqual(rf.track,7)
        response = client.get(reverse('get_delete_update_song',
            kwargs={'slug': rf.slug }))
        serializer=ss.SongSerializer(rf)
        self.assertEqual(response.data,serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_invalid_single_song(self):
        response = client.get(reverse('get_delete_update_song',
            kwargs={'slug': 'no_song_like_this' }))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        

class SongTestCreate(TestCase):
    
    def setUp(self):
        a = collection.CollectionMixins()
        kind = choices.SONG
        tag = 'abc'
        path = 'mp3s/Duffy'
        album, artist = a.add_members(path,2,kind,tag)
        #dbobj = bmodels.Song(title=title,slug=sSlug,fileName=fileName, collection=sCollection)
        rf = db.Song.objects.get(title__icontains='mercy')
        self.assertEqual(rf.track,7)

        self.valid_payload = {
           'title': 'valid title',
           'slug': 'valid_slug',
           'fileName': 'valid_fileName',
           #'collection': album
        }    
        self.invalid_payload = {
           'title': '',
           'slug': rf.slug, 
           'fileName': rf.fileName,
           #'collection': album
        }    
    
    def test_create_valid_song(self):
        response = client.post(
            reverse('get_post_songs'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_invalid_song(self):
        response = client.post(
            reverse('get_post_songs'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
