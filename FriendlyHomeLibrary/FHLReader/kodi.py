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

class MyException(Exception):
    def __init__(self, msg):
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
            message = (res["error"]["message"])
            print(message)
            raise MyException(message)
        else:
            message = ("Kodi Unknown error : '%s'" % (res))
            print(message)
            raise MyException(message)
        if success:
            print("Success.")
    return success

def to_kodi(thefile,host,xbmc_i):
    ping_result = xbmc_i.JSONRPC.Ping()
    look_at_res(ping_result)
    if ping_result:
        print('File to kodi %s' % thefile)
        context = {'item':{'file':thefile}}
        #guess at what a close might look like, not working
        #cresult = xbmc_i.Player.Close()
        #look_at_res(cresult)
        result = xbmc_i.Player.Open(context)
        look_at_res(result)
    else:
        message = unicode('Error unable to ping kodi at host %s' % host)
        raise MyException(message)    

def send_to_kodi(ob,hosta,local=False):
    host = hosta+':8080' 
    if local:
        # use files from the local symbols links, no longer required
        # only need when running from 127.0.0.1
        thefile = utils.object_path_local(ob)
    else:
        print("using Samba")
        thefile = utils.object_path_samba(ob)
    try:
        print("Attempt to init with host %s" % host)
        xbmc_i = init_xbmc(host)
        to_kodi(thefile,host,xbmc_i)
    except Exception as ex:
        # in this case I want to see what the exception is
        # but there's no way to handle it, 
        message = unicode('Cannot init_xbmc host %s exception %s' % (host,type(ex).__name__))
        print (message)
        raise MyException(message)

def send_to_kodi_local(ob,request):
    print('kodi_local')
    try:
        clientip = request.META['REMOTE_ADDR']
    except KeyError:
        message = unicode('ERROR could not get client ip from request')
        print(message)
        raise MyException(message)
    send_to_kodi(ob,clientip)

def send_to_kodi_lf(ob):
    print('kodi_lf')
    # using the local path until kodi is correctly configured for samba
    send_to_kodi(ob,settings.HOST_LF)

def send_to_kodi_bf(ob):
    print('kodi_bf')
    send_to_kodi(obj.settings.HOST_BF)
        
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

def playback_requests(obj,request):
    if 'StreamMovie' in request.POST:
        stream_to_vlc(obj,request)
    elif 'kodi_local' in request.POST:
        send_to_kodi_local(obj,request)
    elif 'kodi_lf' in request.POST:
        send_to_kodi_lf(obj)
    elif 'kodi_bf' in request.POST:
        send_to_kodi_bf(obj)
    elif 'vlc_plugin' in request.POST:
        return True
    return False
    
