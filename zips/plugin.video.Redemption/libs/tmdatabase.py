# -*- coding: utf-8 -*-
#modes 500-600
import base64 
import byb_modules as BYB 
import byb_api as BYBAPI 
import datetime
from dateutil.parser import parse as dparser
import _Edit
import koding
import re

from libs._addon import *
from libs._common import *

Dolog = koding.dolog
#string = '<externallink>tmdb=(movie|tv|company*|network*|**list):list_id=(**list id|company id*|network id*):list_type=(latest|popular|nowplaying|toprated|upcoming|movies*|tv*):=list</externallink>'
def tmdb_list(url):
	imdb = ''
	debrid = False
	ApiKey = apikey()
	Page = '1'
	PageTotal = '0'
	if not 'page=' in url:
		ListAssign = url.replace('=:','=none:')
		ListAssignItems =re.compile( r'tmdb=(.+?):list_id=(.+?):list_type=(.+?):=list').findall(ListAssign)
		for ListHeader,ListId,ListType in ListAssignItems:
			if ListHeader.lower() == 'list':
				BYBAPI.tmdb_list_get_items(ApiKey,ListId)
			elif ListHeader.lower() == 'company':
				BYBAPI.tmdb_company_get_results(ApiKey,ListId,ListType)
				Page,PageTotal = BYBAPI.tmdb_company_get_results_page_counter(ApiKey,ListId,ListType)
			elif ListHeader == 'movie' or ListHeader == 'tv':
				BYBAPI.tmdb_movietv_get_lists(ApiKey,ListHeader,ListType)
				Page,PageTotal = BYBAPI.tmdb_movietv_get_lists_page_counter(ApiKey,ListHeader,ListType)
			elif ListHeader.lower() == 'network':
				BYBAPI.tmdb_networks_get_results(ApiKey,ListId)
				Page,PageTotal = BYBAPI.tmdb_networks_get_results_page_counter(ApiKey,ListId)
				Dolog('Page={} PageTotal={}'.format(Page,PageTotal),line_info=True)
	elif 'page=' in url:
		ListAssign = url.replace('=:','=none:')
		ListAssignItems =re.compile( r'tmdb=(.+?):list_id=(.+?):list_type=(.+?):page=(.+?):=list').findall(ListAssign)
		for ListHeader,ListId,ListType,Page in ListAssignItems:
			if ListHeader.lower() == 'list':
				BYBAPI.tmdb_list_get_items(ApiKey,ListId)
			elif ListHeader.lower() == 'company':
				BYBAPI.tmdb_company_get_results(ApiKey,ListId,ListType,Page)
				Page,PageTotal = BYBAPI.tmdb_company_get_results_page_counter(ApiKey,ListId,ListType,Page)
			elif ListHeader == 'movie' or ListHeader == 'tv':
				BYBAPI.tmdb_movietv_get_lists(ApiKey,ListHeader,ListType,Page)
				Page,PageTotal = BYBAPI.tmdb_movietv_get_lists_page_counter(ApiKey,ListHeader,ListType,Page)
			elif ListHeader.lower() == 'network':
				BYBAPI.tmdb_networks_get_results(ApiKey,ListId,Page)
				Page,PageTotal = BYBAPI.tmdb_networks_get_results_page_counter(ApiKey,ListId,Page)
	for items in BYBAPI.Details_list:
		name = items.get('title','Title Missing')
		date = items.get('release_date','')
		Year = date.split('-')[0]
		MediaType = items.get('mediatype','').lower()
		TmdbDataString = ''
		if _Edit.TMDBMovieList == 'search_addon':
			mode = 404
			TmdbDataString = 'tmdb={}'.format(items.get('ID',''))
		elif _Edit.TMDBMovieList == 'search_internet':
			if MediaType == 'movie' or ListHeader == 'movie' or ListType == 'movies':
				mode = 600 
				TmdbDataString = '#search=movies:name={}:year={}:imdb={}:debrid={}'.format(name.encode('utf-8', 'ignore').strip(':'),Year,imdb,debrid)
			elif MediaType == 'tv' or ListHeader == 'tv' or ListType == 'tv':
				mode = 501
				TmdbDataString = str(items.get('ID',''))
		Name = name if len(name) > 0 else 'Name Missing'
		Name = '{}'.format(Name.encode('utf-8', 'ignore').strip(':'))
		BYB.addDir(ChannelColor(Name),TmdbDataString,mode,items.get('poster_path',icon_tmdb),items.get('backdrop_path',fanart_tmdb),items.get('overview','').encode('utf-8', 'ignore'),items.get('Genres',''),date.encode('utf-8','ignore'),'')
	if int(Page)+1 <= int(PageTotal):
		NextPage =  str(int(Page) + 1)
		BYB.addDir(ChannelColor('Next Page {}'.format(NextPage)),'tmdb={}:list_id={}:list_type={}:page={}:=list'.format(ListHeader,ListId,ListType,NextPage),500,icon_nextpage,addon_fanart,'Next Page {} of {}'.format(NextPage,PageTotal),'','','')


def apikey():
	if _Edit.UseTMDB :
	    if _Edit.TMDB_api != '':
	        TMDB_api = base64.b64decode(_Edit.TMDB_api)
	    elif _Edit.TMDB_api == '':
	        TMDB_api = setting('tmdb_key')
	    if len(_Edit.TMDB_api) > 0 and len(setting('tmdb_key')) > 0:
	        TMDB_api = setting('tmdb_key')
	else:
		Dolog('Check _Edit.py settings of UseTMDB',line_info=True)
		TMDB_api = None 
	return TMDB_api


def tmdb_seasons(url,fanart,iconimage):
	ApiKey = apikey()
	seasons = BYBAPI.tmdb_tv_total_seasons(ApiKey,url)
	if int(seasons) > 1:
		BYBAPI.tmdb_tv_show_get_seasons(url,ApiKey)
		for items in BYBAPI.Details_list:
			ID = items.get('ID','')
			overview = items.get('overview','')
			season_number = items.get('season_number','')
			info_string = 'ID={}:season={}:'.format(ID,season_number)
			description = '{} Episodes: {}'.format(items.get('episode_count',''),overview.encode('utf-8'))
			BYB.addDir(ChannelColor(items.get('name','').encode('utf-8')),info_string,502,items.get('poster_path',addon_icon),fanart,description,'','','')
	else:
		tmdb_season_episodes(fanart,'ID={}:season=1:'.format(url),iconimage)
	del BYBAPI.Details_list[:]

def tmdb_season_episodes(fanart,url,iconimage):
	ApiKey = apikey()
	ID,season = re.findall('ID=(.*[0-9]):season=(.*[0-9]):',url)[0]
	BYBAPI.tmdb_tv_show_get_season_episodes(ID,season,ApiKey)
	EpisodeStartNo = int(BYBAPI.Details_list[0].get('episode_number',''))
	ShowName = BYBAPI.tmdb_tv_show_title(ID,ApiKey)
	for items in BYBAPI.Details_list:
		episode_number = items.get('episode_number','')
		if episode_number != '' or episode_number != None:
			if EpisodeStartNo != 1:
				episode_number = str(int(episode_number)+1)
			else:
				episode_number = episode_number
		icon=items.get('still_path','')
		if icon == '' or icon == None or not icon.endswith(('.png','.jpg')):
			icon = iconimage
		try:
			AirDate = items.get('air_date','').encode('utf-8','ignore')
		except:
			AirDate = ''
		try:
			year = dparser(AirDate)
			year = datetime.date.strftime(year,'%Y')
		except:
			year = ''
		name = items.get('name','')
		if len(name) == 0:
			name = ShowName.encode('utf-8','ignore')
		else:
			name = name.encode('utf-8','ignore')
		
		try:
			description =  items.get('overview','').encode('utf-8','ignore')
		except:
			description = ''
		SearchString = '#search=tv:name={}:show_year=:year={}:season={}:episode={}:imdb=:tvdb=:debrid='.format(ShowName,year,season,episode_number)
		Dolog(SearchString,line_info=True)
		try:
			BYB.addDir(ItemColor('{}. {}'.format(episode_number,name)),SearchString,600,icon,fanart,description,'',AirDate,'')
		except:pass
	del BYBAPI.Details_list[:]


