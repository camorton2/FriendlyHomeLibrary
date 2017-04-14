# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from FHLBuilder.utility import object_path, to_str
from FriendlyHomeLibrary import settings
from xbmcjson import XBMC, PLAYER_VIDEO


def initializeXbmc():
    host = self.getHost()
    user = self.getUser()
    password = self.getPassword()
    if not host:
        raise Exception(
            "No host found. Have you configured the default config file %s ?"
            % (self.getDefaultConfig()))
    if not user:
        raise Exception(
                "No user found. Have you configured the default config file %s ?"
                % (self.getDefaultConfig()))
    self.xbmc = XBMC(self.getJsonRpc(host), user, password)


def send_to_kodi(ob):
    # http://127.0.0.1:8000/home/catherine/FHL/FriendlyHomeLibrary/static/links/drive2/mp3s/Bruce_Cockburn/01-christmas/01-adeste_fidelis.mp3
    # this starts from /links
    sstr = object_path(ob)
    # settings.STATIC_URL is from /home ... static/
    # settings.HTTP_URL is http://127.0.0.1:8000
    
    url = settings.XBMC_HOST+settings.STATIC_URL+sstr
    print(url)
    #os.system('/home/catherine/.local/bin/xbmc-client --url ' + url)
    
    
