import byb_api as BYBAPI
import byb_modules as BYB 
import datetime
import dateutil.parser as dparser
import _Edit
import koding
from os.path import join
import xbmc
import xbmcaddon


addon           = addon = xbmcaddon.Addon()
addoninfo       = addon.getAddonInfo
addon_path      = xbmc.translatePath(addoninfo('path').decode('utf-8'))
addon_resources = join(addon_path, 'resources')
addon_art       = join(addon_resources,'art')
setting         = addon.getSetting
setting_true    = lambda x: bool(True if setting(str(x)) == "true" else False)
#Addon info
addon_name      = addoninfo('name')
addon_fanart    = addoninfo('fanart')
#art work 
icon_tmdb       = join(addon_art,'tmdb.png')            if _Edit.TmdbIcon           == "" else _Edit.TmdbIcon
fanart_tmdb     = addon_fanart                          if _Edit.TmdbFanart         == "" else _Edit.TmdbFanart

addDir          = BYB.addDir
table           ='tmdbapisession'
DateTimeNow     = datetime.datetime.today()

def CreateSession(apikey):
	Auth,SessionId,StatusMessageSession  = BYBAPI.tmdb_session(apikey)
	columns = { "columns":{"auth":"TEXT", "sessionid":"TEXT","statusmessage":"TEXT","sessiontime":"TEXT"} }
	koding.Create_Table(table, columns)
	if Auth == False:
		BYB.Notify(title= str(addon_name),message='Failed to create session\nBecause '+str(StatusMessageSession)+'\nPlease check settings if using own API Key')
	else:
		add = {"auth":Auth, "sessionid":SessionId,"statusmessage":StatusMessageSession,"sessiontime":DateTimeNow}
		koding.Add_To_Table(table, add)
	return Auth,SessionId,StatusMessageSession

def CheckSession(apikey):
	hour = datetime.timedelta(minutes=60)
	results = koding.Get_All_From_Table(table)
	for item in results:
		Auth = item.get('auth',False)
		Auth = True if Auth == 'True' else False
		SessionId = item.get('sessionid','')
		StatusMessageSession = item.get('statusmessage','')
		SessionTime = item.get('sessiontime','2018-04-30 23:25:13.671000')
		SessionTime = dparser.parse(SessionTime)
		EndSessionTime = SessionTime+hour
	if DateTimeNow > EndSessionTime:
		BYB.Notify(title=str(addon_name),message='TMDB Session has expired creating new one')
		koding.Remove_Table(table)
		Auth,SessionId,StatusMessageSession = CreateSession(apikey)
	return Auth,SessionId,StatusMessageSession

def index(url):
	apikey = url
	Auth,SessionId,StatusMessageSession = CheckSession(apikey)
	if Auth == True:
		addDir('My Favorite Movies',SessionId+'+'+apikey,303,icon_tmdb,fanart_tmdb,'','','','')
		addDir('My Favorite TV Shows',SessionId+'+'+apikey,303,icon_tmdb,fanart_tmdb,'','','','')
		addDir('My Rated Movies',SessionId+'+'+apikey,303,icon_tmdb,fanart_tmdb,'','','','')
		addDir('My Rated TV Shows',SessionId+'+'+apikey,303,icon_tmdb,fanart_tmdb,'','','','')
		addDir('My Watchlist Movies',SessionId+'+'+apikey,303,icon_tmdb,fanart_tmdb,'','','','')
		addDir('My Watchlist TV Shows',SessionId+'+'+apikey,303,icon_tmdb,fanart_tmdb,'','','','')



def MyLists(name,url):
	Name = name.lower().lstrip('my').strip()
	content_type = 'movies' if 'movies' in Name else 'tv'
	list_type = Name.split(' ')[0]
	koding.dolog(url,line_info=True)
	session_id,apikey = url.split('+')
	BYBAPI.tmdb_my_lists(apikey,session_id,content_type,list_type)
	for items in BYBAPI.Details_list:
		addDir(items.get('title','Title Missing'),'tmdb='+items.get('ID',''),404,items.get('poster_path',icon_tmdb),items.get('backdrop_path',fanart_tmdb),items.get('overview',''),'',items.get('release_date',''),'','')





'''POST
Mark as Favorite
POST
Add to Watchlist'''



	







