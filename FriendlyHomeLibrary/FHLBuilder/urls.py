# urls
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from FHLBuilder import views as bv

urlpatterns = [
#    url(r'^$',HomePage.as_view(),name='homepage'),

#lists
    url(r'^tag/$',
      bv.TagList.as_view(),
      name='builder_tag_list'),
    url(r'^song/$',
      bv.SongList.as_view(),
      name='builder_song_list'),
    url(r'^collection/$',
      bv.CollectionList.as_view(),
      name='builder_collection_list'),
    url(r'^movie/$',
      bv.MovieList.as_view(),
      name='builder_movie_list'),
    url(r'^concert/$',
      bv.ConcertList.as_view(),
      name='builder_concert_list'),
    url(r'^tv/$',
      bv.TVList.as_view(),
      name='builder_TV_list'),
    url(r'^miniseries/$',
      bv.MiniSeriesList.as_view(),
      name='builder_miniseries_list'),      
    url(r'^actor/$',
      bv.ActorList.as_view(),
      name='builder_actor_list'),
    url(r'^director/$',
      bv.DirectorList.as_view(),
      name='builder_director_list'),
    url(r'^musician/$',
      bv.MusicianList.as_view(),
      name='builder_musician_list'),

      
# Tags
    url(r'^tag/create/$',
      login_required(bv.TagFormView.as_view()),
      name='builder_tag_create'),
    url(r'^tag/(?P<slug>[\w\-]+)/$',
      bv.TagDetailView.as_view(),
      name='builder_tag_detail'),
    url(r'^tag/(?P<slug>[\w\-]+)/update/$',
      login_required(bv.TagUpdate.as_view()),
      name='builder_tag_update'),

# Actors
    url(r'^actor/(?P<slug>[\w\-]+)/$',
      bv.ActorDetailView.as_view(),
      name='builder_actor_detail'),

# Directors
    url(r'^director/(?P<slug>[\w\-]+)/$',
      bv.DirectorDetailView.as_view(),
      name='builder_director_detail'),

# Musicians
    url(r'^musician/(?P<slug>[\w\-]+)/$',
      bv.MusicianDetailView.as_view(),
      name='builder_musician_detail'),

# Songs
    url(r'^song/create/$',
      login_required(bv.SongFormView.as_view()),
      name='builder_song_create'),
    url(r'^song/(?P<slug>[\w\-]+)/$',
      bv.SongDetailView.as_view(),
      name='builder_song_detail'),
    url(r'^song/(?P<slug>[\w\-]+)/update/$',
      login_required(bv.SongUpdate.as_view()),
      name='builder_song_update'),

# Collections
    url(r'^collection/create/$',
      login_required(bv.CollectionFormView.as_view()),
      name='builder_collection_create'),
    url(r'^collection/(?P<slug>[\w\-]+)/$',
      bv.CollectionDetailView.as_view(),
      name='builder_collection_detail'),
    url(r'^collection/(?P<slug>[\w\-]+)/update/$',
      login_required(bv.CollectionUpdate.as_view()),
      name='builder_collection_update'),

# Movies
    url(r'^movie/create/$',
      login_required(bv.MovieFormView.as_view()),
      name='builder_movie_create'),
    url(r'^movie/(?P<slug>[\w\-]+)/$',
      bv.MovieDetailView.as_view(),
      name='builder_movie_detail'),
    url(r'^movie/(?P<slug>[\w\-]+)/update/$',
      login_required(bv.MovieUpdate.as_view()),
      name='builder_movie_update'),

]
