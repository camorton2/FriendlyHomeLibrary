from django.test import TestCase

# Create your tests here.

from FHLBuilder.models import Song, Collection, Movie, Picture, Musician
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


class Manx(TestCase):
    
    def setUp(self):
        a = CollectionMixins()
        kind = choices.SONG
        tag = 'mmm'
        path = 'mp3s/Harry Manx'
        album, artist = a.add_members(path,2,kind,tag)
        
    def test1(self):
        rf = Collection.objects.get(title__icontains='lift')
        self.assertEqual(rf.songs.count(),12)
        
    def test2(self):
        rf = Song.objects.get(title__icontains='spark')
        self.assertEqual(rf.track,10)
    
    def test3(self):
        mus = Musician.objects.get(fullName__icontains='manx')
        self.assertEqual(mus.albums.count(),1)


class SherylCrow(TestCase):
    
    def setUp(self):
        a = CollectionMixins()
        kind = choices.SONG
        tag = 'mmm'
        path = 'mp3s/Sheryl_Crow'
        album, artist = a.add_members(path,2,kind,tag)
        album, artist = a.add_members(path,2,kind,tag)
        album, artist = a.add_members(path,2,kind,tag)
        album, artist = a.add_members(path,2,kind,tag)
        
    def test1(self):
        rf = Collection.objects.get(title__icontains='myself')
        self.assertEqual(rf.songs.count(),11)
        
    def test2(self):
        rf = Song.objects.get(title__icontains='skate')
        self.assertEqual(rf.track,5)
    
    def test3(self):
        mus = Musician.objects.get(fullName__icontains='sheryl')
        self.assertEqual(mus.albums.count(),4)
        

class Springsteen(TestCase):
    
    def setUp(self):
        a = CollectionMixins()
        kind = choices.SONG
        tag = 'abc'
        path = 'mp3s/Bruce_Springsteen'
        album, artist = a.add_members(path,2,kind,tag)

    def test1(self):
        rf = Collection.objects.get(title__icontains='dublin')
        self.assertEqual(rf.songs.count(),23)        
        
    def test2(self):
        rf = Collection.objects.get(title__icontains='born_in')
        self.assertEqual(rf.songs.count(),12)
        
    def test3(self):
        rf = Song.objects.get(title__icontains='on fire')
        self.assertEqual(rf.track,6)
    
    def test4(self):
        mus = Musician.objects.get(fullName__icontains='springsteen')
        self.assertEqual(mus.albums.count(),10)



class MovieCollection(TestCase):
    
    def setUp(self):
        a = CollectionMixins()
        kind = choices.MOVIE
        tag = 'xxx'
        path = 'Videos/movies-x'
        album, artist = a.add_members(path,1,kind,tag)
                
    def test1(self):
        rf = Movie.objects.filter(title__icontains='x-men')
        self.assertEqual(rf.count(),10)
    
    def test2(self):
        self.assertEqual(Movie.objects.count(),13)
        

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


