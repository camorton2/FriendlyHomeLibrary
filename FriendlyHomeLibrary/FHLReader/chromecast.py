# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import time, os
import pychromecast

import FHLBuilder.utility as utils
import FHLReader.utility as rutils


def find_chrome_casts():
    """ find all chromecasts and return an enumerated list """
    try:
        chromecasts = pychromecast.get_chromecasts()
    except Exception as ex:
        # in this case I want to see what the exception is
        # but there's no way to handle it, just pass it back for display
        message = unicode('Chromecast fail' % (type(ex).__name__))
        print (message)
        raise rutils.MyException(message)
    
    res = []
    for x in chromecasts:
        item = chromecasts.index(x),x.device.friendly_name
        res.append(item)
        x.disconnect()
        
    print(res)
    return res
       
       
def cast_picture(devs,picture):
    """ send a given picture to a given chromecast device """
    
    try:
        chromecasts = pychromecast.get_chromecasts()
        dev = int(devs)
        cast = chromecasts[dev]
        
        # wait for device to be ready
        cast.wait()
        print(cast.device)
        print(cast.status)
        mc=cast.media_controller
 
        thefile = utils.object_path_web(picture)
        print('HERE PATH: %s' % (thefile))
        mc.play_media(thefile,'imag/jpg')
        #time.sleep(20)
        #mc.play()
                
    except Exception as ex:
        # in this case I want to see what the exception is
        # but there's no way to handle it, just pass it back for display
        message = unicode('ChromeCast exception %s' % (type(ex).__name__))
        print (message)
        raise rutils.MyException(message)


def cast_slides(devs,pictures,me, add_title):
    """ pass a list of pictures to the specificed device """   
    try:
        chromecasts = pychromecast.get_chromecasts()
        dev = int(devs)
        print('slides to %d' % dev)
        cast = chromecasts[dev]
        
        # wait for device to be ready
        cast.wait()
        print(cast.device)
        print(cast.status)
        mc=cast.media_controller
        if add_title:
            # cleanup working directory
            rutils.cleanup_my_private_directory(me)

        for picture in pictures:
            tmp_file = None
            if add_title:
                thefile,tmp_file = rutils.annotate(picture,me)
            else:
                thefile = utils.object_path_web(picture)
            print('HERE PATH: %s' % (thefile))
            mc.play_media(thefile,'imag/jpg')
            time.sleep(20)
            if add_title:
                print('remove %s' % tmp_file)
                os.unlink(tmp_file)
        cast.disconnect()
                
    except Exception as ex:
        # in this case I want to see what the exception is
        # but there's no way to handle it, just pass it back for display
        message = unicode('ChromeCast exception %s' % (type(ex).__name__))
        print (message)
        raise rutils.MyException(message)


def cast_slides_all(pictures,me, add_title):
    """ cast pictures to all chromecast deviced """    
    try:
        chromecasts = pychromecast.get_chromecasts()
        
        mcs = []
        for cc in chromecasts:
            # get list of ready devices
            cc.wait()
            print(cc.device)
            print(cc.status)
            mc = cc.media_controller
            mcs.append(mc)
            
        if add_title:
            # cleanup working directory
            rutils.cleanup_my_private_directory(me)
 
        for picture in pictures:
            tmp_file = None
            if add_title:
                thefile,tmp_file = rutils.annotate(picture,me)
            else:
                thefile = utils.object_path_web(picture)
            print('HERE PATH: %s' % (thefile))
            for mc in mcs:
                mc.play_media(thefile,'imag/jpg', title=picture.title)
            time.sleep(20)
            if add_title:
                print('remove %s' % tmp_file)
                os.unlink(tmp_file)
        for cc in chromecasts:
            cc.disconnect()
                
    except Exception as ex:
        # in this case I want to see what the exception is
        # but there's no way to handle it, just pass it back for display
        message = unicode('ChromeCast exception %s' % (type(ex).__name__))
        print (message)
        raise rutils.MyException(message)


    
    
