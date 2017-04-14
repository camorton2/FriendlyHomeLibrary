# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import FHLBuilder.utility as utils
from FriendlyHomeLibrary import settings
from xbmcjson import XBMC

##
# Note xbmc stuff based on/copied from
# https://github.com/jcsaaddupuy/xbmc-client/blob/master/src/xbmc_client/xbmc_client.py
##



def get_json_rpc(host):
    jsonrpc = "jsonrpc"
    if not host.endswith("/"):
        jsonrpc = "/" + jsonrpc
    return host + jsonrpc

def init_xbmc():
    host = settings.XBMC_HOST
    user = settings.XBMC_USER
    password = settings.XBMC_PASSWD
    if not host:
        raise Exception("No host found")
    if not user:
        raise Exception("No user found")
    xbmc_i = XBMC(get_json_rpc(host), user, password)
    return xbmc_i

def init_xbmc_BF():
    host = settings.XBMC_HOST_BF
    user = settings.XBMC_USER_BF
    password = settings.XBMC_PASSWD_BF
    if not host:
        raise Exception("No host found")
    if not user:
        raise Exception("No user found")
    xbmc_i = XBMC(get_json_rpc(host), user, password)
    return xbmc_i


def look_at_res(res):
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
            print(res["error"]["message"])
        else:
            print("Unknown error : '%s'" % (res))
        if success:
            print("Success.")
    return success

def send_to_kodi_lf(ob):
    sstr = utils.object_path(ob)
    #url = settings.HTTP_URL+settings.STATIC_URL+sstr
    #print(url)
    xbmc_i = init_xbmc()
    ping_result = xbmc_i.JSONRPC.Ping()
    look_at_res(ping_result)
    if ping_result:
        thefile = settings.STATIC_URL+sstr
        context = {"item":{"file":thefile}}
        result = xbmc_i.Player.Open(context)
        look_at_res(result)
    else:
        print("Ooops unable to ping kodi_lf - maybe she is sleeping")

def send_to_kodi_bf(ob):
    sstr = utils.object_path(ob)
    #url = settings.HTTP_URL+settings.STATIC_URL+sstr
    #print(url)
    xbmc_i = init_xbmc_BF()
    ping_result = xbmc_i.JSONRPC.Ping()
    look_at_res(ping_result)
    if ping_result:
        thefile = settings.STATIC_URL+sstr
        context = {"item":{"file":thefile}}
        result = xbmc_i.Player.Open(context)
        look_at_res(result)
    else:
        print("Ooops unable to ping kodi_bf - maybe he is sleeping")

def songs_to_kodi_bf(songlist):
    print ("Wouldn't this be nice to have")

def songs_to_kodi_lf(songlist):
    print ("Wouldn't this be nice to have")
    xbmc_i = init_xbmc()
    playlist = []
    for song,path in songlist:
        print ("adding to playlist %s" % song.title)
        sstr = utils.object_path(song)
        thefile = settings.STATIC_URL+sstr
        playlist.append(thefile)
    # playlist.shuffle()
    ping_result = xbmc_i.JSONRPC.Ping()
    look_at_res(ping_result)
    if ping_result:
        context = {"item":{"playlistid":1}}
        #context = {"item":{"file":playlist}}
        result = xbmc_i.Player.Open(context)
        look_at_res(result)
    else:
        print("Ooops unable to ping kodi_lf - maybe she is sleeping")
    
    
##
# 
# //Play a single video from file
# http://192.168.15.117/jsonrpc?request={"jsonrpc":"2.0","id":"1","method":"Player.Open","params":{"item":{"file":"Media/Big_Buck_Bunny_1080p.mov"}}}    
# http://192.168.2.30/



def stream_to_vlc(movie,request):
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

