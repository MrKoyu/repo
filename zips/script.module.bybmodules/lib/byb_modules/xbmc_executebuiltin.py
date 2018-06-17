# -*- coding: utf-8 -*-
import koding
import xbmc


Addon_Name    = koding.Addon_Info(id='name')
Addon_Icon    = koding.Addon_Info(id='icon')


def Notify(title='',message='',times='',icon=''):
	if title == '':
		title = Addon_Name
	if times == '':
		times = '10000'
	if icon == '':
		icon = Addon_Icon
	Notification = 'XBMC.Notification(%s,%s,%s,%s)'%(title,message,times,icon)
	xbmc.executebuiltin(str(Notification))



def SetView(view_name):
	#not finished yet 
	skin_used = xbmc.getSkinDir()

def sort_date_reverse():
	xbmc.executebuiltin('Container.SetSortMethod(2)')
	xbmc.executebuiltin('Container.SetSortDirection(Descending)')

def refresh_container():
	xbmc.executebuiltin("XBMC.Container.Refresh")
