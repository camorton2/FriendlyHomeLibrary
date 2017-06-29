# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import FHLBuilder.models as mods


from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = mods.Tag
        fields = ('name',)
        lookup_field = 'slug'


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = mods.Collection
        fields = ('title',)
        lookup_field = 'slug'


class CommonFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = mods.CommonFile
        fields = ('title','year')
        lookup_field = 'slug'


class SongSerializer(CommonFileSerializer):
    class Meta:
        model = mods.Song
        exclude = ('title','year','tags','likes','loves','dislikes')
        lookup_field = 'slug'
        


