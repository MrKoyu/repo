# -*- coding: utf-8 -*-
#
#      Copyright (C) 2013 Tommy Winther
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

import os
import threading
import datetime
import time
from xml.etree import ElementTree
import re

from strings import *
from guideTypes import *
from fileFetcher import *

import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon
import sqlite3
import utils


SETTINGS_TO_CHECK = ['source', 'xmltv.type', 'xmltv.file', 'xmltv.url', 'sub.xmltv.url', 'xmltv.logo.folder']
timeshift = xbmc.translatePath('special://profile/addon_data/script.ivueguide/timezone.ini')
path_to_settings = xbmc.translatePath('special://profile/addon_data/script.ivueguide')
current_db = xbmc.translatePath('special://profile/addon_data/script.ivueguide/program.db')
class Channel(object):
    def __init__(self, id, title, logo=None, streamUrl=None, visible=True, weight=-1):
        self.id = id
        self.title = title
        self.logo = logo
        self.streamUrl = streamUrl
        self.visible = visible
        self.weight = weight

    def isPlayable(self):
        return hasattr(self, 'streamUrl') and self.streamUrl

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return 'Channel(id=%s, title=%s, logo=%s, streamUrl=%s)' \
               % (self.id, self.title, self.logo, self.streamUrl)


class Program(object):
    def __init__(self, channel, title, startDate, endDate, description, categories, imageLarge=None, imageSmall=None,
                 notificationScheduled=None, season=None, episode=None, is_movie=None, date=None, language="en"):
        """

        @param channel:
        @type channel: source.Channel
        @param title:
        @param startDate:
        @param endDate:
        @param description:
        @param imageLarge:
        @param imageSmall:
        """
        self.channel = channel
        self.title = title
        self.startDate = startDate
        self.endDate = endDate
        self.description = description
        self.categories = categories
        self.imageLarge = imageLarge
        self.imageSmall = imageSmall
        self.notificationScheduled = notificationScheduled
        self.season = season
        self.episode = episode
        self.is_movie = is_movie
        self.date = date
        self.language = language

    def __repr__(self):
        return 'Program(channel=%s, title=%s, startDate=%s, endDate=%s, description=%s, categories=%s, imageLarge=%s, ' \
               'imageSmall=%s, episode=%s, season=%s, is_movie=%s, date=%s)' % (self.channel, self.title, self.startDate,
                                                                       self.endDate, self.description, self.categories, self.imageLarge,
                                                                       self.imageSmall, self.season, self.episode,
                                                                       self.is_movie, self.date)


class SourceException(Exception):
    pass


class SourceUpdateCanceledException(SourceException):
    pass


class SourceNotConfiguredException(SourceException):
    pass


class DatabaseSchemaException(sqlite3.DatabaseError):
    pass


class Database(object):
    SOURCE_DB = 'master.db'
    CHANNELS_PER_PAGE = 8

    def __init__(self):
        self.conn = None
        self.eventQueue = list()
        self.event = threading.Event()
        self.eventResults = dict()

        self.source = instantiateSource()

        self.updateInProgress = False
        self.updateFailed = False
        self.settingsChanged = None
        self.alreadyTriedUnlinking = False
        self.channelList = list()
        self.category = "All Channels" 
        self.osdcategory = None

        profilePath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
        if not os.path.exists(profilePath):
            os.makedirs(profilePath)
        self.databasePath = os.path.join(profilePath, Database.SOURCE_DB)

        threading.Thread(name='Database Event Loop', target=self.eventLoop).start()

    def setCategory(self,category):
        self.category = category
        self.channelList = None

    def getCategory(self):
        return self.category

    def eventLoop(self):
        print 'Database.eventLoop() >>>>>>>>>> starting...'
        while True:
            self.event.wait()
            self.event.clear()

            event = self.eventQueue.pop(0)

            command = event[0]
            callback = event[1]

            print 'Database.eventLoop() >>>>>>>>>> processing command: ' + command.__name__

            try:
                result = command(*event[2:])
                self.eventResults[command.__name__] = result

                if callback:
                    if self._initialize == command:
                        threading.Thread(name='Database callback', target=callback, args=[result]).start()
                    else:
                        threading.Thread(name='Database callback', target=callback).start()

                if self._close == command:
                    del self.eventQueue[:]
                    break

            except Exception:
                print 'Database.eventLoop() >>>>>>>>>> exception!'

        print 'Database.eventLoop() >>>>>>>>>> exiting...'

    def _invokeAndBlockForResult(self, method, *args):
        event = [method, None]
        event.extend(args)
        self.eventQueue.append(event)
        self.event.set()

        while not method.__name__ in self.eventResults:
            time.sleep(0.1)

        result = self.eventResults.get(method.__name__)
        del self.eventResults[method.__name__]
        return result

    def initialize(self, callback, cancel_requested_callback=None):
        self.eventQueue.append([self._initialize, callback, cancel_requested_callback])
        self.event.set()

    def _initialize(self, cancel_requested_callback):
        sqlite3.register_adapter(datetime.datetime, self.adapt_datetime)
        sqlite3.register_converter('timestamp', self.convert_datetime)

        self.alreadyTriedUnlinking = False
        while True:
            if cancel_requested_callback is not None and cancel_requested_callback():
                break

            try:
                self.conn = sqlite3.connect(self.databasePath, detect_types=sqlite3.PARSE_DECLTYPES)
                self.conn.execute('PRAGMA foreign_keys = ON')
                self.conn.row_factory = sqlite3.Row

                # create and drop dummy table to check if database is locked
                c = self.conn.cursor()
                c.execute('CREATE TABLE IF NOT EXISTS database_lock_check(id TEXT PRIMARY KEY)')
                c.execute('DROP TABLE database_lock_check')
                c.close()

                self._createTables()
                self.settingsChanged = self._wasSettingsChanged(ADDON)
                break

            except sqlite3.OperationalError:
                if cancel_requested_callback is None:
                    xbmc.log('[script.ivueguide] Database is locked, bailing out...', xbmc.LOGDEBUG)
                    break
                else:  # ignore 'database is locked'
                    xbmc.log('[script.ivueguide] Database is locked, retrying...', xbmc.LOGDEBUG)

            except sqlite3.DatabaseError:
                self.conn = None
                if self.alreadyTriedUnlinking:
                    xbmc.log('[script.ivueguide] Database is broken and unlink() failed', xbmc.LOGDEBUG)
                    break
                else:
                    try:
                        os.unlink(self.databasePath)
                    except OSError:
                        pass
                    self.alreadyTriedUnlinking = True
                    xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), strings(DATABASE_SCHEMA_ERROR_1),
                                        strings(DATABASE_SCHEMA_ERROR_2), strings(DATABASE_SCHEMA_ERROR_3))

        return self.conn is not None

    def close(self, callback=None):
        self.eventQueue.append([self._close, callback])
        self.event.set()

    def _close(self):
        try:
            # rollback any non-commit'ed changes to avoid database lock
            if self.conn:
                self.conn.rollback()
        except sqlite3.OperationalError:
            pass  # no transaction is active
        if self.conn:
            self.conn.close()

    def _wasSettingsChanged(self, addon):
        gType = GuideTypes()
        if int(addon.getSetting('xmltv.type')) == gType.CUSTOM_FILE_ID:
            settingsChanged = addon.getSetting('xmltv.refresh') == 'true'
        else:
            settingsChanged = False
        noRows = True
        count = 0

        c = self.conn.cursor()
        c.execute('SELECT * FROM settings')
        for row in c:
            noRows = False
            key = row['key']
            if SETTINGS_TO_CHECK.count(key):
                count += 1
                if row['value'] != addon.getSetting(key):
                    settingsChanged = True

        if count != len(SETTINGS_TO_CHECK):
            settingsChanged = True

        if settingsChanged or noRows:
            for key in SETTINGS_TO_CHECK:
                value = addon.getSetting(key).decode('utf-8', 'ignore')
                c.execute('INSERT OR IGNORE INTO settings(key, value) VALUES (?, ?)', [key, value])
                if not c.rowcount:
                    c.execute('UPDATE settings SET value=? WHERE key=?', [value, key])
            self.conn.commit()

        c.close()
        print 'Settings changed: ' + str(settingsChanged)
        return settingsChanged

    def _isCacheExpired(self, date):
        if self.settingsChanged:
            return True

        # check if channel data is up-to-date in database
        try:
            c = self.conn.cursor()
            c.execute('SELECT channels_updated FROM sources WHERE id=?', [self.source.KEY])
            row = c.fetchone()
            if not row:
                return True
            channelsLastUpdated = row['channels_updated']
            c.close()
        except TypeError:
            return True

        # check if program data is up-to-date in database
        dateStr = date.strftime('%Y-%m-%d')
        c = self.conn.cursor()
        c.execute('SELECT programs_updated FROM updates WHERE source=? AND date=?', [self.source.KEY, dateStr])
        row = c.fetchone()
        if row:
            programsLastUpdated = row['programs_updated']
        else:
            programsLastUpdated = datetime.datetime.fromtimestamp(0)
        c.close()

        return self.source.isUpdated(channelsLastUpdated, programsLastUpdated)

    def updateChannelAndProgramListCaches(self, callback, date=datetime.datetime.now(), progress_callback=None,
                                          clearExistingProgramList=True):
        self.eventQueue.append(
            [self._updateChannelAndProgramListCaches, callback, date, progress_callback, clearExistingProgramList])
        self.event.set()

    def _updateChannelAndProgramListCaches(self, date, progress_callback, clearExistingProgramList):
        # todo workaround service.py 'forgets' the adapter and convert set in _initialize.. wtf?!
        sqlite3.register_adapter(datetime.datetime, self.adapt_datetime)
        sqlite3.register_converter('timestamp', self.convert_datetime)

        if not self._isCacheExpired(date) and not self.source.needReset:
            return
        else:
            # if the xmltv data needs to be loaded the database
            # should be reset to avoid ghosting!
            self.updateInProgress = True
            c = self.conn.cursor()
            c.execute("DELETE FROM updates")
            c.execute("UPDATE sources SET channels_updated=0")
            self.conn.commit()
            c.close()
            self.source.needReset = False

        self.updateInProgress = True
        self.updateFailed = False
        dateStr = date.strftime('%Y-%m-%d')
        c = self.conn.cursor()
        try:
            if os.path.exists(timeshift):
                os.remove(timeshift)
            xbmc.log('[script.ivueguide] Updating caches...', xbmc.LOGDEBUG)
            if progress_callback:
                progress_callback(0)

            if self.settingsChanged:
                c.execute('DELETE FROM channels WHERE source=?', [self.source.KEY])
                c.execute('DELETE FROM programs WHERE source=?', [self.source.KEY])
                c.execute("DELETE FROM updates WHERE source=?", [self.source.KEY])
            self.settingsChanged = False  # only want to update once due to changed settings

            if clearExistingProgramList:
                c.execute("DELETE FROM updates WHERE source=?",
                          [self.source.KEY])  # cascades and deletes associated programs records
            else:
                c.execute("DELETE FROM updates WHERE source=? AND date=?",
                          [self.source.KEY, dateStr])  # cascades and deletes associated programs records

            # programs updated
            c.execute("INSERT INTO updates(source, date, programs_updated) VALUES(?, ?, ?)",
                      [self.source.KEY, dateStr, datetime.datetime.now()])
            updatesId = c.lastrowid

            if not os.path.exists(current_db):
                imported = imported_channels = imported_programs = 0
                for item in self.source.getDataFromExternal(date, progress_callback):
                    imported += 1

                    if imported % 10000 == 0:
                        self.conn.commit()

                    if isinstance(item, Channel):
                        imported_channels += 1
                        channel = item
                        c.execute(
                            'INSERT OR IGNORE INTO channels(id, title, logo, stream_url, visible, weight, source) VALUES(?, ?, ?, ?, ?, (CASE ? WHEN -1 THEN (SELECT COALESCE(MAX(weight)+1, 0) FROM channels WHERE source=?) ELSE ? END), ?)',
                            [channel.id, channel.title, channel.logo, channel.streamUrl, channel.visible, channel.weight,
                             self.source.KEY, channel.weight, self.source.KEY])
                        if not c.rowcount:
                            c.execute(
                                'UPDATE channels SET title=?, logo=?, stream_url=?, visible=(CASE ? WHEN -1 THEN visible ELSE ? END), weight=(CASE ? WHEN -1 THEN weight ELSE ? END) WHERE id=? AND source=?',
                                [channel.title, channel.logo, channel.streamUrl, channel.weight, channel.visible,
                                 channel.weight, channel.weight, channel.id, self.source.KEY])

                    elif isinstance(item, Program):
                        imported_programs += 1
                        program = item
                        if isinstance(program.channel, Channel):
                            channel = program.channel.id
                        else:
                            channel = program.channel

                        try:
                            c.execute(
                                'INSERT INTO programs(channel, title, start_date, end_date, description, categories, image_large, image_small, season, episode, is_movie, date, language, source, updates_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                [channel, program.title, program.startDate, program.endDate, program.description, program.categories,
                                 program.imageLarge, program.imageSmall, program.season, program.episode, program.is_movie,
                                 program.date, program.language, self.source.KEY, updatesId])
                        except sqlite3.InterfaceError:
                            pass

                if imported_channels == 0 or imported_programs == 0:
                    self.updateFailed = True

            else:
                c.execute('PRAGMA foreign_keys = OFF')
                channels = self.source.parseXMLTVchannels(progress_callback)
                c.executemany(
                    'INSERT OR IGNORE INTO channels(id, title, logo, stream_url, source, visible, weight) VALUES(?, ?, ?, ?, ?, ?, ?)',
                    channels, )
                if progress_callback:
                    progress_callback(32)


                #c.execute("DROP TABLE IF EXISTS programs") 
                c.execute("ATTACH DATABASE ? AS db2", (current_db,))
                c.execute("SELECT * FROM db2.sqlite_master WHERE type='table' AND name='programs'")
                c.fetchone()[0]
                c.execute("INSERT INTO programs SELECT * FROM db2.programs") 
                if progress_callback:
                    progress_callback(99)
        



            # channels updated
            c.execute("UPDATE sources SET channels_updated=? WHERE id=?", [datetime.datetime.now(), self.source.KEY])
            self.conn.commit()


        except SourceUpdateCanceledException:
            # force source update on next load
            c.execute('UPDATE sources SET channels_updated=? WHERE id=?', [0, self.source.KEY])
            c.execute("DELETE FROM updates WHERE source=?",
                      [self.source.KEY])  # cascades and deletes associated programs records
            self.conn.commit()

        except Exception:
            import traceback as tb
            import sys

            (etype, value, traceback) = sys.exc_info()
            tb.print_exception(etype, value, traceback)

            try:
                self.conn.rollback()
            except sqlite3.OperationalError:
                pass  # no transaction is active

            try:
                # invalidate cached data
                c.execute('UPDATE sources SET channels_updated=? WHERE id=?', [0, self.source.KEY])
                self.conn.commit()
            except sqlite3.OperationalError:
                pass  # database is locked

            self.updateFailed = True
        finally:
            self.updateInProgress = False
            c.close()

    def getEPGView(self, channelStart, date=datetime.datetime.now(), progress_callback=None,
                   clearExistingProgramList=True,category=None):
        result = self._invokeAndBlockForResult(self._getEPGView, channelStart, date, progress_callback,
                                               clearExistingProgramList,category)

        if self.updateFailed:
            raise SourceException('No channels or programs imported')

        return result

    def _getEPGView(self, channelStart, date, progress_callback, clearExistingProgramList,category):
        self._updateChannelAndProgramListCaches(date, progress_callback, clearExistingProgramList)

        channels = self._getChannelList(onlyVisible=True)

        if category and category != "All Channels":
            f = xbmcvfs.File(utils.CatFile,'rb')
            lines = f.read().splitlines()
            f.close()
            filter = []
            seen = set()
            for line in lines:
                if "=" not in line:
                    continue
                name,cat = line.split('=')
                if cat == category:
                    if name not in seen:
                        filter.append(name)
                    seen.add(name)

            NONE = "0"
            SORT = "1"
            CATEGORIES = "2"
            new_channels = []
            if ADDON.getSetting('channel.filter.sort') == CATEGORIES:
                for filter_name in filter:
                    for channel in channels:
                        if channel.title == filter_name:
                            new_channels.append(channel)
                if new_channels:
                    channels = new_channels
            else:
                for channel in channels:
                    if channel.title in filter:
                        new_channels.append(channel)
                if new_channels:
                    if ADDON.getSetting('channel.filter.sort') == SORT:
                        channels = sorted(new_channels, key=lambda channel: channel.title.lower())
                    else:
                        channels = new_channels 

        if channelStart < 0:
            channelStart = len(channels) - 1
        elif channelStart > len(channels) - 1:
            channelStart = 0
        channelEnd = channelStart + Database.CHANNELS_PER_PAGE
        channelsOnPage = channels[channelStart: channelEnd]

        programs = self._getProgramList(channelsOnPage, date)

        return [channelStart, channelsOnPage, programs]


    def programSearch(self, search):
        return self._invokeAndBlockForResult(self._programSearch, search)

    def _programSearch(self, search):
        programList = []
        now = datetime.datetime.now()
        startTime = now - datetime.timedelta(days= 7)
        endTime = now + datetime.timedelta(days=7)
        c = self.conn.cursor()
        channelList = self._getChannelList(True, all=True)
        search = "%%%s%%" % search
        for channel in channelList:

            try: c.execute('SELECT p.*, (SELECT 1 FROM notifications n WHERE n.channel=p.channel AND n.program_title=p.title AND n.source=p.source AND n.start_date=p.start_date) AS notification_scheduled FROM programs p WHERE p.channel=? AND p.source=? AND p.start_date>=? AND p.end_date<=? AND (p.title LIKE ?)',
                      [channel.id, self.source.KEY, startTime, endTime, search])
            except: return
            for row in c:
                program = Program(channel, title=row['title'], startDate=row['start_date'], endDate=row['end_date'],
                              description=row['description'], categories=row['categories'],
                              imageLarge=row['image_large'], imageSmall=row['image_small'], notificationScheduled=row['notification_scheduled'])
                programList.append(program)
        c.close()
        return programList


    def searchChannel(self, chan):
        return self._invokeAndBlockForResult(self._searchChannel, chan)

    def _searchChannel(self, chan):
        now = datetime.datetime.now()
        endTime = now + datetime.timedelta(days=7)
        channelList = self._getChannelList(True)
        for channel in channelList:
            if channel.title == chan:
                programList = []
                c = self.conn.cursor()

                c.execute('SELECT p.*, (SELECT 1 FROM notifications n WHERE n.channel=p.channel AND n.program_title=p.title AND n.source=p.source AND n.start_date=p.start_date) AS notification_scheduled FROM programs p WHERE p.channel=? AND p.source=? AND  p.end_date>=?',
                     [channel.id, self.source.KEY, now])

                for row in c:
                    program = Program(channel, title=row['title'], startDate=row['start_date'], endDate=row['end_date'],
                                  description=row['description'], categories=row['categories'],
                                  imageLarge=row['image_large'], imageSmall=row['image_small'], notificationScheduled=row['notification_scheduled'])
                    programList.append(program)
                c.close()

        return programList

    def onNowEpg(self, category):
        return self._invokeAndBlockForResult(self._onNowEpg, category)

    def _onNowEpg(self, category):
        self.osdcategory = category
        programList = []
        now = datetime.datetime.now()
        channels = self._getChannelList(True, all=False, osdCat=True)
        channelIds = [c.id for c in channels]
        channelMap = dict()
        for cc in channels:
            if cc.id:
                channelMap[cc.id] = cc

        c = self.conn.cursor()
        c.execute(
            'SELECT DISTINCT p.*' +
            'FROM programs p, channels c WHERE p.channel IN (\'' + ('\',\''.join(channelIds)) + '\') AND p.channel=c.id AND p.source=? AND p.end_date >= ? AND p.start_date <= ?' +
            'ORDER BY c.weight',
            [self.source.KEY, now, now])

        for row in c:
            notification_scheduled = ''
            program = Program(channelMap[row['channel']], title=row['title'], startDate=row['start_date'], endDate=row['end_date'],
                              description=row['description'], categories=row['categories'],
                              imageLarge=row['image_large'], imageSmall=row['image_small'],
                              notificationScheduled=notification_scheduled)
            programList.append(program)
        c.close()
        return programList

    def getChannel(self, idx):
        channels = self.getChannelList()
        if idx > len(channels) - 1:
            idx = 0
        return channels[idx]


    def getNextChannel(self, currentChannel):
        channels = self.getChannelList()
        idx = channels.index(currentChannel)
        idx += 1
        if idx > len(channels) - 1:
            idx = 0
        return channels[idx]

    def getPreviousChannel(self, currentChannel):
        channels = self.getChannelList()
        idx = channels.index(currentChannel)
        idx -= 1
        if idx < 0:
            idx = len(channels) - 1
        return channels[idx]

    def saveChannelList(self, callback, channelList):
        self.eventQueue.append([self._saveChannelList, callback, channelList])
        self.event.set()

    def _saveChannelList(self, channelList):
        c = self.conn.cursor()
        for idx, channel in enumerate(channelList):
            c.execute(
                'INSERT OR IGNORE INTO channels(id, title, logo, stream_url, visible, weight, source) VALUES(?, ?, ?, ?, ?, (CASE ? WHEN -1 THEN (SELECT COALESCE(MAX(weight)+1, 0) FROM channels WHERE source=?) ELSE ? END), ?)',
                [channel.id, channel.title, channel.logo, channel.streamUrl, channel.visible, channel.weight,
                 self.source.KEY, channel.weight, self.source.KEY])
            if not c.rowcount:
                c.execute(
                    'UPDATE channels SET title=?, logo=?, stream_url=?, visible=?, weight=(CASE ? WHEN -1 THEN weight ELSE ? END) WHERE id=? AND source=?',
                    [channel.title, channel.logo, channel.streamUrl, channel.visible, channel.weight, channel.weight,
                     channel.id, self.source.KEY])

        c.execute("UPDATE sources SET channels_updated=? WHERE id=?", [datetime.datetime.now(), self.source.KEY])
        self.channelList = None
        self.conn.commit()

    def getChannelList(self, onlyVisible=True, all=False, notVisible=False, osdCat=False):
        if not self.channelList or not onlyVisible:
            result = self._invokeAndBlockForResult(self._getChannelList, onlyVisible, all, notVisible, osdCat)

            if not onlyVisible:
                return result

            self.channelList = result
        return self.channelList


    def _getChannelList(self, onlyVisible, all=False, notVisible=False, osdCat=False):
        c = self.conn.cursor()
        channelList = list()
        if notVisible == True:
            c.execute('SELECT * FROM channels WHERE source=? AND visible=? ORDER BY weight', [self.source.KEY, False])
        elif onlyVisible:
            c.execute('SELECT * FROM channels WHERE source=? AND visible=? ORDER BY weight', [self.source.KEY, True])
        else:
            c.execute('SELECT * FROM channels WHERE source=? ORDER BY weight', [self.source.KEY])
        for row in c:
            channel = Channel(row['id'], row['title'], row['logo'], row['stream_url'], row['visible'], row['weight'])
            channelList.append(channel)

        if self.osdcategory is not None and osdCat == True:
            setCat = self.osdcategory
        else:
            setCat = self.category
        if all == False and setCat != "All Channels":
            f = xbmcvfs.File(utils.CatFile,'rb')
            lines = f.read().splitlines()
            f.close()
            filter = []
            seen = set()
            for line in lines:
                if "=" not in line:
                    continue
                name,cat = line.split('=')
                if cat == setCat:
                    if name not in seen:
                        filter.append(name)
                    seen.add(name)

            NONE = "0"
            SORT = "1"
            CATEGORIES = "2"
            new_channels = []
            if ADDON.getSetting('channel.filter.sort') == CATEGORIES:
                for filter_name in filter:
                    for channel in channelList:
                        if channel.title == filter_name:
                            new_channels.append(channel)
                if new_channels:
                    channelList = new_channels
            else:
                for channel in channelList:
                    if channel.title in filter:
                        new_channels.append(channel)
                if new_channels:
                    if ADDON.getSetting('channel.filter.sort') == SORT:
                        channelList = sorted(new_channels, key=lambda channel: channel.title.lower())
                    else:
                        channelList = new_channels
        c.close()
                
        return channelList
        #self.osdcategory = None

    def getChannelINI(self):
	if not os.path.exists(xbmc.translatePath('special://profile/addon_data/plugin.video.IVUEcreator')):
            os.makedirs(xbmc.translatePath('special://profile/addon_data/plugin.video.IVUEcreator'))
        channelsList = self.getChannelList(False,True)
        channels = [channel.title for channel in channelsList]
        ini = xbmcvfs.File('special://profile/addon_data/plugin.video.IVUEcreator/custom_channels.ini','wb')
        for channel in sorted(channels):
            ini.write("%s\n" % channel.encode("utf8"))
        ini.close()

    def channelSetup(self, append=None):
        setupPath = xbmc.translatePath('special://profile/addon_data/script.ivueguide/resources/guide_setups')
        if not os.path.exists(setupPath):
            os.mkdir(setupPath)
        xmltvType = ADDON.getSetting('xmltv.type_select')
        if xmltvType == '':
            xmltvType = 'IVUE (Freeview UK)'
        elif xmltvType == 'Sub File':
            xmltvType = ADDON.getSetting('sub.xmltv')
        xmltvfile = xmltvType + '.ini'
        channelsList = self.getChannelList(False,True)
        ini = xbmcvfs.File('special://profile/addon_data/script.ivueguide/resources/guide_setups/%s' % xmltvfile,'wb')
        for channel in channelsList:
            ini.write("%s , Visible = %s , Position = %s\n" % (str(channel.id.encode("utf8")), str(channel.visible), str(channel.weight)))
        ini.close()

    def getCurrentProgram(self, channel):
        return self._invokeAndBlockForResult(self._getCurrentProgram, channel)

    def _getCurrentProgram(self, channel):
        """

        @param channel:
        @type channel: source.Channel
        @return:
        """
        program = None
        now = datetime.datetime.now()
        c = self.conn.cursor()

        c.execute('SELECT * FROM programs WHERE channel=? AND source=? AND start_date <= ? AND end_date >= ?',
                  [channel.id, self.source.KEY, now, now])
        row = c.fetchone()
        if row:
            program = Program(channel, row['title'], row['start_date'], row['end_date'], row['description'], row['categories'],
                              row['image_large'], row['image_small'], None, row['season'], row['episode'],
                              row['is_movie'], row['date'], row['language'])
        c.close()

        return program


    def getNextProgram(self, channel):
        return self._invokeAndBlockForResult(self._getNextProgram, channel)

    def _getNextProgram(self, program):
        try:
            nextProgram = None
            c = self.conn.cursor()
            c.execute(
                'SELECT * FROM programs WHERE channel=? AND source=? AND start_date >= ? ORDER BY start_date ASC LIMIT 1',
                [program.channel.id, self.source.KEY, program.endDate])
            row = c.fetchone()
            if row:
                nextProgram = Program(program.channel, row['title'], row['start_date'], row['end_date'], row['description'], row['categories'],
                                      row['image_large'], row['image_small'], None, row['season'], row['episode'],
                                      row['is_movie'], row['date'], row['language'])
            c.close()

            return nextProgram

        except:
            return

    def getPreviousProgram(self, channel):
        return self._invokeAndBlockForResult(self._getPreviousProgram, channel)

    def _getPreviousProgram(self, program):
        try:
            previousProgram = None
            c = self.conn.cursor()
            c.execute(
                'SELECT * FROM programs WHERE channel=? AND source=? AND end_date <= ? ORDER BY start_date DESC LIMIT 1',
                [program.channel.id, self.source.KEY, program.startDate])
            row = c.fetchone()
            if row:
                previousProgram = Program(program.channel, row['title'], row['start_date'], row['end_date'], row['description'], row['categories'],
                                      row['image_large'], row['image_small'], None, row['season'], row['episode'],
                                      row['is_movie'], row['date'], row['language'])
            c.close()

            return previousProgram

        except:
            return


    def _getProgramList(self, channels, startTime):
        """

        @param channels:
        @type channels: list of source.Channel
        @param startTime:
        @type startTime: datetime.datetime
        @return:
        """
        endTime = startTime + datetime.timedelta(hours=2)
        programList = list()

        channelMap = dict()
        for c in channels:
            if c.id:
                channelMap[c.id] = c

        if not channels:
            return []



        c = self.conn.cursor()
        c.execute(
            'SELECT p.*, (SELECT 1 FROM notifications n WHERE n.channel=p.channel AND n.program_title=p.title AND n.source=p.source AND n.start_date=p.start_date) AS notification_scheduled FROM programs p WHERE p.channel IN (\'' + (
                '\',\''.join(channelMap.keys())) + '\') AND p.source=? AND p.end_date > ? AND p.start_date < ?',
            [self.source.KEY, startTime, endTime])
        for row in c:
            program = Program(channelMap[row['channel']], row['title'], row['start_date'], row['end_date'],
                              row['description'], row['categories'], row['image_large'], row['image_small'], row['notification_scheduled'],
                              row['season'], row['episode'], row['is_movie'], row['date'], row['language'])
            programList.append(program)

        return programList

    def _isProgramListCacheExpired(self, date=datetime.datetime.now()):
        # check if data is up-to-date in database
        dateStr = date.strftime('%Y-%m-%d')
        c = self.conn.cursor()
        c.execute('SELECT programs_updated FROM updates WHERE source=? AND date=?', [self.source.KEY, dateStr])
        row = c.fetchone()
        today = datetime.datetime.now()
        expired = row is None or row['programs_updated'].day != today.day
        c.close()
        return expired

    def setCustomStreamUrl(self, channel, stream_url):
        if stream_url is not None:
            self._invokeAndBlockForResult(self._setCustomStreamUrl, channel, stream_url)
            # no result, but block until operation is done

    def _setCustomStreamUrl(self, channel, stream_url):
        if stream_url is not None:
            c = self.conn.cursor()
            c.execute("UPDATE channels SET stream_url=? WHERE id=?", [stream_url.decode('utf-8', 'ignore'), channel.id])
            c.execute("DELETE FROM custom_stream_url WHERE channel=?", [channel.id])
            c.execute("INSERT INTO custom_stream_url(channel, stream_url) VALUES(?, ?)",
                      [channel.id, stream_url.decode('utf-8', 'ignore')])
            self.conn.commit()
            c.close()

    def getCustomStreamUrl(self, channel):
        return self._invokeAndBlockForResult(self._getCustomStreamUrl, channel)

    def _getCustomStreamUrl(self, channel):
        c = self.conn.cursor()
        c.execute("SELECT stream_url FROM custom_stream_url WHERE channel=?", [channel.id])
        stream_url = c.fetchone()
        c.close()

        if stream_url:
            return stream_url[0]
        else:
            return None

    def deleteCustomStreamUrl(self, channel):
        self.eventQueue.append([self._deleteCustomStreamUrl, None, channel])
        self.event.set()

    def _deleteCustomStreamUrl(self, channel):
        c = self.conn.cursor()
        c.execute("UPDATE channels SET stream_url=? WHERE id=?", [None, channel.id])
        c.execute("DELETE FROM custom_stream_url WHERE channel=?", [channel.id])
        self.conn.commit()
        c.close()

    def getStreamUrl(self, channel):
        customStreamUrl = self.getCustomStreamUrl(channel)
        if customStreamUrl:
            customStreamUrl = customStreamUrl.encode('utf-8', 'ignore')
            return customStreamUrl

        return None

    @staticmethod
    def adapt_datetime(ts):
        # http://docs.python.org/2/library/sqlite3.html#registering-an-adapter-callable
        return time.mktime(ts.timetuple())

    @staticmethod
    def convert_datetime(ts):
        try:
            return datetime.datetime.fromtimestamp(float(ts))
        except ValueError:
            return None

    def _createTables(self):
        c = self.conn.cursor()

        try:
            c.execute('SELECT major, minor, patch FROM version')
            (major, minor, patch) = c.fetchone()
            version = [major, minor, patch]
        except sqlite3.OperationalError:
            version = [0, 0, 0]

        try:
            if version < [1, 3, 0]:
                c.execute('CREATE TABLE IF NOT EXISTS custom_stream_url(channel TEXT, stream_url TEXT)')
                c.execute('CREATE TABLE version (major INTEGER, minor INTEGER, patch INTEGER)')
                c.execute('INSERT INTO version(major, minor, patch) VALUES(1, 3, 0)')
                # For caching data
                c.execute('CREATE TABLE sources(id TEXT PRIMARY KEY, channels_updated TIMESTAMP)')
                c.execute(
                    'CREATE TABLE updates(id INTEGER PRIMARY KEY, source TEXT, date TEXT, programs_updated TIMESTAMP)')
                c.execute(
                    'CREATE TABLE channels(id TEXT, title TEXT, logo TEXT, stream_url TEXT, source TEXT, visible BOOLEAN, weight INTEGER, PRIMARY KEY (id, source), FOREIGN KEY(source) REFERENCES sources(id) ON DELETE CASCADE)')
                c.execute(
                    'CREATE TABLE programs(channel TEXT, title TEXT, start_date TIMESTAMP, end_date TIMESTAMP, description TEXT, image_large TEXT, image_small TEXT, source TEXT, updates_id INTEGER, FOREIGN KEY(channel, source) REFERENCES channels(id, source) ON DELETE CASCADE, FOREIGN KEY(updates_id) REFERENCES updates(id) ON DELETE CASCADE)')
                c.execute('CREATE INDEX program_list_idx ON programs(source, channel, start_date, end_date)')
                c.execute('CREATE INDEX start_date_idx ON programs(start_date)')
                c.execute('CREATE INDEX end_date_idx ON programs(end_date)')
                # For active setting
                c.execute('CREATE TABLE settings(key TEXT PRIMARY KEY, value TEXT)')
                # For notifications
                c.execute(
                    "CREATE TABLE notifications(channel TEXT, program_title TEXT, source TEXT, FOREIGN KEY(channel, source) REFERENCES channels(id, source) ON DELETE CASCADE)")
            if version < [1, 3, 1]:
                # Recreate tables with FOREIGN KEYS as DEFERRABLE INITIALLY DEFERRED
                c.execute('UPDATE version SET major=1, minor=3, patch=1')
                c.execute('DROP TABLE channels')
                c.execute('DROP TABLE programs')
                c.execute(
                    'CREATE TABLE channels(id TEXT, title TEXT, logo TEXT, stream_url TEXT, source TEXT, visible BOOLEAN, weight INTEGER, PRIMARY KEY (id, source), FOREIGN KEY(source) REFERENCES sources(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED)')
                c.execute(
                    'CREATE TABLE programs(channel TEXT, title TEXT, start_date TIMESTAMP, end_date TIMESTAMP, description TEXT, image_large TEXT, image_small TEXT, source TEXT, updates_id INTEGER, FOREIGN KEY(channel, source) REFERENCES channels(id, source) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED, FOREIGN KEY(updates_id) REFERENCES updates(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED)')
                c.execute('CREATE INDEX program_list_idx ON programs(source, channel, start_date, end_date)')
                c.execute('CREATE INDEX start_date_idx ON programs(start_date)')
                c.execute('CREATE INDEX end_date_idx ON programs(end_date)')
            if version < [1, 3, 5]:
                # Recreate tables with date and ratings
                c.execute('UPDATE version SET major=1, minor=3, patch=5')
                c.execute('DROP TABLE programs')
                c.execute(
                    "CREATE TABLE programs(channel TEXT, title TEXT, start_date TIMESTAMP, end_date TIMESTAMP, description TEXT, categories TEXT, image_large TEXT, image_small TEXT, season TEXT, episode TEXT, is_movie TEXT, date TEXT, language TEXT, source TEXT, updates_id INTEGER, FOREIGN KEY(channel, source) REFERENCES channels(id, source) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED, FOREIGN KEY(updates_id) REFERENCES updates(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED)")
                c.execute('DROP TABLE notifications')
                c.execute(
                    "CREATE TABLE notifications(channel TEXT, channel_title TEXT, program_title TEXT, start_date TIMESTAMP, source TEXT, FOREIGN KEY(channel, source) REFERENCES channels(id, source) ON DELETE CASCADE)")
                c.execute('CREATE INDEX program_list_idx ON programs(source, channel, start_date, end_date)')
                c.execute('CREATE INDEX start_date_idx ON programs(start_date)')
                c.execute('CREATE INDEX end_date_idx ON programs(end_date)')
            # make sure we have a record in sources for this Source
            c.execute("INSERT OR IGNORE INTO sources(id, channels_updated) VALUES(?, ?)", [self.source.KEY, 0])

            self.conn.commit()
            c.close()

        except sqlite3.OperationalError, ex:
            raise DatabaseSchemaException(ex)

    def addNotification(self, program):
        self._invokeAndBlockForResult(self._addNotification, program)
        # no result, but block until operation is done

    def _addNotification(self, program):
        """
        @type program: source.program
        """
        c = self.conn.cursor()
        c.execute("INSERT INTO notifications(channel, channel_title, program_title, start_date, source) VALUES(?, ?, ?, ?, ?)",
                  [program.channel.id, program.channel.title, program.title, program.startDate, self.source.KEY])
        self.conn.commit()
        c.close()

    def removeNotification(self, program):
        self._invokeAndBlockForResult(self._removeNotification, program)
        # no result, but block until operation is done

    def _removeNotification(self, program):
        """
        @type program: source.program
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM notifications WHERE channel=? AND program_title=? AND start_date=? AND source=?",
                  [program.channel.id, program.title, program.startDate, self.source.KEY])
        self.conn.commit()
        c.close()

    def showNotifications(self, channel, startDate):
        profilePath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
        self.databasePath = os.path.join(profilePath, Database.SOURCE_DB)
        self.conn = sqlite3.connect(self.databasePath, detect_types=sqlite3.PARSE_DECLTYPES) 
        c = self.conn.cursor()
        c.execute("SELECT channel_title FROM notifications WHERE channel=? AND start_date=?", [channel.id, startDate])
        stream_url = c.fetchone()
        c.close()

        if stream_url:
            return stream_url[0]
        else:
            return None

    def getNotifications(self, daysLimit=7):
        return self._invokeAndBlockForResult(self._getNotifications, daysLimit)

    def _getNotifications(self, daysLimit):
        start = datetime.datetime.now()
        end = start + datetime.timedelta(days=daysLimit)
        c = self.conn.cursor()
        c.execute(
            "SELECT DISTINCT c.id, c.title, p.title, p.start_date FROM notifications n, channels c, programs p WHERE n.channel = c.id AND p.channel = c.id AND n.program_title = p.title AND n.source=? AND p.start_date >= ? AND p.end_date <= ?",
            [self.source.KEY, start, end])
        programs = c.fetchone()
        c.close()

        return programs

    def showReminders(self, daysLimit=7):
        return self._invokeAndBlockForResult(self._showReminders, daysLimit)

    def _showReminders(self, daysLimit):
        start = datetime.datetime.now()
        end = start + datetime.timedelta(days=daysLimit)
        programList = list()
        c = self.conn.cursor()
        c.execute(
            "SELECT DISTINCT c.id, c.title as channeltitle,c.logo,c.stream_url,c.visible,c.weight, p.* FROM notifications n, channels c, programs p WHERE n.channel = c.id AND p.channel = c.id AND n.program_title = p.title AND n.source=? AND n.start_date = p.start_date",
            [self.source.KEY])
        for row in c:
            channel = Channel(row["id"], row["channeltitle"], row["logo"], row["stream_url"], row["visible"], row["weight"])
            program = Program(channel, title=row['title'], startDate=row['start_date'], endDate=row['end_date'],
                            description=row['description'],categories=row['categories'],imageLarge=row["image_large"],
                            imageSmall=row["image_small"],language=row["language"],
                            notificationScheduled=None)
            programList.append(program)
        c.close()
        return programList


    def isNotificationRequiredForProgram(self, program):
        return self._invokeAndBlockForResult(self._isNotificationRequiredForProgram, program)

    def _isNotificationRequiredForProgram(self, program):
        """
        @type program: source.program
        """
        c = self.conn.cursor()
        c.execute("SELECT 1 FROM notifications WHERE channel=? AND program_title=? AND source=?",
                  [program.channel.id, program.title, self.source.KEY])
        result = c.fetchone()
        c.close()

        return result

    def clearAllNotifications(self):
        self._invokeAndBlockForResult(self._clearAllNotifications)
        # no result, but block until operation is done

    def _clearAllNotifications(self):
        c = self.conn.cursor()
        c.execute('DELETE FROM notifications')
        self.conn.commit()
        c.close()


class Source(object):
    def getDataFromExternal(self, date, progress_callback=None):
        """
        Retrieve data from external as a list or iterable. Data may contain both Channel and Program objects.
        The source may choose to ignore the date parameter and return all data available.

        @param date: the date to retrieve the data for
        @param progress_callback:
        @return:
        """
        return None

    def isUpdated(self, channelsLastUpdated, programsLastUpdated):
        today = datetime.datetime.now()
        if channelsLastUpdated is None or channelsLastUpdated.day != today.day:
            return True

        if programsLastUpdated is None or programsLastUpdated.day != today.day:
            return True
        return False

class XMLTVSource(Source):
    PLUGIN_DATA = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ivueguide'))
    KEY = 'xmltv'
    LOGO_SOURCE_IVUE = 0
    LOGO_SOURCE_SUB = 1
    LOGO_SOURCE_CUSTOM = 2

    def __init__(self, addon):
        self.conn = None
        gType = GuideTypes()

        self.needReset = False
        self.fetchError = False
        self.xmltvType = int(addon.getSetting('xmltv.type'))
        self.xmltvInterval = int(addon.getSetting('xmltv.interval'))
        self.logoSource = int(addon.getSetting('logos.source'))

	LOGO_URL = addon.getSetting('logos')

		
        # make sure the folder in the user's profile exists or create it!
        if not os.path.exists(XMLTVSource.PLUGIN_DATA):
            os.makedirs(XMLTVSource.PLUGIN_DATA)

        if self.logoSource == XMLTVSource.LOGO_SOURCE_IVUE:
            self.logoFolder = LOGO_URL
        elif self.logoSource == XMLTVSource.LOGO_SOURCE_SUB:
            self.logoFolder = None
        else:
            self.logoFolder = str(addon.getSetting('logos.folder'))

#Karls changes start
#Karls custom xml import for creator
        

        if self.xmltvType == gType.CUSTOM_FILE_ID:
            if addon.getSetting('custom.xmltv.type') == "0":
            	try:
                    os.remove(current_db)
                except:
                    pass
                xmltvTemp = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ivueguide', 'custom.xml'))
                customXmltv = str(addon.getSetting('xmltv.file'))
                shutil.copy(customXmltv, xmltvTemp)
                self.xmltvFile = str(addon.getSetting('xmltv.file'))# uses local file provided by user!
            else:
                self.xmltvFile = self.updateLocalFile(str(addon.getSetting('xmltv.url')), addon)

        elif self.xmltvType == gType.SUB_FILE_ID and addon.getSetting('sub.xmltv.url') != '':
            self.xmltvFile = self.updateLocalFile(str(addon.getSetting('sub.xmltv.url')), addon)
        else:
            self.xmltvFile = self.updateLocalFile(gType.getGuideDataItem(self.xmltvType, gType.GUIDE_FILE), addon)

        self.xml = open(self.xmltvFile).read()

        if not self.xmltvFile or not xbmcvfs.exists(self.xmltvFile):
            raise SourceNotConfiguredException()

    def updateLocalFile(self, name, addon):
        try:
            os.remove(current_db)
        except:
            pass
        fetcher = FileFetcher(name, addon)
        if name == addon.getSetting('xmltv.url'):
            name = 'custom.xml'
        if name == addon.getSetting('sub.xmltv.url'):
            name = addon.getSetting('sub.xmltv')+'.xml'
        if name == addon.getSetting('xmltv.url') and name.endswith(".zip"):
            name = 'custom.xml'

        path = os.path.join(XMLTVSource.PLUGIN_DATA, name)
        retVal = fetcher.fetchFile()
        if retVal == fetcher.FETCH_OK:
            self.needReset = True
        elif retVal == fetcher.FETCH_ERROR:
            xbmcgui.Dialog().ok(strings(FETCH_ERROR_TITLE), strings(FETCH_ERROR_LINE1), strings(FETCH_ERROR_LINE2))

        return path

    def getDataFromExternal(self, date, progress_callback=None):

        f = FileWrapper(self.xmltvFile)
        context = ElementTree.iterparse(f, events=("start", "end"))
        size = f.size

        return self.parseXMLTV(context, f, size, self.logoFolder, progress_callback)

    def isUpdated(self, channelsLastUpdated, programLastUpdate):
        if channelsLastUpdated is None or not xbmcvfs.exists(self.xmltvFile):
            return True

        stat = xbmcvfs.Stat(self.xmltvFile)
        fileUpdated = datetime.datetime.fromtimestamp(stat.st_mtime())
        return fileUpdated > channelsLastUpdated

    def parseXMLTVDate(self, origDateString):
        if origDateString.find(' ') != -1:
            # get timezone information
            dateParts = origDateString.split()
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

            # normalize the given time to UTC by applying the timedelta provided in the timestamp
            try:
                t_tmp = datetime.datetime.strptime(dateString, '%Y%m%d%H%M%S')
            except TypeError:
                xbmc.log('[script.ivueguide] strptime error with this date: %s' % dateString, xbmc.LOGDEBUG)
                t_tmp = datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString, '%Y%m%d%H%M%S')))
            if offSign == '+':
                t = t_tmp - td
            elif offSign == '-':
                t = t_tmp + td
            else:
                t = t_tmp

            # get the local timezone offset in seconds
            is_dst = time.daylight and time.localtime().tm_isdst > 0
            utc_offset = - (time.altzone if is_dst else time.timezone)
            td_local = datetime.timedelta(seconds=utc_offset)

            t = t + td_local

            return t

        else:
            return None

    def matchCustomStreamUrl(self, channel):
        profilePath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
        if not os.path.exists(profilePath):
            os.makedirs(profilePath)
        self.databasePath = os.path.join(profilePath, Database.SOURCE_DB)
        self.conn = sqlite3.connect(self.databasePath, detect_types=sqlite3.PARSE_DECLTYPES)    	
        c = self.conn.cursor()
        c.execute("SELECT stream_url FROM custom_stream_url WHERE channel=?", [channel])
        stream_url = c.fetchone()
        c.close()

        if stream_url:
            return stream_url[0]
        else:
            return None

    def searchXml(self, item, start, end):
            try: r = re.search("(?i)" + start + "([\S\s]+?)" + end, item).group(1)
            except: r = ''
            return r

    def parseXMLTV(self, context, f, size, logoFolder, progress_callback):
        event, root = context.next()
        elements_parsed = 0
        meta_installed = False

        try:
            xbmcaddon.Addon("plugin.video.meta")
            meta_installed = True
        except Exception:
            pass  # ignore addons that are not installed
        category_count = {}
        for event, elem in context:
            if event == "end":
                result = None
                if elem.tag == "programme":
                    channel = elem.get("channel").replace("'", "")  # Make ID safe to use as ' can cause crashes!
                    date_tag = elem.findtext("date")
                    description = elem.findtext("desc")
                    category = elem.findall("category")
                    iconElement = elem.find("icon")
                    icon = None
                    date = None
                    if iconElement is not None:
                        icon = iconElement.get("src")
                    if not description:
                        description = strings(NO_DESCRIPTION)
                    if date_tag is not None:
                        date = date_tag
                    season = None
                    episode = None
                    is_movie = None
	            if elem.findtext('title') is not None:
                        language = elem.find("title").get("lang")
                    else:
                        language = ""
                    category_list = []
                    for c in category:
                        txt = c.text
                        if txt:
                            if txt in category_count:
                                category_count[txt] = category_count[txt] + 1
                            else:
                                category_count[txt] = 1
                            category_list.append(txt)
                    categories = ','.join(category_list)

                    episode_num = elem.findtext("episode-num")

                    for genre in category:
                        if genre.text and ("movie" in genre.text.lower() or channel.lower().find("sky movies") != -1 \
                                or "film" in genre.text.lower()):
                            is_movie = "Movie"
                            break

                    if episode_num is not None and is_movie is None:
                        episode_num = unicode.encode(unicode(episode_num), 'ascii','ignore')
                        if str.find(episode_num, ".") != -1:
                            splitted = str.split(episode_num, ".")
                            if splitted[0] != "":
                                try:
                                    season = int(splitted[0]) + 1
                                    is_movie = None
                                    if str.find(splitted[1], "/") != -1:
                                        episode = int(splitted[1].split("/")[0]) + 1
                                    elif splitted[1] != "":
                                        episode = int(splitted[1]) + 1
                                except:
                                    episode = ""
                                    season = ""

                        elif str.find(episode_num.lower(), "season") != -1 and episode_num != "Season ,Episode ":
                            pattern = re.compile(r"Season\s(\d+).*?Episode\s+(\d+).*",re.I|re.U)
                            match = re.search(pattern,episode_num)
                            if match:
                                season = int(match.group(1))
                                episode = int(match.group(2))
                        else:
                            pattern = re.compile(r"S([0-9]+)E([0-9]+)",re.I|re.U)
                            match = re.search(pattern,episode_num)
                            if match:
                                season = int(match.group(1))
                                episode = int(match.group(2))

                    result = Program(channel, elem.findtext('title').replace('&amp;','&'), self.parseXMLTVDate(elem.get('start')),
                                     self.parseXMLTVDate(elem.get('stop')), description.replace('&amp;','&'), categories, imageSmall=icon,
                                     season = season, episode = episode, is_movie = is_movie, date = date, language= language)


                elif elem.tag == "channel":
                    weight = -1
                    cid = elem.get("id").replace("'", "")  # Make ID safe to use as ' can cause crashes!
                    title = elem.findtext("display-name").replace('UK: ', '').replace('USA/CA: ', '').replace('USA: ', '').replace('CA: ', '').replace('INT: ', '').replace('ENT: ','').replace('UK:', '').replace('USA/CA:', '').replace('USA:', '').replace('CA:', '').replace('INT:', '').replace('ENT:','').replace('NZ : ','').replace('CA : ','').replace('AU : ','').replace('NZ : ','').replace('UK : ','').replace('USA : ','')

                    logo = None
                    if logoFolder:
                        logoFile = os.path.join(logoFolder, title + '.png')
                        if self.logoSource == XMLTVSource.LOGO_SOURCE_IVUE:
                            logo = logoFile.replace(' ', '%20')  # needed due to fetching from a server!
                        elif xbmcvfs.exists(logoFile):
                            logo = logoFile  # local file instead of remote!
                    else:
                        iconElement = elem.find("icon")
                        if iconElement is not None: 
                            logo = iconElement.get("src")
                        else:
                            logoURL = ADDON.getSetting('logos')
                            logoFile = os.path.join(logoURL, title + '.png')
                            logo = logoFile.replace(' ', '%20')

                    streamElement = self.matchCustomStreamUrl(cid)#elem.find("stream")
                    streamUrl = None
                    if streamElement is not None:
                        streamUrl = str(streamElement)
                    visible = elem.get("visible")
                    if visible == "0":
                        visible = False
                    else:
                        visible = True

                    xmltvType = ADDON.getSetting('xmltv.type_select')
                    if xmltvType == '':
                        xmltvType = 'IVUE (Freeview UK)'
                    elif xmltvType == 'Sub File':
                        xmltvType = ADDON.getSetting('sub.xmltv')
                    xmltvfile = xmltvType + '.ini'
                    inifile = xbmc.translatePath('special://profile/addon_data/script.ivueguide/resources/guide_setups/%s' % xmltvfile)
                    if os.path.exists(inifile):
                        ini = open(inifile, "rb")
                        mysetup= []
                        readini = ini.readlines()
                        for line in readini:
                            mysetup.append(line)
                        getlist = sorted(mysetup)
                        for setup in getlist:
                            if cid == setup.split(' , Visible')[0]:
                                visible = setup.split('Visible = ')[1].split(' , Position')[0]
                                weight = int(setup.split('Position = ')[1])
                                             
                    result = Channel(cid, title, logo, streamUrl, visible, weight)

                if result:
                    elements_parsed += 1
                    if progress_callback and elements_parsed % 500 == 0:
                        if not progress_callback(100.0 / size * f.tell()):
                            raise SourceUpdateCanceledException()
                    yield result

            root.clear()
        f.close()
        if self.conn:
            self.conn.close()

        #f = xbmcvfs.File('special://profile/addon_data/script.ivueguide/program_category.ini',"wb")
        #for c in sorted(category_count):
            #s = "%s=%s\n" % (c, category_count[c])
            #f.write(s.encode("utf8"))
        #f.close()

    def parseXMLTVchannels(self, progress_callback):
        if self.conn:
            self.conn.close()
        #while self.parseXMLTVprograms():
        logoFolder = self.logoFolder
        #dialog = xbmcgui.DialogProgress()
        #dialog.create('iVue TV Guide', "Loading EPG Data")
        weight = -1
        chanList = []
        channels = re.compile('<channel(.+?)</channel>', re.DOTALL).findall(self.xml)
        for channel in channels:
            weight += 1
            cid = self.searchXml(channel, 'id="', '">').replace("'", "")  # Make ID safe to use as ' can cause crashes!
            title = self.searchXml(channel, '<display-name lang=".+?">', '</display-name>')
            logo = None
            if logoFolder:
                logoFile = os.path.join(logoFolder, title + '.png')
                if (self.logoSource == XMLTVSource.LOGO_SOURCE_IVUE) or (self.logoSource == XMLTVSource.LOGO_SOURCE_SUB):
                    logo = logoFile.replace(' ', '%20')  # needed due to fetching from a server!
                elif xbmcvfs.exists(logoFile):
                    logo = logoFile  # local file instead of remote!
            else:
                iconElement = self.searchXml(channel, 'icon src="', '" />')
                if iconElement is not None: 
                    logo = iconElement
                else:
                    logoURL = ADDON.getSetting('logos')
                    logoFile = os.path.join(logoURL, title + '.png')
                    logo = logoFile.replace(' ', '%20')

            streamElement = self.matchCustomStreamUrl(cid.decode("utf8"))#elem.find("stream")
            streamUrl = None
            if streamElement is not None:
                streamUrl = str(streamElement)
            visible = True

            xmltvType = ADDON.getSetting('xmltv.type_select')
            if xmltvType == '':
                xmltvType = 'IVUE (Freeview UK)'
            elif xmltvType == 'Sub File':
                xmltvType = ADDON.getSetting('sub.xmltv')
            xmltvfile = xmltvType + '.ini'
            inifile = xbmc.translatePath('special://profile/addon_data/script.ivueguide/resources/guide_setups/%s' % xmltvfile)
            if os.path.exists(inifile):
                ini = open(inifile, "rb")
                mysetup= []
                readini = ini.readlines()
                for line in readini:
                    mysetup.append(line)
                getlist = sorted(mysetup)
                for setup in getlist:
                    if cid == setup.split(' , Visible')[0]:
                        visible = setup.split('Visible = ')[1].split(' , Position')[0]
                        weight = int(setup.split('Position = ')[1])

            chanList = [str(cid).decode("utf8"), str(title).decode("utf8"), str(logo).decode("utf8"), streamUrl, 'xmltv', visible, weight]
            yield chanList
        if self.conn:
            self.conn.close()

class FileWrapper(object):
    def __init__(self, filename):
        self.vfsfile = xbmcvfs.File(filename)
        self.size = self.vfsfile.size()
        self.bytesRead = 0

    def close(self):
        self.vfsfile.close()

    def read(self, byteCount):
        self.bytesRead += byteCount
        return self.vfsfile.read(byteCount)

    def tell(self):
        return self.bytesRead


def instantiateSource():
    return XMLTVSource(ADDON)
