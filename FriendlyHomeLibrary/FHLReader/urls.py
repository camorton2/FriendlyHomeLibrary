# urls
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from FHLReader import views

urlpatterns = [
    url(r'^$', views.UserDetail.as_view(), name='user_page'),    
    url(r'^songs', views.UserSongList.as_view(), name='user_songs'),
    url(r'^movies', views.UserMovieList.as_view(), name='user_movies'),
    url(r'^channels', views.UserChannels.as_view(), name='user_channels'),
    url(r'^random', views.RandomList.as_view(), name='random_list'),
    url(r'^cached', views.CachedFileList.as_view(), name='cached_list'),
]
