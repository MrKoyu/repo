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

    NuMb3r5 Add-on

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
        self.addDirectoryItem('[B][COLOR white]• [/COLOR][/B][B][COLOR white]NuMb3r5[/COLOR][/B][B][COLOR white] •[/COLOR][/B]',  'ShowChangelog',  'icon.png',  'DefaultFolder.png')
        self.addDirectoryItem(32001, 'movieNavigator', 'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvNavigator', 'tvshows.png', 'DefaultTVShows.png')
        if not control.setting('lists.widget') == '0':
            #self.addDirectoryItem(32003, 'mymovieNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')
            #self.addDirectoryItem(32004, 'mytvNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')
            self.addDirectoryItem(32711, 'collectionsNavigator', 'collections.png', 'DefaultMovies.png')
            self.addDirectoryItem(32708, 'tvNetworks', 'networks.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32709, 'boxsetsNavigator', 'boxsets1.png', 'boxsets1.png')

        self.addDirectoryItem(32700, 'docuHeaven', 'documentaries.png', 'DefaultMovies.png')

        self.addDirectoryItem(32008, 'toolNavigator', 'tools.png', 'DefaultAddonProgram.png')

        downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        if downloads == True:
            self.addDirectoryItem(32009, 'downloadNavigator', 'downloads.png', 'DefaultFolder.png')

        self.addDirectoryItem(32010, 'searchNavigator', 'search.png', 'DefaultFolder.png')
        #self.addDirectoryItem('Changelog',  'ShowChangelog',  'icon.gif',  'DefaultFolder.png')        

        self.endDirectory()


    def movies(self, lite=False):
        self.addDirectoryItem(32022, 'movies&url=theaters', 'in-theaters.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32011, 'movieGenres', 'genres.png', 'DefaultMovies.png')
        self.addDirectoryItem(32012, 'movieYears', 'years.png', 'DefaultMovies.png')
        self.addDirectoryItem(32013, 'moviePersons', 'people.png', 'DefaultMovies.png')
        self.addDirectoryItem(32014, 'movieLanguages', 'international.png', 'DefaultMovies.png')
        #self.addDirectoryItem(32015, 'movieCertificates', 'certificates.png', 'DefaultMovies.png')
        self.addDirectoryItem(32017, 'movies&url=trending', 'people-watching.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32018, 'movies&url=popular', 'most-popular.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Romantic Comedy[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=romance', 'romance.png', 'DefaultMovies.png')  
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Marvel Studios[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=marvel', 'marvel_studios.png', 'DefaultMovies.png') 
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]DC Movies[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=dcmovies', 'dc2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]DC Animated[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=dcanimate', 'dc.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Horror 2018-2000[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=tophorr', 'horror.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Horror 1999-Under[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=horror', 'horror2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Standup Comedy[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'movies&url=standup', 'standup.png', 'DefaultMovies.png')       
        self.addDirectoryItem(32019, 'movies&url=views', 'most-voted.png', 'DefaultMovies.png')
        self.addDirectoryItem(32020, 'movies&url=boxoffice', 'box-office.png', 'DefaultMovies.png')
        self.addDirectoryItem(32021, 'movies&url=oscars', 'oscar-winners.png', 'DefaultMovies.png')
        self.addDirectoryItem(32005, 'movieWidget', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')

        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32003, 'mymovieliteNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')

            self.addDirectoryItem(32028, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')

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

        self.addDirectoryItem(32039, 'movieUserlists', 'userlists.png', 'DefaultMovies.png')

        if lite == False:
            self.addDirectoryItem(32031, 'movieliteNavigator', 'movies.png', 'DefaultMovies.png')
            self.addDirectoryItem(32028, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')

        self.endDirectory()


    def tvshows(self, lite=False):
        self.addDirectoryItem(32701, 'tvGenres', 'genres2.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32708, 'tvNetworks', 'networks.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32702, 'tvLanguages', 'international2.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32703, 'tvCertificates', 'certificates2.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32704, 'tvshows&url=trending', 'people-watching2.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(32705, 'tvshows&url=popular', 'most-popular2.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32710, 'tvshows&url=marveltv', 'marvel_tv.png', 'DefaultMovies.png')
        self.addDirectoryItem(32023, 'tvshows&url=rating', 'highly-rated.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32706, 'tvshows&url=views', 'most-voted2.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32024, 'tvshows&url=airing', 'airing-today.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32025, 'tvshows&url=active', 'returning-tvshows.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32026, 'tvshows&url=premiere', 'new-tvshows.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32006, 'calendar&url=added', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
        self.addDirectoryItem(32027, 'calendars', 'calendar2.png', 'DefaultRecentlyAddedEpisodes.png')

        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32004, 'mytvliteNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')

            self.addDirectoryItem(32712, 'tvPerson', 'people-search2.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'search2.png', 'DefaultTVShows.png')

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
            self.addDirectoryItem(32031, 'tvliteNavigator', 'tvshows.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32028, 'tvPerson', 'people-search2.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'search2.png', 'DefaultTVShows.png')

        self.endDirectory()


    def tools(self):
        self.addDirectoryItem(32609, 'urlResolverRDTorrent', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32073, 'authTrakt', 'trakt.png', 'DefaultAddonProgram.png')
        #self.addDirectoryItem(32640, 'urlResolverRDAuthorize', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32043, 'openSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32044, 'openSettings&query=4.1', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32628, 'openSettings&query=1.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32045, 'openSettings&query=2.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32046, 'openSettings&query=7.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32047, 'openSettings&query=3.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32556, 'libraryNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32048, 'openSettings&query=6.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32049, 'viewsNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32050, 'clearSources', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32604, 'clearCacheSearch', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32052, 'clearCache', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32614, 'clearMetaCache', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32613, 'clearAllCache', 'tools.png', 'DefaultAddonProgram.png')

        self.endDirectory()

    def library(self):
        self.addDirectoryItem(32557, 'openSettings&query=5.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'library_update.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32559, control.setting('library.movie'), 'movies.png', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem(32560, control.setting('library.tv'), 'tvshows.png', 'DefaultTVShows.png', isAction=False)

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
        self.addDirectoryItem(32001, 'movieSearch', 'search.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvSearch', 'search2.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32029, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
        self.addDirectoryItem(32030, 'tvPerson', 'people-search2.png', 'DefaultTVShows.png')

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

    def collections(self, lite=False):
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Actor Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collectionActors', 'collections.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Movie Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collectionBoxset', 'collections.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Kids Collections[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collectionKids', 'collections.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Marvel Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collections&url=marvelmovies', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]DC Comics Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collections&url=dcmovies', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Superhero Collections[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collectionSuperhero', 'collections.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Car Movie Collections[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collections&url=carmovies', 'collections.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Christmas Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collections&url=xmasmovies', 'collections.png', 'DefaultMovies.png')
        
        self.endDirectory()

    def collectionActors(self):
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Adam Sandler[/COLOR]', 'collections&url=adamsandler', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Al Pacino[/COLOR]', 'collections&url=alpacino', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Alan Rickman[/COLOR]', 'collections&url=alanrickman', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Anthony Hopkins[/COLOR]', 'collections&url=anthonyhopkins', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Angelina Jolie[/COLOR]', 'collections&url=angelinajolie', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Arnold Schwarzenegger[/COLOR]', 'collections&url=arnoldschwarzenegger', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Charlize Theron[/COLOR]', 'collections&url=charlizetheron', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Clint Eastwood[/COLOR]', 'collections&url=clinteastwood', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Demi Moore[/COLOR]', 'collections&url=demimoore', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Denzel Washington[/COLOR]', 'collections&url=denzelwashington', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Eddie Murphy[/COLOR]', 'collections&url=eddiemurphy', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Elvis Presley[/COLOR]', 'collections&url=elvispresley', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Gene Wilder[/COLOR]', 'collections&url=genewilder', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Gerard Butler[/COLOR]', 'collections&url=gerardbutler', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Goldie Hawn[/COLOR]', 'collections&url=goldiehawn', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Jason Statham[/COLOR]', 'collections&url=jasonstatham', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Jean-Claude Van Damme[/COLOR]', 'collections&url=jeanclaudevandamme', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Jeffrey Dean Morgan[/COLOR]', 'collections&url=jeffreydeanmorgan', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]John Travolta[/COLOR]', 'collections&url=johntravolta', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Johnny Depp[/COLOR]', 'collections&url=johnnydepp', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Julia Roberts[/COLOR]', 'collections&url=juliaroberts', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Kevin Costner[/COLOR]', 'collections&url=kevincostner', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Liam Neeson[/COLOR]', 'collections&url=liamneeson', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Mel Gibson[/COLOR]', 'collections&url=melgibson', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Melissa McCarthy[/COLOR]', 'collections&url=melissamccarthy', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Meryl Streep[/COLOR]', 'collections&url=merylstreep', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Michelle Pfeiffer[/COLOR]', 'collections&url=michellepfeiffer', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Nicolas Cage[/COLOR]', 'collections&url=nicolascage', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Nicole Kidman[/COLOR]', 'collections&url=nicolekidman', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Paul Newman[/COLOR]', 'collections&url=paulnewman', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Reese Witherspoon[/COLOR]', 'collections&url=reesewitherspoon', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Robert De Niro[/COLOR]', 'collections&url=robertdeniro', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Samuel L Jackson[/COLOR]', 'collections&url=samueljackson', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Sean Connery[/COLOR]', 'collections&url=seanconnery', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Scarlett Johansson[/COLOR]', 'collections&url=scarlettjohansson', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Sharon Stone[/COLOR]', 'collections&url=sharonstone', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Sigourney Weaver[/COLOR]', 'collections&url=sigourneyweaver', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Steven Seagal[/COLOR]', 'collections&url=stevenseagal', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Tom Hanks[/COLOR]', 'collections&url=tomhanks', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Vin Diesel[/COLOR]', 'collections&url=vindiesel', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Wesley Snipes[/COLOR]', 'collections&url=wesleysnipes', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Will Smith[/COLOR]', 'collections&url=willsmith', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Winona Ryder[/COLOR]', 'collections&url=winonaryder', 'collections.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()
    

    def collectionBoxset(self):
        self.addDirectoryItem('48 Hrs. (1982-1990)', 'collections&url=fortyeighthours', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ace Ventura (1994-1995)', 'collections&url=aceventura', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Airplane (1980-1982)', 'collections&url=airplane', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Airport (1970-1979)', 'collections&url=airport', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('American Graffiti (1973-1979)', 'collections&url=americangraffiti', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Anaconda (1997-2004)', 'collections&url=anaconda', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Analyze This (1999-2002)', 'collections&url=analyzethis', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Anchorman (2004-2013)', 'collections&url=anchorman', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Austin Powers (1997-2002)', 'collections&url=austinpowers', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Back to the Future (1985-1990)', 'collections&url=backtothefuture', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bad Boys (1995-2003)', 'collections&url=badboys', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bad Santa (2003-2016)', 'collections&url=badsanta', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Basic Instinct (1992-2006)', 'collections&url=basicinstinct', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Beverly Hills Cop (1984-1994)', 'collections&url=beverlyhillscop', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Big Mommas House (2000-2011)', 'collections&url=bigmommashouse', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Blues Brothers (1980-1998)', 'collections&url=bluesbrothers', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bourne (2002-2016)', 'collections&url=bourne', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bruce Almighty (2003-2007)', 'collections&url=brucealmighty', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Caddyshack (1980-1988)', 'collections&url=caddyshack', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cheaper by the Dozen (2003-2005)', 'collections&url=cheaperbythedozen', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cheech and Chong (1978-1984)', 'collections&url=cheechandchong', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Childs Play (1988-2004)', 'collections&url=childsplay', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('City Slickers (1991-1994)', 'collections&url=cityslickers', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Conan (1982-2011)', 'collections&url=conan', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Crank (2006-2009)', 'collections&url=crank', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Crocodile Dundee (1986-2001)', 'collections&url=crodiledunde', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Da Vinci Code (2006-2017)', 'collections&url=davincicode', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Daddy Day Care (2003-2007)', 'collections&url=daddydaycare', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Death Wish (1974-1994)', 'collections&url=deathwish', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Delta Force (1986-1990)', 'collections&url=deltaforce', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Die Hard (1988-2013)', 'collections&url=diehard', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dirty Dancing (1987-2004)', 'collections&url=dirtydancing', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dirty Harry (1971-1988)', 'collections&url=dirtyharry', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dumb and Dumber (1994-2014)', 'collections&url=dumbanddumber', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Escape from New York (1981-1996)', 'collections&url=escapefromnewyork', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Every Which Way But Loose (1978-1980)', 'collections&url=everywhichwaybutloose', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Exorcist (1973-2005)', 'collections&url=exorcist', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Expendables (2010-2014)', 'collections&url=theexpendables', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fast and the Furious (2001-2017)', 'collections&url=fastandthefurious', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Father of the Bride (1991-1995)', 'collections&url=fatherofthebride', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fletch (1985-1989)', 'collections&url=fletch', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Friday (1995-2002)', 'collections&url=friday', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Friday the 13th (1980-2009)', 'collections&url=fridaythe13th', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fugitive (1993-1998)', 'collections&url=fugitive', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('G.I. Joe (2009-2013)', 'collections&url=gijoe', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Get Shorty (1995-2005)', 'collections&url=getshorty', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gettysburg (1993-2003)', 'collections&url=gettysburg', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ghost Rider (2007-2011)', 'collections&url=ghostrider', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ghostbusters (1984-2016)', 'collections&url=ghostbusters', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gods Not Dead (2014-2016)', 'collections&url=godsnotdead', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Godfather (1972-1990)', 'collections&url=godfather', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Godzilla (1956-2016)', 'collections&url=godzilla', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Grown Ups (2010-2013)', 'collections&url=grownups', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Grumpy Old Men (2010-2013)', 'collections&url=grumpyoldmen', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Guns of Navarone (1961-1978)', 'collections&url=gunsofnavarone', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Halloween (1978-2009)', 'collections&url=halloween', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hangover (2009-2013)', 'collections&url=hangover', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hannibal Lector (1986-2007)', 'collections&url=hanniballector', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hellraiser (1987-1996)', 'collections&url=hellraiser', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Honey I Shrunk the Kids (1989-1995)', 'collections&url=honeyishrunkthekids', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Horrible Bosses (2011-2014)', 'collections&url=horriblebosses', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hostel (2005-2011)', 'collections&url=hostel', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hot Shots (1991-1996)', 'collections&url=hotshots', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Independence Day (1996-2016)', 'collections&url=independenceday', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Indiana Jones (1981-2008)', 'collections&url=indianajones', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Insidious (2010-2015)', 'collections&url=insidious', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Iron Eagle (1986-1992)', 'collections&url=ironeagle', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jack Reacher (2012-2016)', 'collections&url=jackreacher', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jack Ryan (1990-2014)', 'collections&url=jackryan', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jackass (2002-2013)', 'collections&url=jackass', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('James Bond (1963-2015)', 'collections&url=jamesbond', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jaws (1975-1987)', 'collections&url=jaws', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jeepers Creepers (2001-2017)', 'collections&url=jeeperscreepers', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('John Wick (2014-2017)', 'collections&url=johnwick', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jumanji (1995-2005)', 'collections&url=jumanji', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jurassic Park (1993-2015)', 'collections&url=jurassicpark', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kick-Ass (2010-2013)', 'collections&url=kickass', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kill Bill (2003-2004)', 'collections&url=killbill', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('King Kong (1933-2016)', 'collections&url=kingkong', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lara Croft (2001-2003)', 'collections&url=laracroft', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Legally Blonde (2001-2003)', 'collections&url=legallyblonde', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lethal Weapon (1987-1998)', 'collections&url=leathalweapon', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Look Whos Talking (1989-1993)', 'collections&url=lookwhostalking', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Machete (2010-2013)', 'collections&url=machete', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Magic Mike (2012-2015)', 'collections&url=magicmike', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Major League (1989-1998)', 'collections&url=majorleague', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Man from Snowy River (1982-1988)', 'collections&url=manfromsnowyriver', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mask (1994-2005)', 'collections&url=mask', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Matrix (1999-2003)', 'collections&url=matrix', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Mechanic (2011-2016)', 'collections&url=themechanic', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Meet the Parents (2000-2010)', 'collections&url=meettheparents', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Men in Black (1997-2012)', 'collections&url=meninblack', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mighty Ducks (1995-1996)', 'collections&url=mightyducks', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Miss Congeniality (2000-2005)', 'collections&url=misscongeniality', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Missing in Action (1984-1988)', 'collections&url=missinginaction', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mission Impossible (1996-2015)', 'collections&url=missionimpossible', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Naked Gun (1988-1994)', 'collections&url=nakedgun', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('National Lampoon (1978-2006)', 'collections&url=nationallampoon', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('National Lampoons Vacation (1983-2015)', 'collections&url=nationallampoonsvacation', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('National Treasure (2004-2007)', 'collections&url=nationaltreasure', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Neighbors (2014-2016)', 'collections&url=neighbors', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Night at the Museum (2006-2014)', 'collections&url=nightatthemuseum', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Nightmare on Elm Street (1984-2010)', 'collections&url=nightmareonelmstreet', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Now You See Me (2013-2016)', 'collections&url=nowyouseeme', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Nutty Professor (1996-2000)', 'collections&url=nuttyprofessor', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Oceans Eleven (2001-2007)', 'collections&url=oceanseleven', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Odd Couple (1968-1998)', 'collections&url=oddcouple', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Oh, God (1977-1984)', 'collections&url=ohgod', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Olympus Has Fallen (2013-2016)', 'collections&url=olympushasfallen', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Omen (1976-1981)', 'collections&url=omen', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Paul Blart Mall Cop (2009-2015)', 'collections&url=paulblart', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Pirates of the Caribbean (2003-2017)', 'collections&url=piratesofthecaribbean', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Planet of the Apes (1968-2014)', 'collections&url=planetoftheapes', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Police Academy (1984-1994)', 'collections&url=policeacademy', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Poltergeist (1982-1988)', 'collections&url=postergeist', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Porkys (1981-1985)', 'collections&url=porkys', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Predator (1987-2010)', 'collections&url=predator', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Purge (2013-2016)', 'collections&url=thepurge', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rambo (1982-2008)', 'collections&url=rambo', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('RED (2010-2013)', 'collections&url=red', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Revenge of the Nerds (1984-1987)', 'collections&url=revengeofthenerds', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Riddick (2000-2013)', 'collections&url=riddick', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ride Along (2014-2016)', 'collections&url=ridealong', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Ring (2002-2017)', 'collections&url=thering', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('RoboCop (1987-1993)', 'collections&url=robocop', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rocky (1976-2015)', 'collections&url=rocky', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Romancing the Stone (1984-1985)', 'collections&url=romancingthestone', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rush Hour (1998-2007)', 'collections&url=rushhour', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Santa Clause (1994-2006)', 'collections&url=santaclause', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Saw (2004-2010)', 'collections&url=saw', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sex and the City (2008-2010)', 'collections&url=sexandthecity', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Shaft (1971-2000)', 'collections&url=shaft', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Shanghai Noon (2000-2003)', 'collections&url=shanghainoon', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sin City (2005-2014)', 'collections&url=sincity', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sinister (2012-2015)', 'collections&url=sinister', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sister Act (1995-1993)', 'collections&url=sisteract', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Smokey and the Bandit (1977-1986)', 'collections&url=smokeyandthebandit', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Speed (1994-1997)', 'collections&url=speed', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Stakeout (1987-1993)', 'collections&url=stakeout', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Star Trek (1979-2016)', 'collections&url=startrek', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Star Wars (1977-2015)', 'collections&url=starwars', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Sting (1973-1983)', 'collections&url=thesting', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Taken (2008-2014)', 'collections&url=taken', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Taxi (1998-2007)', 'collections&url=taxi', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ted (2012-2015)', 'collections&url=ted', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Teen Wolf (1985-1987)', 'collections&url=teenwolf', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Terminator (1984-2015)', 'collections&url=terminator', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Terms of Endearment (1983-1996)', 'collections&url=termsofendearment', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Texas Chainsaw Massacre (1974-2013)', 'collections&url=texaschainsawmassacre', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Thing (1982-2011)', 'collections&url=thething', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Thomas Crown Affair (1968-1999)', 'collections&url=thomascrownaffair', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Transporter (2002-2015)', 'collections&url=transporter', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Under Siege (1992-1995)', 'collections&url=undersiege', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Universal Soldier (1992-2012)', 'collections&url=universalsoldier', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Wall Street (1987-2010)', 'collections&url=wallstreet', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Waynes World (1992-1993)', 'collections&url=waynesworld', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Weekend at Bernies (1989-1993)', 'collections&url=weekendatbernies', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Whole Nine Yards (2000-2004)', 'collections&url=wholenineyards', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('X-Files (1998-2008)', 'collections&url=xfiles', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('xXx (2002-2005)', 'collections&url=xxx', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Young Guns (1988-1990)', 'collections&url=youngguns', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Zoolander (2001-2016)', 'collections&url=zoolander', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Zorro (1998-2005)', 'collections&url=zorro', 'collections.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()


    def collectionKids(self):
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Disney Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collections&url=disneymovies', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Kids Boxset Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collectionBoxsetKids', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Kids Movie Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collections&url=kidsmovies', 'collections.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()
        

    def collectionBoxsetKids(self):
        self.addDirectoryItem('101 Dalmations (1961-2003)', 'collections&url=onehundredonedalmations', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Addams Family (1991-1998)', 'collections&url=addamsfamily', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Aladdin (1992-1996)', 'collections&url=aladdin', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Alvin and the Chipmunks (2007-2015)', 'collections&url=alvinandthechipmunks', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Atlantis (2001-2003)', 'collections&url=atlantis', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Babe (1995-1998)', 'collections&url=babe', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Balto (1995-1998)', 'collections&url=balto', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bambi (1942-2006)', 'collections&url=bambi', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Beauty and the Beast (1991-2017)', 'collections&url=beautyandthebeast', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Beethoven (1992-2014)', 'collections&url=beethoven', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Brother Bear (2003-2006)', 'collections&url=brotherbear', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cars (2006-2017)', 'collections&url=cars', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cinderella (1950-2007)', 'collections&url=cinderella', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cloudy With a Chance of Meatballs (2009-2013)', 'collections&url=cloudywithachanceofmeatballs', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Despicable Me (2010-2015)', 'collections&url=despicableme', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Finding Nemo (2003-2016)', 'collections&url=findingnemo', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fox and the Hound (1981-2006)', 'collections&url=foxandthehound', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Free Willy (1993-2010)', 'collections&url=freewilly', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ghostbusters (1984-2016)', 'collections&url=ghostbusters', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gremlins (1984-2016)', 'collections&url=gremlins', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Happy Feet (2006-2011)', 'collections&url=happyfeet', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Harry Potter (2001-2011)', 'collections&url=harrypotter', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Home Alone (1990-2012)', 'collections&url=homealone', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Homeward Bound (1993-1996)', 'collections&url=homewardbound', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Honey, I Shrunk the Kids (1989-1997)', 'collections&url=honeyishrunkthekids', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hotel Transylvania (2012-2015)', 'collections&url=hoteltransylvania', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('How to Train Your Dragon (2010-2014)', 'collections&url=howtotrainyourdragon', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hunchback of Notre Dame (1996-2002)', 'collections&url=hunchbackofnotredame', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ice Age (2002-2016)', 'collections&url=iceage', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jurassic Park (1993-2015)', 'collections&url=jurassicpark', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kung Fu Panda (2008-2016)', 'collections&url=kungfupanda', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lady and the Tramp (1955-2001)', 'collections&url=ladyandthetramp', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lilo and Stitch (2002-2006)', 'collections&url=liloandstitch', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Madagascar (2005-2014)', 'collections&url=madagascar', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Monsters Inc (2001-2013)', 'collections&url=monstersinc', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mulan (1998-2004)', 'collections&url=mulan', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Narnia (2005-2010)', 'collections&url=narnia', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('New Groove (2000-2005)', 'collections&url=newgroove', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Open Season (2006-2015)', 'collections&url=openseason', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Planes (2013-2014)', 'collections&url=planes', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Pocahontas (1995-1998)', 'collections&url=pocahontas', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Problem Child (1990-1995)', 'collections&url=problemchild', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rio (2011-2014)', 'collections&url=rio', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sammys Adventures (2010-2012)', 'collections&url=sammysadventures', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Scooby-Doo (2002-2014)', 'collections&url=scoobydoo', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Short Circuit (1986-1988)', 'collections&url=shortcircuit', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Shrek (2001-2011)', 'collections&url=shrek', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('SpongeBob SquarePants (2004-2017)', 'collections&url=spongebobsquarepants', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Spy Kids (2001-2011)', 'collections&url=spykids', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Star Wars (1977-2015)', 'collections&url=starwars', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Stuart Little (1999-2002)', 'collections&url=stuartlittle', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tarzan (1999-2016)', 'collections&url=tarzan', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Teenage Mutant Ninja Turtles (1978-2009)', 'collections&url=teenagemutantninjaturtles', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Jungle Book (1967-2003)', 'collections&url=thejunglebook', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Karate Kid (1984-2010)', 'collections&url=thekaratekid', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Lion King (1994-2016)', 'collections&url=thelionking', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Little Mermaid (1989-1995)', 'collections&url=thelittlemermaid', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Neverending Story (1984-1994)', 'collections&url=theneverendingstory', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Smurfs (2011-2013)', 'collections&url=thesmurfs', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tooth Fairy (2010-2012)', 'collections&url=toothfairy', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tinker Bell (2008-2014)', 'collections&url=tinkerbell', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tom and Jerry (1992-2013)', 'collections&url=tomandjerry', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Toy Story (1995-2014)', 'collections&url=toystory', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('VeggieTales (2002-2008)', 'collections&url=veggietales', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Winnie the Pooh (2000-2005)', 'collections&url=winniethepooh', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Wizard of Oz (1939-2013)', 'collections&url=wizardofoz', 'collections.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()


    def collectionSuperhero(self):
        self.addDirectoryItem('Avengers (2008-2017)', 'collections&url=avengers', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Batman (1989-2016)', 'collections&url=batman', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Captain America (2011-2016)', 'collections&url=captainamerica', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dark Knight Trilogy (2005-2013)', 'collections&url=darkknight', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fantastic Four (2005-2015)', 'collections&url=fantasticfour', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hulk (2003-2008)', 'collections&url=hulk', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Iron Man (2008-2013)', 'collections&url=ironman', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Spider-Man (2002-2017)', 'collections&url=spiderman', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Superman (1978-2016)', 'collections&url=superman', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('X-Men (2000-2016)', 'collections&url=xmen', 'collections.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()
            

    def endDirectory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


