# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.text import slugify

from .models import Tag, CommonFile, Song, Collection, Movie
from .models import Actor, Director, Musician, CHAR_LENGTH
from .collection import add_collection
import os

from FriendlyHomeLibrary import settings
from . import choices

# Create your models here.

class CommonFileForm(ModelForm):
    class Meta:
        model=CommonFile
        fields='__all__'

class TagForm(ModelForm):
    class Meta:
        model=Tag
        fields=['name']
    def clean_name(self):
        return self.cleaned_data['name'].lower()
    def clean_slug(self):
        new_slug=(self.cleaned_data['slug'].lower())
        if(new_slug=='create'):
            raise ValidationError('Slug may not be "create".')
        return new_slug

class ActorForm(ModelForm):
    class Meta:
        model=Actor
        fields='__all__'
    def clean_slug(self):
        new_slug=(self.cleaned_data['slug'].lower())
        if(new_slug=='create'):
            raise ValidationError('Slug may not be "create".')
        return new_slug

class DirectorForm(ModelForm):
    class Meta:
        model=Director
        fields='__all__'
    def clean_slug(self):
        new_slug=(self.cleaned_data['slug'].lower())
        if(new_slug=='create'):
            raise ValidationError('Slug may not be "create".')
        return new_slug

class MusicianForm(ModelForm):
    class Meta:
        model=Musician
        fields='__all__'
    def clean_slug(self):
        new_slug=(self.cleaned_data['slug'].lower())
        if(new_slug=='create'):
            raise ValidationError('Slug may not be "create".')
        return new_slug

class SongForm(CommonFileForm):
    class Meta:
        model=Song
        fields=['title','year','fileKind']

class MovieForm(CommonFileForm):
    class Meta:
        model=Movie
        fields=['title','year','fileKind']

class BasicCollectionForm(ModelForm):
    class Meta:
        model=Collection
        fields=[]
    # Used to select fileKind to apply to everything in the collection
    kind = forms.MultipleChoiceField(choices = choices.KIND_CHOICES,initial=choices.UNKNOWN)
    # Used to add a tag to everything in the collection
    tag = forms.CharField(max_length=CHAR_LENGTH,required=False)


class CollectionForm(ModelForm):
    #hardCodeHead = '/home/catherine/Media/'
    class Meta:
        model=Collection
        fields=['filePath']

    # Used to select fileKind to apply to everything in the collection
    kind = forms.MultipleChoiceField(choices = choices.KIND_CHOICES,initial=choices.UNKNOWN)
    # Used to add a tag to everything in the collection
    tag = forms.CharField(max_length=CHAR_LENGTH,required=False)

    def clean_filePath(self):
        new_path=self.cleaned_data['filePath']
        if os.path.exists(os.path.join(settings.MY_MEDIA_FILES_ROOT,new_path)):
            last = new_path.rpartition('/')[2]
            if len(last):
                return new_path
            # remove final /
            return new_path[:-1]
        raise ValidationError('Path does not exist'+settings.MY_MEDIA_FILES_ROOT+new_path)

