# urls
from django.conf.urls import url
from .views import HomePage, TagList, tag_detail, CommonList, SongList

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
    url(r'^tag/(?P<slug>[\w\-]+)/$',
      tag_detail,
      name='builder_tag_detail'),
]
