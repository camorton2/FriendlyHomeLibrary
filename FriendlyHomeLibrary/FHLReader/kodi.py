import os
import time

from FHLBuilder import models,choices
import FHLBuilder.utility as utils
import FHLReader.utility as rutils

from FriendlyHomeLibrary import settings

from xbmcjson import XBMC

##
# Note xbmc stuff based on/copied from
# https://github.com/jcsaaddupuy/xbmc-client/blob/master/src/xbmc_client/xbmc_client.py
##



def get_json_rpc(host):
    """ given the host construct the json rpc """
    jsonrpc = "jsonrpc"
    if not host.endswith("/"):
        jsonrpc = "/" + jsonrpc
    return host + jsonrpc


def init_xbmc(ip):
    """ given an ip address, setup the kodi connection """
    host = str('http://%s' % ip)
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
            raise rutils.MyException(amsg)
        else:
            message = ("Kodi Unknown error : '%s'" % (res))
            amsg = ('msg %s %s' % (msg,message))
            raise rutils.MyException(amsg)
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
        message = str('Error unable to ping kodi at host %s' % host)
        raise rutils.MyException(message)


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
        thefile = utils.object_path_samba(ob)
    try:
        xbmc_i = init_xbmc(host)
        to_kodi(thefile,host,xbmc_i)
    except Exception as ex:
        # in this case I want to see what the exception is
        # but there's no way to handle it, just pass it back for display
        message = str('Cannot init_xbmc host %s exception %s' % (host,type(ex).__name__))
        print (message)
        raise rutils.MyException(message)


def playback_requests(ob,request):
    """ handle playback requests for object (song,movie)
        given the html POST request
        caller should catch MyException which is used for all
        errors in kodi playback
        vlc stream does not handle errors as it issues command line
        vlc plugin simple sets a flag to add the plugin to html
    """
    if 'StreamMovie' in request.POST:
        stream_to_vlc(ob,request)
    elif 'kodi_local' in request.POST:
        clientip = rutils.ip_from_request(request)
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
# Kodi playlist section
##########################################################

def play_kodi(playlist,host,xbmc_i):
    """ ping kodi and if successful create a playlist and open kodi
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
            acontext = {'file': thefile }
            pcontext = {'playlistid': settings.KODI_PLAYLIST,
                'item': acontext }
            addresult = xbmc_i.Playlist.Add(pcontext)
            msg = ('playlist add %s' % thefile)
            look_at_res(msg, addresult)

        # play it
        result = xbmc_i.Player.Open(open_context)
        look_at_res('playlist open', result)
    else:
        message = str('Error unable to ping kodi at host %s' % host)
        raise rutils.MyException(message)


def play_to_kodi(playlist,ip,me):
    """ send the playlist to kodi for playback
        where ip is the ip address
        of kodi where playback is requested
    """
    host = ip + settings.KODI_PORT
    print('play_to_kodi host %s' % host)
    try:
        xbmc_i = init_xbmc(host)
        if playlist[0] and playlist[0].fileKind == choices.PICTURE:
            slideshow_kodi(playlist,host,xbmc_i,me)
            print('after calling slideshow_kodi')
        else:
            play_kodi(playlist,host,xbmc_i)
    except Exception as ex:
        # in this case I want to see what the exception is
        # but there's no way to handle it, just give back message
        message = str('Cannot init_xbmc host %s exception %s' % (host,type(ex).__name__))
        print (message)
        raise rutils.MyException(message)


def playlist_requests_new(playlist,pattern,me,request):
    """ handle play requests for playlist
        given the html GET request
        caller should catch MyException which is used for all
        errors in kodi playback
    """
    
    if 'kodi_local' == pattern:
        try:
            clientip = request.META['REMOTE_ADDR']
        except KeyError:
            message = str('ERROR could not get client ip from request')
            print(message)
            raise rutils.MyException(message)
        time.sleep(5)
        play_to_kodi(playlist,clientip,me)
        return True
    elif 'kodi_lf' == pattern:
        play_to_kodi(playlist,settings.HOST_LF,me)
        return True
    elif 'kodi_bf' == pattern:
        time.sleep(5)
        play_to_kodi(playlist,settings.HOST_BF,me)
        return True
    return False


def playlist_select(playlist,playback,request):
    """ handle play requests for playlist
        given playback from choices.songplay
        caller should catch MyException which is used for all
        errors in kodi playback
    """
    try:
        me = models.User.objects.get(username=request.user)
    except models.User.DoesNotExist:
        me = None
    
    if playback == choices.KODI_LOCAL:
        print('local')
        try:
            clientip = request.META['REMOTE_ADDR']
        except KeyError:
            message = str('ERROR could not get client ip from request')
            print(message)
            raise rutils.MyException(message)
        time.sleep(5)
        play_to_kodi(playlist,clientip,me)
        return True
    elif playback == choices.KODI_LF:
        print('lf')
        play_to_kodi(playlist,settings.HOST_LF,me)
        return True
    elif playback == choices.KODI_BF:
        print('bf')
        time.sleep(5)
        play_to_kodi(playlist,settings.HOST_BF,me)
        return True
    return False


def playlist_requests(playlist,request):
    """ handle play requests for playlist
        given the html GET request
        caller should catch MyException which is used for all
        errors in kodi playback
    """
    if 'kodi_local' in request.GET:
        return playlist_select(playlist,choices.KODI_LOCAL,request)
    elif 'kodi_lf' in request.GET:
        return playlist_select(playlist,choices.KODI_LF,request)
    elif 'kodi_bf' in request.GET:
        return playlist_select(playlist,choices.KODI_BF,request)
    return False


def slideshow_kodi(playlist,host,xbmc_i, me):
    """ kodi playlist is from a directory, so this annotates the 
        pictures in the playlist and copies them to /tmp/slides-username
        Still to do: clean up pictures from previous slide shows
    """    
    
    print("picturelist to kodi")
    try:
        rutils.cleanup_my_private_directory(me,'slides')
        file_path,_ = rutils.my_private_directory(me,'slides')
        # put all the pictures in the directory
        for picture in playlist:
            _,_ = rutils.annotate(picture,me)

        ping_result = xbmc_i.JSONRPC.Ping()
        look_at_res('ping',ping_result)
        if ping_result:
            print('after ping with file_path %s' % file_path)
            path_context = { 'directory': file_path}
            open_context = {'item':path_context}

            # play it
            result = xbmc_i.Player.Open(open_context)
            look_at_res('playlist open', result)
        else:
            message = str('Error unable to ping kodi at host %s' % host)
            raise rutils.MyException(message)

    except Exception as ex:
        # in this case I want to see what the exception is
        # but there's no way to handle it, just give back message
        message = str('Cannot create/link kodi directory %s' % (type(ex).__name__))
        print (message)
        print (playlist)
        raise rutils.MyException(message)

    

############## vlc ################
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



