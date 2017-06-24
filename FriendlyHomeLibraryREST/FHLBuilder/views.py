# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import FHLBuilder.models as db
import FHLBuilder.serializers as ss

# Create your views here.

@api_view(['GET','DELETE','PUT'])
def get_delete_update_song(request,slug):
    try:
        target = db.Song.objects.get(slug=slug)
    except db.Song.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    # get details of a single song
    if request.method == 'GET':
        serializer=ss.SongSerializer(target)
        return Response(serializer.data)
        
    # delete details of a single song
    elif request.method == 'DELETE':
        return Response({})
    
    # update details of a single song
    elif request.method == 'PUT':
        return Response({})

@api_view(['GET','POST'])
def get_post_songs(request):
    # all songs
    if request.method == 'GET':
        songs = db.Song.objects.all()
        serializer = ss.SongSerializer(songs,many=True)
        return Response(serializer.data)

    # insert a new record for a song
    elif request.method == 'POST':
        data = {
           'title': request.data.get('title'),
           'slug': request.data.get('slug'),
           'fileName': request.data.get('fileName'),
           #'collection': album
        }    
        serializer = ss.SongSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
