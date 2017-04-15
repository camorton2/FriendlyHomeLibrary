# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import string
from FriendlyHomeLibrary import settings

#Utility functions
def to_str(unicode_or_string):
    if isinstance(unicode_or_string,unicode):
        value = unicode_or_string.encode('utf-8')
    else:
        value = unicode_or_string
    return value

def slugCompare(s1,s2):
    remove = to_str('-_')
    c1 = to_str(s1).translate(None,remove)
    c2 = to_str(s2).translate(None,remove)
    return c1==c2

def get_drive(driveNo):
    return to_str(settings.DRIVES[driveNo-1])

# return the constructed path of an object (CommonFile)
# this is from the symbolic link in static for web links
# used when path is needed inside html
def object_path(obj):
    drive=to_str('drive') + str(obj.collection.drive)
    thePath = os.path.join("links/", drive)
    thePath = os.path.join(thePath, obj.collection.filePath,obj.fileName) 
    return to_str(thePath)

#used when path is needed outside html
def object_path_with_static(obj):
    drive=to_str('drive') + str(obj.collection.drive)
    thePath = os.path.join("static/links/", drive)
    thePath = os.path.join(thePath, obj.collection.filePath,obj.fileName) 
    return to_str(thePath)

# Given a list of songs, create a list containing pairs of path,song
# which can be passed to playlist
def songList(songs):
    finalList = []
    if songs is not None:
        for song in songs:
            item = (song, object_path(song))
            finalList.append(item)
    return finalList
    
