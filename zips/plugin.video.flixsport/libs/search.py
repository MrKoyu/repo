import byb_modules as BYB
import byb_api as BYBAPI  
import _Edit
import koding
import sys
import xbmcplugin
from libs._addon import *

# search functions use mode 400 - 500 

addDir = BYB.addDir

def index(url):
	if _Edit.Search_Tv == True:
		addDir('Search TV Shows',url,401,icon_Search,fanart_Search,'Search Addon for TV Shows','TV Shows','','')
	if _Edit.Search_Movies == True:
		addDir('Search Movies',url,402,icon_Search,fanart_Search,'Search Addon for Movies','Movies','','')
	if _Edit.Search_Content == True:
		addDir('Search Addon','',40,icon_Search,fanart_Search,'Search Addon for cotent','videos','','')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def SearchTv(url):
	#search tv shows using TMDB api list
	SearchString = koding.Keyboard('Enter Name of TV')
	BYBAPI.tmdb_search(url,search_type='tv',search_term=SearchString,total_pages=1)
	for items in BYBAPI.Details_list:
		addDir(items.get('title','').encode('utf-8'),'tmdb='+items.get('ID',''),404,items.get('poster_path',icon_Search),items.get('backdrop_path',fanart_Search),items.get('overview','').encode('utf-8'),str(items.get('Genres','')).encode('utf-8'),items.get('release_date','').encode('utf-8'),'')
	del BYBAPI.Details_list[:]




def SearchMovie(url):
	SearchString = koding.Keyboard('Enter Name of Movie')
	BYBAPI.tmdb_search(url,search_type='movie',search_term=SearchString,total_pages=1)
	for items in BYBAPI.Details_list:
		addDir(items.get('title','').encode('utf-8'),'tmdb='+items.get('ID',''),404,items.get('poster_path',icon_Search),items.get('backdrop_path',fanart_Search),items.get('overview','').encode('utf-8'),str(items.get('Genres','')).encode('utf-8'),items.get('release_date','').encode('utf-8'),'')
	del BYBAPI.Details_list[:]

