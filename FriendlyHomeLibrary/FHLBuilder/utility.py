# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import string
from FriendlyHomeLibrary import settings

#Utility functions
def to_str(unicode_or_string):
    try:
        if isinstance(unicode_or_string,unicode):
            value = unicode_or_string.encode('utf-8')
        else:
            value = unicode_or_string
        return value
    except UnicodeDecodeError:
        print("RATS UnicodeDecodeError in to_str with %s" % unicode_or_string)
        print(type(unicode_or_string))
        return 'x'
        

def slugCompare(s1,s2):
    remove = to_str('-_')
    c1 = to_str(s1).translate(None,remove)
    c2 = to_str(s2).translate(None,remove)
    return c1==c2

def get_drive(driveNo):
    return unicode(settings.DRIVES[driveNo-1])

def get_drive_samba(driveNo):
    return unicode(settings.SDRIVES[driveNo-1])

def get_drive_slink(driveNo):
    return unicode(settings.LDRIVES[driveNo-1])


# return the constructed path of an object (CommonFile)
# this is from the symbolic link in static for web links
# used when path is needed inside html
def object_path(obj):
    #drive=unicode('drive') + unicode(obj.collection.drive)
    drive = get_drive_slink(obj.collection.drive)
    thePath = unicode(os.path.join(u'links/', drive))
    thePath = unicode(os.path.join(thePath, obj.collection.filePath,obj.fileName))
    return unicode(thePath)

def object_path_local(obj):
    #drive=unicode('drive') + unicode(obj.collection.drive)
    thePath = get_drive(obj.collection.drive)
    #thePath = unicode(os.path.join(u'links/', drive))
    thePath = unicode(os.path.join(thePath, obj.collection.filePath,obj.fileName))
    return unicode(thePath)

def object_path_samba(obj):
    #drive=unicode('drive') + unicode(obj.collection.drive)
    thePath = get_drive_samba(obj.collection.drive)
    #thePath = unicode(os.path.join(u'links/', drive))
    thePath = unicode(os.path.join(thePath, obj.collection.filePath,obj.fileName))
    return unicode(thePath)


#used when path is needed outside html
def object_path_with_static(obj):
    drive=unicode(u'drive') + unicode(obj.collection.drive)
    thePath = os.path.join(u'static/links/', drive)
    thePath = os.path.join(thePath, obj.collection.filePath,obj.fileName)
    return unicode(thePath)

# Given a list of objects, create a list containing pairs of path,object
# which can be passed to a playlist (song) or a picture list
def link_file_list(things):
    finalList = []
    if things is not None:
        for one in things:
            item = (one, object_path(one))
            finalList.append(item)
    return finalList

def collection_sets(collections):
    songc = []
    moviec = []
    picturec = []
    variousc = []
    if collections is not None:
        for current in collections:
            sc = current.song_set.count()
            mc = current.movie_set.count()
            pc = current.picture_set.count()
            if sc and not mc and not pc:
                # only songs
                songc.append(current)
            elif mc and not sc and not pc:
                # only movies
                moviec.append(current)
            elif pc and not sc and not mc:
                # only pictures
                picturec.append(current)
            else:
                # various
                if sc > pc:
                    # some albums have a few pictures/movies
                    songc.append(current)
                elif pc > mc:
                    # picture directories may contain mini-movies
                    picturec.append(current)
                else:
                    variousc.append(current)
    return songc,moviec,picturec,variousc


