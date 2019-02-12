# -*- coding: utf-8 -*-

'''
    Some Add-on

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


from resources.lib.modules import log_utils
from resources.lib.modules import control
from resources.lib.modules import youtube
from resources.lib.modules import youtube_menu

import os,sys,re,datetime,urlparse

thishandle = int(sys.argv[1])

# initializes as Kids Corner, functions can override based on action and subid.
class yt_index:
    def __init__(self):
        self.action = 'kidscorner'
        self.base_url = 'aHR0cDovL20zdS54eXovbXRiL2tpZHNuYXRpb24vbWFzdGVyLw=='.decode('base64')
        self.mainmenu = 'JXNrbm1haW4udHh0'.decode('base64') % (self.base_url)
        self.submenu  = 'JXMvJXMudHh0'.decode('base64')
        self.default_icon   = 'JXMvaWNvbnMvaWNvbi5wbmc='.decode('base64')
        self.default_fanart = 'JXMvaWNvbnMvZmFuYXJ0LmpwZw=='.decode('base64')

    def init_vars(self, action):
        try:
            if action == 'fitness':
                self.action   = 'fitness'
                self.base_url = 'aHR0cDovL20zdS54eXovbXRiL2ZpdG5lc3N6b25lL21hc3Rlci8='.decode('base64')
                self.mainmenu = 'JXNmem1haW4udHh0'.decode('base64') % (self.base_url)
            elif action == 'legends':
                self.action   = 'legends'
                self.base_url = 'aHR0cDovL20zdS54eXovbXRiL2xlZ2VuZHNhZGRvbi9tYXN0ZXIvbWVudS8='.decode('base64')
                self.mainmenu = 'JXNpaG1haW4udHh0'.decode('base64') % (self.base_url)
            elif action == 'moviesyt':
                self.action   = 'moviesyt'
                self.base_url = 'aHR0cDovL20zdS54eXovbXRiL3l0bW92aWVzLw=='.decode('base64')
                self.mainmenu = 'JXNtb3ZpZXMucGhw'.decode('base64') % (self.base_url)
            elif action == 'kings':
                self.action   = 'kings'
                self.base_url = 'aHR0cDovL20zdS54eXovbXRiL3l0bW92aWVzLw=='.decode('base64')
                self.mainmenu = 'JXNraW5ncy5waHA='.decode('base64') % (self.base_url)
            elif action == 'kungfu':
                self.action   = 'kungfu'
                self.base_url = 'aHR0cDovL20zdS54eXovbXRiL3l0bW92aWVzLw=='.decode('base64')
                self.mainmenu = 'JXNrdW5nZnUucGhw'.decode('base64') % (self.base_url)
            elif action == 'urban':
                self.action   = 'urban'
                self.base_url = 'aHR0cDovL20zdS54eXovbXRiL3l0bW92aWVzLw=='.decode('base64')
                self.mainmenu = 'JXN1cmJhbi5waHA='.decode('base64') % (self.base_url)
            elif action == 'scifi':
                self.action   = 'scifi'
                self.base_url = 'aHR0cDovL20zdS54eXovbXRiL3l0bW92aWVzLw=='.decode('base64')
                self.mainmenu = 'JXNzY2lmaS50eHQ='.decode('base64') % (self.base_url)
            elif action == 'tvReviews':
                self.action   = 'tvReviews'
                self.base_url = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL211YWRkaWJ0dHYvdGhlY3JpdGljcy9tYXN0ZXIv'.decode('base64')
                self.mainmenu = 'JXN0ZWxldmlzaW9uLnR4dA=='.decode('base64') % (self.base_url)
            elif action == 'movieReviews':
                self.action   = 'movieReviews'
                self.base_url = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL211YWRkaWJ0dHYvdGhlY3JpdGljcy9tYXN0ZXIv'.decode('base64')
                self.mainmenu = 'JXNtb3ZpZXMudHh0'.decode('base64') % (self.base_url)
            self.submenu = self.submenu % (self.base_url, '%s')
            self.default_icon = self.default_icon % (self.base_url)
            self.default_fanart = self.default_fanart % (self.base_url)
        except:
            pass

    def root(self, action):
        try:
            self.init_vars(action)
            menuItems = youtube_menu.youtube_menu().processMenuFile(self.mainmenu)
            for name,section,searchid,subid,playlistid,channelid,videoid,iconimage,fanart,description in menuItems:
                if not subid == 'false': # Means this item points to a submenu
                    youtube_menu.youtube_menu().addMenuItem(name, self.action, subid, iconimage, fanart, description, True)
                elif not searchid == 'false': # Means this is a search term
                    youtube_menu.youtube_menu().addSearchItem(name, searchid, iconimage, fanart)
                elif not videoid == 'false': # Means this is a video id entry
                    youtube_menu.youtube_menu().addVideoItem(name, videoid, iconimage, fanart)
                elif not channelid == 'false': # Means this is a channel id entry
                    youtube_menu.youtube_menu().addChannelItem(name, channelid, iconimage, fanart)
                elif not playlistid == 'false': # Means this is a playlist id entry
                    youtube_menu.youtube_menu().addPlaylistItem(name, playlistid, iconimage, fanart)
                elif not section == 'false': # Means this is a section placeholder/info line
                    youtube_menu.youtube_menu().addSectionItem(name, self.default_icon, self.default_fanart)
            self.endDirectory()
        except:
            pass

    def get(self, action, subid):
        try:
            self.init_vars(action)
            thisMenuFile = self.submenu % (subid)
            menuItems = youtube_menu.youtube_menu().processMenuFile(thisMenuFile)
            for name,section,searchid,subid,playlistid,channelid,videoid,iconimage,fanart,description in menuItems:
                if not subid == 'false': # Means this item points to a submenu
                    youtube_menu.youtube_menu().addMenuItem(name, self.action, subid, iconimage, fanart, description, True)
                elif not searchid == 'false': # Means this is a search term
                    youtube_menu.youtube_menu().addSearchItem(name, searchid, iconimage, fanart)
                elif not videoid == 'false': # Means this is a video id entry
                    youtube_menu.youtube_menu().addVideoItem(name, videoid, iconimage, fanart)
                elif not channelid == 'false': # Means this is a channel id entry
                    youtube_menu.youtube_menu().addChannelItem(name, channelid, iconimage, fanart)
                elif not playlistid == 'false': # Means this is a playlist id entry
                    youtube_menu.youtube_menu().addPlaylistItem(name, playlistid, iconimage, fanart)
                elif not section == 'false': # Means this is a section placeholder/info line
                    youtube_menu.youtube_menu().addSectionItem(name, self.default_icon, self.default_fanart)
            self.endDirectory()
        except:
            pass

    def endDirectory(self):
        control.directory(thishandle, cacheToDisc=True)
