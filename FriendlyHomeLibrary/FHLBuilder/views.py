# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from FHLBuilder.models import Tag, Song

# Create your views here.

def poke(request):
    #t1 = Tag(name="testTag1", slug="test_tag1")
    t1 = Tag.objects.get(slug_contains='test_tag1')
    #t2 = Tag(name="testTag2", slug="test_tag2")
    t1 = Tag.objects.get(slug_contains='test_tag1')
    #t3 = Tag(name="testTag3", slug="test_tag3")
    t1 = Tag.objects.get(slug_contains='test_tag1')
    song1 = Song(artist="Billy Bo", 
                 track=1, 
                 title="Some Silly Song",
                 filename="SSS",
                 filepath="path/to/Songs",
                 slug="sss_page",
                 )
    song1.tags.add(t1)
    song1.tags.add(t2)
    song2 = Song(artist="Janey Bo", 
                 track=1, 
                 title="Another Silly Song",
                 filename="ASS",
                 filepath="path/to/Songs",
                 slug="ass_page",
                 )
    song2.tags.add(t2)
    song2.tags.add(t3)
    song1.save()
    song2.save()             
    tag_list = Tag.objects.all()
    output = "Welcome to Friendly Home Library  tags: "
    for tag in tag_list:
        output=output+ " " + tag.name
    return HttpResponse(output)
    
    
