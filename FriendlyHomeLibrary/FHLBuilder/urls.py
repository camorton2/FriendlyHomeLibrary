# urls
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import HomePage, TagList, SongList, CollectionList,MovieList
from .views import ActorList, DirectorList, MusicianList, UserDetail
from .views import TagFormView, TagUpdate, TagDetailView
from .views import SongFormView, SongUpdate, SongDetailView
from .views import MovieFormView, MovieUpdate, MovieDetailView
from .views import ActorFormView, ActorUpdate, ActorDetailView
from .views import DirectorFormView, DirectorUpdate, DirectorDetailView
from .views import MusicianFormView, MusicianUpdate, MusicianDetailView
from .views import CollectionFormView, CollectionUpdate, CollectionDetailView

urlpatterns = [
#    url(r'^$',HomePage.as_view(),name='homepage'),

    url(r'^user/$',
      UserDetail.as_view(),
      name='user_page'),    

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


]
