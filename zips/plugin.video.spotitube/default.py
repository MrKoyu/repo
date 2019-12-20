# -*- coding: utf-8 -*-

import sys
import os
import re
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY2:
	from urllib import quote, unquote, quote_plus, unquote_plus, urlencode  # Python 2.X
	from urllib2 import build_opener, HTTPCookieProcessor, Request, urlopen  # Python 2.X
	from cookielib import LWPCookieJar  # Python 2.X
	from urlparse import urljoin, urlparse, urlunparse  # Python 2.X
elif PY3:
	from urllib.parse import quote, unquote, quote_plus, unquote_plus, urlencode, urljoin, urlparse, urlunparse  # Python 3+
	from urllib.request import build_opener, HTTPCookieProcessor, Request, urlopen  # Python 3+
	from http.cookiejar import LWPCookieJar  # Python 3+
import json
import xbmcvfs
import shutil
import socket
import time
import datetime
import random
import io
import gzip
import ssl

try: _create_unverified_https_context = ssl._create_unverified_context
except AttributeError: pass
else: ssl._create_default_https_context = _create_unverified_https_context


global debuging
pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon()
socket.setdefaulttimeout(40)
addonPath = xbmc.translatePath(addon.getAddonInfo('path')).encode('utf-8').decode('utf-8')
dataPath = xbmc.translatePath(addon.getAddonInfo('profile')).encode('utf-8').decode('utf-8')
region = xbmc.getLanguage(xbmc.ISO_639_1, region=True).split("-")[1]
icon = os.path.join(addonPath, 'icon.png')
defaultFanart = os.path.join(addonPath, 'fanart.jpg')
pic = os.path.join(addonPath, 'resources', 'media', '').encode('utf-8').decode('utf-8')
blackList = addon.getSetting("blacklist").split(',')
infoEnabled = addon.getSetting("showInfo") == "true"
infoType = addon.getSetting("infoType")
infoDelay = int(addon.getSetting("infoDelay"))
infoDuration = int(addon.getSetting("infoDuration"))
useThumbAsFanart = addon.getSetting("useThumbAsFanart") == 'true'
cachePath = xbmc.translatePath(os.path.join(addon.getSetting("cacheDir")))
cacheDays = int(addon.getSetting("cacheLong"))
deezerSearchDisplay = str(addon.getSetting("deezerSearch_count"))
deezerVideosDisplay = str(addon.getSetting("deezerVideos_count"))
itunesShowSubGenres = addon.getSetting("itunesShowSubGenres") == 'true'
itunesForceCountry = addon.getSetting("itunesForceCountry") == 'true'
itunesCountry = addon.getSetting("itunesCountry")
forceView = addon.getSetting("forceView") == 'true'
viewIDGenres = str(addon.getSetting("viewIDGenres"))
viewIDPlaylists = str(addon.getSetting("viewIDPlaylists"))
viewIDVideos = str(addon.getSetting("viewIDVideos"))
urlBaseBP = "https://www.beatport.com"
urlBaseBB = "https://www.billboard.com"
urlBaseDDP = "http://www.dj-playlist.de/"
urlBaseHypem = "https://hypem.com"
urlBaseOC = "http://www.officialcharts.com"
urlBaseSCC = "https://spotifycharts.com/"
#REtoken2 = "AIzaSyAdORXg7UZUo7sePv97JyoDqtQVi3Ll0b8"
#REtoken3 = "AIzaSyDDxfHuYTdjwAUnFPeFUgqGvJM8qqLpdGc"
token = "AIzaSyCIM4EzNqi1in22f4Z3Ru3iYvLaY8tc3bo"
xbmcplugin.setContent(int(sys.argv[1]), 'musicvideos')

if itunesForceCountry and itunesCountry:
	iTunesRegion = itunesCountry
else:
	iTunesRegion = region

if not os.path.isdir(dataPath):
	os.makedirs(dataPath)

if cachePath == "":
	addon.setSetting(id='cacheDir', value='special://profile/addon_data/'+addon.getAddonInfo('id')+'/cache')
elif cachePath != "" and not os.path.isdir(cachePath) and not cachePath.startswith(('smb://', 'nfs://', 'upnp://', 'ftp://')):
	os.mkdir(cachePath)
elif cachePath != "" and not os.path.isdir(cachePath) and cachePath.startswith(('smb://', 'nfs://', 'upnp://', 'ftp://')):
	addon.setSetting(id='cacheDir', value='special://profile/addon_data/'+addon.getAddonInfo('id')+'/cache') and os.mkdir(cachePath)
elif cachePath != "" and os.path.isdir(cachePath):
		xDays = cacheDays # Days after which Files would be deleted
		now = time.time() # Date and time now
		for root, dirs, files in os.walk(cachePath):
			for name in files:
				filename = os.path.join(root, name).encode('utf-8').decode('utf-8')
				try:
					if os.path.exists(filename):
						if os.path.getmtime(filename) < now - (60*60*24*xDays): # Check if CACHE-File exists and remove CACHE-File after defined xDays
							os.unlink(filename)
				except: pass

def py2_enc(s, encoding='utf-8'):
	if PY2 and isinstance(s, unicode):
		s = s.encode(encoding)
	return s

def py2_uni(s, encoding='utf-8'):
	if PY2 and isinstance(s, str):
		s = unicode(s, encoding)
	return s

def py3_dec(d, encoding='utf-8'):
	if PY3 and isinstance(d, bytes):
		d = d.decode(encoding)
	return d

def TitleCase(s):
	return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0)[0].upper()+mo.group(0)[1:].lower(), s)

def translation(id):
	LANGUAGE = addon.getLocalizedString(id)
	LANGUAGE = py2_enc(LANGUAGE)
	return LANGUAGE

def failing(content):
	log(content, xbmc.LOGERROR)

def debug(content):
	log(content, xbmc.LOGDEBUG)

def log(msg, level=xbmc.LOGNOTICE):
	msg = py2_enc(msg)
	xbmc.log("["+addon.getAddonInfo('id')+"-"+addon.getAddonInfo('version')+"]"+msg, level)

def index():
	addDir(translation(30802), "", "SearchDeezer", pic+'deepsearch.gif')
	addDir(translation(30601), "", "beatportMain", pic+'beatport.png')
	addDir(translation(30602), "", "billboardMain", pic+'billboard.png')
	addDir(translation(30603), "", "ddpMain", pic+'ddp-international.png')
	addDir(translation(30604), "", "hypemMain", pic+'hypem.png')
	addDir(translation(30605), "", "itunesMain", pic+'itunes.png')
	addDir(translation(30606), "", "ocMain", pic+'official.png')
	addDir(translation(30607), "", "spotifyMain", pic+'spotify.png')
	addDir(translation(30801), "", "Settings", pic+'settings.png')
	xbmcplugin.endOfDirectory(pluginhandle)

def beatportMain():
	content = cache('https://pro.beatport.com', 30)
	content = content[content.find('<div class="mobile-menu-body">')+1:]
	content = content[:content.find('<!-- End Mobile Touch Menu -->')]
	match = re.compile('<a href="(.*?)" class="(.*?)" data-name=".+?">(.*?)</a>', re.DOTALL).findall(content)
	allTitle = translation(30620)
	addAutoPlayDir(allTitle, urlBaseBP+"/top-100", "listBeatportVideos", pic+'beatport.png', "", "browse")
	for genreURL, genreTYPE, genreTITLE in match:
		topUrl = urlBaseBP+genreURL+'/top-100'
		title = cleanTitle(genreTITLE)
		addAutoPlayDir(title, topUrl, "listBeatportVideos", pic+'beatport.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')

def listBeatportVideos(type, url, limit):
	musicVideos = []
	count = 0
	if type == "play":
		playlist = xbmc.PlayList(1)
		playlist.clear()
	content = cache(url, 1)
	spl = content.split('bucket-item ec-item track')
	for i in range(1,len(spl),1):
		entry = spl[i]
		artist = re.compile('data-artist=".+?">(.*?)</a>', re.DOTALL).findall(entry)[0]
		artist = cleanTitle(artist)
		song = re.compile('<span class="buk-track-primary-title" title=".+?">(.*?)</span>', re.DOTALL).findall(entry)[0]
		remix = re.compile('<span class="buk-track-remixed">(.*?)</span>', re.DOTALL).findall(entry)
		if "(original mix)" in song.lower():
			song = song.lower().split('(original mix)')[0]
		song = cleanTitle(song)
		if "(feat." in song.lower() and " feat." in song.lower():
			song = song.split(')')[0]+')'
		elif not "(feat." in song.lower() and " feat." in song.lower():
			firstSong = song.lower().split(' feat.')[0]
			secondSong = song.lower().split(' feat.')[1]
			song = firstSong+' (feat.'+secondSong+')'
		if remix and not "original" in remix[0].lower():
			newRemix = remix[0].replace('[', '').replace(']', '')
			song += ' ['+cleanTitle(newRemix)+']'
		firstTitle = artist+" - "+song
		try:
			oldDate = re.compile('<p class="buk-track-released">(.*?)</p>', re.DOTALL).findall(entry)[0]
			convert = time.strptime(oldDate,'%Y-%m-%d')
			newDate = time.strftime('%d.%m.%Y',convert)
			completeTitle = firstTitle+'   [COLOR deepskyblue]['+str(newDate)+'][/COLOR]'
		except: completeTitle = firstTitle
		try:
			thumb = re.compile('data-src="(http.*?.jpg)"', re.DOTALL).findall(entry)[0]
			thumb = thumb.split('image_size')[0]+'image/'+thumb.split('/')[-1]
			#thumb = thumb.replace("/30x30/","/500x500/").replace("/60x60/","/500x500/").replace("/95x95/","/500x500/").replace("/250x250/","/500x500/")
		except: thumb = pic+'noimage.png'
		filtered = False
		for snippet in blackList:
			if snippet.strip().lower() and snippet.strip().lower() in firstTitle.lower():
				filtered = True
		if filtered:
			continue
		if type == "play":
			url = "plugin://"+addon.getAddonInfo('id')+"/?url="+quote_plus(firstTitle.replace(" - ", " "))+"&mode=playYTByTitle"
		else:
			url = firstTitle
		musicVideos.append([firstTitle, completeTitle, url, thumb])
	if type == "browse":
		for firstTitle, completeTitle, url, thumb in musicVideos:
			count += 1
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+completeTitle
			addLink(name, url.replace(" - ", " "), "playYTByTitle", thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for firstTitle, completeTitle, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(firstTitle, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)

def billboardMain():
	addAutoPlayDir(translation(30630), urlBaseBB+"/charts/hot-100", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
	addAutoPlayDir(translation(30631), urlBaseBB+"/charts/billboard-200", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
	addDir(translation(30632), "", "listBillboardArchiveYears", pic+'billboard.png')
	addDir(translation(30633), "genre", "listBillboardCharts", pic+'billboard.png')
	addDir(translation(30634), "country", "listBillboardCharts", pic+'billboard.png')
	addDir(translation(30635), "other", "listBillboardCharts", pic+'billboard.png')
	xbmcplugin.endOfDirectory(pluginhandle)

def listBillboardArchiveYears():
	for i in range(datetime.date.today().year,1957,-1):
		addDir(str(i), urlBaseBB+"/archive/charts/"+str(i), "listBillboardAR_Genres", pic+'billboard.png')
	xbmcplugin.endOfDirectory(pluginhandle)

def listBillboardAR_Genres(url):
	xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
	UN_Supported = ['album', 'artist 100', 'billboard 200', 'greatest of all time', 'next big', 'social 50', 'tastemaker', 'uncharted'] # if Artist and Song are the same or if Album
	content = cache(url, 30)
	content = content[content.find('<li class="year-list__decade last">')+1:]
	content = content[:content.find('<aside class="simple-page__body-supplementary">')]
	match = re.compile('<a href="/archive/charts/(.*?)">(.*?)</a>', re.DOTALL).findall(content)
	for url2, title in match:
		if title != "" and not "empty" in title and not any(x in title.strip().lower() for x in UN_Supported):
			addAutoPlayDir(cleanTitle(title), urlBaseBB+'/archive/charts/'+url2, "listBillboardAR_Videos", pic+'billboard.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')

def listBillboardAR_Videos(type, url, limit):
	musicVideos = []
	musicIsolated = set()
	count = 0
	if type == "play":
		playlist = xbmc.PlayList(1)
		playlist.clear()
	content = cache(url, 30)
	content = content[content.find('<tbody>')+1:]
	content = content[:content.find('</tbody>')]
	spl = content.split('<tr>')
	for i in range(1,len(spl),1):
		entry = spl[i]
		try:
			song = re.findall('<t.+?>(.*?)</td>',entry,re.S)[1]
			artist = re.findall('<t.+?>(.*?)</td>',entry,re.S)[2]
		except: pass
		if song == "" or artist == "":
			continue
		song = cleanTitle(song)
		artist = cleanTitle(artist)
		if song.strip().lower() != artist.strip().lower():
			title = artist+" - "+song
			newTitle = song.lower()
			if newTitle in musicIsolated:
				continue
			musicIsolated.add(newTitle)
			if title.isupper():
				title = TitleCase(title)
			filtered = False
			for snippet in blackList:
				if snippet.strip().lower() and snippet.strip().lower() in title.lower():
					filtered = True
			if filtered:
				continue
			if type == "play":
				url = "plugin://"+addon.getAddonInfo('id')+"/?url="+quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
			else:
				url = title
			musicVideos.append([title, url])
	if type == "browse":
		for title, url in musicVideos:
			count += 1
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title
			addLink(name, url.replace(" - ", " "), "playYTByTitle", "")
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for title, url in musicVideos:
			listitem = xbmcgui.ListItem(title)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)

def listBillboardCharts(type):
	if type == "genre":
		addAutoPlayDir("Alternative", urlBaseBB+"/charts/alternative-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Country", urlBaseBB+"/charts/country-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Dance/Club", urlBaseBB+"/charts/dance-club-play-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Dance/Electronic", urlBaseBB+"/charts/dance-electronic-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Gospel", urlBaseBB+"/charts/gospel-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Latin", urlBaseBB+"/charts/latin-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Pop", urlBaseBB+"/charts/pop-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Rap", urlBaseBB+"/charts/rap-song", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("R&B", urlBaseBB+"/charts/r-and-b-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("R&B/Hip-Hop", urlBaseBB+"/charts/r-b-hip-hop-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Rhythmic", urlBaseBB+"/charts/rhythmic-40", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Rock", urlBaseBB+"/charts/rock-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Smooth Jazz", urlBaseBB+"/charts/jazz-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Soundtracks", urlBaseBB+"/charts/soundtracks", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Tropical", urlBaseBB+"/charts/tropical-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
	elif type == "country":
		addAutoPlayDir("Argentina Hot-100", urlBaseBB+"/charts/billboard-argentina-hot-100", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Canada Hot-100", urlBaseBB+"/charts/canadian-hot-100", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Japan Hot-100", urlBaseBB+"/charts/japan-hot-100", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("France Songs", urlBaseBB+"/charts/france-digital-song-sales", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Germany Songs", urlBaseBB+"/charts/germany-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("U.K. Charts", urlBaseBB+"/charts/official-uk-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
	elif type == "other":
		addAutoPlayDir("Digital Song Sales", urlBaseBB+"/charts/digital-song-sales", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("On-Demand Streaming Songs", urlBaseBB+"/charts/on-demand-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Radio Songs", urlBaseBB+"/charts/radio-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("TOP Songs of the '90s", urlBaseBB+"/charts/greatest-billboards-top-songs-90s", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("TOP Songs of the '80s", urlBaseBB+"/charts/greatest-billboards-top-songs-80s", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("All Time Hot 100 Singles", urlBaseBB+"/charts/greatest-hot-100-singles", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("All Time Greatest Alternative Songs", urlBaseBB+"/charts/greatest-alternative-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("All Time Greatest Country Songs", urlBaseBB+"/charts/greatest-country-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("All Time Greatest Latin Songs", urlBaseBB+"/charts/greatest-hot-latin-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("All Time Greatest Pop Songs", urlBaseBB+"/charts/greatest-of-all-time-pop-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')

def listBillboardCH_Videos(type, url, limit):
	musicVideos = []
	count = 0
	if type == "play":
		playlist = xbmc.PlayList(1)
		playlist.clear()
	content = cache(url, 1)
	spl = content.split('class="chart-list-item__image-wrapper">')
	for i in range(1,len(spl),1):
		entry = spl[i]
		song = re.compile('<span class="chart-list-item__title-text">(.*?)</span>', re.DOTALL).findall(entry)[0]
		song = re.sub(r'\<.*?>', '', song)
		song = cleanTitle(song)
		artist = re.compile('<div class="chart-list-item__artist">(.*?)</div>', re.DOTALL).findall(entry)[0]
		artist = re.sub(r'\<.*?>', '', artist)
		artist = cleanTitle(artist)
		try:
			thumb = re.compile(r'data-srcset="(?:.+?w, )?(https?:.+?(?:\.jpg|\.jpeg|\.png))', re.DOTALL).findall(entry)[0]
			thumb = thumb.replace('-53x53', '').replace('-87x87', '').replace('-106x106', '').replace('-174x174', '').strip()
			if "bb-placeholder" in thumb:
				unThumb_2 = re.compile(r'class="chart-video__wrapper" data-brightcove-data="(.+?)data-rank=', re.DOTALL).findall(entry)[0]
				newTHUMB_2 = unThumb_2.replace('\/', '/').replace('&quot;', '"').strip()
				thumb = re.compile('.*?(https?:.+?(?:\.jpg|\.jpeg|\.png)).*?', re.DOTALL).findall(newTHUMB_2)[0]
		except: thumb = pic+'noimage.png'
		title = artist+" - "+song
		filtered = False
		for snippet in blackList:
			if snippet.strip().lower() and snippet.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == "play":
			url = "plugin://"+addon.getAddonInfo('id')+"/?url="+quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
		else:
			url = title
		musicVideos.append([title, url, thumb])
	if type == "browse":
		for title, url, thumb in musicVideos:
			count += 1
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title
			addLink(name, url.replace(" - ", " "), "playYTByTitle", thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)

def ddpMain():
	content = cache(urlBaseDDP+"DDP-Charts/", 30)
	content = content[content.find('<div class="ddp_subnavigation_top ddp">')+1:]
	content = content[:content.find('<div class="contentbox">')]
	match = re.compile('<li><a href="(.*?)">(.*?)</a></li>', re.DOTALL).findall(content)
	addDir("[COLOR deepskyblue]"+translation(30640)+"[/COLOR]", "", "ddpMain", pic+'ddp-international.png')
	addAutoPlayDir("     AKTUELLE VIDEOS TOP 30", urlBaseDDP+"DDP-Videochart/", "listDdpVideos", pic+'ddp-international.png', "", "browse")
	for url2, title in match:
		title = cleanTitle(title)
		if not 'ddp' in title.lower() and not 'archiv' in title.lower() and not 'highscores' in title.lower():
			if not 'schlager' in url2.lower():
				if 'top 100' in title.lower() or 'hot 50' in title.lower() or 'einsteiger' in title.lower():
					addAutoPlayDir('     '+title, url2, "listDdpVideos", pic+'ddp-international.png', "", "browse")
				elif 'jahrescharts' in title.lower():
					addDir('     '+title, url2, "listDdpYearCharts", pic+'ddp-international.png')
	addDir("[COLOR deepskyblue]"+translation(30641)+"[/COLOR]", "", "ddpMain", pic+'ddp-schlager.png')
	for url2, title in match:
		title = cleanTitle(title)
		if not 'ddp' in title.lower() and not 'archiv' in title.lower() and not 'highscores' in title.lower():
			if 'schlager' in url2.lower():
				if 'top 100' in title.lower() or 'hot 50' in title.lower() or 'einsteiger' in title.lower():
					addAutoPlayDir('     '+title, url2, "listDdpVideos", pic+'ddp-schlager.png', "", "browse")
				elif 'jahrescharts' in title.lower():
					addDir('     '+title, url2, "listDdpYearCharts", pic+'ddp-schlager.png')
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')

def listDdpYearCharts(url):
	musicVideos = []
	content = cache(url, 1)
	content = content[content.find('<div class="contentbox">')+1:]
	content = content[:content.find('</p>')]
	match = re.compile('<a href="(.*?)" alt="(.*?)">', re.DOTALL).findall(content)
	for url2, title in match:
		if 'schlager' in url.lower():
			endURL = urlBaseDDP+'DDP-Schlager-Jahrescharts/?'+url2.split('/?')[1]
			thumb = pic+'ddp-schlager.png'
		elif not 'schlager' in url.lower():
			endURL = urlBaseDDP+'DDP-Jahrescharts/?'+url2.split('/?')[1]
			thumb = pic+'ddp-international.png'
		musicVideos.append([title, endURL, thumb])
	musicVideos = sorted(musicVideos, key=lambda b:b[0], reverse=True)
	for title, endURL, thumb in musicVideos:
		addAutoPlayDir(cleanTitle(title), endURL, "listDdpVideos", thumb, "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')

def listDdpVideos(type, url, limit):
	musicVideos = []
	musicIsolated = set()
	if type == "play":
		playlist = xbmc.PlayList(1)
		playlist.clear()
	content = cache(url, 1)
	content = content[content.find('<div class="eintrag" id="charthead">')+1:]
	content = content[:content.find('<div id="banner_fuss">')]
	spl = content.split('<div class="eintrag">')
	for i in range(1,len(spl),1):
		entry = spl[i]
		rank = re.compile('<div class="platz">(.*?)</div>', re.DOTALL).findall(entry)[0]
		artist = re.compile('<div class="interpret">(.*?)</div>', re.DOTALL).findall(entry)[0]
		song = re.compile('<div class="titel">(.*?)</div>', re.DOTALL).findall(entry)[0]
		if song == "" or artist == "":
			continue
		if artist.isupper():
			artist = py2_uni(artist).title()
		artist = cleanTitle(artist)
		if song.isupper():
			song = py2_uni(song).title()
		song = cleanTitle(song)
		firstTitle = artist+" - "+song
		if firstTitle in musicIsolated:
			continue
		musicIsolated.add(firstTitle)
		try:
			newRE = re.compile('<div class="platz">(.*?)</div>', re.DOTALL).findall(entry)[1]
			LW = re.compile('<div class="platz">(.*?)</div>', re.DOTALL).findall(entry)[2]
			twoW = re.compile('<div class="platz">(.*?)</div>', re.DOTALL).findall(entry)[3]
			threeW = re.compile('<div class="platz">(.*?)</div>', re.DOTALL).findall(entry)[4]
			if ('RE' in newRE or 'NEU' in newRE) and not 'images' in newRE:
				completeTitle = firstTitle+'   [COLOR deepskyblue]['+str(newRE)+'][/COLOR]'
			else:
				completeTitle = firstTitle+'   [COLOR deepskyblue][AW: '+str(LW)+'|2W: '+str(twoW)+'|3W: '+str(threeW)+'][/COLOR]'
		except: completeTitle = firstTitle
		try:
			thumb = re.findall('style="background.+?//poolposition.mp3(.*?);"',entry,re.S)[0]
			if thumb:
				thumb = "https://poolposition.mp3"+thumb.split('&amp;width')[0]
		except: thumb = pic+'noimage.png'
		filtered = False
		for snippet in blackList:
			if snippet.strip().lower() and snippet.strip().lower() in firstTitle.lower():
				filtered = True
		if filtered:
			continue
		if type == "play":
			url = "plugin://"+addon.getAddonInfo('id')+"/?url="+quote_plus(firstTitle.replace(" - ", " "))+"&mode=playYTByTitle"
		else:
			url = firstTitle
		musicVideos.append([int(rank), firstTitle, completeTitle, url, thumb])
	musicVideos = sorted(musicVideos, key=lambda b:b[0], reverse=False)
	if type == "browse":
		for rank, firstTitle, completeTitle, url, thumb in musicVideos:
			name = '[COLOR chartreuse]'+str(rank)+' •  [/COLOR]'+completeTitle
			addLink(name, url.replace(" - ", " "), "playYTByTitle", thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for rank, firstTitle, completeTitle, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(firstTitle, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)

def hypemMain():
	addAutoPlayDir(translation(30650), urlBaseHypem+"/popular?ax=1&sortby=shuffle", 'listHypemVideos', pic+'hypem.png', "", "browse")
	addAutoPlayDir(translation(30651), urlBaseHypem+"/popular/lastweek?ax=1&sortby=shuffle", 'listHypemVideos', pic+'hypem.png', "", "browse")
	addDir(translation(30652), "", 'listHypemMachine', pic+'hypem.png')
	xbmcplugin.endOfDirectory(pluginhandle)

def listHypemMachine():
	for i in range(1, 210, 1):
		dt = datetime.date.today()
		while dt.weekday() != 0:
			dt -= datetime.timedelta(days=1)
		dt -= datetime.timedelta(weeks=i)
		months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
		month = months[int(dt.strftime("%m")) - 1]
		addAutoPlayDir(dt.strftime("%d. %b - %Y").replace("Mar", translation(30653)).replace("May", translation(30654)).replace("Oct", translation(30655)).replace("Dec", translation(30656)), urlBaseHypem+"/popular/week:"+month+"-"+dt.strftime("%d-%Y")+"?ax=1&sortby=shuffle", 'listHypemVideos', pic+'hypem.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')

def listHypemVideos(type, url, limit):
	musicVideos = []
	musicIsolated = set()
	count = 0
	if type == "play":
		playlist = xbmc.PlayList(1)
		playlist.clear()
	content = cache(url, 1)
	jsonObject = json.loads(re.compile('id="displayList-data">(.*?)</', re.DOTALL).findall(content)[0])
	for track in jsonObject['tracks']:
		artist = cleanTitle(track['artist'])
		song = cleanTitle(track['song'])
		title = artist+" - "+song
		if title in musicIsolated or artist == "":
			continue
		musicIsolated.add(title)
		thumb = ""
		match = re.compile('href="/track/'+track['id']+'/.+?background:url\\((.+?)\\)', re.DOTALL).findall(content)
		if match:
			thumb = match[0] #.replace('_320.jpg)', '_500.jpg')
		filtered = False
		for snippet in blackList:
			if snippet.strip().lower() and snippet.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == "play":
			url = "plugin://"+addon.getAddonInfo('id')+"/?url="+quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
		else:
			url = title
		musicVideos.append([title, url, thumb])
	if type == "browse":
		for title, url, thumb in musicVideos:
			count += 1
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title
			addLink(name, url.replace(" - ", " "), "playYTByTitle", thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)

def itunesMain():
	content = cache("https://music.apple.com/"+iTunesRegion+"/genre/music/id34", 30)
	content = content[content.find('id="genre-nav"'):]
	content = content[:content.find('</div>')]
	match = re.compile('<li><a href="https://music.apple.com/.+?/genre/.+?/id(.*?)"(.*?)title=".+?">(.*?)</a>', re.DOTALL).findall(content)
	allTitle = translation(30660)
	addAutoPlayDir(allTitle, "0", "listItunesVideos", pic+'itunes.png', "", "browse")
	for genreID, genreTYPE, genreTITLE in match:
		title = cleanTitle(genreTITLE)
		if 'class="top-level-genre"' in genreTYPE:
			if itunesShowSubGenres:
				title = '[COLOR FF1E90FF]'+title+'[/COLOR]'
			addAutoPlayDir(title, genreID, "listItunesVideos", pic+'itunes.png', "", "browse")
		elif itunesShowSubGenres:
			title = '     '+title
			addAutoPlayDir(title, genreID, "listItunesVideos", pic+'itunes.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')

def listItunesVideos(type, genreID, limit):
	musicVideos = []
	musicIsolated = set()
	count = 0
	if type == "play":
		playlist = xbmc.PlayList(1)
		playlist.clear()
	url = "https://itunes.apple.com/"+iTunesRegion+"/rss/topsongs/limit=100"
	if genreID != "0":
		url += "/genre="+genreID
	url += "/explicit=true/json"
	content = cache(url, 1)
	response = json.loads(content)
	try:
		for item in response['feed']['entry']:
			artist = cleanTitle(item['im:artist']['label'])
			song = cleanTitle(item['im:name']['label'])
			title = artist+" - "+song
			newTitle = song.lower()
			if newTitle in musicIsolated:
				continue
			musicIsolated.add(newTitle)
			if len(artist) > 30:
				artist = artist[:30]
			if len(song) > 30:
				song = song[:30]
			shortenTitle = artist+" - "+song
			try: thumb = item['im:image'][2]['label']#.replace('/170x170bb-85.png', '/626x0w.jpg')
			except: thumb = pic+'noimage.png'
			aired = item['im:releaseDate']['attributes']['label']
			filtered = False
			for snippet in blackList:
				if snippet.strip().lower() and snippet.strip().lower() in title.lower():
					filtered = True
			if filtered:
				continue
			if type == "play":
				url = "plugin://"+addon.getAddonInfo('id')+"/?url="+quote_plus(shortenTitle.replace(" - ", " "))+"&mode=playYTByTitle"
			else:
				url = shortenTitle
			musicVideos.append([title, aired, url, thumb])
		if type == "browse":
			for title, aired, url, thumb in musicVideos:
				count += 1
				name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title+'   [COLOR deepskyblue]['+str(aired)+'][/COLOR]'
				addLink(name, url.replace(" - ", " "), "playYTByTitle", thumb)
			xbmcplugin.endOfDirectory(pluginhandle)
			if forceView:
				xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
		else:
			if limit:
				musicVideos = musicVideos[:int(limit)]
			random.shuffle(musicVideos)
			for title, aired, url, thumb in musicVideos:
				listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
				playlist.add(url, listitem)
			xbmc.Player().play(playlist)
	except: pass

def ocMain():
	addAutoPlayDir(translation(30670), urlBaseOC+"/charts/singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(30671), urlBaseOC+"/charts/uk-top-40-singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(30672), urlBaseOC+"/charts/singles-chart-update/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(30673), urlBaseOC+"/charts/singles-downloads-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(30674), urlBaseOC+"/charts/singles-sales-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(30675), urlBaseOC+"/charts/audio-streaming-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(30676), urlBaseOC+"/charts/dance-singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(30677), urlBaseOC+"/charts/classical-singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(30678), urlBaseOC+"/charts/r-and-b-singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(30679), urlBaseOC+"/charts/rock-and-metal-singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(30680), urlBaseOC+"/charts/irish-singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(30681), urlBaseOC+"/charts/scottish-singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(30682), urlBaseOC+"/charts/end-of-year-singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(30683), urlBaseOC+"/charts/physical-singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')

def listOcVideos(type, url, limit):
	musicVideos = []
	musicIsolated = set()
	count = 0
	if type == "play":
		playlist = xbmc.PlayList(1)
		playlist.clear()
	content = cache(url, 1)
	match = re.findall(r'<div class=["\']track["\']>(.*?)<div class=["\']actions["\']>', content, re.DOTALL)
	for video in match:
		photo = re.compile(r'<img src=["\'](.*?)["\']', re.DOTALL).findall(video)[0]
		if "images-amazon" in photo or "coverartarchive.org" in photo:
			thumb = photo.split('img/small?url=')[1]
		elif "/img/small?url=/images/artwork/" in photo:
			thumb = photo.replace("/img/small?url=", "")
		else:
			thumb = pic+'noimage.png'
		song = re.compile(r'<a href=["\'].+?["\']>(.*?)</a>', re.DOTALL).findall(video)[0]
		artist = re.compile(r'<a href=["\'].+?["\']>(.*?)</a>', re.DOTALL).findall(video)[1]
		if "/" in artist:
			artist = artist.split('/')[0]
		song = cleanTitle(song)
		song = TitleCase(song)
		artist = cleanTitle(artist)
		artist = TitleCase(artist)
		title = artist+" - "+song
		filtered = False
		for snippet in blackList:
			if snippet.strip().lower() and snippet.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == "play":
			url = "plugin://"+addon.getAddonInfo('id')+"/?url="+quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
		else:
			url = title
		musicVideos.append([title, url, thumb])
	if type == "browse":
		for title, url, thumb in musicVideos:
			count += 1
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title
			addLink(name, url.replace(" - ", " "), "playYTByTitle", thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)

def spotifyMain():
	addDir(translation(30690), "viraldaily", "listSpotifyCC_Countries", pic+'spotify.png')
	addDir(translation(30691), "viralweekly", "listSpotifyCC_Countries", pic+'spotify.png')
	addDir(translation(30692), "topdaily", "listSpotifyCC_Countries", pic+'spotify.png')
	addDir(translation(30693), "topweekly", "listSpotifyCC_Countries", pic+'spotify.png')
	xbmcplugin.endOfDirectory(pluginhandle)

def listSpotifyCC_Countries(type):
	xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
	musicIsolated = set()
	UN_Supported = ['andorra', 'bulgaria', 'cyprus', 'hong kong', 'israel', 'japan', 'monaco', 'malta', 'nicaragua', 'singapore', 'thailand', 'taiwan'] # these lists are empty or signs are not readable
	content = cache(urlBaseSCC+'regional', 1)
	content = content[content.find('<div class="responsive-select" data-type="country">')+1:]
	content = content[:content.find('<div class="responsive-select" data-type="recurrence">')]
	match = re.compile('<li data-value="(.*?)" class=.+?>(.*?)</li>', re.DOTALL).findall(content)
	for url2, toptitle in match:
		if any(x in toptitle.strip().lower() for x in UN_Supported):
			continue
		if toptitle.strip() in musicIsolated:
			continue
		musicIsolated.add(toptitle)
		if type == "viraldaily":
			addAutoPlayDir(cleanTitle(toptitle), urlBaseSCC+'viral/'+url2+'/daily/latest', "listSpotifyCC_Videos", pic+'spotify.png', "", "browse")
		elif type == "viralweekly":
			addAutoPlayDir(cleanTitle(toptitle), urlBaseSCC+'viral/'+url2+'/weekly/latest', "listSpotifyCC_Videos", pic+'spotify.png', "", "browse")
		elif type == "topdaily":
			addAutoPlayDir(cleanTitle(toptitle), urlBaseSCC+'regional/'+url2+'/daily/latest', "listSpotifyCC_Videos", pic+'spotify.png', "", "browse")
		elif type == "topweekly":
			addAutoPlayDir(cleanTitle(toptitle), urlBaseSCC+'regional/'+url2+'/weekly/latest', "listSpotifyCC_Videos", pic+'spotify.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')

def listSpotifyCC_Videos(type, url, limit):
	musicVideos = []
	musicIsolated = set()
	count = 0
	if type == "play":
		playlist = xbmc.PlayList(1)
		playlist.clear()
	content = cache(url, 1)
	content = content[content.find('<tbody>')+1:]
	content = content[:content.find('</tbody>')]
	spl = content.split('<tr>')
	for i in range(1,len(spl),1):
		entry = spl[i]
		song = re.compile('<strong>(.*?)</strong>', re.DOTALL).findall(entry)[0]
		song = cleanTitle(song)
		artist = re.compile('<span>(.*?)</span>', re.DOTALL).findall(entry)[0]
		artist = cleanTitle(artist)
		if "(remix)" in song.lower():
			song = song.lower().replace('(remix)', '')
		if " - " in song:
			firstSong = song[:song.rfind(' - ')]
			secondSong = song[song.rfind(' - ')+3:]
			song = firstSong+' ['+secondSong+']'
		if artist.lower().startswith('by', 0, 2):
			artist = artist.lower().split('by ')[1]
		if artist.islower():
			artist = TitleCase(artist)
		title = artist+" - "+song
		if title in musicIsolated or artist == "":
			continue
		musicIsolated.add(title)
		try:
			thumb = re.compile('<img src="(.*?)">', re.DOTALL).findall(entry)[0]
			if thumb[:4] != "http":
				#thumb = "https://u.scdn.co/images/pl/default/"+thumb
				thumb = "https://i.scdn.co/image/"+thumb
		except: thumb = pic+'noimage.png'
		try:
			streams = re.compile('<td class="chart-table-streams">(.*?)</td>', re.DOTALL).findall(entry)[0]
		except: streams = ""
		filtered = False
		for snippet in blackList:
			if snippet.strip().lower() and snippet.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == "play":
			url = "plugin://"+addon.getAddonInfo('id')+"/?url="+quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
		else:
			url = title
		musicVideos.append([title, streams, url, thumb])
	if type == "browse":
		for title, streams, url, thumb in musicVideos:
			count += 1
			if streams != "":
				name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title+'   [COLOR deepskyblue][DL: '+str(streams).replace(',', '.')+'][/COLOR]'
			else:
				name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title
			addLink(name, url.replace(" - ", " "), "playYTByTitle", thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for title, streams, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)

def SearchDeezer():
	someReceived = False
	word = xbmcgui.Dialog().input(translation(30803), type=xbmcgui.INPUT_ALPHANUM)
	word = quote_plus(word, safe='')
	if word == "": return
	artistSEARCH = cache("https://api.deezer.com/search/artist?q="+word+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
	trackSEARCH = cache("https://api.deezer.com/search/track?q="+word+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
	albumSEARCH = cache("https://api.deezer.com/search/album?q="+word+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
	playlistSEARCH = cache("https://api.deezer.com/search/playlist?q="+word+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
	userlistSEARCH = cache("https://api.deezer.com/search/user?q="+word+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
	strukturARTIST = json.loads(artistSEARCH)
	if strukturARTIST['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]ARTIST[COLOR orangered]  •  •  •[/COLOR][/B]', word, "listDeezerArtists", pic+'searchartists.png')
		someReceived = True
	strukturTRACK = json.loads(trackSEARCH)
	if strukturTRACK['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]SONG[COLOR orangered]     •  •  •[/COLOR][/B]', word, "listDeezerTracks", pic+'searchsongs.png')
		someReceived = True
	strukturALBUM = json.loads(albumSEARCH)
	if strukturALBUM['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]ALBUM[COLOR orangered]  •  •  •[/COLOR][/B]', word, "listDeezerAlbums", pic+'searchalbums.png')
		someReceived = True
	strukturPLAYLIST = json.loads(playlistSEARCH)
	if strukturPLAYLIST['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]PLAYLIST[COLOR orangered]  •  •  •[/COLOR][/B]', word, "listDeezerPlaylists", pic+'searchplaylists.png')
		someReceived = True
	strukturUSERLIST = json.loads(userlistSEARCH)
	if strukturUSERLIST['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]USER[COLOR orangered]     •  •  •[/COLOR][/B]', word, "listDeezerUserlists", pic+'searchuserlists.png')
		someReceived = True
	if not someReceived:
		addDir(translation(30804), word, "", pic+'noresults.png')
	xbmcplugin.endOfDirectory(pluginhandle)

def listDeezerArtists(url):
	musicVideos = []
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache("https://api.deezer.com/search/artist?q="+url+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
		response = json.loads(Original)
	for item in response['data']:
		artist = cleanTitle(item['name'])
		if artist.strip().lower() in musicIsolated or artist == "":
			continue
		musicIsolated.add(artist)
		try:
			thumb = item['picture_big']
			if thumb.endswith('artist//500x500-000000-80-0-0.jpg'):
				thumb = pic+'noavatar.gif'
		except: thumb = pic+'noavatar.gif'
		liked = item['nb_fan']
		tracksUrl = item['tracklist'].split('top?limit=')[0]+"top?limit="+deezerVideosDisplay+"&index=0"
		musicVideos.append([int(liked), artist, tracksUrl, thumb])
	musicVideos = sorted(musicVideos, key=lambda b:b[0], reverse=True)
	for liked, artist, tracksUrl, thumb in musicVideos:
		name = artist+"   [COLOR FFFFA500][Fans: "+str(liked).strip()+"][/COLOR]"
		addAutoPlayDir(name, tracksUrl, "listDeezerVideos", thumb, "", "browse")
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(30805), nextPage, "listDeezerArtists", pic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')

def listDeezerTracks(url):
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache("https://api.deezer.com/search/track?q="+url+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
		response = json.loads(Original)
	for item in response['data']:
		artist = cleanTitle(item['artist']['name'])
		song = cleanTitle(item['title'])
		title = artist+" - "+song
		if title in musicIsolated or artist == "":
			continue
		musicIsolated.add(title)
		album = cleanTitle(item['album']['title'])
		try: thumb = item['album']['cover_big']
		except: thumb = pic+'noimage.png'
		filtered = False
		for snippet in blackList:
			if snippet.strip().lower() and snippet.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		name = title+"   [COLOR deepskyblue][Album: "+album+"][/COLOR]"
		addLink(name, title.replace(" - ", " "), "playYTByTitle", thumb)
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(30805), nextPage, "listDeezerTracks", pic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')

def listDeezerAlbums(url):
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache("https://api.deezer.com/search/album?q="+url+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
		response = json.loads(Original)
	for item in response['data']:
		artist = cleanTitle(item['artist']['name'])
		album = cleanTitle(item['title'])
		title = artist+" - "+album
		if title in musicIsolated or artist == "":
			continue
		musicIsolated.add(title)
		try: thumb = item['cover_big']
		except: thumb = pic+'noimage.png'
		numbers = item['nb_tracks']
		tracksUrl = item['tracklist']+"?limit="+deezerVideosDisplay+"&index=0"
		version = cleanTitle(item['record_type'])
		name = title+"   [COLOR deepskyblue]["+version.title()+"[/COLOR] - [COLOR FFFFA500]Tracks: "+str(numbers).strip()+"][/COLOR]"
		addAutoPlayDir(name, tracksUrl, "listDeezerVideos", thumb, "", "browse")
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(30805), nextPage, "listDeezerAlbums", pic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')

def listDeezerPlaylists(url):
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache("https://api.deezer.com/search/playlist?q="+url+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
		response = json.loads(Original)
	for item in response['data']:
		artist = cleanTitle(item['title'])
		try: thumb = item['picture_big']
		except: thumb = pic+'noimage.png'
		numbers = item['nb_tracks']
		tracksUrl = item['tracklist']+"?limit="+deezerVideosDisplay+"&index=0"
		user = cleanTitle(item['user']['name'])
		name = artist.title()+"   [COLOR deepskyblue][User: "+user.title()+"[/COLOR] - [COLOR FFFFA500]Tracks: "+str(numbers).strip()+"][/COLOR]"
		special = artist+" - "+user.title()
		if special in musicIsolated or artist == "":
			continue
		musicIsolated.add(special)
		addAutoPlayDir(name, tracksUrl, "listDeezerVideos", thumb, "", "browse")
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(30805), nextPage, "listDeezerPlaylists", pic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')

def listDeezerUserlists(url):
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache("https://api.deezer.com/search/user?q="+url+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
		response = json.loads(Original)
	for item in response['data']:
		user = cleanTitle(item['name'])
		try:
			thumb = item['picture_big']
			if thumb.endswith('user//500x500-000000-80-0-0.jpg'):
				thumb = pic+'noavatar.gif'
		except: thumb = pic+'noavatar.gif'
		tracksUrl = item['tracklist']+"?limit="+deezerVideosDisplay+"&index=0"
		name = TitleCase(user)
		if name in musicIsolated or user == "":
			continue
		musicIsolated.add(name)
		addAutoPlayDir(name, tracksUrl, "listDeezerVideos", thumb, "", "browse")
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(30805), nextPage, "listDeezerUserlists", pic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')

def listDeezerVideos(type, url, image, limit):
	musicVideos = []
	musicIsolated = set()
	count = 0
	if type == "play":
		playlist = xbmc.PlayList(1)
		playlist.clear()
	if not "&index=0" in url:
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache(url, 1)
		response = json.loads(Original)
	for item in response['data']:
		song = cleanTitle(item['title'])
		if song.isupper():
			song = TitleCase(song)
		artist = cleanTitle(item['artist']['name'])
		title = artist+" - "+song
		if title in musicIsolated or artist == "":
			continue
		musicIsolated.add(title)
		filtered = False
		for snippet in blackList:
			if snippet.strip().lower() and snippet.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == "play":
			url = "plugin://"+addon.getAddonInfo('id')+"/?url="+quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
		else:
			url = title
		musicVideos.append([title, url, image])
	if type == "browse":
		for title, url, image in musicVideos:
			count += 1
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title
			addLink(name, url.replace(" - ", " "), "playYTByTitle", image)
		try:
			nextPage = response['next']
			if 'https://api.deezer.com/' in nextPage:
				addAutoPlayDir(translation(30805), nextPage, "listDeezerVideos", image, "", "browse")
		except: pass
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for title, url, image in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=image)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)

def getHTML(url, headers=False, referer=False):
	req = Request(url)
	if headers:
		for key in headers:
			req.add_header(key, headers[key])
	else:
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0')
		req.add_header('Accept-Encoding','gzip, deflate')
	if referer:
		req.add_header('Referer', referer)
	response = urlopen(req, timeout=30)
	if response.info().get('Content-Encoding') == 'gzip':
		link = py3_dec(gzip.GzipFile(fileobj=io.BytesIO(response.read())).read())
	else:
		link = py3_dec(response.read())
	response.close()
	return link

def cache(url, duration=0):
	cacheFile = os.path.join(cachePath, (''.join(c for c in py2_uni(url) if c not in '/\\:?"*|<>')).strip())
	if len(cacheFile) > 255:
		cacheFile = cacheFile.replace("part=snippet&type=video&maxResults=5&order=relevance&q", "")
		cacheFile = cacheFile[:255]
	if os.path.exists(cacheFile) and duration !=0 and os.path.getmtime(cacheFile) < time.time() - (60*60*24*duration):
		fh = xbmcvfs.File(cacheFile, 'r')
		content = fh.read()
		fh.close()
	else:
		content = getHTML(url)
		fh = xbmcvfs.File(cacheFile, 'w')
		fh.write(content)
		fh.close()
	return content

def getYoutubeId(title):
	title = quote_plus(title.lower()).replace('%5B', '').replace('%5D', '').replace('%28', '').replace('%29', '')
	videoBest = False
	movieID = []
	content = cache("https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=5&order=relevance&q=%s&key=%s" %(title,token), 1)
	response = json.loads(content)
	for videoTrack in response.get('items', []):
		if videoTrack['id']['kind'] == "youtube#video":
			movieID.append('%s @@@ %s' %(videoTrack['snippet']['title'], videoTrack['id']['videoId']))
	if len(movieID) > 0:
		for videoTrack in movieID:
			best = movieID[:]
			if not 'audio' in best[0].strip().lower():
				VIDEOexAUDIO = best[0].split('@@@ ')[1].strip()
			elif not 'audio' in best[1].strip().lower():
				VIDEOexAUDIO = best[1].split('@@@ ')[1].strip()
			elif not 'audio' in best[2].strip().lower():
				VIDEOexAUDIO = best[2].split('@@@ ')[1].strip()
			else:
				VIDEOexAUDIO = best[0].split('@@@ ')[1].strip()
		videoBest = VIDEOexAUDIO
	else:
		xbmcgui.Dialog().notification('Youtube Music : [COLOR red]!!! URL - ERROR !!![/COLOR]', 'ERROR = [COLOR red]No *SingleEntry* found on YOUTUBE ![/COLOR]', icon, 6000)
	return videoBest

def playYTByTitle(title):
	try:
		youtubeID = getYoutubeId('official '+title)
		finalURL = 'plugin://plugin.video.youtube/play/?video_id='+youtubeID
		xbmcplugin.setResolvedUrl(pluginhandle, True, xbmcgui.ListItem(path=finalURL))
		xbmc.sleep(1000)
		if infoEnabled and not xbmc.abortRequested:
			showInfo()
	except: pass

def showInfo():
	count = 0
	while not xbmc.Player().isPlaying():
		xbmc.sleep(200)
		if count == 50:
			break
		count += 1
	xbmc.sleep(infoDelay*1000)
	if xbmc.Player().isPlaying() and infoType == '0':
		xbmc.sleep(1500)
		xbmc.executebuiltin('ActivateWindow(12901)')
		xbmc.sleep(infoDuration*1000)
		xbmc.executebuiltin('ActivateWindow(12005)')
		xbmc.sleep(500)
		xbmc.executebuiltin('Action(Back)')
	elif xbmc.Player().isPlaying() and infoType == '1':
		TOP = translation(30806)
		xbmc.getInfoLabel('Player.Title')
		xbmc.getInfoLabel('Player.Duration')
		xbmc.getInfoLabel('Player.Art(thumb)')
		xbmc.sleep(500)
		title = xbmc.getInfoLabel('Player.Title')
		relTitle = cleanTitle(title)
		if relTitle.isupper() or relTitle.islower():
			relTitle = TitleCase(relTitle)
		runTime = xbmc.getInfoLabel('Player.Duration')
		photo = xbmc.getInfoLabel('Player.Art(thumb)')
		xbmc.sleep(1000)
		xbmcgui.Dialog().notification(TOP, relTitle+"[COLOR blue]  * "+runTime+" *[/COLOR]", photo, infoDuration*1000)
	else: pass

def cleanTitle(title):
	title = py2_enc(title)
	title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&Amp;", "&").replace("&#34;", "”").replace("&#39;", "'").replace("&#039;", "'").replace("&quot;", "\"").replace("&Quot;", "\"").replace("&szlig;", "ß").replace("&mdash;", "-").replace("&ndash;", "-").replace('–', '-')
	title = title.replace("&#x00c4", "Ä").replace("&#x00e4", "ä").replace("&#x00d6", "Ö").replace("&#x00f6", "ö").replace("&#x00dc", "Ü").replace("&#x00fc", "ü").replace("&#x00df", "ß")
	title = title.replace("&Auml;", "Ä").replace("&auml;", "ä").replace("&Euml;", "Ë").replace("&euml;", "ë").replace("&Iuml;", "Ï").replace("&iuml;", "ï").replace("&Ouml;", "Ö").replace("&ouml;", "ö").replace("&Uuml;", "Ü").replace("&uuml;", "ü").replace("&#376;", "Ÿ").replace("&yuml;", "ÿ")
	title = title.replace("&agrave;", "à").replace("&Agrave;", "À").replace("&aacute;", "á").replace("&Aacute;", "Á").replace("&egrave;", "è").replace("&Egrave;", "È").replace("&eacute;", "é").replace("&Eacute;", "É").replace("&igrave;", "ì").replace("&Igrave;", "Ì").replace("&iacute;", "í").replace("&Iacute;", "Í")
	title = title.replace("&ograve;", "ò").replace("&Ograve;", "Ò").replace("&oacute;", "ó").replace("&Oacute;", "ó").replace("&ugrave;", "ù").replace("&Ugrave;", "Ù").replace("&uacute;", "ú").replace("&Uacute;", "Ú").replace("&yacute;", "ý").replace("&Yacute;", "Ý")
	title = title.replace("&atilde;", "ã").replace("&Atilde;", "Ã").replace("&ntilde;", "ñ").replace("&Ntilde;", "Ñ").replace("&otilde;", "õ").replace("&Otilde;", "Õ").replace("&Scaron;", "Š").replace("&scaron;", "š")
	title = title.replace("&acirc;", "â").replace("&Acirc;", "Â").replace("&ccedil;", "ç").replace("&Ccedil;", "Ç").replace("&ecirc;", "ê").replace("&Ecirc;", "Ê").replace("&icirc;", "î").replace("&Icirc;", "Î").replace("&ocirc;", "ô").replace("&Ocirc;", "Ô").replace("&ucirc;", "û").replace("&Ucirc;", "Û")
	title = title.replace("&alpha;", "a").replace("&Alpha;", "A").replace("&aring;", "å").replace("&Aring;", "Å").replace("&aelig;", "æ").replace("&AElig;", "Æ").replace("&epsilon;", "e").replace("&Epsilon;", "Ε").replace("&eth;", "ð").replace("&ETH;", "Ð").replace("&gamma;", "g").replace("&Gamma;", "G")
	title = title.replace("&oslash;", "ø").replace("&Oslash;", "Ø").replace("&theta;", "θ").replace("&thorn;", "þ").replace("&THORN;", "Þ")
	title = title.replace("\\'", "'").replace("&x27;", "'").replace("&bull;", "•").replace("&iexcl;", "¡").replace("&iquest;", "¿").replace("&rsquo;", "’").replace("&lsquo;", "‘").replace("&sbquo;", "’").replace("&rdquo;", "”").replace("&ldquo;", "“").replace("&bdquo;", "”").replace("&rsaquo;", "›").replace("lsaquo;", "‹").replace("&raquo;", "»").replace("&laquo;", "«")
	title = title.replace(" ft ", " feat. ").replace(" FT ", " feat. ").replace(" Ft ", " feat. ").replace("Ft.", "feat.").replace("ft.", "feat.").replace(" FEAT ", " feat. ").replace(" Feat ", " feat. ").replace("Feat.", "feat.").replace("Featuring", "feat.").replace("&copy;", "©").replace("&reg;", "®").replace("™", "")
	title = title.strip()
	return title

def parameters_string_to_dict(parameters):
	paramDict = {}
	if parameters:
		paramPairs = parameters[1:].split("&")
		for paramsPair in paramPairs:
			paramSplits = paramsPair.split('=')
			if (len(paramSplits)) == 2:
				paramDict[paramSplits[0]] = paramSplits[1]
	return paramDict

def addVideoList(url, name, image):
	PL = xbmc.PlayList(1)
	listitem = xbmcgui.ListItem(name, thumbnailImage=image)
	if useThumbAsFanart:
		listitem.setArt({'fanart': defaultFanart})
	listitem.setProperty('IsPlayable', 'true')
	listitem.setContentLookup(False)
	PL.add(url, listitem)

def addLink(name, url, mode, image, plot=None):
	u = sys.argv[0]+"?url="+quote_plus(url)+"&mode="+str(mode)
	liz = xbmcgui.ListItem(name, iconImage='DefaultAudio.png', thumbnailImage=image)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': plot, 'mediatype':'video'})
	if useThumbAsFanart:
		liz.setArt({'fanart': defaultFanart})
	liz.setProperty('IsPlayable', 'true')
	liz.addContextMenuItems([(translation(30807), 'RunPlugin(plugin://{0}/?mode=addVideoList&url={1}&name={2}&image={3})'.format(addon.getAddonInfo('id'), quote_plus(u), quote_plus(name), quote_plus(image)))])
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)

def addDir(name, url, mode, image, plot=None):
	u = sys.argv[0]+"?url="+quote_plus(url)+"&mode="+str(mode)
	liz = xbmcgui.ListItem(name, iconImage='DefaultMusicVideos.png', thumbnailImage=image)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': plot})
	if useThumbAsFanart:
		liz.setArt({'fanart': defaultFanart})
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)

def addAutoPlayDir(name, url, mode, image, plot=None, type=None, limit=None):
	u = sys.argv[0]+"?url="+quote_plus(url)+"&mode="+str(mode)+"&type="+str(type)+"&limit="+str(limit)+'&image='+quote_plus(image)
	liz = xbmcgui.ListItem(name, iconImage='DefaultMusicVideos.png', thumbnailImage=image)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': plot, 'mediatype':'video'})
	if useThumbAsFanart:
		liz.setArt({'fanart': defaultFanart})
	entries = []
	entries.append([translation(30831), 'RunPlugin(plugin://'+addon.getAddonInfo('id')+'/?mode='+str(mode)+'&url='+quote_plus(url)+'&type=play&limit=)'])
	entries.append([translation(30832), 'RunPlugin(plugin://'+addon.getAddonInfo('id')+'/?mode='+str(mode)+'&url='+quote_plus(url)+'&type=play&limit=10)'])
	entries.append([translation(30833), 'RunPlugin(plugin://'+addon.getAddonInfo('id')+'/?mode='+str(mode)+'&url='+quote_plus(url)+'&type=play&limit=20)'])
	entries.append([translation(30834), 'RunPlugin(plugin://'+addon.getAddonInfo('id')+'/?mode='+str(mode)+'&url='+quote_plus(url)+'&type=play&limit=30)'])
	entries.append([translation(30835), 'RunPlugin(plugin://'+addon.getAddonInfo('id')+'/?mode='+str(mode)+'&url='+quote_plus(url)+'&type=play&limit=40)'])
	entries.append([translation(30836), 'RunPlugin(plugin://'+addon.getAddonInfo('id')+'/?mode='+str(mode)+'&url='+quote_plus(url)+'&type=play&limit=50)'])
	liz.addContextMenuItems(entries, replaceItems=False)
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)

params = parameters_string_to_dict(sys.argv[2])
name = unquote_plus(params.get('name', ''))
url = unquote_plus(params.get('url', ''))
mode = unquote_plus(params.get('mode', ''))
image = unquote_plus(params.get('image', ''))
type = unquote_plus(params.get('type', ''))
limit = unquote_plus(params.get('limit', ''))
referer = unquote_plus(params.get('referer', ''))

if mode == 'beatportMain':
	beatportMain()
elif mode == 'listBeatportVideos':
	listBeatportVideos(type, url, limit)
elif mode == 'billboardMain':
	billboardMain()
elif mode == 'listBillboardArchiveYears':
	listBillboardArchiveYears()
elif mode == 'listBillboardAR_Genres':
	listBillboardAR_Genres(url)
elif mode == 'listBillboardAR_Videos':
	listBillboardAR_Videos(type, url, limit)
elif mode == 'listBillboardCharts':
	listBillboardCharts(url)
elif mode == 'listBillboardCH_Videos':
	listBillboardCH_Videos(type, url, limit)
elif mode == 'ddpMain':
	ddpMain()
elif mode == 'listDdpYearCharts':
	listDdpYearCharts(url)
elif mode == 'listDdpVideos':
	listDdpVideos(type, url, limit)
elif mode == 'hypemMain':
	hypemMain()
elif mode == 'listHypemMachine':
	listHypemMachine()
elif mode == 'listHypemVideos':
	listHypemVideos(type, url, limit)
elif mode == 'itunesMain':
	itunesMain()
elif mode == 'listItunesVideos':
	listItunesVideos(type, url, limit)
elif mode == 'ocMain':
	ocMain()
elif mode == 'listOcVideos':
	listOcVideos(type, url, limit)
elif mode == 'spotifyMain':
	spotifyMain()
elif mode == 'listSpotifyCC_Countries':
	listSpotifyCC_Countries(url)
elif mode == 'listSpotifyCC_Videos':
	listSpotifyCC_Videos(type, url, limit)
elif mode == 'SearchDeezer':
	SearchDeezer()
elif mode == 'listDeezerArtists':
	listDeezerArtists(url) 
elif mode == 'listDeezerTracks':
	listDeezerTracks(url) 
elif mode == 'listDeezerAlbums':
	listDeezerAlbums(url)
elif mode == 'listDeezerPlaylists':
	listDeezerPlaylists(url)
elif mode == 'listDeezerUserlists':
	listDeezerUserlists(url)
elif mode == 'listDeezerVideos':
	listDeezerVideos(type, url, image, limit)
elif mode == 'playYTByTitle':
	playYTByTitle(url)
elif mode == 'addVideoList':
	addVideoList(url, name, image)
elif mode == 'Settings':
	addon.openSettings()
else:
	index()