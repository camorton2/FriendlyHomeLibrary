# urls
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from FHLBuilder import views as bv
from FHLBuilder.url_utility import sorder, artist


urlpatterns = [

#lists
    url(r'^tag/$',
      bv.TagList.as_view(),
      name='builder_tag_list'),
    url(r'^collection/$',
      bv.CollectionList.as_view(),
      name='builder_collection_list'),
    url(r'^byfile/$',
      bv.AllFilesView.as_view(),
      name='builder_all_list'),
# uncached is better when debugging
#    url(sorder, 
#        bv.FileList.as_view(), 
#        name='builder_file_list'),
    url(sorder, 
        cache_page(60*15)(bv.FileList.as_view()), 
        name='builder_file_list'),
    url(artist, bv.ArtistList.as_view(), name='artist_list'),
    
# Tags
    url(r'^tag-cleanup/$',
      login_required(bv.TagCleanupView.as_view()),
      name='builder_tag_remove'),
    url(r'^tag/(?P<slug>[\w\-]+)/$',
      bv.TagDetailView.as_view(),
      name='builder_tag_detail'),

# Actors
    url(r'^actor-cleanup/$',
      login_required(bv.ActorCleanupView.as_view()),
      name='builder_actor_remove'),
    url(r'^actor/(?P<slug>[\w\-]+)/$',
      bv.ActorDetailView.as_view(),
      name='builder_actor_detail'),

# Directors
    url(r'^director-cleanup/$',
      login_required(bv.DirectorCleanupView.as_view()),
      name='builder_director_remove'),
    url(r'^director/(?P<slug>[\w\-]+)/$',
      bv.DirectorDetailView.as_view(),
      name='builder_director_detail'),

# Musicians
    url(r'^musician-cleanup/$',
      login_required(bv.MusicianCleanupView.as_view()),
      name='builder_musician_remove'),
    url(r'^musician/(?P<slug>[\w\-]+)/$',
      bv.MusicianDetailView.as_view(),
      name='builder_musician_detail'),

# Songs
    url(r'^song-cleanup/$',
      login_required(bv.SongCleanupView.as_view()),
      name='builder_song_remove'),
    url(r'^song/(?P<slug>[\w\-]+)/$',
      bv.SongDetailView.as_view(),
      name='builder_song_detail'),

# Pictures
    url(r'^picture-cleanup/$',
      login_required(bv.PictureCleanupView.as_view()),
      name='builder_picture_remove'),
    url(r'^picture/(?P<slug>[\w\-]+)/$',
      bv.PictureDetailView.as_view(),
      name='builder_picture_detail'),
    url(r'^picture-show/(?P<slug>[\w\-]+)/((?P<index>[0-9]+))/(?P<pictureCount>[0-9]+)/$',
      bv.PictureShowView.as_view(),
      name='builder_picture_show'),

# Collections
    url(r'^collection-cleanup/$',
      login_required(bv.CollectionCleanupView.as_view()),
      name='builder_collection_remove'),
    url(r'^collection/create/$',
      login_required(bv.CollectionFormView.as_view()),
      name='builder_collection_create'),
    url(r'^collection/(?P<slug>[\w\-]+)/update/$',
      login_required(bv.CollectionUpdate.as_view()),
      name='builder_collection_update'),      
    url(r'^collection/(?P<slug>[\w\-]+)/$',
      bv.CollectionDetailView.as_view(),
      name='builder_collection_detail'),

# Movies
    url(r'^movie-cleanup/$',
      login_required(bv.MovieCleanupView.as_view()),
      name='builder_movie_remove'),
    url(r'^movie/(?P<slug>[\w\-]+)/$',
      bv.MovieDetailView.as_view(),
      name='builder_movie_detail'),

# diagnostics
    url(r'^diagnostics/$', 
        login_required(bv.DiagnosticsView.as_view()),
        name='builder_diagnostics'),
]
