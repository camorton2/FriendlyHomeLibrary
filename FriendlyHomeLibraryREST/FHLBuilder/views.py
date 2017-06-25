# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import FHLBuilder.models as db
import FHLBuilder.serializers as ss
from FHLBuilder import choices

# Create your views here.

@api_view(['GET','DELETE','PUT'])
def get_delete_update_song(request,slug,format=None):
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
        target.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # update details of a single song
    elif request.method == 'PUT':
        serializer = ss.SongSerializer(target,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def get_post_songs(request,format=None):
    # all songs
    if request.method == 'GET':
        songs = db.Song.objects.all()
        serializer = ss.SongSerializer(songs,many=True)
        return Response(serializer.data)

    # insert a new record for a song
    elif request.method == 'POST':
        data = {
            # this must be song, so either check it here
            # or on imput
            'fileKind': choices.SONG,
            'fileName': request.data.get('fileName'),
            'year': request.data.get('year'),
            'title': request.data.get('title'),
            'slug': request.data.get('slug'),
            # default should be in model for date_added
            #'date_added' = now
            # still need to figure out how to do collection
            #'collection' = request.data.get('collection') 
            'track': request.data.get('track') 
        
           
        }    
        serializer = ss.SongSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
