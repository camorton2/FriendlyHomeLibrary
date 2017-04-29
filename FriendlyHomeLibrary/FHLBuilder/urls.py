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
    url(r'^collection/$',
      bv.CollectionList.as_view(),
      name='builder_collection_list'),
    url(r'^files/$',
      bv.FileList.as_view(),
      name='builder_file_list'),
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
    url(r'^tag/(?P<slug>[\w\-]+)/$',
      bv.TagDetailView.as_view(),
      name='builder_tag_detail'),

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
    url(r'^song/(?P<slug>[\w\-]+)/$',
      bv.SongDetailView.as_view(),
      name='builder_song_detail'),

# Pictures
    url(r'^picture/(?P<slug>[\w\-]+)/$',
      bv.PictureDetailView.as_view(),
      name='builder_picture_detail'),

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
    url(r'^movie/(?P<slug>[\w\-]+)/$',
      bv.MovieDetailView.as_view(),
      name='builder_movie_detail'),

# diagnostics
    url(r'^diagnostics/$', bv.DiagnosticsView.as_view(),
        name='builder_diagnostics'),
]
