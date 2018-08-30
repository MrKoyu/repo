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
from libs._addon import *
from libs._common import *

PodcastRss       =  BYBSC.PodcastRss()

EnableListLenght = setting_true('podcastreturnlimit')
ListLenght       = setting('podcastlistlenght')


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
		BYB.addDir(ChannelColor(title),url,201,icon,fanart,description,'Podcast','','')
		del PodcastRss.CHANNEL[:]

def AddEpisodes(url,fanart):
	if EnableListLenght == True:
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
		BYB.addDir_file(ItemColor(title),playlink,33,icon,fanart,description,'Podcast','','')



def _image(image,fanart):
	if image == '':
		icon = addon_icon
		fanart = addon_fanart
	else:
		icon = image
		if fanart =='':
			if _Edit.PodcastFanart:
				fanart = image
			else:
				fanart = addon_fanart
	return icon,fanart