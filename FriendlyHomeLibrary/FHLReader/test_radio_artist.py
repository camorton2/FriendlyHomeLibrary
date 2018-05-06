# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase
from django.db.models import Q

from FHLBuilder.models import Collection, Musician
from FHLBuilder.views import CollectionMixins
from FHLBuilder import choices, collection

from FHLReader import query


class Radio1(TestCase):
    
    def setUp(self):
        self.me = User.objects.create_user('tester','nothere@nothere.com','notreal')
        a = CollectionMixins()
        kind = choices.SONG
        xtag = collection.add_tag('christmas','christmas')
        _,_ = a.add_members('mp3s/Chris Isaak',2,kind,'isa')
        _,_ = a.add_members('mp3s/Blue_Rodeo',2,kind,'blu')
        _,_ = a.add_members('mp3s/Holly_Cole',2,kind,'goo')
        _,_ = a.add_members('mp3s/Dixie_Chicks',2,kind,'goo')
        xmas = Collection.objects.get(title__icontains='merrie')
        for s in xmas.songs.all():
            s.tags.add(xtag)

        
    def test1(self):

        x1 = Q(fullName__icontains='dixie')        
        
        b1 = Q(fullName__icontains='blue')
        b2 = Q(fullName__icontains='isaak')
        b3 = Q(fullName__icontains='cole')
        
        art = Musician.objects.filter(b1|b2|b3)
        nope = Musician.objects.filter(x1)
        
        radio = query.artist_radio_select(art,False)
        
        for s in radio:
            xt = s.tags.filter(name__icontains='christmas')
            self.assertTrue(len(xt)==0)
            for sart in s.song_musicians.all():
                self.assertNotIn(sart,nope)
                
                
    def check_christmas(self,radio):
        """ make sure list has at least 1 christmas song """
        xcount = 0
        for s in radio:
            if s.tags.filter(name__icontains='christmas'):
                xcount=xcount+1
        self.assertTrue(xcount > 0)
        

    def test2(self):

        x1 = Q(fullName__icontains='dixie')        
        
        b1 = Q(fullName__icontains='blue')
        b2 = Q(fullName__icontains='isaak')
        b3 = Q(fullName__icontains='cole')
        
        art = Musician.objects.filter(b1|b2|b3)
        nope = Musician.objects.filter(x1)
        
        radio = query.artist_radio_select(art,True)
        self.check_christmas(radio)
        
        
