# urls
from django.conf.urls import url
from .views import HomePage, TagList, SongList, CollectionList
from .views import TagFormView, TagUpdate, TagDelete, TagDetailView
from .views import SongFormView, SongUpdate, SongDelete, SongDetailView
from .views import CollectionFormView, CollectionUpdate, CollectionDelete, CollectionDetailView

urlpatterns = [
    url(r'^$',HomePage.as_view()),

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

]
