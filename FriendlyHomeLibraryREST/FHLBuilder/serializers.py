# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import FHLBuilder.models as mods
from FHLBuilder import choices
from django.utils.timezone import now


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model =mods.Tag
        fields = ('name','slug')


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model =mods.Collection
        fields = ('filePath','drive','title','slug')


class CommonFileSerializer(serializers.ModelSerializer):
    class Meta:
        model =mods.CommonFile
        fields = ('fileKind','fileName','year','title','slug','data_added')


class MovieSerializer(CommonFileSerializer):
    class Meta:
        model =mods.Movie
        fields = ('collection','tags','likes','loves','dislikes')


class GameSerializer(CommonFileSerializer):
    class Meta:
        model =mods.Game
        fields = ('collection','tags','likes','loves','dislikes')


class BookSerializer(CommonFileSerializer):
    class Meta:
        model =mods.Book
        fields = ('collection','tags','likes','loves','dislikes')


class Picture(CommonFileSerializer):
    class Meta:
        model =mods.Picture
        fields = ('collection','tags','likes','loves','diskikes'
            'data1','data2','data3','data4','data5')


class SongSerializer(CommonFileSerializer):
    class Meta:
        model =mods.Song
        fields = ('collection','track','tags','likes','loves','dislikes')


class ChapterSerializer(CommonFileSerializer):
    class Meta:
        model =mods.Chapter
        fields = ('collection')

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model =mods.Artist
        fields = ('fullName','slug')


class ActorSerializer(ArtistSerializer):
    class Meta:
        model =mods.Actor
        fields = ('movies')


class DirectorSerializer(ArtistSerializer):
    class Meta:
        model =mods.Director
        fields = ('movies')


class MusicianSerializer(ArtistSerializer):
    class Meta:
        model =mods.Musician
        fields = ('albums','concerts','songs')

