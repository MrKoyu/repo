# -*- coding: UTF-8 -*-
'''
    Updated and refactored by someone.
    Originally created by others.
'''
# Addon Name: MTB
# Addon id: plugin.video.movietheaterbutter
# Addon Provider: SomeBody

import re
import sys
import urllib2

import xbmcgui
import xbmcplugin
from resources.lib.modules import control

syshandle = int(sys.argv[1])


class youtube_menu(object):
    def __init__(self):
        self.agent = 'VGFudHJ1bUFkZG9uQWdlbnQ='.decode('base64')
        self.key_id = 'QUl6YVN5QTU2ckhCQXlLMENsMFA0dURNXzEyc05Pd1VtQWFhczhF'.decode('base64')

    def openMenuFile(self, menuFile):
        req = urllib2.Request(menuFile)
        req.add_header('User-Agent', self.agent)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        return link

    def processMenuFile(self, menuFile):
        link = self.openMenuFile(menuFile).replace('\n', '').replace('\r', '')
        match = re.compile(
            'name="(.+?)".+?ection="(.+?)".+?earch="(.+?)".+?ubid="(.+?)".+?laylistid="(.+?)".+?hannelid="(.+?)".+?ideoid="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        return match

    def addMenuItem(self, name, action, subid, iconimage, fanart, description='', isFolder=True):
        u = sys.argv[0] + "?action=" + action + "&subid=" + subid
        liz = control.item(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
        liz.setProperty('fanart_image', fanart)
        control.addItem(handle=syshandle, url=u, listitem=liz, isFolder=isFolder)

    def addSectionItem(self, name, iconimage, fanart):
        u = sys.argv[0]+"?action=sectionItem"
        liz = control.item(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        control.addItem(handle=syshandle, url=u, listitem=liz, isFolder=False)

    def addSearchItem(self, name, search_id, icon, fanart):
        work_url = "plugin://plugin.video.youtube/kodion/search/query/?q="+search_id+"/"
        liz = control.item(name)
        liz.setInfo(type="Video", infoLabels={"Title": name})
        liz.setArt({'thumb': icon, 'banner': 'DefaultVideo.png', 'fanart': fanart})
#        liz.setPath(work_url)
        control.addItem(handle=syshandle, url=work_url, listitem=liz, isFolder=True)

    def addChannelItem(self, name, channel_id, icon, fanart):
        work_url = "plugin://plugin.video.youtube/channel/"+channel_id+"/"
        liz = control.item(name)
        liz.setInfo(type="Video", infoLabels={"Title": name})
        liz.setArt({'thumb': icon, 'banner': 'DefaultVideo.png', 'fanart': fanart})
#        liz.setPath(work_url)
        control.addItem(handle=syshandle, url=work_url, listitem=liz, isFolder=True)

    def addPlaylistItem(self, name, playlist_id, icon, fanart):
        work_url = "plugin://plugin.video.youtube/playlist/"+playlist_id+"/"
        liz = control.item(name)
        liz.setInfo(type="Video", infoLabels={"Title": name})
        liz.setArt({'thumb': icon, 'banner': 'DefaultVideo.png', 'fanart': fanart})
#        liz.setPath(work_url)
        control.addItem(handle=syshandle, url=work_url, listitem=liz, isFolder=True)

    def addVideoItem(self, name, video_id, icon, fanart):
        work_url = "plugin://plugin.video.youtube/play/?video_id="+video_id
        liz = control.item(name)
        liz.setInfo(type="Video", infoLabels={"Title": name})
        liz.setArt({'thumb': icon, 'banner': 'DefaultVideo.png', 'fanart': fanart})
#        liz.setPath(work_url)
        liz.setProperty('IsPlayable', 'true')
        control.addItem(handle=syshandle, url=work_url, listitem=liz, isFolder=True)
