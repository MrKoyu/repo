 #############Imports#############
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,base64,os,re,unicodedata,requests,time,string,sys,urllib,urllib2,json,urlparse,datetime,zipfile,shutil,plugintools
from resources.modules import client,control,tools,shortlinks
from resources.ivue import ivuesetup
from datetime import date
import xml.etree.ElementTree as ElementTree
import difflib
#################################

#############Defined Strings#############
addon_id     = 'plugin.video.hypersonicIPTV2'
selfAddon    = xbmcaddon.Addon(id=addon_id)
icon         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
search2      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'search2.gif'))
canada         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'canada.png'))
system       = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/system.png'))
airing       = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/airing.png'))
guide         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/guide.png'))
extra         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/extra.png'))
catch         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/catch.png'))
vodtv         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/vodtv.png'))
american       = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/american.png'))
britsh       = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/britsh.png'))
international         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/international.png'))
music         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/music.png'))
adult         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/adult.png'))
ppv         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/ppv.png'))
mlb         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/mlb.png'))
sports2         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/sports2.png'))
nba         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/nba.png'))
nfl         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/nfl.png'))
cache         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/cache.png'))
nhl         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/nhl.png'))
speed         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/speed2.png'))
ncaa         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/ncaa.png'))
mls         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/mls.png'))
topenglish         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/topenglish.png'))
entertainment         = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/CellarDoorTV/CDTV/master/Infusion_icons/enter.png'))

username     = control.setting('Username')
password     = control.setting('Password')
adultset     = control.setting('Adult.Set')
adultpwset      = control.setting('Adult.PWSet')
adultpw = control.setting('Adult.PW')

host         = 'http://main.tvstreams.xyz'
port         = '83'

live_url     = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_categories'%(host,port,username,password)
vod_url      = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,port,username,password)
panel_api    = '%s:%s/panel_api.php?username=%s&password=%s'%(host,port,username,password)
play_url     = '%s:%s/live/%s/%s/'%(host,port,username,password)

#CATEGORIES
All='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=0'%(host,port,username,password)
USA_Entertainment='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1'%(host,port,username,password)
USA_Sports='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=689'%(host,port,username,password)
USA_SPORTS_REGIONALS='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1159'%(host,port,username,password)
UK_Entertainment='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=691'%(host,port,username,password)
UK_Sports_2='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=690'%(host,port,username,password)
UK_Movies='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=693'%(host,port,username,password)
UK_News='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1214'%(host,port,username,password)
UK_Documentaries='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=692'%(host,port,username,password)
UK_Kids='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=694'%(host,port,username,password)
Canada='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=665'%(host,port,username,password)
Canada_News='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1186'%(host,port,username,password)
Canada_Movies='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1177'%(host,port,username,password)
Canada_Reality='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1178'%(host,port,username,password)
Canada_Kids='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1179'%(host,port,username,password)
Canadian_Sports='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=713'%(host,port,username,password)
CARIBBEAN='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1213'%(host,port,username,password)
PPV___Live_Events='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=41'%(host,port,username,password)
PPV_Replay='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1164'%(host,port,username,password)
Music_Choice='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=669'%(host,port,username,password)
TwentyFourSeven='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=18'%(host,port,username,password)
NBC_GOLD___Premier_League='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1188'%(host,port,username,password)
All_Sports='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=16'%(host,port,username,password)
NFL_Package='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=10'%(host,port,username,password)
NHL_Package='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=11'%(host,port,username,password)
NBA_Package='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=12'%(host,port,username,password)
MLB_Package='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=13'%(host,port,username,password)
NCAAB='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=59'%(host,port,username,password)
NCAAF='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=58'%(host,port,username,password)
International_Sports='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=9'%(host,port,username,password)
SOUTH_AMERICA='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1189'%(host,port,username,password)
Australia='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1184'%(host,port,username,password)
Africa='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=43'%(host,port,username,password)
Albania='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=44'%(host,port,username,password)
Arabic='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=56'%(host,port,username,password)
Armenia='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=17'%(host,port,username,password)
Belgium='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1320'%(host,port,username,password)
Brazil='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=45'%(host,port,username,password)
Bulgaria='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=53'%(host,port,username,password)
#China='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1317'%(host,port,username,password)
Czech_Republic='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=26'%(host,port,username,password)
USNEWS='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=65'%(host,port,username,password)
EX_YU='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=28'%(host,port,username,password)
EGYPT='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1367'%(host,port,username,password)
France='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=47'%(host,port,username,password)
German='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=52'%(host,port,username,password)
Greek='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=29'%(host,port,username,password)
Hungary='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=46'%(host,port,username,password)
India='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=48'%(host,port,username,password)
Indonesia='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1370'%(host,port,username,password)
#Iran='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=31'%(host,port,username,password)
Irish='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1180'%(host,port,username,password)
Israel='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1319'%(host,port,username,password)
direct_test='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=662'%(host,port,username,password)
Japan='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=34'%(host,port,username,password)
Korea='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=35'%(host,port,username,password)
Latino='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=24'%(host,port,username,password)
#Macedonia='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=51'%(host,port,username,password)
Netherlands='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=36'%(host,port,username,password)
Pakistan='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=54'%(host,port,username,password)
Persian='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=22'%(host,port,username,password)
Philippines='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1318'%(host,port,username,password)
Polish='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=21'%(host,port,username,password)
Portugal='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=55'%(host,port,username,password)
Romania='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=50'%(host,port,username,password)
Russia='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=49'%(host,port,username,password)
Spain='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1174'%(host,port,username,password)
Denmark='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=38'%(host,port,username,password)
Sweden='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1330'%(host,port,username,password)
#Switzerland='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1331'%(host,port,username,password)
Italy='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=33'%(host,port,username,password)
Turkish='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=40'%(host,port,username,password)
#Vietnam='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=62'%(host,port,username,password)
Adult='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=23'%(host,port,username,password)
twentyfourseven_Kids='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1176'%(host,port,username,password)
twentyfourseven_Movies='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=709'%(host,port,username,password)
twentyfourseven_TV='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=18'%(host,port,username,password)
USA_Reality='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=706'%(host,port,username,password)
USA_LOCAL_NETWORKS='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1375'%(host,port,username,password)
USA_KIDS='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=702'%(host,port,username,password)
USA__Movies='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=707'%(host,port,username,password)
USA_Music='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1216'%(host,port,username,password)

Guide = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.hypersonicIPTV2/resources/catchup', 'guide.xml'))
GuideLoc = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.hypersonicIPTV2/resources/catchup', 'g'))

advanced_settings           =  xbmc.translatePath('special://home/addons/'+addon_id+'/resources/advanced_settings')
advanced_settings_target    =  xbmc.translatePath(os.path.join('special://home/userdata','advancedsettings.xml'))

USER_DATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDON_DATA   =  xbmc.translatePath(os.path.join(USER_DATA,'addon_data'))
durextvfol = xbmc.translatePath(os.path.join(ADDON_DATA,'plugin.video.hypersonicIPTV2'))
durextvset = xbmc.translatePath(os.path.join(ADDON_DATA,'settings.xml'))
ini          =  xbmc.translatePath(os.path.join('special://home/addons/plugin.video.hypersonicIPTV2/resources/ivue','addons_index.ini'))
inizip       = 	xbmc.translatePath(os.path.join('special://home/addons/plugin.video.hypersonicIPTV2/resources/ivue','addons_index.zip'))
tmpini       =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ivuetarget   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.ivueguide/'))
ivueaddons2ini   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.ivueguide/addons2.ini'))
ivuecreate   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.IVUEcreator/'))
ivuecreateini   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.IVUEcreator/addons_index.ini'))
PVRSimple   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/pvr.iptvsimple/settings.xml'))
databasePath = xbmc.translatePath('special://profile/addon_data/script.ivueguide')
subPath = xbmc.translatePath('special://profile/addon_data/script.ivueguide/resources/ini')
pyPath = xbmc.translatePath('special://profile/addon_data/script.ivueguide/resources/subs')
setupPath = xbmc.translatePath('special://profile/addon_data/script.ivueguide/resources/guide_setups')
drxaddons2ini = xbmc.translatePath('special://profile/addon_data/script.ivueguide/addons2.ini')
dialog = xbmcgui.Dialog()
#########################################
def start():
	if username=="":
		user = userpopup()
		passw= passpopup()
		control.setSetting('Username',user)
		control.setSetting('Password',passw)
		#xbmc.executebuiltin('Container.Refresh')
		auth = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,port,user,passw)
		auth = tools.OPEN_URL(auth)
		if auth == "":
			line1 = "[COLOR red]Incorrect Login Details![/COLOR]"
			line2 = "Please Re-enter" 
			line3 = "To unlock your TV PRO go to:[COLOR yellowgreen] http://getnow.hypersonic-tv.com[/COLOR]" 
			xbmcgui.Dialog().ok('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]', line1, line2, line3)
			start()
		else:
			line1 = "[COLOR lime]Login Successfull![/COLOR]"
			line2 = "Welcome to [COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]" 
			line3 = ('[COLOR blue]%s[/COLOR]'%user)
			xbmcgui.Dialog().ok('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]', line1, line2, line3)
			addonsettings('ADS2','')
			adult_settings()
			xbmc.executebuiltin('Container.Refresh')
			home()
	else:
		auth = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,port,username,password)
		auth = tools.OPEN_URL(auth)
		if not auth=="":
			tools.addDir('[B][COLOR white]=-=-=-=-=[/COLOR][/B] [B][COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR][/B] [B][COLOR white]=-=-=-=-=[/COLOR][/B]','','',icon,fanart,'')
			tools.addDir('[COLOR white]Account Information[/COLOR]','url',6,icon,fanart,'')
			tools.addDir('[COLOR yellowgreen]Live TV[/COLOR]','live',21,airing,fanart,'')
			#if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
				#tools.addDir('[COLOR yellowgreen]Simple PVR Client TV Guide[/COLOR]','pvr',7,guide,fanart,'')
			#if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
				#tools.addDir('[COLOR yellowgreen]Simple PVR Client Channels Guide[/COLOR]','pvr',45,icon,fanart,'')
			tools.addDir('[COLOR yellowgreen]Video on Demand[/COLOR]','vod',3,vodtv,fanart,'')
			tools.addDir('[COLOR yellowgreen]24/7[/COLOR]','url',49,catch,fanart,'')
			tools.addDir('[COLOR yellowgreen]Music Channels[/COLOR]',Music_Choice,25,music,fanart,'')
			tools.addDir('[COLOR white]Search[/COLOR]','url',5,search2,fanart,'')
			#tools.addDir('[COLOR white]Search VOD[/COLOR]','url',43,icon,fanart,'')
			tools.addDir('[B][COLOR white]=-=-=-=-=[/COLOR][/B] [B][COLOR steelblue]TOOLS[/COLOR][/B] [B][COLOR white]=-=-=-=-=[/COLOR][/B]','','',icon,fanart,'')
			#tools.addDir('[COLOR white]Setup Simple PVR[/COLOR]','tv',11,guide,fanart,'')
			tools.addDir('[COLOR white]Clear Cache[/COLOR]','CC',10,cache,fanart,'')
			tools.addDir('[COLOR white]Extras[/COLOR]','url',16,extra,fanart,'')
			tools.addDir('[COLOR white]Settings[/COLOR]','url',8,system,fanart,'')
			tools.addDir('[COLOR gray]Original Playlist[/COLOR]','live',1,icon,fanart,'')
			tools.addDir('[COLOR gray]Test[/COLOR]','live',37,icon,fanart,'')
			plugintools.set_view( plugintools.LIST )
			setView()
def home():
	tools.addDir('[B][COLOR white]=-=-=-=-=[/COLOR][/B] [B][COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR][/B] [B][COLOR white]=-=-=-=-=[/COLOR][/B]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Account Information[/COLOR]','url',6,icon,fanart,'')
	tools.addDir('[COLOR yellowgreen]Live TV[/COLOR]','live',21,airing,fanart,'')
	#if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
		#tools.addDir('[COLOR yellowgreen]TV Guide[/COLOR]','pvr',7,guide,fanart,'')
	#if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
		#tools.addDir('[COLOR yellowgreen]Channels Guide[/COLOR]','pvr',45,icon,fanart,'')
	tools.addDir('[COLOR yellowgreen]Video on Demand[/COLOR]','vod',3,vodtv,fanart,'')
	tools.addDir('[COLOR yellowgreen]24/7[/COLOR]','url',49,catch,fanart,'')
	tools.addDir('[COLOR yellowgreen]Music Channels[/COLOR]',Music_Choice,25,music,fanart,'')
	tools.addDir('[COLOR white]Search[/COLOR]','url',5,search2,fanart,'')
	#tools.addDir('[COLOR white]Search VOD[/COLOR]','url',43,icon,fanart,'')
	tools.addDir('[B][COLOR white]=-=-=-=-=[/COLOR][/B] [B][COLOR steelblue]TOOLS[/COLOR][/B] [B][COLOR white]=-=-=-=-=[/COLOR][/B]','','',icon,fanart,'')
	#tools.addDir('[COLOR white]Setup Simple PVR[/COLOR]','tv',11,guide,fanart,'')
	tools.addDir('[COLOR white]Clear Cache[/COLOR]','CC',10,cache,fanart,'')
	tools.addDir('[COLOR white]Extras[/COLOR]','url',16,extra,fanart,'')
	tools.addDir('[COLOR white]Settings[/COLOR]','url',8,system,fanart,'')
	tools.addDir('[COLOR gray]Original Playlist[/COLOR]','live',1,icon,fanart,'')
	tools.addDir('[COLOR gray]Test[/COLOR]','live',37,icon,fanart,'')
	plugintools.set_view( plugintools.LIST )
	setView()
	
def NEW_MENU():
	tools.addDir('[B][COLOR white]=-=-=-=-=-=-=-=-=-=[/COLOR][/B] [B][COLOR steelblue]LIVE TV[/COLOR][/B] [B][COLOR white]=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','','',icon,fanart,'')
	tools.addDir('[COLOR white]All Channels[/COLOR]',All,2,icon,fanart,'')
	tools.addDir('[COLOR gold]PPV/Live Events[/COLOR]',PPV___Live_Events,25,ppv,fanart,'')
	#tools.addDir('[COLOR gold]PPV Replay[/COLOR]',PPV_Replay,25,ppv,fanart,'')
	tools.addDir('[COLOR crimson]US[/COLOR]',url,22,american,fanart,'')
	tools.addDir('[COLOR blue]UK[/COLOR]',url,23,britsh,fanart,'')
	tools.addDir('[COLOR red]CA[/COLOR]',url,50,canada,fanart,'')
	tools.addDir('[COLOR yellowgreen]International[/COLOR]',url,24,international,fanart,'')
	#tools.addDir('[COLOR white]All Sports[/COLOR]',All_Sports,25,icon,fanart,'')
	if adultset == "false":
		tools.addDir('[COLOR pink]Adult[/COLOR]',Adult,25,adult,fanart,'')
	tools.addDir('[COLOR gray]Original Playlist[/COLOR]','live',1,icon,fanart,'')
	tools.addDir('[B][COLOR white]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Clear Cache[/COLOR]','CC',10,cache,fanart,'')
	tools.addDir('[COLOR white]Search[/COLOR]','url',5,search2,fanart,'')
	setView()

	
def US():
	tools.addDir('[B][COLOR white]=-=-=-=-=-=-=-=-=-=[/COLOR][/B] [B][COLOR crimson]US LIVE[/COLOR][/B] [B][COLOR white]=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','','',american,fanart,'')
	tools.addDir('[COLOR white]US Entertainment[/COLOR]',USA_Entertainment,25,entertainment,fanart,'')
	tools.addDir('[COLOR white]US Reality[/COLOR]',USA_Reality,25,icon,fanart,'')
	tools.addDir('[COLOR white]US Networks[/COLOR]',USA_LOCAL_NETWORKS,25,icon,fanart,'')
	tools.addDir('[COLOR white]US Music[/COLOR]',USA_Music,25,icon,fanart,'')
	tools.addDir('[COLOR white]US Kids[/COLOR]',USA_KIDS,25,icon,fanart,'')
	tools.addDir('[COLOR white]US Premium Movies[/COLOR]',USA__Movies,25,icon,fanart,'')
	tools.addDir('[COLOR white]US News[/COLOR]',USNEWS,25,icon,fanart,'')	
	tools.addDir('[COLOR white]--------[/COLOR] [COLOR crimson][B]US SPORTS[/B][/COLOR] [COLOR white]--------[/COLOR]','','',american,fanart,'')
	tools.addDir('[COLOR white]US Sports[/COLOR]',USA_Sports,25,topenglish,fanart,'')
	tools.addDir('[COLOR white]US Sports Regionals[/COLOR]',USA_SPORTS_REGIONALS,25,topenglish,fanart,'')
	tools.addDir('[COLOR white]NFL[/COLOR]',NFL_Package,25,nfl,fanart,'')
	tools.addDir('[COLOR white]NBA[/COLOR]',NBA_Package,25,nba,fanart,'')
	tools.addDir('[COLOR white]NHL[/COLOR]',NHL_Package,25,nhl,fanart,'')
	tools.addDir('[COLOR white]MLB[/COLOR]',MLB_Package,25,mlb,fanart,'')
	#tools.addDir('[COLOR white]NCAAF[/COLOR]',NCAAF,25,ncaa,fanart,'')
	#tools.addDir('[COLOR white]NCAAB[/COLOR]',NCAAB,25,ncaa,fanart,'')
	tools.addDir('[B][COLOR white]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Clear Cache[/COLOR]','CC',10,cache,fanart,'')
	tools.addDir('[COLOR white]Search[/COLOR]','url',5,search2,fanart,'')
	setView()
	
def UK():
	tools.addDir('[B][COLOR white]=-=-=-=-=-=-=-=-=-=[/COLOR][/B] [B][COLOR blue]UK LIVE[/COLOR][/B] [B][COLOR white]=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','','',britsh,fanart,'')
	tools.addDir('[COLOR white]UK Entertainment[/COLOR]',UK_Entertainment,25,entertainment,fanart,'')
	tools.addDir('[COLOR white]UK News[/COLOR]',UK_News,25,icon,fanart,'')
	tools.addDir('[COLOR white]UK Movies[/COLOR]',UK_Movies,25,icon,fanart,'')
	tools.addDir('[COLOR white]UK Documentaries[/COLOR]',UK_Documentaries,25,icon,fanart,'')
	tools.addDir('[COLOR white]UK Kids[/COLOR]',UK_Kids,25,icon,fanart,'')
	tools.addDir('[COLOR white]--------[/COLOR] [COLOR blue][B]UK SPORTS[/B][/COLOR] [COLOR white]--------[/COLOR]','','',britsh,fanart,'')
	tools.addDir('[COLOR white]UK Sports[/COLOR]',UK_Sports_2,25,topenglish,fanart,'')
	tools.addDir('[COLOR white]EPL[/COLOR]',NBC_GOLD___Premier_League,25,sports2,fanart,'')
	tools.addDir('[B][COLOR white]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Clear Cache[/COLOR]','CC',10,cache,fanart,'')
	tools.addDir('[COLOR white]Search[/COLOR]','url',5,search2,fanart,'')
	setView()

def CANADA():
	tools.addDir('[B][COLOR white]=-=-=-=-=-=-=-=-=-=[/COLOR][/B] [B][COLOR red]CA LIVE[/COLOR][/B] [B][COLOR white]=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','','',canada,fanart,'')
	tools.addDir('[COLOR white]CA Entertainment[/COLOR]',Canada,25,entertainment,fanart,'')
	tools.addDir('[COLOR white]CA News[/COLOR]',Canada_News,25,icon,fanart,'')
	tools.addDir('[COLOR white]CA Movies[/COLOR]',Canada_Movies,25,icon,fanart,'')
	tools.addDir('[COLOR white]CA Kids[/COLOR]',Canada_Kids,25,icon,fanart,'')
	tools.addDir('[COLOR white]--------[/COLOR] [COLOR red][B]CA SPORTS[/B][/COLOR] [COLOR white]--------[/COLOR]','','',canada,fanart,'')
	tools.addDir('[COLOR white]CA Sports[/COLOR]',Canadian_Sports,25,topenglish,fanart,'')
	tools.addDir('[B][COLOR white]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Clear Cache[/COLOR]','CC',10,cache,fanart,'')
	tools.addDir('[COLOR white]Search[/COLOR]','url',5,search2,fanart,'')
	setView()	

def INT():
	tools.addDir('[B][COLOR white]=-=-=-=-=-=-=-=-=-=[/COLOR][/B] [B][COLOR yellowgreen]INTERNATIONAL[/COLOR][/B] [B][COLOR white]=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','','',international,fanart,'')
	tools.addDir('[COLOR white]International Sports[/COLOR]',International_Sports,25,icon,fanart,'')
	tools.addDir('[COLOR white]Latino[/COLOR]',Latino,25,international,fanart,'')
	tools.addDir('[COLOR white]Africa[/COLOR]',Africa,25,international,fanart,'')
	tools.addDir('[COLOR white]Albania[/COLOR]',Albania,25,international,fanart,'')
	tools.addDir('[COLOR white]Arabic[/COLOR]',Arabic,25,international,fanart,'')
	tools.addDir('[COLOR white]Armenia[/COLOR]',Armenia,25,international,fanart,'')
	tools.addDir('[COLOR white]America[/COLOR]',SOUTH_AMERICA,25,international,fanart,'')
	tools.addDir('[COLOR white]Australia[/COLOR]',Australia,25,international,fanart,'')
	tools.addDir('[COLOR white]Belgium[/COLOR]',Belgium,25,international,fanart,'')
	tools.addDir('[COLOR white]Brazil[/COLOR]',Brazil,25,international,fanart,'')
	tools.addDir('[COLOR white]Bulgaria[/COLOR]',Bulgaria,25,international,fanart,'')
	tools.addDir('[COLOR white]Canada[/COLOR]',Canada,25,international,fanart,'')
	#tools.addDir('[COLOR white]China[/COLOR]',China,25,international,fanart,'')
	tools.addDir('[COLOR white]Caribbean[/COLOR]',CARIBBEAN,25,international,fanart,'')
	tools.addDir('[COLOR white]Czech Republic[/COLOR]',Czech_Republic,25,international,fanart,'')
	tools.addDir('[COLOR white]Denmark[/COLOR]',Denmark,25,international,fanart,'')
	tools.addDir('[COLOR white]Egypt[/COLOR]',EGYPT,25,international,fanart,'')
	tools.addDir('[COLOR white]EX YU[/COLOR]',EX_YU,25,international,fanart,'')
	tools.addDir('[COLOR white]France[/COLOR]',France,25,international,fanart,'')
	tools.addDir('[COLOR white]Germany[/COLOR]',German,25,international,fanart,'')
	tools.addDir('[COLOR white]Greek[/COLOR]',Greek,25,international,fanart,'')
	tools.addDir('[COLOR white]Hungary[/COLOR]',Hungary,25,international,fanart,'')
	tools.addDir('[COLOR white]Philippines[/COLOR]',Philippines,25,international,fanart,'')
	tools.addDir('[COLOR white]India[/COLOR]',India,25,international,fanart,'')
	tools.addDir('[COLOR white]Ireland[/COLOR]',Irish,25,international,fanart,'')
	tools.addDir('[COLOR white]Indonesia[/COLOR]',Indonesia,25,international,fanart,'')
	#tools.addDir('[COLOR white]Iran[/COLOR]',Iran,25,international,fanart,'')
	tools.addDir('[COLOR white]Israel[/COLOR]',Israel,25,international,fanart,'')
	tools.addDir('[COLOR white]Italy[/COLOR]',Italy,25,international,fanart,'')
	tools.addDir('[COLOR white]Japan[/COLOR]',Japan,25,international,fanart,'')
	tools.addDir('[COLOR white]Korea[/COLOR]',Korea,25,international,fanart,'')
	#tools.addDir('[COLOR white]Macedonia[/COLOR]',Macedonia,25,international,fanart,'')
	tools.addDir('[COLOR white]Netherlands[/COLOR]',Netherlands,25,international,fanart,'')
	tools.addDir('[COLOR white]Pakistan[/COLOR]',Pakistan,25,international,fanart,'')
	tools.addDir('[COLOR white]Persian[/COLOR]',Pakistan,25,international,fanart,'')
	tools.addDir('[COLOR white]Polish[/COLOR]',Polish,25,international,fanart,'')
	tools.addDir('[COLOR white]Portugal[/COLOR]',Portugal,25,international,fanart,'')
	tools.addDir('[COLOR white]Romania[/COLOR]',Romania,25,international,fanart,'')
	tools.addDir('[COLOR white]Russia[/COLOR]',Russia,25,international,fanart,'')
	tools.addDir('[COLOR white]Spain[/COLOR]',Spain,25,international,fanart,'')
	tools.addDir('[COLOR white]Sweden[/COLOR]',Sweden,25,international,fanart,'')
	#tools.addDir('[COLOR white]Switzerland[/COLOR]',Switzerland,25,international,fanart,'')
	tools.addDir('[COLOR white]Turkish[/COLOR]',Turkish,25,international,fanart,'')
	#tools.addDir('[COLOR white]Vietnam[/COLOR]',Vietnam,25,international,fanart,'')
	tools.addDir('[B][COLOR white]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Clear Cache[/COLOR]','CC',10,cache,fanart,'')
	tools.addDir('[COLOR white]Search[/COLOR]','url',5,search2,fanart,'')
	
def extras():
	tools.addDir('[COLOR white]Create a Short M3U & EPG URL[/COLOR]','url',17,icon,fanart,'')
	tools.addDir('[COLOR white]Run a Speed Test[/COLOR]','ST',10,speed,fanart,'')
	#if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
		#tools.addDir('[COLOR yellowgreen]Simple PVR Client TV Guide[/COLOR]','pvr',7,guide,fanart,'')
	#if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
		#tools.addDir('[COLOR yellowgreen]Simple PVR Client Channels Guide[/COLOR]','pvr',45,icon,fanart,'')
	tools.addDir('[COLOR white]Setup Simple PVR[/COLOR]','tv',11,guide,fanart,'')
	tools.addDir('[COLOR blue]iVue TV Guide[/COLOR]','pvr',44,guide,fanart,'')
	tools.addDir('[COLOR white]Setup iVue TV Guide -Old-[/COLOR]','tv',15,guide,fanart,'')
	#tools.addDir('[COLOR white]Setup iVue TV Guide -New-[/COLOR]','tv',36,guide,fanart,'')
	tools.addDir('[COLOR white]iVue TV Guide Settings[/COLOR]','tv',38,guide,fanart,'')
	tools.addDir('[COLOR white]Reboot iVue TV Guide[/COLOR]','url',20,guide,fanart,'')
	
def settingsmenu():
	tools.addDir('Settings','tv',39,icon,fanart,'')
	tools.addDir('Edit Advanced Settings','ADS',10,icon,fanart,'')
	tools.addDir('Log Out','LO',10,icon,fanart,'')
	
def ALL_247():	
	tools.addDir('[B][COLOR white]=-=-=-=-=-=-=-=-=-=[/COLOR][/B] [B][COLOR crimson]24/7[/COLOR][/B] [B][COLOR white]=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Movies[/COLOR]',twentyfourseven_Movies,25,catch,fanart,'')
	tools.addDir('[COLOR white]TV Shows[/COLOR]',twentyfourseven_TV,25,catch,fanart,'')
	tools.addDir('[COLOR white]Kids TV Shows[/COLOR]',twentyfourseven_Kids,25,catch,fanart,'')
	tools.addDir('[COLOR crimson]-------------------------------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Search[/COLOR]','url',5,search2,fanart,'')
	tools.addDir('[COLOR white]Clear Cache[/COLOR]','CC',10,cache,fanart,'')
	setView()
	

	
def US_ALL():
	US = [" US ", " us "]
	live_url	 = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=0'%(host,port,username,password)
	list = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(list,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		for item in US:
			if item in name:
				if " IN " in name:
					pass
				else:
					tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
	plugintools.set_view( plugintools.EPISODES )
	
def US_NEWS():
	US_NEWS = ["News", "NEWS", "FOX 25", "CNN", "Bloomberg", "CNBC", "MSN", "MSNBC"]
	live_url	 = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=0'%(host,port,username,password)
	list = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(list,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		for item in US_NEWS:
			if item in name:
				if " US " in name:
					tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
				else:
					pass
	plugintools.set_view( plugintools.EPISODES )
	
def UK_NEWS():
	UK_NEWS = ["News", "NEWS", "ITV UK"]
	live_url	 = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=0'%(host,port,username,password)
	list = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(list,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		for item in UK_NEWS:
			if item in name:
				if " UK " in name:
					tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
				else:
					pass
	plugintools.set_view( plugintools.EPISODES )
					
def MUSIC_ALL():
	MUSIC = ["MUSIC", "music", "Music", "MTV", "VH1"]
	live_url	 = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=0'%(host,port,username,password)
	list = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(list,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		for item in MUSIC:
			if item in name:
				tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
	plugintools.set_view( plugintools.LIST )		
def SPORTS_ALL():
	SPORTS =["Sport", "SPORT", "Sports", "SPORTS", "NHL", "MLB", "NBA", "NFL", "PAC", "TSN", "ESPN", "Fox", "Golf", "Tennis", "Football", "UFC", "moto", "celtic tv", "rangers tv", "LFC TV", "boxnation", "NCAA", "MLS"]
	live_url	 = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=0'%(host,port,username,password)
	list = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(list,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		for item in SPORTS:
			if item in name:
				tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
	plugintools.set_view( plugintools.EPISODES )				

				
	
	
def UK_ALL():
	UK = [" UK ", " uk "]
	live_url	 = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=0'%(host,port,username,password)
	list = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(list,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		for item in UK:
			if item in name:
				if " IN " in name:
					pass
				else:
					tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
	plugintools.set_view( plugintools.EPISODES )
					
					
def SoftReset():
	clearFiles = ["guides.ini", "addons.ini", "guide.xml", "amylist.xml", "teamexpat.xml", "otttv.xml", "guide2.xml", "uk3.xml", "guide3.xmltv", "master.xml"]
	for root, dirs, files in os.walk(databasePath,topdown=True):
		dirs[:] = [d for d in dirs]
		for name in files:
			if name in clearFiles:
				try:
					os.remove(os.path.join(root,name))
				except:
					dialog.ok('Soft Reset', 'Error Removing ' + str(name),'')
					pass
			else:
				continue
	dialog.ok('Ivue guide Soft reset', 'Please restart iVue TV Guide ','for changes to take effect.')
	home()

def DESTROY_PATH(path):
    shutil.rmtree(path, ignore_errors=True)

def exit():
    xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
    if os.path.exists(durextvfol):   
        DESTROY_PATH(durextvfol)

		
def livecategory(url):
	
	open = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
		tools.addDir(name,url1,2,icon,fanart,'')
		plugintools.set_view( plugintools.LIST )
		
def Livelist(url):
	open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
	plugintools.set_view( plugintools.LIST )
	
def LiveInfolist(url):
	open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
	plugintools.set_view( plugintools.EPISODES )
		
	
def vod(url):
	if url =="vod":
		open = tools.OPEN_URL(vod_url)
	else:
		open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		if '<playlist_url>' in open:
			name = tools.regex_from_to(a,'<title>','</title>')
			url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
			tools.addDir(str(base64.b64decode(name)).replace('?',''),url1,3,icon,fanart,'')
			plugintools.set_view( plugintools.LIST )
		else:
			if xbmcaddon.Addon().getSetting('meta') == 'true':
				try:
					name = tools.regex_from_to(a,'<title>','</title>')
					name = base64.b64decode(name)
					thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
					url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
					desc = tools.regex_from_to(a,'<description>','</description>')
					desc = base64.b64decode(desc)
					plot = tools.regex_from_to(desc,'PLOT:','\n')
					cast = tools.regex_from_to(desc,'CAST:','\n')
					ratin= tools.regex_from_to(desc,'RATING:','\n')
					year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
					year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
					runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
					genre= tools.regex_from_to(desc,'GENRE:','\n')
					tools.addDirMeta(str(name).replace('[/COLOR].','.[/COLOR]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
				except:pass
				xbmcplugin.setContent(int(sys.argv[1]), 'movies')
			else:
				name = tools.regex_from_to(a,'<title>','</title>')
				name = base64.b64decode(name)
				thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
				url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
				desc = tools.regex_from_to(a,'<description>','</description>')
				tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
		
		
##########################################
def catchup():
    loginurl   = "http://main.tvstreams.xyz:83/get.php?username=" + username + "&password=" + password + "&type=m3u_plus&output=ts"
    try:
        connection = urllib2.urlopen(loginurl)
        print connection.getcode()
        connection.close()
        #playlist found, user active & login correct, proceed to addon
        pass
        
    except urllib2.HTTPError, e:
        print e.getcode()
        dialog.ok("[COLOR white]Expired Account[/COLOR]",'[COLOR white]You cannot use this service with an expired account[/COLOR]',' ','[COLOR white]Please check your account information[/COLOR]')
        sys.exit(1)
        xbmc.executebuiltin("Dialog.Close(busydialog)")

    url = "%s:%s/xmltv.php?username=%s&password=%s"%(host,port,username,password)
    DownloaderClass(url,GuideLoc + "uide.xml")
    
    f = open(Guide, 'r+')
    input = open(Guide).read().decode('UTF-8')
    output = unicodedata.normalize('NFKD', input).encode('ASCII', 'ignore')
    f.write(output)
    f.truncate()
    f.close()
    listcatchup()
		
def listcatchup():
	open = tools.OPEN_URL(panel_api)
	all  = tools.regex_get_all(open,'{"num','direct')
	for a in all:
		if '"tv_archive":1' in a:
			name = tools.regex_from_to(a,'"epg_channel_id":"','"')
			thumb= tools.regex_from_to(a,'"stream_icon":"','"').replace('\/','/')
			id   = tools.regex_from_to(a,'stream_id":"','"')
			tools.addDir(name.replace('ENT:','[COLOR blue]ENT:[/COLOR]').replace('DOC:','[COLOR blue]DOC:[/COLOR]').replace('MOV:','[COLOR blue]MOV:[/COLOR]').replace('SSS:','[COLOR blue]SSS[/COLOR]').replace('BTS:','[COLOR blue]BTS:[/COLOR]').replace('TEST','[COLOR blue]TEST[/COLOR]').replace('Install','[COLOR blue]Install[/COLOR]').replace('24/7','[COLOR blue]24/7[/COLOR]').replace('INT:','[COLOR blue]INT:[/COLOR]').replace('DE:','[COLOR blue]DE:[/COLOR]').replace('FR:','[COLOR blue]FR:[/COLOR]').replace('PL:','[COLOR blue]PL:[/COLOR]').replace('AR:','[COLOR blue]AR:[/COLOR]').replace('LIVE:','[COLOR blue]LIVE:[/COLOR]').replace('ES:','[COLOR blue]ES:[/COLOR]').replace('IN:','[COLOR blue]IN:[/COLOR]').replace('PK:','[COLOR blue]PK:[/COLOR]'),'url',13,thumb,fanart,id)
			

def tvarchive(name,description):
    name = str(name.replace('[COLOR blue]ENT:[/COLOR]','ENT:').replace('[COLOR blue]DOC:[/COLOR]','DOC:').replace('[COLOR blue]MOV:[/COLOR]','MOV').replace('[COLOR blue]SSSS[/COLOR]','SSS:').replace('[COLOR blue]BTS:[/COLOR]','BTS:').replace('[COLOR blue]INT:[/COLOR]','INT:').replace('[COLOR blue]DE:[/COLOR]','DE:').replace('[COLOR blue]FR:[/COLOR]','FR:').replace('[COLOR blue]PL:[/COLOR]','PL:').replace('[COLOR blue]AR:[/COLOR]','AR:').replace('[COLOR blue]LIVE:[/COLOR]','LIVE:').replace('[COLOR blue]ES:[/COLOR]','ES:').replace('[COLOR blue]IN:[/COLOR]','IN:').replace('[COLOR blue]PK:[/COLOR]','PK'))
    filename = open(Guide)
    tree = ElementTree.parse(filename)
    pony = "apples"
    import datetime as dt
    from datetime import time
    date3 = datetime.datetime.now() - datetime.timedelta(days=5)
    date = str(date3)
    now = str(datetime.datetime.now()).replace('-','').replace(':','').replace(' ','')
    programmes = tree.findall("programme")
    for programme in programmes:
        if name in programme.attrib.get('channel'):
            showtime = programme.attrib.get('start')
            head, sep, tail = showtime.partition(' +')
            date = str(date).replace('-','').replace(':','').replace(' ','')
            year, month, day = showtime.partition('2017')
            kanalinimi = programme.find('title').text + showtime
            day = day[:-6]
            if head > date:
                if head < now:
                    head2 = head
                    head2 = head2[:4] + '/' + head2[4:]
                    head = head[:4] + '-' + head[4:]
                    head2 = head2[:7] + '/' + head2[7:]
                    head = head[:7] + '-' + head[7:]
                    head2 = head2[:10] + ' - ' + head2[10:]
                    head = head[:10] + ':' + head[10:]
                    head2 = head2[:15] + ':' + head2[15:]
                    head = head[:13] + '-' + head[13:]
                    head2 = head2[:-2]
                    head = head[:-2]
                    poo1 = ("%s:%s/streaming/timeshift.php?username=%s&password=%s&stream=%s&start=")%(host,port,username,password,description)
                    pony = poo1 + str(head) + "&duration=240"
                    head2 = '[COLOR blue]%s - [/COLOR]'%head2 
                    kanalinimi = str(head2)+ programme.find('title').text
                    desc  = programme.find('desc').text
                    tools.addDir(kanalinimi,pony,4,icon,fanart,desc)
                    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
	
					
def DownloaderClass(url, dest):
    dp = xbmcgui.DialogProgress()
    dp.create('Fetching latest Catch Up',"Fetching latest Catch Up...",' ', ' ')
    dp.update(0)
    start_time=time.time()
    urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))

def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: 
                eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: 
                eta = 0 
            kbps_speed = kbps_speed / 1024 
            mbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '[COLOR white]%.02f MB of less than 5MB[/COLOR]' % (currently_downloaded)
            e = '[COLOR white]Speed:  %.02f Mb/s ' % mbps_speed  + '[/COLOR]'
            dp.update(percent, mbs, e)
        except: 
            percent = 100 
            dp.update(percent) 
        if dp.iscanceled():
            dialog = xbmcgui.Dialog()
            dialog.ok("[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]", 'The download was cancelled.')
				
            sys.exit()
            dp.close()
#####################################################################


def ivuetvguide():
	if xbmc.getCondVisibility('System.HasAddon(script.ivueguide)'):
		if not os.path.exists(drxaddons2ini):
			IVUEtvguidesetup()
		else:
			EXIT()
			xbmc.executebuiltin('RunAddon(script.ivueguide)')
		
def simpletvguide():
	if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
		if not os.path.exists(PVRSimple):
			SIMPLEtvguidesetup()
		else:
			EXIT()
			xbmc.executebuiltin('ActivateWindow(TVGuide)')
			
def simplechannels():
	if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
		if not os.path.exists(PVRSimple):
			SIMPLEtvguidesetup()
		else:
			EXIT()
			xbmc.executebuiltin('ActivateWindow(TVChannels)')
			
def EXIT():
    xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
    xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
				
def stream_video(url):
	if adultpwset == "true":
		a = 'XO', 'XXX', 'Adult', 'Adults','ADULT','ADULTS','adult','adults','Porn','PORN','porn','Porn','xxx'
		if any(s in name for s in a):
			text = control.inputDialog(heading='Enter Adult Password:')
			if text ==control.setting('Adult.PW'):
				url = str(url).replace('USERNAME',username).replace('PASSWORD',password)
				liz = xbmcgui.ListItem('', iconImage='DefaultVideo.png', thumbnailImage=icon)
				liz.setInfo(type='Video', infoLabels={'Title': '', 'Plot': ''})
				liz.setProperty('IsPlayable','true')
				liz.setPath(str(url))
				xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
			else:
				xbmc.executebuiltin((u'XBMC.Notification("Parental Lock", "Incorrect Password!", 2000)'))
				return
		else:
			url = str(url).replace('USERNAME',username).replace('PASSWORD',password)
			liz = xbmcgui.ListItem('', iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': '', 'Plot': ''})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(url))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
		
	else:
		url = str(url).replace('USERNAME',username).replace('PASSWORD',password)
		liz = xbmcgui.ListItem('', iconImage='DefaultVideo.png', thumbnailImage=icon)
		liz.setInfo(type='Video', infoLabels={'Title': '', 'Plot': ''})
		liz.setProperty('IsPlayable','true')
		liz.setPath(str(url))
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
	
def searchdialog():
	search = control.inputDialog(heading='Search [COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]:')
	if search=="":
		return
	else:
		return search

	
def search():
	if mode==3:
		return False
	text = searchdialog()
	if not text:
		xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Search is Empty[/B][/COLOR],Aborting search,4000,"+icon+")")
		return
	xbmc.log(str(text))
	open = tools.OPEN_URL(panel_api)
	all_chans = tools.regex_get_all(open,'{"num":','epg')
	for a in all_chans:
		name = tools.regex_from_to(a,'name":"','"').replace('\/','/')
		url  = tools.regex_from_to(a,'"stream_id":"','"')
		thumb= tools.regex_from_to(a,'stream_icon":"','"').replace('\/','/')
		if text in name.lower():
			tools.addDir(name,play_url+url+'.ts',4,thumb,fanart,'')
		elif text not in name.lower() and text in name:
			tools.addDir(name,play_url+url+'.ts',4,thumb,fanart,'')

	

def addonsettings(url,description):
	if   url =="CC":
		tools.clear_cache()
	elif url =="AS":
		xbmc.executebuiltin('Addon.OpenSettings(%s)'%addon_id)
	elif url =="ADS":
		dialog = xbmcgui.Dialog().select('Edit Advanced Settings', ['Enable Fire TV Stick AS','Enable Fire TV AS','Enable 1GB Ram or Lower AS','Enable 2GB Ram or Higher AS','3GB Ram or Higher (Nvidia Shield) AS','Disable AS'])
		if dialog==0:
			advancedsettings('stick')
			xbmcgui.Dialog().ok('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]', 'Set Advanced Settings')
		elif dialog==1:
			advancedsettings('firetv')
			xbmcgui.Dialog().ok('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]', 'Set Advanced Settings')
		elif dialog==2:
			advancedsettings('lessthan')
			xbmcgui.Dialog().ok('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]', 'Set Advanced Settings')
		elif dialog==3:
			advancedsettings('morethan')
			xbmcgui.Dialog().ok('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]', 'Set Advanced Settings')
		elif dialog==4:
			advancedsettings('shield')
			xbmcgui.Dialog().ok('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]', 'Set Advanced Settings')
		elif dialog==5:
			advancedsettings('remove')
			xbmcgui.Dialog().ok('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]', 'Advanced Settings Removed')
	elif url =="ADS2":
		dialog = xbmcgui.Dialog().select('Select Your Device Or Closest To', ['Fire TV Stick ','Fire TV','1GB Ram or Lower','2GB Ram or Higher','3GB Ram or Higher (Nvidia Shield)'])
		if dialog==0:
			advancedsettings('stick')
			xbmcgui.Dialog().ok('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]', 'Set Advanced Settings')
		elif dialog==1:
			advancedsettings('firetv')
			xbmcgui.Dialog().ok('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]', 'Set Advanced Settings')
		elif dialog==2:
			advancedsettings('lessthan')
			xbmcgui.Dialog().ok('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]', 'Set Advanced Settings')
		elif dialog==3:
			advancedsettings('morethan')
			xbmcgui.Dialog().ok('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]', 'Set Advanced Settings')
		elif dialog==4:
			advancedsettings('shield')
			xbmcgui.Dialog().ok('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]', 'Set Advanced Settings')
	elif url =="tv":
		ivueint()

	elif url =="ST":
		xbmc.executebuiltin('Runscript("special://home/addons/plugin.video.hypersonicIPTV2/resources/modules/speedtest.py")')
	elif url =="META":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('meta','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('meta','true')
			xbmc.executebuiltin('Container.Refresh')
	elif url =="LO":
		xbmcaddon.Addon().setSetting('Username','')
		xbmcaddon.Addon().setSetting('Password','')
		xbmc.executebuiltin('XBMC.ActivateWindow(Videos,addons://sources/video/)')
		xbmc.executebuiltin('Container.Refresh')
	elif url =="UPDATE":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('update','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('update','true')
			xbmc.executebuiltin('Container.Refresh')
	
		
def advancedsettings(device):
	if device == 'stick':
		file = open(os.path.join(advanced_settings, 'stick.xml'))
	elif device == 'firetv':
		file = open(os.path.join(advanced_settings, 'firetv.xml'))
	elif device == 'lessthan':
		file = open(os.path.join(advanced_settings, 'lessthan1GB.xml'))
	elif device == 'morethan':
		file = open(os.path.join(advanced_settings, 'morethan1GB.xml'))
	elif device == 'shield':
		file = open(os.path.join(advanced_settings, 'shield.xml'))
	elif device == 'remove':
		os.remove(advanced_settings_target)
	
	try:
		read = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(read)
		f.close()
	except:
		pass
		
	
def pvrsetup():
	correctPVR()
	killxbmc()
	return
		
		
def asettings():
	choice = xbmcgui.Dialog().yesno('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]', 'Please Select The RAM Size of Your Device', yeslabel='Less than 1GB RAM', nolabel='More than 1GB RAM')
	if choice:
		lessthan()
	else:
		morethan()
	

def morethan():
		file = open(os.path.join(advanced_settings, 'morethan.xml'))
		a = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(a)
		f.close()

		
def lessthan():
		file = open(os.path.join(advanced_settings, 'lessthan.xml'))
		a = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(a)
		f.close()
		
		
def userpopup():
	kb =xbmc.Keyboard ('', 'heading', True)
	kb.setHeading('Enter Username')
	kb.setHiddenInput(False)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		return text
	else:
		return False

		
def passpopup():
	kb =xbmc.Keyboard ('', 'heading', True)
	kb.setHeading('Enter Password')
	kb.setHiddenInput(False)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		return text
	else:
		return False
		
		
def accountinfo():
	data = json.load(urllib2.urlopen(panel_api))
	null = ["0", " " , "null"]
	today = datetime.date.today()
	x=data['user_info']
	Username = x['username']
	Status = x['status']
	Creation = x['created_at']
	Created = datetime.datetime.fromtimestamp(int(Creation)).strftime('%H:%M %m/%d/%Y')
	Current = x['active_cons']
	Max = x['max_connections']
	Expiry = x['exp_date']
	if Expiry == None:
		Expired = 'Never'
	else:
		Expired = datetime.datetime.fromtimestamp(int(Expiry)).strftime('%H:%M %m/%d/%Y')
	tools.addDir('[COLOR white]--------[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR] [COLOR white]ACCOUNT INFO[/COLOR][COLOR white]--------[/COLOR]','','',icon,fanart,'')
	tools.addDir('[COLOR white]Username :[/COLOR] '+Username,'','',icon,fanart,'')
	tools.addDir('[COLOR white]Expire Date:[/COLOR] '+Expired,'','',icon,fanart,'')
	tools.addDir('[COLOR white]Account Status :[/COLOR] '+Status,'','',icon,fanart,'')
	tools.addDir('[COLOR white]Current Connections:[/COLOR] '+Current,'','',icon,fanart,'')
	tools.addDir('[COLOR white]Allowed Connections:[/COLOR] '+Max,'','',icon,fanart,'')
	tools.addDir('[COLOR white]Created:[/COLOR] '+Created,'','',icon,fanart,'')
	tools.addDir('To purchase account email:[COLOR yellowgreen] hypersonictvpro@gmail.com[/COLOR]',All,2,icon,fanart,'')
	plugintools.set_view( plugintools.LIST )

	
def correctPVR():

	addon = xbmcaddon.Addon('plugin.video.hypersonicIPTV2')
	username_text = addon.getSetting(id='Username')
	password_text = addon.getSetting(id='Password')
	jsonSetPVR = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":true},"id":1}'
	IPTVon 	   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}'
	nulldemo   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.demo","enabled":false},"id":1}'
	loginurl   = "http://main.tvstreams.xyz:83/get.php?username=" + username_text + "&password=" + password_text + "&type=m3u_plus&output=ts"
	EPGurl     = "http://main.tvstreams.xyz:83/xmltv.php?username=" + username_text + "&password=" + password_text + "&type=m3u_plus&output=ts"

	xbmc.executeJSONRPC(jsonSetPVR)
	xbmc.executeJSONRPC(IPTVon)
	xbmc.executeJSONRPC(nulldemo)
	
	moist = xbmcaddon.Addon('pvr.iptvsimple')
	moist.setSetting(id='m3uUrl', value=loginurl)
	moist.setSetting(id='epgUrl', value=EPGurl)
	moist.setSetting(id='m3uCache', value="false")
	moist.setSetting(id='epgCache', value="false")
	
def ivueint():
	ivuesetup.iVueInt()
	xbmcgui.Dialog().ok('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]', 'iVue Integration Complete')
	xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.IVUEcreator/update_addon/plugin.video.hypersonicIPTV2",return)')
	xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
	
def ivueint2():
	ivuesetup.iVueInt2()
	xbmcgui.Dialog().ok('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]', 'iVue Integration Complete')
	home()
	
	
def SIMPLEtvguidesetup():
	dialog = xbmcgui.Dialog().yesno('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]','Would you like us to setup Simple PVR Guide for you?')
	if dialog:
		pvrsetup()
	else:
		home()
		
def IVUEtvguidesetup():
	dialog = xbmcgui.Dialog().yesno('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]','Would You like us to Setup iVue TV Guide for You?')
	if dialog:
		ivueint()
	else:
		home()
		
def ivue_settings():
	xbmc.executebuiltin("Addon.OpenSettings(script.ivueguide)")

def drx_settings():
	xbmc.executebuiltin("Addon.OpenSettings(plugin.video.hypersonicIPTV2)")

	
def setView():
	xbmc.executebuiltin("Container.SetViewMode(50)")
	
def killxbmc(over=None):
	killdialog = xbmcgui.Dialog().yesno('Force Close Kodi', '[COLOR white]You are about to close Kodi', 'Would you like to continue?[/COLOR]', nolabel='[B][COLOR red] No Cancel[/COLOR][/B]',yeslabel='[B][COLOR green]Force Close Kodi[/COLOR][/B]')
	if killdialog:
		os._exit(1)
	else:
		home()
		
def adultpopup():
	kb =xbmc.Keyboard ('', 'heading', True)
	kb.setHeading('Enter Adult Password')
	kb.setHiddenInput(False)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		return text
	else:
		return False

def adult_settings():
	dialog = xbmcgui.Dialog().yesno('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]','Would you like to HIDE [COLOR pink]Adult Menu[/COLOR]?', 'You can always change this in settings later on.')
	if dialog:
		control.setSetting('Adult.Set','true')
		pass
	else:
		control.setSetting('Adult.Set','false')
		pass
	dialog = xbmcgui.Dialog().yesno('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]','Would you like to PASSWORD PROTECT [COLOR pink]Adult Channels[/COLOR]?', 'You can always change this in settings later on.')
	if dialog:
		control.setSetting('Adult.PWSet','true')
		adulter = adultpopup()
		control.setSetting('Adult.PW',adulter)
	else:
		control.setSetting('Adult.PWSet','false')
		pass
		

def testarea():
	durextvcat   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.hypersonicIPTV2/categories.db'))
	channels = []
	
	if os.path.isfile(durextvcat):
		os.remove(durextvcat)

	
	list_a = tools.OPEN_URL(live_url)
	all_chan = tools.regex_get_all(list_a,'<channel>','</channel>')
	for a in all_chan:
			name = tools.regex_from_to(a,'<title>','</title>')
			name = base64.b64decode(name)
			name = re.sub(' ','_',name)
			name = re.sub('&','_',name)
			name = re.sub('\/','_',name)
			name = re.sub('\+','_',name)
			xbmc.log(str(name))
			try:
				name = re.sub('\[.*?min ','-',name)
			except:
				pass
			catnum  = tools.regex_from_to(a,'<category_id>','</category_id>')
			line = "%s = %s\n"%(name, catnum)
			channels.append(line)
					
	for item3 in channels:
		f = open(durextvcat, mode='a')
		f.write(item3)
		f.close()
		

		

		
		
def changenumbers(s):

    numbers = {'1' : 'one' ,'2' : 'two', '3' : 'three', '4':'four', '5' : 'five' ,'6' : 'six' ,
               '7' : 'seven', '8' : 'eight', '9':'nine', '10' : 'ten', '11':'eleven', '12' : 'twelve',}

    for src, target in numbers.iteritems():
        if src in s:
            s = s.replace(src, target)

    return s

def num2day(num):
	if num =="0":
		day = 'monday'
	elif num=="1":
		day = 'tuesday'
	elif num=="2":
		day = 'wednesday'
	elif num=="3":
		day = 'thursday'
	elif num=="4":
		day = 'friday'
	elif num=="5":
		day = 'saturday'
	elif num=="6":
		day = 'sunday'
	return day
	
setView()
params=tools.get_params()
url=None
name=None
mode=None
iconimage=None
description=None
query=None
type=None

try:
	url=urllib.unquote_plus(params["url"])
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
	mode=int(params["mode"])
except:
	pass
try:
	description=urllib.unquote_plus(params["description"])
except:
	pass
try:
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	type=urllib.unquote_plus(params["type"])
except:
	pass

if mode==None or url==None or len(url)<1:
	start()

elif mode==1:
	livecategory(url)
	
elif mode==2:
	Livelist(url)
	
elif mode==3:
	vod(url)
	
elif mode==4:
	stream_video(url)
	
elif mode==5:
	search()
	
elif mode==6:
	accountinfo()
	
elif mode==7:
	simpletvguide()
	
elif mode==8:
	settingsmenu()
	
elif mode==9:
	xbmc.executebuiltin('ActivateWindow(busydialog)')
	tools.Trailer().play(url) 
	xbmc.executebuiltin('Dialog.Close(busydialog)')
	
elif mode==10:
	addonsettings(url,description)
	
elif mode==11:
	SIMPLEtvguidesetup()
	
elif mode==12:
	catchup()

elif mode==13:
	tvarchive(name,description)
	
elif mode==14:
	listcatchup2()
	
elif mode==15:
	ivueint()
	
elif mode==16:
	extras()
	
elif mode==17:
	shortlinks.Get()

elif mode==18:
	footballguidesearch(description)
	
elif mode==19:
	get()
	
elif mode==20:
	SoftReset()
	
elif mode==21:
	NEW_MENU()
	
elif mode==22:
	US()
	
elif mode==23:
	UK()
	
elif mode==24:
	INT()
	
elif mode==25:
	LiveInfolist(url)

elif mode==26:
	NFL()
	
elif mode==27:
	NHL()
	
elif mode==28:
	LIVE_FOOTBALL()	
	
elif mode==29:
	US_ALL()
	
elif mode==30:
	UK_ALL()
	
elif mode==31:
	MUSIC_ALL()
	
elif mode==32:
	SPORTS_ALL()
	
elif mode==33:
	US_NEWS()
	
elif mode==34:
	UK_NEWS()
	
elif mode==35:
	NEWS_ALL()
	
elif mode==36:
	ivueint2()
	
elif mode==37:
	testarea()

elif mode==38:
	ivue_settings()

	
elif mode==39:
	drx_settings()
	
elif mode==40:
	simpletvguide()
	
elif mode==44:
	ivuetvguide()
	
elif mode==45:	
	simplechannels()
	
elif mode==48:		
	ALL_ADULT()
	
elif mode==49:		
	ALL_247()

elif mode==50:
	CANADA()
	
	
	





xbmcplugin.endOfDirectory(int(sys.argv[1]))