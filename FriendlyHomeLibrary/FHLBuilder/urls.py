# urls
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

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
      login_required(TagFormView.as_view()),
      name='builder_tag_create'),
    url(r'^tag/(?P<slug>[\w\-]+)/$',
      TagDetailView.as_view(),
      name='builder_tag_detail'),
    url(r'^tag/(?P<slug>[\w\-]+)/update/$',
      login_required(TagUpdate.as_view()),
      name='builder_tag_update'),
    url(r'^tag/(?P<slug>[\w\-]+)/delete/$',
      login_required(TagDelete.as_view()),
      name='builder_tag_delete'),

# Actors
    url(r'^actor/create/$',
      login_required(ActorFormView.as_view()),
      name='builder_actor_create'),
    url(r'^actor/(?P<slug>[\w\-]+)/$',
      ActorDetailView.as_view(),
      name='builder_actor_detail'),
    url(r'^actor/(?P<slug>[\w\-]+)/update/$',
      login_required(ActorUpdate.as_view()),
      name='builder_actor_update'),
    url(r'^actor/(?P<slug>[\w\-]+)/delete/$',
      login_required(ActorDelete.as_view()),
      name='builder_actor_delete'),

# Directors
    url(r'^director/create/$',
      login_required(DirectorFormView.as_view()),
      name='builder_director_create'),
    url(r'^director/(?P<slug>[\w\-]+)/$',
      DirectorDetailView.as_view(),
      name='builder_director_detail'),
    url(r'^director/(?P<slug>[\w\-]+)/update/$',
      login_required(DirectorUpdate.as_view()),
      name='builder_director_update'),
    url(r'^director/(?P<slug>[\w\-]+)/delete/$',
      login_required(DirectorDelete.as_view()),
      name='builder_director_delete'),

# Musicians
    url(r'^musician/create/$',
      login_required(MusicianFormView.as_view()),
      name='builder_musician_create'),
    url(r'^musician/(?P<slug>[\w\-]+)/$',
      MusicianDetailView.as_view(),
      name='builder_musician_detail'),
    url(r'^musician/(?P<slug>[\w\-]+)/update/$',
      login_required(MusicianUpdate.as_view()),
      name='builder_musician_update'),
    url(r'^musician/(?P<slug>[\w\-]+)/delete/$',
      login_required(MusicianDelete.as_view()),
      name='builder_musician_delete'),

# Songs
    url(r'^song/create/$',
      login_required(SongFormView.as_view()),
      name='builder_song_create'),
    url(r'^song/(?P<slug>[\w\-]+)/$',
      SongDetailView.as_view(),
      name='builder_song_detail'),
    url(r'^song/(?P<slug>[\w\-]+)/update/$',
      login_required(SongUpdate.as_view()),
      name='builder_song_update'),
    url(r'^song/(?P<slug>[\w\-]+)/delete/$',
      login_required(SongDelete.as_view()),
      name='builder_song_delete'),

# Collections
    url(r'^collection/create/$',
      login_required(CollectionFormView.as_view()),
      name='builder_collection_create'),
    url(r'^collection/(?P<slug>[\w\-]+)/$',
      CollectionDetailView.as_view(),
      name='builder_collection_detail'),
    url(r'^collection/(?P<slug>[\w\-]+)/update/$',
      login_required(CollectionUpdate.as_view()),
      name='builder_collection_update'),
    url(r'^collection/(?P<slug>[\w\-]+)/delete/$',
      login_required(CollectionDelete.as_view()),
      name='builder_collection_delete'),

# Movies
    url(r'^movie/create/$',
      login_required(MovieFormView.as_view()),
      name='builder_movie_create'),
    url(r'^movie/(?P<slug>[\w\-]+)/$',
      MovieDetailView.as_view(),
      name='builder_movie_detail'),
    url(r'^movie/(?P<slug>[\w\-]+)/update/$',
      login_required(MovieUpdate.as_view()),
      name='builder_movie_update'),
    url(r'^movie/(?P<slug>[\w\-]+)/delete/$',
      login_required(MovieDelete.as_view()),
      name='builder_movie_delete'),


]
