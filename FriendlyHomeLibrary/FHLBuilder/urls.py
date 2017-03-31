# urls
from django.conf.urls import url
from .views import HomePage, TagList, SongList, CollectionList,MovieList
from .views import ActorList, DirectorList, MusicianList
from .views import TagFormView, TagUpdate, TagDelete, TagDetailView
from .views import SongFormView, SongUpdate, SongDelete, SongDetailView
from .views import MovieFormView, MovieUpdate, MovieDelete, MovieDetailView
from .views import ActorFormView, ActorUpdate, ActorDelete, ActorDetailView
from .views import DirectorFormView, DirectorUpdate, DirectorDelete, DirectorDetailView
from .views import MusicianFormView, MusicianUpdate, MusicianDelete, MusicianDetailView
from .views import CollectionFormView, CollectionUpdate, CollectionDelete, CollectionDetailView

urlpatterns = [
#    url(r'^$',HomePage.as_view(),name='homepage'),

#lists
    url(r'^tag/$',
      TagList.as_view(),
      name='builder_tag_list'),
    url(r'^song/$',
      SongList.as_view(),
      name='builder_song_list'),
    url(r'^collection/$',
      CollectionList.as_view(),
      name='builder_collection_list'),
    url(r'^movie/$',
      MovieList.as_view(),
      name='builder_movie_list'),
    url(r'^actor/$',
      ActorList.as_view(),
      name='builder_actor_list'),
    url(r'^director/$',
      DirectorList.as_view(),
      name='builder_director_list'),
    url(r'^musician/$',
      MusicianList.as_view(),
      name='builder_musician_list'),

      
# Tags
    url(r'^tag/create/$',
      TagFormView.as_view(),
      name='builder_tag_create'),
    url(r'^tag/(?P<slug>[\w\-]+)/$',
      TagDetailView.as_view(),
      name='builder_tag_detail'),
    url(r'^tag/(?P<slug>[\w\-]+)/update/$',
      TagUpdate.as_view(),
      name='builder_tag_update'),
    url(r'^tag/(?P<slug>[\w\-]+)/delete/$',
      TagDelete.as_view(),
      name='builder_tag_delete'),

# Actors
    url(r'^actor/create/$',
      ActorFormView.as_view(),
      name='builder_actor_create'),
    url(r'^actor/(?P<slug>[\w\-]+)/$',
      ActorDetailView.as_view(),
      name='builder_actor_detail'),
    url(r'^actor/(?P<slug>[\w\-]+)/update/$',
      ActorUpdate.as_view(),
      name='builder_actor_update'),
    url(r'^actor/(?P<slug>[\w\-]+)/delete/$',
      ActorDelete.as_view(),
      name='builder_actor_delete'),

# Directors
    url(r'^director/create/$',
      DirectorFormView.as_view(),
      name='builder_director_create'),
    url(r'^director/(?P<slug>[\w\-]+)/$',
      DirectorDetailView.as_view(),
      name='builder_director_detail'),
    url(r'^director/(?P<slug>[\w\-]+)/update/$',
      DirectorUpdate.as_view(),
      name='builder_director_update'),
    url(r'^director/(?P<slug>[\w\-]+)/delete/$',
      DirectorDelete.as_view(),
      name='builder_director_delete'),

# Musicians
    url(r'^musician/create/$',
      MusicianFormView.as_view(),
      name='builder_musician_create'),
    url(r'^musician/(?P<slug>[\w\-]+)/$',
      MusicianDetailView.as_view(),
      name='builder_musician_detail'),
    url(r'^musician/(?P<slug>[\w\-]+)/update/$',
      MusicianUpdate.as_view(),
      name='builder_musician_update'),
    url(r'^musician/(?P<slug>[\w\-]+)/delete/$',
      MusicianDelete.as_view(),
      name='builder_musician_delete'),

# Songs
    url(r'^song/create/$',
      SongFormView.as_view(),
      name='builder_song_create'),
    url(r'^song/(?P<slug>[\w\-]+)/$',
      SongDetailView.as_view(),
      name='builder_song_detail'),
    url(r'^song/(?P<slug>[\w\-]+)/update/$',
      SongUpdate.as_view(),
      name='builder_song_update'),
    url(r'^song/(?P<slug>[\w\-]+)/delete/$',
      SongDelete.as_view(),
      name='builder_song_delete'),

# Collections
    url(r'^collection/create/$',
      CollectionFormView.as_view(),
      name='builder_collection_create'),
    url(r'^collection/(?P<slug>[\w\-]+)/$',
      CollectionDetailView.as_view(),
      name='builder_collection_detail'),
    url(r'^collection/(?P<slug>[\w\-]+)/update/$',
      CollectionUpdate.as_view(),
      name='builder_collection_update'),
    url(r'^collection/(?P<slug>[\w\-]+)/delete/$',
      CollectionDelete.as_view(),
      name='builder_collection_delete'),

# Movies
    url(r'^movie/create/$',
      MovieFormView.as_view(),
      name='builder_movie_create'),
    url(r'^movie/(?P<slug>[\w\-]+)/$',
      MovieDetailView.as_view(),
      name='builder_movie_detail'),
    url(r'^movie/(?P<slug>[\w\-]+)/update/$',
      MovieUpdate.as_view(),
      name='builder_movie_update'),
    url(r'^movie/(?P<slug>[\w\-]+)/delete/$',
      MovieDelete.as_view(),
      name='builder_movie_delete'),


]
