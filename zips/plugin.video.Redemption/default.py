# -*- coding: utf-8 -*-
#update 2018-04-23 
import urllib
import urllib2
import datetime
import re
import os
import sys
import base64
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import traceback
import cookielib
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
try:
    # import json
    from json import loads,dumps
except:
    # import simplejson as json
    from simplejson import loads,dumps
import SimpleDownloader as downloader
import time
import requests
import koding
import byb_modules as BYB
import byb_api as BYBAPI
import _Edit
from libs._addon import *
from libs._common import *
from t0mm0.common.net import Net
# ADDED BY DEMO
from xbmcaddon import Addon
from xbmc import translatePath,getCondVisibility,executebuiltin
from os.path import join, exists
from base64 import b64decode as decode64
# ADDON FUNCTIONS AND CLASSES
addon           = addon = Addon()
addoninfo       = addon.getAddonInfo
setting         = addon.getSetting
setting_true    = lambda x: bool(True if setting(str(x)) == "true" else False)
setting_set     = addon.setSetting

# ADDON VARIABLES

#ADDON SPECIFIC VARIABLES
addon_version   = addoninfo('version')
addon_name      = addoninfo('name')
addon_id        = addoninfo('id')
addon_icon      = addoninfo("icon")
addon_fanart    = addoninfo("fanart")

#ADDON PATH VARIABLES
addon_profile   = translatePath(addoninfo('profile').decode('utf-8'))
addon_path      = translatePath(addoninfo('path').decode('utf-8'))	
addon_favorites = join(addon_profile, 'favorites')
addon_history   = join(addon_profile, 'history')
addon_revision  = join(addon_profile, 'list_revision')
addon_source    = join(addon_profile, 'source_file')
addon_resources = join(addon_path, 'resources')
addon_art       = join(addon_resources,'art')

#ADDON SETTINGS
setting_debug   = setting('debug')
setting_resolve = setting("resolverURL")
setting_tmdb    = setting('tmdb_key')
#ADDON BOOLEANS

# VARIOUS FUNCTIONS & CASSES
downloader      = downloader.SimpleDownloader()
hasaddon        = lambda x:         getCondVisibility("System.HasAddon({addon})".format(addon=str(x)))
notification    = lambda msg,icon=addon_icon,time=10,name=addon_name:    executebuiltin("XBMC.Notification({addon},{msg},{time},{icon})".format(msg=str(msg),icon=icon,addon=name,time=str(int(time)*1000)))
container       = lambda x:         executebuiltin("XBMC.Container.Update({data})".format(str(x)))
# VARIOUS VARIABLES
headers             = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}
resolve_url         = ['allmyvideos.net','docs.google.com','plus.google.com','picasaweb.google.com','mail.ru','my.mail.ru','bitshare.com','k2s.cc','rapidgator.net', 'uploaded.net','vidspot.net','vidzi.tv']
g_ignoreSetResolved = ['plugin.video.dramasonline','plugin.video.f4mTester','plugin.video.shahidmbcnet','plugin.video.SportsDevil','plugin.stream.vaughnlive.tv','plugin.video.ZemTV-shani']

class NoRedirection(urllib2.HTTPErrorProcessor):
   def http_response(self, request, response):
       return response
   https_response = http_response

functions_dir   = addon_profile


FAV         = open(addon_favorites).read()  if exists(addon_favorites)      else []
SOURCES     = open(addon_source).read()     if exists(addon_source)         else []

icon_Setting            = join(addon_art,'tools.png')           if _Edit.SettingIcon        == "" else _Edit.SettingIcon
icon_History            = join(addon_art,'history.png')         if _Edit.HistoryIcon        == "" else _Edit.HistoryIcon
icon_YouTube            = join(addon_art,'youtube.png')         if _Edit.YouTubeIcon        == "" else _Edit.YouTubeIcon
icon_Favorite           = join(addon_art,'favorite.png')        if _Edit.FavoriteIcon       == "" else _Edit.FavoriteIcon
icon_DailyMotion        = join(addon_art,'dailymotion.png')     if _Edit.DailyMotionIcon    == "" else _Edit.DailyMotionIcon
icon_nextpage           = join(addon_art,'nextpage.png')        if _Edit.NextPageIcon       == "" else _Edit.NextPageIcon
icon_tmdb               = join(addon_art,'tmdb.png')            if _Edit.TmdbIcon           == "" else _Edit.TmdbIcon
fanart_Setting          = addon_fanart                          if _Edit.SettingFanart      == "" else _Edit.SettingFanart
fanart_History          = addon_fanart                          if _Edit.HistoryFanart      == "" else _Edit.HistoryFanart
fanart_YouTube          = addon_fanart                          if _Edit.YouTubeFanart      == "" else _Edit.YouTubeFanart
fanart_Favorite         = addon_fanart                          if _Edit.FavoriteFanart     == "" else _Edit.FavoriteFanart
fanart_DailyMotion      = addon_fanart                          if _Edit.DailyMotionFanart  == "" else _Edit.DailyMotionFanart
fanart_tmdb             = addon_fanart                          if _Edit.TmdbFanart         == "" else _Edit.TmdbFanart

if      setting_resolve     == "resolveurl":                                            import resolveurl as RESOLVE
elif    setting_resolve     == "urlresolver" and hasaddon('script.module.urlresolver'):  import urlresolver as RESOLVE
else:
    setting_set('resolverURL','resolveurl')     
    import resolveurl as RESOLVE

koding.dolog('Resolver in use = "{resolver}"'.format(resolver=setting_resolve),line_info=True)

if _Edit.UseTMDB :
    if _Edit.TMDB_api != '':
        TMDB_api = base64.b64decode(_Edit.TMDB_api)
    elif _Edit.TMDB_api == '':
        TMDB_api = setting('tmdb_key')
    if len(_Edit.TMDB_api) > 0 and len(setting('tmdb_key')) > 0:
        TMDB_api = setting('tmdb_key')
    if  len(TMDB_api) == 0:
        tmdbapi = koding.YesNo_Dialog(title=local_string(30015),message=local_string(30036))
        if tmdbapi:
            koding.Open_Settings(focus='2.1')
        else:
            pass
else:
    TMDB_api = ''

if _Edit.PodcastListSetLength:
    if not setting_true('podcastreturnlimit'):
        setting_set('podcastreturnlimit','true')
        if setting(int('podcastlistlenght')) == 0:
            setting_set('podcastlistlenght',_Edit.PodcastListLength)

def decode(String):
    try:
      return decode64(String)
    except TypeError:
      return String

def read(file):
    path = translatePath(file)
    f = open(path,"r")
    content = f.read()
    f.close()
    return content

def write(file,data):
    path = translatePath(file)
    f = open(path,"w+")
    f.write(data)
    f.close()

def makeRequest(url, headers=headers):
        try:
            req = urllib2.Request(url,None,headers)
            response = urllib2.urlopen(req)
            data = response.read()
            response.close()
            return data
        except urllib2.URLError, e:
            koding.dolog('URL: '+url,line_info=True)
            if hasattr(e, 'code'):
                koding.dolog('We failed with error code - %s.' % e.code,line_info=True)
                notification("We failed with error code - " + str(e.code))
            elif hasattr(e, 'reason'):
                koding.dolog('We failed to reach a server.',line_info=True)
                koding.dolog('Reason: '+str(e.reason),line_info=True)
                notification("We failed to reach a server. - "+str(e.reason))

def SKindex():
    koding.dolog("SKindex",line_info=True)
    BaseMode = True
    try:
        getData(_Edit.MainBase,'')
    except:
        try:
            if _Edit.BackUp != '':
                xbmc.executebuiltin("XBMC.Notification({},{},10000,{})".format(addon_name,local_string(30037),addon_icon))
                getData(_Edit.BackUp,'')
            else:
                raise
        except:
            BaseMode = koding.YesNo_Dialog(title=SingleColor('{}, {}'.format(addon_name,local_string(30039)),_Edit.DialogBoxColor1),message=SingleColor(local_string(30038),_Edit.DialogBoxColor2))
    if BaseMode != False:
        if _Edit.Enable_Search_Dir:
            addDir(ChannelColor(local_string(30040)),str(TMDB_api),400,icon_Search,fanart_Search,'','','','')
        getSources()
        if _Edit.Enable_ToolsSetting_Dir:
            addDir(ChannelColor(local_string(30041)),'',36,icon_Setting ,fanart_Setting,local_string(30041),'','','')
        if setting_true('devmode'):
            addDir(ChannelColor('Scraper Example'),'',900,addon_icon ,addon_fanart,'','','','')
            BYB.addDir_file(ChannelColor(local_string(30078)),'',1000,addon_icon ,addon_fanart,'','','','')
    else:
        xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
def getSources():
        if exists(addon_favorites):
            addDir(ChannelColor(local_string(30042)),'url',4 ,icon_Favorite,fanart_Favorite,'','','','')
        if setting_true("browse_xml_database"):
            addDir(ChannelColor(local_string(30043)),'http://xbmcplus.xb.funpic.de/www-data/filesystem/',15,addon_icon,addon_fanart,'','','','')
        if setting_true("browse_community"):
            addDir(ChannelColor(local_string(30044)),'community_files',16,addon_icon,addon_fanart,'','','','')
        if exists(addon_history) and setting_true('searchhistorymenu'):
            addDir(ChannelColor(local_string(30045)),'history',25,icon_History,fanart_History,'','','','')
        if setting_true("searchyt"):
            addDir(ChannelColor(local_string(30046)),'youtube',25,icon_YouTube,fanart_YouTube,'','','','')
        if setting_true("searchDM"):
            addDir(ChannelColor(local_string(30047)),'dmotion',25,icon_DailyMotion,fanart_DailyMotion,'','','','')
        if setting_true("PulsarM"):
            addDir(ChannelColor(local_string(30048)),'IMDBidplay',27,addon_icon,addon_fanart,'','','','')
        if setting_true('tmdb_use_own_data'):
            addDir(ChannelColor(local_string(30049)),TMDB_api,300,icon_tmdb,fanart_tmdb,'','','','')
        if exists(addon_source):
            sources = loads(read(addon_source))
            if len(sources) > 1:
                for i in sources:
                    ## for pre 1.0.8 sources
                    if isinstance(i, list):
                        addDir(i[0].encode('utf-8'),i[1].encode('utf-8'),1,addon_icon,addon_fanart,'','','','','source')
                    else:
                        thumb = addon_icon
                        fanart = addon_fanart
                        desc = ''
                        date = ''
                        credits = ''
                        genre = ''
                        if i.has_key('thumbnail'):
                            thumb = i['thumbnail']
                        if i.has_key('fanart'):
                            fanart = i['fanart']
                        if i.has_key('description'):
                            desc = i['description']
                        if i.has_key('date'):
                            date = i['date']
                        if i.has_key('genre'):
                            genre = i['genre']
                        if i.has_key('credits'):
                            credits = i['credits']
                        addDir(i['title'].encode('utf-8'),i['url'].encode('utf-8'),1,thumb,fanart,desc,genre,date,credits,'source')

            else:
                if len(sources) == 1:
                    if isinstance(sources[0], list):
                        getData(sources[0][1].encode('utf-8'),addon_fanart)
                    else:
                        getData(sources[0]['url'], sources[0]['fanart'])

def addSource(url=None):
        if url is None:
            if not setting("new_file_source") == "":
               source_url = setting('new_file_source').decode('utf-8')
            elif not setting("new_url_source") == "":
               source_url = setting('new_url_source').decode('utf-8')
        else:
            source_url = url
        if source_url == '' or source_url is None:
            return
        koding.dolog('Adding New Source: '+source_url.encode('utf-8'),line_info=True)
        media_info = None
        #print 'source_url',source_url
        data = getSoup(source_url)
        print 'source_url',source_url
        if isinstance(data,BeautifulSOAP):
            if data.find('channels_info'):
                media_info = data.channels_info
            elif data.find('items_info'):
                media_info = data.items_info
        if media_info:
            source_media = {}
            source_media['url'] = source_url
            try: source_media['title'] = media_info.title.string
            except: pass
            try: source_media['thumbnail'] = media_info.thumbnail.string
            except: pass
            try: source_media['fanart'] = media_info.fanart.string
            except: pass
            try: source_media['genre'] = media_info.genre.string
            except: pass
            try: source_media['description'] = media_info.description.string
            except: pass
            try: source_media['date'] = media_info.date.string
            except: pass
            try: source_media['credits'] = media_info.credits.string
            except: pass
        else:
            if '/' in source_url:
                nameStr = source_url.split('/')[-1].split('.')[0]
            if '\\' in source_url:
                nameStr = source_url.split('\\')[-1].split('.')[0]
            if '%' in nameStr:
                nameStr = urllib.unquote_plus(nameStr)
            keyboard = xbmc.Keyboard(nameStr,'Displayed Name, Rename?')
            keyboard.doModal()
            if (keyboard.isConfirmed() == False):
                return
            newStr = keyboard.getText()
            if len(newStr) == 0:
                return
            source_media = {}
            source_media['title'] = newStr
            source_media['url'] = source_url
            source_media['fanart'] = addon_fanart

        if exists(source_file):
            sources = loads(read(source_file))
            sources.append(source_media)
            write(source_file,dumps(sources))
        else:
            source_list = []
            source_list.append(source_media)
            write(source_file,dumps(source_list))
        setting_set('new_url_source', "")
        Setting_set('new_file_source', "")
        notification("New source added.",time=5)
        if not url is None:
            if 'xbmcplus.xb.funpic.de' in url:
                container("%s?mode=14,replace".format(sys.argv[0]))
            elif 'community-links' in url:
                container("%s?mode=10,replace".format(sys.argv[0]))
        else: addon.openSettings()

def rmSource(name):
        sources = loads(read(source_file))
        for index in range(len(sources)):
            if isinstance(sources[index], list):
                if sources[index][0] == name:
                    del sources[index]
                    write(source_file,dumps(sources))
                    break
            else:
                if sources[index]['title'] == name:
                    del sources[index]
                    write(source_file,dumps(sources))
                    break
        executebuiltin("XBMC.Container.Refresh")



def get_xml_database(url, browse=False):
        if url is None:
            url = 'http://xbmcplus.xb.funpic.de/www-data/filesystem/'
        soup = BeautifulSoup(makeRequest(url), convertEntities=BeautifulSoup.HTML_ENTITIES)
        for i in soup('a'):
            href = i['href']
            if not href.startswith('?'):
                name = i.string
                if name not in ['Parent Directory', 'recycle_bin/']:
                    if href.endswith('/'):
                        if browse:
                            addDir(name,url+href,15,addon_icon,addon_fanart,'','','')
                        else:
                            addDir(name,url+href,14,addon_icon,addon_fanart,'','','')
                    elif href.endswith('.xml'):
                        if browse:
                            addDir(name,url+href,1,addon_icon,addon_fanart,'','','','','download')
                        else:
                            if exists(source_file):
                                if name in SOURCES:
                                    addDir(name+' (in use)',url+href,11,addon_icon,addon_fanart,'','','','','download')
                                else:
                                    addDir(name,url+href,11,addon_icon,addon_fanart,'','','','','download')
                            else:
                                addDir(name,url+href,11,addon_icon,addon_fanart,'','','','','download')


def getCommunitySources(browse=False):
        url = 'http://community-links.googlecode.com/svn/trunk/'
        soup = BeautifulSoup(makeRequest(url), convertEntities=BeautifulSoup.HTML_ENTITIES)
        files = soup('ul')[0]('li')[1:]
        for i in files:
            name = i('a')[0]['href']
            if browse:
                addDir(name,url+name,1,addon_icon,addon_fanart,'','','','','download')
            else:
                addDir(name,url+name,11,addon_icon,addon_fanart,'','','','','download')


def getSoup(url,data=None):
        print 'getsoup',url,data
        if url.startswith('http://') or url.startswith('https://'):
            data = makeRequest(url)
            if re.search("#EXTM3U",data) or 'm3u' in url: 
                print 'found m3u data',data
                return data
                
        elif data == None:
            if xbmcvfs.exists(url):
                if url.startswith("smb://") or url.startswith("nfs://"):
                    copy = xbmcvfs.copy(url, join(addon_profile, 'temp', 'sorce_temp.txt'))
                    if copy:
                        data = read(join(addon_profile, 'temp', 'sorce_temp.txt'))
                        xbmcvfs.delete(join(addon_profile, 'temp', 'sorce_temp.txt'))
                    else:
                        koding.dolog("failed to copy from smb:",line_info=True)
                else:
                    data = read(url)
                    if re.match("#EXTM3U",data)or 'm3u' in url: 
                        print 'found m3u data',data
                        return data
            else:
                koding.dolog("Soup Data not found!",line_info=True)
                return
        return BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)


def getData(url,fanart):
    print 'url-getData',url
    SetViewLayout = "List"
    if not url.startswith(('http','tmdb=','plugin://plugin','plugin://script')):
        koding.dolog('Trying decode of link'+str(url),line_info=True)
        url = base64.urlsafe_b64decode(str(url))
    else:
        url = url 
    soup = getSoup(url)
    #print type(soup)
    tmdbapi = False 
    if isinstance(soup,BeautifulSOAP):
        if len(soup('layoutype')) > 0:
            SetViewLayout = "Thumbnail"		    

        if len(soup('channels')) > 0:
            channels = soup('channel')
            for channel in channels:
                linkedUrl=''
                lcount=0
                try:
                    linkedUrl =  channel('externallink')[0].string
                    lcount=len(channel('externallink'))
                except: pass
                if lcount>1: linkedUrl=''
                name = channel('name')[0].string
                if name.startswith('tmdb='):
                    tmdbapi = True
                    ID = name.split('=')[1]
                    if name.endswith('tv'):
                        BYBAPI.tmdb_tv_show_get_details(ID,TMDB_api)
                    elif name.endswith('tvseason'):
                        details = name.split('=')[2]
                        detail = re.compile('s(.+?)tvseason').findall(str(details))
                        for s in detail:
                            koding.dolog(s,line_info=True)
                            BYBAPI.tmdb_tv_show_get_season_details(ID,TMDB_api,s)
                    for items in BYBAPI.Details_list:
                        name = items.get('title','Name Missing')
                        tmdb_icon = items.get('poster_path',iconimage)
                        tmdb_fanart = items.get('backdrop_path',addon_fanart)
                        tmdb_description = items.get('overview','Overview Missing')
                        tmdb_date = items.get('release_date','Release date missing')
                        tmdb_genres = items.get('Genres','Genres Missing')
                        tmdb_season = items.get('season_number','')
                        tmdb_episode = items.get('episode_number','')
                try:
                    thumbnail = channel('thumbnail')[0].string
                except: 
                    thumbnail = None
                if thumbnail == None:
                    if linkedUrl.startswith('#YTsearch'):
                        thumbnail = join(addon_art,'youtube.png') if _Edit.YouTubeIcon == '' else _Edit.YouTubeIcon 
                    elif tmdbapi:
                        thumbnail = tmdb_icon
                    else:
                        thumbnail = ''
                try:
                    if not channel('fanart'):
                        if setting_true('use_thumb'):
                            fanArt = thumbnail
                        elif tmdbapi:
                            fanArt = tmdb_fanart
                        else:
                            fanArt = fanart
                    else:
                        fanArt = channel('fanart')[0].string
                    if fanArt == None:
                        if linkedUrl.startswith('https://www.youtube.com/') and not 'playlist?list=' in linkedUrl:
                            fanArt = ''
                        elif linkedUrl.startswith('#YTsearch'):
                            if _Edit.YT_SearchFanart == '':
                                fanArt = addon_fanart
                            else:
                                fanArt = _Edit.YT_SearchFanart
                        elif tmdbapi:
                            fanArt = tmdb_fanart
                        else:
                            raise
                except:
                    fanArt = fanart

                try:
                    if not channel('info'):
                        if tmdbapi:
                            desc = tmdb_description
                    else:
                        desc = channel('info')[0].string
                    if desc == None:
                        if tmdbapi:
                            desc = tmdb_description
                        else:
                            raise
                except:
                    desc = ''

                try:
                    if not channel('genre'):
                        if tmdbapi:
                            genre = tmdb_genres
                    else:
                        genre = channel('genre')[0].string
                    if genre == None:
                        if tmdbapi:
                            genre = tmdb_genres
                        else:
                            raise
                except:
                    genre = ''

                try:
                    if not channel('date'):
                        if tmdbapi:
                            date =  tmdb_date
                    else:
                        date = channel('date')[0].string
                    if date == None:
                        if tmdbapi:
                            date =  tmdb_date
                        else:
                            raise
                except:
                    date = ''

                try:
                    credits = channel('credits')[0].string
                    if credits == None:
                        raise
                except:
                    credits = ''
                #koding.dolog('passcode={}'.format(channel('passcode')[0].string))
                try:
                    PassCode = channel('passcode')[0].string
                    passcode = True if PassCode == 'true' else False
                except:
                    passcode = False
                try:
                    koding.dolog('name=%s linkedUrl=%s thumbnail=%s  fanArt=%s  desc=%s  genre=%s  date=%s credits=%s'%(name,linkedUrl,thumbnail,fanArt,desc,genre,date,credits),line_info=True)
                except:pass 
                try:
                    if linkedUrl=='' and passcode == False:
                        addDir(ChannelColor(name.encode('utf-8', 'ignore')),url.encode('utf-8'),2,thumbnail,fanArt,desc,genre,date,credits,True)
                    elif linkedUrl.startswith('https://www.youtube.com/') and not 'playlist?list=' in linkedUrl and passcode == False:
                        from libs import YouTube
                        YouTube.AddChannel(name,linkedUrl,thumbnail,fanArt,desc,genre,date,credits)
                    elif linkedUrl.startswith('#YTsearch')and passcode == False:
                        if '=' in linkedUrl:
                            search_term = linkedUrl.split('=')[1]
                            search_term = search_term.replace(' ','+')
                        else:
                            search_term = ''
                        addDir(ChannelColor(name.encode('utf-8')),search_term,35,thumbnail,fanArt,desc,genre,date,credits)
                    elif linkedUrl.startswith('tmdb=') and linkedUrl.endswith('=list')and passcode == False:
                        addDir(ChannelColor(name.encode('utf-8')),linkedUrl,500,thumbnail,fanArt,desc,genre,date,credits)
                    elif linkedUrl.startswith(('plugin://plugin.video.youtube/playlist/','https://www.youtube.com/playlist?list='))and passcode == False:
                        if linkedUrl.startswith('https://www.youtube.com/playlist?list='):
                            linkedUrl = linkedUrl.replace('https://www.youtube.com/playlist?list=','plugin://plugin.video.youtube/playlist/')+'/'
                        BYB.plugintools.add_item(title=ChannelColor(name.encode('utf-8')),url=linkedUrl,thumbnail=thumbnail,fanart=fanArt,folder=True)
                    elif linkedUrl.startswith('plugin://plugin') and not 'youtube/playlist' in linkedUrl and passcode == False:
                        BYB.plugintools.add_item(title=ChannelColor(name.encode('utf-8')),url=linkedUrl,thumbnail=thumbnail,fanart=fanArt,folder=True)
                    elif linkedUrl.startswith('plugin://script') and passcode == False:
                        BYB.plugintools.add_item(title=ChannelColor(name.encode('utf-8')),url=linkedUrl,thumbnail=thumbnail,fanart=fanArt,folder=True)
                    elif passcode == True:
                        addDir(ChannelColor(name.encode('utf-8')),linkedUrl.encode('utf-8'),37,thumbnail,fanArt,desc,genre,date,None,'source')
                    else:
                        addDir(ChannelColor(name.encode('utf-8')),linkedUrl.encode('utf-8'),1,thumbnail,fanArt,desc,genre,date,None,'source')
                except:
                    koding.dolog('There was a problem adding directory from getData(): '+ChannelColor(name.encode('utf-8', 'ignore')),line_info=True)
        else:
            koding.dolog('No Channels: getItems',line_info=True)
            getItems(soup('item'),fanart)
    else:
        koding.dolog('parse_m3u(soup)',line_info=True)
        parse_m3u(soup)

    if SetViewLayout == "Thumbnail":
       SetViewThumbnail()

	
	
# borrow from https://github.com/enen92/P2P-Streams-XBMC/blob/master/plugin.video.p2p-streams/resources/core/livestreams.py
# This will not go through the getItems functions ( means you must have ready to play url, no regex)
def parse_m3u(data):
    content = data.rstrip()
    match = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\n]+)').findall(content)
    total = len(match)
    print 'total m3u links',total
    for other,channel_name,stream_url in match:
        if 'tvg-logo' in other:
            thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
            if thumbnail:
                if thumbnail.startswith('http'):
                    thumbnail = thumbnail
                
                elif not setting('logo-folderPath') == "":
                    logo_url = setting('logo-folderPath')
                    thumbnail = logo_url + thumbnail

                else:
                    thumbnail = thumbnail
            #else:
            
        else:
            thumbnail = ''
        if 'type' in other:
            mode_type = re_me(other,'type=[\'"](.*?)[\'"]')
            if mode_type == 'yt-dl':
                stream_url = stream_url +"&mode=18"
            elif mode_type == 'regex':
                url = stream_url.split('&regexs=')
                #print url[0] getSoup(url,data=None)
                regexs = parse_regex(getSoup('',data=url[1]))
                
                addLink(url[0], channel_name,thumbnail,'','','','','',None,regexs,total)
                continue
        if stream_url.startswith('http') and stream_url.endswith('.ts'):
            stream_url = 'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(stream_url)+'&amp;streamtype=TSDOWNLOADER'
        addLink(stream_url, channel_name,thumbnail,'','','','','',None,'',total)
		
    xbmc.executebuiltin("Container.SetViewMode(50)")
	
def getChannelItems(name,url,fanart):
        soup = getSoup(url)
        channel_list = soup.find('channel', attrs={'name' : name.decode('utf-8')})
        items = channel_list('item')
        try:
            fanArt = channel_list('fanart')[0].string
            if fanArt == None:
                raise
        except:
            fanArt = fanart
        for channel in channel_list('subchannel'):
            name = channel('name')[0].string
            try:
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    raise
            except:
                thumbnail = ''
            try:
                if not channel('fanart'):
                    if setting_true('use_thumb'):
                        fanArt = thumbnail
                else:
                    fanArt = channel('fanart')[0].string
                if fanArt == None:
                    raise
            except:
                pass
            try:
                desc = channel('info')[0].string
                if desc == None:
                    raise
            except:
                desc = ''

            try:
                genre = channel('genre')[0].string
                if genre == None:
                    raise
            except:
                genre = ''

            try:
                date = channel('date')[0].string
                if date == None:
                    raise
            except:
                date = ''

            try:
                credits = channel('credits')[0].string
                if credits == None:
                    raise
            except:
                credits = ''

            try:
                addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),3,thumbnail,fanArt,desc,genre,credits,date)
            except:
                koding.dolog('There was a problem adding directory - '+name.encode('utf-8', 'ignore'),line_info=True)
        getItems(items,fanArt)


def getSubChannelItems(name,url,fanart):
        soup = getSoup(url)
        channel_list = soup.find('subchannel', attrs={'name' : name.decode('utf-8')})
        items = channel_list('subitem')
        getItems(items,fanart)

#hakamac sublink:playlink=:name=:#
def GetSublinks(name,url,iconimage,fanart):
    Name = name
    name = ''
    koding.dolog('using get sublinks',line_info=True)
    List=[]; ListU=[]; c=0
    all_videos = regex_get_all(url, 'sublink:', '#')
    for a in all_videos:
        if not 'playlink=' in a and not 'name=' in a:
            vurl = a.replace('sublink:','').replace('#','')
            if len(vurl) > 10:
                c=c+1; List.append(name+ ' Source ['+str(c)+']'); ListU.append(vurl)
        elif 'playlink=' in a and 'name=' in a:
            playlink = regex_from_to(a,'playlink=', ':name')
            koding.dolog(playlink,line_info=True)
            name = regex_from_to(a,'name=',':')
            if len(name) == 0:
                name = 'item Name Missing'
            koding.dolog(name,line_info=True)
            if len(playlink) > 10:
                c=c+1; List.append(name); ListU.append(playlink)
    if c==1:
        try:
            liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=ListU[0],listitem=liz)
            xbmc.Player().play(urlsolver(ListU[0]), liz)
        except:
            pass
    else:
        koding.dolog('using dialog for sublinks',line_info=True)
        dialog=xbmcgui.Dialog()
        if 'episode' in url.lower():
            message = '{} Select a Episode'.format(Name)
        elif 'channel' in url.lower():
            message = '{} Select a Channel'.format(Name)
        else:
            message = '{} Select A Source'.format(Name)
        rNo=dialog.select(message, List)
        if rNo>=0:
            rName=name
            rURL=str(ListU[rNo])
             #print 'Sublinks   Name:' + name + '   url:' + rURL
            try:
                liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=rURL,listitem=liz)
                xbmc.Player().play(urlsolver(rURL), liz)
            except:
                pass

				
def SearchChannels(Searchkey=False):
#hakamac code
    tmdbapi = False
    if Searchkey == False:
        Searchkey = ''
        keyboard = xbmc.Keyboard(Searchkey,_Edit.Search_Content_KeyBoardMsg)
        keyboard.doModal()
        if keyboard.isConfirmed():
           Searchkey = keyboard.getText().replace('\n','').strip()
           if len(Searchkey) == 0: 
              xbmcgui.Dialog().ok('RobinHood', 'Nothing Entered')
              return	   
    
    Searchkey = Searchkey.lower()
    List=[]
    if not _Edit.MainBase.startswith('http'):
        koding.dolog('Trying decode of link'+str(_Edit.MainBase),line_info=True)
        url = base64.urlsafe_b64decode(str(_Edit.MainBase))
    else:
        url = _Edit.MainBase
    List.append(url)
    PassedUrls = 0
    FoundChannel = 1 
    ReadChannel = 0
    FoundMatch = 0
    progress = xbmcgui.DialogProgress()
    progress.create('{} {}'.format(addon_name,local_string(30074)),' ')
	
    while FoundChannel != ReadChannel:
        BaseSearch = List[ReadChannel].strip()
        koding.dolog('read this one from file list (' + str(ReadChannel) + ')',line_info=True)  
        ReadChannel = ReadChannel + 1

        PageSource = ''
        net = Net()
        koding.dolog(BaseSearch,line_info=True)
        if not BaseSearch.startswith('http')and not BaseSearch.startswith('#') and not BaseSearch.startswith('tmdb=') :
            koding.dolog('Trying decode of link'+str(_Edit.MainBase),line_info=True)
            try:
                BaseSearch = base64.urlsafe_b64decode(str(BaseSearch))
            except:
                BaseSearch = BaseSearch
        try:
            PageSource = net.http_GET(BaseSearch).content
            PageSource = PageSource.encode('ascii', 'ignore').decode('ascii')
            #time.sleep(1)
        except: 
            pass
		
        if len(PageSource) < 10:
            PageSource = ''
            PassedUrls = PassedUrls + 1
            koding.dolog('*** PASSED ****' + BaseSearch + '  ************* Total Passed Urls: ' + str(PassedUrls),line_info=True)
            time.sleep(.5)
 
        percent = int( ( ReadChannel / 300) * 100) 
        message = '     Pages Read: '+str(ReadChannel)+'        Matches Found: ' + str(FoundMatch)
        progress.update(percent,"", message, "" )

        if progress.iscanceled():
           return
 		
        if len(PageSource) > 10:
            all_links = regex_get_all(PageSource, '<channel>', '</channel>')
            for a in all_links:
                vurl = regex_from_to(a, '<externallink>', '</externallink>')
                #name = regex_from_to(a, '<name>', '</name>')
                #print name + '    ' + vurl
                if len(vurl) > 5:
                   FoundChannel = FoundChannel + 1
                   List.append(vurl)
                   #print 'Found Channel: '+ str(FoundChannel) +' : '+ vurl 

            all_items = regex_get_all(PageSource, '<item>', '</item>')
            for a in all_items:
                vurl = regex_from_to(a, '<link>', '</link>')
                name = regex_from_to(a, '<title>', '</title>')
                nxtpage = regex_from_to(a,'<nextpage>','</nextpage>')
                if len(nxtpage) >5:
                    List.append(nxtpage)
                TestName = '  ' + name.lower() + '  '
                #print 'Testing:' + TestName + '  ' + Searchkey
                if len(vurl) > 5 and TestName.find(Searchkey) > 0:
                    FoundMatch = FoundMatch + 1
                    fanart = ''
                    if name.startswith('tmdb='):
                        fullname = name
                        koding.dolog('Using TMDB for Meta Data',line_info=True)
                        tmdbapi = True
                        ID = name.split('=')[1]
                        if name.endswith('movie'):
                            BYBAPI.tmdb_movies_get_details(ID,TMDB_api)
                        elif name.endswith('tv'):
                            BYBAPI.tmdb_tv_show_get_details(ID,TMDB_api)
                        elif name.endswith('tvshow'):
                            details = name.split('=')[2]
                            detail = re.compile('s(.+?)_e(.+?)tvshow').findall(str(details))
                            for s,e in detail:
                                BYBAPI.tmdb_tv_show_get_episode_details(ID,TMDB_api,s,e)
                        for items in BYBAPI.Details_list:
                            name = items.get('title','')
                            if name == '':
                                name = items.get('name','Name Missing')
                            tmdb_icon = items.get('poster_path',addon_icon)
                            tmdb_fanart = items.get('backdrop_path',addon_fanart)
                            tmdb_description = items.get('overview','Overview Missing')
                            tmdb_date = items.get('release_date','Release date missing')
                            tmdb_genres = items.get('Genres','Genres Missing')
                            tmdb_season = items.get('season_number','')
                            tmdb_episode = items.get('episode_number','')
                        if fullname.startswith('tmdb=') and fullname.endswith('tvshow'):
                            if setting('season_episode_number') == 'true':
                                name = str(tmdb_season)+'x'+str(tmdb_episode)+' '+name
                    thumbnail = regex_from_to(a, '<thumbnail>', '</thumbnail>')
                    fanart = regex_from_to(a, '<fanart>', '</fanart>')
                    if len(fanart) < 5:
                       fanart = addon_fanart
                    if vurl.find('sublink') > 0:
                        addDir(ChannelColor(name),vurl,30,thumbnail,fanart,'','','','')
                    elif tmdbapi == True:
                        if vurl.startswith('#search='):
                            iconimage = tmdb_icon
                            addDir(ItemColor(name),str(vurl),600,iconimage,tmdb_fanart,tmdb_description,tmdb_genres,tmdb_date,'')
                        else:
                            addLink(str(vurl),ItemColor(name),tmdb_icon,tmdb_fanart,tmdb_description,tmdb_genres,tmdb_date,True,None,'',1)
                    else: 
                        addLink(str(vurl),ItemColor(name),thumbnail,fanart,'','','',True,None,'',1)
						
    
    progress.close()
    xbmc.executebuiltin("Container.SetViewMode(50)")
	
def Search_m3u(data,Searchkey):
    content = data.rstrip()
    match = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\n]+)').findall(content)
    total = len(match)
    koding.dolog('total m3u links'+str(total),line_info=True)
    for other,channel_name,stream_url in match:
        if 'tvg-logo' in other:
            thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
            if thumbnail:
                if thumbnail.startswith('http'):
                    thumbnail = thumbnail
                
                elif not setting('logo-folderPath') == "":
                    logo_url = setting('logo-folderPath')
                    thumbnail = logo_url + thumbnail

                else:
                    thumbnail = thumbnail
            #else:
            
        else:
            thumbnail = ''
        if 'type' in other:
            mode_type = re_me(other,'type=[\'"](.*?)[\'"]')
            if mode_type == 'yt-dl':
                stream_url = stream_url +"&mode=18"
            elif mode_type == 'regex':
                url = stream_url.split('&regexs=')
                #print url[0] getSoup(url,data=None)
                regexs = parse_regex(getSoup('',data=url[1]))
                
                addLink(url[0],ItemColor(channel_name),thumbnail,'','','','','',None,regexs,total)
                continue
        addLink(stream_url,ItemColor( channel_name),thumbnail,'','','','','',None,'',total)

def FindFirstPattern(text,pattern):
    result = ""
    try:    
        matches = re.findall(pattern,text, flags=re.DOTALL)
        result = matches[0]
    except:
        result = ""

    return result
	
def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r				

def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
	   try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
	   except: r = ''
    else:
       try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
       except: r = ''
    return r

def getItems(items,fanart):
        total = len(items)
        print 'START GET ITEMS *****'
        koding.dolog('Total Items: %s' %total,line_info=True)
        for item in items:
            isXMLSource=False
            isJsonrpc = False
            tmdbapi = False
            try:
                name = item('title')[0].string
                fullname = name
                if name.startswith('tmdb='):
                    koding.dolog('Using TMDB for Meta Data',line_info=True)
                    tmdbapi = True
                    ID = name.split('=')[1]
                    if name.endswith('movie'):
                        BYBAPI.tmdb_movies_get_details(ID,TMDB_api)
                    elif name.endswith('tv'):
                        BYBAPI.tmdb_tv_show_get_details(ID,TMDB_api)
                    elif name.endswith('tvshow'):
                        details = name.split('=')[2]
                        detail = re.compile('s(.+?)_e(.+?)tvshow').findall(str(details))
                        for s,e in detail:
                            BYBAPI.tmdb_tv_show_get_episode_details(ID,TMDB_api,s,e)
                    for items in BYBAPI.Details_list:
                        name = items.get('title','Name Missing')
                        tmdb_icon = items.get('poster_path',iconimage)
                        tmdb_fanart = items.get('backdrop_path',addon_fanart)
                        tmdb_description = items.get('overview','Overview Missing')
                        tmdb_date = items.get('release_date','Release date missing')
                        tmdb_genres = items.get('Genres','Genres Missing')
                        tmdb_season = items.get('season_number','')
                        tmdb_episode = items.get('episode_number','')
                    if fullname.startswith('tmdb=') and fullname.endswith('tvshow'):
                        if setting('season_episode_number') == 'true':
                            name = str(tmdb_season)+'x'+str(tmdb_episode)+' '+name
                elif name is None:
                    name = 'unknown?'
            except:
                koding.dolog('Name Error',line_info=True)
                name = ''


            try:
                if item('epg'):
                    if item.epg_url:
                        koding.dolog('Get EPG Regex',line_info=True)
                        epg_url = item.epg_url.string
                        epg_regex = item.epg_regex.string
                        epg_name = get_epg(epg_url, epg_regex)
                        if epg_name:
                            name += ' - ' + epg_name
                    elif item('epg')[0].string > 1:
                        name += getepg(item('epg')[0].string)
                else:
                    pass
            except:
                koding.dolog('EPG Error',line_info=True)
            try:
                url = []
                if len(item('link')) >0:
#                    print 'item link', item('link')
                    for i in item('link'):
                        if not i.string == None:
                            url.append(i.string)
                    
                elif len(item('sportsdevil')) >0:
                    for i in item('sportsdevil'):
                        if not i.string == None:
                            sportsdevil = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' +i.string
                            referer = item('referer')[0].string
                            if referer:
                                #print 'referer found'
                                sportsdevil = sportsdevil + '%26referer=' +referer
                            url.append(sportsdevil)
                elif len(item('p2p')) >0:
                    for i in item('p2p'):
                        if not i.string == None:
                            if 'sop://' in i:
                                sop = 'plugin://plugin.video.p2p-streams/?url='+i.string +'&amp;mode=2&amp;' + 'name='+name 
                                url.append(sop) 
                            else:
                                p2p='plugin://plugin.video.p2p-streams/?url='+i.string +'&amp;mode=1&amp;' + 'name='+name 
                                url.append(p2p)
                elif len(item('vaughn')) >0:
                    for i in item('vaughn'):
                        if not i.string == None:
                            vaughn = 'plugin://plugin.stream.vaughnlive.tv/?mode=PlayLiveStream&amp;channel='+i.string
                            url.append(vaughn)
                elif len(item('ilive')) >0:
                    for i in item('ilive'):
                        if not i.string == None:
                            if not 'http' in i.string:
                                ilive = 'plugin://plugin.video.tbh.ilive/?url=http://www.streamlive.to/view/'+i.string+'&amp;link=99&amp;mode=iLivePlay'
                            else:
                                ilive = 'plugin://plugin.video.tbh.ilive/?url='+i.string+'&amp;link=99&amp;mode=iLivePlay'
                elif len(item('yt-dl')) >0:
                    for i in item('yt-dl'):
                        if not i.string == None:
                            ytdl = i.string + '&mode=18'
                            url.append(ytdl)
                elif len(item('utube')) >0:
                    for i in item('utube'):
                        if not i.string == None:
                            if len(i.string) == 11:
                                utube = 'plugin://plugin.video.youtube/play/?video_id='+ i.string 
                            elif i.string.startswith('PL') and not '&order=' in i.string :
                                utube = 'plugin://plugin.video.youtube/play/?&order=default&playlist_id=' + i.string
                            else:
                                utube = 'plugin://plugin.video.youtube/play/?playlist_id=' + i.string 
                    url.append(utube)
                elif len(item('imdb')) >0:
                    for i in item('imdb'):
                        if not i.string == None:
                            if setting('genesisorpulsar') == '0':
                                imdb = 'plugin://plugin.video.genesis/?action=play&imdb='+i.string
                            else:
                                imdb = 'plugin://plugin.video.pulsar/movie/tt'+i.string+'/play'
                            url.append(imdb)                      
                elif len(item('f4m')) >0:
                        for i in item('f4m'):
                            if not i.string == None:
                                if '.f4m' in i.string:
                                    f4m = 'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(i.string)
                                elif '.m3u8' in i.string:
                                    f4m = 'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(i.string)+'&amp;streamtype=HLS'
                                    
                                else:
                                    f4m = 'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(i.string)+'&amp;streamtype=SIMPLE'
                        url.append(f4m)
                elif len(item('ftv')) >0:
                    for i in item('ftv'):
                        if not i.string == None:
                            ftv = 'plugin://plugin.video.F.T.V/?name='+urllib.quote(name) +'&url=' +i.string +'&mode=125&ch_fanart=na'
                        url.append(ftv)                        
                if len(url) < 1:
                    raise
            except:
                koding.dolog('Error <link> element, Passing:'+name.encode('utf-8', 'ignore'),line_info=True)
                #continue
                
            isXMLSource = False
            isNextPage  = False
            try:
                isNextPage = item('nextpage')[0].string
            except:pass
            if isNextPage:
                ext_url = [isNextPage]
                isNextPage = True
            else:
                isNextPage = False

            try:
                isXMLSource = item('externallink')[0].string
            except: pass
            
            if isXMLSource:
                ext_url=[isXMLSource]
                isXMLSource=True
            else:
                isXMLSource=False
            koding.dolog('isXMLSource = '+str(isXMLSource),line_info=True)
            try:
                isJsonrpc = item('jsonrpc')[0].string
            except: pass
            if isJsonrpc:
                ext_url=[isJsonrpc]
                isJsonrpc=True
            else:
                isJsonrpc=False            
            try:
                thumbnail = item('thumbnail')[0].string
                if thumbnail == None:
                    if tmdbapi:
                        thumbnail = tmdb_icon
                    else:
                        raise
            except:
                thumbnail = ''
            try:
                if not item('fanart'):
                    if setting('use_thumb') == "true":
                        fanArt = thumbnail
                    elif tmdbapi:
                        fanArt = tmdb_fanart
                    else:
                        fanArt = fanart
                else:
                    fanArt = item('fanart')[0].string
                if fanArt == None:
                    if tmdbapi:
                        fanArt = tmdb_fanart
                    else:
                        raise
            except:
                fanArt = fanart
            try:
                if not item('info'):
                    if tmdbapi == True:
                        desc = tmdb_description
                else:
                    desc = item('info')[0].string
                if desc == None:
                    if tmdbapi == True:
                        desc = tmdb_description
                    else:
                        raise
            except:
                desc = ''

            try:
                if not item('genre'):
                    if tmdbapi:
                        if tmdb_genres is list:
                            genre =  ', '.join(tmdb_genres)
                        else:
                            genre = tmdb_genres
                else:
                    genre = item('genre')[0].string
                if genre == None:
                    if tmdbapi:
                        if tmdb_genres is list:
                            genre =  ', '.join(tmdb_genres)
                        else:
                            genre = tmdb_genres
                    else:
                        raise
            except:
                genre = ''

            try:
                if not item('date'):
                    if tmdbapi == True:
                        date = tmdb_date
                else:
                    date = item('date')[0].string
                if date == None:
                    if tmdbapi == True:
                        date = tmdb_date
                    else:
                        raise
            except:
                date = ''

            regexs = None
            if item('regex'):
                try:
                    reg_item = item('regex')
                    regexs = parse_regex(reg_item)
                except:
                    pass            
            koding.dolog('url list= %s len of list= %s'%(url,len(url)),line_info=True)
            koding.dolog(ItemColor(name),line_info=True)
            try:
                if len(url) > 1:
                    host = RESOLVE.HostedMediaFile(url)
                    ValidUrl = host.valid_url()
                    alt = 0
                    playlist = []
                    koding.dolog('url = %s'%url,line_info=True)
                    for i in url:
                        koding.dolog('url= %s'%i,line_info=True)
                        if setting('ask_playlist_items') == 'true':
                            if regexs:
                                playlist.append(i+'&regexs='+regexs)
                            elif  any(x in i for x in resolve_url) or ValidUrl == True and  i.startswith('http'):
                                playlist.append(i+'&mode=19')                           
                        else:
                            playlist.append(i)
                    if setting('add_playlist') == "false":                    
                            for i in url:
                                alt += 1
                                print 'ADDLINK 1'
                                addLink(i,'%s) %s' %(alt, name.encode('utf-8', 'ignore')),thumbnail,fanArt,desc,genre,date,True,playlist,regexs,total)                            
                    else:
                        addLink('',Item( name.encode('utf-8', 'ignore')),thumbnail,fanArt,desc,genre,date,True,playlist,regexs,total)
                else:
                    if isXMLSource:
                    	addDir(ChannelColor(name.encode('utf-8')),ext_url[0].encode('utf-8'),1,thumbnail,fanart,desc,genre,date,None,'source')
                    elif isNextPage:
                        addDir(ChannelColor(name.encode('utf-8')),ext_url[0].encode('utf-8'),1,icon_nextpage,fanart,'','','',None,'source')
                    elif isJsonrpc:
                        addDir(ChannelColor(name.encode('utf-8')),ext_url[0],53,thumbnail,fanart,desc,genre,date,None,'source')
                    elif url[0].find('sublink') > 0:
                        addDir(ChannelColor(name.encode('utf-8')),url[0],30,thumbnail,fanart,'','','','')
                        #addDir(name.encode('utf-8'),url[0],30,thumbnail,fanart,desc,genre,date,'sublink')
                    elif str(url[0]) == '#infoline':
                        BYB.addDir_file(ItemColor(name.encode('utf-8')),'',00,thumbnail,fanArt,desc,'','','')
                    elif str(url[0]).startswith('#search'):
                        BYB.addDir(ItemColor(name.encode('utf-8','ignore')),url[0],600,thumbnail,fanArt,desc,genre,date,'','')				
                    else: 
                        addLink(url[0],ItemColor(name.encode('utf-8', 'ignore')),thumbnail,fanArt,desc,genre,date,True,None,regexs,total)
                    del BYBAPI.Details_list[:]
            except:
                koding.dolog('There was a problem adding item - '+name.encode('utf-8', 'ignore'),line_info=True)     

def parse_regex(reg_item):
                try:
                    regexs = {}
                    for i in reg_item:
                        regexs[i('name')[0].string] = {}
                        #regexs[i('name')[0].string]['expre'] = i('expres')[0].string
                        try:
                            regexs[i('name')[0].string]['expre'] = i('expres')[0].string
                            if not regexs[i('name')[0].string]['expre']:
                                regexs[i('name')[0].string]['expre']=''
                        except:
                            koding.dolog("Regex: -- No Referer --",line_info=True)
                        regexs[i('name')[0].string]['page'] = i('page')[0].string
                        try:
                            regexs[i('name')[0].string]['refer'] = i('referer')[0].string
                        except:
                            koding.dolog("Regex: -- No Referer --",line_info=True)
                        try:
                            regexs[i('name')[0].string]['connection'] = i('connection')[0].string
                        except:
                            koding.dolog("Regex: -- No connection --",line_info=True)

                        try:
                            regexs[i('name')[0].string]['notplayable'] = i('notplayable')[0].string
                        except:
                            koding.dolog("Regex: -- No notplayable --",line_info=True)
                            
                        try:
                            regexs[i('name')[0].string]['noredirect'] = i('noredirect')[0].string
                        except:
                            koding.dolog("Regex: -- No noredirect --",line_info=True)
                        try:
                            regexs[i('name')[0].string]['origin'] = i('origin')[0].string
                        except:
                            koding.dolog("Regex: -- No origin --",line_info=True)
                        try:
                            regexs[i('name')[0].string]['includeheaders'] = i('includeheaders')[0].string
                        except:
                            koding.dolog("Regex: -- No includeheaders --",line_info=True)                            
                            
                        try:
                            regexs[i('name')[0].string]['x-req'] = i('x-req')[0].string
                        except:
                            koding.dolog("Regex: -- No x-req --",line_info=True)
                        try:
                            regexs[i('name')[0].string]['x-forward'] = i('x-forward')[0].string
                        except:
                            koding.dolog("Regex: -- No x-forward --",line_info=True)

                        try:
                            regexs[i('name')[0].string]['agent'] = i('agent')[0].string
                        except:
                            koding.dolog("Regex: -- No User Agent --",line_info=True)
                        try:
                            regexs[i('name')[0].string]['post'] = i('post')[0].string
                        except:
                            koding.dolog("Regex: -- Not a post",line_info=True)
                        try:
                            regexs[i('name')[0].string]['rawpost'] = i('rawpost')[0].string
                        except:
                            koding.dolog("Regex: -- Not a rawpost",line_info=True)
                        try:
                            regexs[i('name')[0].string]['htmlunescape'] = i('htmlunescape')[0].string
                        except:
                            koding.dolog("Regex: -- Not a htmlunescape",line_info=True)


                        try:
                            regexs[i('name')[0].string]['readcookieonly'] = i('readcookieonly')[0].string
                        except:
                            koding.dolog("Regex: -- Not a readCookieOnly",line_info=True)
                        #print i
                        try:
                            regexs[i('name')[0].string]['cookiejar'] = i('cookiejar')[0].string
                            if not regexs[i('name')[0].string]['cookiejar']:
                                regexs[i('name')[0].string]['cookiejar']=''
                        except:
                            koding.dolog("Regex: -- Not a cookieJar")							
                        try:
                            regexs[i('name')[0].string]['setcookie'] = i('setcookie')[0].string
                        except:
                            koding.dolog("Regex: -- Not a setcookie",line_info=True)
                        try:
                            regexs[i('name')[0].string]['appendcookie'] = i('appendcookie')[0].string
                        except:
                            koding.dolog("Regex: -- Not a appendcookie",line_info=True)
                                                    
                        try:
                            regexs[i('name')[0].string]['ignorecache'] = i('ignorecache')[0].string
                        except:
                            koding.dolog("Regex: -- no ignorecache",line_info=True)
                        #try:
                        #    regexs[i('name')[0].string]['ignorecache'] = i('ignorecache')[0].string
                        #except:
                        #    koding.dolog("Regex: -- no ignorecache")			

                    regexs = urllib.quote(repr(regexs))
                    return regexs
                    #print regexs
                except:
                    regexs = None
                    koding.dolog('regex Error: '+name.encode('utf-8', 'ignore'),line_info=True)
#copies from lamda's implementation
def get_ustream(url):
    try:
        for i in range(1, 51):
            result = getUrl(url)
            if "EXT-X-STREAM-INF" in result: return url
            if not "EXTM3U" in result: return
            xbmc.sleep(2000)
        return
    except:
        return
        
 
def getRegexParsed(regexs, url,cookieJar=None,forCookieJarOnly=False,recursiveCall=False,cachedPages={}, rawPost=False, cookie_jar_file=None):#0,1,2 = URL, regexOnly, CookieJarOnly
        if not recursiveCall:
            regexs = eval(urllib.unquote(regexs))
        #cachedPages = {}
        doRegexs = re.compile('\$doregex\[([^\]]*)\]').findall(url)
        setresolved=True
        for k in doRegexs:
            if k in regexs:
                #print 'processing ' ,k
                m = regexs[k]
                #print m
                cookieJarParam=False
                if  'cookiejar' in m: # so either create or reuse existing jar
                    cookieJarParam=m['cookiejar']
                    if  '$doregex' in cookieJarParam:
                        cookieJar=getRegexParsed(regexs, m['cookiejar'],cookieJar,True, True,cachedPages)
                        cookieJarParam=True
                    else:
                        cookieJarParam=True
                if cookieJarParam:
                    if cookieJar==None:
                        cookie_jar_file=None
                        if 'open[' in m['cookiejar']:
                            cookie_jar_file=m['cookiejar'].split('open[')[1].split(']')[0]
                        cookieJar=getCookieJar(cookie_jar_file)
                        if cookie_jar_file:
                            saveCookieJar(cookieJar,cookie_jar_file)
                    elif 'save[' in m['cookiejar']:
                        cookie_jar_file=m['cookiejar'].split('save[')[1].split(']')[0]
                        complete_path=join(profile,cookie_jar_file)
                        print 'complete_path',complete_path
                        saveCookieJar(cookieJar,cookie_jar_file)
                if  m['page'] and '$doregex' in m['page']:
                    m['page']=getRegexParsed(regexs, m['page'],cookieJar,recursiveCall=True,cachedPages=cachedPages)

                if 'setcookie' in m and m['setcookie'] and '$doregex' in m['setcookie']:
                    m['setcookie']=getRegexParsed(regexs, m['setcookie'],cookieJar,recursiveCall=True,cachedPages=cachedPages)
                if 'appendcookie' in m and m['appendcookie'] and '$doregex' in m['appendcookie']:
                    m['appendcookie']=getRegexParsed(regexs, m['appendcookie'],cookieJar,recursiveCall=True,cachedPages=cachedPages)
                if  'post' in m and '$doregex' in m['post']:
                    m['post']=getRegexParsed(regexs, m['post'],cookieJar,recursiveCall=True,cachedPages=cachedPages)
                if  'rawpost' in m and '$doregex' in m['rawpost']:
                    m['rawpost']=getRegexParsed(regexs, m['rawpost'],cookieJar,recursiveCall=True,cachedPages=cachedPages,rawPost=True)
                if 'rawpost' in m and '$epoctime$' in m['rawpost']:
                    m['rawpost']=m['rawpost'].replace('$epoctime$',getEpocTime())
                if 'rawpost' in m and '$epoctime2$' in m['rawpost']:
                    m['rawpost']=m['rawpost'].replace('$epoctime2$',getEpocTime2())
                link=''
                if m['page'] and m['page'] in cachedPages and not 'ignorecache' in m and forCookieJarOnly==False :
                    link = cachedPages[m['page']]
                else:
                    if m['page'] and  not m['page']=='' and  m['page'].startswith('http'):
                        if '$epoctime$' in m['page']:
                            m['page']=m['page'].replace('$epoctime$',getEpocTime())
                        if '$epoctime2$' in m['page']:
                            m['page']=m['page'].replace('$epoctime2$',getEpocTime2())
                        page_split=m['page'].split('|')
                        pageUrl=page_split[0]
                        header_in_page=None
                        if len(page_split)>1:
                            header_in_page=page_split[1]
                        req = urllib2.Request(pageUrl)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
                        if 'refer' in m:
                            req.add_header('Referer', m['refer'])
                        if 'agent' in m:
                            req.add_header('User-agent', m['agent'])
                        if 'x-req' in m:
                            req.add_header('X-Requested-With', m['x-req'])
                        if 'x-forward' in m:
                            req.add_header('X-Forwarded-For', m['x-forward'])
                        if 'setcookie' in m:
                            req.add_header('Cookie', m['setcookie'])
                        if 'appendcookie' in m:
                            cookiestoApend=m['appendcookie']
                            cookiestoApend=cookiestoApend.split(';')
                            for h in cookiestoApend:
                                n,v=h.split('=')
                                w,n= n.split(':')
                                ck = cookielib.Cookie(version=0, name=n, value=v, port=None, port_specified=False, domain=w, domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
                                cookieJar.set_cookie(ck)  
                        if 'origin' in m:
                            req.add_header('Origin', m['origin'])
                        if header_in_page:
                            header_in_page=header_in_page.split('&')
                            for h in header_in_page:
                                n,v=h.split('=')
                                req.add_header(n,v)
                        if not cookieJar==None:
                            cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
                            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
                            opener = urllib2.install_opener(opener)
                            if 'noredirect' in m:
                                opener2 = urllib2.build_opener(NoRedirection)
                                opener = urllib2.install_opener(opener2)      
                        if 'connection' in m:
                            print '..........................connection//////.',m['connection']
                            from keepalive import HTTPHandler
                            keepalive_handler = HTTPHandler()
                            opener = urllib2.build_opener(keepalive_handler)
                            urllib2.install_opener(opener)
                        post=None
                        if 'post' in m:
                            postData=m['post']
                            if '$LiveStreamRecaptcha' in postData:
                                (captcha_challenge,catpcha_word)=processRecaptcha(m['page'])
                                if captcha_challenge:
                                    postData+='recaptcha_challenge_field:'+captcha_challenge+',recaptcha_response_field:'+catpcha_word
                            splitpost=postData.split(',');
                            post={}
                            for p in splitpost:
                                n=p.split(':')[0];
                                v=p.split(':')[1];
                                post[n]=v
                            post = urllib.urlencode(post)
                        if 'rawpost' in m:
                            post=m['rawpost']
                            if '$LiveStreamRecaptcha' in post:
                                (captcha_challenge,catpcha_word)=processRecaptcha(m['page'])
                                if captcha_challenge:
                                   post+='&recaptcha_challenge_field='+captcha_challenge+'&recaptcha_response_field='+catpcha_word
                        if post:
                            response = urllib2.urlopen(req,post)
                        else:
                            response = urllib2.urlopen(req)

                        link = response.read()
                        link=javascriptUnEscape(link)
                        if 'includeheaders' in m:
                            link+=str(response.headers.get('Set-Cookie'))

                        response.close()
                        cachedPages[m['page']] = link
                        #print link
                        #print 'store link for',m['page'],forCookieJarOnly
                        
                        if forCookieJarOnly:
                            return cookieJar# do nothing
                    elif m['page'] and  not m['page'].startswith('http'):
                        if m['page'].startswith('$pyFunction:'):
                            val=doEval(m['page'].split('$pyFunction:')[1],'',cookieJar )
                            if forCookieJarOnly:
                                return cookieJar# do nothing
                            link=val
                        else:
                            link=m['page']
                if '$pyFunction:playmedia(' in m['expre'] or 'ActivateWindow'  in m['expre']   or  any(x in url for x in g_ignoreSetResolved):
                    setresolved=False
                if  '$doregex' in m['expre']:
                    m['expre']=getRegexParsed(regexs, m['expre'],cookieJar,recursiveCall=True,cachedPages=cachedPages)
                    
                
                if not m['expre']=='':
                    print 'doing it ',m['expre']
                    if '$LiveStreamCaptcha' in m['expre']:
                        val=askCaptcha(m,link,cookieJar)
                        #print 'url and val',url,val
                        url = url.replace("$doregex[" + k + "]", val)
                    elif m['expre'].startswith('$pyFunction:'):
                        val=doEval(m['expre'].split('$pyFunction:')[1],link,cookieJar )
                        if 'ActivateWindow' in m['expre']: return 
                        print 'still hre'
                        print 'url k val',url,k,val

                        url = url.replace("$doregex[" + k + "]", val)
                    else:
                        if not link=='':
                            reg = re.compile(m['expre']).search(link)
                            val=''
                            try:
                                val=reg.group(1).strip()
                            except: traceback.print_exc()
                        else:
                            val=m['expre']
                        if rawPost:
                            print 'rawpost'
                            val=urllib.quote_plus(val)
                        if 'htmlunescape' in m:
                            #val=urllib.unquote_plus(val)
                            import HTMLParser
                            val=HTMLParser.HTMLParser().unescape(val)                     
                        url = url.replace("$doregex[" + k + "]", val)
                        #return val
                else:           
                    url = url.replace("$doregex[" + k + "]",'')
        if '$epoctime$' in url:
            url=url.replace('$epoctime$',getEpocTime())
        if '$epoctime2$' in url:
            url=url.replace('$epoctime2$',getEpocTime2())

        if '$GUID$' in url:
            import uuid
            url=url.replace('$GUID$',str(uuid.uuid1()).upper())
        if '$get_cookies$' in url:
            url=url.replace('$get_cookies$',getCookiesString(cookieJar))   

        if recursiveCall: return url
        print 'final url',url
        if url=="": 
        	return
        else:
        	return url,setresolved

            
        
def getmd5(t):
    import hashlib
    h=hashlib.md5()
    h.update(t)
    return h.hexdigest()

def decrypt_vaughnlive(encrypted):
    retVal=""
    for val in encrypted.split(':'):
        retVal+=chr(int(val.replace("0m0",""))/84/5)
    return retVal

def playmedia(media_url):
    try:
        import  CustomPlayer
        player = CustomPlayer.MyXBMCPlayer()
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=media_url )
        player.play( media_url,listitem)
        xbmc.sleep(1000)
        while player.is_active:
            xbmc.sleep(200)
    except:
        traceback.print_exc()
    return ''
    
        
def get_saw_rtmp(page_value, referer=None):
    if referer:
        referer=[('Referer',referer)]
    if page_value.startswith("http"):
        page_url=page_value
        page_value= getUrl(page_value,headers=referer)

    str_pattern="(eval\(function\(p,a,c,k,e,(?:r|d).*)"

    reg_res=re.compile(str_pattern).findall(page_value)
    r=""
    if reg_res and len(reg_res)>0:
        for v in reg_res:
            r1=get_unpacked(v)
            r2=re_me(r1,'\'(.*?)\'')
            if 'unescape' in r1:
                r1=urllib.unquote(r2)
            r+=r1+'\n'
        print 'final value is ',r
        
        page_url=re_me(r,'src="(.*?)"')
        
        page_value= getUrl(page_url,headers=referer)

    #print page_value

    rtmp=re_me(page_value,'streamer\'.*?\'(.*?)\'\)')
    playpath=re_me(page_value,'file\',\s\'(.*?)\'')

    
    return rtmp+' playpath='+playpath +' pageUrl='+page_url
    
def get_leton_rtmp(page_value, referer=None):
    if referer:
        referer=[('Referer',referer)]
    if page_value.startswith("http"):
        page_value= getUrl(page_value,headers=referer)
    str_pattern="var a = (.*?);\s*var b = (.*?);\s*var c = (.*?);\s*var d = (.*?);\s*var f = (.*?);\s*var v_part = '(.*?)';"
    reg_res=re.compile(str_pattern).findall(page_value)[0] 

    a,b,c,d,f,v=(reg_res)
    f=int(f)
    a=int(a)/f
    b=int(b)/f
    c=int(c)/f
    d=int(d)/f

    ret= 'rtmp://' + str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d) + v;
    return ret

def createM3uForDash(url,useragent=None):
    str='#EXTM3U'
    str+='\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=361816'
    str+='\n'+url+'&bytes=0-200000'#+'|User-Agent='+useragent
    source_file = join(profile, 'testfile.m3u')
    str+='\n'
    SaveToFile(source_file,str)
    #return 'C:/Users/shani/Downloads/test.m3u8'
    return source_file

def SaveToFile(file_name,page_data,append=False):
    if append:
        f = open(file_name, 'a')
        f.write(page_data)
        f.close()        
    else:
        f=open(file_name,'wb')
        f.write(page_data)
        f.close()
        return ''
    
def LoadFile(file_name):
	f=open(file_name,'rb')
	d=f.read()
	f.close()
	return d
    
def get_packed_iphonetv_url(page_data):
	import re,base64,urllib; 
	s=page_data
	while 'geh(' in s:
		if s.startswith('lol('): s=s[5:-1]    
#		print 's is ',s
		s=re.compile('"(.*?)"').findall(s)[0]; 
		s=  base64.b64decode(s); 
		s=urllib.unquote(s); 
	print s
	return s

def get_ferrari_url(page_data):
    print 'get_dag_url2',page_data
    page_data2=getUrl(page_data);
    patt='(http.*)'
    import uuid
    playback=str(uuid.uuid1()).upper()
    links=re.compile(patt).findall(page_data2)
    headers=[('X-Playback-Session-Id',playback)]
    for l in links:
        try:
                page_datatemp=getUrl(l,headers=headers);
                    
        except: pass
    
    return page_data+'|&X-Playback-Session-Id='+playback

    
def get_dag_url(page_data):
    print 'get_dag_url',page_data
    if page_data.startswith('http://dag.total-stream.net'):
        headers=[('User-Agent','Verismo-BlackUI_(2.4.7.5.8.0.34)')]
        page_data=getUrl(page_data,headers=headers);

    if '127.0.0.1' in page_data:
        return revist_dag(page_data)
    elif re_me(page_data, 'wmsAuthSign%3D([^%&]+)') != '':
        final_url = re_me(page_data, '&ver_t=([^&]+)&') + '?wmsAuthSign=' + re_me(page_data, 'wmsAuthSign%3D([^%&]+)') + '==/mp4:' + re_me(page_data, '\\?y=([^&]+)&')
    else:
        final_url = re_me(page_data, 'href="([^"]+)"[^"]+$')
        if len(final_url)==0:
            final_url=page_data
    final_url = final_url.replace(' ', '%20')
    return final_url

def re_me(data, re_patten):
    match = ''
    m = re.search(re_patten, data)
    if m != None:
        match = m.group(1)
    else:
        match = ''
    return match

def revist_dag(page_data):
    final_url = ''
    if '127.0.0.1' in page_data:
        final_url = re_me(page_data, '&ver_t=([^&]+)&') + ' live=true timeout=15 playpath=' + re_me(page_data, '\\?y=([a-zA-Z0-9-_\\.@]+)')
        
    if re_me(page_data, 'token=([^&]+)&') != '':
        final_url = final_url + '?token=' + re_me(page_data, 'token=([^&]+)&')
    elif re_me(page_data, 'wmsAuthSign%3D([^%&]+)') != '':
        final_url = re_me(page_data, '&ver_t=([^&]+)&') + '?wmsAuthSign=' + re_me(page_data, 'wmsAuthSign%3D([^%&]+)') + '==/mp4:' + re_me(page_data, '\\?y=([^&]+)&')
    else:
        final_url = re_me(page_data, 'HREF="([^"]+)"')

    if 'dag1.asx' in final_url:
        return get_dag_url(final_url)

    if 'devinlivefs.fplive.net' not in final_url:
        final_url = final_url.replace('devinlive', 'flive')
    if 'permlivefs.fplive.net' not in final_url:
        final_url = final_url.replace('permlive', 'flive')
    return final_url


def get_unwise( str_eval):
    page_value=""
    try:        
        ss="w,i,s,e=("+str_eval+')' 
        exec (ss)
        page_value=unwise_func(w,i,s,e)
    except: traceback.print_exc(file=sys.stdout)
    #print 'unpacked',page_value
    return page_value
    
def unwise_func( w, i, s, e):
    lIll = 0;
    ll1I = 0;
    Il1l = 0;
    ll1l = [];
    l1lI = [];
    while True:
        if (lIll < 5):
            l1lI.append(w[lIll])
        elif (lIll < len(w)):
            ll1l.append(w[lIll]);
        lIll+=1;
        if (ll1I < 5):
            l1lI.append(i[ll1I])
        elif (ll1I < len(i)):
            ll1l.append(i[ll1I])
        ll1I+=1;
        if (Il1l < 5):
            l1lI.append(s[Il1l])
        elif (Il1l < len(s)):
            ll1l.append(s[Il1l]);
        Il1l+=1;
        if (len(w) + len(i) + len(s) + len(e) == len(ll1l) + len(l1lI) + len(e)):
            break;
        
    lI1l = ''.join(ll1l)#.join('');
    I1lI = ''.join(l1lI)#.join('');
    ll1I = 0;
    l1ll = [];
    for lIll in range(0,len(ll1l),2):
        #print 'array i',lIll,len(ll1l)
        ll11 = -1;
        if ( ord(I1lI[ll1I]) % 2):
            ll11 = 1;
        #print 'val is ', lI1l[lIll: lIll+2]
        l1ll.append(chr(    int(lI1l[lIll: lIll+2], 36) - ll11));
        ll1I+=1;
        if (ll1I >= len(l1lI)):
            ll1I = 0;
    ret=''.join(l1ll)
    if 'eval(function(w,i,s,e)' in ret:
        print 'STILL GOing'
        ret=re.compile('eval\(function\(w,i,s,e\).*}\((.*?)\)').findall(ret)[0] 
        return get_unwise(ret)
    else:
        print 'FINISHED'
        return ret
    
def get_unpacked( page_value, regex_for_text='', iterations=1, total_iteration=1):
    try:        
        reg_data=None
        if page_value.startswith("http"):
            page_value= getUrl(page_value)
        print 'page_value',page_value
        if regex_for_text and len(regex_for_text)>0:
            page_value=re.compile(regex_for_text).findall(page_value)[0] #get the js variable
        
        page_value=unpack(page_value,iterations,total_iteration)
    except: traceback.print_exc(file=sys.stdout)
    print 'unpacked',page_value
    if 'sav1live.tv' in page_value:
        page_value=page_value.replace('sav1live.tv','sawlive.tv') #quick fix some bug somewhere
        print 'sav1 unpacked',page_value
    return page_value

def unpack(sJavascript,iteration=1, totaliterations=2  ):
    print 'iteration',iteration
    if sJavascript.startswith('var _0xcb8a='):
        aSplit=sJavascript.split('var _0xcb8a=')
        ss="myarray="+aSplit[1].split("eval(")[0]
        exec(ss)
        a1=62
        c1=int(aSplit[1].split(",62,")[1].split(',')[0])
        p1=myarray[0]
        k1=myarray[3]
        with open('temp file'+str(iteration)+'.js', "wb") as filewriter:
            filewriter.write(str(k1))
        #aa=1/0
    else:

        aSplit = sJavascript.split("rn p}('")
        print aSplit
        
        p1,a1,c1,k1=('','0','0','')
     
        ss="p1,a1,c1,k1=('"+aSplit[1].split(".spli")[0]+')' 
        exec(ss)
    k1=k1.split('|')
    aSplit = aSplit[1].split("))'")
#    print ' p array is ',len(aSplit)
#   print len(aSplit )

    #p=str(aSplit[0]+'))')#.replace("\\","")#.replace('\\\\','\\')

    #print aSplit[1]
    #aSplit = aSplit[1].split(",")
    #print aSplit[0] 
    #a = int(aSplit[1])
    #c = int(aSplit[2])
    #k = aSplit[3].split(".")[0].replace("'", '').split('|')
    #a=int(a)
    #c=int(c)
    
    #p=p.replace('\\', '')
#    print 'p val is ',p[0:100],'............',p[-100:],len(p)
#    print 'p1 val is ',p1[0:100],'............',p1[-100:],len(p1)
    
    #print a,a1
    #print c,a1
    #print 'k val is ',k[-10:],len(k)
#    print 'k1 val is ',k1[-10:],len(k1)
    e = ''
    d = ''#32823

    #sUnpacked = str(__unpack(p, a, c, k, e, d))
    sUnpacked1 = str(__unpack(p1, a1, c1, k1, e, d,iteration))
    
    #print sUnpacked[:200]+'....'+sUnpacked[-100:], len(sUnpacked)
#    print sUnpacked1[:200]+'....'+sUnpacked1[-100:], len(sUnpacked1)
    
    #exec('sUnpacked1="'+sUnpacked1+'"')
    if iteration>=totaliterations:
#        print 'final res',sUnpacked1[:200]+'....'+sUnpacked1[-100:], len(sUnpacked1)
        return sUnpacked1#.replace('\\\\', '\\')
    else:
#        print 'final res for this iteration is',iteration
        return unpack(sUnpacked1,iteration+1)#.replace('\\', ''),iteration)#.replace('\\', '');#unpack(sUnpacked.replace('\\', ''))

def __unpack(p, a, c, k, e, d, iteration,v=1):

    #with open('before file'+str(iteration)+'.js', "wb") as filewriter:
    #    filewriter.write(str(p))
    while (c >= 1):
        c = c -1
        if (k[c]):
            aa=str(__itoaNew(c, a))
            if v==1:
                p=re.sub('\\b' + aa +'\\b', k[c], p)# THIS IS Bloody slow!
            else:
                p=findAndReplaceWord(p,aa,k[c])

            #p=findAndReplaceWord(p,aa,k[c])

            
    #with open('after file'+str(iteration)+'.js', "wb") as filewriter:
    #    filewriter.write(str(p))
    return p

#
#function equalavent to re.sub('\\b' + aa +'\\b', k[c], p)
def findAndReplaceWord(source_str, word_to_find,replace_with):
    splits=None
    splits=source_str.split(word_to_find)
    if len(splits)>1:
        new_string=[]
        current_index=0
        for current_split in splits:
            #print 'here',i
            new_string.append(current_split)
            val=word_to_find#by default assume it was wrong to split

            #if its first one and item is blank then check next item is valid or not
            if current_index==len(splits)-1:
                val='' # last one nothing to append normally
            else:
                if len(current_split)==0: #if blank check next one with current split value
                    if ( len(splits[current_index+1])==0 and word_to_find[0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_') or (len(splits[current_index+1])>0  and splits[current_index+1][0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_'):# first just just check next
                        val=replace_with
                #not blank, then check current endvalue and next first value
                else:
                    if (splits[current_index][-1].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_') and (( len(splits[current_index+1])==0 and word_to_find[0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_') or (len(splits[current_index+1])>0  and splits[current_index+1][0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_')):# first just just check next
                        val=replace_with
                        
            new_string.append(val)
            current_index+=1
        #aaaa=1/0
        source_str=''.join(new_string)
    return source_str        

def __itoa(num, radix):
#    print 'num red',num, radix
    result = ""
    if num==0: return '0'
    while num > 0:
        result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
        num /= radix
    return result
	
def __itoaNew(cc, a):
    aa="" if cc < a else __itoaNew(int(cc / a),a) 
    cc = (cc % a)
    bb=chr(cc + 29) if cc> 35 else str(__itoa(cc,36))
    return aa+bb


def getCookiesString(cookieJar):
    try:
        cookieString=""
        for index, cookie in enumerate(cookieJar):
            cookieString+=cookie.name + "=" + cookie.value +";"
    except: pass
    #print 'cookieString',cookieString
    return cookieString


def saveCookieJar(cookieJar,COOKIEFILE):
	try:
		complete_path=join(profile,COOKIEFILE)
		cookieJar.save(complete_path,ignore_discard=True)
	except: pass

def getCookieJar(COOKIEFILE):

	cookieJar=None
	if COOKIEFILE:
		try:
			complete_path=join(profile,COOKIEFILE)
			cookieJar = cookielib.LWPCookieJar()
			cookieJar.load(complete_path,ignore_discard=True)
		except: 
			cookieJar=None
	
	if not cookieJar:
		cookieJar = cookielib.LWPCookieJar()
	
	return cookieJar
    
def doEval(fun_call,page_data,Cookie_Jar):
    ret_val=''
    if functions_dir not in sys.path:
        sys.path.append(functions_dir)
    
    print fun_call
    try:
        py_file='import '+fun_call.split('.')[0]
        print py_file,sys.path
        exec( py_file)
        print 'done'
    except:
        print 'error in import'
        traceback.print_exc(file=sys.stdout)
    print 'ret_val='+fun_call
    exec ('ret_val='+fun_call)
    print ret_val
    #exec('ret_val=1+1')
    return str(ret_val)
    
def processRecaptcha(url):
	html_text=getUrl(url)
	recapChallenge=""
	solution=""
	cap_reg="<script.*?src=\"(.*?recap.*?)\""
	match =re.findall(cap_reg, html_text)
	captcha=False
	captcha_reload_response_chall=None
	solution=None
	
	if match and len(match)>0: #new shiny captcha!
		captcha_url=match[0]
		captcha=True
		
		cap_chall_reg='challenge.*?\'(.*?)\''
		cap_image_reg='\'(.*?)\''
		captcha_script=getUrl(captcha_url)
		recapChallenge=re.findall(cap_chall_reg, captcha_script)[0]
		captcha_reload='http://www.google.com/recaptcha/api/reload?c=';
		captcha_k=captcha_url.split('k=')[1]
		captcha_reload+=recapChallenge+'&k='+captcha_k+'&captcha_k=1&type=image&lang=en-GB'
		captcha_reload_js=getUrl(captcha_reload)
		captcha_reload_response_chall=re.findall(cap_image_reg, captcha_reload_js)[0]
		captcha_image_url='http://www.google.com/recaptcha/api/image?c='+captcha_reload_response_chall
		if not captcha_image_url.startswith("http"):
			captcha_image_url='http://www.google.com/recaptcha/api/'+captcha_image_url
		import random
		n=random.randrange(100,1000,5)
		local_captcha = join(profile,str(n) +"captcha.img" )
		localFile = open(local_captcha, "wb")
		localFile.write(getUrl(captcha_image_url))
		localFile.close()
		solver = InputWindow(captcha=local_captcha)
		solution = solver.get()
		os.remove(local_captcha)
	return captcha_reload_response_chall ,solution

def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None):


	cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
	opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
	#opener = urllib2.install_opener(opener)
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	if headers:
		for h,hv in headers:
			req.add_header(h,hv)

	response = opener.open(req,post,timeout=timeout)
	link=response.read()
	response.close()
	return link;

def get_decode(str,reg=None):
	if reg:
		str=re.findall(reg, str)[0]
	s1 = urllib.unquote(str[0: len(str)-1]);
	t = '';
	for i in range( len(s1)):
		t += chr(ord(s1[i]) - s1[len(s1)-1]);
	t=urllib.unquote(t)
	print t
	return t

def javascriptUnEscape(str):
	js=re.findall('unescape\(\'(.*?)\'',str)
	print 'js',js
	if (not js==None) and len(js)>0:
		for j in js:
			#print urllib.unquote(j)
			str=str.replace(j ,urllib.unquote(j))
	return str

iid=0
def askCaptcha(m,html_page, cookieJar):
    global iid
    iid+=1
    expre= m['expre']
    page_url = m['page']
    captcha_regex=re.compile('\$LiveStreamCaptcha\[([^\]]*)\]').findall(expre)[0]

    captcha_url=re.compile(captcha_regex).findall(html_page)[0]
    print expre,captcha_regex,captcha_url
    if not captcha_url.startswith("http"):
        page_='http://'+"".join(page_url.split('/')[2:3])
        if captcha_url.startswith("/"):
            captcha_url=page_+captcha_url
        else:
            captcha_url=page_+'/'+captcha_url
    
    local_captcha = join(profile, str(iid)+"captcha.jpg" )
    localFile = open(local_captcha, "wb")
    print ' c capurl',captcha_url
    req = urllib2.Request(captcha_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
    if 'refer' in m:
        req.add_header('Referer', m['refer'])
    if 'agent' in m:
        req.add_header('User-agent', m['agent'])
    if 'setcookie' in m:
        print 'adding cookie',m['setcookie']
        req.add_header('Cookie', m['setcookie'])
        
    #cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    #opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    urllib2.urlopen(req)
    response = urllib2.urlopen(req)

    localFile.write(response.read())
    response.close()
    localFile.close()
    solver = InputWindow(captcha=local_captcha)
    solution = solver.get()
    return solution
    
class InputWindow(xbmcgui.WindowDialog):
    def __init__(self, *args, **kwargs):
        self.cptloc = kwargs.get('captcha')
        self.img = xbmcgui.ControlImage(335,30,624,60,self.cptloc)
        self.addControl(self.img)
        self.kbd = xbmc.Keyboard()

    def get(self):
        self.show()
        time.sleep(2)        
        self.kbd.doModal()
        if (self.kbd.isConfirmed()):
            text = self.kbd.getText()
            self.close()
            return text
        self.close()
        return False
    
def getEpocTime():
    import time
    return str(int(time.time()*1000))

def getEpocTime2():
    import time
    return str(int(time.time()))

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                splitparams={}
                splitparams=pairsofparams[i].split('=')
                if (len(splitparams))==2:
                    param[splitparams[0]]=splitparams[1]
        return param


def getFavorites():
        items = json.loads(open(favorites).read())
        total = len(items)
        for i in items:
            name = i[0]
            url = i[1]
            iconimage = i[2]
            try:
                fanArt = i[3]
                if fanArt == None:
                    raise
            except:
                if setting('use_thumb') == "true":
                    fanArt = iconimage
                else:
                    fanArt = fanart
            try: playlist = i[5]
            except: playlist = None
            try: regexs = i[6]
            except: regexs = None

            if i[4] == 0:
                addLink(url,ItemColor(name),iconimage,fanArt,'','','','fav',playlist,regexs,total)
            else:
                addDir(ChannelColor(name),url,i[4],iconimage,fanart,'','','','','fav')


def addFavorite(name,url,iconimage,fanart,mode,playlist=None,regexs=None):
        favList = []
        if not os.path.exists(favorites + 'txt'):
            os.makedirs(favorites + 'txt')
        if not os.path.exists(history):
            os.makedirs(history)
        try:
            # seems that after
            name = name.encode('utf-8', 'ignore')
        except:
            pass
        if os.path.exists(favorites)==False:
            koding.dolog('Making Favorites File',line_info=True)
            favList.append((name,url,iconimage,fanart,mode,playlist,regexs))
            a = open(favorites, "w")
            a.write(json.dumps(favList))
            a.close()
        else:
            koding.dolog('Appending Favorites',line_info=True)
            a = open(favorites).read()
            data = json.loads(a)
            data.append((name,url,iconimage,fanart,mode))
            b = open(favorites, "w")
            b.write(json.dumps(data))
            b.close()


def rmFavorite(name):
        data = json.loads(open(favorites).read())
        for index in range(len(data)):
            if data[index][0]==name:
                del data[index]
                b = open(favorites, "w")
                b.write(json.dumps(data))
                b.close()
                break
        xbmc.executebuiltin("XBMC.Container.Refresh")


def urlsolver(url):
    host = RESOLVE.HostedMediaFile(url)
    ValidUrl = host.valid_url()
    if ValidUrl == True :
        resolver = RESOLVE.resolve(url)
    elif ValidUrl == False:
        import genesisresolvers
        resolved=genesisresolvers.get(url).result
        if resolved :
            if isinstance(resolved,list):
                for k in resolved:
                    quality = setting('quality')
                    if k['quality'] == 'HD'  :
                        resolver = k['url']
                        break
                    elif k['quality'] == 'SD' :
                        resolver = k['url']
                    elif k['quality'] == '1080p' and setting('1080pquality') == 'true' :
                        resolver = k['url']
                        break
            else:
                resolver = resolved
    return resolver

def play_playlist(name, mu_playlist):
        import urlparse
        if setting('ask_playlist_items') == 'true':
            names = []
            for i in mu_playlist:
                d_name=urlparse.urlparse(i).netloc
                if d_name == '':
                    names.append(name)
                else:
                    names.append(d_name)
            dialog = xbmcgui.Diakoding.dolog()
            index = dialog.select('Choose a video source', names)
            if index >= 0:
                if "&mode=19" in mu_playlist[index]:
                    xbmc.Player().play(urlsolver(mu_playlist[index].replace('&mode=19','')))
                elif "$doregex" in mu_playlist[index] :

                    sepate = mu_playlist[index].split('&regexs=')

                    url,setresolved = getRegexParsed(sepate[1], sepate[0])
                    xbmc.Player().play(url)
                else:
                    url = mu_playlist[index]
                    xbmc.Player().play(url)
        else:
            playlist = xbmc.PlayList(1) # 1 means video
            playlist.clear()
            item = 0
            for i in mu_playlist:
                item += 1
                info = xbmcgui.ListItem('%s) %s' %(str(item),name))
                playlist.add(i, info)
                xbmc.executebuiltin('playlist.playoffset(video,0)')


def download_file(name, url):
        if setting('save_location') == "":
            xbmc.executebuiltin("XBMC.Notification('%s','Choose a location to save files.',15000,"+addon_icon+")"%addon_name)
            addon.openSettings()
        params = {'url': url, 'download_path': setting('save_location')}
        downloader.download(name, params)
        diakoding.dolog = xbmcgui.Dialog()
        ret = dialog.yesno('%s'%addon_name, 'Do you want to add this file as a source?')
        if ret:
            addSource(join(setting('save_location'), name))


def addDir(name,url,mode,iconimage,fanart,description,genre,date,credits,showcontext=False):
        
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        if date == '':
            date = None
        else:
            description += '\n\nDate: %s' %date
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Genre": genre, "dateadded": date, "credits": credits })
        liz.setProperty("Fanart_Image", fanart)
        if showcontext:
            contextMenu = []
            if showcontext == 'source':
                if name in str(SOURCES):
                    contextMenu.append(('Remove from Sources','XBMC.RunPlugin(%s?mode=8&name=%s)' %(sys.argv[0], urllib.quote_plus(name))))
            elif showcontext == 'download':
                contextMenu.append(('Download','XBMC.RunPlugin(%s?url=%s&mode=9&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
            elif showcontext == 'fav':
                contextMenu.append(('Remove from Add-on Favorites','XBMC.RunPlugin(%s?mode=6&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(name))))
									
            if not name in FAV:
                contextMenu.append(('Add to Add-on Favorites','XBMC.RunPlugin(%s?mode=5&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(fanart), mode)))
            liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)

        return ok
def ytdl_download(url,title,media_type='video'):
    # play in xbmc while playing go back to contextMenu(c) to "!!Download!!"
    # Trial yasceen: seperate |User-Agent=
    import youtubedl
    if not url == '':
        if media_type== 'audio':
            youtubedl.single_YD(url,download=True,audio=True)
        else:
            youtubedl.single_YD(url,download=True)   
    elif xbmc.Player().isPlaying() == True :
        import YDStreamExtractor
        if YDStreamExtractor.isDownloading() == True:

            YDStreamExtractor.manageDownloads()
        else:
            xbmc_url = xbmc.Player().getPlayingFile()

            xbmc_url = xbmc_url.split('|User-Agent=')[0]
            info = {'url':xbmc_url,'title':title,'media_type':media_type}
            youtubedl.single_YD('',download=True,dl_info=info)    
    else:
        xbmc.executebuiltin("XBMC.Notification(DOWNLOAD,First Play [COLOR yellow]WHILE playing download[/COLOR] ,10000)")
 
def search(site_name,search_term=None):
    thumbnail=''
    if os.path.exists(addon_history) == False or setting('clearseachhistory')=='true':
        SaveToFile(addon_history,'')
        addon.setSetting("clearseachhistory","false")
    if site_name == 'history' :
        content = LoadFile(addon_history)
        match = re.compile('(.+?):(.*?)(?:\r|\n)').findall(content)

        for name,search_term in match:
            if 'plugin://' in search_term:
                addLink(search_term, name,thumbnail,'','','','','',None,'',total=int(len(match)))
            else:
                addDir(name+':'+search_term,name,26,icon,addon_fanart,'','','','')
    if not search_term:    
        keyboard = xbmc.Keyboard('','Enter Search Term')
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
            return
        search_term = keyboard.getText()
        if len(search_term) == 0:
            return        
    search_term = search_term.replace(' ','+')
    search_term = search_term.encode('utf-8')
    koding.dolog('site_name= %s search_term= %s'%(site_name,search_term),line_info=True)
    if 'youtube' in site_name:
        koding.dolog('search_term=%s site_name=%s'%(search_term,site_name),line_info=True)
        from libs import YouTube
        YouTubesearch(search_term)
        page_data = site_name +':'+ search_term + '\n'
        SaveToFile(join(profile,'history'),page_data,append=True)
    elif 'dmotion' in site_name:
        urlMain = "https://api.dailymotion.com" 
        import _DMsearch
        familyFilter = str(setting('familyFilter'))
        _DMsearch.listVideos(urlMain+"/videos?fields=description,duration,id,owner.username,taken_time,thumbnail_large_url,title,views_total&search="+search_term+"&sort=relevance&limit=100&family_filter="+familyFilter+"&localization=en_EN&page=1")
    
        page_data = site_name +':'+ search_term+ '\n'
        SaveToFile(join(profile,'history'),page_data,append=True)        
    elif 'IMDBidplay' in site_name:
        urlMain = "http://www.omdbapi.com/?t=" 
        url= urlMain+search_term

        headers = dict({'User-Agent':'Mozilla/5.0 (Windows NT 6.3; rv:33.0) Gecko/20100101 Firefox/33.0','Referer': 'http://joker.org/','Accept-Encoding':'gzip, deflate','Content-Type': 'application/json;charset=utf-8','Accept': 'application/json, text/plain, */*'})
    
        r=requests.get(url,headers=headers)
        data = r.json()
        res = data['Response']
        if res == 'True':
            imdbID = data['imdbID']
            name= data['Title'] + data['Released']
            dialog = xbmcgui.Diakoding.dolog()
            ret = dialog.yesno('Check Movie Title', 'PLAY :: %s ?'%name)
            if ret:
                url = 'plugin://plugin.video.pulsar/movie/'+imdbID+'/play'
                page_data = name +':'+ url+ '\n'
                SaveToFile(history,page_data,append=True)
                return url
        else:
            xbmc.executebuiltin("XBMC.Notification(%s,No IMDB match found ,7000,%s)"%(addon_name,icon))
## Lunatixz PseudoTV feature
def ascii(string):
    if isinstance(string, basestring):
        if isinstance(string, unicode):
           string = string.encode('ascii', 'ignore')
    return string
def uni(string, encoding = 'utf-8'):
    if isinstance(string, basestring):
        if not isinstance(string, unicode):
            string = unicode(string, encoding, 'ignore')
    return string
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def sendJSON( command):
    data = ''
    try:
        data = xbmc.executeJSONRPC(uni(command))
    except UnicodeEncodeError:
        data = xbmc.executeJSONRPC(ascii(command))

    return uni(data)

#hakamac thanks Roman_V_M
def SetViewThumbnail():
    skin_used = xbmc.getSkinDir()
    if skin_used == 'skin.confluence':
        xbmc.executebuiltin('Container.SetViewMode(500)')
    elif skin_used == 'skin.aeon.nox':
        xbmc.executebuiltin('Container.SetViewMode(511)') 
    else:
        xbmc.executebuiltin('Container.SetViewMode(500)')
	
	
def pluginquerybyJSON(url):
    json_query = uni('{"jsonrpc":"2.0","method":"Files.GetDirectory","params":{"directory":"%s","media":"video","properties":["thumbnail","title","year","dateadded","fanart","rating","season","episode","studio"]},"id":1}') %url

    json_folder_detail = json.loads(sendJSON(json_query))
    for i in json_folder_detail['result']['files'] :
        url = i['file']
        name = removeNonAscii(i['label'])
        thumbnail = removeNonAscii(i['thumbnail'])
        try:
            fanart = removeNonAscii(i['fanart'])
        except Exception:
            fanart = ''
        try:
            date = i['year']
        except Exception:
            date = ''
        try:
            episode = i['episode']
            season = i['season']
            if episode == -1 or season == -1:
                description = ''
            else:
                description = '[COLOR yellow] S' + str(season)+'[/COLOR][COLOR hotpink] E' + str(episode) +'[/COLOR]'
        except Exception:
            description = ''
        try:
            studio = i['studio']
            if studio:
                description += '\n Studio:[COLOR steelblue] ' + studio[0] + '[/COLOR]'
        except Exception:
            studio = ''

        if i['filetype'] == 'file':
            addLink(url,name,thumbnail,fanart,description,'',date,'',None,'',total=len(json_folder_detail['result']['files']))
            #xbmc.executebuiltin("Container.SetViewMode(500)")

        else:
            addDir(name,url,53,thumbnail,fanart,description,'',date,'')
            #xbmc.executebuiltin("Container.SetViewMode(500)")

def addLink(url,name,iconimage,fanart,description,genre,date,showcontext,playlist,regexs,total,setCookie=""):
        #print 'url,name',url,name
        contextMenu =[]
        try:
            name = name.encode('utf-8')
        except: pass
        ok = True
        host = RESOLVE.HostedMediaFile(url)
        if regexs: 
            mode = '17'
           
            contextMenu.append((SingleColor(string=local_string(30082),color=_Edit.DialogBoxColor2),'XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))           
        elif  any(x in url for x in resolve_url) or host  and  url.startswith('http'):
            mode = '19'
          
            contextMenu.append((SingleColor(string=local_string(30082),color=_Edit.DialogBoxColor2),'XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
            contextMenu.append((SingleColor(string=local_string(30081),color=_Edit.DialogBoxColor2),'XBMC.RunPlugin({}?mode=106)'.format(sys.argv[0])))           
        elif url.endswith('&mode=18'):
            url=url.replace('&mode=18','')
            mode = '18' 
          
            contextMenu.append((SingleColor(string=local_string(30082),color=_Edit.DialogBoxColor2),'XBMC.RunPlugin(%s?url=%s&mode=23&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name)))) 
            if setting('dlaudioonly') == 'true':
                contextMenu.append(('Download [COLOR seablue]Audio[/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=24&name=%s)'
                                        %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))                                     
        elif url.startswith('magnet:?xt=') or '.torrent' in url:
          
            if '&' in url and not '&amp;' in url :
                url = url.replace('&','&amp;')
            url = 'plugin://plugin.video.pulsar/play?uri=' + url
            mode = '12'           
        else: 
            mode = '12'
      
            contextMenu.append((SingleColor(string=local_string(30082),color=_Edit.DialogBoxColor2),'XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))           
        u=sys.argv[0]+"?"
        play_list = False
      
        if playlist:
            if setting('add_playlist') == "false":
                u += "url="+urllib.quote_plus(url)+"&mode="+mode
            else:
                u += "mode=13&name=%s&playlist=%s" %(urllib.quote_plus(name), urllib.quote_plus(str(playlist).replace(',','||')))
                name = name + '[COLOR magenta] (' + str(len(playlist)) + ' items )[/COLOR]'
                play_list = True
        else:
            u += "url="+urllib.quote_plus(url)+"&mode="+mode
        if regexs:
            u += "&regexs="+regexs
        if not setCookie == '':
            u += "&setCookie="+urllib.quote_plus(setCookie)
  
        if date == '':
            date = None
        else:
            description += '\n\nDate: %s' %date
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Genre": genre, "dateadded": date })
        liz.setProperty("Fanart_Image", fanart)
        
        if (not play_list) and not any(x in url for x in g_ignoreSetResolved):#  (not url.startswith('plugin://plugin.video.f4mTester')):
            if regexs:
                if '$pyFunction:playmedia(' not in urllib.unquote_plus(regexs) and 'notplayable' not in urllib.unquote_plus(regexs)  :
                    #print 'setting isplayable',url, urllib.unquote_plus(regexs),url
                    liz.setProperty('IsPlayable', 'true')
            else:
                liz.setProperty('IsPlayable', 'true')
        else:
            koding.dolog( 'NOT setting isplayable'+url,line_info=True)
       
        if showcontext:
            #contextMenu = []
            if showcontext == 'fav':
                contextMenu.append(
                    ('Remove from Add-on Favorites','XBMC.RunPlugin(%s?mode=6&name=%s)'
                     %(sys.argv[0], urllib.quote_plus(name)))
                     )
            elif not name in FAV:
                fav_params = (
                    '%s?mode=5&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=0'
                    %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(fanart))
                    )
                if playlist:
                    fav_params += 'playlist='+urllib.quote_plus(str(playlist).replace(',','||'))
                if regexs:
                    fav_params += "&regexs="+regexs
                contextMenu.append(('Add to Add-on Favorites','XBMC.RunPlugin(%s)' %fav_params))
            liz.addContextMenuItems(contextMenu)
       
        if not playlist is None:
            if setting('add_playlist') == "false":
                playlist_name = name.split(') ')[1]
                contextMenu_ = [
                    ('Play '+playlist_name+' PlayList','XBMC.RunPlugin(%s?mode=13&name=%s&playlist=%s)'
                     %(sys.argv[0], urllib.quote_plus(playlist_name), urllib.quote_plus(str(playlist).replace(',','||'))))
                     ]
                liz.addContextMenuItems(contextMenu_)
        #print 'adding',name
 #       print url,totalitems
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,totalItems=total)
        #print 'added',name
        return ok

def playsetresolved(url,name,iconimage,setresolved=True):
    if setresolved:
        koding.dolog(url,line_info=True)
        liz = xbmcgui.ListItem(name, iconImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':name})
        liz.setProperty("IsPlayable","true")
        liz.setPath(str(url))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    else:
        koding.dolog('playsetresolved not setresolved',line_info=True)
        xbmc.executebuiltin('XBMC.RunPlugin('+url+')')      


## Thanks to daschacka, an epg scraper for http://i.teleboy.ch/programm/station_select.php
##  http://forum.xbmc.org/post.php?p=936228&postcount=1076
def getepg(link):
        url=urllib.urlopen(link)
        source=url.read()
        url.close()
        source2 = source.split("Jetzt")
        source3 = source2[1].split('programm/detail.php?const_id=')
        sourceuhrzeit = source3[1].split('<br /><a href="/')
        nowtime = sourceuhrzeit[0][40:len(sourceuhrzeit[0])]
        sourcetitle = source3[2].split("</a></p></div>")
        nowtitle = sourcetitle[0][17:len(sourcetitle[0])]
        nowtitle = nowtitle.encode('utf-8')
        return "  - "+nowtitle+" - "+nowtime


def get_epg(url, regex):
        data = makeRequest(url)
        try:
            item = re.findall(regex, data)[0]
            return item
        except:
            koding.dolog('regex failed')
            koding.dolog(regex)
            return




xbmcplugin.setContent(int(sys.argv[1]), 'movies')

try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)
except:
    pass

params=get_params()

url=None
name=None
mode=None
playlist=None
iconimage=None
fanart=addon_fanart
playlist=None
fav_mode=None
regexs=None

try:
    url=urllib.unquote_plus(params["url"]).decode('utf-8')
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    iconimage=urllib.unquote_plus(params["iconimage"])
except:
    pass
try:
    fanart=urllib.unquote_plus(params["fanart"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass
try:
    playlist=eval(urllib.unquote_plus(params["playlist"]).replace('||',','))
except:
    pass
try:
    fav_mode=int(params["fav_mode"])
except:
    pass
try:
    regexs=params["regexs"]
except:
    pass

koding.dolog("Mode: "+str(mode),line_info=True)
if not url is None:
    koding.dolog("URL: "+str(url.encode('utf-8')),line_info=True)
koding.dolog("Name: "+str(name),line_info=True)

if mode==None:
    koding.dolog("Index",line_info=False)
    SKindex()

elif mode==00:
    koding.dolog('Info line',line_info=True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))	

elif mode==1:
    koding.dolog("getData",line_info=True)
    getData(url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==2:
    koding.dolog("getChannelItems",line_info=True)
    getChannelItems(name,url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==3:
    koding.dolog("getSubChannelItems",line_info=True)
    getSubChannelItems(name,url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==4:
    koding.dolog("getFavorites",line_info=True)
    getFavorites()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==5:
    koding.dolog("addFavorite")
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    addFavorite(name,url,iconimage,fanart,fav_mode)

elif mode==6:
    koding.dolog("rmFavorite")
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    rmFavorite(name)

elif mode==7:
    koding.dolog("addSource")
    addSource(url)

elif mode==8:
    koding.dolog("rmSource")
    rmSource(name)

elif mode==9:
    koding.dolog("download_file")
    download_file(name, url)

elif mode==10:
    koding.dolog("getCommunitySources")
    getCommunitySources()

elif mode==11:
    koding.dolog("addSource",line_info=True)
    addSource(url)

elif mode==12:
    koding.dolog("setResolvedUrl",line_info=True)
    if not url.startswith('plugin://plugin') or not any(x in url for x in g_ignoreSetResolved):
        koding.dolog(url,line_info=True)
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    else:
        koding.dolog('Not setting setResolvedUrl',line_info=True)
        xbmc.executebuiltin('XBMC.RunPlugin('+url+')')


elif mode==13:
    koding.dolog("play_playlist")
    play_playlist(name, playlist)

elif mode==14:
    koding.dolog("get_xml_database")
    get_xml_database(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==15:
    koding.dolog("browse_xml_database")
    get_xml_database(url, True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==16:
    koding.dolog("browse_community")
    getCommunitySources(True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==17:
    koding.dolog("getRegexParsed")
    url,setresolved = getRegexParsed(regexs, url)
    if url:
        playsetresolved(url,name,iconimage,setresolved)
    else:
        xbmc.executebuiltin("XBMC.Notification(%s ,Failed to extract regex. - "+"this"+",4000,"+icon+")"%addon_name)
elif mode==18:
    koding.dolog("youtubedl")
    try:
        import youtubedl
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(%s,Please [COLOR yellow]install the Youtube Addon[/COLOR] module ,10000,"")"%(addon_name))
    stream_url=youtubedl.single_YD(url)
    playsetresolved(stream_url,name,iconimage)
elif mode==19:
	koding.dolog("Genesiscommonresolvers",line_info=True)
	playsetresolved (urlsolver(url),name,iconimage,True)	

elif mode==20:
    koding.dolog('Search all channels')
    SearchChannels()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==21:
    koding.dolog("download current file using youtube-dl service",line_info=True)
    ytdl_download('',name,'video')
elif mode==23:
    koding.dolog("get info then download",line_info=True)
    ytdl_download(url,name,'video') 
elif mode==24:
    koding.dolog("Audio only youtube download",line_info=True)
    ytdl_download(url,name,'audio')
elif mode==25:
    koding.dolog("YouTube/DMotion",line_info=True)
    search(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==26:
    koding.dolog("YouTube/DMotion From Search History",line_info=True)
    name = name.split(':')
    search(url,search_term=name[1])
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==27:
    koding.dolog("Using IMDB id to play in Pulsar",line_info=True)
    pulsarIMDB=search(url)
    xbmc.Player().play(pulsarIMDB)

elif mode==28:
    koding.dolog('YouTube Channel Index',line_info=True)
    from libs import YouTube
    YouTube.indexs(name,url,iconimage,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1])) 

elif mode==29:
    koding.dolog('YouTube channel Videos',line_info=True)
    from libs import YouTube
    YouTube.videos(url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1])) 

elif mode==30:
    koding.dolog('Getting Sublinks',line_info=True)
    GetSublinks(name,url,iconimage,fanart)

elif mode==31:
    koding.dolog('YouTube channel PlayLists',line_info=True)
    from libs import YouTube
    YouTube.playlist_lists(url,iconimage,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1])) 

elif mode==32:
    koding.dolog('YouTube channel Search',line_info=True)
    from libs import YouTube
    YouTube.channel_search(url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1])) 

elif mode==33:
    koding.dolog('Playing YouTube link {}'.format(url),line_info=True)
    from libs import YouTube
    YouTube.play(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1])) 

elif mode==34:
    koding.dolog('YouTube Channel PlayList Videos',line_info=True)
    from libs import YouTube
    YouTube.playlist_video(url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1])) 

elif mode==35:
    koding.dolog('search youtube search_term= {}'.format(url),line_info=True)
    if url == '':
        search(site_name='youtube')
    else:
        search(site_name='youtube',search_term=url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==36:
    koding.dolog('Tools Index',line_info=True)
    from libs import tools
    tools.index(iconimage,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==37:
    koding.dolog('getData with passcode',line_info=True)
    code =  BYB.KeyBoardNumeric(Type=0,msg='Enter PassCode')
    if code == setting('passcodetoenter'):
        getData(url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
elif mode==40:
    koding.dolog('SearchChannels')
    SearchChannels()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
elif mode==53:
    koding.dolog("Requesting JSON-RPC Items",line_info=True)
    pluginquerybyJSON(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==100:
    koding.dolog('Opening Settings',line_info=True)
    xbmcaddon.Addon().openSettings()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==101:
    koding.dolog('Clearing Cookies',line_info=True)
    from libs import tools
    tools.clear_cookies()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==102:
    koding.dolog('Opening Dependencies Settings Menu',line_info=True)
    from libs import tools
    tools.Dependency_OpenSettings()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==103:
    koding.dolog('Opening Dependencies Settings Menu',line_info=True)
    from libs import tools
    tools.Dependency_OpenSetting(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==104:
    koding.dolog('Opening Kodi Log',line_info=True)
    from libs import tools
    tools.kodilog()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==105:
    koding.dolog('Clearing Cache DB',line_info=True)
    from libs import tools
    tools.clear_cache()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==106:
    koding.dolog('Open Pairing Tool',line_info=True)
    BYB.PairTool(headercolor=[_Edit.DialogBoxColor1],itemcolor=[_Edit.DialogBoxColor2])
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==201:
    koding.dolog('Adding podcast episodes',line_info=True)
    from libs import podcast
    podcast.AddEpisodes(url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


elif mode==300:
    koding.dolog('My TMDB Data',line_info=True)
    from libs import mytmdb
    mytmdb.index(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==303:
    from libs import mytmdb
    mytmdb.MyLists(name,url)
    koding.dolog('My TMDB Data: '+str(name),line_info=True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==400:
    koding.dolog('Search Addon',line_info=True)
    from libs import search
    search.index(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==401:
    koding.dolog('Search TV Shows',line_info=True)
    from libs import search
    search.SearchTv(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==402:
    koding.dolog('Search Movies',line_info=True)
    from libs import search
    search.SearchMovie(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


elif mode==404:
    koding.dolog('Search Addon txt files',line_info=True)
    SearchChannels(Searchkey=url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==500:
    koding.dolog('tmdb lists',line_info=True)
    from libs import tmdatabase
    tmdatabase.tmdb_list(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==501:
    koding.dolog('tmdb lists tv seasons list',line_info=True)
    from libs import tmdatabase
    tmdatabase.tmdb_seasons(url,fanart,iconimage)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==502:
    koding.dolog('tmdb lists tv season episode list',line_info=True)
    from libs import tmdatabase
    tmdatabase.tmdb_season_episodes(fanart,url,iconimage)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==600:
    from libs import uniscrape
    uniscraper = uniscrape.uniscraper(iconimage=iconimage)
    uniscraper.Run(str(name),url,fanart)
    koding.dolog('UniSearch= {} iconimage= {} Fanart= {}'.format(uniscraper.NameClean(name),iconimage,fanart),line_info=True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==900:
    koding.dolog('scraper example',line_info=True)
    from libs import scraper_example
    scraper_example.index()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==901:
    koding.dolog('Scraper example retroclassic',line_info=True)
    from libs import scraper_example
    scraper_example.retroclassic()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==902:
    koding.dolog('Scraper example play',line_info=True)
    from libs import scraper_example
    scraper_example.Play(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==1000:
    koding.dolog('Dev Test Mode',line_info=True)
    xbmc.executebuiltin('RunScript(script.module.swiftstreamz)')
    #xbmcplugin.endOfDirectory(int(sys.argv[1]))
