# urls
from django.conf.urls import url

from FHLReader import views

from FHLBuilder.url_utility import vchannel, schannel


urlpatterns = [
    url(r'^$', views.UserDetail.as_view(), name='user_page'),    
    url(r'^pictures/(liked|loved|both|random)$', views.UserPictureList.as_view(), name='user_pictures'),
    url(r'^songs/(liked|loved|both|random)$', views.UserSongList.as_view(), name='user_songs'),
    url(r'^videos/(liked|loved|both|random)$', views.UserVideoList.as_view(), name='user_videos'),
    url(vchannel, views.MovieChannel.as_view(), name='movie_channel'),    
    url(schannel, views.SpecialChannel.as_view(), name='special_channel'),
    url(r'^radio$', views.RadioChannel.as_view(), name='radio_channel'),
    url(r'^radio_mus$', views.MusicianRadioChannel.as_view(), name='mus-radio_channel'),
    url(r'^random$', views.RandomList.as_view(), name='random_list'),
    url(r'^recent$', views.RecentList.as_view(), name='recent_list'),
    url(r'^cached$', views.CachedFileList.as_view(), name='cached_list'),
]
