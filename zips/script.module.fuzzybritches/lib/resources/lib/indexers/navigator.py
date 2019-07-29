# -*- coding: utf-8 -*-

'''
 ███▄    █  █    ██  ███▄ ▄███▓ ▄▄▄▄   ▓█████  ██▀███    ██████ 
 ██ ▀█   █  ██  ▓██▒▓██▒▀█▀ ██▒▓█████▄ ▓█   ▀ ▓██ ▒ ██▒▒██    ▒ 
▓██  ▀█ ██▒▓██  ▒██░▓██    ▓██░▒██▒ ▄██▒███   ▓██ ░▄█ ▒░ ▓██▄   
▓██▒  ▐▌██▒▓▓█  ░██░▒██    ▒██ ▒██░█▀  ▒▓█  ▄ ▒██▀▀█▄    ▒   ██▒
▒██░   ▓██░▒▒█████▓ ▒██▒   ░██▒░▓█  ▀█▓░▒████▒░██▓ ▒██▒▒██████▒▒
░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░░▒▓███▀▒░░ ▒░ ░░ ▒▓ ░▒▓░▒ ▒▓▒ ▒ ░
░ ░░   ░ ▒░░░▒░ ░ ░ ░  ░      ░▒░▒   ░  ░ ░  ░  ░▒ ░ ▒░░ ░▒  ░ ░
   ░   ░ ░  ░░░ ░ ░ ░      ░    ░    ░    ░     ░░   ░ ░  ░  ░  
         ░    ░            ░    ░         ░  ░   ░           ░  
                                     ░                          

    NuMbErS Add-on

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import os, base64, sys, urllib2, urlparse
import xbmc, xbmcaddon, xbmcgui

from resources.lib.modules import control
from resources.lib.modules import trakt
from resources.lib.modules import cache

sysaddon = sys.argv[0] ; syshandle = int(sys.argv[1]) ; 

artPath = control.artPath() ; addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()

traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065).encode('utf-8')


class navigator:
    def root(self):
        self.addDirectoryItem('[B][COLOR gold]• [/COLOR][/B][B][COLOR lime]Fuzzy Britches is a COPY & PASTE of NuMb3r5 Addon[/COLOR][/B][B][COLOR gold] •[/COLOR][/B]',  'movieNavigator',  'fuckoff.gif',  'DefaultFolder.png')
        self.addDirectoryItem('[B][COLOR gold]• [/COLOR][/B][B][COLOR lime]DO NOT SUPPORT PEOPLE SUCH AS The Papaw[/COLOR][/B][B][COLOR gold] •[/COLOR][/B]',  'movieNavigator',  'fuckoff.gif',  'DefaultFolder.png')
        self.addDirectoryItem(32001, 'movieNavigator', 'ThePapaw_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvNavigator', 'ThePapaw_cunt.png', 'DefaultTVShows.png')
        if not control.setting('lists.widget') == '0':
            #self.addDirectoryItem(32003, 'mymovieNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')
            #self.addDirectoryItem(32004, 'mytvNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')
            self.addDirectoryItem(32711, 'collectionsNavigator', 'ThePapaw_cunt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32708, 'tvNetworks', 'ThePapaw_cunt.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32709, 'boxsetsNavigator', 'ThePapaw_cunt.png', 'ThePapaw_cunt.png')

#        self.addDirectoryItem(32700, 'docuHeaven', 'documentaries.png', 'DefaultMovies.png')

        self.addDirectoryItem(32008, 'toolNavigator', 'ThePapaw_copyandpaste.png', 'DefaultAddonProgram.png')

        downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        if downloads == True:
            self.addDirectoryItem(32009, 'downloadNavigator', 'ThePapaw_copyandpaste.png', 'DefaultFolder.png')

        self.addDirectoryItem(32010, 'searchNavigator', 'fuckoff.gif', 'DefaultFolder.png')
        #self.addDirectoryItem('Changelog',  'ShowChangelog',  'icon.gif',  'DefaultFolder.png')        

        self.endDirectory()


    def movies(self, lite=False):
        self.addDirectoryItem(32022, 'movies&url=theaters', 'ThePapaw_copyandpaste.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32011, 'movieGenres', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png')
        self.addDirectoryItem(32012, 'movieYears', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png')
        self.addDirectoryItem(32013, 'moviePersons', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png')
        self.addDirectoryItem(32014, 'movieLanguages', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png')
        self.addDirectoryItem(32015, 'movieCertificates', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png')
        self.addDirectoryItem(32017, 'movies&url=trending', 'ThePapaw_copyandpaste.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32018, 'movies&url=popular', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Romantic Comedy[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=romance', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png')  
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Marvel Studios[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=marvel', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png') 
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]DC Movies[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=dcmovies', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]DC Animated[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=dcanimate', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Horror 2018-2000[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=tophorr', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Horror 1999-Under[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=horror', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Standup Comedy[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=standup', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png')       
        self.addDirectoryItem(32019, 'movies&url=views', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png')
        self.addDirectoryItem(32020, 'movies&url=boxoffice', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png')
        self.addDirectoryItem(32021, 'movies&url=oscars', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png')
        self.addDirectoryItem(32005, 'movieWidget', 'ThePapaw_copyandpaste.png', 'DefaultRecentlyAddedMovies.png')

        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32003, 'mymovieliteNavigator', 'ThePapaw_copyandpaste.png', 'DefaultVideoPlaylists.png')

            self.addDirectoryItem(32028, 'moviePerson', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'fuckoff.gif', 'DefaultMovies.png')

        self.endDirectory()


    def mymovies(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'movies&url=imdbwatchlist', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png', queue=True)

        elif traktCredentials == True:
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(32032, 'movies&url=imdbwatchlist', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32033, 'movies&url=imdbwatchlist2', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png', queue=True)

        if traktCredentials == True:
            self.addDirectoryItem(32035, 'movies&url=traktfeatured', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png', queue=True)

        elif imdbCredentials == True:
            self.addDirectoryItem(32035, 'movies&url=featured', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(32036, 'movies&url=trakthistory', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png', queue=True)

        self.addDirectoryItem(32039, 'movieUserlists', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png')

        if lite == False:
            self.addDirectoryItem(32031, 'movieliteNavigator', 'ThePapaw_cunt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32028, 'moviePerson', 'ThePapaw_copyandpaste.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'fuckoff.gif', 'DefaultMovies.png')

        self.endDirectory()


    def tvshows(self, lite=False):
        self.addDirectoryItem(32701, 'tvGenres', 'ThePapaw_cunt.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32708, 'tvNetworks', 'networks.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32702, 'tvLanguages', 'ThePapaw_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32703, 'tvCertificates', 'ThePapaw_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32704, 'tvshows&url=trending', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(32705, 'tvshows&url=popular', 'ThePapaw_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32710, 'tvshows&url=marveltv', 'ThePapaw_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem(32023, 'tvshows&url=rating', 'ThePapaw_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32706, 'tvshows&url=views', 'ThePapaw_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32024, 'tvshows&url=airing', 'ThePapaw_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32025, 'tvshows&url=active', 'ThePapaw_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32026, 'tvshows&url=premiere', 'ThePapaw_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32006, 'calendar&url=added', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
        self.addDirectoryItem(32027, 'calendars', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedEpisodes.png')

        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32004, 'mytvliteNavigator', 'ThePapaw_cunt.png', 'DefaultVideoPlaylists.png')

            self.addDirectoryItem(32712, 'tvPerson', 'ThePapaw_cunt.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'fuckoff.gif', 'DefaultTVShows.png')

        self.endDirectory()


    def mytvshows(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')

        elif traktCredentials == True:
            self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(32032, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32033, 'tvshows&url=imdbwatchlist2', 'imdb.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32035, 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')

        elif imdbCredentials == True:
            self.addDirectoryItem(32035, 'tvshows&url=trending', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
            self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
            self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)

        self.addDirectoryItem(32040, 'tvUserlists', 'userlists.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32041, 'episodeUserlists', 'userlists.png', 'DefaultTVShows.png')

        if lite == False:
            self.addDirectoryItem(32031, 'tvliteNavigator', 'ThePapaw_cunt.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32028, 'tvPerson', 'people-search2.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'search2.png', 'DefaultTVShows.png')

        self.endDirectory()


    def tools(self):
        self.addDirectoryItem(32609, 'urlResolverRDTorrent', 'ThePapaw_copyandpaste.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32073, 'authTrakt', 'ThePapaw_cunt.png', 'DefaultAddonProgram.png')
        #self.addDirectoryItem(32640, 'urlResolverRDAuthorize', 'ThePapaw_copyandpaste.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32043, 'openSettings&query=0.0', 'ThePapaw_copyandpaste.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32044, 'openSettings&query=4.1', 'ThePapaw_copyandpaste.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32628, 'openSettings&query=1.0', 'ThePapaw_copyandpaste.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32045, 'openSettings&query=2.0', 'ThePapaw_copyandpaste.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32046, 'openSettings&query=7.0', 'ThePapaw_copyandpaste.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32047, 'openSettings&query=3.0', 'ThePapaw_copyandpaste.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32556, 'libraryNavigator', 'ThePapaw_copyandpaste.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32048, 'openSettings&query=6.0', 'ThePapaw_copyandpaste.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32049, 'viewsNavigator', 'ThePapaw_copyandpaste.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32050, 'clearSources', 'ThePapaw_copyandpaste.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32604, 'clearCacheSearch', 'ThePapaw_copyandpaste.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32052, 'clearCache', 'ThePapaw_copyandpaste.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32614, 'clearMetaCache', 'ThePapaw_copyandpaste.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32613, 'clearAllCache', 'ThePapaw_copyandpaste.png', 'DefaultAddonProgram.png')

        self.endDirectory()

    def library(self):
        self.addDirectoryItem(32557, 'openSettings&query=5.0', 'ThePapaw_copyandpaste.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'ThePapaw_cunt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32559, control.setting('library.movie'), 'ThePapaw_cunt.png', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem(32560, control.setting('library.tv'), 'ThePapaw_cunt.png', 'DefaultTVShows.png', isAction=False)

        if trakt.getTraktCredentialsInfo():
            self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'ThePapaw_cunt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'ThePapaw_cunt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'ThePapaw_cunt.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'ThePapaw_cunt.png', 'DefaultTVShows.png')

        self.endDirectory()

    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')

        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(32001, movie_downloads, 'ThePapaw_cunt.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(32002, tv_downloads, 'ThePapaw_cunt.png', 'DefaultTVShows.png', isAction=False)

        self.endDirectory()


    def search(self):
        self.addDirectoryItem(32001, 'movieSearch', 'fuckoff.gif', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvSearch', 'search2.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32029, 'moviePerson', 'ThePapaw_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem(32030, 'tvPerson', 'ThePapaw_cunt.png', 'DefaultTVShows.png')

        self.endDirectory()

    def views(self):
        try:
            control.idle()

            items = [ (control.lang(32001).encode('utf-8'), 'movies'), (control.lang(32002).encode('utf-8'), 'tvshows'), (control.lang(32054).encode('utf-8'), 'seasons'), (control.lang(32038).encode('utf-8'), 'episodes') ]

            select = control.selectDialog([i[0] for i in items], control.lang(32049).encode('utf-8'))

            if select == -1: return

            content = items[select][1]

            title = control.lang(32059).encode('utf-8')
            url = '%s?action=addView&content=%s' % (sys.argv[0], content)

            poster, banner, fanart = control.addonPoster(), control.addonBanner(), control.addonFanart()

            item = control.item(label=title)
            item.setInfo(type='Video', infoLabels = {'title': title})
            item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'banner': banner})
            item.setProperty('Fanart_Image', fanart)

            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
            control.content(int(sys.argv[1]), content)
            control.directory(int(sys.argv[1]), cacheToDisc=True)

            from resources.lib.modules import views
            views.setView(content, {})
        except:
            return


    def accountCheck(self):
        if traktCredentials == False and imdbCredentials == False:
            control.idle()
            control.infoDialog(control.lang(32042).encode('utf-8'), sound=True, icon='WARNING')
            sys.exit()


    def infoCheck(self, version):
        try:
            control.infoDialog('', control.lang(32074).encode('utf-8'), time=5000, sound=False)
            return '1'
        except:
            return '1'


    def clearCache(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def clearCacheMeta(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_meta()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def clearCacheProviders(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_providers()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def clearCacheSearch(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_search()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def clearCacheAll(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_all()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try: name = control.lang(name).encode('utf-8')
        except: pass
        url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
        thumb = os.path.join(artPath, thumb) if not artPath == None else icon
        cm = []
        cm.append(('Fuzzy Britches Settings', 'RunPlugin(%s?action=openSettings&query=(0,0))' % sysaddon))
        if queue == True: cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if not context == None: cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def collections(self, lite=False):
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Actor Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collectionActors', 'ThePapaw_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Movie Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collectionBoxset', 'ThePapaw_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Kids Collections[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collectionKids', 'ThePapaw_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Marvel Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collections&url=marvelmovies', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]DC Comics Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collections&url=dcmovies', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Superhero Collections[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collectionSuperhero', 'ThePapaw_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Car Movie Collections[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collections&url=carmovies', 'ThePapaw_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Christmas Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collections&url=xmasmovies', 'ThePapaw_cunt.png', 'DefaultMovies.png')
        
        self.endDirectory()

    def collectionActors(self):
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Adam Sandler[/COLOR]', 'collections&url=adamsandler', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Al Pacino[/COLOR]', 'collections&url=alpacino', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Alan Rickman[/COLOR]', 'collections&url=alanrickman', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Anthony Hopkins[/COLOR]', 'collections&url=anthonyhopkins', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Angelina Jolie[/COLOR]', 'collections&url=angelinajolie', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Arnold Schwarzenegger[/COLOR]', 'collections&url=arnoldschwarzenegger', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Charlize Theron[/COLOR]', 'collections&url=charlizetheron', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Clint Eastwood[/COLOR]', 'collections&url=clinteastwood', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Demi Moore[/COLOR]', 'collections&url=demimoore', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Denzel Washington[/COLOR]', 'collections&url=denzelwashington', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Eddie Murphy[/COLOR]', 'collections&url=eddiemurphy', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Elvis Presley[/COLOR]', 'collections&url=elvispresley', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Gene Wilder[/COLOR]', 'collections&url=genewilder', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Gerard Butler[/COLOR]', 'collections&url=gerardbutler', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Goldie Hawn[/COLOR]', 'collections&url=goldiehawn', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Jason Statham[/COLOR]', 'collections&url=jasonstatham', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Jean-Claude Van Damme[/COLOR]', 'collections&url=jeanclaudevandamme', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Jeffrey Dean Morgan[/COLOR]', 'collections&url=jeffreydeanmorgan', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]John Travolta[/COLOR]', 'collections&url=johntravolta', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Johnny Depp[/COLOR]', 'collections&url=johnnydepp', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Julia Roberts[/COLOR]', 'collections&url=juliaroberts', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Kevin Costner[/COLOR]', 'collections&url=kevincostner', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Liam Neeson[/COLOR]', 'collections&url=liamneeson', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Mel Gibson[/COLOR]', 'collections&url=melgibson', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Melissa McCarthy[/COLOR]', 'collections&url=melissamccarthy', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Meryl Streep[/COLOR]', 'collections&url=merylstreep', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Michelle Pfeiffer[/COLOR]', 'collections&url=michellepfeiffer', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Nicolas Cage[/COLOR]', 'collections&url=nicolascage', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Nicole Kidman[/COLOR]', 'collections&url=nicolekidman', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Paul Newman[/COLOR]', 'collections&url=paulnewman', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Reese Witherspoon[/COLOR]', 'collections&url=reesewitherspoon', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Robert De Niro[/COLOR]', 'collections&url=robertdeniro', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Samuel L Jackson[/COLOR]', 'collections&url=samueljackson', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Sean Connery[/COLOR]', 'collections&url=seanconnery', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Scarlett Johansson[/COLOR]', 'collections&url=scarlettjohansson', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Sharon Stone[/COLOR]', 'collections&url=sharonstone', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Sigourney Weaver[/COLOR]', 'collections&url=sigourneyweaver', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Steven Seagal[/COLOR]', 'collections&url=stevenseagal', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Tom Hanks[/COLOR]', 'collections&url=tomhanks', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Vin Diesel[/COLOR]', 'collections&url=vindiesel', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Wesley Snipes[/COLOR]', 'collections&url=wesleysnipes', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Will Smith[/COLOR]', 'collections&url=willsmith', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Winona Ryder[/COLOR]', 'collections&url=winonaryder', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()
    

    def collectionBoxset(self):
        self.addDirectoryItem('48 Hrs. (1982-1990)', 'collections&url=fortyeighthours', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ace Ventura (1994-1995)', 'collections&url=aceventura', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Airplane (1980-1982)', 'collections&url=airplane', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Airport (1970-1979)', 'collections&url=airport', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('American Graffiti (1973-1979)', 'collections&url=americangraffiti', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Anaconda (1997-2004)', 'collections&url=anaconda', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Analyze This (1999-2002)', 'collections&url=analyzethis', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Anchorman (2004-2013)', 'collections&url=anchorman', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Austin Powers (1997-2002)', 'collections&url=austinpowers', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Back to the Future (1985-1990)', 'collections&url=backtothefuture', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bad Boys (1995-2003)', 'collections&url=badboys', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bad Santa (2003-2016)', 'collections&url=badsanta', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Basic Instinct (1992-2006)', 'collections&url=basicinstinct', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Beverly Hills Cop (1984-1994)', 'collections&url=beverlyhillscop', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Big Mommas House (2000-2011)', 'collections&url=bigmommashouse', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Blues Brothers (1980-1998)', 'collections&url=bluesbrothers', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bourne (2002-2016)', 'collections&url=bourne', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bruce Almighty (2003-2007)', 'collections&url=brucealmighty', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Caddyshack (1980-1988)', 'collections&url=caddyshack', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cheaper by the Dozen (2003-2005)', 'collections&url=cheaperbythedozen', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cheech and Chong (1978-1984)', 'collections&url=cheechandchong', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Childs Play (1988-2004)', 'collections&url=childsplay', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('City Slickers (1991-1994)', 'collections&url=cityslickers', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Conan (1982-2011)', 'collections&url=conan', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Crank (2006-2009)', 'collections&url=crank', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Crocodile Dundee (1986-2001)', 'collections&url=crodiledunde', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Da Vinci Code (2006-2017)', 'collections&url=davincicode', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Daddy Day Care (2003-2007)', 'collections&url=daddydaycare', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Death Wish (1974-1994)', 'collections&url=deathwish', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Delta Force (1986-1990)', 'collections&url=deltaforce', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Die Hard (1988-2013)', 'collections&url=diehard', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dirty Dancing (1987-2004)', 'collections&url=dirtydancing', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dirty Harry (1971-1988)', 'collections&url=dirtyharry', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dumb and Dumber (1994-2014)', 'collections&url=dumbanddumber', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Escape from New York (1981-1996)', 'collections&url=escapefromnewyork', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Every Which Way But Loose (1978-1980)', 'collections&url=everywhichwaybutloose', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Exorcist (1973-2005)', 'collections&url=exorcist', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Expendables (2010-2014)', 'collections&url=theexpendables', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fast and the Furious (2001-2017)', 'collections&url=fastandthefurious', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Father of the Bride (1991-1995)', 'collections&url=fatherofthebride', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fletch (1985-1989)', 'collections&url=fletch', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Friday (1995-2002)', 'collections&url=friday', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Friday the 13th (1980-2009)', 'collections&url=fridaythe13th', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fugitive (1993-1998)', 'collections&url=fugitive', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('G.I. Joe (2009-2013)', 'collections&url=gijoe', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Get Shorty (1995-2005)', 'collections&url=getshorty', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gettysburg (1993-2003)', 'collections&url=gettysburg', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ghost Rider (2007-2011)', 'collections&url=ghostrider', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ghostbusters (1984-2016)', 'collections&url=ghostbusters', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gods Not Dead (2014-2016)', 'collections&url=godsnotdead', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Godfather (1972-1990)', 'collections&url=godfather', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Godzilla (1956-2016)', 'collections&url=godzilla', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Grown Ups (2010-2013)', 'collections&url=grownups', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Grumpy Old Men (2010-2013)', 'collections&url=grumpyoldmen', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Guns of Navarone (1961-1978)', 'collections&url=gunsofnavarone', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Halloween (1978-2009)', 'collections&url=halloween', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hangover (2009-2013)', 'collections&url=hangover', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hannibal Lector (1986-2007)', 'collections&url=hanniballector', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hellraiser (1987-1996)', 'collections&url=hellraiser', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Honey I Shrunk the Kids (1989-1995)', 'collections&url=honeyishrunkthekids', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Horrible Bosses (2011-2014)', 'collections&url=horriblebosses', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hostel (2005-2011)', 'collections&url=hostel', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hot Shots (1991-1996)', 'collections&url=hotshots', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Independence Day (1996-2016)', 'collections&url=independenceday', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Indiana Jones (1981-2008)', 'collections&url=indianajones', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Insidious (2010-2015)', 'collections&url=insidious', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Iron Eagle (1986-1992)', 'collections&url=ironeagle', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jack Reacher (2012-2016)', 'collections&url=jackreacher', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jack Ryan (1990-2014)', 'collections&url=jackryan', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jackass (2002-2013)', 'collections&url=jackass', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('James Bond (1963-2015)', 'collections&url=jamesbond', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jaws (1975-1987)', 'collections&url=jaws', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jeepers Creepers (2001-2017)', 'collections&url=jeeperscreepers', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('John Wick (2014-2017)', 'collections&url=johnwick', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jumanji (1995-2005)', 'collections&url=jumanji', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jurassic Park (1993-2015)', 'collections&url=jurassicpark', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kick-Ass (2010-2013)', 'collections&url=kickass', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kill Bill (2003-2004)', 'collections&url=killbill', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('King Kong (1933-2016)', 'collections&url=kingkong', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lara Croft (2001-2003)', 'collections&url=laracroft', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Legally Blonde (2001-2003)', 'collections&url=legallyblonde', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lethal Weapon (1987-1998)', 'collections&url=leathalweapon', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Look Whos Talking (1989-1993)', 'collections&url=lookwhostalking', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Machete (2010-2013)', 'collections&url=machete', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Magic Mike (2012-2015)', 'collections&url=magicmike', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Major League (1989-1998)', 'collections&url=majorleague', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Man from Snowy River (1982-1988)', 'collections&url=manfromsnowyriver', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mask (1994-2005)', 'collections&url=mask', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Matrix (1999-2003)', 'collections&url=matrix', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Mechanic (2011-2016)', 'collections&url=themechanic', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Meet the Parents (2000-2010)', 'collections&url=meettheparents', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Men in Black (1997-2012)', 'collections&url=meninblack', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mighty Ducks (1995-1996)', 'collections&url=mightyducks', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Miss Congeniality (2000-2005)', 'collections&url=misscongeniality', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Missing in Action (1984-1988)', 'collections&url=missinginaction', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mission Impossible (1996-2015)', 'collections&url=missionimpossible', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Naked Gun (1988-1994)', 'collections&url=nakedgun', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('National Lampoon (1978-2006)', 'collections&url=nationallampoon', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('National Lampoons Vacation (1983-2015)', 'collections&url=nationallampoonsvacation', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('National Treasure (2004-2007)', 'collections&url=nationaltreasure', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Neighbors (2014-2016)', 'collections&url=neighbors', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Night at the Museum (2006-2014)', 'collections&url=nightatthemuseum', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Nightmare on Elm Street (1984-2010)', 'collections&url=nightmareonelmstreet', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Now You See Me (2013-2016)', 'collections&url=nowyouseeme', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Nutty Professor (1996-2000)', 'collections&url=nuttyprofessor', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Oceans Eleven (2001-2007)', 'collections&url=oceanseleven', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Odd Couple (1968-1998)', 'collections&url=oddcouple', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Oh, God (1977-1984)', 'collections&url=ohgod', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Olympus Has Fallen (2013-2016)', 'collections&url=olympushasfallen', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Omen (1976-1981)', 'collections&url=omen', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Paul Blart Mall Cop (2009-2015)', 'collections&url=paulblart', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Pirates of the Caribbean (2003-2017)', 'collections&url=piratesofthecaribbean', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Planet of the Apes (1968-2014)', 'collections&url=planetoftheapes', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Police Academy (1984-1994)', 'collections&url=policeacademy', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Poltergeist (1982-1988)', 'collections&url=postergeist', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Porkys (1981-1985)', 'collections&url=porkys', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Predator (1987-2010)', 'collections&url=predator', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Purge (2013-2016)', 'collections&url=thepurge', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rambo (1982-2008)', 'collections&url=rambo', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('RED (2010-2013)', 'collections&url=red', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Revenge of the Nerds (1984-1987)', 'collections&url=revengeofthenerds', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Riddick (2000-2013)', 'collections&url=riddick', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ride Along (2014-2016)', 'collections&url=ridealong', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Ring (2002-2017)', 'collections&url=thering', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('RoboCop (1987-1993)', 'collections&url=robocop', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rocky (1976-2015)', 'collections&url=rocky', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Romancing the Stone (1984-1985)', 'collections&url=romancingthestone', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rush Hour (1998-2007)', 'collections&url=rushhour', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Santa Clause (1994-2006)', 'collections&url=santaclause', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Saw (2004-2010)', 'collections&url=saw', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sex and the City (2008-2010)', 'collections&url=sexandthecity', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Shaft (1971-2000)', 'collections&url=shaft', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Shanghai Noon (2000-2003)', 'collections&url=shanghainoon', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sin City (2005-2014)', 'collections&url=sincity', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sinister (2012-2015)', 'collections&url=sinister', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sister Act (1995-1993)', 'collections&url=sisteract', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Smokey and the Bandit (1977-1986)', 'collections&url=smokeyandthebandit', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Speed (1994-1997)', 'collections&url=speed', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Stakeout (1987-1993)', 'collections&url=stakeout', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Star Trek (1979-2016)', 'collections&url=startrek', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Star Wars (1977-2015)', 'collections&url=starwars', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Sting (1973-1983)', 'collections&url=thesting', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Taken (2008-2014)', 'collections&url=taken', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Taxi (1998-2007)', 'collections&url=taxi', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ted (2012-2015)', 'collections&url=ted', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Teen Wolf (1985-1987)', 'collections&url=teenwolf', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Terminator (1984-2015)', 'collections&url=terminator', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Terms of Endearment (1983-1996)', 'collections&url=termsofendearment', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Texas Chainsaw Massacre (1974-2013)', 'collections&url=texaschainsawmassacre', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Thing (1982-2011)', 'collections&url=thething', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Thomas Crown Affair (1968-1999)', 'collections&url=thomascrownaffair', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Transporter (2002-2015)', 'collections&url=transporter', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Under Siege (1992-1995)', 'collections&url=undersiege', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Universal Soldier (1992-2012)', 'collections&url=universalsoldier', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Wall Street (1987-2010)', 'collections&url=wallstreet', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Waynes World (1992-1993)', 'collections&url=waynesworld', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Weekend at Bernies (1989-1993)', 'collections&url=weekendatbernies', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Whole Nine Yards (2000-2004)', 'collections&url=wholenineyards', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('X-Files (1998-2008)', 'collections&url=xfiles', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('xXx (2002-2005)', 'collections&url=xxx', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Young Guns (1988-1990)', 'collections&url=youngguns', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Zoolander (2001-2016)', 'collections&url=zoolander', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Zorro (1998-2005)', 'collections&url=zorro', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()


    def collectionKids(self):
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Disney Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collections&url=disneymovies', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Kids Boxset Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collectionBoxsetKids', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Kids Movie Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collections&url=kidsmovies', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()
        

    def collectionBoxsetKids(self):
        self.addDirectoryItem('101 Dalmations (1961-2003)', 'collections&url=onehundredonedalmations', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Addams Family (1991-1998)', 'collections&url=addamsfamily', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Aladdin (1992-1996)', 'collections&url=aladdin', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Alvin and the Chipmunks (2007-2015)', 'collections&url=alvinandthechipmunks', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Atlantis (2001-2003)', 'collections&url=atlantis', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Babe (1995-1998)', 'collections&url=babe', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Balto (1995-1998)', 'collections&url=balto', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bambi (1942-2006)', 'collections&url=bambi', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Beauty and the Beast (1991-2017)', 'collections&url=beautyandthebeast', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Beethoven (1992-2014)', 'collections&url=beethoven', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Brother Bear (2003-2006)', 'collections&url=brotherbear', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cars (2006-2017)', 'collections&url=cars', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cinderella (1950-2007)', 'collections&url=cinderella', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cloudy With a Chance of Meatballs (2009-2013)', 'collections&url=cloudywithachanceofmeatballs', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Despicable Me (2010-2015)', 'collections&url=despicableme', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Finding Nemo (2003-2016)', 'collections&url=findingnemo', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fox and the Hound (1981-2006)', 'collections&url=foxandthehound', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Free Willy (1993-2010)', 'collections&url=freewilly', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ghostbusters (1984-2016)', 'collections&url=ghostbusters', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gremlins (1984-2016)', 'collections&url=gremlins', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Happy Feet (2006-2011)', 'collections&url=happyfeet', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Harry Potter (2001-2011)', 'collections&url=harrypotter', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Home Alone (1990-2012)', 'collections&url=homealone', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Homeward Bound (1993-1996)', 'collections&url=homewardbound', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Honey, I Shrunk the Kids (1989-1997)', 'collections&url=honeyishrunkthekids', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hotel Transylvania (2012-2015)', 'collections&url=hoteltransylvania', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('How to Train Your Dragon (2010-2014)', 'collections&url=howtotrainyourdragon', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hunchback of Notre Dame (1996-2002)', 'collections&url=hunchbackofnotredame', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ice Age (2002-2016)', 'collections&url=iceage', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jurassic Park (1993-2015)', 'collections&url=jurassicpark', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kung Fu Panda (2008-2016)', 'collections&url=kungfupanda', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lady and the Tramp (1955-2001)', 'collections&url=ladyandthetramp', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lilo and Stitch (2002-2006)', 'collections&url=liloandstitch', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Madagascar (2005-2014)', 'collections&url=madagascar', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Monsters Inc (2001-2013)', 'collections&url=monstersinc', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mulan (1998-2004)', 'collections&url=mulan', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Narnia (2005-2010)', 'collections&url=narnia', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('New Groove (2000-2005)', 'collections&url=newgroove', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Open Season (2006-2015)', 'collections&url=openseason', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Planes (2013-2014)', 'collections&url=planes', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Pocahontas (1995-1998)', 'collections&url=pocahontas', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Problem Child (1990-1995)', 'collections&url=problemchild', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rio (2011-2014)', 'collections&url=rio', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sammys Adventures (2010-2012)', 'collections&url=sammysadventures', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Scooby-Doo (2002-2014)', 'collections&url=scoobydoo', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Short Circuit (1986-1988)', 'collections&url=shortcircuit', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Shrek (2001-2011)', 'collections&url=shrek', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('SpongeBob SquarePants (2004-2017)', 'collections&url=spongebobsquarepants', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Spy Kids (2001-2011)', 'collections&url=spykids', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Star Wars (1977-2015)', 'collections&url=starwars', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Stuart Little (1999-2002)', 'collections&url=stuartlittle', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tarzan (1999-2016)', 'collections&url=tarzan', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Teenage Mutant Ninja Turtles (1978-2009)', 'collections&url=teenagemutantninjaturtles', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Jungle Book (1967-2003)', 'collections&url=thejunglebook', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Karate Kid (1984-2010)', 'collections&url=thekaratekid', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Lion King (1994-2016)', 'collections&url=thelionking', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Little Mermaid (1989-1995)', 'collections&url=thelittlemermaid', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Neverending Story (1984-1994)', 'collections&url=theneverendingstory', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Smurfs (2011-2013)', 'collections&url=thesmurfs', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tooth Fairy (2010-2012)', 'collections&url=toothfairy', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tinker Bell (2008-2014)', 'collections&url=tinkerbell', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tom and Jerry (1992-2013)', 'collections&url=tomandjerry', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Toy Story (1995-2014)', 'collections&url=toystory', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('VeggieTales (2002-2008)', 'collections&url=veggietales', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Winnie the Pooh (2000-2005)', 'collections&url=winniethepooh', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Wizard of Oz (1939-2013)', 'collections&url=wizardofoz', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()


    def collectionSuperhero(self):
        self.addDirectoryItem('Avengers (2008-2017)', 'collections&url=avengers', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Batman (1989-2016)', 'collections&url=batman', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Captain America (2011-2016)', 'collections&url=captainamerica', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dark Knight Trilogy (2005-2013)', 'collections&url=darkknight', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fantastic Four (2005-2015)', 'collections&url=fantasticfour', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hulk (2003-2008)', 'collections&url=hulk', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Iron Man (2008-2013)', 'collections&url=ironman', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Spider-Man (2002-2017)', 'collections&url=spiderman', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Superman (1978-2016)', 'collections&url=superman', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('X-Men (2000-2016)', 'collections&url=xmen', 'ThePapaw_cunt.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()
            

    def endDirectory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


