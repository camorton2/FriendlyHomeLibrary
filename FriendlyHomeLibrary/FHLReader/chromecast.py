# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import time
import pychromecast
from FHLReader.kodi import MyException
import FHLBuilder.utility as utils
#from FriendlyHomeLibrary import settings

def find_chrome_casts():
    try:
        chromecasts = pychromecast.get_chromecasts()
    except Exception as ex:
        # in this case I want to see what the exception is
        # but there's no way to handle it, just pass it back for display
        message = unicode('Chromecast fail' % (type(ex).__name__))
        print (message)
        raise MyException(message)

    for cc in chromecasts:
        print('cast found %s' % (cc.device.friendly_name))
    
    #cz = ','.join(x.device.friendly_name for x in chromecasts)
    res = []
    for x in chromecasts:
        item = chromecasts.index(x),x.device.friendly_name
        res.append(item)
        
    print(res)
    return res
       
    
def cast_movie(devs,movie):
    try:
        chromecasts = pychromecast.get_chromecasts()
        dev = int(devs)
        cast = chromecasts[dev]
        
        # see notes on problem with is_active
        #pychromecast.IGNORE_CEC.append(cast.device.friendly_name)
        #pychromecast.IGNORE_CEC.append('*')
        # wait for device to be ready
        cast.wait()
        print(cast.device)
        print(cast.status)
        mc=cast.media_controller
        
        
        thefile = utils.object_path_samba(movie)
        #lpath = utils.object_path_with_static(movie)
        #thefile = ('%s%s%s' % (settings.HTTP_URL,settings.STATIC_URL,lpath))
        #thefile = utils.object_path_with_static(movie)
        
        print('before play_media %s' % (thefile))
        mc.play_media(thefile,'video/mp4',autoplay=False)
        print('block until active')
        mc.block_until_active()
        print('ready to play')
        mc.play()
        #print('before status')
        #print(mc.status())
        #print('before pause')
        #mc.pause()
        #print('before sleep')
        #time.sleep(5)
        #print('before play %s' % (thefile))
        #mc.play()
        print('after play')
        print(cast.status)
        #print('movie? %s' % mc.media_is_movie())
    except Exception as ex:
        # in this case I want to see what the exception is
        # but there's no way to handle it, just pass it back for display
        message = unicode('ChromeCast exception %s' % (type(ex).__name__))
        print (message)
        raise MyException(message)
    
    
def cast_picture(devs,picture):
    try:
        chromecasts = pychromecast.get_chromecasts()
        dev = int(devs)
        cast = chromecasts[dev]
        
        # see notes on problem with is_active
        #pychromecast.IGNORE_CEC.append(cast.device.friendly_name)
        #pychromecast.IGNORE_CEC.append('*')
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
        raise MyException(message)



def cast_slides(devs,pictures):
    
    try:
        chromecasts = pychromecast.get_chromecasts()
        dev = int(devs)
        print('slides to %d' % dev)
        cast = chromecasts[dev]
        
        # see notes on problem with is_active
        #pychromecast.IGNORE_CEC.append(cast.device.friendly_name)
        #pychromecast.IGNORE_CEC.append('*')
        # wait for device to be ready
        cast.wait()
        print(cast.device)
        print(cast.status)
        mc=cast.media_controller
 
        for picture in pictures:
            thefile = utils.object_path_web(picture)
            print('HERE PATH: %s' % (thefile))
            mc.play_media(thefile,'imag/jpg', title=picture.title)
            time.sleep(20)
            #cast.disconnect()
            #mc.play()
                
    except Exception as ex:
        # in this case I want to see what the exception is
        # but there's no way to handle it, just pass it back for display
        message = unicode('ChromeCast exception %s' % (type(ex).__name__))
        print (message)
        raise MyException(message)



def cast_slides_all(pictures):
    
    try:
        chromecasts = pychromecast.get_chromecasts()
        
        mcs = []
        for cc in chromecasts:        
            cc.wait()
            print(cc.device)
            print(cc.status)
            mc = cc.media_controller
            mcs.append(mc)
 
        for picture in pictures:
            thefile = utils.object_path_web(picture)
            print('HERE PATH: %s' % (thefile))
            for mc in mcs:
                mc.play_media(thefile,'imag/jpg', title=picture.title)
            time.sleep(20)
            #cast.disconnect()
            #mc.play()
                
    except Exception as ex:
        # in this case I want to see what the exception is
        # but there's no way to handle it, just pass it back for display
        message = unicode('ChromeCast exception %s' % (type(ex).__name__))
        print (message)
        raise MyException(message)

