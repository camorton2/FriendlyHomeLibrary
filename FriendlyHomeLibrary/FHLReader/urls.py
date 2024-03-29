# urls
from django.conf.urls import url

from FHLReader import views

from FHLBuilder.url_utility import vchannel, schannel

mYearA = r'(?P<yearA>200[0-9]|201[0-9]|202[0-9]|203[0-9]|204[0-9])'
mYearB = r'(?P<yearB>200[0-9]|201[0-9]|202[0-9]|203[0-9]|204[0-9])'
mMonthA = r'(?P<monthA>[1-9]|1[0-2])'
mMonthB = r'(?P<monthB>[1-9]|1[0-2])'

mYearAB = mYearA + r'/' + mYearB
mYearMonthA = mYearA + r'/' + mMonthA
mYearMonthB = mYearB + r'/' + mMonthB

urlpatterns = [
    url(r'^$', views.UserDetail.as_view(), name='user_page'),    
    url(r'^pictures/(liked|loved|both|random)$', views.UserPictureList.as_view(), name='user_pictures'),
    url(r'^songs/(liked|loved|both|random)$', views.UserSongList.as_view(), name='user_songs'),
    url(r'^videos/(liked|loved|both|random)$', views.UserVideoList.as_view(), name='user_videos'),
    url(vchannel, views.MovieChannel.as_view(), name='movie_channel'),    
    url(schannel, views.SpecialChannel.as_view(), name='special_channel'),
    url(r'^radio$', views.RadioChannel.as_view(), name='radio_channel'),
    url(r'^radio_mus$', views.MusicianRadioChannel.as_view(), name='mus-radio_channel'),
    url(r'^radio_col$', views.CollectionRadioChannel.as_view(), name='col-radio_channel'),
    url(r'^radio_song$', views.SongRadioChannel.as_view(), name='song-radio_channel'),
    url(r'^radio_date$', views.DateRadioChannel.as_view(), name='date_radio_channel'),
    url(r'^picture_date$', views.DatePictureChannel.as_view(), name='date_picture_channel'),
    # since this is year added, limit 2000-2018, no library before that
    
    # radio by date
    # single year
    url(r'^radio/' + mYearA + r'/$',
        views.date_added_radio_channel,
        name='date_added_radio_channel'),
    # single year/month
    url(r'^radio/' + mYearMonthA + r'/$',
        views.date_added_radio_channel,
        name='date_added_radio_channel'),
    # 2 years for a range
    url(r'^radio/range/' + mYearAB + r'/$',
        views.range_added_radio_channel,
        name='range_added_radio_channel'),
    # 2 year/month for a range
    url(r'^radio/' + mYearMonthA + r'/' + mYearMonthB + r'/$',
        views.range_added_radio_channel,
        name='range_added_radio_channel'),
    
    # pictures by date        
    # single year
    url(r'^picture/' + mYearA + r'/$',
        views.date_added_picture_channel,
        name='date_added_picture_channel'),
    # single year/month
    url(r'^picture/' + mYearMonthA + r'/$',
        views.date_added_picture_channel,
        name='date_added_picture_channel'),
    # 2 years for a range
    url(r'^picture/range/' + mYearAB + r'/$',
        views.range_added_picture_channel,
        name='range_added_picture_channel'),
    # 2 year/month for a range
    url(r'^picture/' + mYearMonthA + r'/' + mYearMonthB + r'/$',
        views.range_added_picture_channel,
        name='range_added_picture_channel'),
        
    url(r'^discography$', views.discography_list, name='discography_list'),
    url(r'^transfer_favourites$', views.transfer_favourites, name='transfer_favourites'),
    url(r'^random$', views.RandomList.as_view(), name='random_list'),
    url(r'^recent$', views.RecentList.as_view(), name='recent_list'),
    url(r'^cached$', views.CachedFileList.as_view(), name='cached_list'),
]
