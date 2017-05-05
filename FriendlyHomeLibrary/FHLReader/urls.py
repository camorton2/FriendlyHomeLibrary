# urls
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from FHLReader import views
from FHLBuilder import choices

liked = 'liked'
loved = 'loved'

y = '|'.join(x for x in choices.videos)
channel = unicode(r'^channel/(%s)$' % y)

urlpatterns = [
    url(r'^$', views.UserDetail.as_view(), name='user_page'),    
    url(r'^pictures/(liked|loved)$', views.UserPictureList.as_view(), name='user_pictures'),
    url(r'^songs/(liked|loved)$', views.UserSongList.as_view(), name='user_songs'),
    url(r'^videos/(liked|loved)$', views.UserVideoList.as_view(), name='user_videos'),
    url(channel, views.MovieChannel.as_view(), name='movie_channel'),
    url(r'^channels$', views.UserChannels.as_view(), name='user_channels'),
    url(r'^cartoons$', views.RandomCartoon.as_view(), name='cartoon_channel'),
    url(r'^random$', views.RandomList.as_view(), name='random_list'),
    url(r'^cached$', views.CachedFileList.as_view(), name='cached_list'),
]
