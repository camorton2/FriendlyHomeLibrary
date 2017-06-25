# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import FHLBuilder.models as mods
from FHLBuilder import choices
from django.utils.timezone import now


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model =mods.Tag
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model =mods.Collection
        fields = '__all__'


class CommonFileSerializer(serializers.ModelSerializer):
    class Meta:
        model =mods.CommonFile
        exclude = ('date_added',)

class MovieSerializer(CommonFileSerializer):
    class Meta:
        model =mods.Movie
        exclude = ('date_added',)


class PictureSerializer(CommonFileSerializer):
    class Meta:
        model =mods.Picture
        exclude = ('date_added',)


class SongSerializer(CommonFileSerializer):
    class Meta:
        model =mods.Song
        exclude = ('date_added',)
        

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model =mods.Artist
        fields = '__all__'


class ActorSerializer(ArtistSerializer):
    class Meta:
        model =mods.Actor
        fields = '__all__'


class DirectorSerializer(ArtistSerializer):
    class Meta:
        model =mods.Director
        fields = '__all__'


class MusicianSerializer(ArtistSerializer):
    class Meta:
        model =mods.Musician
        fields = '__all__'

