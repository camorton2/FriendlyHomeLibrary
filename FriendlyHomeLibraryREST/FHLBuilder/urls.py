# urls
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
#from django.contrib.auth.decorators import login_required
#from django.views.decorators.cache import cache_page

from FHLBuilder import views

urlpatterns = [


# Songs
   url(
       r'^api/v1/songs/(?P<slug>[\w\-]+)/$',
       views.get_delete_update_song,
       name='get_delete_update_song'
   ),
   url(
       r'^api/v1/songs/$',
       views.get_post_songs,
       name='get_post_songs'       
   ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
