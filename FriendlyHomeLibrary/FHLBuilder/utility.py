# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import string
import datetime

from FriendlyHomeLibrary import settings


#Utility functions

def log(msg):
    try:
        log = unicode('%s/log%s' % (settings.LOG_PATH,datetime.date.today()))
        with open(log,'a+') as f:
            f.write(msg)
            f.write('\n')
            f.close()
    except UnicodeDecodeError:
        print("RATS UnicodeDecodeError in to_str with %s" % msg)
        f.close()
    except UnicodeEncodeError:
        print("RATS UnicodeEncodeError in to_str with %s" % msg)
        f.close()


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


def object_path(obj):
    """ return the path from links in django's static path """
    if obj is None:
        message = unicode('error - request path object None')
        raise Exception(message)        
    if obj.collection is None:
        message = unicode('error - request path object collection none %s type %s' % (obj.title,type(obj)))
        raise Exception(message)
    drive = get_drive_slink(obj.collection.drive)
    thePath = unicode(os.path.join(u'links/', drive))
    thePath = unicode(os.path.join(thePath, obj.collection.filePath,obj.fileName))
    return unicode(thePath)


def object_path_with_static(obj):
    """ return the path from static/links django's static path """
    drive=unicode(u'drive') + unicode(obj.collection.drive)
    thePath = os.path.join(u'static/links/', drive)
    thePath = os.path.join(thePath, obj.collection.filePath,obj.fileName)
    return unicode(thePath)


def object_path_no_static(obj):
    """ return the path from static/links django's static path """
    drive=unicode(u'drive') + unicode(obj.collection.drive)
    thePath = os.path.join(u'links/', drive)
    thePath = os.path.join(thePath, obj.collection.filePath,obj.fileName)
    return unicode(thePath)


def object_path_web(obj):
    """ return the path from static/links django's static path """
    #drive=using path+unicode(u'drive') + unicode(obj.collection.drive)
    drive = get_drive_slink(obj.collection.drive)
    thePath = os.path.join(u'links/', drive)
    thePath = os.path.join(settings.HTTP_PREFIX,thePath)
    thePath = os.path.join(thePath, obj.collection.filePath,obj.fileName)
    return unicode(thePath)



def object_path_local(obj):
    """ real path to object using local samba link """
    thePath = get_drive(obj.collection.drive)
    thePath = unicode(os.path.join(thePath, obj.collection.filePath,obj.fileName))
    return unicode(thePath)


def object_path_samba(obj):
    """ real samba path to object for use on all machines """
    thePath = get_drive_samba(obj.collection.drive)
    thePath = unicode(os.path.join(thePath, obj.collection.filePath,obj.fileName))
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
            sc = current.songs.count()
            mc = current.movies.count()
            pc = current.pictures.count()
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


