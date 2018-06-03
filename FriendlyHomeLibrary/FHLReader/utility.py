# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import os

import FHLBuilder.utility as utils
from FriendlyHomeLibrary import settings
from shutil import copyfile

### Utilities

class MyException(Exception):
    """ simple exception takes message """
    def __init__(self, msg):
        Exception.__init__(self)
        print('CTOR MyException %s' % msg)
        self.message = msg

def ip_from_request(request):
    try:
        return request.META['REMOTE_ADDR']
    except KeyError:
        message = unicode('ERROR could not get client ip from request')
        print(message)
        raise MyException(message)


def my_private_directory(me, identifier):
    """ create my private working directory """
    try:
        if me is None:
            my_dir = (u'%s-%s' % (identifier, 'anon'))
        else:
            my_dir = (u'%s-%s' % (identifier, me.username))
        
        
        # my_path is hard-coded in /tmp, kodi does not like samba
        my_path = os.path.join(r'/tmp/', my_dir)
        
        drive = utils.get_drive_slink(2)
        web_path = os.path.join(u'links/', drive)
        web_path = os.path.join(settings.HTTP_PREFIX,web_path)
        web_path = os.path.join(web_path, my_dir)

        #no longer used, kodi does not like samba path
        #smb_path = utils.get_drive_samba(2)
        #smb_path = os.path.join(smb_path, my_dir)
        print('my_path %s' % (my_path))  
        if os.path.exists(my_path):
            print('exists')
        else:
            print('not there')
            os.mkdir(my_path)
        
        return my_path,web_path
    except Exception as ex:
        # would eventually like to catch the correct message
        message = unicode('Error creating my working directory %s' % (type(ex).__name__))
        print (message)
        raise MyException(message)


def cleanup_my_private_directory(me,identifier):
    my_path, _ = my_private_directory(me, identifier)
    print('cleanup my_path %s' % (my_path))  
    if os.path.exists(my_path):
        print('cleanup exists')
        for target in os.listdir(my_path):
            tpath = os.path.join(my_path,target)
            print('to delete %s' % (tpath))
            os.remove(tpath)
    

def annotate(picture,me):
    """ decorate a picture with its friendly_name """
    #print('start annotate')
    filename = picture.fileName
    me_local, me_web = my_private_directory(me,'slides')
    tmp_file = os.path.join(me_local,filename)
    web_file = os.path.join(me_web,filename)
    pic_path = utils.object_path_local(picture)
    #print('source %s destination %s' % (pic_path,tmp_file))
    #shutil.copyfile(pic_path,tmp_file)
    
    ccmd = '/usr/bin/convert '
    opts0 = ' -scale 1280x1080 '
    opts = ' -pointsize 30 -fill black -undercolor white -annotate +0+22 '
    acmd = ccmd + pic_path + opts0 + opts + picture.friendly_name() + ' ' + tmp_file
    # print('acmd %s' % acmd)    
    os.system(acmd)
    return web_file, tmp_file

def transfer_to_my_directory(me,songs):
    cleanup_my_private_directory(me,u'favourites')
    my_path,_ = my_private_directory(me,u'favourites')
        
    for song in songs:
        src_path = utils.object_path_local(song)
        song_path = os.path.basename(song.friendly_name())
        dest_path = os.path.join(my_path,song_path)
        
        print('source %s destination %s' % (src_path,dest_path))
        try:
            
            copy(src_path,dest_path)
        except Exception as ex:
            # would eventually like to catch the correct message
            message = unicode('Error during file copy %s' % (type(ex).__name__))
            print (message)
            raise MyException(message)

    
    return my_path
    
