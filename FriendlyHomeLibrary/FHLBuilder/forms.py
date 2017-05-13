# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from FHLBuilder import models, choices, utility
from FriendlyHomeLibrary import settings


class CommonFileForm(forms.ModelForm):
    class Meta:
        model=models.CommonFile
        fields='__all__'
    pref = forms.ChoiceField(choices = choices.PREF_CHOICES,
        widget=forms.RadioSelect,
        initial=choices.INDIFFERENT)
    tag = forms.CharField(max_length=models.CHAR_LENGTH,
        required=False,
        label='add tag')

class SongForm(CommonFileForm):
    class Meta:
        model=models.Song
        fields=['title','year']
    musician = forms.CharField(max_length=models.CHAR_LENGTH,
        required=False,
        label='add musician')

class PictureForm(CommonFileForm):
    class Meta:
        model=models.Picture
        fields=['title','year']


class MovieForm(CommonFileForm):
    class Meta:
        model=models.Movie
        fields=['title','year','fileKind']
    actor = forms.CharField(max_length=models.CHAR_LENGTH,
        required=False,
        label='add actor')
    director = forms.CharField(max_length=models.CHAR_LENGTH,
        required=False,
        label='add director')        
    musician = forms.CharField(max_length=models.CHAR_LENGTH,
        required=False,
        label='add musician')

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


class AllFilesForm(forms.ModelForm):
    class Meta:
        model=models.CommonFile
        fields=[]
    
    kind = forms.ChoiceField(choices = choices.LIVE_CHOICES,
        widget=forms.RadioSelect, label = 'Pick a kind',
        initial=choices.SONG)    

    order = forms.ChoiceField(choices = choices.ORDER_CHOICES,
        widget=forms.RadioSelect, label = 'Pick an Order',
        initial=choices.NAME)    

    def clean_count(self):
        count=self.cleaned_data['count']
        if count > 0:
            return count
        raise ValidationError(u'please select a count above 0')
    


class BasicCollectionForm(forms.ModelForm):
    class Meta:
        model=models.Collection
        fields=[]
    
    kind = forms.ChoiceField(choices = choices.VIDEO_CHOICES_FORM,
        widget=forms.RadioSelect, label = 'kind for videos',
        initial=choices.MOVIE)    
    
    # Used to add a tag to everything in the collection
    tag = forms.CharField(max_length=models.CHAR_LENGTH,required=False)


class CollectionForm(forms.ModelForm):
    class Meta:
        model=models.Collection
        fields=['filePath']

    kind = forms.ChoiceField(choices = choices.VIDEO_CHOICES_FORM,
        widget=forms.RadioSelect, label = 'kind for videos',
        initial=choices.MOVIE)    
    
    # Used to add a tag to everything in the collection
    tag = forms.CharField(max_length=models.CHAR_LENGTH,required=False)
    drive = -1
    
    def clean_filePath(self):
        self.drive = -1
        new_path=self.cleaned_data['filePath']
        for i,drive in enumerate(settings.DRIVES,1):
            toCheck = os.path.join(settings.MY_MEDIA_FILES_ROOT,drive,new_path)
            utility.log("checking drive %d name %s path %s" % (i,drive,new_path))
            utility.log(toCheck)
            if os.path.exists(toCheck):
                self.drive=i
                utility.log("OK selecting drive %d" % i)
                break
        if self.drive > 0:
            last = new_path.rpartition('/')[2]
            if len(last):
                return utility.to_str(new_path)
            # remove final /
            return to_str(new_path[:-1])
        utility.log("DOES NOT EXIST")
        raise ValidationError(u'Path does not exist '+new_path,code=u'invalid')

