# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import FHLBuilder.models as db
import FHLBuilder.serializers as ss
#from FHLBuilder import choices

from rest_framework import generics
from rest_framework import permissions

# Reader Views


class ReaderSongList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    #queryset = db.Song.objects.all()
    # smaller list for testing
    queryset = db.Song.objects.filter(title__icontains='saturday')
    serializer_class = ss.SongSerializer
    
class ReaderSongDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    #queryset = db.Song.objects.all()
    # smaller list for testing
    queryset = db.Song.objects.filter(title__icontains='saturday')
    serializer_class = ss.SongSerializer
    lookup_field = 'slug'
    
