from django.contrib.auth.models import User
from django.test import TestCase
from django.db.models import Q

from FHLBuilder.models import Collection
from FHLBuilder.views import CollectionMixins
from FHLBuilder import choices, collection

from FHLReader import query


class Radio1(TestCase):
    
    def setUp(self):
        self.me = User.objects.create_user('tester','nothere@nothere.com','notreal')
        a = CollectionMixins()
        kind = choices.SONG
        xtag = collection.add_tag('christmas','christmas')
        _,_ = a.add_members('mp3s/Bruce_Cockburn',2,kind,'isa')
        xmas = Collection.objects.get(title__icontains='christmas')
        for s in xmas.songs.all():
            s.tags.add(xtag)

        
    def test1(self):
        
        x1 = Q(title__icontains='landmine')
        
        b1 = Q(title__icontains='glory')
        b2 = Q(title__icontains='bruce')
        b3 = Q(title__icontains='christmas')
        
        colls = Collection.objects.filter(b1|b2|b3)
        nope = Collection.objects.filter(x1)
        
        radio = query.collection_radio_select(colls,False)
        
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

        x1 = Q(title__icontains='landmine')
        
        b1 = Q(title__icontains='glory')
        b2 = Q(title__icontains='bruce')
        b3 = Q(title__icontains='christmas')
        
        colls = Collection.objects.filter(b1|b2|b3)
        nope = Collection.objects.filter(x1)
        
        radio = query.collection_radio_select(colls,True)
        self.check_christmas(radio)
        
        
    def test3(self):

        x1 = Q(title__icontains='landmine')
        
        b1 = Q(title__icontains='glory')
        b2 = Q(title__icontains='bruce')
        b3 = Q(title__icontains='christmas')
        
        colls = Collection.objects.filter(b1|b2|b3)
        nope = Collection.objects.filter(x1)
        
        for b in colls:
            collection.remove_collection(b)
        for x in nope:
            collection.remove_collection(x)
            
            
