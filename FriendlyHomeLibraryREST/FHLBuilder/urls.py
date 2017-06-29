# urls
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
#from django.contrib.auth.decorators import login_required
#from django.views.decorators.cache import cache_page

from FHLBuilder import views

# BUILDER URL PATTERNS

urlpatterns = [

# Users
   url(
       r'^api/v1/users/(?P<pk>[0-9]+)/$',
       views.UserDetail.as_view(),
       name='user_detail'
   ),
   url(
       r'^api/v1/users/$',
       views.UserList.as_view(),
       name='user_list'       
   ),

# Songs
   url(
       r'^api/v1/songs/(?P<slug>[\w\-]+)/$',
       views.builder_song_detail,
       name='builder_song_detail'
   ),
   url(
       r'^api/v1/songs/$',
       views.builder_song_list,
       name='builder_song_list'       
   ),
# Movies
   url(
       r'^api/v1/movies/(?P<slug>[\w\-]+)/$',
       views.BuilderMovieDetail.as_view(),
       name='builder_movie_detail'
   ),
   url(
       r'^api/v1/movies/$',
       views.BuilderMovieList.as_view(),
       name='builder_movie_list'       
   ),

# Pictures 
   url(
       r'^api/v1/pictures/(?P<slug>[\w\-]+)/$',
       views.BuilderPictureDetail.as_view(),
       name='builder_picture_detail'
   ),
   url(
       r'^api/v1/pictures/$',
       views.BuilderPictureList.as_view(),
       name='builder_picture_list'       
   ),
   
]

urlpatterns = format_suffix_patterns(urlpatterns)
