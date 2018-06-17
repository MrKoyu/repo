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


addon          = _Edit.addon
addon_id       = addon.getAddonInfo('id')
profile        = xbmc.translatePath(addon.getAddonInfo('profile').decode('utf-8'))
true_profile   = koding.Physical_Path(profile)
COOKIES        = os.path.join(true_profile,'cookies')
pDialog        = xbmcgui.DialogProgress()

def index(iconimage,fanart):
	BYB.addDir_file('Open settings','',100,iconimage,fanart,'Open settings for addon','','','')
	BYB.addDir_file('Delete Cookies','',101,iconimage,fanart,'Clear all Cookies from Cookie cache','','','')
	BYB.addDir('Dependencies OpenSettings','',102,iconimage,fanart,'Open settings of all dependencies required by this addon','','','')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def clear_cookies():
	pDialog.create('Deleting Cookies','')
	pDialog.update(0,line1='Searching Cookies in '+str(COOKIES))
	xbmc.sleep(1000)
	cookie_files = koding.Get_Contents(COOKIES,folders=False,subfolders=False,full_path=False)
	total_cookies = len(cookie_files)
	count = 0
	if total_cookies >= 1:
		percent_per_item = 100.00/total_cookies
		for cookie_file in cookie_files:
			count +=1
			percent_update = percent_per_item*count
			pDialog.update(int(percent_update),line1='Removing '+str(cookie_file)+' Cookie file')
			Cookies_deleted = koding.Delete_Cookies(cookie_file)
			deleted = ''
			if Cookies_deleted:
				#deleted.append(cookie_file)
				deleted += '%s,'%cookie_file
		deleted = deleted.rstrip(',')
		message = 'Process Complete'
		message2 =  'Files deleted\n%s'%deleted
	else:
		message ='No Files to delete'
		message2 = 'The Cookie Jar is empty'
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
					BYB.addDir_file('Open settings for '+str(AddonTitle),dependacy,103,AddonIcon,AddonFanart,'Open settings for '+str(AddonTitle),'','','')
				except:
					pass

def Dependency_OpenSetting(url):
	koding.dolog('Opening Dependency  Settings Menu for '+str(url),line_info=True)
	koding.Open_Settings(addon_id=url)
