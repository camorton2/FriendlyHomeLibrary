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



class PictureTestAdd(TestCase):
    """ no views, just check database creation """    
    def setUp(self):
        a = collection.CollectionMixins()
        kind = choices.MOVIE
        tag = 'xxx'
        path = 'picturesbackup/win2001'
        album, artist = a.add_members(path,2,kind,tag)
                
    def test1(self):
        rf = db.Picture.objects.get(title__icontains='capture')
        self.assertEqual(rf.title,'Capture_00001')
    
    def test2(self):
        self.assertEqual(db.Picture.objects.count(),9)


class PictureTestGet(TestCase):
    """ view functions for get """
    def setUp(self):
        a = collection.CollectionMixins()
        kind = choices.MOVIE
        tag = 'xxx'
        path = 'picturesbackup/win2001'
        album, artist = a.add_members(path,2,kind,tag)
    
    def test_get_all_pictures(self):
        response = client.get(reverse('builder_picture_list'))
        # get data from db
        pictures = db.Picture.objects.all()
        serializer = ss.PictureSerializer(pictures,many=True)
        self.assertEqual(response.data,serializer.data)        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_valid_single_picture(self):
        rf = db.Picture.objects.get(title__icontains='capture')
        response = client.get(reverse('builder_picture_detail',
            kwargs={'slug': rf.slug }))
        serializer=ss.PictureSerializer(rf)
        self.assertEqual(response.data,serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_invalid_single_picture(self):
        response = client.get(reverse('builder_picture_detail',
            kwargs={'slug': 'no_picture_like_this' }))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        

class PictureTestCreate(TestCase):
    
    def setUp(self):
        a = collection.CollectionMixins()
        kind = choices.MOVIE
        tag = 'xxx'
        path = 'picturesbackup/win2001'
        album, artist = a.add_members(path,2,kind,tag)                
        rf = db.Picture.objects.get(title__icontains='capture')

        self.valid_payload = {
            'year': rf.year,
            'title': rf.title,
            'slug': 'a_slug',
            'fileName': rf.fileName,
            #'collection': album # todo figure out nested
        }    
        self.invalid_payload = {
            'year': 'a_a', # error not valid year
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

    
    def test_create_valid_picture(self):
        response = client.post(
            reverse('builder_picture_list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_invalid_picture(self):
        response = client.post(
            reverse('builder_picture_list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_picture1(self):
        response = client.post(
            reverse('builder_picture_list'),
            data=json.dumps(self.invalid_payload1),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

class PictureTestUpdate(TestCase):
    
    def setUp(self):
        a = collection.CollectionMixins()
        kind = choices.MOVIE
        tag = 'xxx'
        path = 'picturesbackup/win2001'
        album, artist = a.add_members(path,2,kind,tag)                
        self.rf = db.Picture.objects.get(title__icontains='capture')

        self.valid_payload = {
            'year': '1994',
            'title': self.rf.title,
            'slug': 'a_slug',
            'fileName': self.rf.fileName,
        }    
        self.invalid_payload = {
            'year': 'a_a', # not valid picture
            'title': self.rf.title,
            'slug': 'b_slug',
            'fileName': self.rf.fileName, 
        }    
        
    
    def test_update_valid_picture(self):
        response = client.put(
            reverse('builder_picture_detail',kwargs={'slug':self.rf.slug}), 
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_update_invalid_picture(self):
        response = client.put(
            reverse('builder_picture_detail',kwargs={'slug':self.rf.slug}), 
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class PictureTestDelete(TestCase):
    
    def setUp(self):
        a = collection.CollectionMixins()
        kind = choices.MOVIE
        tag = 'xxx'
        path = 'picturesbackup/win2001'
        album, artist = a.add_members(path,2,kind,tag)                
        
    def test_delete_valid_single_picture(self):
        rf = db.Picture.objects.get(title__icontains='capture')
        response = client.delete(reverse('builder_picture_detail',
            kwargs={'slug': rf.slug }))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_delete_invalid_single_picture(self):
        response = client.delete(reverse('builder_picture_detail',
            kwargs={'slug': 'no_picture_like_this' }))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        

