from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client

from FHLBuilder.models import Song, Movie, Musician, Picture
from FHLBuilder.views import CollectionMixins
from FHLBuilder import choices, collection

# test client
client = Client()

class ViewPostFunction(TestCase):
    """ testing get from views using post
        Still to do, pass data, check results other that status
    """
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
        r1 = client.post(reverse('builder_song_detail', kwargs={'slug':self.song.slug}))
        self.assertEqual(r1.status_code, 200)

    def test2(self):
        r1 = client.post(reverse('builder_all_list'))
        self.assertEqual(r1.status_code, 200)

    def test3(self):
        r1 = client.post(reverse('builder_collection_create'))
        # permission denined for reader, need builder
        self.assertEqual(r1.status_code, 403)
        
    def test4(self):
        r1 = client.post(reverse('builder_collection_update',kwargs={'slug':self.col.slug}))
        # required builder permission
        self.assertEqual(r1.status_code, 403)

    def test5(self):
        r1 = client.post(reverse('builder_movie_detail', kwargs={'slug':self.mv.slug}))
        self.assertEqual(r1.status_code, 200)

    def test6(self):
        r1 = client.get(reverse('builder_picture_detail', kwargs={'slug':self.pict.slug}))
        self.assertEqual(r1.status_code, 200)

