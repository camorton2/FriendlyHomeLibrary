# urls
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
#from django.contrib.auth.decorators import login_required
#from django.views.decorators.cache import cache_page

from FHLReader import views

# READER URLS

urlpatterns = [

# Songs
   url(
       r'^api/v1/songs/(?P<slug>[\w\-]+)/$',
       views.ReaderSongDetail.as_view(),
       name='reader-song-detail'
   ),
   url(
       r'^api/v1/songs/$',
       views.ReaderSongList.as_view(),
       name='reader-song-list'       
   ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
