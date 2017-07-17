# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from FHLBuilder.models import Song, Movie, Musician, Picture
from FHLBuilder.views import CollectionMixins
from FHLBuilder import choices, collection

# test client
client = Client()

class ViewGetFunction(TestCase):
    """ testing get from views """
    def setUp(self):
        self.me = User.objects.create_user('tester','nothere@nothere.com','notreal')
        response = client.post(reverse('FHLUser_Login'), {'username': 'tester', 'password': 'notreal'})
        a = CollectionMixins()
        
        self.col,_ = a.add_members('mp3s/Dixie_Chicks',2,choices.SONG,'aaa')
        _,_ = a.add_members('Videos/movies-x',1,choices.MOVIE,'bbb')
        _,_ = a.add_members('picturesbackup/win2001',2,choices.MINI_MOVIE,'ccc')
        
        self.act_slug = 'joe-actor'
        act = collection.add_actor('Joe Actor',self.act_slug)
        self.dtor_slug = 'joe-director'
        dtor = collection.add_director('Joe Actor',self.dtor_slug)
        for x in Movie.objects.all():
            act.movies.add(x)
            dtor.movies.add(x)
        self.song = Song.objects.all()[1]
        self.mus = Musician.objects.all()[0]
        self.mv = Movie.objects.all()[0]
        self.pict = Picture.objects.all()[0]
        
    def test1(self):
        r1 = client.get(reverse('builder_tag_list'))
        self.assertEqual(r1.status_code, 200)
        
    def test2(self):
        r1 = client.get(reverse('builder_collection_list'))
        self.assertEqual(r1.status_code, 200)
        
    def test3(self):
        r1 = client.get(reverse('builder_all_list'))
        self.assertEqual(r1.status_code, 200)

    def test4(self):
        for x in choices.live:
            for y in choices.ordering:
                rx = client.get(reverse('builder_file_list', args=[x,y]))
                self.assertEqual(rx.status_code,200)

    def test5(self):
        r1 = client.get(reverse('builder_tag_detail', kwargs={'slug':'aaa'}))
        self.assertEqual(r1.status_code, 200)

    def test6(self):
        r1 = client.get(reverse('builder_actor_detail', kwargs={'slug':self.act_slug}))
        self.assertEqual(r1.status_code, 200)

    def test7(self):
        r1 = client.get(reverse('builder_movie_detail', kwargs={'slug':self.mv.slug}))
        self.assertEqual(r1.status_code, 200)

    def test8(self):
        r1 = client.get(reverse('builder_song_detail', kwargs={'slug':self.song.slug}))
        self.assertEqual(r1.status_code, 200)

    def test9(self):
        r1 = client.get(reverse('builder_picture_detail', kwargs={'slug':self.pict.slug}))
        self.assertEqual(r1.status_code, 200)

    def test10(self):
        r1 = client.get(reverse('builder_musician_detail', kwargs={'slug':self.mus.slug}))
        self.assertEqual(r1.status_code, 200)

    def test11(self):
        r1 = client.get(reverse('builder_collection_detail', kwargs={'slug':self.col.slug}))
        self.assertEqual(r1.status_code, 200)
