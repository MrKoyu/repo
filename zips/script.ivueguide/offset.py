import sqlite3
import xbmc
import xbmcgui
import xbmcaddon
import os, re
import xbmcgui
import json
import time
import datetime
from guideTypes import *

def adapt_datetime(ts):
    return time.mktime(ts.timetuple())

def convert_datetime(ts):
    try:
        return datetime.datetime.fromtimestamp(float(ts))
    except ValueError:
        return None

addonID = 'script.ivueguide'
addon = xbmcaddon.Addon(addonID)
current_xml = int(addon.getSetting('xmltv.type'))
gTypes = GuideTypes()
typeName = gTypes.getGuideDataItem(current_xml, 3)
path_to_channels = xbmc.translatePath('special://profile/addon_data/script.ivueguide/%s' % typeName)
timeshift = xbmc.translatePath('special://profile/addon_data/script.ivueguide/timezone.ini')
xml = open(path_to_channels).read()

shift = addon.getSetting('shift.time')
timeDiff = time.strptime(shift[1:],'%H:%M')
profilePath = xbmc.translatePath(addon.getAddonInfo('profile'))
databasePath = os.path.join(profilePath, 'master.db')
sqlite3.register_adapter(datetime.datetime, adapt_datetime)
sqlite3.register_converter('timestamp', convert_datetime)
conn = sqlite3.connect(databasePath, detect_types=sqlite3.PARSE_DECLTYPES)    	
c = conn.cursor()
d = xbmcgui.Dialog()
prnum=""
try:
    prnum= sys.argv[ 1 ]
except:
    pass


def searchXml(item, start, end):
    try: r = re.search("(?i)" + start + "([\S\s]+?)" + end, item).group(1)
    except: r = ''
    return r


def parseTime(origTime, new=None, channelOffset=None):
    if origTime.find(' ') != -1:
        dateParts = origTime.split()
        if len(dateParts) == 2:
            dateString = dateParts[0]
            offset = dateParts[1]
            if len(offset) == 5:
                offSign = offset[0]
                offHrs = int(offset[1:3])
                offMins = int(offset[-2:])
                td = datetime.timedelta(minutes=offMins, hours=offHrs)
            else:
                td = datetime.timedelta(seconds=0)
        elif len(dateParts) == 1:
            dateString = dateParts[0]
            td = datetime.timedelta(seconds=0)
        else:
            return None

        try:
            t_tmp = datetime.datetime.strptime(dateString, '%Y%m%d%H%M%S')
        except TypeError:
            t_tmp = datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString, '%Y%m%d%H%M%S')))
        if offSign == '+':
            t = t_tmp - td
        elif offSign == '-':
            t = t_tmp + td
        else:
            t = t_tmp
        if new is not None and channelOffset is None:
            if '+' in shift:
                t = t + datetime.timedelta(minutes=timeDiff.tm_min, hours=timeDiff.tm_hour)
            elif '-' in shift:
                t = t - datetime.timedelta(minutes=timeDiff.tm_min, hours=timeDiff.tm_hour)

        if new is not None and channelOffset is not None:
            userOffset = time.strptime(channelOffset[1:],'%H:%M')
            if '+' in channelOffset:
                t = t + datetime.timedelta(minutes=userOffset.tm_min, hours=userOffset.tm_hour)
            elif '-' in channelOffset:
                t = t - datetime.timedelta(minutes=userOffset.tm_min, hours=userOffset.tm_hour)

        is_dst = time.daylight and time.localtime().tm_isdst > 0
        utc_offset = - (time.altzone if is_dst else time.timezone)
        td_local = datetime.timedelta(seconds=utc_offset)

        t = t + td_local

        return t

    else:
        return None


def update_time(channel, channelOffset=None, reset=None):
    programs = re.compile('<programme(.+?)</programme>', re.DOTALL).findall(xml)
    programme = 0
    for program in programs:
        channels = searchXml(program, 'channel="', '">')
        if channels == channel:
            title = searchXml(program, '<title lang=".+?">', '</title>')
            starttime = searchXml(program, 'start="', '"')
            endtime = searchXml(program, 'stop="', '"')
            oldstarttime = parseTime(starttime)
            oldendtime = parseTime(endtime)
            correctStart = parseTime(starttime, new='yes', channelOffset=channelOffset)
            correctEnd = parseTime(endtime, new='yes', channelOffset=channelOffset)
            if reset == 'yes':
                c.execute("UPDATE programs SET start_date=?, end_date=? WHERE channel=? AND title=? AND start_date=?", [oldstarttime, oldendtime, channels.decode("utf-8"), title.decode("utf-8"), correctStart])
            else:
                c.execute("UPDATE programs SET start_date=?, end_date=? WHERE channel=? AND title=? AND start_date=?", [correctStart, correctEnd, channel.decode("utf-8"), title.decode("utf-8"), oldstarttime])
    conn.commit()


def Timeshift():
    saved = {}
    if os.path.exists(timeshift):
        findSaved = open(timeshift).readlines()
        for item in findSaved:
            saved[item.split(' =')[0]] = item.split(' = ')[1]
    channels = {}
    getChannels = re.compile('<channel(.+?)</channel>', re.DOTALL).findall(xml)
    for channel in getChannels:
        cid = searchXml(channel, 'id="', '">').replace("'", "")
        if not cid in saved:
            title = searchXml(channel, '<display-name lang=".+?">', '</display-name>')
            channels[title] = cid
    channellist = sorted(channels)
    selections = d.multiselect('Please select the channels you would like to adjust', channellist)

    if not selections:
        selections = []

    for selection in selections:
        if selection < -1:
            addon.openSettings()
        else:
            channelTitle = channellist[selection]
            update_time(channels[channelTitle])
            f = open(timeshift, 'a+')
            chan = {}
            f.write('%s = %s\n' % (channels[channelTitle], shift))
    d.ok('iVue TV Guide', 'Your selected channels have been shifted.', 'They will be re-configured next time', 'you launch the guide')
    c.close()


def resetTimeshift():
    saved = []
    if os.path.exists(timeshift):
        findSaved = open(timeshift).readlines()
        for item in findSaved:
            saved.append(item)
    else:
        d.ok('iVue Time shift', 'No channels have been found','')
        return
    if len(saved) <= 0:
        d.ok('iVue Time shift', 'No channels have been found','')
        return
    channellist = sorted(saved)
    selections = d.multiselect('Please select the channels you would like to reset', channellist)

    if not selections:
        d.ok('iVue Time shift', 'No channels have been reset','')
        return
    else:
        for selection in selections:
            saved.remove(channellist[selection])
            channelTitle = channellist[selection]
            channel = channelTitle.split(' =')[0]
            channelTime = channelTitle.split(' = ')[1][:5]
            update_time(channel, channelOffset=channelTime, reset='yes')
                    
        f = open(timeshift, 'w')
        for item in saved:
            if len(item) > 1:
                f.writelines('%s' % item)
        f.close()
        d.ok('iVue TV Guide', 'Your selected channels have been reset.', 'They will be re-configured next time', 'you launch the guide')
        c.close()


if prnum == 'update':
    Timeshift()
 
elif prnum == 'reset':
    resetTimeshift()

