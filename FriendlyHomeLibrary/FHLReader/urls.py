# urls
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from FHLReader import views
from FHLBuilder import choices

liked = 'liked'
loved = 'loved'

v = '|'.join(x for x in choices.videos)
vchannel = unicode(r'^channel/(%s)$' % v)

special = ['sitcom','saturday-morning','silly',
    'scifi','drama','scary']
st = '|'.join(x for x in special)
schannel = unicode(r'^channel/(%s)$' % st)


urlpatterns = [
    url(r'^$', views.UserDetail.as_view(), name='user_page'),    
    url(r'^pictures/(liked|loved)$', views.UserPictureList.as_view(), name='user_pictures'),
    url(r'^songs/(liked|loved)$', views.UserSongList.as_view(), name='user_songs'),
    url(r'^videos/(liked|loved)$', views.UserVideoList.as_view(), name='user_videos'),
    url(vchannel, views.MovieChannel.as_view(), name='movie_channel'),    
    url(schannel, views.SpecialChannel.as_view(), name='special_channel'),
    url(r'^radio$', views.RadioChannel.as_view(), name='radio_channel'),
    url(r'^random$', views.RandomList.as_view(), name='random_list'),
    url(r'^cached$', views.CachedFileList.as_view(), name='cached_list'),
]
