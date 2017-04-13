# urls
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from views import UserDetail, UserSongList, UserMovieList


urlpatterns = [
    url(r'^$', UserDetail.as_view(), name='user_page'),    
    url(r'^songs', UserSongList.as_view(), name='user_songs'),
    url(r'^movies', UserMovieList.as_view(), name='user_movies'),
]
