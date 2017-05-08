# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from FHLBuilder import models, choices, utility
from FriendlyHomeLibrary import settings


class RandomForm(forms.ModelForm):
    """
    The idea is to allow the user to create a list of count
    random objects matching a kind and/or tag
    For songs, a playlist can be created in html
    but the ultimate goal is to create a playlist for kodi
    """
    class Meta:
        model=models.Collection
        fields=[]
     
    kind = forms.ChoiceField(choices = choices.LIVE_CHOICES,
        widget=forms.RadioSelect, label = 'Pick a kind',
        initial=choices.MOVIE)
    tag = forms.CharField(max_length=models.CHAR_LENGTH,required=False)
    count = forms.IntegerField(initial=15, label='How many would you like')

    def clean_count(self):
        count=self.cleaned_data['count']
        if count > 0:
            return count
        raise ValidationError(u'please select a count above 0')


class RecentForm(forms.ModelForm):
    """
    The idea is to allow the user to create a list of count
    most recent objects matching a kind and/or tag
    For songs, a playlist can be created in html
    but the ultimate goal is to create a playlist for kodi
    """
    class Meta:
        model=models.Collection
        fields=[]
     
    kind = forms.ChoiceField(choices = choices.LIVE_CHOICES,
        widget=forms.RadioSelect, label = 'Pick a kind',
        initial=choices.MOVIE)
        
    count = forms.IntegerField(initial=15, label='How many would you like')

    def clean_count(self):
        count=self.cleaned_data['count']
        if count > 0:
            return count
        raise ValidationError(u'please select a count above 0')


class CountForm(forms.ModelForm):
    """
    Used for specialty channels to get only a count, the rest is
    selected automatically
    """
    class Meta:
        model=models.Collection
        fields=[]
     
    count = forms.IntegerField(initial=15, label='How many would you like')

    def clean_count(self):
        count=self.cleaned_data['count']
        if count > 0:
            return count
        raise ValidationError(u'please select a count above 0')


class RadioForm(forms.ModelForm):
    """
    Used for radio stations which pick random songs based on 
    selected users
    """
    class Meta:
        model=models.Collection
        fields=[]
     
    count = forms.IntegerField(initial=40, label='How many would you like')
    kind = forms.ChoiceField(choices = choices.RADIO_CHOICES,
        widget=forms.RadioSelect,
        initial=choices.ALL,label = 'who is listening')
    xmas = forms.BooleanField(label = 'include Christmas', 
        initial=False,required=False)
    def clean_count(self):
        count=self.cleaned_data['count']
        if count > 0:
            return count
        raise ValidationError(u'please select a count above 0')


class MovieChannelForm(forms.ModelForm):
    """
    The idea is to allow the user to create a playlist of count
    random items, optionally matching by tag or title
    """
    class Meta:
        model=models.Collection
        fields=[]
     
    atitle = forms.CharField(max_length=models.CHAR_LENGTH,
        required=False,
        label='title contains')
    atag = forms.CharField(max_length=models.CHAR_LENGTH,required=False,
        label='with tag')
    count = forms.IntegerField(initial=15)

    def clean_count(self):
        count=self.cleaned_data['count']
        if count > 0:
            return count
        raise ValidationError(u'please select a count above 0')


