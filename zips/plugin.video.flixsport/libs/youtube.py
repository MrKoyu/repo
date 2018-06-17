import byb_scrapers as byb 
import byb_modules as BYB 
import _Edit
import koding
import sys
import xbmc
import xbmcplugin

YouTube_Scraper = byb.YouTube_Scraper()


def AddChannel(name,linkedUrl,thumbnail,fanArt,desc,genre,date,credits):
	YouTube_Scraper.channel_info(channel_url=linkedUrl)
	for items in YouTube_Scraper.CHANNEL_INFO:
		title = items.get('title','Title Missing')
		description = items.get('description','')
		icon = items.get('icon','')
		artwork = items.get('artwork','')
		channel_url = items.get('channel_url','')
		if name == '':
			name = title
		if thumbnail == '':
			thumbnail = icon
		if fanArt == '':
			fanArt = artwork
		if desc == '':
			desc = description
		BYB.addDir(name,linkedUrl,28,iconimage=thumbnail,fanart=fanArt,description=desc,genre=genre,date=date,credits=credits)
		del YouTube_Scraper.CHANNEL_INFO[:]


def indexs(name,url,iconimage,fanart):
	BYB.addDir('Videos',url,29,iconimage,fanart,'','','','')
	BYB.addDir('PlayLists',url,31,iconimage,fanart,'','','','')
	BYB.addDir('Search this Channel',url,32,iconimage,fanart,'','','','')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def videos(url,fanart):
	YouTube_Scraper.channel_video(url)
	for items in YouTube_Scraper.CHANNEL_VIDEO:
		title = items.get('title','Title Missing')
		playlink = items.get('playlink','')
		icon = items.get('icon','')
		date = items.get('date','')
		description = items.get('description','')
		BYB.addDir_file(title,playlink,33,icon,fanart,description,'',date,'')
	del YouTube_Scraper.CHANNEL_VIDEO[:]


def playlist_lists(url,iconimage,fanart):
	YouTube_Scraper.channel_playlist(url)
	for items in YouTube_Scraper.CHANNEL_PLAYLIST:
		PlayListName = items.get('playlist_name','Name Missing')
		PlayListUrl = items.get('playlist_url','')
		BYB.addDir(PlayListName,PlayListUrl,34,iconimage,fanart,'','','','')

def playlist_video(url,fanart):
	YouTube_Scraper.channel_playlist_video(url)
	for items in YouTube_Scraper.CHANNEL_VIDEO:
		title = items.get('title','Title Missing')
		playlink = items.get('playlink','')
		icon = items.get('icon','')
		date = items.get('date','')
		description = items.get('description','')
		BYB.addDir_file(title,playlink,33,icon,fanart,description,'',date,'')
	del YouTube_Scraper.CHANNEL_VIDEO[:]

def channel_search(url,fanart):
	search_item = koding.Keyboard(heading='Search Item')
	koding.dolog('search item = %s'%search_item,line_info=True)
	YouTube_Scraper.channel_search(url,search_item)
	for items in YouTube_Scraper.CHANNEL_SEARCH:
		title = items.get('title','Title Missing')
		playlink = items.get('playlink','')
		icon = items.get('artwork','')
		date = items.get('date','')
		description = items.get('description','')
		BYB.addDir_file(title,playlink,33,icon,fanart,description,'',date,'')

def search(search_item=None):
	if search_item == None:
		search_item = koding.Keyboard(heading='Search Item')
		koding.dolog('search item = %s'%search_item,line_info=True)
	if _Edit.YT_SearchFanart == '':
		fanart = koding.Addon_Info('fanart')
	else:
		fanart = _Edit.YT_SearchFanart
	YouTube_Scraper.search(search_item)
	for items in YouTube_Scraper.SEARCH_VIDEO:
		title = items.get('title','Title Missing')
		playlink = items.get('playlink','')
		icon = items.get('icon')
		BYB.addDir_file(title,playlink,33,icon,fanart,'','','','')


def play(url):
	Play = xbmc.Player()
	try:
		Play.play(url)
	except:pass
