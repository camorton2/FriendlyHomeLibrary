# -*- coding: utf-8 -*-
from __future__ import unicode_literals

MOVIE = 'MV'
MOVIE_3D = 'M3'
MINI_MOVIE = 'MM'
CONCERT = 'CC'
DOCUMENTARY = 'DD'
GAME = 'GG'
TV = 'TV'
MINISERIES = 'MS'
AUDIO_BOOK = 'AB'
EBOOK = 'EB'
SONG = 'SG'
PICTURE = 'PT'
UNKNOWN = 'UN'
TV_CARTOON = 'TC'
MV_CARTOON = 'MC'
TV_SITCOM = 'TS'
BF_RANDOM = 'BR'
STANDUP = 'ST'

KIND_CHOICES = (
    (SONG, 'song'),
    (PICTURE, 'picture'),    
    (MOVIE, 'Movie'),
    (MOVIE_3D, '3D Movie'),
    (MV_CARTOON, 'Movie-Cartoon'),
    (MINI_MOVIE, 'Mini-movie'),
    (CONCERT, 'Concert'),
    (DOCUMENTARY,'Documentary'),
    (TV, 'TV-show'),
    (TV_CARTOON, 'TV-Cartoon'),
    (TV_SITCOM, 'TV-Sitcom'),
    (MINISERIES, 'Mini-series'),
    (STANDUP, 'Standup-comedy'),
    (BF_RANDOM, 'BF-random'),
    (AUDIO_BOOK, 'audio-book'),
    (EBOOK, 'e-book'),
    (GAME, 'Game'),
    (UNKNOWN, 'unknown')
)

# all choices that are video files

live = [SONG,PICTURE,MOVIE,MOVIE_3D,MINI_MOVIE,CONCERT,DOCUMENTARY,TV,MINISERIES,
    TV_CARTOON,TV_SITCOM,MV_CARTOON,STANDUP]
videos = live[2:]


VIDEO_CHOICES = KIND_CHOICES[2:13]
VIDEO_CHOICES_FORM = KIND_CHOICES[2:14]
LIVE_CHOICES = KIND_CHOICES[0:13]


#radio listeners

ME = 'm'
ALL = 'a'

RADIO_CHOICES = (
    (ME, 'just me'),
    (ALL, 'everyone'))

LIKE = 'lk'
LOVE = 'lv'
DISLIKE = 'dl'
INDIFFERENT = 'in'

# preference choices

PREF_CHOICES = (
    (LOVE, 'love'),
    (LIKE, 'like'),
    (DISLIKE, 'dislike'),
    (INDIFFERENT, 'indifferent')
    )

# order choices

NAME = 'NM'
NEWEST = 'NN'
OLDEST = 'OO'

ordering = [NAME,NEWEST,OLDEST]

ORDER_CHOICES = (
    (NAME, 'By Name'),
    (NEWEST, 'Newest First'),
    (OLDEST, 'Oldest First'),
    )

# song playlist choices

WEB = 'PP'
FLIST = 'FF'
KODI_LOCAL = 'KL'
KODI_BF = 'BF'
KODI_LF = 'LF'

songplay = [WEB,FLIST,KODI_LOCAL,KODI_BF,KODI_LF]

SONGPLAY_CHOICES = (
    (FLIST, 'No playback, just list files'),
    (WEB, 'html playlist'),
    (KODI_LOCAL, 'Kodi local'),
    (KODI_BF, 'Kodi BF'),
    (KODI_LF, 'Kodi LF'),
    )

# month for dialogue box

SKIP = '0'
JANUARY = '1'
FEBRUARY = '2'
MARCH = '3'
APRIL = '4'
MAY = '5'
JUNE = '6'
JULY = '7'
AUGUST = '8'
SEPTEMBER = '9'
OCTOBER = '10'
NOVEMBER = '11'
DECEMBER = '12'

MONTH_CHOICES = (
   (SKIP,'no month'),
   (JANUARY,'January'),
   (FEBRUARY,'February'),
   (MARCH,'March'),
   (APRIL,'April'),
   (MAY,'May'),
   (JUNE,'June'),
   (JULY,'July'),
   (AUGUST,'August'),
   (SEPTEMBER,'September'),
   (OCTOBER,'October'),
   (NOVEMBER,'November'),
   (DECEMBER,'December'),
)

# extensions considered pictures
picts = [
    '.jpg',
    '.img',
    '.png',
    '.tiff',
    '.tif',
    '.pe4',
    '.gif',
    '.thm'
    ]

# extensions considered movies
movs = [
    '.mkv',
    '.mov',
    '.mp4',
    '.avi',
    '.flv',
    '.wmv',
    '.mpg',
    '.wav'
    ]



