#      Copyright (C) 2015 Justin Mills
#      
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import sys, urllib,urllib2, urlparse, os, xbmcvfs
import xbmc, xbmcgui, xbmcaddon, xbmcplugin ,re, base64
import datetime
import time

addonID = 'script.ivueguide'
addon = xbmcaddon.Addon(addonID)
SkinDir = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ivueguide', 'resources', 'skins'))
ivuedirectory = base64.decodestring(b'aHR0cDovL2l2dWV0dmd1aWRlLmNvbS9pdnVlZ3VpZGV4bWwv==')
CatFile = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ivueguide', 'resources', 'categories', addon.getSetting('categories.path')+'.ini'))
demand = xbmcvfs.File('special://profile/addon_data/script.ivueguide/resources/catchup.xml','rb').read()
dialog = xbmcgui.Dialog() 

	#Plays a video
def playMedia(name, image, link, mediaType='Video') :
    li = xbmcgui.ListItem(label=name, iconImage=image, thumbnailImage=image, path=link)
    li.setInfo(type=mediaType, infoLabels={ "Title": name })
    xbmc.Player().play(item=link, listitem=li)

	#Displays a notification to the user
def notify(addonId, message, timeShown=5000):
    addon = xbmcaddon.Addon(addonId)
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (addon.getAddonInfo('name'), message, timeShown, addon.getAddonInfo('icon')))

	#Shows an error to the user and logs it
def showError(addonId, errorMessage):
    notify(addonId, errorMessage)
    xbmc.log(errorMessage, xbmc.LOGERROR)

	#Download a file url/file to save
def download_file(url,file):
    urllib.urlretrieve(url, file)

	#Create user addon directory
def create_userdata(AddOnID):
    addon_data_dir = os.path.join(xbmc.translatePath("special://userdata/addon_data" ).decode("utf-8"), AddOnID)
    if not os.path.exists(addon_data_dir):
        os.makedirs(addon_data_dir)	
		
def get_setting(addonId,setting):
	addon = xbmcaddon.Addon(addonId)
	return addon.getSetting(setting)
    
def set_setting(addonId,setting, string):
	addon = xbmcaddon.Addon(addonId)
	return addon.setSetting(setting, string)

def remove_formatting(label):
    label = re.sub(r"\[/?[BI]\]",'',label)
    label = re.sub(r"\[/?COLOR.*?\]",'',label)
    return label

def unescape(text):
    text = text.replace('&amp;',  '&')
    text = text.replace('&quot;', '"')
    text = text.replace('&apos;', '\'')
    text = text.replace('&gt;',   '>')
    text = text.replace('&lt;',   '<')
    return text

def folder():
	ivuedirectcry = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ivueguide'))
	if not os.path.exists(ivuedirectcry):
	    os.makedirs(ivuedirectcry)
	return ivuedirectory

def calculateTime(dt):
    return time.mktime(dt.timetuple())

def percent(start_time, end_time):
    total = calculateTime(end_time) - calculateTime(start_time)
    current_time = datetime.datetime.now()
    current = calculateTime(current_time) - calculateTime(start_time)
    percentagefloat = (100.0 * current) / total
    return int(round(percentagefloat))
	
def path():
    ivuedir = base64.decodestring(b'aHR0cDovL2l2dWV0dmd1aWRlLmNvbS9pdnVlZ3VpZGV4bWwv==')
    return user

def formatDate(timestamp, longdate=False, day=False):
    if timestamp and day == True:
        today = datetime.datetime.today()
        tomorrow = today + datetime.timedelta(days=1)
        yesterday = today - datetime.timedelta(days=1)
        if today.date() == timestamp.date():
            return 'Today'
        elif tomorrow.date() == timestamp.date():
            return 'Tomorrow'
        elif yesterday.date() == timestamp.date():
            return 'Yesterday'
        else:
            return timestamp.strftime("%A")
    elif timestamp and day == False:
        if longdate == True:
            today = datetime.datetime.today()
            tomorrow = today + datetime.timedelta(days=1)
            yesterday = today - datetime.timedelta(days=1)
            restofdate = timestamp.strftime("%d %B")
            if today.date() == timestamp.date():
                day = 'Today ' + restofdate
                return day
            elif tomorrow.date() == timestamp.date():
                day = 'Tomorrow ' + restofdate
                return day
            elif yesterday.date() == timestamp.date():
                day = 'Yesterday ' + restofdate
                return day
            else:
                return timestamp.strftime("%A %d %B")

        else:
            today = datetime.datetime.today()
            tomorrow = today + datetime.timedelta(days=1)
            yesterday = today - datetime.timedelta(days=1)
            if today.date() == timestamp.date():
                day = 'Today'
                return day
            elif tomorrow.date() == timestamp.date():
                day = 'Tomorrow'
                return day
            elif yesterday.date() == timestamp.date():
                day = 'Yesterday'
                return day
            else:
                return timestamp.strftime("%a %d %b")
    else:
        return ''


def addons(shortcut=None):
    resp = ''
    filter = []
    dialog = xbmcgui.Dialog()
    if not shortcut: 
        shortcut = ''
        resp = dialog.select('[COLOR fffea800]iVue Default Shortcuts[/COLOR]', ['BBC iPlayer', 'ITV player', 'Project D', 'Skynet', 'Covenant', 'Specto', 'Youtube', 'WolfPack', 'Supremacy', 'Picasso'])
    if resp == 0 or shortcut ==1:
        title = 'BBC iPlayer'
        image = 'special://home/addons/script.ivueguide/resources/png/bbc icon.png'
        link = 'RunAddon(plugin.video.iplayerwww)'
        filter.append(title)
        filter.append(image)
        filter.append(link)
    if resp == 1 or shortcut ==2:
        title = 'ITV Player'
        image = 'special://home/addons/script.ivueguide/resources/png/itv icon.png'
        link = 'RunAddon(plugin.video.itv)'
        filter.append(title)
        filter.append(image)
        filter.append(link)
    if resp == 2 or shortcut ==3:
        title = 'Project D'
        image = 'special://home/addons/script.ivueguide/resources/png/projectd.png'
        link = 'RunAddon(plugin.video.pdsports)'
        filter.append(title)
        filter.append(image)
        filter.append(link)
    if resp == 3 or shortcut ==4:
        title = 'Skynet'
        image = 'special://home/addons/script.ivueguide/resources/png/skynet.png'
        link = 'RunAddon(plugin.video.SkyNet)'
        filter.append(title)
        filter.append(image)
        filter.append(link)
    if resp == 4 or shortcut ==5:
        title = 'Covenant'
        image = 'special://home/addons/script.ivueguide/resources/png/Covenant.png'
        link = 'RunAddon(plugin.video.covenant)'
        filter.append(title)
        filter.append(image)
        filter.append(link)
    if resp == 5 or shortcut ==6:
        title = 'Specto'
        image = 'special://home/addons/script.ivueguide/resources/png/specto icon.png'
        link = 'RunAddon(plugin.video.specto)'
        filter.append(title)
        filter.append(image)
        filter.append(link)
    if resp == 6 or shortcut ==7:
        title = 'Youtube'
        image = 'special://home/addons/script.ivueguide/resources/png/youtube.png'
        link = 'RunAddon(plugin.video.youtube)'
        filter.append(title)
        filter.append(image)
        filter.append(link)
    if resp == 7 or shortcut ==8:
        title = 'WolfPack'
        image = 'special://home/addons/script.ivueguide/resources/png/wolfpack.png'
        link = 'RunAddon(plugin.video.wolfpack)'
        filter.append(title)
        filter.append(image)
        filter.append(link)
    if resp == 8 or shortcut ==9:
        title = 'Supremacy'
        image = 'special://home/addons/script.ivueguide/resources/png/supremacy.png'
        link = 'RunAddon(plugin.video.supremacy)'
        filter.append(title)
        filter.append(image)
        filter.append(link)
    if resp == 9 or shortcut ==10:
        title = 'Picasso'
        image = 'special://home/addons/script.ivueguide/resources/png/picasso.png'
        link = 'RunAddon(plugin.video.picasso)'
        filter.append(title)
        filter.append(image)
        filter.append(link)
    return filter