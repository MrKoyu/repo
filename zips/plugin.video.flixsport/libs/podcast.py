import byb_modules as BYB
import byb_scrapers as BYBSC
import _Edit  
import koding
import os 
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

PodcastRss       =  BYBSC.PodcastRss()
addon            = _Edit.addon
AddonIcon        = addon.getAddonInfo('icon')
AddonFanart      = addon.getAddonInfo('fanart')
EnableListLenght = addon.getSetting('podcastreturnlimit')
ListLenght       = addon.getSetting('podcastlistlenght')


def addcontent(url,fanart):
	url = url.lstrip('#podcast=')
	koding.dolog('adding podcast content url='+str(url),line_info=True)
	if url.startswith('http'):
		AddAllContent(url,fanart)
	elif url.startswith('episode'):
		url = url.lstrip('episode=')
		AddEpisodes(url,fanart)
	#elif url.startswith('channel') 

def AddAllContent(url,fanart):
	PodcastRss.Channel(url)
	for channel in PodcastRss.CHANNEL:
		title = channel.get('title','Title Missing')
		description = channel.get('description','')
		image = channel.get('image','')
		icon,fanart = _image(image,fanart)
		url = channel.get('rss_url','')
		BYB.addDir(title,url,201,icon,fanart,description,'Podcast','','')
		del PodcastRss.CHANNEL[:]

def AddEpisodes(url,fanart):
	if EnableListLenght == 'true':
		itemcount = PodcastRss.ItemCount(url)
		if itemcount > int(ListLenght):
			PodcastRss.Items(url,ListLenght)
		else:
			PodcastRss.Items(url)
	else:
		PodcastRss.Items(url)
	for item in PodcastRss.ITEM:
		koding.dolog(item,line_info=True)
		title = item.get('title','Title Missing')
		image = item.get('image','')
		description = item.get('description','description missing')
		date = item.get('date','')
		playlink = item.get('playlink','')
		icon,fanart = _image(image,fanart)
		BYB.addDir_file(title,playlink,33,icon,fanart,description,'Podcast','','')



def _image(image,fanart):
	if image == '':
		icon = AddonIcon
		fanart = AddonFanart
	else:
		icon = image
		if fanart =='':
			if _Edit.PodcastFanart:
				fanart = image
			else:
				fanart = AddonFanart
	return icon,fanart