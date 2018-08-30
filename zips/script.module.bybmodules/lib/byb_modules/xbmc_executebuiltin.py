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
	Notification = 'XBMC.Notification({},{},{},{})'.format(title,message,times,icon)
	xbmc.executebuiltin(str(Notification))

def set_sort_method(sortid=0):
	xbmc.executebuiltin('Container.SetSortMethod({})'.format(sortid))

def set_sort_method_rev(sortid=0):
	xbmc.executebuiltin('Container.SetSortMethod({})'.format(sortid))
	xbmc.executebuiltin('Container.SetSortDirection(Descending)')

def sort_date_reverse():
	xbmc.executebuiltin('Container.SetSortMethod(2)')
	xbmc.executebuiltin('Container.SetSortDirection(Descending)')

def refresh_container():
	xbmc.executebuiltin("XBMC.Container.Refresh")
