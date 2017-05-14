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

PREF_CHOICES = (
    (LOVE, 'love'),
    (LIKE, 'like'),
    (DISLIKE, 'dislike'),
    (INDIFFERENT, 'indifferent')
    )


NAME = 'NM'
NEWEST = 'NN'
OLDEST = 'OO'

ordering = [NAME,NEWEST,OLDEST]

ORDER_CHOICES = (
    (NAME, 'By Name'),
    (NEWEST, 'Newest First'),
    (OLDEST, 'Oldest First'),
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

