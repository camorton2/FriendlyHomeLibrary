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

# initialize the APIClient app
client = Client()


class MovieTestAdd(TestCase):
    """ no views, just check database creation """    
    def setUp(self):
        a = collection.CollectionMixins()
        kind = choices.MOVIE
        tag = 'xxx'
        path = 'Videos/movies-x'
        album, artist = a.add_members(path,1,kind,tag)
                
    def test1(self):
        rf = db.Movie.objects.filter(title__icontains='x-men')
        self.assertEqual(rf.count(),10)
    
    def test2(self):
        self.assertEqual(db.Movie.objects.count(),13)


class MovieTestGet(TestCase):
    """ view functions for get """
    def setUp(self):
        a = collection.CollectionMixins()
        kind = choices.MOVIE
        tag = 'xxx'
        path = 'Videos/movies-x'
        album, artist = a.add_members(path,1,kind,tag)
    
    def test_get_all_movies(self):
        response = client.get(reverse('builder_movie_list'))
        # get data from db
        movies = db.Movie.objects.all()
        serializer = ss.MovieSerializer(movies,many=True)
        self.assertEqual(response.data,serializer.data)        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_valid_single_Movie(self):
        rf = db.Movie.objects.get(title__icontains='apocalypse')
        response = client.get(reverse('builder_movie_detail',
            kwargs={'slug': rf.slug }))
        serializer=ss.MovieSerializer(rf)
        self.assertEqual(response.data,serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_invalid_single_movie(self):
        response = client.get(reverse('builder_movie_detail',
            kwargs={'slug': 'no_movie_like_this' }))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        

class MovieTestCreate(TestCase):
    
    def setUp(self):
        a = collection.CollectionMixins()
        kind = choices.MOVIE
        tag = 'xxx'
        path = 'Videos/movies-x'
        album, artist = a.add_members(path,1,kind,tag)
        rf = db.Movie.objects.get(title__icontains='apocalypse')

        self.valid_payload = {
            'year': rf.year,
            'title': rf.title,
            'slug': 'a_slug',
            'fileName': rf.fileName,
            #'collection': album # todo figure out nested
        }    
        self.invalid_payload = {
            'year': 'not a valid year',
            'title': rf.title,
            'slug': 'b_slug',
            'fileName': rf.fileName, 
            #'collection': album # todo figure out nested
        }    
        self.invalid_payload1 = {
            'year': rf.year,
            'title': 'title',
            'slug': rf.slug, # error not unique
            'fileName': rf.fileName, 
            #'collection': album # todo figure out nested
        }    

    
    def test_create_valid_movie(self):
        response = client.post(
            reverse('builder_movie_list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_invalid_movie(self):
        response = client.post(
            reverse('builder_movie_list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_movie1(self):
        response = client.post(
            reverse('builder_movie_list'),
            data=json.dumps(self.invalid_payload1),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

class MovieTestUpdate(TestCase):
    
    def setUp(self):
        a = collection.CollectionMixins()
        kind = choices.MOVIE
        tag = 'xxx'
        path = 'Videos/movies-x'
        album, artist = a.add_members(path,1,kind,tag)
        self.rf = db.Movie.objects.get(title__icontains='apocalypse')

        self.valid_payload = {
            'year': '1994',
            'title': self.rf.title,
            'slug': 'a_slug',
            'fileName': self.rf.fileName,
        }    
        self.invalid_payload = {
            'year': 'not valid year',
            'title': self.rf.title,
            'slug': 'b_slug',
            'fileName': self.rf.fileName, 
        }    
        
    
    def test_update_valid_movie(self):
        response = client.put(
            reverse('builder_movie_detail',kwargs={'slug':self.rf.slug}), 
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_update_invalid_movie(self):
        response = client.put(
            reverse('builder_movie_detail',kwargs={'slug':self.rf.slug}), 
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class MovieTestDelete(TestCase):
    
    def setUp(self):
        a = collection.CollectionMixins()
        kind = choices.MOVIE
        tag = 'xxx'
        path = 'Videos/movies-x'
        album, artist = a.add_members(path,1,kind,tag)
        
    def test_delete_valid_single_movie(self):
        rf = db.Movie.objects.get(title__icontains='apocalypse')
        response = client.delete(reverse('builder_movie_detail',
            kwargs={'slug': rf.slug }))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_delete_invalid_single_movie(self):
        response = client.delete(reverse('builder_movie_detail',
            kwargs={'slug': 'no_movie_like_this' }))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        

