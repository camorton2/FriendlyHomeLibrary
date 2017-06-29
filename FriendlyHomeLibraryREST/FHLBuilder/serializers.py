# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import FHLBuilder.models as mods
from FHLBuilder import choices
from django.utils.timezone import now

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = mods.User
        fields = '__all__'
        lookup_field = 'name'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = mods.Tag
        fields = '__all__'
        lookup_field = 'slug'


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = mods.Collection
        fields = '__all__'
        lookup_field = 'slug'


class CommonFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = mods.CommonFile
        exclude = ('date_added',)
        lookup_field = 'slug'

class MovieSerializer(CommonFileSerializer):
    class Meta:
        model = mods.Movie
        exclude = ('date_added',)
        lookup_field = 'slug'


class PictureSerializer(CommonFileSerializer):
    class Meta:
        model = mods.Picture
        exclude = ('date_added',)
        lookup_field = 'slug'


class SongSerializer(CommonFileSerializer):
    class Meta:
        model = mods.Song
        exclude = ('date_added',)
        lookup_field = 'slug'
        

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = mods.Artist
        fields = '__all__'
        lookup_field = 'slug'


class ActorSerializer(ArtistSerializer):
    class Meta:
        model = mods.Actor
        fields = '__all__'
        lookup_field = 'slug'


class DirectorSerializer(ArtistSerializer):
    class Meta:
        model = mods.Director
        fields = '__all__'
        lookup_field = 'slug'


class MusicianSerializer(ArtistSerializer):
    class Meta:
        model = mods.Musician
        fields = '__all__'
        lookup_field = 'slug'

