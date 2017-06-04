# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase

from FHLBuilder.models import Song, Collection
from FHLBuilder.views import CollectionMixins
from FHLBuilder import choices, collection

from FHLReader import query


class Radio1(TestCase):
    
    def setUp(self):
        self.me = User.objects.create_user('tester','nothere@nothere.com','notreal')
        a = CollectionMixins()
        kind = choices.SONG
        xtag = collection.add_tag('christmas','christmas')
        _,_ = a.add_members('mp3s/Chris_Isaak',2,kind,'isa')
        _,_ = a.add_members('mp3s/Chris_Rea',2,kind,'rea')
        _,_ = a.add_members('mp3s/Good_Family',2,kind,'goo')
        _,_ = a.add_members('mp3s/Dixie_Chicks',2,kind,'goo')
        xmas = Collection.objects.get(title__icontains='christmas')
        for s in xmas.songs.all():
            s.tags.add(xtag)
        nosongq = Song.objects.filter(title__icontains='road')
        self.nosong = list(nosongq)
        for x in self.nosong:
            x.dislikes.add(self.me)
        self.assertFalse(len(self.nosong) == 0)
        self.mysong = []
        
    def test1(self):
        full = query.radio_select(False,self.me,Song.objects.all())
        radio = full[:30]
        for s in radio:
            xt = s.tags.filter(name__icontains='christmas')
            self.assertTrue(len(xt)==0)
    
        self.assertNotIn(self.nosong,radio)        
        

    def test2(self):
        # no songs in my list
        self.assertTrue(len(self.mysong)==0)
        full = query.radio_select(True,self.me,Song.random_objects.all())
        radio = full[:30]
        for s in radio:
            xt = s.tags.filter(name__icontains='christmas')
            self.assertTrue(len(xt)==0)
        for x in self.nosong:
            self.assertNotIn(x,radio)        


    def test3(self):
        # one song in my list
        mysongq = Song.objects.filter(title__icontains='remember')
        self.mysong = list(mysongq)
        self.assertTrue(len(self.mysong)==1)
        for x in self.mysong:
            x.loves.add(self.me)
        
        full = query.radio_select(True,self.me,Song.random_objects.all())
        radio = full[:30]
        for s in radio:
            xt = s.tags.filter(name__icontains='christmas')
            self.assertTrue(len(xt)==0)
        for x in self.nosong:
            self.assertNotIn(x,radio)
        for y in self.mysong:
            self.assertIn(y,radio)
        

    def test4(self):
        # more than one song in my list
        for sg in  Song.objects.filter(title__icontains='remember'):
            self.mysong.append(sg)
            sg.loves.add(self.me)
        for sg in Song.objects.filter(title__icontains='heartache'):
            sg.likes.add(self.me)
            self.mysong.append(sg)
           
        self.assertTrue(len(self.mysong)>1)
        
        full = query.radio_select(True,self.me,Song.random_objects.all())
        radio = full[:50]
        for s in radio:
            xt = s.tags.filter(name__icontains='christmas')
            self.assertTrue(len(xt)==0)
        for x in self.nosong:
            self.assertNotIn(x,radio)
        for y in self.mysong:
            self.assertIn(y,radio)


    def check_christmas(self,radio):
        """ make sure list has at least 1 christmas song """
        xcount = 0
        for s in radio:
            if s.tags.filter(name__icontains='christmas'):
                xcount=xcount+1
        self.assertTrue(xcount > 0)


    def test5(self):
        full = query.radio_select_christmas(False,self.me,Song.objects.all())
        radio = full[:30]
        self.check_christmas(radio)
        self.assertNotIn(self.nosong,radio)        


    def test6(self):
        # no songs in my list
        self.assertTrue(len(self.mysong)==0)
        full = query.radio_select_christmas(True,self.me,Song.random_objects.all())
        radio = full[:30]
        self.check_christmas(radio)
        for x in self.nosong:
            self.assertNotIn(x,radio)        


    def test7(self):
        # one song in my list
        mysongq = Song.objects.filter(title__icontains='remember')
        self.mysong = list(mysongq)
        self.assertTrue(len(self.mysong)==1)
        for x in self.mysong:
            x.loves.add(self.me)
        
        full = query.radio_select_christmas(True,self.me,Song.random_objects.all())
        radio = full[:30]
        self.check_christmas(radio)
        for x in self.nosong:
            self.assertNotIn(x,radio)
        for y in self.mysong:
            self.assertIn(y,radio)
        

    def test8(self):
        # more than one song in my list
        for sg in  Song.objects.filter(title__icontains='remember'):
            self.mysong.append(sg)
            sg.loves.add(self.me)
        for sg in Song.objects.filter(title__icontains='heartache'):
            sg.likes.add(self.me)
            self.mysong.append(sg)
           
        self.assertTrue(len(self.mysong)>1)
        
        full = query.radio_select_christmas(True,self.me,Song.random_objects.all())
        radio = full[:50]
        
        self.check_christmas(radio)
                
        for x in self.nosong:
            self.assertNotIn(x,radio)
        for y in self.mysong:
            self.assertIn(y,radio)


