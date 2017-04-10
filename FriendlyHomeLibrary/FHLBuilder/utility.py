# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import string


#Utility functions
def to_str(unicode_or_string):
    if isinstance(unicode_or_string,unicode):
        value = unicode_or_string.encode('utf-8')
    #    print("Value %s " % (value))
    else:
        value = unicode_or_string
    return value

def slugCompare(s1,s2):
    remove = to_str('-_')
    c1 = to_str(s1).translate(None,remove)
    c2 = to_str(s2).translate(None,remove)
    #print("comparing %s with %s" % (c1,c2))
    return c1==c2

# return the constructed path of an object (CommonFile)
def objectPath(obj):
    return "mediafiles/" + obj.collection.filePath + '/' + obj.fileName

# Given a list of songs, create a list containing pairs of path,song
# which can be passed to playlist
def songList(songs):
    finalList = []
    if songs is not None:
        for song in songs:
            item = (song, objectPath(song))
            finalList.append(item)
    return finalList
    
