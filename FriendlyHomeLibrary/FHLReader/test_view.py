# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from FHLBuilder.views import CollectionMixins
from FHLBuilder import choices, url_utility

# test client
client = Client()

class ViewGetFunction(TestCase):
    """ testing get from views 
        Still to do: verify results rather than just status_code
    """
    def setUp(self):
        self.me = User.objects.create_user('tester','nothere@nothere.com','notreal')
        response = client.post(reverse('FHLUser_Login'), {'username': 'tester', 'password': 'notreal'})
        a = CollectionMixins()
        _,_ = a.add_members('mp3s/Dixie_Chicks',2,choices.SONG,'aaa')
        _,_ = a.add_members('Videos/movies-x',1,choices.MOVIE,'bbb')
        _,_ = a.add_members('picturesbackup/win2001',2,choices.MINI_MOVIE,'ccc')
        
    def test1(self):
        r1 = client.get(reverse('user_page'))
        self.assertEqual(r1.status_code, 200)
        #print(r1.context)
        
    def test2(self):
        #url(r'^pictures/(liked|loved|both|random)$', views.UserPictureList.as_view(), name='user_pictures'),    
        r2 = client.get(reverse('user_pictures', args=['liked']))
        self.assertEqual(r2.status_code, 200)
        r2 = client.get(reverse('user_pictures', args=['loved']))
        self.assertEqual(r2.status_code, 200)
        r2 = client.get(reverse('user_pictures', args=['both']))
        self.assertEqual(r2.status_code, 200)
        r2 = client.get(reverse('user_pictures', args=['random']))
        self.assertEqual(r2.status_code, 200)

    def test3(self):
        #url(r'^songs/(liked|loved|both|random)$', views.UserSongList.as_view(), name='user_songs'),
        r2 = client.get(reverse('user_songs', args=['liked']))
        self.assertEqual(r2.status_code, 200)
        r2 = client.get(reverse('user_songs', args=['loved']))
        self.assertEqual(r2.status_code, 200)
        r2 = client.get(reverse('user_songs', args=['both']))
        self.assertEqual(r2.status_code, 200)
        r2 = client.get(reverse('user_songs', args=['random']))
        self.assertEqual(r2.status_code, 200)
        
    def test4(self):
        #url(r'^videos/(liked|loved|both|random)$', views.UserVideoList.as_view(), name='user_videos'),
        r2 = client.get(reverse('user_videos', args=['liked']))
        self.assertEqual(r2.status_code, 200)
        r2 = client.get(reverse('user_videos', args=['loved']))
        self.assertEqual(r2.status_code, 200)
        r2 = client.get(reverse('user_videos', args=['both']))
        self.assertEqual(r2.status_code, 200)
        r2 = client.get(reverse('user_videos', args=['random']))
        self.assertEqual(r2.status_code, 200)
            
    def test5(self):
        #url(vchannel, views.MovieChannel.as_view(), name='movie_channel'),
        for x in choices.videos:
            rx = client.get(reverse('movie_channel', args=[x]))
            self.assertEqual(rx.status_code,200)

    def test6(self):        
        #url(schannel, views.SpecialChannel.as_view(), name='special_channel'),
        for x in url_utility.special:
            rx = client.get(reverse('special_channel', args=[x]))
            self.assertEqual(rx.status_code,200)

    def test7(self):
        #url(r'^radio$', views.RadioChannel.as_view(), name='radio_channel'),
        r = client.get(reverse('radio_channel'))
        self.assertEqual(r.status_code,200)
    
    def test8(self):
        #url(r'^radio_mus$', views.MusicianRadioChannel.as_view(), name='mus-radio_channel'),
        r = client.get(reverse('mus-radio_channel'))
        self.assertEqual(r.status_code,200)

    def test9(self):
        #url(r'^radio_col$', views.CollectionRadioChannel.as_view(), name='col-radio_channel'),
        r = client.get(reverse('col-radio_channel'))
        self.assertEqual(r.status_code,200)
    
    def test10(self):
        #url(r'^radio_song$', views.SongRadioChannel.as_view(), name='song-radio_channel'),
        r = client.get(reverse('song-radio_channel'))
        self.assertEqual(r.status_code,200)

    def test11(self):
        #url(r'^random$', views.RandomList.as_view(), name='random_list'),
        r = client.get(reverse('random_list'))
        self.assertEqual(r.status_code,200)
        
    def test12(self):
        #url(r'^recent$', views.RecentList.as_view(), name='recent_list'),
        r = client.get(reverse('recent_list'))
        self.assertEqual(r.status_code,200)
        
    def test13(self):
        #url(r'^cached$', views.CachedFileList.as_view(), name='cached_list'),
        r = client.get(reverse('cached_list'))
        self.assertEqual(r.status_code,200)

    def test14(self):
        r1 = client.get(reverse('date_added_radio_channel', kwargs={'yearA':'2016'}))
        self.assertEqual(r1.status_code, 200)
        
    def test15(self):
        r2 = client.get(reverse('range_added_radio_channel', kwargs={'yearA':'2016','yearB':'2017'}))
        self.assertEqual(r2.status_code, 200)

    def test16(self):
        r1 = client.get(reverse('date_added_radio_channel', kwargs={'yearA':'2017','monthA':'5'}))
        self.assertEqual(r1.status_code, 200)
        
    def test17(self):
        k={'yearA':'2016','monthA':'6','yearB':'2017', 'monthB':'7'}
        r2 = client.get(reverse('range_added_radio_channel', kwargs=k))
        self.assertEqual(r2.status_code, 200)

        
