# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Tag, FHLUser, Common, Chapter, Actor, Director
from .models import Musician, Band, AudioBook, Song, Album, Movie

# Create your models here.


class TagForm(ModelForm):
    class Meta:
        model=Tag
        fields='__all__'
    def clean_name(self):
        return self.cleaned_data['name'].lower()
    def clean_slug(self):
        new_slug=(self.cleaned_data['slug'].lower())
        if(new_slug=='create'):
            raise ValidationError('Slug may not be "create".')
        return new_slug

class FHLUserForm(ModelForm):
    class Meta:
        model=FHLUser
        fields='__all__'


class CommonForm(ModelForm):
    class Meta:
        model=Tag
        fields='__all__'


# Audio book chapter
class ChapterForm(CommonForm):
    class Meta:
        model=Tag
        fields='__all__'

class ActorForm(ModelForm):
    class Meta:
        model=Tag
        fields='__all__'

class DirectorForm(ModelForm):
    class Meta:
        model=Tag
        fields='__all__'

class MusicianForm(ModelForm):
    class Meta:
        model=Tag
        fields='__all__'

class BandForm(ModelForm):
    class Meta:
        model=Tag
        fields='__all__'

class AudioBookForm(CommonForm):
    class Meta:
        model=AudioBook
        fields='__all__'

class SongForm(CommonForm):
    class Meta:
        model=Song
        fields='__all__'

class AlbumForm(CommonForm):
    class Meta:
        model=Album
        fields='__all__'

class MovieForm(CommonForm):
    class Meta:
        model=Movie
        fields='__all__'

