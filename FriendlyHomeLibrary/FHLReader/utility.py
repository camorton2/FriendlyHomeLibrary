# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import os

import FHLBuilder.utility as utils
from FriendlyHomeLibrary import settings

### Utilities

class MyException(Exception):
    """ simple exception takes message """
    def __init__(self, msg):
        Exception.__init__(self)
        print('CTOR MyException %s' % msg)
        self.message = msg


def my_private_directory(me):
    """ create my private working directory """
    try:
        if me is None:
            my_dir = (u'FHL/slides-%s' % 'anon')
        else:
            my_dir = (u'FHL/slides-%s' % me.username)
        my_path = os.path.join(settings.DRIVES[1], my_dir)
        
        drive = utils.get_drive_slink(2)
        web_path = os.path.join(u'links/', drive)
        web_path = os.path.join(settings.HTTP_PREFIX,web_path)
        web_path = os.path.join(web_path, my_dir)

        smb_path = utils.get_drive_samba(2)
        smb_path = os.path.join(smb_path, my_dir)
    
        if os.path.exists(my_path):
            print('exists')
        else:
            print('not there')
            os.mkdir(my_path)
        
        return my_path,web_path,smb_path
    except Exception as ex:
        # would eventually like to catch the correct message
        message = unicode('Error creating my working directory %s' % (type(ex).__name__))
        print (message)
        raise MyException(message)


#def cleanup_my_private_directory(me):
#    pass


def annotate(picture,me):
    """ decorate a picture with its friendly_name """
    filename = picture.fileName
    me_local, me_web, _ = my_private_directory(me)
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
    
    
