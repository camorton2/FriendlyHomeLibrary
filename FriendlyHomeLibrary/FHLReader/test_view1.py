# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client

from FHLBuilder.views import CollectionMixins
from FHLBuilder import choices, url_utility

# test client
client = Client()

class ViewPostFunction(TestCase):
    """ testing post from views 
        Still to do: pass forms, verify results rather than just
        status_code
    """
    def setUp(self):
        self.me = User.objects.create_user('tester','nothere@nothere.com','notreal')
        response = client.post(reverse('FHLUser_Login'), {'username': 'tester', 'password': 'notreal'})
        a = CollectionMixins()
        _,_ = a.add_members('mp3s/Dixie_Chicks',2,choices.SONG,'aaa')
        _,_ = a.add_members('Videos/movies-x',1,choices.MOVIE,'bbb')
        _,_ = a.add_members('picturesbackup/win2001',2,choices.MINI_MOVIE,'ccc')
        
    def test1(self):
        r1 = client.post(reverse('random_list'))
        self.assertEqual(r1.status_code, 200)
    
    def test2(self):
        r = client.post(reverse('recent_list'))
        self.assertEqual(r.status_code,200)
        
    def test3(self):
        for x in url_utility.special:
            rx = client.post(reverse('special_channel', args=[x]))
            self.assertEqual(rx.status_code,200)

    def test4(self):
        for x in choices.videos:
            rx = client.post(reverse('movie_channel', args=[x]))
            self.assertEqual(rx.status_code,200)

    def test5(self):
        r = client.post(reverse('radio_channel'))
        self.assertEqual(r.status_code,200)

    def test6(self):
        r = client.post(reverse('mus-radio_channel'))
        self.assertEqual(r.status_code,200)

    def test7(self):
        r = client.post(reverse('col-radio_channel'))
        self.assertEqual(r.status_code,200)

    def test8(self):
        r = client.post(reverse('song-radio_channel'))
        self.assertEqual(r.status_code,200)

    def test9(self):
        r1 = client.post(reverse('date_added_radio_channel', kwargs={'yearA':'2016'}))
        self.assertEqual(r1.status_code, 200)
        
    def test10(self):
        r2 = client.post(reverse('range_added_radio_channel', kwargs={'yearA':'2016','yearB':'2017'}))
        self.assertEqual(r2.status_code, 200)

    def test11(self):
        r1 = client.post(reverse('date_added_radio_channel', kwargs={'yearA':'2017','monthA':'5'}))
        self.assertEqual(r1.status_code, 200)
        
    def test12(self):
        k={'yearA':'2016','monthA':'6','yearB':'2017', 'monthB':'7'}
        r2 = client.post(reverse('range_added_radio_channel', kwargs=k))
        self.assertEqual(r2.status_code, 200)

