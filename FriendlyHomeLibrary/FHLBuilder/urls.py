# urls
from django.conf.urls import url
from .views import HomePage, TagList, CommonList, SongList
from .views import TagFormView, TagUpdate, TagDelete, TagDetailView
from .views import SongFormView, SongUpdate, SongDelete, SongDetailView

urlpatterns = [
    url(r'^$',HomePage.as_view()),
    url(r'^tag/$',
      TagList.as_view(),
      name='builder_tag_list'),
    url(r'^common/$',
      CommonList.as_view(),
      name='builder_common_list'),
    url(r'^song/$',
      SongList.as_view(),
      name='builder_song_list'),
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
      
      
]
