# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Tag, Common, Song, Collection
from os.path import exists

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

class CommonForm(ModelForm):
    class Meta:
        model=Tag
        fields='__all__'

class SongForm(CommonForm):
    class Meta:
        model=Song
        fields='__all__'

class CollectionForm(CommonForm):
    hardCodeHead = '/home/catherine/Media/'
    class Meta:
        model=Collection
        fields='__all__'
    def clean_filepath(self):
        new_path=self.cleaned_data['filepath']
        if exists(self.hardCodeHead+new_path):
            return new_path
        raise ValidationError('Path does not exist'+self.hardCodeHead+new_path)

