# -*- coding: utf-8 -*-

'''
    Umpidy Add-on

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


import os,sys,urlparse

from resources.lib.modules import control
from resources.lib.modules import trakt
from resources.lib.modules import cache

sysaddon = sys.argv[0] ; syshandle = int(sys.argv[1]) ; control.moderator()

artPath = control.artPath() ; addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()

traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065).encode('utf-8')


class navigator:
    def root(self):
        self.addDirectoryItem('[B][COLOR gold]• [/COLOR][/B][B][COLOR lime]Umpidy is a COPY & PASTE of NuMbErS Addon[/COLOR][/B][B][COLOR gold] •[/COLOR][/B]',  'movieNavigator',  'fuckoff.gif',  'DefaultFolder.png')
        self.addDirectoryItem('[B][COLOR gold]• [/COLOR][/B][B][COLOR lime]DO NOT SUPPORT PEOPLE SUCH AS GRICE ADVICE[/COLOR][/B][B][COLOR gold] •[/COLOR][/B]',  'movieNavigator',  'fuckoff.gif',  'DefaultFolder.png')
        self.addDirectoryItem(32001, 'movieNavigator', 'fuckoff.gif', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvNavigator', 'fuckoff.gif', 'DefaultTVShows.png')
        if not control.setting('lists.widget') == '0':
            self.addDirectoryItem(32003, 'mymovieNavigator', 'fuckoff.gif', 'DefaultVideoPlaylists.png')
            self.addDirectoryItem(32004, 'mytvNavigator', 'fuckoff.gif', 'DefaultVideoPlaylists.png')
            self.addDirectoryItem(32616, 'tvNetworks', 'fuckoff.gif', 'DefaultTVShows.png')
            self.addDirectoryItem(32617, 'boxsetsNavigator', 'fuckoff.gif', 'grice_advice_is_a_cunt.png')

        self.addDirectoryItem('[B][COLOR forestgreen]• [/COLOR][/B][COLOR ghostwhite]Documentaries[/COLOR]', 'movieNavigator', 'fuckoff.gif', 'DefaultMovies.png')

        self.addDirectoryItem(32008, 'toolNavigator', 'fuckoff.gif', 'DefaultAddonProgram.png')

        downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        if downloads == True:
            self.addDirectoryItem(32009, 'downloadNavigator', 'fuckoff.gif', 'DefaultFolder.png')

        self.addDirectoryItem(32010, 'searchNavigator', 'fuckoff.gif', 'DefaultFolder.png')
        #self.addDirectoryItem('Changelog',  'ShowChangelog',  'fuckoff.gif',  'DefaultFolder.png')		

        self.endDirectory()


    def movies(self, lite=False):
        self.addDirectoryItem(32022, 'movies&url=theaters', 'grice_advice_is_a_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32011, 'movieGenres', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem(32012, 'movieYears', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem(32013, 'moviePersons', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem(32014, 'movieLanguages', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem(32015, 'movieCertificates', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem(32017, 'movies&url=trending', 'grice_advice_is_a_cunt.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32018, 'movies&url=popular', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Romantic Comedy[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=romance', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')	
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Marvel Studios[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=marvel', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')	
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]DC Movies[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=dcmovies', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]DC Animated[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=dcanimate', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Horror 2018-2000[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=tophorr', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Horror 1999-Under[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=horror', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Standup Comedy[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=standup', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')		
        self.addDirectoryItem(32019, 'movies&url=views', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem(32020, 'movies&url=boxoffice', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem(32021, 'movies&url=oscars', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem(32005, 'movieWidget', 'grice_advice_is_a_cunt.png', 'DefaultRecentlyAddedMovies.png')

        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32003, 'mymovieliteNavigator', 'grice_advice_is_a_cunt.png', 'DefaultVideoPlaylists.png')

            self.addDirectoryItem(32028, 'moviePerson', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')

        self.endDirectory()


    def mymovies(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)

        elif traktCredentials == True:
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(32032, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32033, 'movies&url=imdbwatchlist2', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktCredentials == True:
            self.addDirectoryItem(32035, 'movies&url=traktfeatured', 'trakt.png', 'DefaultMovies.png', queue=True)

        elif imdbCredentials == True:
            self.addDirectoryItem(32035, 'movies&url=featured', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)

        self.addDirectoryItem(32039, 'movieUserlists', 'fuckoff.gif', 'DefaultMovies.png')

        if lite == False:
            self.addDirectoryItem(32031, 'movieliteNavigator', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32028, 'moviePerson', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')

        self.endDirectory()


    def tvshows(self, lite=False):
        self.addDirectoryItem(32609, 'tvGenres', 'grice_advice_is_a_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32016, 'tvNetworks', 'grice_advice_is_a_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32610, 'tvLanguages', 'grice_advice_is_a_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32611, 'tvCertificates', 'grice_advice_is_a_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32612, 'tvshows&url=trending', 'grice_advice_is_a_cunt.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(32613, 'tvshows&url=popular', 'grice_advice_is_a_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Marvel TV[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'tvshows&url=marveltv', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem(32023, 'tvshows&url=rating', 'grice_advice_is_a_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32614, 'tvshows&url=views', 'grice_advice_is_a_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32024, 'tvshows&url=airing', 'grice_advice_is_a_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32025, 'tvshows&url=active', 'grice_advice_is_a_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32026, 'tvshows&url=premiere', 'grice_advice_is_a_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32006, 'calendar&url=added', 'grice_advice_is_a_cunt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
        self.addDirectoryItem(32027, 'calendars', 'grice_advice_is_a_cunt.png', 'DefaultRecentlyAddedEpisodes.png')

        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32004, 'mytvliteNavigator', 'grice_advice_is_a_cunt.png', 'DefaultVideoPlaylists.png')

            self.addDirectoryItem(32615, 'tvPerson', 'grice_advice_is_a_cunt.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'grice_advice_is_a_cunt.png', 'DefaultTVShows.png')

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

        self.addDirectoryItem(32040, 'tvUserlists', 'fuckoff.gif', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32041, 'episodeUserlists', 'fuckoff.gif', 'DefaultTVShows.png')

        if lite == False:
            self.addDirectoryItem(32031, 'tvliteNavigator', 'fuckoff.gif', 'DefaultTVShows.png')
            self.addDirectoryItem(32028, 'tvPerson', 'fuckoff.gif', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'fuckoff.gif', 'DefaultTVShows.png')

        self.endDirectory()


    def tools(self):
        self.addDirectoryItem(32043, 'openSettings&query=0.0', 'grice_advice_is_a_cunt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32044, 'openSettings&query=3.1', 'grice_advice_is_a_cunt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32045, 'openSettings&query=1.0', 'grice_advice_is_a_cunt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32046, 'openSettings&query=6.0', 'grice_advice_is_a_cunt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32047, 'openSettings&query=2.0', 'grice_advice_is_a_cunt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32556, 'libraryNavigator', 'grice_advice_is_a_cunt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32048, 'openSettings&query=5.0', 'grice_advice_is_a_cunt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32049, 'viewsNavigator', 'grice_advice_is_a_cunt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32050, 'clearSources', 'grice_advice_is_a_cunt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32604, 'clearCacheSearch', 'grice_advice_is_a_cunt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32052, 'clearCache', 'grice_advice_is_a_cunt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32073, 'authTrakt', 'fuckoff.gif', 'DefaultAddonProgram.png')

        self.endDirectory()

    def library(self):
        self.addDirectoryItem(32557, 'openSettings&query=4.0', 'grice_advice_is_a_cunt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'fuckoff.gif', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32559, control.setting('library.movie'), 'fuckoff.gif', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem(32560, control.setting('library.tv'), 'fuckoff.gif', 'DefaultTVShows.png', isAction=False)

        if trakt.getTraktCredentialsInfo():
            self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'trakt.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png')

        self.endDirectory()

    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')

        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(32001, movie_downloads, 'movies.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(32002, tv_downloads, 'tvshows.png', 'DefaultTVShows.png', isAction=False)

        self.endDirectory()


    def search(self):
        self.addDirectoryItem(32001, 'movieSearch', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvSearch', 'grice_advice_is_a_cunt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32029, 'moviePerson', 'grice_advice_is_a_cunt.png', 'DefaultMovies.png')
        self.addDirectoryItem(32030, 'tvPerson', 'grice_advice_is_a_cunt.png', 'DefaultTVShows.png')

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
        if queue == True: cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if not context == None: cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def getMenuEnabled(self, menu_title):
        is_enabled = control.setting(menu_title).strip()
        if (is_enabled == '' or is_enabled == 'false'): return False
        return True

    def endDirectory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


