# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

from FHLBuilder.models import Song, Collection, Movie, Musician
from FHLBuilder.models import Tag
from FHLBuilder.views import CollectionMixins
from FHLBuilder import choices
from FHLBuilder import collection as cu



class SpringsteenRemove(TestCase):
    
    def setUp(self):
        a = CollectionMixins()
        kind = choices.SONG
        tag = 'abc'
        path = 'mp3s/Bruce_Springsteen'
        album, artist = a.add_members(path,2,kind,tag)
        path1 = 'mp3s/Doobie_Brothers'
        album1, artist1 = a.add_members(path1,2,kind,tag)
        
    
    def test1(self):
        self.assertEqual(Musician.objects.count(),2)
        mus = Musician.objects.get(fullName__icontains='springsteen')
        self.assertEqual(mus.albums.count(),10)
        cu.remove_musician(mus)
        self.assertEqual(Musician.objects.count(),1)
        mus = Musician.objects.filter(fullName__icontains='springsteen')
        self.assertEqual(mus.count(),0)
        mus = Musician.objects.get(fullName__icontains='doobie')
        self.assertEqual(Song.objects.count(),11)
        collections = Collection.objects.all()
        self.assertEqual(collections.count(),1)
        self.assertEqual(collections[0].title, 'best of the doobies')


class MovieRemove(TestCase):
    
    def setUp(self):
        a = CollectionMixins()
        kind = choices.SONG
        tag = 'mva'
        path = 'Videos/movies-a'
        album, artist = a.add_members(path,1,kind,tag)
        tag1 = 'mvb'
        path1 = 'Videos/movies-b'
        album1, artist1 = a.add_members(path1,1,kind,tag1)
        
    
    def test1(self):
        tga = Tag.objects.get(name__icontains='mva')
        tgb = Tag.objects.get(name__icontains='mvb')
        amovie = Movie.objects.filter(title__icontains='airport')
        self.assertEqual(amovie.count(),3)
        bmovie = Movie.objects.filter(title__icontains='batman')
        self.assertEqual(bmovie.count(),9)
        for mv in amovie.all():
            mv.tags.add(tgb)
        for mv in bmovie.all():
            mv.tags.add(tga)
        cu.remove_tag(tga)
        for mv in Movie.objects.all():
            for tg in mv.tags.all():
                self.assertEqual(tg.name,'mvb')
                
    def test2(self):
        amovie = Movie.objects.filter(title__icontains='airport')
        self.assertEqual(amovie.count(),3)
        bmovie = Movie.objects.filter(title__icontains='batman')
        self.assertEqual(bmovie.count(),9)
        cu.remove_movie(bmovie[3])
        self.assertEqual(bmovie.count(),8)



