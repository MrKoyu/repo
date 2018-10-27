# -*- coding: utf-8 -*-

#      Copyright (C) 2014 Tommy Winther
#      http://tommy.winther.nu
#
#      Modified for FTV Guide (09/2014 onwards)
#      by Thomas Geppert [bluezed] - bluezed.apps@gmail.com
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

import datetime
import threading
import time
import xbmc
import xbmcgui
import source as src
from notification import Notification
from strings import *
import os
import sys
import re
import colors
import streaming
import utils
import json
import urllib
import reset
import urllib2
import config
import base64
from xml.etree import ElementTree


DEBUG = False

MODE_EPG = 'EPG'
MODE_TV = 'TV'
MODE_OSD = 'OSD'

ACTION_LEFT = 1
ACTION_RIGHT = 2
ACTION_UP = 3
ACTION_DOWN = 4
ACTION_PAGE_UP = 5
ACTION_PAGE_DOWN = 6
ACTION_SELECT_ITEM = 7
ACTION_PARENT_DIR = 9
ACTION_PREVIOUS_MENU = 10
ACTION_SHOW_INFO = 11
ACTION_NEXT_ITEM = 14
ACTION_PREV_ITEM = 15
ACTION_PLAY = 68
ACTION_STOP = 13

ACTION_MOUSE_LEFT_CLICK = 100
ACTION_MOUSE_RIGHT_CLICK = 101
ACTION_MOUSE_MIDDLE_CLICK = 102
ACTION_MOUSE_DOUBLE_CLICK = 103
ACTION_MOUSE_WHEEL_UP = 104
ACTION_MOUSE_WHEEL_DOWN = 105
ACTION_MOUSE_MOVE = 107
ACTION_MOUSE_LONG_CLICK = 108

ACTION_GESTURE_SWIPE_DOWN = 541
ACTION_GESTURE_SWIPE_DOWN_TEN = 550
ACTION_GESTURE_SWIPE_LEFT = 511
ACTION_GESTURE_SWIPE_LEFT_TEN = 520
ACTION_GESTURE_SWIPE_RIGHT = 521
ACTION_GESTURE_SWIPE_RIGHT_TEN = 530
ACTION_GESTURE_SWIPE_UP = 531
ACTION_GESTURE_SWIPE_UP_TEN = 540

REMOTE_0 = 58
REMOTE_1 = 59
REMOTE_2 = 60
REMOTE_3 = 61
REMOTE_4 = 62
REMOTE_5 = 63
REMOTE_6 = 64
REMOTE_7 = 65
REMOTE_8 = 66
REMOTE_9 = 67

KEY_BUTTON_X =  258
KEY_NAV_BACK = 92
KEY_CONTEXT_MENU = 117
KEY_HOME = 159
KEY_ESC = 61467

CHANNELS_PER_PAGE = 8

HALF_HOUR = datetime.timedelta(minutes=30)

# Custom

IGNORESTRM = ADDON.getSetting('ignore.stream') == 'true'

# for extras players

ADDONID = 'script.ivueguide'
ADDON = xbmcaddon.Addon(ADDONID)
HOME = ADDON.getAddonInfo('path')
ICON = os.path.join(HOME, 'icon.png')
ICON = xbmc.translatePath(ICON)
PROFILE = xbmc.translatePath(ADDON.getAddonInfo('profile'))
RESOURCES = os.path.join(HOME, 'resources')
SKIN = ADDON.getSetting('skin')
S_ADDON = os.path.join(PROFILE, 'resources', 'skins', SKIN, '720p', 'script-tvguide-streamcustom.xml')
SKINCOLOURS = xbmc.translatePath(os.path.join(PROFILE, 'resources', 'skins', SKIN, '720p', 'default_colours.txt'))
SKINFOLDER = os.path.join(PROFILE)
#Karls changes

baseUrl = base64.b64decode('aHR0cDovL2xpdmVvbnNhdC5jb20=')


streams = streaming.StreamsService(ADDON)
shift = ADDON.getSetting('los.shift.time')
timeDiff = time.strptime(shift[1:],'%H:%M')



if ADDON.getSetting('categories.launch') == 'true' and os.path.exists(utils.CatFile):
    filter = []
    with open(utils.CatFile ,'rb') as file:
        lines = file.read().splitlines()

        file.close()
        for line in lines:
            if '=' in line:
                name = line.strip().split('=')[1]
                if name not in filter:
                    filter.append(name)
    filter.insert(0, "All channels")
    resp = utils.dialog.select('Select A Category', filter)
    if resp > -1:       
        ADDON.setSetting('category', filter[resp])

def timedelta_total_seconds(timedelta):
    return (
        timedelta.microseconds + 0.0 +
        (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6

#Karls changes end


# Below here needed for player


def debug(s):
    if DEBUG:
        xbmc.log(str(s), xbmc.LOGDEBUG)


class Point(object):

    def __init__(self):
        self.x = self.y = 0

    def __repr__(self):
        return 'Point(x=%d, y=%d)' % (self.x, self.y)


class EPGView(object):

    def __init__(self):
        self.top = self.left = self.right = self.bottom = self.width = \
            self.cellHeight = 0


class ControlAndProgram(object):

    def __init__(self, control, program):
        self.control = control
        self.program = program

C_MAIN_PLUGIN_ICON = 6007
C_MAIN_PLUGIN_NAME = 6008
C_MAIN_OSD_PLUGIN_ICON = 6017
C_MAIN_OSD_PLUGIN_NAME = 6018

class TVGuide(xbmcgui.WindowXML):
    C_MAIN_PROGRESS = 3996
    C_MAIN_DURATION = 3998
    C_MAIN_DATE_LONG = 3999
    C_MAIN_DATE = 4000
    C_MAIN_TITLE = 4020
    C_MAIN_TIME = 4021
    C_MAIN_DESCRIPTION = 4022
    C_MAIN_IMAGE = 4023
    C_MAIN_LOGO = 4024
    C_MAIN_CHANTITLE = 4025
    C_MAIN_TIMEBAR = 4100
    C_MAIN_LOADING = 4200
    C_MAIN_LOADING_PROGRESS = 4201
    C_MAIN_LOADING_TIME_LEFT = 4202
    C_MAIN_LOADING_CANCEL = 4203
    C_MAIN_MOUSE_CONTROLS = 4300
    C_MAIN_MOUSE_HOME = 4301
    C_MAIN_MOUSE_LEFT = 4302
    C_MAIN_MOUSE_UP = 4303
    C_MAIN_MOUSE_DOWN = 4304
    C_MAIN_MOUSE_RIGHT = 4305
    C_MAIN_MOUSE_EXIT = 4306
    C_MAIN_MOUSE_CATS = 4307
    C_MAIN_BACKGROUND = 4600
    C_MAIN_EPG = 5000
    C_MAIN_EPG_VIEW_MARKER = 5001
    C_MAIN_OSD = 6000
    C_MAIN_OSD_TITLE = 6001
    C_MAIN_OSD_TIME = 6002
    C_MAIN_OSD_DESCRIPTION = 6003
    C_MAIN_OSD_CHANNEL_LOGO = 6004
    C_MAIN_OSD_CHANNEL_TITLE = 6005
    C_PREV_OSD_TITLE = 6009
    C_NEXT_OSD_TITLE = 6010
    C_PREV_OSD_TIME = 6011
    C_NEXT_OSD_TIME = 6012
    C_MAIN_OSD_PROGRESS = 6013
    C_MAIN_OSD_DURATION = 6015
    C_MAIN_OSD_PROGIMAGE = 6016
    C_MAIN_OSD_NEXTIMAGE = 6019
    C_MAIN_OSD_NOW = 6020
    C_MAIN_OSD_NEXT = 6021
    C_MAIN_OSD_NEXTDESC = 6022
    C_MAIN_CAT_LABEL = 6006

    def __new__(cls):

        # Skin in resources
        # return super(TVGuide, cls).__new__(cls, 'script-tvguide-main.xml', ADDON.getAddonInfo('path'), SKIN)
        # Skin in user settings

        return super(TVGuide, cls).__new__(cls,
                'script-tvguide-main.xml', SKINFOLDER,
                SKIN)

    def __init__(self):

        super(TVGuide, self).__init__()
        self.notification = None
        self.redrawingEPG = False
        self.isClosing = False
        self.controlAndProgramList = list()
        self.ignoreMissingControlIds = list()
        self.channelIdx = 0
        self.focusPoint = Point()
        self.epgView = EPGView()
        self.streamingService = streaming.StreamsService(ADDON)
        self.player = xbmc.Player()
        self.database = None
        self.mode = MODE_EPG
        self.currentChannel = None
        self.category = ADDON.getSetting('category')
        self.osdCategory = self.category
        self.lastchan_file = xbmc.translatePath(os.path.join(ADDON.getAddonInfo('profile'), 'lastchannel'))
        self.lastPlayed = None
        self.osdLastProg = None

        f = utils.xbmcvfs.File(utils.CatFile,'rb')
        lines = f.read().splitlines()
        f.close()
        categories = set()
        for line in lines:
            if "=" not in line:
                continue
            name,cat = line.split('=')
            categories.add(cat)
        categories = sorted(categories)
        self.categories = categories 

        self.osdEnabled = ADDON.getSetting('enable.osd') == 'true' \
            and ADDON.getSetting('alternative.playback') != 'true'
        self.alternativePlayback = \
            ADDON.getSetting('alternative.playback') == 'true'
        self.osdChannel = None
        self.osdProgram = None

        # find nearest half hour

        self.viewStartDate = datetime.datetime.today()
        self.viewStartDate -= \
            datetime.timedelta(minutes=self.viewStartDate.minute % 30,
                               seconds=self.viewStartDate.second)

    def getControl(self, controlId):
        try:
            return super(TVGuide, self).getControl(controlId)
        except:
            if controlId in self.ignoreMissingControlIds:
                return None
            #if not self.isClosing:
                #self.close()
            return None

    def close(self):
        if not self.isClosing:
            self.isClosing = True
            if self.player.isPlaying():
                if ADDON.getSetting('stop-stream') == "true":
                    self.player.stop()
            if self.database:
                self.database.close(super(TVGuide, self).close)

            else:
                if self.player.isPlaying():
                    if ADDON.getSetting('stop-stream') == "true":
                        self.player.stop()
                super(TVGuide, self).close()          

    def onInit(self):
        self._hideControl(self.C_MAIN_MOUSE_CONTROLS, self.C_MAIN_OSD)
        self._showControl(self.C_MAIN_EPG, self.C_MAIN_LOADING)
        self.setControlLabel(self.C_MAIN_LOADING_TIME_LEFT,
                             strings(BACKGROUND_UPDATE_IN_PROGRESS))
        self.setFocusId(self.C_MAIN_LOADING_CANCEL)

        control = self.getControl(self.C_MAIN_EPG_VIEW_MARKER)
        if control:
            (left, top) = control.getPosition()
            self.focusPoint.x = left

            self.epgView.left = left
            self.epgView.top = top
            self.epgView.right = left + control.getWidth()
            self.epgView.bottom = top + control.getHeight()
            self.epgView.width = control.getWidth()
            self.epgView.cellHeight = control.getHeight() \
                / CHANNELS_PER_PAGE
            self.focusPoint.y = top

        if self.database:
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)
        else:
            try:
                self.database = src.Database()
            except src.SourceNotConfiguredException:
                self.onSourceNotConfigured()
                self.close()
                return
            self.database.setCategory(self.category)
            if self.category == '':
                self.setControlLabel(self.C_MAIN_CAT_LABEL, '[B]All Channels[/B]')
            else:
                self.setControlLabel(self.C_MAIN_CAT_LABEL, '[B]%s[/B]' % self.category)
            self.database.initialize(self.onSourceInitialized,
                    self.isSourceInitializationCancelled)

        self.updateTimebar()

    def onAction(self, action):
        debug('Mode is: %s' % self.mode)

        if self.mode == MODE_TV:
            self.onActionTVMode(action)
        elif self.mode == MODE_OSD:
            self.onActionOSDMode(action)
        elif self.mode == MODE_EPG:
            self.onActionEPGMode(action)

    def onActionTVMode(self, action):

        if action.getId() == ACTION_PAGE_UP:
            self._channelUp()

        elif action.getId() == ACTION_PAGE_DOWN:
            self._channelDown()

        elif action.getId() in [ACTION_GESTURE_SWIPE_LEFT, ACTION_LEFT, KEY_CONTEXT_MENU]:
            self.osdEpg(self.database.getCategory())

        elif action.getId() in [ACTION_GESTURE_SWIPE_UP, REMOTE_0]:
            if self.lastPlayed:
                channel = self.lastPlayed
                program = self.database.getCurrentProgram(channel)
                self.osdProgram = program
                self.play(program)

        elif action.getId() in [ACTION_GESTURE_SWIPE_RIGHT, REMOTE_1, REMOTE_2, REMOTE_3, REMOTE_4, REMOTE_5, REMOTE_6, REMOTE_7, REMOTE_8, REMOTE_9]:
            self.playByNumOSD(action.getId())

        elif not self.osdEnabled:
            pass  # skip the rest of the actions

        elif action.getId() in [ACTION_PARENT_DIR, KEY_NAV_BACK, ACTION_PREVIOUS_MENU,KEY_BUTTON_X, ACTION_STOP]:
            self.viewStartDate = datetime.datetime.today()
            self.viewStartDate -= \
                datetime.timedelta(minutes=self.viewStartDate.minute % 30,
                                   seconds=self.viewStartDate.second)
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)

        elif action.getId() in [ACTION_SHOW_INFO, ACTION_UP, ACTION_DOWN, ACTION_MOUSE_WHEEL_UP, ACTION_MOUSE_WHEEL_DOWN,ACTION_GESTURE_SWIPE_DOWN]:
            self.osdChannel = self.currentChannel
            self.osdProgram = self.database.getCurrentProgram(self.osdChannel)
            self._showOsd()


    def onActionOSDMode(self, action):

        if action.getId() in [ACTION_PARENT_DIR, KEY_NAV_BACK, ACTION_PREVIOUS_MENU, ACTION_SHOW_INFO, ACTION_MOUSE_RIGHT_CLICK]:
            self._hideOsd()

        elif action.getId() in [KEY_BUTTON_X, ACTION_STOP]:
            self._hideOsd()
            self.viewStartDate = datetime.datetime.today()
            self.viewStartDate -= \
                datetime.timedelta(minutes=self.viewStartDate.minute % 30,
                                   seconds=self.viewStartDate.second)
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)

        elif action.getId() == REMOTE_0:
            if self.lastPlayed:
                channel = self.lastPlayed
                program = self.database.getCurrentProgram(channel)
                self.osdProgram = program
                self.play(program)

        elif action.getId() in [REMOTE_1, REMOTE_2, REMOTE_3, REMOTE_4, REMOTE_5, REMOTE_6, REMOTE_7, REMOTE_8, REMOTE_9]:
            self.playByNumOSD(action.getId())

        #elif action.getId() in [KEY_CONTEXT_MENU]:
            #self._showosdContextMenu(self.osdProgram)
            
        elif action.getId() in [ACTION_SELECT_ITEM, ACTION_PLAY, ACTION_MOUSE_LEFT_CLICK]:
            if self.play(self.osdProgram):
                self._hideOsd()
                
        elif action.getId() == ACTION_PAGE_UP:
            self._channelUp()
            self._hideOsd()
            
        elif action.getId() == ACTION_PAGE_DOWN:
            self._channelDown()
            self._hideOsd()
            
        elif action.getId() in [ACTION_LEFT, ACTION_GESTURE_SWIPE_LEFT]:
            previousProgram = self.database.getPreviousProgram(self.osdProgram)
            if previousProgram:
                self.osdProgram = previousProgram
                self._showOsd()
            self.osdActive = True
                
        elif action.getId() in [ACTION_RIGHT, ACTION_GESTURE_SWIPE_RIGHT]:
            nextProgram = self.database.getNextProgram(self.osdProgram)
            if nextProgram:
                self.osdProgram = nextProgram
                self._showOsd()
            self.osdActive = True

        elif action.getId() in [ACTION_UP, ACTION_MOUSE_WHEEL_UP, ACTION_GESTURE_SWIPE_UP]:           
            self.osdChannel = self.database.getPreviousChannel(self.osdChannel)
            self.osdProgram = self.database.getCurrentProgram(self.osdChannel)
            self._showOsd()
            self.osdActive = True

        elif action.getId() in [ACTION_DOWN, ACTION_MOUSE_WHEEL_DOWN, ACTION_GESTURE_SWIPE_DOWN]:
            self.osdChannel = self.database.getNextChannel(self.osdChannel)
            self.osdProgram = self.database.getCurrentProgram(self.osdChannel)
            self._showOsd()
            self.osdActive = True
            
    def onActionEPGMode(self, action):
        controlInFocus = None
        currentFocus = self.focusPoint
        try:
            controlInFocus = self.getFocus()
            if controlInFocus in [elem.control for elem in self.controlAndProgramList]:
                (left, top) = controlInFocus.getPosition()
                currentFocus = Point()
                currentFocus.x = left + (controlInFocus.getWidth() / 2)
                currentFocus.y = top + (controlInFocus.getHeight() / 2)
        except Exception:
            control = self._findControlAt(self.focusPoint)
            if control is None and len(self.controlAndProgramList) > 0:
                control = self.controlAndProgramList[0].control
            if control is not None:
                self.setFocus(control)
                return
        program = self._getProgramFromControl(controlInFocus)
        programInfo = ''
        if program is not None:
            programInfo = program

        if action.getId() in [ACTION_PARENT_DIR, KEY_NAV_BACK]:
            self._skinexitMenu(programInfo)

        # catch the ESC key
        elif action.getId() == ACTION_PREVIOUS_MENU and action.getButtonCode() == KEY_ESC:
            self.close()
            return
        elif action.getId() == ACTION_MOUSE_MOVE:

            self._showControl(self.C_MAIN_MOUSE_CONTROLS)
            return
        elif action.getId() in [ACTION_SHOW_INFO, ACTION_MOUSE_MIDDLE_CLICK, ACTION_MOUSE_DOUBLE_CLICK, ACTION_MOUSE_LONG_CLICK]:
            self._infoMenu()

        elif action.getId() == KEY_CONTEXT_MENU:

            if self.player.isPlaying():
                self._hideEpg()

        if action.getId() == ACTION_LEFT:
            self._left(currentFocus)
        elif action.getId() == ACTION_RIGHT:
            self._right(currentFocus)
        elif action.getId() == ACTION_UP:
            self._up(currentFocus)
        elif action.getId() == ACTION_DOWN:
            self._down(currentFocus)
        elif action.getId() == ACTION_NEXT_ITEM:
            self._nextDay()
        elif action.getId() == ACTION_PREV_ITEM:
            self._previousDay()
        elif action.getId() == ACTION_PAGE_UP:
            self._moveUp(CHANNELS_PER_PAGE)
        elif action.getId() == ACTION_PAGE_DOWN:
            self._moveDown(CHANNELS_PER_PAGE)
        elif action.getId() == ACTION_MOUSE_WHEEL_UP:
            self._moveUp(scrollEvent=True)
        elif action.getId() == ACTION_MOUSE_WHEEL_DOWN:
            self._moveDown(scrollEvent=True)
        elif action.getId() == KEY_HOME:
            self.viewStartDate = datetime.datetime.today()
            self.viewStartDate -= datetime.timedelta(minutes=self.viewStartDate.minute % 30,
                                                     seconds=self.viewStartDate.second)
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)

        elif action.getId() in [KEY_CONTEXT_MENU, ACTION_PREVIOUS_MENU] and controlInFocus is not None:
            program = self._getProgramFromControl(controlInFocus)
            if program is not None:
                self._showContextMenu(program)

        elif action.getId() in [ACTION_GESTURE_SWIPE_DOWN, REMOTE_1, REMOTE_2, REMOTE_3, REMOTE_4, REMOTE_5, REMOTE_6, REMOTE_7, REMOTE_8, REMOTE_9]:
            self.playByNum(action.getId())

        elif action.getId() == REMOTE_0:
            if self.lastPlayed:
                channel = self.lastPlayed
                program = self.database.getCurrentProgram(channel)
                self.play(program)
        else:
            xbmc.log('[script.ivueguide] Unhandled ActionId: '
                     + str(action.getId()), xbmc.LOGDEBUG)

    def onClick(self, controlId):
        if controlId in [self.C_MAIN_LOADING_CANCEL, self.C_MAIN_MOUSE_EXIT]:
            self.close()
            return

        if self.isClosing:
            return

        if controlId == self.C_MAIN_MOUSE_CATS:
            self._showCatMenu()

        elif controlId == self.C_MAIN_MOUSE_HOME:
            self.viewStartDate = datetime.datetime.today()
            self.viewStartDate -= datetime.timedelta(minutes=self.viewStartDate.minute % 30, seconds=self.viewStartDate.second)
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)
            return
        elif controlId == self.C_MAIN_MOUSE_LEFT:
            self.viewStartDate -= datetime.timedelta(hours=2)
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)
            return
        elif controlId == self.C_MAIN_MOUSE_UP:
            self._moveUp(count=CHANNELS_PER_PAGE)
            return
        elif controlId == self.C_MAIN_MOUSE_DOWN:
            self._moveDown(count=CHANNELS_PER_PAGE)
            return
        elif controlId == self.C_MAIN_MOUSE_RIGHT:
            self.viewStartDate += datetime.timedelta(hours=2)
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)
            return
        else:
            program = self._getProgramFromControl(self.getControl(controlId))
            self.play(program)

    def play(self,program, demand=True):

        if program is None:
            return

        playChannel = True
        if demand == True:
            if program.startDate and program.endDate:
                if program.endDate < datetime.datetime.now():
                    playChannel = False
                    self.checkAddons(program)
                elif program.startDate > datetime.datetime.now():
                    playChannel = False
                    if program.notificationScheduled:
                        yes_pressed=utils.dialog.yesno('[COLOR ffff7e14][B]IVUE REMINDER[/B][/COLOR]', 'Remove reminder for ', '[COLOR ffff7e14]'+program.title+'[/COLOR]  '+self.formatTime(program.startDate),nolabel='Cancel',yeslabel='Remove')

                        if yes_pressed:
                            xbmc.executebuiltin('XBMC.Notification(%s removed from planner, 2000, %s)' % (program.title, ICON))
                            self.notification.removeNotification(program)
                            if not xbmc.Player().isPlaying():
                                self.onRedrawEPG(self.channelIdx, self.viewStartDate)
                        else:
                            return
                    else:
                        yes_pressed=utils.dialog.yesno('[COLOR ffff7e14][B]IVUE REMINDER[/B][/COLOR]', 'Set reminder for ', '[COLOR ffff7e14]'+program.title+'[/COLOR]  '+self.formatTime(program.startDate),nolabel='Cancel',yeslabel='Set')

                        if yes_pressed:
                            xbmc.executebuiltin('XBMC.Notification(%s added to planner, 2000, %s)' % (program.title, ICON))
                            self.notification.addNotification(program)
                            if not xbmc.Player().isPlaying():
                                self.onRedrawEPG(self.channelIdx, self.viewStartDate)
                        else:
                            return
                else:
                    playChannel = True                
        if playChannel:
            if not self.playChannel(program.channel):
                result = self.streamingService.detectStream(program.channel)
                if not result:

                    # could not detect stream, show context menu

                    self._showContextMenu(program)
                elif type(result) == str:

                    # one single stream detected, save it and start streaming

                    self.database.setCustomStreamUrl(program.channel,
                            result)
                    self.playChannel(program.channel, program)
                else:

                    # multiple matches, let user decide

                    d = ChooseStreamAddonDialog(result)
                    d.doModal()
                    if d.stream is not None:
                        self.database.setCustomStreamUrl(program.channel,
                            d.stream)
                        self.playChannel(program.channel, program)
                    

                        # Custom ignore stream in database

                        if IGNORESTRM:

                            # self.database.deleteCustomStreamUrl(program.channel, program)

                            self.database.deleteCustomStreamUrl(program.channel)

                                          

    def playByNum(self, num):
        default = int(num) - 58
        validInput = self.database.getChannelList(onlyVisible=True,all=True)
        chanNum = utils.dialog.numeric(0,"Channel Number", str(default))

        if chanNum:
            if int(chanNum) -1 < int(len(validInput)) and int(chanNum) !=0:
                getNum = int(chanNum) -1
                for chan in range(0,1200,8):
                    if int(chanNum ) == chan and chan !=0:
                        self.focusPoint.y = self.epgView.top + self.epgView.cellHeight*7
                        getNum = int(chanNum) -8
                    if int(chanNum ) == (chan +1):
                        self.focusPoint.y = self.epgView.top
                        getNum = int(chanNum) -1
                    elif int(chanNum ) == (chan +2):
                        self.focusPoint.y = self.epgView.top + self.epgView.cellHeight*1
                        getNum = int(chanNum) -2
                    elif int(chanNum) == (chan +3):
                        self.focusPoint.y = self.epgView.top + self.epgView.cellHeight*2
                        getNum = int(chanNum) -3
                    elif int(chanNum) == (chan +4):
                        self.focusPoint.y = self.epgView.top + self.epgView.cellHeight*3
                        getNum = int(chanNum) -4
                    elif int(chanNum) == (chan +5):
                        self.focusPoint.y = self.epgView.top + self.epgView.cellHeight*4
                        getNum = int(chanNum) -5
                    elif int(chanNum) == (chan +6):
                        self.focusPoint.y = self.epgView.top + self.epgView.cellHeight*5
                        getNum = int(chanNum) -6
                    elif int(chanNum) == (chan +7):
                        self.focusPoint.y = self.epgView.top + self.epgView.cellHeight*6
                        getNum = int(chanNum) -7

                self.onRedrawEPG(getNum, self.viewStartDate)
                try:
                    controlInFocus = self.getFocus()
                except:
                    controlInFocus = None
                program = self._getProgramFromControl(controlInFocus)
                if program is not None and ADDON.getSetting('play.number')=='true':
                    self.play(program, demand=False)
            else:
                xbmc.executebuiltin('XBMC.Notification([B]%s[/B], invalid channel, 2000, %s)' % (chanNum,ICON))


    def playByNumOSD(self, num):
        default = int(num) - 58
        validInput = self.database.getChannelList(onlyVisible=True,all=True)
        chanNum = utils.dialog.numeric(0,"Channel Number", str(default))

        if chanNum:
            if int(chanNum) -1 < int(len(validInput)) and int(chanNum) !=0:
                self.osdChannel = self.database.getChannel(int(chanNum) -1)
                self.osdProgram = self.database.getCurrentProgram(self.osdChannel)
                self._showOsd()
                self.osdActive = True

                if self.osdProgram is not None:
                    self.play(self.osdProgram, demand=False)
            else:
                xbmc.executebuiltin('XBMC.Notification([B]%s[/B], invalid channel, 2000, %s)' % (chanNum,ICON))


    def checkAddons(self, program):
        matches = re.compile('name="(.*?)".+?type="(.*?)">(.*?)<').findall(utils.demand)
        ivueProgram = str(program.title).replace('!', '').replace(':', '')
        movie = ['movie','all']
        tv = ['tv','all']
        ivueAdd = '%2520'
        ivueEncode = '%20'
        ivueDash = '-'
        addons = {}
        if program.is_movie:
            for name, type, value in matches:
                if type in movie:
                    installed = value.split('plugin://')[1].split('/')[0]
                    name = utils.remove_formatting(name)
                    value = re.sub('&quot;','',value)
                    pathToaddon = os.path.join(xbmc.translatePath('special://home/addons'), installed) 
                    if os.path.exists(pathToaddon):
                        addons[name] = utils.unescape(value)

        else:
            for name, type, value in matches:
                if type in tv:
                    installed = value.split('plugin://')[1].split('/')[0]
                    name = utils.remove_formatting(name)
                    value = re.sub('&quot;','',value)
                    pathToaddon = os.path.join(xbmc.translatePath('special://home/addons'), installed) 
                    if os.path.exists(pathToaddon):
                        addons[name] = utils.unescape(value)
        names = sorted(addons)
 
        resp = utils.dialog.select('[COLOR fffea800]On Demand - %s[/COLOR]' % program.title, names)
        programTitle = ivueProgram.lower()
        if resp < 0:
            return
        else:
            addon_name = names[resp]
            programAdd = programTitle.replace(' ', ivueAdd)
            programEncode = programTitle.replace(' ', ivueEncode)
            programDash = programTitle.replace(' ', ivueDash)
            programItv = ''
            programItvName = ''
            if addon_name == '.ITV Hub':
                searchITV = '%s itvhub' % ivueProgram
                quoteurl = urllib.quote(searchITV)
                itvurl = 'https://www.google.co.uk/search?q=%s' % quoteurl
                req = urllib2.Request(itvurl)
                req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                foundProg = False
                gResult = re.compile('href="(.*?)"',re.DOTALL).findall(link)
                for site in gResult:
                    if 'itv.com/hub/' in site:
                        programItv = site.split('hub/')[1].split('/')[0]
                        programItvName = programItv
                        foundProg = True
                        break
                if foundProg == False:
                    utils.dialog.ok('[COLOR fffea800]ITV Hub[/COLOR]', program.title, 'Is not available for on demand right now', '')
                    return

            link = addons[addon_name].replace('ivueProgram',programTitle).replace('ivueAdd+', programAdd).replace('ivueAdd-', programDash).replace('ivueEncode', programEncode).replace('ivueItvName', programItvName).replace('ivueItv', programItv).replace('ivueflashshow', str(program.title.replace("'","!quote!"))).replace('ivueflashchan', str(program.channel.title))
            xbmc.executebuiltin(''+ link +'')


    def _showosdContextMenu(self, program):
        self.set_playing()
        self._hideControl(self.C_MAIN_MOUSE_CONTROLS)
        d = osdPopupMenu(self.database, program,
                      not program.notificationScheduled)
        d.doModal()
        buttonClicked = d.buttonClicked
        action = d.action
        del d

        if buttonClicked == PopupMenu.C_OSDPOPUP_REMIND:
            if program.notificationScheduled:
                self.notification.removeNotification(program)
            else:
                self.notification.addNotification(program)
 


    def _showContextMenu(self, program):
        self.set_playing()
        self._hideControl(self.C_MAIN_MOUSE_CONTROLS)
        d = PopupMenu(self.database, program,
                      not program.notificationScheduled)
        d.doModal()
        buttonClicked = d.buttonClicked
        action = d.action
        del d

        if action == KEY_NAV_BACK:
            self.focus_lastchan()

        if buttonClicked == PopupMenu.C_POPUP_REMIND:
            if program.notificationScheduled:
                self.notification.removeNotification(program)
            else:
                self.notification.addNotification(program)

            self.onRedrawEPG(self.channelIdx, self.viewStartDate)
 
        elif buttonClicked == PopupMenu.C_POPUP_CHOOSE_STREAM:

            d = StreamSetupDialog(self.database, program.channel)
            d.doModal()
            del d

        elif buttonClicked == PopupMenu.C_POPUP_CHANNELS:

            d = ChannelsMenu(self.database)
            d.doModal()
            del d
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)
        elif buttonClicked == PopupMenu.C_POPUP_QUIT:

            self.close()

        elif buttonClicked == 30011:

        # Custom addons1 to menu tab
            addon1 = ADDON.getSetting('CustomAddon1')
            xbmc.executebuiltin(''+ addon1 +'')

        elif buttonClicked == 30012:

        # Custom addons2 to menu tab........................
            addon2 = ADDON.getSetting('CustomAddon2')
            xbmc.executebuiltin(''+ addon2 +'')

        elif buttonClicked == 30013:

        # Custom addons3 to menu tab............
            addon3 = ADDON.getSetting('CustomAddon3')
            xbmc.executebuiltin(''+ addon3 +'')

        elif buttonClicked == 30014:

        # Custom addons4 to menu tab............
            addon4 = ADDON.getSetting('CustomAddon4')
            xbmc.executebuiltin(''+ addon4 +'')

        elif buttonClicked == 30015:

        # Custom addons5 to menu tab............
            addon5 = ADDON.getSetting('CustomAddon5')
            xbmc.executebuiltin(''+ addon5 +'')

        elif buttonClicked == 30016:

        # Custom addons6 to menu tab............
            addon6 = ADDON.getSetting('CustomAddon6')
            xbmc.executebuiltin(''+ addon6 +'')

        elif buttonClicked == 30017:

        # Custom addons7 to menu tab............
            addon7 = ADDON.getSetting('CustomAddon7')
            xbmc.executebuiltin(''+ addon7 +'')

        elif buttonClicked == 30018:

        # Custom addons8 to menu tab............
            addon8 = ADDON.getSetting('CustomAddon8')
            xbmc.executebuiltin(''+ addon8 +'')

        elif buttonClicked == 30019:

        # Custom addons9 to menu tab............
            addon9 = ADDON.getSetting('CustomAddon9')
            xbmc.executebuiltin(''+ addon9 +'')

        elif buttonClicked == 30020:

        # Custom addons10 to menu tab............
            addon10 = ADDON.getSetting('CustomAddon10')
            xbmc.executebuiltin(''+ addon10 +'')

    def set_removeReminders(self, program):
        title = 'REMINDER SET'
        title2 = 'REMINDER REMOVED'
        if program.notificationScheduled:
            xbmc.executebuiltin('XBMC.Notification(%s, , 2000, %s)' % (title2, ICON))
            self.notification.removeNotification(program)
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)
            return program
        else:
            xbmc.executebuiltin('XBMC.Notification(%s, , 2000, %s)' % (title, ICON))
            self.notification.addNotification(program)
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)
            return program


    def _skinexitMenu(self, program):
        d = ExitDialog()
        d.doModal()
        action = d.action
        buttonClicked = d.buttonClicked
        if buttonClicked == 2000:
            self.close()
        elif buttonClicked == 2001:
            self._showCatMenu()
        elif buttonClicked == 2002:
            self.programSearch()
        elif buttonClicked == 2003:
            self.getReminders()
        elif buttonClicked == 2004:
            self._showSchMenu(program)
        elif buttonClicked == 2005:
            self._infoMenu()
        elif buttonClicked == 2006:
            self._showToolsMenu(program)
        elif buttonClicked == 2007:
            self.player.stop()

    def _infoMenu(self):
        d = startUp()
        d.doModal()
        buttonClicked = d.buttonClicked
        action = d.action
        del d


    def _showSchMenu(self, program):
        today = datetime.datetime.today()
        for x in range(0, 1):
           Day = today + datetime.timedelta(days=x)
           now = Day.strftime(" %d %B ")
        for x in range(0, 2):
           Day = today + datetime.timedelta(days=x)
           one = Day.strftime("Tomorrow %d %B %Y")
        for x in range(0, 3):
           Day = today + datetime.timedelta(days=x)
           two = Day.strftime("%A %d %B %Y")

        resp = utils.dialog.select('[COLOR fffea800]iVue Schedule[/COLOR]', ['Today (%s)' % (now), '%s' % (one), '%s' % (two)])
        if resp <0:
            self._skinexitMenu(program)            

        if resp == 0:
            ADDON.setSetting('day','0')
            self._showHourMenu('Today %s' % (now), program) 
        if resp == 1:
            ADDON.setSetting('day','1')
            self._showHourMenu(one, program)
        if resp == 2:
            ADDON.setSetting('day','2')
            self._showHourMenu(two, program)

    def _showHourMenu(self, title, program):
        Times = []
        today = datetime.datetime.today().strftime(" %d %B ")
        for i in range(00, 24):
            if title == 'Today %s' %(today):
                now = int(time.strftime("%H")) + 2
                if i>now: 
                    if i<10:
                        conv = str('0%s:00') % (i)
                        Times.append(conv)
                    if i>10:
                        conv = str('%s:00') % (i)
                        Times.append(conv)  
            else:              
                if i<10:
                    conv = str('0%s:00') % (i)
                    Times.append(conv)
                if i>10:
                    conv = str('%s:00') % (i)
                    Times.append(conv)

        resp = utils.dialog.select('[COLOR fffea800]%s[/COLOR]' % title, Times) 
        now = datetime.datetime.now()
        if resp <0:
            self._showSchMenu(program)
        else:
            selected = Times[resp]
            selected = re.sub(r':00', '', selected)
            self.viewStartDate = now.replace(hour=int(selected), minute=0, second=0, microsecond=0) + datetime.timedelta(days=int(ADDON.getSetting('day')))
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)

    def _showToolsMenu(self, program):

        if xbmc.getCondVisibility('system.platform.android'):
            from resources import xbmccodecs

            resp = utils.dialog.select('[COLOR fffea800]iVue Tools[/COLOR]', ['iVue Creator', 'View Kodi Log', 'Purge Database', 'Soft Reset', 'Hard Reset', xbmccodecs.media, xbmccodecs.surfacemedia]) 
        else:
            resp = utils.dialog.select('[COLOR fffea800]iVue Tools[/COLOR]', ['iVue Creator', 'View Kodi Log', 'Purge Database', 'Soft Reset', 'Hard Reset'])

        if resp <0:
            self._skinexitMenu(program)            
        if resp == 0:
			    xbmc.executebuiltin('RunAddon(plugin.video.IVUEcreator)')        
        if resp == 1:
			    import log_viewer  
        if resp == 2:
            self.close()
            reset.purgeDB()
        if resp == 3:
            self.close()
            reset.SoftReset()
        if resp == 4:
            self.close()
            reset.HardReset()
        if resp == 5:
            xbmccodecs.setCodec()
            self.close()
        if resp == 6:
            xbmccodecs.setSurfaceCodec()
            self.close()

    def _showCatMenu(self):
        self._hideControl(self.C_MAIN_MOUSE_CONTROLS)
        d = CatMenu(self.database, self.category, self.categories)
        d.doModal()
        buttonClicked = d.buttonClicked
        self.category = d.category
        ADDON.setSetting('category',self.category)
        self.setControlLabel(self.C_MAIN_CAT_LABEL, '[B]%s[/B]' % self.category)
        self.database.setCategory(self.category)
        self.categories = d.categories 
        del d

        if buttonClicked == CatMenu.C_CAT_CATEGORY:

            control = self.getControl(self.C_MAIN_EPG_VIEW_MARKER)
            if control:
                (left, top) = control.getPosition()
                self.focusPoint.y = top
            else:
                self.focusPoint.y = 0
            self.onRedrawEPG(0, self.viewStartDate)

        elif buttonClicked == CatMenu.C_CAT_QUIT:
            self.close()

        else:
            control = self.getControl(self.C_MAIN_EPG_VIEW_MARKER)
            if control:
                (left, top) = control.getPosition()
                self.focusPoint.y = top
            else:
                self.focusPoint.y = 0
            self.onRedrawEPG(0, self.viewStartDate)

    def programSearch(self):
        action = utils.dialog.select("iVue Search", ['Search by program', 'Search by channel'])
        if action == -1:
            return
        if action == 0:
            self.searchProg()
        if action == 1:
            self.searchChan()


    def searchProg(self, search=None):

        title = '?'
        try:
            controlInFocus = self.getFocus()
            if controlInFocus:
                program = self._getProgramFromControl(controlInFocus)
                if program:
                    title = program.title
        except:
            title = ''
        file_name = "special://profile/addon_data/script.ivueguide/title_search.list"
        f = utils.xbmcvfs.File(file_name,"rb")
        searches = sorted(f.read().splitlines())
        f.close()
        actions = ["New Search", "Remove Search"] + searches
        action = utils.dialog.select("Program Search: %s" % title, actions)
        if action == -1:
            return
        elif action == 0:
            pass
        elif action == 1:
            which = utils.dialog.select("Remove Search",searches)
            if which == -1:
                return
            else:
                del searches[which]
                f = utils.xbmcvfs.File(file_name,"wb")
                f.write('\n'.join(searches))
                f.close()
                return
        else:
            title = searches[action-2]
        search = utils.dialog.input("Program Search",title)
        if not search:
            return
        searches = list(set([search] + searches))
        f = utils.xbmcvfs.File(file_name,"wb")
        f.write('\n'.join(searches))
        f.close()
        programList = self.database.programSearch(search)
        title = "Search"
        d = ProgramListDialog(title, programList, True)
        d.doModal()
        index = d.index
        action = d.action
        buttonClicked = d.buttonClicked
        if buttonClicked == 1003:
            self.programSearch()
        elif buttonClicked == 1004:
            self.close()
        elif buttonClicked == 1005:
            self._infoMenu()
        elif buttonClicked == 1006:
            self.getReminders()
        elif action == KEY_CONTEXT_MENU:
            if index > -1:
                self.set_removeReminders(programList[index])
                self.programSearch()
        else:
            if index > -1:
                self.play(programList[index])


    def searchChan(self, search=None):
        channel = ''
        chanList = self.database.getChannelList()
        actions = []
        for chan in chanList:
            actions.append(chan.title)
        action = utils.dialog.select("Channel Search", actions)
        if action == -1:
            return
        else:
            channel = actions[action]

        programList = self.database.searchChannel(channel)
        title = "Search"
        d = ProgramListDialog(title, programList, True)
        d.doModal()
        index = d.index
        action = d.action
        buttonClicked = d.buttonClicked
        if buttonClicked == 1003:
            self.programSearch()
        elif buttonClicked == 1004:
            self.close()
        elif buttonClicked == 1005:
            self._infoMenu()
        elif buttonClicked == 1006:
            self.getReminders()
        elif action == KEY_CONTEXT_MENU:
            if index > -1:
                self.set_removeReminders(programList[index])
                self.programSearch()
        else:
            if index > -1:
                self.play(programList[index])

    def getReminders(self):
        programList = self.database.showReminders(5)
        title = "Planner"
        d = ProgramListDialog(title,programList, True)
        d.doModal()
        index = d.index
        action = d.action
        buttonClicked = d.buttonClicked
        if buttonClicked == 1003:
            self.programSearch()
        elif buttonClicked == 1004:
            self.close()
        elif buttonClicked == 1005:
            self._infoMenu()
        elif buttonClicked == 1006:
            yes=utils.dialog.yesno("iVue Planner", 'You are about to delete all saved programs', 'Are you sure?', nolabel='No', yeslabel='Yes');
            if yes:	
                self.database.clearAllNotifications()
                self.onRedrawEPG(self.channelIdx, self.viewStartDate)
                utils.dialog.ok("Planner Cleared", 'Your planner has been wiped Clean', '', '')
            else: 
                self.getReminders()
        elif action == KEY_CONTEXT_MENU:
            if index > -1:
                self.set_removeReminders(programList[index])
                self.getReminders()
        else:
            if index > -1:
                self.play(programList[index])


    def osdEpg(self, category):
        if category == '':
            category = 'All Channels'        
        d = osdOnNowDialog(self.database, category)
        d.doModal()
        index = d.index
        action = d.action
        channel = d.channel
        cat = d.cat
        if action == KEY_CONTEXT_MENU:
            if index > -1:
                self._showContextMenu(channel[index])
        else:
            if index > -1:
                self.osdCategory = cat
                program = channel[index]
                self.play(program)


    def setFocusId(self, controlId):
        control = self.getControl(controlId)
        if control:
            self.setFocus(control)

    def setFocus(self, control):
        debug('setFocus %d' % control.getId())
        if control in [elem.control for elem in self.controlAndProgramList]:
            debug('Focus before %s' % self.focusPoint)
            (left, top) = control.getPosition()
            if left > self.focusPoint.x or left + control.getWidth() < self.focusPoint.x:
                self.focusPoint.x = left
            self.focusPoint.y = top + (control.getHeight() / 2)
            debug('New focus at %s' % self.focusPoint)

        super(TVGuide, self).setFocus(control)

    def streamAddon(self, program):
        thumb = ICON
        title = 'No add-on\nLinked to %s' % program.channel.title
        if program.channel.streamUrl is not None:
            if str(program.channel.streamUrl).startswith('plugin://'):
                linked= str(program.channel.streamUrl).split('://')[1].split('/')[0]
                thumb = xbmcaddon.Addon(linked).getAddonInfo('icon')
                title = xbmcaddon.Addon(linked).getAddonInfo('name') + '\nLinked to %s' % program.channel.title
            elif str(program.channel.streamUrl).startswith('pvr://'):
                thumb = os.path.join(RESOURCES, 'png', 'pvr.png')
                title = 'PVR Playlist\nLinked to %s' % program.channel.title
        addonInfo = [thumb, title]
        return addonInfo


    def onFocus(self, controlId):
        try:
            controlInFocus = self.getControl(controlId)
        except Exception:
            return
        duration_str = ""

        program = self._getProgramFromControl(controlInFocus)
        if program is None:
            return

        self.setControlLabel(self.C_MAIN_TITLE, '[B]%s[/B]' % program.title.replace(' (?)', '').replace('&amp;','&'))
        progresspercent = self.getControl(self.C_MAIN_PROGRESS)
        if program.startDate or program.endDate:
            self.setControlLabel(self.C_MAIN_TIME,
                                 '[B]%s - %s[/B]' % (self.formatTime(program.startDate), self.formatTime(program.endDate)))

            if program.endDate - (datetime.datetime.now() - program.startDate) > program.startDate and program.startDate < datetime.datetime.now() :

                remaining = int(timedelta_total_seconds(program.endDate - datetime.datetime.now()) / 60 + 1)
                self.setControlLabel(self.C_MAIN_DURATION,  '%s mins left' % remaining)
                #if progresspercent:
                progress = utils.percent(program.startDate,program.endDate)
                progresspercent.setPercent(progress)

            else:
                progresspercent.setPercent(0)
                self.setControlLabel(self.C_MAIN_DURATION, '  ')
        else:
            self.setControlLabel(self.C_MAIN_TIME, '')


        if program.description:
            description = program.description.replace('&amp;','&')
        else:
            description = 'Sorry there is no program information available at the moment'
        if ADDON.getSetting('skin.colours')=='true' and os.path.exists(SKINCOLOURS):

            with open(SKINCOLOURS ,'rb') as file:
                lines = file.read().splitlines()

                file.close()
                for line in lines:
                    if 'program_description' in line:
                        color = line.strip().split(' = ')[1]
        else:
            color = utils.remove_formatting(ADDON.getSetting('description.color'))
        self.setControlText(self.C_MAIN_DESCRIPTION,'[COLOR %s]%s[/COLOR]' %(color, description))

        if program.channel.logo is not None:
            self.setControlImage(self.C_MAIN_LOGO, program.channel.logo)
        else:
            self.setControlImage(self.C_MAIN_LOGO, '')

        try:
            self.setControlLabel(self.C_MAIN_CHANTITLE, '[B]%s[/B]' %program.channel.title)
        except:
            pass

        if program.imageSmall is not None:
            if not program.imageSmall == '':
                self.setControlImage(self.C_MAIN_IMAGE, program.imageSmall)
            else:
                self.setControlImage(self.C_MAIN_IMAGE, 'tvguide-logo-epg.png')
        else:
            self.setControlImage(self.C_MAIN_IMAGE, 'tvguide-logo-epg.png')

        if ADDON.getSetting('linked.addon') == 'true' and ADDON.getSetting('ignore.stream') == 'false':
            checkStream = self.streamAddon(program)
            self.setControlImage(C_MAIN_PLUGIN_ICON, checkStream[0])
            self.setControlLabel(C_MAIN_PLUGIN_NAME, checkStream[1])
        else: 
            self._showControl(C_MAIN_PLUGIN_NAME)
            self._showControl(C_MAIN_PLUGIN_ICON)
        if not self.osdEnabled and self.player.isPlaying():
            self.player.stop()

    def _left(self, currentFocus):
        control = self._findControlOnLeft(currentFocus)
        if control is not None:
            self.setFocus(control)
        elif control is None:
            self.viewStartDate -= datetime.timedelta(hours=2)
            self.focusPoint.x = self.epgView.right
            self.onRedrawEPG(self.channelIdx, self.viewStartDate, focusFunction=self._findControlOnLeft)

    def _right(self, currentFocus):
        control = self._findControlOnRight(currentFocus)
        if control is not None:
            self.setFocus(control)
        elif control is None:
            self.viewStartDate += datetime.timedelta(hours=2)
            self.focusPoint.x = self.epgView.left
            self.onRedrawEPG(self.channelIdx, self.viewStartDate, focusFunction=self._findControlOnRight)

    def _up(self, currentFocus):
        currentFocus.x = self.focusPoint.x
        control = self._findControlAbove(currentFocus)
        if control is not None:
            self.setFocus(control)
        elif control is None:
            self.focusPoint.y = self.epgView.bottom
            self.onRedrawEPG(self.channelIdx - CHANNELS_PER_PAGE,
                             self.viewStartDate,
                             focusFunction=self._findControlAbove)

    def _down(self, currentFocus):
        currentFocus.x = self.focusPoint.x
        control = self._findControlBelow(currentFocus)
        if control is not None:
            self.setFocus(control)
        elif control is None:
            self.focusPoint.y = self.epgView.top
            self.onRedrawEPG(self.channelIdx + CHANNELS_PER_PAGE,
                             self.viewStartDate,
                             focusFunction=self._findControlBelow)

    def _nextDay(self):
        self.viewStartDate += datetime.timedelta(days=1)
        self.onRedrawEPG(self.channelIdx, self.viewStartDate)

    def _previousDay(self):
        self.viewStartDate -= datetime.timedelta(days=1)
        self.onRedrawEPG(self.channelIdx, self.viewStartDate)

    def _moveUp(self, count=1, scrollEvent=False):
        if scrollEvent:
            self.onRedrawEPG(self.channelIdx - count, self.viewStartDate)
        else:
            self.focusPoint.y = self.epgView.bottom
            self.onRedrawEPG(self.channelIdx - count, self.viewStartDate, focusFunction=self._findControlAbove)

    def _moveDown(self, count=1, scrollEvent=False):
        if scrollEvent:
            self.onRedrawEPG(self.channelIdx + count, self.viewStartDate)
        else:
            self.focusPoint.y = self.epgView.top
            self.onRedrawEPG(self.channelIdx + count, self.viewStartDate, focusFunction=self._findControlBelow)

    def _channelUp(self):
        channel = self.database.getNextChannel(self.currentChannel)
        program = self.database.getCurrentProgram(channel)
        self.playChannel(channel, program)

    def _channelDown(self):
        channel = self.database.getPreviousChannel(self.currentChannel)
        program = self.database.getCurrentProgram(channel)
        self.playChannel(channel, program)

    def playChannel(self, channel, program=None):
        if self.currentChannel:
            if self.lastPlayed:
                if not channel == self.currentChannel:
                    self.lastPlayed = self.currentChannel
            else:
                self.lastPlayed = self.currentChannel
        self.currentChannel = channel
        url = self.database.getStreamUrl(channel)
        if url:
            stream = str(url).split('plugin://')[1].split('/')[0]
            self.set_playing()
           # pvr

            if config.radio(stream, url) == False:
                return
		    
            
            if url.isdigit():
                command = \
                    '{"jsonrpc": "2.0", "id":"1", "method": "Player.Open","params":{"item":{"channelid":%s}}}' \
                    % url
                xbmc.executeJSONRPC(command)
                return

            if url[0:9] == 'plugin://':
                if self.alternativePlayback:
                    xbmc.executebuiltin('XBMC.RunPlugin(%s)' % url)
                elif self.osdEnabled:
                    self.player.play(item=url, windowed=True)
                else:
                    xbmc.executebuiltin('PlayMedia(%s)' % url)
            else:
                self.player.play(item=url, windowed=True)

            self._hideEpg()

            threading.Timer(1, self.waitForPlayBackStopped).start()
    
        self.osdProgram = self.database.getCurrentProgram(self.currentChannel)
        return url is not None

    def waitForPlayBackStopped(self):
        time.sleep(0.5)

        self._showOsd()
        self.osdActive = False

        countdown = int(ADDON.getSetting('osd.timer'))
        while countdown:
            time.sleep(1)
            countdown = countdown - 1
        if self.player.isPlaying():
            if self.mode == MODE_OSD and not self.osdActive:
                self._hideOsd()
            return

        if not self.osdActive:
            self._hideOsd()
        self.onPlayBackStopped()

    def _showOsd(self):
        if not ADDON.getSetting('osd.epg') == 'true':
            return

        if self.mode != MODE_OSD:
            self.osdChannel = self.currentChannel
        progresspercent = self.getControl(self.C_MAIN_OSD_PROGRESS)
        if self.osdProgram is not None:

            if self.osdProgram.startDate or self.osdProgram.endDate:
                self.setControlLabel(self.C_MAIN_OSD_TIME, '[B]%s[/B]' % (
                    self.formatTime(self.osdProgram.startDate)))

                if self.osdProgram.endDate - (datetime.datetime.now() - self.osdProgram.startDate) > self.osdProgram.startDate and self.osdProgram.startDate < datetime.datetime.now() :
                    try:
                        self.setControlImage(self.C_MAIN_OSD_NOW, 'now.png')
                        self.setControlImage(self.C_MAIN_OSD_NEXT, 'next.png')
                    except:
                        pass

                    remaining = int(timedelta_total_seconds(self.osdProgram.endDate - datetime.datetime.now()) / 60 + 1)
                    self.setControlLabel(self.C_MAIN_OSD_DURATION,  '%s mins left' % remaining)
                    if progresspercent:
                        progress = utils.percent(self.osdProgram.startDate,self.osdProgram.endDate)
                        progresspercent.setPercent(progress)

                else:
                    try:
                        self.setControlImage(self.C_MAIN_OSD_NOW, ' ')
                        self.setControlImage(self.C_MAIN_OSD_NEXT, ' ')
                    except:
                        pass
                    progresspercent.setPercent(0)
                    self.setControlLabel(self.C_MAIN_OSD_DURATION, '  ')

            else:
                self.setControlLabel(self.C_MAIN_OSD_TIME, '')
            self.setControlLabel(self.C_MAIN_OSD_TITLE, '[B]%s[/B]' % self.osdProgram.title.replace(' (?)', '').replace('&amp;','&'))
            self.setControlText(self.C_MAIN_OSD_DESCRIPTION, self.osdProgram.description.replace('&amp;','&'))
            self.setControlLabel(self.C_MAIN_OSD_CHANNEL_TITLE, '[B]%s[/B]' %self.osdChannel.title)
            if self.osdProgram.channel.logo is not None:
                self.setControlImage(self.C_MAIN_OSD_CHANNEL_LOGO, self.osdProgram.channel.logo)
            else:
                self.setControlImage(self.C_MAIN_OSD_CHANNEL_LOGO, '')

            if ADDON.getSetting('linked.addon') == 'true' and ADDON.getSetting('ignore.stream') == 'false':
                checkStream = self.streamAddon(self.osdProgram)
                self.setControlImage(C_MAIN_OSD_PLUGIN_ICON, checkStream[0])
                self.setControlLabel(C_MAIN_OSD_PLUGIN_NAME, checkStream[1])
            else: 
                self._showControl(C_MAIN_OSD_PLUGIN_NAME)
                self._showControl(C_MAIN_OSD_PLUGIN_ICON)

            try:
                if self.osdProgram.imageSmall is not None:
                    if not self.osdProgram.imageSmall == '':
                        self.setControlImage(self.C_MAIN_OSD_PROGIMAGE, self.osdProgram.imageSmall)
                    else:
                        self.setControlImage(self.C_MAIN_OSD_PROGIMAGE, 'tvguide-logo-epg.png')
                else:
                    self.setControlImage(self.C_MAIN_OSD_PROGIMAGE, 'tvguide-logo-epg.png')
            except:
                pass

        prevOsdProgram = self.database.getPreviousProgram(self.osdProgram)
        if prevOsdProgram:
            self.setControlLabel(self.C_PREV_OSD_TITLE, '[B]%s[/B]' % prevOsdProgram.title.replace(' (?)', '').replace('&amp;','&'))
            if prevOsdProgram.startDate or prevOsdProgram.endDate:
                self.setControlLabel(self.C_PREV_OSD_TIME, '[B]%s[/B]' % (
                    self.formatTime(prevOsdProgram.startDate)))
            else:
                self.setControlLabel(self.C_PREV_OSD_TIME, '')

        nextOsdProgram = self.database.getNextProgram(self.osdProgram)
        if nextOsdProgram:
            self.setControlLabel(self.C_NEXT_OSD_TITLE, '[B]%s[/B]' % nextOsdProgram.title.replace(' (?)', '').replace('&amp;','&'))
            if nextOsdProgram.startDate or nextOsdProgram.endDate:
                self.setControlLabel(self.C_NEXT_OSD_TIME, '[B]%s[/B]' % (
                    self.formatTime(nextOsdProgram.startDate)))
            else:
                self.setControlLabel(self.C_NEXT_OSD_TIME, '')

            try:
                if nextOsdProgram.imageSmall is not None:
                    if not nextOsdProgram.imageSmall == '':
                        self.setControlImage(self.C_MAIN_OSD_NEXTIMAGE, nextOsdProgram.imageSmall)
                    else:
                        self.setControlImage(self.C_MAIN_OSD_NEXTIMAGE, 'tvguide-logo-epg.png')
                else:
                    self.setControlImage(self.C_MAIN_OSD_NEXTIMAGE, 'tvguide-logo-epg.png')
            except:
                pass

            try:
                control = self.getControl(self.C_MAIN_OSD_NEXTDESC)
                if control:
                    self.setControlText(self.C_MAIN_OSD_NEXTDESC, nextOsdProgram.description.replace('&amp;','&'))
            except:
                pass

        self.mode = MODE_OSD
        self._showControl(self.C_MAIN_OSD)

    def _hideOsd(self):
        self.mode = MODE_TV
        self._hideControl(self.C_MAIN_OSD)

    def _hideEpg(self):
        self._hideControl(self.C_MAIN_EPG)
        self.mode = MODE_TV
        self._clearEpg()

    def onRedrawEPG(self, channelStart, startTime, focusFunction=None):
        if self.redrawingEPG or (self.database is not None and self.database.updateInProgress) or self.isClosing:
            debug('onRedrawEPG - already redrawing')
            return   # ignore redraw request while redrawing
        debug('onRedrawEPG')

        self.redrawingEPG = True
        self.mode = MODE_EPG
        self._showControl(self.C_MAIN_EPG)
        self.updateTimebar(scheduleTimer=False)

        # show Loading screen

        self.setControlLabel(self.C_MAIN_LOADING_TIME_LEFT,
                             strings(CALCULATING_REMAINING_TIME))
        self._showControl(self.C_MAIN_LOADING)
        self.setFocusId(self.C_MAIN_LOADING_CANCEL)

        # remove existing controls

        self._clearEpg()

        try:
            self.channelIdx, channels, programs = self.database.getEPGView(channelStart, startTime, self.onSourceProgressUpdate, clearExistingProgramList=False, category=self.category)
        except src.SourceException:
            self.onEPGLoadError()
            return

        channelsWithoutPrograms = list(channels)

        # date and time row
        self.setControlLabel(self.C_MAIN_DATE, utils.formatDate(self.viewStartDate, False, False))
        self.setControlLabel(self.C_MAIN_DATE_LONG, utils.formatDate(self.viewStartDate, True, False))
        for col in range(1, 5):
            self.setControlLabel(4000 + col, self.formatTime(startTime))
            try:
                timeFormat = self.formatTime(startTime).replace(':','')
                try:
                    timesplit = timeFormat.split(' ')[1]
                except:
                    timesplit = timeFormat
                if 'PM' in timesplit:
                    timeOld = timeFormat.replace(' PM','').replace('1200','0000').replace('1230','0030')
                    timeFormat = int(timeOld)
                    timeFormat += 1200
                else:
                    if 'AM' in timesplit:
                        timeFormat = timeFormat.replace(' AM','').replace('1200','0000').replace('1230','0030')
                self.setControlImage(40000 + col, xbmc.translatePath(os.path.join(PROFILE, 'resources', 'skins', SKIN, 'media', 'times', str(timeFormat)+'.png')))
            except:
                pass
            startTime += HALF_HOUR

        if programs is None:
            self.onEPGLoadError()
            return

        showLogo = ADDON.getSetting('logos.enabled') == 'true'
        for idx in range(0, CHANNELS_PER_PAGE):
            if idx >= len(channels):
                self.setControlImage(4110 + idx, ' ')
                self.setControlLabel(4010 + idx, ' ')
                self.setControlLabel(40100 + idx, ' ')
            else:
                channelStart += 1
                channel = channels[idx]

                try:
                    chanList = self.database.getChannelList()
                    chanidx = chanList.index(channel)
                    chanidx += 1
                except:
                    chanidx = ''

                if ADDON.getSetting('skin.colours')=='true' and os.path.exists(SKINCOLOURS):
                    with open(SKINCOLOURS ,'rb') as file:
                        lines = file.read().splitlines()

                        file.close()
                        for line in lines:
                            if 'channels' in line:
                                color = line.strip().split(' = ')[1]
                else:
                    color = utils.remove_formatting(ADDON.getSetting('channel.color'))

                if ADDON.getSetting('channel.num')=='true' and chanidx !='':
                    self.setControlLabel(4010 + idx, '[COLOR %s]%s[/COLOR]' % (color, channel.title))
                    try:
                        chanNum = self.getControl(40100 + idx)
                        if xbmc.getCondVisibility( "Control.IsVisible(%s)" % str(40100 + idx) ):
                            self.setControlLabel(40100 + idx, '[COLOR %s]%s[/COLOR]' % (color, chanidx))
                            self.setControlLabel(4010 + idx, '[COLOR %s]%s[/COLOR]' % (color, channel.title))
                        else:
                            self.setControlLabel(4010 + idx, '[COLOR %s]%s. %s[/COLOR]' % (color, chanidx,channel.title))
                    except:
                        self.setControlLabel(4010 + idx, '[COLOR %s]%s. %s[/COLOR]' % (color, chanidx,channel.title))
                else:
                    self.setControlLabel(4010 + idx, '[COLOR %s]%s[/COLOR]' % (color, channel.title))

                if channel.logo is not None and showLogo == True:
                    self.setControlImage(4110 + idx, channel.logo)
                else:
                    self.setControlImage(4110 + idx, ' ')

					
        #Jules and Karls changes focus colour here
        if ADDON.getSetting('skin.colours')=='true' and os.path.exists(SKINCOLOURS):

            with open(SKINCOLOURS ,'rb') as file:
                lines = file.read().splitlines()

                file.close()
                for line in lines:
                    if 'program_focus' in line:
                        focusColor = line.strip().split(' = ')[1]
                    if 'program_nofocus' in line:
                        noFocusColor = line.strip().split(' = ')[1]
        else:

            name = utils.remove_formatting(ADDON.getSetting('focus.color'))
            focusColor = colors.color_name[name]

            name = utils.remove_formatting(ADDON.getSetting('nofocus.color'))
            noFocusColor = colors.color_name[name]

        if ADDON.getSetting('font') == 'Enabled': 		
            fontSize = 'font30'
        else: 		
            fontSize = 'font13'
        for program in programs:
            idx = channels.index(program.channel)
            if program.channel in channelsWithoutPrograms:
                channelsWithoutPrograms.remove(program.channel)

            startDelta = program.startDate - self.viewStartDate
            stopDelta = program.endDate - self.viewStartDate

            cellStart = self._secondsToXposition(startDelta.seconds)
            if startDelta.days < 0:
                cellStart = self.epgView.left
            cellWidth = self._secondsToXposition(stopDelta.seconds) - cellStart
            if cellStart + cellWidth > self.epgView.right:
                cellWidth = self.epgView.right - cellStart

            if cellWidth > 1:
                if program.notificationScheduled:
                    noFocusTexture = 'tvguide-program-red.png'
                    focusTexture = 'tvguide-program-red-focus.png'

                elif os.path.exists(os.path.join(PROFILE, 'resources', 'skins', SKIN, 'media', 'tvguide-program-now.png')) and program.startDate < datetime.datetime.today() and program.endDate > datetime.datetime.today():
                    noFocusTexture = 'tvguide-program-now.png'
                    focusTexture = 'tvguide-program-grey-focus.png'

                elif os.path.exists(os.path.join(PROFILE, 'resources', 'skins', SKIN, 'media', 'tvguide-program-finished.png')) and program.startDate < datetime.datetime.today() and program.endDate < datetime.datetime.today():
                    noFocusTexture = 'tvguide-program-finished.png'
                    focusTexture = 'tvguide-program-grey-focus.png'
                else:
                    noFocusTexture = 'tvguide-program-grey.png'
                    focusTexture = 'tvguide-program-grey-focus.png'

                if cellWidth < 25:
                    title = ''
                else:
                    title = program.title.replace(' (?)', '').replace('&amp;','&')

                control = xbmcgui.ControlButton(
                    cellStart,
                    self.epgView.top + self.epgView.cellHeight * idx,
                    cellWidth - 2,
                    self.epgView.cellHeight - 2,
                    title,
                    font='%s'%fontSize,
                    focusedColor= focusColor,
                    textColor=noFocusColor,					
                    noFocusTexture=noFocusTexture,
                    focusTexture=focusTexture
                )

                self.controlAndProgramList.append(ControlAndProgram(control, program))

        for channel in channelsWithoutPrograms:
            idx = channels.index(channel)

            control = xbmcgui.ControlButton(
                self.epgView.left,
                self.epgView.top + self.epgView.cellHeight * idx,
                (self.epgView.right - self.epgView.left) - 2,
                self.epgView.cellHeight - 2,
                'Sorry there is no information available',
                font='%s'%fontSize,
                focusedColor=focusColor,
                textColor=noFocusColor,				
                noFocusTexture='tvguide-program-grey.png',
                focusTexture='tvguide-program-grey-focus.png'
            )

            program = src.Program(channel,
                                  'Sorry there is no information available', None,
                                  None, None, None)
            self.controlAndProgramList.append(ControlAndProgram(control,
                    program))

        # add program controls

        if focusFunction is None:
            focusFunction = self._findControlAt
        focusControl = focusFunction(self.focusPoint)
        controls = [elem.control for elem in self.controlAndProgramList]
        self.addControls(controls)
        if focusControl is not None:
            debug('onRedrawEPG - setFocus %d' % focusControl.getId())
            self.setFocus(focusControl)

        self.ignoreMissingControlIds.extend([elem.control.getId()
                for elem in self.controlAndProgramList])

        if focusControl is None and len(self.controlAndProgramList) > 0:
            self.setFocus(self.controlAndProgramList[0].control)

        self._hideControl(self.C_MAIN_LOADING)
        self.redrawingEPG = False

    def _clearEpg(self):
        controls = [elem.control for elem in self.controlAndProgramList]
        try:
            self.removeControls(controls)
        except RuntimeError:
            for elem in self.controlAndProgramList:
                try:
                    self.removeControl(elem.control)
                except RuntimeError:
                    pass  # happens if we try to remove a control that doesn't exist
        del self.controlAndProgramList[:]

    def onEPGLoadError(self):
        self.redrawingEPG = False
        self._hideControl(self.C_MAIN_LOADING)
        utils.dialog.ok(strings(LOAD_ERROR_TITLE),
                            strings(LOAD_ERROR_LINE1),
                            strings(LOAD_ERROR_LINE2))
        self.close()

    def onSourceNotConfigured(self):
        self.redrawingEPG = False
        self._hideControl(self.C_MAIN_LOADING)
        utils.dialog.ok(strings(LOAD_ERROR_TITLE),
                            strings(LOAD_ERROR_LINE1),
                            strings(CONFIGURATION_ERROR_LINE2))
        self.close()

    def isSourceInitializationCancelled(self):
        return xbmc.abortRequested or self.isClosing

    def onSourceInitialized(self, success):
        if success:
            self.notification = Notification(self.database,
                    ADDON.getAddonInfo('path'))
            self.onRedrawEPG(0, self.viewStartDate)
            self.database.getChannelINI()
            self.database.channelSetup()

    def onSourceProgressUpdate(self, percentageComplete):
        control = self.getControl(self.C_MAIN_LOADING_PROGRESS)
        if percentageComplete < 1:
            if control:
                control.setPercent(1)
            self.progressStartTime = datetime.datetime.now()
            self.progressPreviousPercentage = percentageComplete
        elif percentageComplete != self.progressPreviousPercentage:
            if control:
                control.setPercent(percentageComplete)
            self.progressPreviousPercentage = percentageComplete
            delta = datetime.datetime.now() - self.progressStartTime

            if percentageComplete < 20:
                self.setControlLabel(self.C_MAIN_LOADING_TIME_LEFT,
                        strings(CALCULATING_REMAINING_TIME))
            else:
                secondsLeft = int(delta.seconds) \
                    / float(percentageComplete) * (100.0
                        - percentageComplete)
                if secondsLeft > 30:
                    secondsLeft -= secondsLeft % 10
                self.setControlLabel(self.C_MAIN_LOADING_TIME_LEFT,
                        strings(TIME_LEFT) % secondsLeft)

        return not xbmc.abortRequested and not self.isClosing

    def focus_lastchan(self):
        f = open(self.lastchan_file, 'r')
        chan_data = {}
        data = f.read()
        if len(data) > 0:
            chan_data = json.loads(data)
        f.close()

        if 'idx' in chan_data:
            self.channelIdx = chan_data['idx']

        if 'posy' in chan_data:
            self.focusPoint.y = chan_data['posy']

        self.viewStartDate = datetime.datetime.now()
        self.viewStartDate -= \
            datetime.timedelta(minutes=self.viewStartDate.minute % 30,
                               seconds=self.viewStartDate.second)
        self.onRedrawEPG(self.channelIdx, self.viewStartDate)
        self.updateTimebar(scheduleTimer=True)

    def set_playing(self):
        f = open(self.lastchan_file, 'w+')
        chan = {'posy': self.focusPoint.y, 'idx': self.channelIdx}
        f.write(json.dumps(chan))
        f.close()

    def onPlayBackStopped(self):
        if not self.player.isPlaying() and not self.isClosing:
            self._hideControl(self.C_MAIN_OSD)
            self.focus_lastchan()

    def _secondsToXposition(self, seconds):
        return self.epgView.left + seconds * self.epgView.width / 7200

    def _findControlOnRight(self, point):
        distanceToNearest = 10000
        nearestControl = None

        for elem in self.controlAndProgramList:
            control = elem.control
            (left, top) = control.getPosition()
            x = left + control.getWidth() / 2
            y = top + control.getHeight() / 2

            if point.x < x and point.y == y:
                distance = abs(point.x - x)
                if distance < distanceToNearest:
                    distanceToNearest = distance
                    nearestControl = control

        return nearestControl

    def _findControlOnLeft(self, point):
        distanceToNearest = 10000
        nearestControl = None

        for elem in self.controlAndProgramList:
            control = elem.control
            (left, top) = control.getPosition()
            x = left + control.getWidth() / 2
            y = top + control.getHeight() / 2

            if point.x > x and point.y == y:
                distance = abs(point.x - x)
                if distance < distanceToNearest:
                    distanceToNearest = distance
                    nearestControl = control

        return nearestControl

    def _findControlBelow(self, point):
        nearestControl = None

        for elem in self.controlAndProgramList:
            control = elem.control
            (leftEdge, top) = control.getPosition()
            y = top + control.getHeight() / 2

            if point.y < y:
                rightEdge = leftEdge + control.getWidth()
                if leftEdge <= point.x < rightEdge and (nearestControl
                        is None or nearestControl.getPosition()[1]
                        > top):
                    nearestControl = control

        return nearestControl

    def _findControlAbove(self, point):
        nearestControl = None
        for elem in self.controlAndProgramList:
            control = elem.control
            (leftEdge, top) = control.getPosition()
            y = top + control.getHeight() / 2

            if point.y > y:
                rightEdge = leftEdge + control.getWidth()
                if leftEdge <= point.x < rightEdge and (nearestControl
                        is None or nearestControl.getPosition()[1]
                        < top):
                    nearestControl = control

        return nearestControl

    def _findControlAt(self, point):
        for elem in self.controlAndProgramList:
            control = elem.control
            (left, top) = control.getPosition()
            bottom = top + control.getHeight()
            right = left + control.getWidth()

            if left <= point.x <= right and top <= point.y <= bottom:
                return control

        return None

    def _getProgramFromControl(self, control):
        for elem in self.controlAndProgramList:
            if elem.control == control:
                return elem.program
        return None

    def _hideControl(self, *controlIds):
        """
........Visibility is inverted in skin
........"""

        for controlId in controlIds:
            control = self.getControl(controlId)
            if control:
                control.setVisible(True)

    def _showControl(self, *controlIds):
        """
........Visibility is inverted in skin
........"""

        for controlId in controlIds:
            control = self.getControl(controlId)
            if control:
                control.setVisible(False)

    def formatTime(self, timestamp, converthour=None):
        if timestamp:
            format = xbmc.getRegion('time').replace(':%S', ''
                    ).replace('%H%H', '%H')
            return timestamp.strftime(format)
        else:
            return ''

    def setControlImage(self, controlId, image):
        control = self.getControl(controlId)
        if control:
            control.setImage(image.encode('utf-8'))

    def setControlLabel(self, controlId, label):
        control = self.getControl(controlId)
        if control and label:
            control.setLabel(label)

    def setControlText(self, controlId, text):
        control = self.getControl(controlId)
        if control:
            control.setText(text)

    def updateTimebar(self, scheduleTimer=True):

        # move timebar to current time

        timeDelta = datetime.datetime.today() - self.viewStartDate
        control = self.getControl(self.C_MAIN_TIMEBAR)
        if control:
            (x, y) = control.getPosition()
            try:

                # Sometimes raises:
                # exceptions.RuntimeError: Unknown exception thrown from the call "setVisible"

                control.setVisible(timeDelta.days == 0)
            except:
                pass
            control.setPosition(self._secondsToXposition(timeDelta.seconds),
                                y)

        if not self.player.isPlaying() and timeDelta.seconds > 1800 and timeDelta.seconds < 7200:
            self.viewStartDate = datetime.datetime.today()
            self.viewStartDate -= \
                datetime.timedelta(minutes=self.viewStartDate.minute % 30,
                                   seconds=self.viewStartDate.second)
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)
            self.updateTimebar(scheduleTimer=True)

        elif scheduleTimer and not xbmc.abortRequested \
            and not self.isClosing:
            threading.Timer(1, self.updateTimebar).start()

class PopupMenu(xbmcgui.WindowXMLDialog):

    C_POPUP_CHOOSE_STREAM = 4001
    C_POPUP_REMIND = 4002
    C_POPUP_CHANNELS = 4003
    C_POPUP_QUIT = 4004
    C_POPUP_PLAY_BEGINNING = 4005
    C_POPUP_CHANNEL_LOGO = 4100
    C_POPUP_CHANNEL_TITLE = 4101
    C_POPUP_PROGRAM_TITLE = 4102
    C_POPUP_PROGRAM_DESC = 4103
    C_POPUP_PROGRAM_IMAGE = 4104
    C_POPUP_ADDON_SELECT = 30009
    C_POPUP_ADDON_IMAGE_iVue = 'special://home/addons/script.ivueguide/resources/png/shortcut.png'


    settings = utils.xbmcvfs.File('special://home/addons/script.ivueguide/resources/settings.xml','rb').read()
    data = utils.xbmcvfs.File('special://profile/favourites.xml','rb').read()
    matches = re.findall(r'<favourite.*?name="(.*?)".*?>(.*?)<',data,flags=(re.DOTALL | re.MULTILINE))
    favourites = {}
    for name,value in matches:
        name = utils.remove_formatting(name)
        value = re.sub('&quot;','',value)
        favourites[name] = utils.unescape(value)
    names = sorted(favourites)
    actions = ["[COLOR red]Reset current shortcut[/COLOR]","[COLOR yellow]iVue default shortcuts[/COLOR]"] + names

    def __new__(
        cls,
        database,
        program,
        showRemind,
        ):

        # Skin in resources
        # return super(PopupMenu, cls).__new__(cls, 'script-tvguide-menu.xml', SKINFOLDER, SKIN)
        # Skin in user settings

        return super(PopupMenu, cls).__new__(cls,
                'script-tvguide-menu.xml', SKINFOLDER, SKIN)

    def __init__(
        self,
        database,
        program,
        showRemind,
        ):
        """

........@type database: source.Database
........@param program:
........@type program: source.Program
........@param showRemind:
........"""

        super(PopupMenu, self).__init__()
        self.database = database
        self.program = program
        self.showRemind = showRemind
        self.buttonClicked = None
        self.action = None

    def onInit(self):
        remindControl = self.getControl(self.C_POPUP_REMIND)
        channelLogoControl = self.getControl(self.C_POPUP_CHANNEL_LOGO)
        channelTitleControl = self.getControl(self.C_POPUP_CHANNEL_TITLE)
        programTitleControl = self.getControl(self.C_POPUP_PROGRAM_TITLE)

        if self.database.getCustomStreamUrl(self.program.channel):
            chooseStrmControl = \
                self.getControl(self.C_POPUP_CHOOSE_STREAM)
            chooseStrmControl.setLabel(strings(REMOVE_STRM_FILE))

        if self.program.channel.logo is not None:
            channelLogoControl.setImage(self.program.channel.logo)
            channelTitleControl.setVisible(False)
        else:
            channelTitleControl.setLabel(self.program.channel.title)
            channelLogoControl.setVisible(False)
        try:
            decControl = self.getControl(self.C_POPUP_PROGRAM_DESC)
            if self.program.description:
                decControl.setText(self.program.description)
            else:
                decControl.setText('Sorry no program information available at the moment')
        except:
            pass

        try:

            picControl = self.getControl(self.C_POPUP_PROGRAM_IMAGE)

            if self.program.imageSmall is not None:
                if not self.program.imageSmall == '':
                    picControl.setImage(self.program.imageSmall)
                else:
                    picControl.setImage('tvguide-logo-epg.png')
            else:
                picControl.setImage('tvguide-logo-epg.png')
        except:
            pass

        programTitleControl.setLabel('[B]%s[/B]' %self.program.title)

        if self.program.startDate:
            remindControl.setEnabled(True)
            if self.showRemind:
                remindControl.setLabel(strings(REMIND_PROGRAM))
            else:
                remindControl.setLabel(strings(DONT_REMIND_PROGRAM))
        else:
            remindControl.setEnabled(False)

        for x in range(1, 11):
            TITLE = 31010 + x
            IMAGE = 32010 + x
            if ADDON.getSetting('CustomAddon%s.label' % x) == '':
                self.getControl(TITLE).setLabel('iVue Shortcut %s' % x)             
            else:
                self.getControl(TITLE).setLabel(ADDON.getSetting('CustomAddon%s.label' % x))

            if ADDON.getSetting('CustomAddon%s.image' % x) == '':
                self.getControl(IMAGE).setImage(self.C_POPUP_ADDON_IMAGE_iVue)             
            else:
                self.getControl(IMAGE).setImage(ADDON.getSetting('CustomAddon%s.image' % x))

    def onAction(self, action):
        if action.getId() in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, KEY_NAV_BACK, KEY_CONTEXT_MENU]:
            self.action = KEY_NAV_BACK
            self.close()
            return

    def onClick(self, controlId):
        if controlId == self.C_POPUP_CHOOSE_STREAM \
            and self.database.getCustomStreamUrl(self.program.channel):
            self.database.deleteCustomStreamUrl(self.program.channel)
            chooseStrmControl = \
                self.getControl(self.C_POPUP_CHOOSE_STREAM)
            chooseStrmControl.setLabel(strings(CHOOSE_STRM_FILE))

        elif controlId == self.C_POPUP_ADDON_SELECT:
            self._editShortcutMenu()

        else:

            self.buttonClicked = controlId
            self.close()

    def _editShortcutMenu(self):
        resp = utils.dialog.select('[COLOR fffea800]iVue Shortcuts Menu[/COLOR]', ['Edit Shortcuts', 'Use Latest iVue Selection'])
        if resp < 0:
            return
        if resp == 0:
            self._showShortcutMenu()
        if resp == 1:
            for x in range(1, 11):
                shortcut = x
                control = utils.addons(shortcut)
                self.default(shortcut, control)


    def _showShortcutMenu(self):
        shortcuts = []
        for x in range(1, 11):
            if  not ADDON.getSetting('CustomAddon%s.label' % x) == '':
                shortcut = ADDON.getSetting('CustomAddon%s.label' % x)
                shortcuts.append(shortcut)
            else:
                shortcut = 'iVue Shortcut %s' % x
                shortcuts.append(shortcut)
        if SKIN == 'sky Vue' or SKIN == 'iVue Default':
            resp = utils.dialog.select('[COLOR fffea800]iVue Shortcuts Menu[/COLOR]', shortcuts[:9])
        elif SKIN == 'iVurgin':
            resp = utils.dialog.select('[COLOR fffea800]iVue Shortcuts Menu[/COLOR]', shortcuts[:5])
        elif SKIN == 'FreeVue Play' or SKIN == 'iVue Classic':
            resp = utils.dialog.select('[COLOR fffea800]iVue Shortcuts Menu[/COLOR]', shortcuts[:4])
        elif SKIN == 'Sky Classic':
            resp = utils.dialog.select('[COLOR fffea800]iVue Shortcuts Menu[/COLOR]', shortcuts[:8])
        else:
            resp = utils.dialog.select('[COLOR fffea800]iVue Shortcuts Menu[/COLOR]', shortcuts)
        if resp < 0:
            return
        if resp == 0:
            self.shortcut(1)
        if resp == 1:
            self.shortcut(2)
        if resp == 2:
            self.shortcut(3)
        if resp == 3:
            self.shortcut(4)  
        if resp == 4:
            self.shortcut(5)
        if resp == 5:
            self.shortcut(6)
        if resp == 6:
            self.shortcut(7)
        if resp == 7:
            self.shortcut(8)
        if resp == 8:
            self.shortcut(9)
        if resp == 9:
            self.shortcut(10)

    def shortcut(self, shortcut):
       TITLE = 31010 + shortcut
       IMAGE = 32010 + shortcut
       fav = utils.dialog.select('Pick A Favourite For Shortcut',self.actions)
       if fav == -1:
           return
       elif fav == 0:
           ADDON.setSetting('CustomAddon%s' % shortcut,'')
           ADDON.setSetting('CustomAddon%s.label' % shortcut,'')
           self.getControl(TITLE).setLabel('iVue Shortcut%s' % shortcut)
           ADDON.setSetting('CustomAddon%s.image' % shortcut,'')
           self.getControl(IMAGE).setImage(self.C_POPUP_ADDON_IMAGE_iVue)
       elif fav == 1:
           control = utils.addons()
           self.default(shortcut, control)

       else:
           fav_name = self.names[fav-2]
           link = self.favourites[fav_name]
           matches = re.compile('name="(.*?)".+?thumb="(.+?)"').findall(self.data)
           label = xbmc.Keyboard(fav_name,'[COLOR yellow][B]Set Shortcut Label[/B][/COLOR]')
           label.doModal()
           if (label.isConfirmed()):
               input= label.getText()
               ADDON.setSetting('CustomAddon%s' % shortcut,link)
               ADDON.setSetting('CustomAddon%s.label' % shortcut,input)
               self.getControl(TITLE).setLabel(input)
               ADDON.setSetting('CustomAddon%s.image' % shortcut,self.C_POPUP_ADDON_IMAGE_iVue)
               self.getControl(IMAGE).setImage(self.C_POPUP_ADDON_IMAGE_iVue)
               for name, thumb in matches:
                   if fav_name not in name:
                       name = utils.remove_formatting(name)
                       if fav_name in name:
                           if thumb:
                               ADDON.setSetting('CustomAddon%s.image' % shortcut,str(thumb))
                               self.getControl(IMAGE).setImage(str(thumb))

                   elif fav_name in name:
                       if thumb:
                           ADDON.setSetting('CustomAddon%s.image' % shortcut,str(thumb))
                           self.getControl(IMAGE).setImage(str(thumb))

           else:
               return

    def default(self, shortcut, list):
       TITLE = 31010 + shortcut
       IMAGE = 32010 + shortcut
       self.getControl(TITLE).setLabel(str(list[0]))
       self.getControl(IMAGE).setImage(list[1]) 
       ADDON.setSetting('CustomAddon%s' % shortcut, list[2])
       ADDON.setSetting('CustomAddon%s.image' % shortcut, list[1])
       ADDON.setSetting('CustomAddon%s.label' % shortcut, list[0])

    def onFocus(self, controlId):
        pass

class CatMenu(xbmcgui.WindowXMLDialog):
    C_CAT_QUIT = 7003
    C_CAT_CATEGORY = 7004
    C_CAT_SET_CATEGORY = 7005 

    def __new__(
        cls,
        database,
        category,
        categories, 
        ):

        # Skin in resources
        # return super(CatMenu, cls).__new__(cls, 'script-tvguide-categories.xml', ADDON.getAddonInfo('path'), SKIN)
        # Skin in user settings

        return super(CatMenu, cls).__new__(cls,
                'script-tvguide-categories.xml', SKINFOLDER, SKIN)

    def __init__(
        self,
        database,
        category,
        categories, 
        ):
        """

........@type database: source.Database
........"""

        super(CatMenu, self).__init__()
        self.database = database
        self.buttonClicked = None
        self.category = category
        self.selected_category = category
        self.categories = categories 

    def onInit(self):

        items = list()
        categories = ["All Channels"] + sorted(self.categories, key=lambda x: x.lower())
        for label in categories:
            item = xbmcgui.ListItem(label)

            items.append(item)
        listControl = self.getControl(self.C_CAT_CATEGORY)
        listControl.addItems(items)
        if self.selected_category and self.selected_category in categories:
            index = categories.index(self.selected_category)
            listControl.selectItem(index)

    def onAction(self, action):
        if action.getId() in [KEY_CONTEXT_MENU]:
            kodi = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
            if kodi < 16:
                utils.dialog.ok('TEAM IVUE', 'Editing categories in Kodi %s is currently not supported.' % kodi, 'If you would like to use this option please update kodi to the latest stable version or you can import you own catergories.ini via the settings. Thank you for using iVue')
            else:
                cList = self.getControl(self.C_CAT_CATEGORY)
                item = cList.getSelectedItem()
                if item:
                    self.selected_category = item.getLabel()
                if self.selected_category == "All Channels":
                    selection = ["Add Category"]
                else:
                    selection = ["Add Channels","Remove Channels","Clear Channels"]
                ret = utils.dialog.select("%s" % self.selected_category, selection)
                if ret < 0:
                    return

                f = utils.xbmcvfs.File(utils.CatFile,'rb')
                lines = f.read().splitlines()
                f.close()
                categories = {}
                if self.selected_category not in ["All Channels"]:
                    categories[self.selected_category] = []
                for line in lines:
                    if '=' in line:
                        name,cat = line.strip().split('=')
                        if cat not in categories:
                            categories[cat] = []
                        categories[cat].append(name)

                if ret == 0:
                    channelList = sorted([channel.title for channel in self.database.getChannelList(onlyVisible=True,all=True)])
                    channelList = [c for c in channelList if c not in categories[self.selected_category]]
                    str = 'Add Channels To %s' % self.selected_category
                    ret = utils.dialog.multiselect(str, channelList)
                    if ret is None:
                        return
                    if not ret:
                        ret = []
                    channels = []
                    for i in ret:
                        channels.append(channelList[i])

                    for channel in channels:
                        if channel not in categories[self.selected_category]:
                            categories[self.selected_category].append(channel)

                elif ret == 1:
                    channelList = sorted(categories[self.selected_category])
                    str = 'Remove Channels From %s' % self.selected_category
                    ret = utils.dialog.multiselect(str, channelList)
                    if ret is None:
                        return
                    if not ret:
                        ret = []
                    channels = []
                    for i in ret:
                        channelList[i] = ""
                    categories[self.selected_category] = []
                    for name in channelList:
                        if name:
                            categories[self.selected_category].append(name)

                elif ret == 2:
                    categories[self.category] = []

                f = utils.xbmcvfs.File(utils.CatFile,'wb')
                for cat in categories:
                    channels = categories[cat]
                    for channel in channels:
                        f.write("%s=%s\n" % (channel.encode("utf8"),cat))
                f.close()
                self.categories = [category for category in categories if category]
        elif action.getId() in [ACTION_PARENT_DIR, KEY_NAV_BACK, KEY_ESC]:
            self.close()

    def onClick(self, controlId):
        if controlId == self.C_CAT_CATEGORY:
            cList = self.getControl(self.C_CAT_CATEGORY)
            item = cList.getSelectedItem()
            if item:
                self.selected_category = item.getLabel()
                self.category = self.selected_category
            self.buttonClicked = controlId
            self.close()
        elif controlId == 80005:
            kodi = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
            if kodi < 16:
                utils.dialog.ok('TEAM IVUE', 'Adding categories in Kodi %s is currently not supported.' % kodi, 'If you would like to use this option please update kodi to the latest stable version or you can import you own catergories.ini via the settings. Thank you for using iVue')
            else:
                cat = utils.dialog.input('Add Category', type=xbmcgui.INPUT_ALPHANUM)
                if cat:
                    categories = set(self.categories)
                    categories.add(cat)
                    self.categories = list(set(categories))
                    items = list()
                    categories = ["All Channels"] + list(self.categories)
                    for label in categories:
                        item = xbmcgui.ListItem(label)
                        items.append(item)
                    listControl = self.getControl(self.C_CAT_CATEGORY)
                    listControl.reset()
                    listControl.addItems(items)
        else:
            self.buttonClicked = controlId
            self.close()

    def onFocus(self, controlId):
        pass


class ChannelsMenu(xbmcgui.WindowXMLDialog):

    C_CHANNELS_LIST = 6000
    C_CHANNELS_SELECTION_VISIBLE = 6001
    C_CHANNELS_SELECTION = 6002
    C_CHANNELS_SAVE = 6003
    C_CHANNELS_CANCEL = 6004

    def __new__(cls, database):

        # Skin in resources
        # return super(ChannelsMenu, cls).__new__(cls, 'script-tvguide-channels.xml', ADDON.getAddonInfo('path'), SKIN)
        # Skin in user settings

        return super(ChannelsMenu, cls).__new__(cls,
                'script-tvguide-channels.xml', SKINFOLDER, SKIN)

    def __init__(self, database):
        """

........@type database: source.Database
........"""

        super(ChannelsMenu, self).__init__()
        self.database = database
        self.channelList = database.getChannelList(onlyVisible=True, all=True, notVisible=False)
        self.swapInProgress = False
        self.Hidden = True
        self.selectedChannel = 0

    def onInit(self, hidden=False):
        if hidden == True:
            self.channelList= self.database.getChannelList(onlyVisible=False, all=True, notVisible=True)
        else:
            self.channelList= self.database.getChannelList(onlyVisible=True, all=True, notVisible=False)
        self.updateChannelList()
        self.setFocusId(self.C_CHANNELS_LIST)

    def onAction(self, action):
        if action.getId() in [ACTION_PARENT_DIR, KEY_NAV_BACK]:
            self.close()
            return

        if self.getFocusId() == self.C_CHANNELS_LIST and action.getId() in [ACTION_PREVIOUS_MENU, ACTION_LEFT,ACTION_GESTURE_SWIPE_LEFT] and self.Hidden != False:
            listControl = self.getControl(self.C_CHANNELS_LIST)
            idx = listControl.getSelectedPosition()
            self.selectedChannel = idx
            buttonControl = self.getControl(self.C_CHANNELS_SELECTION)
            buttonControl.setLabel('[B]%s[/B]' % (self.channelList[idx].title))

            self.getControl(self.C_CHANNELS_SELECTION_VISIBLE).setVisible(False)
            self.setFocusId(self.C_CHANNELS_SELECTION)

        elif self.getFocusId() == self.C_CHANNELS_SELECTION and action.getId() in [ACTION_RIGHT, ACTION_SELECT_ITEM]:
            self.getControl(self.C_CHANNELS_SELECTION_VISIBLE).setVisible(True)
            xbmc.sleep(350)
            self.setFocusId(self.C_CHANNELS_LIST)
            
        elif self.getFocusId() == self.C_CHANNELS_LIST and action.getId() in [KEY_CONTEXT_MENU]:
            if self.Hidden == True:
                self.Hidden = False
                self.onInit(hidden=True)
            else:
                self.onInit()
                self.Hidden = True
        elif self.getFocusId() == self.C_CHANNELS_SELECTION and action.getId() in [ACTION_PREVIOUS_MENU,KEY_CONTEXT_MENU]:
            listControl = self.getControl(self.C_CHANNELS_LIST)
            idx = listControl.getSelectedPosition()
            self.swapChannels(self.selectedChannel, idx)
            self.getControl(self.C_CHANNELS_SELECTION_VISIBLE).setVisible(True)
            xbmc.sleep(350)
            self.setFocusId(self.C_CHANNELS_LIST)

        elif self.getFocusId() == self.C_CHANNELS_SELECTION and action.getId() == ACTION_UP:
            listControl = self.getControl(self.C_CHANNELS_LIST)
            idx = listControl.getSelectedPosition()
            if idx > 0:
                self.swapChannels(idx, idx - 1)

        elif self.getFocusId() == self.C_CHANNELS_SELECTION and action.getId() == ACTION_DOWN:
            listControl = self.getControl(self.C_CHANNELS_LIST)
            idx = listControl.getSelectedPosition()
            if idx < listControl.size() - 1:
                self.swapChannels(idx, idx + 1)

    def onClick(self, controlId):
        if controlId == self.C_CHANNELS_LIST:
            listControl = self.getControl(self.C_CHANNELS_LIST)
            item = listControl.getSelectedItem()
            channel = self.channelList[int(item.getProperty('idx'))]
            channel.visible = not channel.visible

            if channel.visible:
                iconImage = 'tvguide-channel-visible.png'
            else:
                iconImage = 'tvguide-channel-hidden.png'
            item.setIconImage(iconImage)
        elif controlId == self.C_CHANNELS_SAVE:
            self.database.saveChannelList(self.close, self.channelList)
            time.sleep(0.5)
            self.database.channelSetup()

        elif controlId == self.C_CHANNELS_CANCEL:

            self.close()

    def onFocus(self, controlId):
        pass

    def updateChannelList(self):
        listControl = self.getControl(self.C_CHANNELS_LIST)
        listControl.reset()
        for (idx, channel) in enumerate(self.channelList):
            if channel.visible:
                iconImage = 'tvguide-channel-visible.png'
            else:
                iconImage = 'tvguide-channel-hidden.png'
            #if self.Hidden == False:
                #idx = channel.weight + 1
            item = xbmcgui.ListItem('%3d. %s' % (idx + 1,
                                    channel.title), iconImage=iconImage)
            item.setProperty('idx', str(idx))
            listControl.addItem(item)

    def updateListItem(self, idx, item):
        channel = self.channelList[idx]
        item.setLabel('%3d. %s' % (idx + 1, channel.title))

        if channel.visible:
            iconImage = 'tvguide-channel-visible.png'
        else:
            iconImage = 'tvguide-channel-hidden.png'
        item.setIconImage(iconImage)
        item.setProperty('idx', str(idx))

    def swapChannels(self, fromIdx, toIdx):
        if self.swapInProgress:
            return
        self.swapInProgress = True

        c = self.channelList[fromIdx]
        self.channelList[fromIdx] = self.channelList[toIdx]
        self.channelList[toIdx] = c

        # recalculate weight

        for (idx, channel) in enumerate(self.channelList):
            channel.weight = idx

        listControl = self.getControl(self.C_CHANNELS_LIST)
        self.updateListItem(fromIdx, listControl.getListItem(fromIdx))
        self.updateListItem(toIdx, listControl.getListItem(toIdx))

        listControl.selectItem(toIdx)
        xbmc.sleep(50)
        self.swapInProgress = False


class StreamSetupDialog(xbmcgui.WindowXMLDialog):

    C_STREAM_STRM_TAB = 101
    C_STREAM_FAVOURITES_TAB = 102
    C_STREAM_ADDONS_TAB = 103
    C_STREAM_STRM_BROWSE = 1001
    C_STREAM_STRM_FILE_LABEL = 1005
    C_STREAM_STRM_PREVIEW = 1002
    C_STREAM_STRM_OK = 1003
    C_STREAM_STRM_CANCEL = 1004
    C_STREAM_FAVOURITES = 2001
    C_STREAM_FAVOURITES_PREVIEW = 2002
    C_STREAM_FAVOURITES_OK = 2003
    C_STREAM_FAVOURITES_CANCEL = 2004
    C_STREAM_ADDONS = 3001
    C_STREAM_ADDONS_STREAMS = 3002
    C_STREAM_ADDONS_NAME = 3003
    C_STREAM_ADDONS_DESCRIPTION = 3004
    C_STREAM_ADDONS_PREVIEW = 3005
    C_STREAM_ADDONS_OK = 3006
    C_STREAM_ADDONS_CANCEL = 3007

    C_STREAM_VISIBILITY_MARKER = 100

    VISIBLE_STRM = 'strm'
    VISIBLE_FAVOURITES = 'favourites'
    VISIBLE_ADDONS = 'addons'

    def __new__(cls, database, channel):

        # Skin in resources
        # return super(StreamSetupDialog, cls).__new__(cls, 'script-tvguide-streamsetup.xml', ADDON.getAddonInfo('path'), SKIN)
        # Skin in user settings

        return super(StreamSetupDialog, cls).__new__(cls,
                'script-tvguide-streamsetup.xml', SKINFOLDER, SKIN)

    def __init__(self, database, channel):
        """
........@type database: source.Database
........@type channel:source.Channel
........"""

        super(StreamSetupDialog, self).__init__()
        self.database = database
        self.channel = channel

        self.player = xbmc.Player()
        self.previousAddonId = None
        self.strmFile = None
        self.streamingService = streaming.StreamsService(ADDON)

    def close(self):
        if self.player.isPlaying():

            # Custom

            self.player.stop()
            print ''
        super(StreamSetupDialog, self).close()

    def onInit(self):
        self.getControl(self.C_STREAM_VISIBILITY_MARKER).setLabel(self.VISIBLE_STRM)

        favourites = self.streamingService.loadFavourites()
        items = list()
        for (label, value) in favourites:
            item = xbmcgui.ListItem(label)
            item.setProperty('stream', value)
            items.append(item)

        listControl = \
            self.getControl(StreamSetupDialog.C_STREAM_FAVOURITES)
        listControl.addItems(items)

        items = list()
        for id in self.streamingService.getAddons():
            try:
                addon = xbmcaddon.Addon(id)  # raises Exception if addon is not installed
                item = xbmcgui.ListItem(addon.getAddonInfo('name'),
                        iconImage=addon.getAddonInfo('icon'))
                item.setProperty('addon_id', id)
                items.append(item)
            except Exception:
                pass
        listControl = self.getControl(StreamSetupDialog.C_STREAM_ADDONS)
        listControl.addItems(items)
        self.updateAddonInfo()

    def onAction(self, action):
        if action.getId() in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU,
                              KEY_NAV_BACK, KEY_CONTEXT_MENU]:
            self.close()
            return
        elif self.getFocusId() == self.C_STREAM_ADDONS:

            self.updateAddonInfo()

    def onClick(self, controlId):
        if controlId == self.C_STREAM_STRM_BROWSE:
            stream = utils.dialog.browse(1,
                    ADDON.getLocalizedString(30304), 'video', '.strm')
            if stream:
                self.database.setCustomStreamUrl(self.channel, stream)
                self.getControl(self.C_STREAM_STRM_FILE_LABEL).setText(stream)
                self.strmFile = stream
        elif controlId == self.C_STREAM_ADDONS_OK:

            listControl = self.getControl(self.C_STREAM_ADDONS_STREAMS)
            item = listControl.getSelectedItem()
            if item:
                stream = item.getProperty('stream')
                self.database.setCustomStreamUrl(self.channel, stream)
            self.close()
        elif controlId == self.C_STREAM_FAVOURITES_OK:

            listControl = self.getControl(self.C_STREAM_FAVOURITES)
            item = listControl.getSelectedItem()
            if item:
                stream = item.getProperty('stream')
                self.database.setCustomStreamUrl(self.channel, stream)
            self.close()
        elif controlId == self.C_STREAM_STRM_OK:

            self.database.setCustomStreamUrl(self.channel,
                    self.strmFile)
            self.close()
        elif controlId in [self.C_STREAM_ADDONS_CANCEL,
                           self.C_STREAM_FAVOURITES_CANCEL,
                           self.C_STREAM_STRM_CANCEL]:

            self.close()
        elif controlId in [self.C_STREAM_ADDONS_PREVIEW,
                           self.C_STREAM_FAVOURITES_PREVIEW,
                           self.C_STREAM_STRM_PREVIEW]:

            if self.player.isPlaying():

                # Custom no stop

                self.player.stop()
                self.getControl(self.C_STREAM_ADDONS_PREVIEW).setLabel(strings(PREVIEW_STREAM))
                self.getControl(self.C_STREAM_FAVOURITES_PREVIEW).setLabel(strings(PREVIEW_STREAM))
                self.getControl(self.C_STREAM_STRM_PREVIEW).setLabel(strings(PREVIEW_STREAM))
                return

            stream = None
            visible = \
                self.getControl(self.C_STREAM_VISIBILITY_MARKER).getLabel()
            if visible == self.VISIBLE_ADDONS:
                listControl = \
                    self.getControl(self.C_STREAM_ADDONS_STREAMS)
                item = listControl.getSelectedItem()
                if item:
                    stream = item.getProperty('stream')
            elif visible == self.VISIBLE_FAVOURITES:
                listControl = self.getControl(self.C_STREAM_FAVOURITES)
                item = listControl.getSelectedItem()
                if item:
                    stream = item.getProperty('stream')
            elif visible == self.VISIBLE_STRM:
                stream = self.strmFile

            if stream is not None:
                self.player.play(item=stream, windowed=True)
                if self.player.isPlaying():
                    self.getControl(self.C_STREAM_ADDONS_PREVIEW).setLabel(strings(STOP_PREVIEW))
                    self.getControl(self.C_STREAM_FAVOURITES_PREVIEW).setLabel(strings(STOP_PREVIEW))
                    self.getControl(self.C_STREAM_STRM_PREVIEW).setLabel(strings(STOP_PREVIEW))

    def onFocus(self, controlId):
        if controlId == self.C_STREAM_STRM_TAB:
            self.getControl(self.C_STREAM_VISIBILITY_MARKER).setLabel(self.VISIBLE_STRM)
        elif controlId == self.C_STREAM_FAVOURITES_TAB:
            self.getControl(self.C_STREAM_VISIBILITY_MARKER).setLabel(self.VISIBLE_FAVOURITES)
        elif controlId == self.C_STREAM_ADDONS_TAB:
            self.getControl(self.C_STREAM_VISIBILITY_MARKER).setLabel(self.VISIBLE_ADDONS)

    def updateAddonInfo(self):
        listControl = self.getControl(self.C_STREAM_ADDONS)
        item = listControl.getSelectedItem()
        if item is None:
            return

        if item.getProperty('addon_id') == self.previousAddonId:
            return

        self.previousAddonId = item.getProperty('addon_id')
        addon = xbmcaddon.Addon(id=item.getProperty('addon_id'))
        self.getControl(self.C_STREAM_ADDONS_NAME).setLabel('[B]%s[/B]'
                % addon.getAddonInfo('name'))
        self.getControl(self.C_STREAM_ADDONS_DESCRIPTION).setText(addon.getAddonInfo('description'
                ))

        streams = \
            self.streamingService.getAddonStreams(item.getProperty('addon_id'
                ))
        items = list()
        for (label, stream) in sorted(streams, key=lambda s: s[0].lower()):
            if item.getProperty('addon_id') == 'plugin.video.meta':
                label = self.channel.title
                stream = stream.replace('<channel>',
                        self.channel.title.replace(' ', '%20'))
            item = xbmcgui.ListItem(label)
            item.setProperty('stream', stream)
            items.append(item)
        listControl = \
            self.getControl(StreamSetupDialog.C_STREAM_ADDONS_STREAMS)
        listControl.reset()
        listControl.addItems(items)

class ChooseStreamAddonDialog(xbmcgui.WindowXMLDialog):

    C_SELECTION_LIST = 1000

    def __new__(cls, addons, custom=None):

        # Skin in resources
        # return super(ChooseStreamAddonDialog, cls).__new__(cls, 'script-tvguide-streamaddon.xml', ADDON.getAddonInfo('path'), SKIN)
        # Skin in user settings
        if custom:
            xml = 'script-tvguide-streamcustom.xml'
        else:
            xml = 'script-tvguide-streamaddon.xml'
        return super(ChooseStreamAddonDialog, cls).__new__(cls,
                xml,
                SKINFOLDER, SKIN)

    def __init__(self, addons, custom=None):
        super(ChooseStreamAddonDialog, self).__init__()
        self.addons = addons
        self.stream = None

    # Custom Players

    def onInit(self):

        items = list()
        for (id, label, url) in self.addons:
            try:

                # elif id == 'kodi-favourite':

                if id == 'kodi-favourite':
                    icon = os.path.join(RESOURCES, 'png', 'favourite.png')
                    name = ''
                elif id == 'super-favourite':
                    icon = os.path.join(RESOURCES, 'png', 'superfavourite.png')
                    name = ''
                elif id == 'iptv-playlist':
                    icon = os.path.join(RESOURCES, 'png', 'm3u.png')
                    name = ''
                elif id == 'plugin.video.IVUEcreator':
                    icon = os.path.join(RESOURCES, 'png', 'pvr.png')
                    name = ''
                elif id == 'pvr.iptvsimple':
                    icon = os.path.join(RESOURCES, 'png', 'pvr.png')
                    name = ''
                elif id == 'script.ivueguide':
                    icon = os.path.join(RESOURCES, 'png', 'pvr.png')
                    name = ''
                else:

                    addon = xbmcaddon.Addon(id)
                    icon = addon.getAddonInfo('icon')
                    name = addon.getAddonInfo('name')

                if not name:
                    name = label
                if not icon:
                    icon = ''

                # addon = xbmcaddon.Addon(id)

                item = xbmcgui.ListItem(label, name, icon)
                item.setProperty('stream', url)
                items.append(item)
            except:

                pass

                # addon = xbmcaddon.Addon(id)

                item = xbmcgui.ListItem(label, '', id)
                item.setProperty('stream', url)
                items.append(item)

        listControl = \
            self.getControl(ChooseStreamAddonDialog.C_SELECTION_LIST)
        listControl.addItems(items)
        try:
            self.setFocus(listControl)
        except:
            pass

    def onAction(self, action):
        if action.getId() in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, KEY_NAV_BACK]:
            self.close()

    def onClick(self, controlId):
        if controlId == ChooseStreamAddonDialog.C_SELECTION_LIST:
            listControl = \
                self.getControl(ChooseStreamAddonDialog.C_SELECTION_LIST)
            self.stream = \
                listControl.getSelectedItem().getProperty('stream')
            self.close()

    def onFocus(self, controlId):
        pass

class ProgramListDialog(xbmcgui.WindowXMLDialog):
    C_PROGRAM_LIST_IMAGE = 1007
    C_PROGRAM_LIST_SHORTCUTS = 1006
    C_PROGRAM_LIST_LISTINGS = 1005
    C_PROGRAM_LIST = 1002

    def __new__(
        cls,
        title,
        program,
        sort_time=False,
        ):

        return super(ProgramListDialog, cls).__new__(cls,
                'script-tvguide-programlist.xml',
                SKINFOLDER, SKIN)

    def __init__(
        self,
        title,
        program,
        sort_time=False,
        ):
        """

........@type database: source.Database
........@param program:
........@type program: source.Program
........@param showRemind:
........"""

        super(ProgramListDialog, self).__init__()
        self.title = title
        self.program = program
        self.index = -1
        self.action = None
        self.buttonClicked = None
        self.sort_time = sort_time

    def onInit(self):
        imageControl = self.getControl(ProgramListDialog.C_PROGRAM_LIST_IMAGE)
        plannerControl = self.getControl(ProgramListDialog.C_PROGRAM_LIST_SHORTCUTS)

        if self.title == 'Search':
            plannerControl.setLabel('My Planner')
            imageControl.setImage('search.png')

        elif self.title == 'Planner':
            plannerControl.setLabel('Clear All')
            imageControl.setImage('planner.png')

        items = list()
        index = 0
        item = xbmcgui.ListItem()

        for program in self.program:

            label = program.title.replace(' (?)', '')
            se_label = ""

            label = label + se_label
            name = ""
            icon = program.channel.logo
            item = xbmcgui.ListItem(label, name, icon)

            item.setProperty('index', str(index))
            index = index + 1

            item.setProperty('ChannelName', program.channel.title)
            item.setProperty('Plot', program.description)
            item.setProperty('startDate', str(time.mktime(program.startDate.timetuple())))

            start = program.startDate
            end = program.endDate
            duration = end - start
            now = datetime.datetime.now()

            if now > start:
                when = datetime.timedelta(-1)
                elapsed = now - start
            else:
                when = start - now
                elapsed = datetime.timedelta(0)


            day = utils.formatDate(start, False, True)
            start_str = start.strftime("%H:%M")
            item.setProperty('StartTime',start_str)
            item.setProperty('Day', day)

            duration_str = "%d mins" % (duration.seconds / 60)
            item.setProperty('Duration', duration_str)

            days = when.days
            hours, remainder = divmod(when.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            if days > 1:
                when_str = "On in %d days %d hrs" % (days, hours)
                item.setProperty('When', when_str)
            elif days > 0:
                when_str = "On in %d day %d hrs" % (days, hours)
                item.setProperty('When', when_str)
            elif hours > 1:
                when_str = "On in %d hrs %d mins" % (hours, minutes)
                item.setProperty('When', when_str)
            elif seconds > 0:
                when_str = "On in %d mins" % (when.seconds / 60)
                item.setProperty('When', when_str)
            elif end < now:
                item.setProperty('When', 'Finished')

            if elapsed.seconds > 0 and end > now:
                item.setProperty('When', 'On Now')

            if elapsed.seconds > 0:
                progress = 100.0 * float(timedelta_total_seconds(elapsed)) / float(duration.seconds+0.001)
                progress = str(int(progress))
            else:
                #TODO hack for progress bar with 0 time
                progress = "0"

            if progress and (int(progress) < 100):
                item.setProperty('Completed', progress)

            #if self.database.showNotifications(program.channel, program.startDate):
            if program.notificationScheduled:
                item.setProperty('Remind', 'search_planner.png')

                #
            if program.imageSmall is not None:
                if not program.imageSmall == '':
                    program_image = program.imageSmall
                else:
                    program_image = 'tvguide-logo-epg.png'
            else:
                program_image = 'tvguide-logo-epg.png'

            item.setProperty('ProgramImage', program_image)
            items.append(item)

        if self.sort_time == True:
            items = sorted(items, key=lambda x: x.getProperty('startDate'))

        listControl = self.getControl(ProgramListDialog.C_PROGRAM_LIST)
        listControl.addItems(items)

        if not self.program:
            item.setProperty('Plot', 'NO PROGRAMS FOUND')
            items.append(item)
            listControl.addItems(items)

        self.setFocusId(self.C_PROGRAM_LIST)

    def onAction(self, action):
        if action.getId() in [KEY_CONTEXT_MENU]:
            listControl = self.getControl(self.C_PROGRAM_LIST)
            self.id = self.getFocusId(self.C_PROGRAM_LIST)
            item = listControl.getSelectedItem()
            if item:
                self.index = int(item.getProperty('index'))
            else:
                self.index = -1
            if action.getId() in [KEY_CONTEXT_MENU]:
                self.close()
                self.action = KEY_CONTEXT_MENU

        if action.getId() in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, KEY_NAV_BACK]:
            self.index = -1
            self.close()         

    def onClick(self, controlId):
        if controlId == self.C_PROGRAM_LIST:
            listControl = self.getControl(self.C_PROGRAM_LIST)
            self.id = self.getFocusId(self.C_PROGRAM_LIST)
            item = listControl.getSelectedItem()
            if item:
                self.index = int(item.getProperty('index'))
            else:
                self.index = -1
            self.close()
        else:       
           self.buttonClicked = controlId
           self.close()


    def onFocus(self, controlId):
        pass

    def close(self):
        super(ProgramListDialog, self).close()


class osdOnNowDialog(xbmcgui.WindowXMLDialog):
    C_OSD_EPG_LISTINGS = 1005
    C_OSD_EPG_LIST = 1002
    C_OSD_EPG_TITLE = 1001


    def __new__(
        cls,
        database,
        category,
        sort_time=False,
        ):

        return super(osdOnNowDialog, cls).__new__(cls,
                'script-tvguide-osdEpg.xml',
                SKINFOLDER, SKIN)

    def __init__(
        self,
        database,
        category,
        sort_time=False,
        ):
        """

........@type database: source.Database
........@param program:
........@type program: source.Program
........@param showRemind:
........"""

        super(osdOnNowDialog, self).__init__()
        self.database = database
        self.program = self.database.onNowEpg(category)
        self.index = -1
        self.osdCategory = category
        self.cat = None
        self.action = None
        self.channel = None
        self.buttonClicked = None
        self.sort_time = sort_time

    def onInit(self, cat=None):
        if cat is not None:        
            self.program = self.database.onNowEpg(cat)
            self.osdCategory = cat

        items = list()
        index = 0
        item = xbmcgui.ListItem()

        control = self.getControl(osdOnNowDialog.C_OSD_EPG_TITLE)
        control.setLabel('[B]'+self.osdCategory+'[/B]')

        for program in self.program:

            label = program.title.replace(' (?)', '')
            se_label = ""

            label = label + se_label
            name = ""
            icon = program.channel.logo
            item = xbmcgui.ListItem(label, name, icon)

            item.setProperty('index', str(index))
            index = index + 1

            item.setProperty('ChannelName', program.channel.title)

            start = program.startDate
            end = program.endDate
            duration = end - start
            now = datetime.datetime.now()

            if now > start:
                when = datetime.timedelta(-1)
                elapsed = now - start
            else:
                when = start - now
                elapsed = datetime.timedelta(0)

            hours, remainder = divmod(when.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            if elapsed.seconds > 0:
                progress = 100.0 * float(timedelta_total_seconds(elapsed)) / float(duration.seconds+0.001)
                progress = str(int(progress))
            else:
                #TODO hack for progress bar with 0 time
                progress = "0"

            if progress and (int(progress) < 100):
                item.setProperty('Completed', progress)


            items.append(item)

        if self.sort_time == True:
            items = sorted(items, key=lambda x: x.getProperty('startDate'))

        listControl = self.getControl(osdOnNowDialog.C_OSD_EPG_LIST)
        listControl.addItems(items)

        self.setFocusId(self.C_OSD_EPG_LIST)

    def onAction(self, action):
        filter = []
        with open(utils.CatFile ,'rb') as file:
            lines = file.read().splitlines()

            file.close()
            for line in lines:
                if '=' in line:
                    name = line.strip().split('=')[1]
                    if name not in filter:
                        filter.append(name)
        filter.insert(0, "All Channels")
        filter = sorted(filter, key=lambda x: x.lower())
        if action.getId() in [KEY_CONTEXT_MENU]:
            listControl = self.getControl(self.C_OSD_EPG_LIST)
            self.id = self.getFocusId(self.C_OSD_EPG_LIST)
            item = listControl.getSelectedItem()
            if item:
                self.index = int(item.getProperty('index'))
            else:
                self.index = -1
            if action.getId() in [KEY_CONTEXT_MENU]:
                self.close()
                self.action = KEY_CONTEXT_MENU
        if action.getId() in [ACTION_RIGHT, ACTION_GESTURE_SWIPE_RIGHT]:
            nextItem = filter.index(self.osdCategory)
            nextCat = nextItem + 1
            #if int(nextItem) == filter[-1]:
                #nextCat = "All Channels"
            listControl = self.getControl(self.C_OSD_EPG_LIST)
            listControl.reset()
            try:
                self.onInit(cat=filter[nextCat])
            except:
                self.onInit(cat='All Channels')

        if action.getId() in [ACTION_LEFT, ACTION_GESTURE_SWIPE_LEFT]:
            prevItem = filter.index(self.osdCategory)
            prevCat = prevItem - 1
            if prevItem == filter[0]:
                prevCat = filter[-1]
            listControl = self.getControl(self.C_OSD_EPG_LIST)
            listControl.reset()
            self.onInit(cat=filter[prevCat])

        if action.getId() in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, KEY_NAV_BACK]:
            self.index = -1
            self.close()         

    def onClick(self, controlId):
        if controlId == self.C_OSD_EPG_LIST:
            listControl = self.getControl(self.C_OSD_EPG_LIST)
            self.id = self.getFocusId(self.C_OSD_EPG_LIST)
            item = listControl.getSelectedItem()
            if item:
                self.channel = self.program
                self.index = int(item.getProperty('index'))
            else:
                self.index = -1
            self.close()
        else:       
           self.buttonClicked = controlId
           self.close()



    def onFocus(self, controlId):
        pass

    def close(self):
        super(osdOnNowDialog, self).close()

class ExitDialog(xbmcgui.WindowXMLDialog):

    C_EXIT_CLOSE = 2000
    C_EXIT_CATEGORIES = 2001
    C_EXIT_SEARCH = 2002
    C_EXIT_PLANNER = 2003
    C_EXIT_SCHEDULE = 2004
    C_EXIT_SPORTS = 2005
    C_EXIT_TOOLS = 2006
    C_EXIT_STOP = 2007

    def __new__(cls):

        # Skin in resources
        # return super(ExitDialog, cls).__new__(cls, 'script-tvguide-exitmenu.xml', ADDON.getAddonInfo('path'), SKIN)
        # Skin in user settings

        return super(ExitDialog, cls).__new__(cls,
                'script-tvguide-exitmenu.xml',
                SKINFOLDER, SKIN)

    def __init__(self):
        super(ExitDialog, self).__init__()

    # Custom Players

    def onInit(self):
        self.action = None
        self.buttonClicked = None
        exitControl = self.getControl(self.C_EXIT_CLOSE)

        #self.setFocus(exitControl)

    def onAction(self, action):
        if action.getId() in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, KEY_NAV_BACK]:
            self.close()

    def onClick(self, controlId):
        self.buttonClicked = controlId
        self.close()        

    def onFocus(self, controlId):
        pass



class startUp(xbmcgui.WindowXMLDialog):
    C_PROGRAM_LIST = 1002

    def __new__(
        cls
        ):

        return super(startUp, cls).__new__(cls,
                'script-tvguide-los.xml',
                SKINFOLDER, SKIN)

    def __init__(
        self
        ):

        super(startUp, self).__init__()
        self.index = -1
        self.action = None
        self.buttonClicked = None

    def onInit(self):

        items = list()
        index = 0
        item = xbmcgui.ListItem()
        for sport in utils.TOP_SPORTS:

            label = '[B]'+sport+'[/B]'
            name = ""
            icon = sport.replace('/','_')+'.png'
            item = xbmcgui.ListItem(label, name, icon)
            item.setProperty('index', str(index))
            item.setProperty('date', '')
            index = index + 1

            items.append(item)

        listControl = self.getControl(startUp.C_PROGRAM_LIST)
        listControl.addItems(items)

        self.setFocusId(self.C_PROGRAM_LIST)


    def onClick(self, controlId):
        if controlId == self.C_PROGRAM_LIST:
            listControl = self.getControl(self.C_PROGRAM_LIST)
            item = listControl.getSelectedItem()
            if item:
                if isinstance(eval('utils.'+item.getLabel().replace('[/B]','').replace('[B]','').replace('/','_').replace(' ','_')), str):
                    w = los_List(eval('utils.'+item.getLabel().replace('[/B]','').replace('[B]','').replace('/','_').replace(' ','_')))
                    w.doModal()
                    del w
                else:
                    w = selectionList(item.getLabel().replace('[/B]','').replace('[B]','').replace('/','_').replace(' ','_'))
                    w.doModal()
                    del w


    def onFocus(self, controlId):

        pass


    def close(self):
        super(startUp, self).close()

class selectionList(xbmcgui.WindowXMLDialog):
    C_PROGRAM_LIST = 1002

    def __new__(
        cls,
        sport
        ):

        return super(selectionList, cls).__new__(cls,
                'script-tvguide-los_selection.xml',
                SKINFOLDER, SKIN)

    def __init__(
        self,
        sport
        ):

        super(selectionList, self).__init__()
        self.index = -1
        self.action = None
        self.buttonClicked = None
        self.sport = sport

    def onInit(self):

        items = list()
        index = 0
        item = xbmcgui.ListItem()
        for type in eval('utils.'+self.sport):

            label = type
            name = ""
            icon = ""
            item = xbmcgui.ListItem(label, name, icon)
            item.setProperty('index', str(index))
            index = index + 1

            items.append(item)

        listControl = self.getControl(selectionList.C_PROGRAM_LIST)
        listControl.addItems(items)

        self.setFocusId(self.C_PROGRAM_LIST)


    def onClick(self, controlId):
        if controlId == self.C_PROGRAM_LIST:
            listControl = self.getControl(self.C_PROGRAM_LIST)
            item = listControl.getSelectedItem()
            if item:
                w = los_List(eval('utils.'+item.getLabel().replace('/','_').replace(' ','_')))
                w.doModal()
                del w


    def onFocus(self, controlId):

        pass


    def close(self):
        super(selectionList, self).close()


class los_List(xbmcgui.WindowXMLDialog):
    C_PROGRAM_LIST = 1002

    def __new__(
        cls,
        label
        ):

        return super(los_List, cls).__new__(cls,
                'script-tvguide-los_list.xml',
                SKINFOLDER, SKIN)

    def __init__(
        self,

       label
        ):

        super(los_List, self).__init__()
        self.index = -1
        self.action = None
        self.buttonClicked = None
        self.label = label

    def onInit(self):
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        found = 0
        items = list()
        index = 0
        item = xbmcgui.ListItem()
        sportUrl = '%s' % (self.label)
        sportUrl = urllib.quote(sportUrl)
        content = self.getContent(baseUrl+sportUrl)
        foundgames = content.split('<div class=floatAndClearL_list>')


        for section in foundgames:
            foundcomp = section.split('<div><span class')
            fixtureDate = re.findall('time_head>(.*?)<',section)
            for comp in foundcomp:
                competition = re.compile('comp_head>(.*?)</span>',re.DOTALL).findall(comp)
                ko = re.compile('ST: (.*?)\n', re.DOTALL).findall(comp)
                games = re.compile('"250"><img src="(.*?)">', re.MULTILINE | re.DOTALL).findall(comp)
                channels = re.findall('onmouseout=".*?">(.*?)</a>', comp)
                for game in games:
                    found += 1
                    label = game
                    name = ""
                    icon = ""
                    item = xbmcgui.ListItem(label, name, icon)

                    item.setProperty('index', str(index))
                    index = index + 1
                    homebadge = baseUrl+game


                    kotime = ko[0].replace(' ','').replace('\r','')
                    try:
                        ko = datetime.datetime.strptime(kotime, '%H:%M')
                    except:
                        ko = datetime.datetime.fromtimestamp(time.mktime(time.strptime(kotime, "%H:%M")))

                    if '+' in shift:
                        ko = ko + datetime.timedelta(minutes=timeDiff.tm_min, hours=timeDiff.tm_hour)
                    elif '-' in shift:
                        ko = ko - datetime.timedelta(minutes=timeDiff.tm_min, hours=timeDiff.tm_hour)
                    ko = ko.time().strftime('%H:%M')
                    #except:
                        #ko = ko[0]


                    item.setProperty('HomeImage', homebadge)
                    item.setProperty('Day', '%s' % fixtureDate[0]+' - '+ko)
                    item.setProperty('Links', str(channels).decode('utf-8'))
                    item.setProperty('Comp', competition[0])
                    item.setProperty('When', ko)
                    items.append(item)

        listControl = self.getControl(los_List.C_PROGRAM_LIST)
        listControl.addItems(items)

        self.setFocusId(self.C_PROGRAM_LIST)
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        if found == 0:
            utils.dialog.ok('[COLOR fffea800]iVue[/COLOR]', 'No fixtures found','') 
            self.close()

    def getContent(self, url):
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            return link
        except:
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            utils.dialog.ok('[COLOR fffea800]iVue[/COLOR]', 'Problem finding fixtures','Please try again soon')
            self.close() 
            
    def onAction(self, action):
        if action.getId() in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, KEY_NAV_BACK]:
            if xbmc.Player().isPlaying():
                xbmc.Player().stop()
            else:
                self.index = -1
                self.close()         



    def onClick(self, controlId):
        if controlId == self.C_PROGRAM_LIST:
            listControl = self.getControl(self.C_PROGRAM_LIST)
            item = listControl.getSelectedItem()
            if item:
                mychannels= []
                Links = item.getProperty('Links')
                sepChan = Links.split(', ')
                for chan in sepChan:
                    mychannels.append(self.unicodetoascii(chan.replace('[','').replace(']','').replace("'","").replace('/','').replace('$','').replace('| ','').replace('  ','').replace('HD','').replace(' MENA ','').replace('ITVITV  ', 'ITV1 ')))
                    
                channels = utils.dialog.select('[COLOR fffea800]Channels[/COLOR]', mychannels) 
                if channels >=0:
                    xbmc.executebuiltin("ActivateWindow(busydialog)")
                    result = streams.detectStreams(mychannels[channels])

                    
                    if result:
                        xbmc.executebuiltin("Dialog.Close(busydialog)")
                        if os.path.exists(S_ADDON):
                            d = ChooseStreamAddonDialog(result, custom=True)
                        else:
                            d = ChooseStreamAddonDialog(result)
                        d.doModal()
                        if d.stream is not None:
                            xbmc.Player().play(item=d.stream, windowed=True)
                    else:
                        xbmc.executebuiltin("Dialog.Close(busydialog)")
                        utils.dialog.ok('[COLOR fffea800]iVue[/COLOR]', 'No streams found please try another channel '+ mychannels[channels],'') 

    def unicodetoascii(self, text): 
        TEXT = text.replace("\\xe2\\x80\\x99", "'")
        return TEXT


    def onFocus(self, controlId):
        pass

    def close(self):
        super(los_List, self).close()





class osdPopupMenu(xbmcgui.WindowXMLDialog):

    C_OSDPOPUP_CHOOSE_STREAM = 4001
    C_OSDPOPUP_REMIND = 4002
    C_OSDPOPUP_CHANNELS = 4003
    C_OSDPOPUP_QUIT = 4004

    def __new__(
        cls,
        database,
        program,
        showRemind,
        ):

        # Skin in resources
        # return super(osdPopupMenu, cls).__new__(cls, 'script-tvguide-osdmenu.xml', SKINFOLDER, SKIN)
        # Skin in user settings

        return super(osdPopupMenu, cls).__new__(cls,
                'script-tvguide-osdmenu.xml', SKINFOLDER, SKIN)

    def __init__(
        self,
        database,
        program,
        showRemind,
        ):
        """

........@type database: source.Database
........@param program:
........@type program: source.Program
........@param showRemind:
........"""

        super(osdPopupMenu, self).__init__()
        self.database = database
        self.program = program
        self.showRemind = showRemind
        self.buttonClicked = None
        self.action = None

    def onInit(self):
        remindControl = self.getControl(self.C_OSDPOPUP_REMIND)

        if self.database.getCustomStreamUrl(self.program.channel):
            chooseStrmControl = \
                self.getControl(self.C_OSDPOPUP_CHOOSE_STREAM)
            chooseStrmControl.setLabel('')


        if self.program.startDate:
            remindControl.setEnabled(True)
            if self.showRemind:
                remindControl.setLabel('')
            else:
                remindControl.setLabel('')
        else:
            remindControl.setEnabled(False)


    def onAction(self, action):
        if action.getId() in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, KEY_NAV_BACK, KEY_CONTEXT_MENU]:
            self.action = KEY_NAV_BACK
            self.close()
            return

    def onClick(self, controlId):
        if controlId == self.C_OSDPOPUP_CHOOSE_STREAM \
            and self.database.getCustomStreamUrl(self.program.channel):
            self.database.deleteCustomStreamUrl(self.program.channel)
            chooseStrmControl = \
                self.getControl(self.C_OSDPOPUP_CHOOSE_STREAM)
            chooseStrmControl.setLabel('')

        else:

            self.buttonClicked = controlId
            self.close()

    def onFocus(self, controlId):
        pass

