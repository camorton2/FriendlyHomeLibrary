# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from FHLBuilder.models import Tag, Song, CommonFile, Collection, Movie
from FHLBuilder.models import Director,Actor,Musician, Artist
from FHLBuilder.models import Game, Book, Picture, Chapter

class MovieAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags','likes','dislikes','loves')

class GameAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags','likes','dislikes','loves')

class BookAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags','likes','dislikes','loves')

class PictureAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags','likes','dislikes','loves')

class SongAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags','likes','dislikes','loves')

class ActorAdmin(admin.ModelAdmin):
    filter_horizontal = ('movies',)

class DirectorAdmin(admin.ModelAdmin):
    filter_horizontal = ('movies',)

class MusicianAdmin(admin.ModelAdmin):
    filter_horizontal = ('albums','concerts','songs')


# Register your models here.
admin.site.register(Tag)
admin.site.register(Collection)
admin.site.register(CommonFile)
admin.site.register(Movie,MovieAdmin)
admin.site.register(Game,GameAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(Picture,PictureAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Chapter)
admin.site.register(Artist)
admin.site.register(Actor,ActorAdmin)
admin.site.register(Director,DirectorAdmin)
admin.site.register(Musician,MusicianAdmin)
