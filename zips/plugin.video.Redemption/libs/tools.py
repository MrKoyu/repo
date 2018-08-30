import byb_modules as BYB
import _Edit  
import koding
import os 
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs
from libs._addon import *
from libs._common import *


addon          = _Edit.addon
addon_id       = addon.getAddonInfo('id')
profile        = xbmc.translatePath(addon.getAddonInfo('profile').decode('utf-8'))
true_profile   = koding.Physical_Path(profile)
COOKIES        = os.path.join(true_profile,'cookies')
pDialog        = xbmcgui.DialogProgress()

def index(iconimage,fanart):
	BYB.addDir_file(ItemColor(local_string(30059)),'',100,icon_Setting,fanart_Setting,local_string(30068),'','','')
	BYB.addDir_file(ItemColor(local_string(30060)),'',101,icon_Setting,fanart_Setting,local_string(30069),'','','')
	BYB.addDir(ChannelColor(local_string(30061)),'',102,icon_Setting,fanart_Setting,local_string(30070),'','','')
	BYB.addDir_file(ItemColor(local_string(30079)),'',104,icon_Setting,fanart_Setting,'','','','')
	BYB.addDir_file(ItemColor(local_string(30080)),'',105,icon_Setting,fanart_Setting,'','','','')
	BYB.addDir_file(ItemColor('Pairing Tool'),'',106,icon_Setting,fanart_Setting,'','','','')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def clear_cookies():
	CookieList = []
	pDialog.create(SingleColor(local_string(30062),_Edit.DialogBoxColor1),'')
	pDialog.update(0,line1=SingleColor(local_string(30063)+str(COOKIES),_Edit.DialogBoxColor2))
	xbmc.sleep(1000)
	cookie_files = koding.Get_Contents(COOKIES,folders=False,subfolders=False,full_path=False)
	total_cookies = len(cookie_files)
	count = 0
	if total_cookies >= 1:
		percent_per_item = 100.00/total_cookies
		for cookie_file in cookie_files:
			count +=1
			percent_update = percent_per_item*count
			pDialog.update(int(percent_update),line1='{} {} {}'.format(local_string(30066),cookie_file,local_string(30067)))
			Cookies_deleted = koding.Delete_Cookies(cookie_file)
			deleted = ''
			if Cookies_deleted:
				CookieList.append(cookie_file)
		deleted  = ','.join(CookieList)
		message  = local_string(30064)
		message2 = '{}\n{}'.format(local_string(30065),deleted)
	else:
		message  = local_string(30071)
		message2 = local_string(30072)
	koding.dolog('Total Cookie files = %s Cookie files = %s %s %s'%(total_cookies,cookie_files,message,message2))			
	pDialog.update(100,line1=message,line2=message2)
	xbmc.sleep(1000)
	pDialog.close()


def Dependency_OpenSettings():
	DepList = [str(addon_id)]
	dependencies = koding.Dependency_Check(addon_id=addon_id, recursive=True)
	addons_path = koding.Physical_Path('special://home/addons/')
	for dependacy in dependencies:
		if not dependacy in DepList:
			DepList.append(dependacy)
			path = str(addons_path)+str(dependacy)+'/resources/settings.xml'
			if xbmcvfs.exists(path):
				try:
					Addon = xbmcaddon.Addon(str(dependacy))
					AddonTitle = Addon.getAddonInfo('name')
					AddonFanart = Addon.getAddonInfo('fanart')
					AddonIcon = Addon.getAddonInfo('icon')
					koding.dolog(str(AddonTitle)+' has file '+str(path),line_info=True)
					BYB.addDir_file(ItemColor('{} {}'.format(local_string(30073),AddonTitle)),dependacy,103,AddonIcon,AddonFanart,'{} {}'.format(local_string(30073),AddonTitle),'','','')
				except:
					pass

def Dependency_OpenSetting(url):
	koding.dolog('Opening Dependency  Settings Menu for '+str(url),line_info=True)
	koding.Open_Settings(addon_id=url)


def kodilog():
	r = open(file_kodi_log)
	text = r.read()
	from libs import customgui
	customgui.PopUpDialog(header=local_string(30079),text = text)


def clear_cache():
	from libs import customgui
	if xbmcvfs.exists(addon_cache):
		BYB.table_names_DB(addon_cache)
		tables = ','.join(BYB.TableNames)
		BYB.del_all_data_DB(addon_cache)
		header='{} Maintenance'.format(addon_name)
		text='Successfully cleared Cache of {}\nTables Cleaned\n{}'.format(addon_name,tables)
	else:
		header='No Cache file to clean of {}'.format(addon_name)
		text=''
	customgui.OkDialog(header,text)
