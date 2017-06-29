# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions

import FHLBuilder.models as db
import FHLBuilder.serializers as ss

# View functions for builder will need to require builder permissions
#   (permission check still to do, pending creation of user in test)
# and the serializers will allow creation, delete, update

# Users
class UserList(generics.ListAPIView):
    #permission_classes = (permissions.IsAdminUser,)
    queryset = db.User.objects.all()
    serializer_class = ss.UserSerializer

class UserDetail(generics.RetrieveAPIView):
    #permission_classes = (permissions.IsAdminUser,)
    queryset = db.User.objects.all()
    serializer_class = ss.UserSerializer

# Generic APIViews Pictures

class BuilderPictureList(generics.ListCreateAPIView):
    queryset = db.Picture.objects.all()
    serializer_class = ss.PictureSerializer

class BuilderPictureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = db.Picture.objects.all()
    serializer_class = ss.PictureSerializer
    lookup_field = 'slug'


# APIViews - Movies
class BuilderMovieDetail(APIView):
    def get_movie(self,slug):
        try:
            return db.Movie.objects.get(slug=slug)
        except db.Movie.DoesNotExist:
            raise Http404
        
    def get(self,request,slug,format=None):
        """ get details of a single movie """
        target = self.get_movie(slug)
        serializer=ss.MovieSerializer(target)
        return Response(serializer.data)
       
    def delete(self,request,slug,format=None):
        """ delete details of a single movie  """
        target=self.get_movie(slug)
        target.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    
    def put(self,request,slug,format=None):
        """ update details of a single movie  """
        target = self.get_movie(slug)
        serializer=ss.MovieSerializer(target,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class BuilderMovieList(APIView):
    def get(self,request,format=None):
        """ list all movies """
        movies = db.Movie.objects.all()
        serializer = ss.MovieSerializer(movies,many=True)
        return Response(serializer.data)

    
    def post(self,request,format=None):
        """ insert a new record for a movie  """
        data = {
           'year': request.data.get('year'),
           'title': request.data.get('title'),
           'slug': request.data.get('slug'),
           'fileName': request.data.get('fileName'),
           #'collection': album
        }    
        serializer = ss.MovieSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



# Manual View Functions

@api_view(['GET','DELETE','PUT'])
def builder_song_detail(request,slug):
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
        serializer=ss.SongSerializer(target,data=request.data)
        if serializer.is_valid():
            serializer.save()
            # default status=status.HTTP_200_OK
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def builder_song_list(request):
    # all songs
    if request.method == 'GET':
        songs = db.Song.objects.all()
        serializer = ss.SongSerializer(songs,many=True)
        return Response(serializer.data)

    # insert a new record for a song
    elif request.method == 'POST':
        data = {
           'year': request.data.get('year'),
           'title': request.data.get('title'),
           'slug': request.data.get('slug'),
           'fileName': request.data.get('fileName'),
           'track': request.data.get('track'),
           #'collection': album
        }    
        serializer = ss.SongSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

