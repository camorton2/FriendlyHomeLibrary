# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from FHLBuilder import models, choices, utility
from FriendlyHomeLibrary import settings

# Create your models here.

class CommonFileForm(forms.ModelForm):
    class Meta:
        model=models.CommonFile
        fields='__all__'


class SongForm(CommonFileForm):
    class Meta:
        model=models.Song
        fields=['title','year','fileKind']


class MovieForm(CommonFileForm):
    class Meta:
        model=models.Movie
        fields=['title','year','fileKind']


class TagForm(forms.ModelForm):
    class Meta:
        model=models.Tag
        fields=['name']
        
    def clean_name(self):
        return self.cleaned_data['name'].lower()
        
    def clean_slug(self):
        new_slug=(self.cleaned_data['slug'].lower())
        if(new_slug=='create'):
            raise ValidationError('Slug may not be "create".')
        return new_slug


class BasicCollectionForm(forms.ModelForm):
    class Meta:
        model=models.Collection
        fields=[]
    # Used to select fileKind to apply to everything in the collection
    kind = forms.MultipleChoiceField(choices = choices.KIND_CHOICES,initial=choices.UNKNOWN)
    # Used to add a tag to everything in the collection
    tag = forms.CharField(max_length=models.CHAR_LENGTH,required=False)


class CollectionForm(forms.ModelForm):
    class Meta:
        model=models.Collection
        fields=['filePath']

    # Used to select fileKind to apply to everything in the collection
    kind = forms.MultipleChoiceField(choices = choices.KIND_CHOICES,initial=choices.UNKNOWN)
    # Used to add a tag to everything in the collection
    tag = forms.CharField(max_length=models.CHAR_LENGTH,required=False)
    drive = -1
    
    def clean_filePath(self):
        new_path=self.cleaned_data['filePath']
        for i,drive in enumerate(settings.DRIVES,1):
            toCheck = os.path.join(settings.MY_MEDIA_FILES_ROOT,drive,new_path)
            print("checking drive %d name %s path %s" % (i,drive,new_path))
            print(toCheck)
            if os.path.exists(toCheck):
                self.drive=i
        if self.drive > 0:
            last = new_path.rpartition('/')[2]
            if len(last):
                return utility.to_str(new_path)
            # remove final /
            return to_str(new_path[:-1])
        raise ValidationError('Path does not exist '+new_path)

