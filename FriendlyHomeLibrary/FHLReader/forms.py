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


class RandomForm(forms.ModelForm):
    """
    The idea is to allow the user to create a playlist of count
    random objects matching a kind and/or tag
    For songs, a playlist can be created in html
    but the ultimate goal is to create a playlist for kodi
    """
    class Meta:
        model=models.Collection
        fields=[]
     
    kind = forms.MultipleChoiceField(choices = choices.KIND_CHOICES,initial=choices.UNKNOWN)
    tag = forms.CharField(max_length=models.CHAR_LENGTH,required=False)
    count = forms.IntegerField(initial=1)

    def clean_count(self):
        count=self.cleaned_data['count']
        if count > 0:
            return count
        raise ValidationError(u'please select a count above 0')


