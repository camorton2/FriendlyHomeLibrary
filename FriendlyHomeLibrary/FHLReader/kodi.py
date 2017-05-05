# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time

import FHLBuilder.utility as utils

from FriendlyHomeLibrary import settings

from xbmcjson import XBMC

##
# Note xbmc stuff based on/copied from
# https://github.com/jcsaaddupuy/xbmc-client/blob/master/src/xbmc_client/xbmc_client.py
##

class MyException(Exception):
    def __init__(self, msg):
        """ simple exception takes message """
        print('CTOR MyException %s' % msg)
        self.message = msg

def get_json_rpc(host):
    jsonrpc = "jsonrpc"
    if not host.endswith("/"):
        jsonrpc = "/" + jsonrpc
    return host + jsonrpc

def init_xbmc(ip):
    host = unicode('http://%s' % ip)
    print('local with host %s' % host)
    user = settings.XBMC_USER
    password = settings.XBMC_PASSWD
    xbmc_i = XBMC(get_json_rpc(host), user, password)
    return xbmc_i

def look_at_res(msg, res):
    """ takes the result from a kodi json command """
    
    if res is not None:
        success = False
        if "result" in res and (res["result"] == "OK" or
            res["result"] == True):
            success = True
            # Application.SetVolume returns an integer
        # JSONRPC.Ping() returns the string 'pong'
        elif "result" in res and res["result"] == "pong":
            print("OK ping returned pong")
            success = True
        elif "error" in res and "message" in res["error"]:
            message = (res["error"]["message"])
            amsg = ('msg %s %s' % (msg,message))
            raise MyException(amsg)
        else:
            message = ("Kodi Unknown error : '%s'" % (res))
            amsg = ('msg %s %s' % (msg,message))
            raise MyException(amsg)
        if success:
            print("Success.")
    return success

def to_kodi(thefile,host,xbmc_i):
    """ ping kodi and if successful open the player with the file
        thefile should be the full samba or local path, not the django
        static file path used for html
        Control of the playback is passed to kodi on the selected host
        xbmc_i should be the initialized kodi connection
        host is unused except in the message for an exception
    """
    ping_result = xbmc_i.JSONRPC.Ping()
    look_at_res('ping', ping_result)
    if ping_result:
        print('File to kodi %s' % thefile)
        context = {'item':{'file':thefile}}
        #guess at what a close might look like, not working
        #cresult = xbmc_i.Player.Close()
        #look_at_res(cresult)
        result = xbmc_i.Player.Open(context)
        look_at_res('Player.Open', result)
    else:
        message = unicode('Error unable to ping kodi at host %s' % host)
        raise MyException(message)

def send_to_kodi(ob,ip,local=False):
    """ send an object (song, movie) to kodi for playback
        where ob is the object, ip is the ip address
        of kodi where playback is requested
    """
    host = ip + settings.KODI_PORT
    if local:
        # use files from the local symbols links, no longer required
        # only need when running from 127.0.0.1
        thefile = utils.object_path_local(ob)
    else:
        print("using Samba")
        thefile = utils.object_path_samba(ob)
    try:
        xbmc_i = init_xbmc(host)
        to_kodi(thefile,host,xbmc_i)
    except Exception as ex:
        # in this case I want to see what the exception is
        # but there's no way to handle it,
        message = unicode('Cannot init_xbmc host %s exception %s' % (host,type(ex).__name__))
        print (message)
        raise MyException(message)


def playback_requests(ob,request):
    """ handle playback requests for object (song,movie)
        given the html POST request
        caller should catch MyException which is used for all
        errors in kodi playback
        vlc stream does not handle errors as it issues command line
        vlc plugin simple sets a flag to add the plugin to html
    """
    if 'StreamMovie' in request.POST:
        stream_to_vlc(obj,request)
    elif 'kodi_local' in request.POST:
        try:
            clientip = request.META['REMOTE_ADDR']
        except KeyError:
            message = unicode('ERROR could not get client ip from request')
            print(message)
            raise MyException(message)
        time.sleep(5)
        send_to_kodi(ob,clientip)
    elif 'kodi_lf' in request.POST:
        send_to_kodi(ob,settings.HOST_LF)
    elif 'kodi_bf' in request.POST:
        send_to_kodi(ob,settings.HOST_BF)    
    elif 'vlc_plugin' in request.POST:
        return True
    return False


##########################################################

def play_kodi(playlist,host,xbmc_i):
    """ ping kodi and if successful open the player with the file
        thefile should be the full samba or local path, not the django
        static file path used for html
        Control of the playback is passed to kodi on the selected host
        xbmc_i should be the initialized kodi connection
        host is unused except in the message for an exception
    """
    
    ping_result = xbmc_i.JSONRPC.Ping()
    look_at_res('ping',ping_result)
    if ping_result:
        id_context = {'playlistid':settings.KODI_PLAYLIST}        
        repeat_context = { 'repeat': 'all'}
        open_context = {'item':id_context, 'options': repeat_context}
        
        # clear the playlist
        cresult = xbmc_i.Playlist.Clear(id_context)
        look_at_res('playlist clear', cresult)
        
        # add to playlist 
        for ob in playlist:
            thefile = utils.object_path_samba(ob)
            print('file %s' % thefile)
            acontext = { 'file': thefile }
            print('acontext')
            pcontext = { 'playlistid': settings.KODI_PLAYLIST, 
                'item': acontext }
            print('pcontext')
            addresult = xbmc_i.Playlist.Add(pcontext)
            print('after Playlist.Add')
            msg = ('playlist add %s' % thefile)
            look_at_res(msg, addresult)
            
        # play it
        print('after for, before open')
        result = xbmc_i.Player.Open(open_context)
        print('after open')
        look_at_res('playlist open', result)
    else:
        message = unicode('Error unable to ping kodi at host %s' % host)
        raise MyException(message)


def play_to_kodi(playlist,ip):
    """ send the playlist to kodi for playback
        where ob is the object, ip is the ip address
        of kodi where playback is requested
    """
    host = ip + settings.KODI_PORT
    
    try:
        print("Attempt to init with host %s" % host)
        xbmc_i = init_xbmc(host)
        play_kodi(playlist,host,xbmc_i)
    except Exception as ex:
        # in this case I want to see what the exception is
        # but there's no way to handle it,
        message = unicode('Cannot init_xbmc host %s exception %s' % (host,type(ex).__name__))
        print (message)
        raise MyException(message)



def playlist_requests(playlist,request):
    """ handle play requests for playlist
        given the html POST request
        caller should catch MyException which is used for all
        errors in kodi playback
    """
    print('playlist_request')
    if 'kodi_local' in request.GET:        
        try:
            clientip = request.META['REMOTE_ADDR']
        except KeyError:
            message = unicode('ERROR could not get client ip from request')
            print(message)
            raise MyException(message)
        time.sleep(5)
        play_to_kodi(playlist,clientip)
        return True
    elif 'kodi_lf' in request.GET:
        play_to_kodi(playlist,settings.HOST_LF)
        return True
    elif 'kodi_bf' in request.GET:
        play_to_kodi(playlist,settings.HOST_BF)
        return True
    return False



##########################################################



##
#
# //Play a single video from file
# http://192.168.15.117/jsonrpc?request={"jsonrpc":"2.0","id":"1","method":"Player.Open","params":{"item":{"file":"Media/Big_Buck_Bunny_1080p.mov"}}}
# http://192.168.2.30/

def stream_to_vlc(movie,request):
    """ instruct vlc to stream the movie using host/client from
        html request
        note, no correct interface at this time, uses command line
    """
    print("User pressed StreamMovie")
    try:
        clientip = request.META['REMOTE_ADDR']
    except KeyError:
        clientip = 'unknown'
    hostip = request.get_host()

    #playit = "/home/catherine/FHL/FriendlyHomeLibrary/static/mediafiles/" + movie.collection.filePath + '/' + movie.fileName
    playit = utils.object_path_with_static(movie)
    sstr = ("vlc -vvv %s --sout \'#rtp{dst=%s,port=1234,sdp=rtsp://%s:8080/test.sdp}\'" % (playit,clientip,hostip[:-5]))
    print(sstr)
    os.system(sstr)



