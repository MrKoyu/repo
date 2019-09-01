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
        self.addDirectoryItem(70003,  'ShowChangelog',  'icon.png',  'DefaultFolder.png')
        self.addDirectoryItem(32001, 'movieNavigator', 'home_movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvNavigator', 'home_tvshows.png', 'DefaultTVShows.png')
        if not control.setting('lists.widget') == '0':
            self.addDirectoryItem(70004, 'kidzoneNavigator', 'home_kids.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32711, 'collectionsNavigator', 'home_collections.png', 'DefaultMovies.png')
            self.addDirectoryItem(32708, 'tvNetworks', 'home_networks.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32709, 'boxsetKingsNavigator', 'home_boxsets.png', 'DefaultMovies.png')
            self.addDirectoryItem(32700, 'docuHeaven', 'home_documentaries.png', 'DefaultMovies.png')
            self.addDirectoryItem(32713, 'twentyfoursevenNavigator', 'home_247.png', 'DefaultMovies.png')
            self.addDirectoryItem(32008, 'systemNavigator', 'tools.png', 'DefaultTVShows.png')

        #self.addDirectoryItem(32008, 'toolNavigator', 'tools.png', 'DefaultAddonProgram.png')

        downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        if downloads == True:
            self.addDirectoryItem(32009, 'downloadNavigator', 'downloads.png', 'DefaultFolder.png')

        self.addDirectoryItem(32010, 'searchNavigator', 'search3.png', 'DefaultFolder.png')        

        self.endDirectory()


    def movies(self, lite=False):
        self.addDirectoryItem(32714, 'eimportalmovies', 'portal_movie.png', 'DefaultMovies.png')
        self.addDirectoryItem(32726, 'randomMoviesNavigator', 'random_movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(32022, 'movies&url=theaters', 'in-theaters.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32017, 'movies&url=trending', 'people-watching.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32011, 'movieGenres', 'genres.png', 'DefaultMovies.png')
        self.addDirectoryItem(32715, 'movies&url=collectionstop1000c', 'mytop1000.png', 'DefaultMovies.png')
        self.addDirectoryItem(32012, 'movieYears', 'years.png', 'DefaultMovies.png')
        self.addDirectoryItem(32014, 'movieLanguages', 'international.png', 'DefaultMovies.png')
        self.addDirectoryItem(32013, 'moviePersons', 'people.png', 'DefaultMovies.png')
        #self.addDirectoryItem(32015, 'movieCertificates', 'certificates.png', 'DefaultMovies.png')
        self.addDirectoryItem(32018, 'movies&url=popular', 'most-popular.png', 'DefaultMovies.png')
        self.addDirectoryItem(32716, 'movies&url=romance', 'romance.png', 'DefaultMovies.png')  
        self.addDirectoryItem(32717, 'movies&url=marvel', 'marvel_studios.png', 'DefaultMovies.png') 
        self.addDirectoryItem(32718, 'movies&url=dcmovies', 'dc2.png', 'DefaultMovies.png')
        self.addDirectoryItem(32719, 'movies&url=dcanimate', 'dc.png', 'DefaultMovies.png')
        self.addDirectoryItem(32720, 'movies&url=tophorr', 'horror.png', 'DefaultMovies.png')
        self.addDirectoryItem(32721, 'movies&url=horror', 'horror2.png', 'DefaultMovies.png')
        self.addDirectoryItem(32722, 'movies&url=standup', 'standup.png', 'DefaultMovies.png')       
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
        self.addDirectoryItem(32723, 'eimportalshows', 'portal_tv.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32724, 'tvshows&url=top250tv', 'imdb250.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32725, 'tvshows&url=advancedsearchnetflixshows', 'netflix.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32701, 'tvGenres', 'genres2.png', 'DefaultTVShows.png')
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
        self.addDirectoryItem(32609, 'ResolveurlRDTorrent', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32073, 'authTrakt', 'trakt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32640, 'urlResolverRDAuthorize', 'tools.png', 'DefaultAddonProgram.png')
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
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Actor Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collectionActors', 'collections_actors.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Best of Collections[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collectionBest', 'collections.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Holidays Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collectionHolidays', 'collections_christmas.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Foreign Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'movies&url=collectionsbestforeign', 'collections_languages.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Lifetime Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collectionLifetime', 'collections_lifetime.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Wallmark Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'movies&url=collectionswallmark', 'collections_wallmart.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Trakt Collections[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'collectionTrakt', 'collections_trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]IMDb Top 1000[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'movies&url=collectionstop1000a', 'collections_imdb.png', 'DefaultMovies.png')
        
        self.endDirectory()

    def collectionActors(self):
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Adam Sandler[/COLOR]', 'collections&url=adamsandler', 'movies_actors/AdamSandler.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Al Pacino[/COLOR]', 'collections&url=alpacino', 'movies_actors/AlPacino.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Alan Rickman[/COLOR]', 'collections&url=alanrickman', 'movies_actors/AlanRickman.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Anthony Hopkins[/COLOR]', 'collections&url=anthonyhopkins', 'movies_actors/AnthonyHopkins.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Angelina Jolie[/COLOR]', 'collections&url=angelinajolie', 'movies_actors/AngelinaJolie.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Arnold Schwarzenegger[/COLOR]', 'collections&url=arnoldschwarzenegger', 'movies_actors/ArnoldSchwarzenegger.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Charlize Theron[/COLOR]', 'collections&url=charlizetheron', 'movies_actors/CharlizeTheron.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Clint Eastwood[/COLOR]', 'collections&url=clinteastwood', 'movies_actors/ClintEastwood.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Demi Moore[/COLOR]', 'collections&url=demimoore', 'movies_actors/DemiMoore.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Denzel Washington[/COLOR]', 'collections&url=denzelwashington', 'movies_actors/DenzelWashington.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Eddie Murphy[/COLOR]', 'collections&url=eddiemurphy', 'movies_actors/EddieMurphy.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Elvis Presley[/COLOR]', 'collections&url=elvispresley', 'movies_actors/ElvisPresley.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Gene Wilder[/COLOR]', 'collections&url=genewilder', 'movies_actors/GeneWilder.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Gerard Butler[/COLOR]', 'collections&url=gerardbutler', 'movies_actors/GerardButler.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Goldie Hawn[/COLOR]', 'collections&url=goldiehawn', 'movies_actors/GoldieHawn.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Jason Statham[/COLOR]', 'collections&url=jasonstatham', 'movies_actors/JasonStatham.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Jean-Claude Van Damme[/COLOR]', 'collections&url=jeanclaudevandamme', 'movies_actors/JeanClaudeVanDamme.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Jeffrey Dean Morgan[/COLOR]', 'collections&url=jeffreydeanmorgan', 'movies_actors/JeffreyDeanMorgan.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]John Travolta[/COLOR]', 'collections&url=johntravolta', 'movies_actors/JohnTravolta.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Johnny Depp[/COLOR]', 'collections&url=johnnydepp', 'movies_actors/JohnnyDepp.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Julia Roberts[/COLOR]', 'collections&url=juliaroberts', 'movies_actors/JuliaRoberts.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Kevin Costner[/COLOR]', 'collections&url=kevincostner', 'movies_actors/KevinCostner.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Liam Neeson[/COLOR]', 'collections&url=liamneeson', 'movies_actors/LiamNeeson.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Mel Gibson[/COLOR]', 'collections&url=melgibson', 'movies_actors/MelGibson.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Melissa McCarthy[/COLOR]', 'collections&url=melissamccarthy', 'movies_actors/MelissaMcCarthy.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Meryl Streep[/COLOR]', 'collections&url=merylstreep', 'movies_actors/MerylStreep.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Michelle Pfeiffer[/COLOR]', 'collections&url=michellepfeiffer', 'movies_actors/MichellePfeiffer.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Nicolas Cage[/COLOR]', 'collections&url=nicolascage', 'movies_actors/NicolasCage.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Nicole Kidman[/COLOR]', 'collections&url=nicolekidman', 'movies_actors/NicoleKidman.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Paul Newman[/COLOR]', 'collections&url=paulnewman', 'movies_actors/PaulNewman.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Reese Witherspoon[/COLOR]', 'collections&url=reesewitherspoon', 'movies_actors/ReeseWitherspoon.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Robert De Niro[/COLOR]', 'collections&url=robertdeniro', 'movies_actors/RobertDeNiro.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Samuel L Jackson[/COLOR]', 'collections&url=samueljackson', 'movies_actors/SamuelLJackson.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Scarlett Johansson[/COLOR]', 'collections&url=scarlettjohansson', 'movies_actors/ScarlettJohansson.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Sean Connery[/COLOR]', 'collections&url=seanconnery', 'movies_actors/SeanConnery.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Sharon Stone[/COLOR]', 'collections&url=sharonstone', 'movies_actors/SharonStone.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Sigourney Weaver[/COLOR]', 'collections&url=sigourneyweaver', 'movies_actors/SigourneyWeaver.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Steven Seagal[/COLOR]', 'collections&url=stevenseagal', 'movies_actors/StevenSeagal.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Tom Hanks[/COLOR]', 'collections&url=tomhanks', 'movies_actors/TomHanks.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Vin Diesel[/COLOR]', 'collections&url=vindiesel', 'movies_actors/VinDiesel.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Wesley Snipes[/COLOR]', 'collections&url=wesleysnipes', 'movies_actors/WesleySnipes.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Will Smith[/COLOR]', 'collections&url=willsmith', 'movies_actors/WillSmith.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Winona Ryder[/COLOR]', 'collections&url=winonaryder', 'movies_actors/WinonaRyder.jpg', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()

    def collectionBest(self):
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Addiction Movies[/COLOR]', 'movies&url=collectionsaddiction', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Action & Adventure Movies[/COLOR]', 'movies&url=collectionsaction', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Animation Movies[/COLOR]', 'movies&url=collectionsanimation', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Asian Movies[/COLOR]', 'movies&url=collectionsinterasian', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Based on True Story Movies[/COLOR]', 'movies&url=collectionstruestory', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Bollywood Erotic Movies[/COLOR]', 'movies&url=collectionsinterbollywooderotic', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Bollywood Movies[/COLOR]', 'movies&url=collectionsinterbollywood', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Brazilian Movies[/COLOR]', 'movies&url=collectionsinterbrazilian', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]British Humor Movies[/COLOR]', 'movies&url=collectionshumor', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Car Movies[/COLOR]', 'collections&url=carmovies', 'collections.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Comedy Movies[/COLOR]', 'movies&url=collectionscomedy', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Courtroom Movies[/COLOR]', 'movies&url=collectionscourtroom', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Child Lead Role Movies[/COLOR]', 'movies&url=collectionschild', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Crime Movies[/COLOR]', 'movies&url=collectionscrime', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Dark Comedy Movies[/COLOR]', 'movies&url=collectionsdarkcomedy', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Dialogue Movies[/COLOR]', 'movies&url=collectionsdialogue', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Disaster & Apocalyptic Movies[/COLOR]', 'movies&url=collectionsdisaster', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Documentary Movies[/COLOR]', 'movies&url=collectionsdocu', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Drama Movies[/COLOR]', 'movies&url=collectionsdrama', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Fantasy Movies[/COLOR]', 'movies&url=https://api.trakt.tv/users/acerider/lists/movies-fantasy/items', 'collections.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Father & Son Movies[/COLOR]', 'movies&url=collectionsfather', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Feel-Good Movies[/COLOR]', 'movies&url=collectionsfeelgood', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Film-Making & Cinema Movies[/COLOR]', 'movies&url=collectionsfilm', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Foreign Movies[/COLOR]', 'movies&url=collectionsforeign', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]French Movies[/COLOR]', 'movies&url=collectionsinterfrench', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Gangster Movies[/COLOR]', 'movies&url=collectionsgangster', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Hackers & Technology Movies[/COLOR]', 'movies&url=collectionshackers', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Heists & Robbers Movies[/COLOR]', 'movies&url=collectionsheists', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Hindi Movies[/COLOR]', 'movies&url=collectionsinterhindi', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Inspirational & Motivational[/COLOR]', 'movies&url=collectionsinspirational', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]International Movies[/COLOR]', 'movies&url=collectionsinterforeign', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Journalism Movies[/COLOR]', 'movies&url=collectionsjornalism', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Mental & Physical illness Movies[/COLOR]', 'movies&url=collectionsmental', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Mindfuck Movies[/COLOR]', 'movies&url=https://api.trakt.tv/users/cdtv/lists/mindfuck-movies/items', 'collections.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Mother & Son Movies[/COLOR]', 'movies&url=collectionsmother', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Music & Musical Movies[/COLOR]', 'movies&url=collectionsmusic', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Mystery & Horror Movies[/COLOR]', 'movies&url=collectionsmystery', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Old Age Movies[/COLOR]', 'movies&url=collectionsoldage', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]One Room Movies[/COLOR]', 'movies&url=collectionsoneroom', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Political Movies[/COLOR]', 'movies&url=collectionspolitical', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Prison & Escape Movies[/COLOR]', 'movies&url=collectionsprison', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Psychological Thriller Movies[/COLOR]', 'movies&url=collectionspsychological', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Revenge Movies[/COLOR]', 'movies&url=collectionsrevenge', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Road Trip & Travel Movies[/COLOR]', 'movies&url=collectionsroadtrip', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Romance Movies[/COLOR]', 'movies&url=collectionsromance', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Romantic Movies[/COLOR]', 'movies&url=https://api.trakt.tv/users/acerider/lists/movies-romantic/items', 'collections.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Serial Killers Movies[/COLOR]', 'movies&url=collectionskillers', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]SuperHero Movies[/COLOR]', 'movies&url=collectionssuperhero', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Survival Movies[/COLOR]', 'movies&url=collectionssurvival', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Sci-Fi Movies[/COLOR]', 'movies&url=https://api.trakt.tv/users/acerider/lists/movies-sci-fi/items', 'collections.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Sport Movies[/COLOR]', 'movies&url=collectionssports', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Spy Movies[/COLOR]', 'movies&url=collectionsspy', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Stephen King Movies[/COLOR]', 'movies&url=https://api.trakt.tv/users/ljransom/lists/stephen-king-movies/items', 'collections.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Teenage Movies[/COLOR]', 'movies&url=collectionsteen', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Time Travel Movies[/COLOR]', 'movies&url=collectionstimetravel', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Thriller Movies[/COLOR]', 'movies&url=https://api.trakt.tv/users/acerider/lists/movies-thriller/items', 'collections.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Twist Ending Movies[/COLOR]', 'movies&url=collectionstwist', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]War Movies[/COLOR]', 'movies&url=collectionswar', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Western Movies[/COLOR]', 'movies&url=collectionswestern', 'collections.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Zombie - Vampire - Alien - Robot Movies[/COLOR]', 'movies&url=collectionszombie', 'collections.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()

    def collectionHolidays(self):
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Valentines Day[/COLOR]', 'movies&url=holidayvalentines', 'collections_valentines.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]St. Patricks Day[/COLOR]', 'movies&url=holidaypatricks', 'collections_patricks.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Easter[/COLOR]', 'movies&url=holidayeaster', 'collections_easter.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Independence Day[/COLOR]', 'movies&url=holidayindependence', 'collections_independence.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Halloween[/COLOR]', 'movies&url=holidayhalloween', 'collections_halloween.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Thanksgiving[/COLOR]', 'movies&url=holidaysthanksgiven', 'collections_thanks.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Christmas[/COLOR]', 'movies&url=holidayschristmas', 'collections_christmas.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()

    def collectionLifetime(self, lite=False):
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Most Popular[/COLOR]', 'movies&url=collectionslifetime', 'collections_lifetime2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Highly Rated[/COLOR]', 'movies&url=collectionslifetimeb', 'collections_lifetime2.png', 'DefaultMovies.png')
        
        self.endDirectory()

    def collectionTrakt(self, lite=False):
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Rotten Tomatoes: Best of 2019[/COLOR]', 'movies&url=https://api.trakt.tv/users/lish408/lists/rotten-tomatoes-best-of-2019/items', 'collections_trakt2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Rotten Tomatoes: Best of 2018[/COLOR]', 'movies&url=https://api.trakt.tv/users/lish408/lists/rotten-tomatoes-best-of-2018/items', 'collections_trakt2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Rotten Tomatoes: Best of 2017[/COLOR]', 'movies&url=https://api.trakt.tv/users/lish408/lists/rotten-tomatoes-best-of-2017/items', 'collections_trakt2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Rotten Tomatoes: Best of 2016[/COLOR]', 'movies&url=https://api.trakt.tv/users/lish408/lists/rotten-tomatoes-best-of-2016/items', 'collections_trakt2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Rotten Tomatoes: Best of 2015[/COLOR]', 'movies&url=https://api.trakt.tv/users/lish408/lists/rotten-tomatoes-best-of-2015/items', 'collections_trakt2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Rotten Tomatoes: Best of 2014[/COLOR]', 'movies&url=https://api.trakt.tv/users/lish408/lists/rotten-tomatoes-best-of-2014/items', 'collections_trakt2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Decade: 2010s[/COLOR]', 'movies&url=https://api.trakt.tv/users/cdtv/lists/trakt-movie-decade-2010s/items', 'collections_trakt2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Decade: 2000s[/COLOR]', 'movies&url=https://api.trakt.tv/users/cdtv/lists/trakt-movie-decade-2000s/items', 'collections_trakt2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Decade: 1990s[/COLOR]', 'movies&url=https://api.trakt.tv/users/cdtv/lists/trakt-movie-decade-1990s/items', 'collections_trakt2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Decade: 1980s[/COLOR]', 'movies&url=https://api.trakt.tv/users/cdtv/lists/trakt-movie-decade-1980s/items', 'collections_trakt2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Decade: 1970s[/COLOR]', 'movies&url=https://api.trakt.tv/users/cdtv/lists/trakt-movie-decade-1970s/items', 'collections_trakt2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Decade: 1960s[/COLOR]', 'movies&url=https://api.trakt.tv/users/cdtv/lists/trakt-movie-decade-1960s/items', 'collections_trakt2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Decade: 1950s[/COLOR]', 'movies&url=https://api.trakt.tv/users/cdtv/lists/trakt-movie-decade-1950s/items', 'collections_trakt2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Decade: 1940s-1910s[/COLOR]', 'movies&url=https://api.trakt.tv/users/cdtv/lists/trakt-movie-decade-1940s-1930s-1920s-1910s/items', 'collections_trakt2.png', 'DefaultMovies.png')

        self.endDirectory()                

    def boxsetKings(self, lite=False):
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Boxset Kings[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'collectionBoxset', 'boxsets14.png', 'boxsets1.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Boxset Genres[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'boxsetsNavigator', 'boxsets14.png', 'boxsets1.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Boxsets[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'tvshows&url=popular', 'boxsets1.png', 'boxsets1.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Boxset Genres[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'boxsetgenres', 'boxsets1.png', 'boxsets1.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Search[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'movieSearch', 'boxsets_search.png', 'boxsets_search.png')
        
        self.endDirectory()

    def TwentyFourSeven(self, lite=False):
        self.addDirectoryItem('[B][COLOR hotpink]• [/COLOR][/B][COLOR ghostwhite]24/7 Movies[/COLOR][B][COLOR hotpink] •[/COLOR][/B]', '247movies', '247.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR hotpink]• [/COLOR][/B][COLOR ghostwhite]24/7 Shows[/COLOR][B][COLOR hotpink] •[/COLOR][/B]', '247shows', '247.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR hotpink]• [/COLOR][/B][COLOR ghostwhite]24/7 Channels[/COLOR][B][COLOR hotpink] •[/COLOR][/B]', '247channels', '247.png', 'DefaultMovies.png')
        
        self.endDirectory()        

    def collectionBoxset(self):
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]48 Hrs.[/COLOR] [COLOR yellow] (1982-1990)[/COLOR]', 'collections&url=fortyeighthours', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Ace Ventura[/COLOR] [COLOR yellow] (1994-1995)[/COLOR]', 'collections&url=aceventura', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Airplane[/COLOR] [COLOR yellow] (1980-1982)[/COLOR]', 'collections&url=airplane', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Airport[/COLOR] [COLOR yellow] (1970-1979)[/COLOR]', 'collections&url=airport', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]American Graffiti[/COLOR] [COLOR yellow] (1973-1979)[/COLOR]', 'collections&url=americangraffiti', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Anaconda[/COLOR] [COLOR yellow] (1997-2004)[/COLOR]', 'collections&url=anaconda', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Analyze This[/COLOR] [COLOR yellow] (1999-2002)[/COLOR]', 'collections&url=analyzethis', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Anchorman[/COLOR] [COLOR yellow] (2004-2013)[/COLOR]', 'collections&url=anchorman', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Austin Powers[/COLOR] [COLOR yellow] (1997-2002)[/COLOR]', 'collections&url=austinpowers', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Avengers[/COLOR] [COLOR yellow] (2008-2017)[/COLOR]', 'collections&url=avengers', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Back to the Future[/COLOR] [COLOR yellow] (1985-1990)[/COLOR]', 'collections&url=backtothefuture', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Bad Boys[/COLOR] [COLOR yellow] (1995-2003)[/COLOR]', 'collections&url=badboys', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Bad Santa[/COLOR] [COLOR yellow] (2003-2016)[/COLOR]', 'collections&url=badsanta', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Basic Instinct[/COLOR] [COLOR yellow] (1992-2006)[/COLOR]', 'collections&url=basicinstinct', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Batman[/COLOR] [COLOR yellow] (1989-2016)[/COLOR]', 'collections&url=batman', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Beverly Hills Cop[/COLOR] [COLOR yellow] (1984-1994)[/COLOR]', 'collections&url=beverlyhillscop', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Big Mommas House[/COLOR] [COLOR yellow] (2000-2011)[/COLOR]', 'collections&url=bigmommashouse', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Blues Brothers[/COLOR] [COLOR yellow] (1980-1998)[/COLOR]', 'collections&url=bluesbrothers', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Bourne[/COLOR] [COLOR yellow] (2002-2016)[/COLOR]', 'collections&url=bourne', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Bruce Almighty[/COLOR] [COLOR yellow] (2003-2007)[/COLOR]', 'collections&url=brucealmighty', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Caddyshack[/COLOR] [COLOR yellow] (1980-1988)[/COLOR]', 'collections&url=caddyshack', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Cheaper by the Dozen[/COLOR] [COLOR yellow] (2003-2005)[/COLOR]', 'collections&url=cheaperbythedozen', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Cheech and Chong[/COLOR] [COLOR yellow] (1978-1984)[/COLOR]', 'collections&url=cheechandchong', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Childs Play[/COLOR] [COLOR yellow] (1988-2004)[/COLOR]', 'collections&url=childsplay', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]City Slickers[/COLOR] [COLOR yellow] (1991-1994)[/COLOR]', 'collections&url=cityslickers', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Conan[/COLOR] [COLOR yellow] (1982-2011)[/COLOR]', 'collections&url=conan', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Crank[/COLOR] [COLOR yellow] (2006-2009)[/COLOR]', 'collections&url=crank', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Crocodile Dundee[/COLOR] [COLOR yellow] (1986-2001)[/COLOR]', 'collections&url=crodiledunde', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Da Vinci Code[/COLOR] [COLOR yellow] (2006-2017)[/COLOR]', 'collections&url=davincicode', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Daddy Day Care[/COLOR] [COLOR yellow] (2003-2007)[/COLOR]', 'collections&url=daddydaycare', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Dark Knight Trilogy[/COLOR] [COLOR yellow] (2005-2013)[/COLOR]', 'collections&url=darkknight', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Death Wish[/COLOR] [COLOR yellow] (1974-1994)[/COLOR]', 'collections&url=deathwish', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Delta Force[/COLOR] [COLOR yellow] (1986-1990)[/COLOR]', 'collections&url=deltaforce', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Die Hard[/COLOR] [COLOR yellow] (1988-2013)[/COLOR]', 'collections&url=diehard', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Dirty Dancing[/COLOR] [COLOR yellow] (1987-2004)[/COLOR]', 'collections&url=dirtydancing', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Dirty Harry[/COLOR] [COLOR yellow] (1971-1988)[/COLOR]', 'collections&url=dirtyharry', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Dumb and Dumber[/COLOR] [COLOR yellow] (1994-2014)[/COLOR]', 'collections&url=dumbanddumber', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Escape from New York[/COLOR] [COLOR yellow] (1981-1996)[/COLOR]', 'collections&url=escapefromnewyork', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Every Which Way But Loose[/COLOR] [COLOR yellow] (1978-1980)[/COLOR]', 'collections&url=everywhichwaybutloose', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Exorcist[/COLOR] [COLOR yellow] (1973-2005)[/COLOR]', 'collections&url=exorcist', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]The Expendables[/COLOR] [COLOR yellow] (2010-2014)[/COLOR]', 'collections&url=theexpendables', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Fantastic Four[/COLOR] [COLOR yellow] (2005-2015)[/COLOR]', 'collections&url=fantasticfour', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Fast and the Furious[/COLOR] [COLOR yellow] (2001-2017)[/COLOR]', 'collections&url=fastandthefurious', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Father of the Bride[/COLOR] [COLOR yellow] (1991-1995)[/COLOR]', 'collections&url=fatherofthebride', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Fletch[/COLOR] [COLOR yellow] (1985-1989)[/COLOR]', 'collections&url=fletch', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Friday[/COLOR] [COLOR yellow] (1995-2002)[/COLOR]', 'collections&url=friday', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Friday the 13th[/COLOR] [COLOR yellow] (1980-2009)[/COLOR]', 'collections&url=fridaythe13th', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Fugitive[/COLOR] [COLOR yellow] (1993-1998)[/COLOR]', 'collections&url=fugitive', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]G.I. Joe[/COLOR] [COLOR yellow] (2009-2013)[/COLOR]', 'collections&url=gijoe', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Get Shorty[/COLOR] [COLOR yellow] (1995-2005)[/COLOR]', 'collections&url=getshorty', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Gettysburg[/COLOR] [COLOR yellow] (1993-2003)[/COLOR]', 'collections&url=gettysburg', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Ghost Rider[/COLOR] [COLOR yellow] (2007-2011)[/COLOR]', 'collections&url=ghostrider', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Ghostbusters[/COLOR] [COLOR yellow] (1984-2016)[/COLOR]', 'collections&url=ghostbusters', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Gods Not Dead[/COLOR] [COLOR yellow] (2014-2016)[/COLOR]', 'collections&url=godsnotdead', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Godfather[/COLOR] [COLOR yellow] (1972-1990)[/COLOR]', 'collections&url=godfather', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Godzilla[/COLOR] [COLOR yellow] (1956-2016)[/COLOR]', 'collections&url=godzilla', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Grown Ups[/COLOR] [COLOR yellow] (2010-2013)[/COLOR]', 'collections&url=grownups', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Grumpy Old Men[/COLOR] [COLOR yellow] (2010-2013)[/COLOR]', 'collections&url=grumpyoldmen', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Guns of Navarone[/COLOR] [COLOR yellow] (1961-1978)[/COLOR]', 'collections&url=gunsofnavarone', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Halloween[/COLOR] [COLOR yellow] (1978-2009)[/COLOR]', 'collections&url=halloween', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Hangover[/COLOR] [COLOR yellow] (2009-2013)[/COLOR]', 'collections&url=hangover', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Hannibal Lector[/COLOR] [COLOR yellow] (1986-2007)[/COLOR]', 'collections&url=hanniballector', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Hellraiser[/COLOR] [COLOR yellow] (1987-1996)[/COLOR]', 'collections&url=hellraiser', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Honey I Shrunk the Kids[/COLOR] [COLOR yellow] (1989-1995)[/COLOR]', 'collections&url=honeyishrunkthekids', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Horrible Bosses[/COLOR] [COLOR yellow] (2011-2014)[/COLOR]', 'collections&url=horriblebosses', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Hostel[/COLOR] [COLOR yellow] (2005-2011)[/COLOR]', 'collections&url=hostel', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Hot Shots[/COLOR] [COLOR yellow] (1991-1996)[/COLOR]', 'collections&url=hotshots', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Hulk[/COLOR] [COLOR yellow] (2003-2008)[/COLOR]', 'collections&url=hulk', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Independence Day[/COLOR] [COLOR yellow] (1996-2016)[/COLOR]', 'collections&url=independenceday', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Indiana Jones[/COLOR] [COLOR yellow] (1981-2008)[/COLOR]', 'collections&url=indianajones', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Insidious[/COLOR] [COLOR yellow] (2010-2015)[/COLOR]', 'collections&url=insidious', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Iron Eagle[/COLOR] [COLOR yellow] (1986-1992)[/COLOR]', 'collections&url=ironeagle', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Iron Man[/COLOR] [COLOR yellow] (2008-2013)[/COLOR]', 'collections&url=ironman', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Jack Reacher[/COLOR] [COLOR yellow] (2012-2016)[/COLOR]', 'collections&url=jackreacher', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Jack Ryan[/COLOR] [COLOR yellow] (1990-2014)[/COLOR]', 'collections&url=jackryan', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Jackass[/COLOR] [COLOR yellow] (2002-2013)[/COLOR]', 'collections&url=jackass', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]James Bond[/COLOR] [COLOR yellow] (1963-2015)[/COLOR]', 'collections&url=jamesbond', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Jaws[/COLOR] [COLOR yellow] (1975-1987)[/COLOR]', 'collections&url=jaws', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Jeepers Creepers[/COLOR] [COLOR yellow] (2001-2017)[/COLOR]', 'collections&url=jeeperscreepers', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]John Wick[/COLOR] [COLOR yellow] (2014-2017)[/COLOR]', 'collections&url=johnwick', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Jumanji[/COLOR] [COLOR yellow] (1995-2005)[/COLOR]', 'collections&url=jumanji', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Jurassic Park[/COLOR] [COLOR yellow] (1993-2015)[/COLOR]', 'collections&url=jurassicpark', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Kick-Ass[/COLOR] [COLOR yellow] (2010-2013)[/COLOR]', 'collections&url=kickass', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Kill Bill[/COLOR] [COLOR yellow] (2003-2004)[/COLOR]', 'collections&url=killbill', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]King Kong[/COLOR] [COLOR yellow] (1933-2016)[/COLOR]', 'collections&url=kingkong', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Lara Croft[/COLOR] [COLOR yellow] (2001-2003)[/COLOR]', 'collections&url=laracroft', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Legally Blonde[/COLOR] [COLOR yellow] (2001-2003)[/COLOR]', 'collections&url=legallyblonde', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Lethal Weapon[/COLOR] [COLOR yellow] (1987-1998)[/COLOR]', 'collections&url=leathalweapon', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Look Whos Talking[/COLOR] [COLOR yellow] (1989-1993)[/COLOR]', 'collections&url=lookwhostalking', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Machete[/COLOR] [COLOR yellow] (2010-2013)[/COLOR]', 'collections&url=machete', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Magic Mike[/COLOR] [COLOR yellow] (2012-2015)[/COLOR]', 'collections&url=magicmike', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Major League[/COLOR] [COLOR yellow] (1989-1998)[/COLOR]', 'collections&url=majorleague', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Man from Snowy River[/COLOR] [COLOR yellow] (1982-1988)[/COLOR]', 'collections&url=manfromsnowyriver', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Mask[/COLOR] [COLOR yellow] (1994-2005)[/COLOR]', 'collections&url=mask', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Matrix[/COLOR] [COLOR yellow] (1999-2003)[/COLOR]', 'collections&url=matrix', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]The Mechanic[/COLOR] [COLOR yellow] (2011-2016)[/COLOR]', 'collections&url=themechanic', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Meet the Parents[/COLOR] [COLOR yellow] (2000-2010)[/COLOR]', 'collections&url=meettheparents', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Men in Black[/COLOR] [COLOR yellow] (1997-2012)[/COLOR]', 'collections&url=meninblack', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Mighty Ducks[/COLOR] [COLOR yellow] (1995-1996)[/COLOR]', 'collections&url=mightyducks', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Miss Congeniality[/COLOR] [COLOR yellow] (2000-2005)[/COLOR]', 'collections&url=misscongeniality', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Missing in Action[/COLOR] [COLOR yellow] (1984-1988)[/COLOR]', 'collections&url=missinginaction', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Mission Impossible[/COLOR] [COLOR yellow] (1996-2015)[/COLOR]', 'collections&url=missionimpossible', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Naked Gun[/COLOR] [COLOR yellow] (1988-1994)[/COLOR]', 'collections&url=nakedgun', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]National Lampoon[/COLOR] [COLOR yellow] (1978-2006)[/COLOR]', 'collections&url=nationallampoon', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]National Lampoons Vacation[/COLOR] [COLOR yellow] (1983-2015)[/COLOR]', 'collections&url=nationallampoonsvacation', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]National Treasure[/COLOR] [COLOR yellow] (2004-2007)[/COLOR]', 'collections&url=nationaltreasure', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Neighbors[/COLOR] [COLOR yellow] (2014-2016)[/COLOR]', 'collections&url=neighbors', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Night at the Museum[/COLOR] [COLOR yellow] (2006-2014)[/COLOR]', 'collections&url=nightatthemuseum', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Nightmare on Elm Street[/COLOR] [COLOR yellow] (1984-2010)[/COLOR]', 'collections&url=nightmareonelmstreet', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Now You See Me[/COLOR] [COLOR yellow] (2013-2016)[/COLOR]', 'collections&url=nowyouseeme', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Nutty Professor[/COLOR] [COLOR yellow] (1996-2000)[/COLOR]', 'collections&url=nuttyprofessor', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Oceans Eleven[/COLOR] [COLOR yellow] (2001-2007)[/COLOR]', 'collections&url=oceanseleven', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Odd Couple[/COLOR] [COLOR yellow] (1968-1998)[/COLOR]', 'collections&url=oddcouple', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Oh, God[/COLOR] [COLOR yellow] (1977-1984)[/COLOR]', 'collections&url=ohgod', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Olympus Has Fallen[/COLOR] [COLOR yellow] (2013-2016)[/COLOR]', 'collections&url=olympushasfallen', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Omen[/COLOR] [COLOR yellow] (1976-1981)[/COLOR]', 'collections&url=omen', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Paul Blart Mall Cop[/COLOR] [COLOR yellow] (2009-2015)[/COLOR]', 'collections&url=paulblart', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Pirates of the Caribbean[/COLOR] [COLOR yellow] (2003-2017)[/COLOR]', 'collections&url=piratesofthecaribbean', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Planet of the Apes[/COLOR] [COLOR yellow] (1968-2014)[/COLOR]', 'collections&url=planetoftheapes', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Police Academy[/COLOR] [COLOR yellow] (1984-1994)[/COLOR]', 'collections&url=policeacademy', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Poltergeist[/COLOR] [COLOR yellow] (1982-1988)[/COLOR]', 'collections&url=postergeist', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Porkys[/COLOR] [COLOR yellow] (1981-1985)[/COLOR]', 'collections&url=porkys', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Predator[/COLOR] [COLOR yellow] (1987-2010)[/COLOR]', 'collections&url=predator', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]The Purge[/COLOR] [COLOR yellow] (2013-2016)[/COLOR]', 'collections&url=thepurge', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Rambo[/COLOR] [COLOR yellow] (1982-2008)[/COLOR]', 'collections&url=rambo', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]RED[/COLOR] [COLOR yellow] (2010-2013)[/COLOR]', 'collections&url=red', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Revenge of the Nerds[/COLOR] [COLOR yellow] (1984-1987)[/COLOR]', 'collections&url=revengeofthenerds', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Riddick[/COLOR] [COLOR yellow] (2000-2013)[/COLOR]', 'collections&url=riddick', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Ride Along[/COLOR] [COLOR yellow] (2014-2016)[/COLOR]', 'collections&url=ridealong', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]The Ring[/COLOR] [COLOR yellow] (2002-2017)[/COLOR]', 'collections&url=thering', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]RoboCop[/COLOR] [COLOR yellow] (1987-1993)[/COLOR]', 'collections&url=robocop', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Rocky[/COLOR] [COLOR yellow] (1976-2015)[/COLOR]', 'collections&url=rocky', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Romancing the Stone[/COLOR] [COLOR yellow] (1984-1985)[/COLOR]', 'collections&url=romancingthestone', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Rush Hour[/COLOR] [COLOR yellow] (1998-2007)[/COLOR]', 'collections&url=rushhour', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Santa Clause[/COLOR] [COLOR yellow] (1994-2006)[/COLOR]', 'collections&url=santaclause', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Saw[/COLOR] [COLOR yellow] (2004-2010)[/COLOR]', 'collections&url=saw', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Sex and the City[/COLOR] [COLOR yellow] (2008-2010)[/COLOR]', 'collections&url=sexandthecity', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Shaft[/COLOR] [COLOR yellow] (1971-2000)[/COLOR]', 'collections&url=shaft', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Shanghai Noon[/COLOR] [COLOR yellow] (2000-2003)[/COLOR]', 'collections&url=shanghainoon', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Sin City[/COLOR] [COLOR yellow] (2005-2014)[/COLOR]', 'collections&url=sincity', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Sinister[/COLOR] [COLOR yellow] (2012-2015)[/COLOR]', 'collections&url=sinister', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Sister Act[/COLOR] [COLOR yellow] (1995-1993)[/COLOR]', 'collections&url=sisteract', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Smokey and the Bandit[/COLOR] [COLOR yellow] (1977-1986)[/COLOR]', 'collections&url=smokeyandthebandit', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Speed[/COLOR] [COLOR yellow] (1994-1997)[/COLOR]', 'collections&url=speed', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Spider-Man[/COLOR] [COLOR yellow] (2002-2017)[/COLOR]', 'collections&url=spiderman', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Stakeout[/COLOR] [COLOR yellow] (1987-1993)[/COLOR]', 'collections&url=stakeout', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Star Trek[/COLOR] [COLOR yellow] (1979-2016)[/COLOR]', 'collections&url=startrek', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Star Wars[/COLOR] [COLOR yellow] (1977-2015)[/COLOR]', 'collections&url=starwars', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Superman[/COLOR] [COLOR yellow] (1978-2016)[/COLOR]', 'collections&url=superman', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]The Sting[/COLOR] [COLOR yellow] (1973-1983)[/COLOR]', 'collections&url=thesting', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Taken[/COLOR] [COLOR yellow] (2008-2014)[/COLOR]', 'collections&url=taken', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Taxi[/COLOR] [COLOR yellow] (1998-2007)[/COLOR]', 'collections&url=taxi', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Ted[/COLOR] [COLOR yellow] (2012-2015)[/COLOR]', 'collections&url=ted', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Teen Wolf[/COLOR] [COLOR yellow] (1985-1987)[/COLOR]', 'collections&url=teenwolf', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Terminator[/COLOR] [COLOR yellow] (1984-2015)[/COLOR]', 'collections&url=terminator', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Terms of Endearment[/COLOR] [COLOR yellow] (1983-1996)[/COLOR]', 'collections&url=termsofendearment', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Texas Chainsaw Massacre[/COLOR] [COLOR yellow] (1974-2013)[/COLOR]', 'collections&url=texaschainsawmassacre', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]The Thing[/COLOR] [COLOR yellow] (1982-2011)[/COLOR]', 'collections&url=thething', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Thomas Crown Affair[/COLOR] [COLOR yellow] (1968-1999)[/COLOR]', 'collections&url=thomascrownaffair', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Transporter[/COLOR] [COLOR yellow] (2002-2015)[/COLOR]', 'collections&url=transporter', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Under Siege[/COLOR] [COLOR yellow] (1992-1995)[/COLOR]', 'collections&url=undersiege', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Universal Soldier[/COLOR] [COLOR yellow] (1992-2012)[/COLOR]', 'collections&url=universalsoldier', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Wall Street[/COLOR] [COLOR yellow] (1987-2010)[/COLOR]', 'collections&url=wallstreet', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Waynes World[/COLOR] [COLOR yellow] (1992-1993)[/COLOR]', 'collections&url=waynesworld', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Weekend at Bernies[/COLOR] [COLOR yellow] (1989-1993)[/COLOR]', 'collections&url=weekendatbernies', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Whole Nine Yards[/COLOR] [COLOR yellow] (2000-2004)[/COLOR]', 'collections&url=wholenineyards', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]X-Files[/COLOR] [COLOR yellow] (1998-2008)[/COLOR]', 'collections&url=xfiles', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]X-Men[/COLOR] [COLOR yellow] (2000-2016)[/COLOR]', 'collections&url=xmen', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]xXx[/COLOR] [COLOR yellow] (2002-2005)[/COLOR]', 'collections&url=xxx', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Young Guns[/COLOR] [COLOR yellow] (1988-1990)[/COLOR]', 'collections&url=youngguns', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Zoolander[/COLOR] [COLOR yellow] (2001-2016)[/COLOR]', 'collections&url=zoolander', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Zorro[/COLOR] [COLOR yellow] (1998-2005)[/COLOR]', 'collections&url=zorro', 'boxsets14.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()

    def kidzone(self, lite=False):
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Kids Movies[/COLOR][B][COLOR deepskyblue] •[/COLOR][/B]', 'kidsmoviesNavigator', 'kids_movies.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Kids TV Shows[/COLOR][B][COLOR deepskyblue] •[/COLOR][/B]', 'kidstvNavigator', 'kids_shows.png', 'DefaultTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Youngsters[/COLOR][B][COLOR deepskyblue] •[/COLOR][/B]', 'toddlerNavigator', 'kids_youngsters.png', 'DefaulTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Anime Movies[/COLOR][B][COLOR deepskyblue] •[/COLOR][/B]', 'animemovieNavigator', 'kids_anime.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Anime TV Shows[/COLOR][B][COLOR deepskyblue] •[/COLOR][/B]', 'animetvNavigator', 'kids_anime2.png', 'DefaulTVShows.png')        

        self.endDirectory()

    def kidsmovies(self, lite=False):       
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Randomly Plays[/COLOR]', 'randomNavigator', 'kids_random.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Kids Trending[/COLOR]', 'movies&url=advancedsearchtrending', 'kids_trending.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Animated Movies[/COLOR]', 'movies&url=advancedsearchanimation', 'kids_animated.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Kids Boxsets[/COLOR]', 'kidsboxsetsNavigator', 'kids_boxsets.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Top 10.000[/COLOR]', 'movies&url=advancedsearchtop10000', 'kids_top10000.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Walt Disney[/COLOR]', 'waltdisneyNavigator', 'kids_disney.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Dreamworks[/COLOR]', 'movies&url=advancedsearchdreamworks', 'kids_dreamworks.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Kids Horror[/COLOR]', 'movies&url=advancedsearchkidshorror', 'kids_horror.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Just Lego[/COLOR]', 'movies&url=advancedsearchjustlego', 'kids_lego.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Teen Movies[/COLOR]', 'movies&url=https://api.trakt.tv/users/acerider/lists/movies-teen/items', 'kids_teen.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Gamers[/COLOR]', 'movies&url=advancedsearchgamers', 'kids_gamers.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Superhero Movies[/COLOR]', 'superheroNavigator', 'kids_superhero.png', 'DefaultMovies.png')
                        
        self.endDirectory()

    def random(self, lite=False):
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Disney Animation[/COLOR]', 'random&rtype=movie&url=advancedsearchdisneyland', 'kids_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Disney Pixar[/COLOR]', 'random&rtype=movie&url=advancedsearchpixar', 'kids_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Dreamworks[/COLOR]', 'random&rtype=movie&url=advancedsearchdreamworks', 'kids_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Superheroes[/COLOR]', 'random&rtype=movie&url=advancedsearchdcvsmarvel', 'kids_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Family Movies[/COLOR]', 'random&rtype=movie&url=advancedsearchtrending', 'kids_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Childrens Horror[/COLOR]', 'random&rtype=movie&url=advancedsearchkidshorror', 'kids_random.png', 'DefaultRecentlyAddedMovies.png')
                
        self.endDirectory()

    def randomflix(self, lite=False):
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Action[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixaction', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Adventure[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixadventure', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Animation[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixanimation', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Biography[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixbiography', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Comedy[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixcomedy', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Crime[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixcrime', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Documentary[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixdocumentary', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Drama[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixdrama', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Family[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixfamily', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Fantasy[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixfantasy', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Film Noir[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixfilmnoir', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random History[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixhistory', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Horror[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixhorror', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Music[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixmusic', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Musical[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixmusical', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Mystery[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixmystery', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Romance[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixromance', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random SciFi[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixscifi', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Short[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixshort', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Sport[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixsport', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Superhero[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixsuperhero', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Thriller[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixthriller', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random War[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixwar', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Random Western[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixwestern', 'random_movies.png', 'DefaultRecentlyAddedMovies.png')
                
        self.endDirectory()    
        
    def kidsboxsets(self, lite=False):
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]3 Ninjas[/COLOR] [COLOR deepskyblue] (1992-1998)[/COLOR]', 'collections&url=advancedsearchninja', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]101 Dalmations[/COLOR] [COLOR deepskyblue] (1968-2003)[/COLOR]', 'collections&url=advancedsearchonehundredonedalmations', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]A Goofy Movie[/COLOR] [COLOR deepskyblue] (1995-2000)[/COLOR]', 'collections&url=advancedsearchgoofy', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Aladdin[/COLOR] [COLOR deepskyblue] (1992-1996)[/COLOR]', 'collections&url=advancedsearchaladdin', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Alvin and the Chipmunks[/COLOR] [COLOR deepskyblue] (1987-2015)[/COLOR]', 'collections&url=advancedsearchalvin', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Angry Birds[/COLOR] [COLOR deepskyblue] (2016-2019)[/COLOR]', 'collections&url=advancedsearchbirds', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Atlantis[/COLOR] [COLOR deepskyblue] (2001-2003)[/COLOR]', 'collections&url=advancedsearchatlantis', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Babe[/COLOR] [COLOR deepskyblue] (1995-1998)[/COLOR]', 'collections&url=advancedsearchbabe', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Back to the Future[/COLOR] [COLOR deepskyblue] (1985-1990)[/COLOR]', 'collections&url=advancedsearchfuture', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Beauty and the Beast[/COLOR] [COLOR deepskyblue] (1991-2017)[/COLOR]', 'collections&url=advancedsearchbeautyandthebeast', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Beethoven[/COLOR] [COLOR deepskyblue] (1992-2014)[/COLOR]', 'collections&url=advancedsearchbeethoven', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Brother Bear[/COLOR] [COLOR deepskyblue] (2003-2006)[/COLOR]', 'collections&url=advancedsearchbear', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Cars[/COLOR] [COLOR deepskyblue] (2006-2017)[/COLOR]', 'collections&url=advancedsearchcars', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Chronicles of Narnia[/COLOR] [COLOR deepskyblue] (2005-2010)[/COLOR]', 'collections&url=advancedsearchnarnia', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Cinderella[/COLOR] [COLOR deepskyblue] (1950-2007)[/COLOR]', 'collections&url=advancedsearchcinderella', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Cloudy with a Chance of Meatballs[/COLOR] [COLOR deepskyblue] (2009-2013)[/COLOR]', 'collections&url=advancedsearchcloudy', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Despicable Me[/COLOR] [COLOR deepskyblue] (2010-2017)[/COLOR]', 'collections&url=advancedsearchdespicable', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Diary of a Wimpy Kid[/COLOR] [COLOR deepskyblue] (2010-2017)[/COLOR]', 'collections&url=advancedsearchwimpy', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Emperors New Groove[/COLOR] [COLOR deepskyblue] (2000-2005)[/COLOR]', 'collections&url=advancedsearchemperor', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Fantastic Beasts[/COLOR] [COLOR deepskyblue] (2016-2018)[/COLOR]', 'collections&url=advancedsearchbeasts', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Finding Nemo[/COLOR] [COLOR deepskyblue] (2003-2016)[/COLOR]', 'collections&url=advancedsearchnemo', 'kids_boxsets.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Fox and the Hound[/COLOR] [COLOR deepskyblue] (1981-2006)[/COLOR]', 'collections&url=advancedsearchfoxandthehound', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Free Willy[/COLOR] [COLOR deepskyblue] (1993-2010)[/COLOR]', 'collections&url=advancedsearchfreewilly', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Frozen[/COLOR] [COLOR deepskyblue] (2013-2019)[/COLOR]', 'collections&url=advancedsearchfrozen', 'kids_boxsets.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Ghostbusters[/COLOR] [COLOR deepskyblue] (1984-2016)[/COLOR]', 'collections&url=advancedsearchghostbusters', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Gremlins[/COLOR] [COLOR deepskyblue] (1984-1990)[/COLOR]', 'collections&url=advancedsearchgremlins', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]G.I. Joe[/COLOR] [COLOR deepskyblue] (2009-2013)[/COLOR]', 'collections&url=advancedsearchgijoe', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Gnomeo & Juliet[/COLOR] [COLOR deepskyblue] (2011-2018)[/COLOR]', 'collections&url=advancedsearchgnomes', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Goosebumps[/COLOR] [COLOR deepskyblue] (2015-2018)[/COLOR]', 'collections&url=advancedsearchgoosebumps', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Happy Feet[/COLOR] [COLOR deepskyblue] (2006-2011)[/COLOR]', 'collections&url=advancedsearchfeet', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Harry Potter[/COLOR] [COLOR deepskyblue] (2001-2009)[/COLOR]', 'collections&url=advancedsearchharry', 'kids_boxsets.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Home Alone[/COLOR] [COLOR deepskyblue] (1990-2012)[/COLOR]', 'collections&url=advancedsearchhomealone', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Honey, I Shrunk the Kids[/COLOR] [COLOR deepskyblue] (1989-1997)[/COLOR]', 'collections&url=advancedsearchshrunk', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Hoodwinked[/COLOR] [COLOR deepskyblue] (2005-2011)[/COLOR]', 'collections&url=advancedsearchhoodwinked', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Hotel Transylvania[/COLOR] [COLOR deepskyblue] (2012-2018)[/COLOR]', 'collections&url=advancedsearchtransylvania', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]How to Train Your Dragon[/COLOR] [COLOR deepskyblue] (2010-2019)[/COLOR]', 'collections&url=advancedsearchdragon', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Hunchback of Notre Dame[/COLOR] [COLOR deepskyblue] (1996-2002)[/COLOR]', 'collections&url=advancedsearchhunchbackofnotredame', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Ice Age[/COLOR] [COLOR deepskyblue] (2002-2016)[/COLOR]', 'collections&url=advancedsearchice', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Jurassic Park[/COLOR] [COLOR deepskyblue] (1993-2018)[/COLOR]', 'collections&url=advancedsearchjurassic', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Kung Fu Panda[/COLOR] [COLOR deepskyblue] (2008-2016)[/COLOR]', 'collections&url=advancedsearchpanda', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Lady and the Tramp[/COLOR] [COLOR deepskyblue] (1955-2001)[/COLOR]', 'collections&url=advancedsearchlady', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Lilo & Stitch[/COLOR] [COLOR deepskyblue] (2002-2005)[/COLOR]', 'collections&url=advancedsearchlilo', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Madagascar[/COLOR] [COLOR deepskyblue] (2005-2014)[/COLOR]', 'collections&url=advancedsearchmad', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Men in Black[/COLOR] [COLOR deepskyblue] (1997-2019)[/COLOR]', 'collections&url=advancedsearchmib', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Minions[/COLOR] [COLOR deepskyblue] (2015-2020)[/COLOR]', 'collections&url=advancedsearchminions', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Monsters, inc.[/COLOR] [COLOR deepskyblue] (2001-2013)[/COLOR]', 'collections&url=advancedsearchmonsters', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Mulan[/COLOR] [COLOR deepskyblue] (1998-2004)[/COLOR]', 'collections&url=advancedsearchmulan', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Nanny McPhee[/COLOR] [COLOR deepskyblue] (2005-2010)[/COLOR]', 'collections&url=advancedsearchnanny', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Narnia[/COLOR] [COLOR deepskyblue] (2005-2010)[/COLOR]', 'collections&url=advancedsearchnarnia', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]New Groove[/COLOR] [COLOR deepskyblue] (2000-2005)[/COLOR]', 'collections&url=advancedsearchnewgroove', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Night at the Museum[/COLOR] [COLOR deepskyblue] (2006-2014)[/COLOR]', 'collections&url=advancedsearchmuseum', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Nut Job[/COLOR] [COLOR deepskyblue] (2014-2017)[/COLOR]', 'collections&url=advancedsearchnut', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Open Season[/COLOR] [COLOR deepskyblue] (2006-2015)[/COLOR]', 'collections&url=advancedsearchopen', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Paddington Bear[/COLOR] [COLOR deepskyblue] (2014-2017)[/COLOR]', 'collections&url=advancedsearchpadd', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Percy Jackson[/COLOR] [COLOR deepskyblue] (2010-2013)[/COLOR]', 'collections&url=advancedsearchpercy', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Pirates of the Caribbean[/COLOR] [COLOR deepskyblue] (2003-2017)[/COLOR]', 'collections&url=advancedsearchpirates', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Planes[/COLOR] [COLOR deepskyblue] (2013-2014)[/COLOR]', 'collections&url=advancedsearchplanes', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Pocahontas[/COLOR] [COLOR deepskyblue] (1995-1998)[/COLOR]', 'collections&url=advancedsearchpocahontas', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Pokémon[/COLOR] [COLOR deepskyblue] (1998-2019)[/COLOR]', 'collections&url=advancedsearchpokemon', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Problem Child[/COLOR] [COLOR deepskyblue] (1990-1995)[/COLOR]', 'collections&url=advancedsearchproblemchild', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Rio[/COLOR] [COLOR deepskyblue] (2011-2014)[/COLOR]', 'collections&url=advancedsearchrio', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Sammys Adventures[/COLOR] [COLOR deepskyblue] (2010-2012)[/COLOR]', 'collections&url=advancedsearchsammysadventures', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Scooby-Doo[/COLOR] [COLOR deepskyblue] (2002-2014)[/COLOR]', 'collections&url=advancedsearchscoobydoo', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Short Circuit[/COLOR] [COLOR deepskyblue] (1986-1988)[/COLOR]', 'collections&url=advancedsearchshortcircuit', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png') 
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Shaun the Sheep[/COLOR] [COLOR deepskyblue] (2015-2019)[/COLOR]', 'collections&url=advancedsearchsheep', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Shrek[/COLOR] [COLOR deepskyblue] (2001-2010)[/COLOR]', 'collections&url=advancedsearchshrek', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Smurfs[/COLOR] [COLOR deepskyblue] (2011-2017)[/COLOR]', 'collections&url=advancedsearchsmurf', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]SpongeBob SquarePants[/COLOR] [COLOR deepskyblue] (2004-2017)[/COLOR]', 'collections&url=advancedsearchspongebobsquarepants', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Spy Kids[/COLOR] [COLOR deepskyblue] (2001-2011)[/COLOR]', 'collections&url=advancedsearchspykids', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Star Wars[/COLOR] [COLOR deepskyblue] (1977-2018)[/COLOR]', 'collections&url=advancedsearchstarwars', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Stuart Little[/COLOR] [COLOR deepskyblue] (1999-2002)[/COLOR]', 'collections&url=advancedsearchstuartlittle', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Surfs Up[/COLOR] [COLOR deepskyblue] (2007-2017)[/COLOR]', 'collections&url=advancedsearchsurf', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Tarzan[/COLOR] [COLOR deepskyblue] (1999-2002)[/COLOR]', 'collections&url=advancedsearchtarzan', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Tinker Bell[/COLOR] [COLOR deepskyblue] (2007-2020)[/COLOR]', 'collections&url=advancedsearchtinker', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]The Addams Family[/COLOR] [COLOR deepskyblue] (1991-1993)[/COLOR]', 'collections&url=advancedsearchaddams', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]The Flintstones[/COLOR] [COLOR deepskyblue] (1994-2000)[/COLOR]', 'collections&url=advancedsearchflint', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]The Incredibles[/COLOR] [COLOR deepskyblue] (2004-2018)[/COLOR]', 'collections&url=advancedsearchincredibles', 'kids_boxsets.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]The Jungle Book[/COLOR] [COLOR deepskyblue] (1967-2003)[/COLOR]', 'collections&url=advancedsearchthejunglebook', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]The Karate Kid[/COLOR] [COLOR deepskyblue] (1984-2010)[/COLOR]', 'collections&url=advancedsearchthekaratekid', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]The Land Before Time[/COLOR] [COLOR deepskyblue] (1988-2007)[/COLOR]', 'collections&url=advancedsearchland', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]The Lion King[/COLOR] [COLOR deepskyblue] (1994-2019)[/COLOR]', 'collections&url=advancedsearchking', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]The Little Mermaid[/COLOR] [COLOR deepskyblue] (1989-1995)[/COLOR]', 'collections&url=advancedsearchthelittlemermaid', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]The Mighty Ducks[/COLOR] [COLOR deepskyblue] (1992-1996)[/COLOR]', 'collections&url=advancedsearchducks', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]The Mummy[/COLOR] [COLOR deepskyblue] (1999-2017)[/COLOR]', 'collections&url=advancedsearchmummy', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]The Neverending Story[/COLOR] [COLOR deepskyblue] (1984-1994)[/COLOR]', 'collections&url=advancedsearchtheneverendingstory', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]The Secret Life of Pets[/COLOR] [COLOR deepskyblue] (2016-2019)[/COLOR]', 'collections&url=advancedsearchpets', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]The Smurfs[/COLOR] [COLOR deepskyblue] (2011-2013)[/COLOR]', 'collections&url=advancedsearchthesmurfs', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Tooth Fairy[/COLOR] [COLOR deepskyblue] (2010-2012)[/COLOR]', 'collections&url=advancedsearchtoothfairy', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]TMNT[/COLOR] [COLOR deepskyblue] (1978-2019)[/COLOR]', 'collections&url=advancedsearchtmnt', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Tom and Jerry[/COLOR] [COLOR deepskyblue] (1992-2013)[/COLOR]', 'collections&url=advancedsearchtomandjerry', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Toy Story[/COLOR] [COLOR deepskyblue] (1995-2019)[/COLOR]', 'collections&url=advancedsearchtoystory', 'kids_boxsets.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Transformers[/COLOR] [COLOR deepskyblue] (1986-2017)[/COLOR]', 'collections&url&url=advancedsearchtransformers', 'kids_boxsets.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]VeggieTales[/COLOR] [COLOR deepskyblue] (2002-2008)[/COLOR]', 'collections&url=advancedsearchveggietales', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Winnie the Pooh[/COLOR] [COLOR deepskyblue] (2000-2005)[/COLOR]', 'collections&url=advancedsearchwinniethepooh', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Wizard of Oz[/COLOR] [COLOR deepskyblue] (1939-2013)[/COLOR]', 'collections&url=advancedsearchwizardofoz', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Wreck it Ralph[/COLOR] [COLOR deepskyblue] (2012-2018)[/COLOR]', 'collections&url=advancedsearchralph', 'kids_boxsets.png', 'DefaultRecentlyAddedMovies.png')
        
        self.endDirectory()

    def waltdisney(self, lite=False):
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Disney Pixar[/COLOR]', 'movies&url=advancedsearchpixar', 'kids_disney2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Disney Nature[/COLOR]', 'movies&url=advancedsearchnature', 'kids_disney2.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Disney Animation[/COLOR]', 'movies&url=advancedsearchdisneyland', 'kids_disney2.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Disney Movie TV[/COLOR]', 'movies&url=advancedsearchdisneymovietv', 'kids_disney2.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Disney Live Action[/COLOR]', 'movies&url=advancedsearchliveaction', 'kids_disney2.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Disney Chronological[/COLOR]', 'movies&url=advancedsearchchronological', 'kids_disney2.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()
                    
    def superhero(self, lite=False):
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Action Hero[/COLOR]', 'movies&url=collectionsactionhero', 'kids_superhero.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]DC vs Marvel[/COLOR]', 'movies&url=advancedsearchdcvsmarvel', 'kids_dcvsmarvel.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Marvel Studios[/COLOR]', 'movies&url=advancedsearchmarvelstudios', 'kids_marvel.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]DC Universe[/COLOR]', 'movies&url=advancedsearchdcuniverse', 'kids_dc.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Marvel Animated[/COLOR]', 'movies&url=advancedsearchmarvelanimation', 'kids_marvel3.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]DC Animated[/COLOR]', 'movies&url=advancedsearchdcanimation', 'kids_dc2.png', 'DefaultMovies.png')

        self.endDirectory()

    def kidstvshows(self, lite=False):
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Popular Cartoons[/COLOR]', 'tvshows&url=advancedsearchcartoons', 'kids_cartoons.png', 'DefaultTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Trending Shows[/COLOR]', 'tvshows&url=advancedsearchfamily', 'kids_trending.png', 'DefaultTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Retro TV Series[/COLOR]', 'tvshows&url=advancedsearchretro', 'kids_retro.png', 'DefaultTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Family TV Series[/COLOR]', 'tvshows&url=advancedsearchhighly', 'kids_family.png', 'DefaultTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Popular Networks[/COLOR]', 'tvNetworksKids', 'kids_networks.png', 'DefaultTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Teen TV Networks[/COLOR]', 'teentvNavigator', 'kids_teen.png', 'DefaulTVShows.png') 
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Marvel TV[/COLOR]', 'tvshows&url=advancedsearchmarveltv', 'kids_marvel2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Lego TV[/COLOR]', 'tvshows&url=advancedsearchlegotv', 'kids_lego2.png', 'DefaulTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Transformers TV[/COLOR]', 'tvshows&url=advancedsearchtransformers', 'kids_transformers.png', 'DefaulTVShows.png')
        
        self.endDirectory()
    
    def toddlertv(self, lite=False):
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Disney Jr Shows[/COLOR]', 'tvshows&url=advancedsearchdisneyjr', 'kids_youngsters2.png', 'DefaulTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Nick Jr Shows[/COLOR]', 'tvshows&url=advancedsearchnickjr', 'kids_youngsters2.png', 'DefaulTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Netflix Shows[/COLOR]', 'tvshows&url=advancedsearchnetflixkids', 'kids_youngsters2.png', 'DefaulTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Highly Rated[/COLOR]', 'tvshows&url=advancedsearchtoddler', 'kids_youngsters2.png', 'DefaultTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Learning TV[/COLOR]', 'learningtv', 'kids_youngsters2.png', 'DefaultMovies.png')
        
        self.endDirectory()
        
    def teentv(self, lite=False):
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Freeform[/COLOR]', 'tvshows&url=advancedsearchfreeformtv', 'kids_teen.png', 'DefualtTVshows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Teen TV Shows[/COLOR]', 'tvshows&url=advancedsearchteentv', 'kids_teen.png', 'DefualtTVshows.png')
                
        self.endDirectory()

    def animemovies(self, lite=False):
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Trending Anime[/COLOR]', 'movies&url=advancedsearchanimetrending', 'kids_anime.png', 'Defaultanimemovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Highly Rated[/COLOR]', 'movies&url=advancedsearchanimehighlyrated', 'kids_anime.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Restricted Rated[/COLOR]', 'movies&url=advancedsearchanimegrownup', 'kids_anime.png', 'Defaultanimemovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Top Anime Movies[/COLOR]', 'movies&url=advancedsearchanimemostviewed', 'kids_anime.png', 'Defaultanimemovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Search Anime Movies[/COLOR]', 'movieSearch', 'search4.png', 'DefaultTVShows.png')
        
        self.endDirectory()
        
    def animetvshows(self, lite=False):
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Trending Anime[/COLOR]', 'tvshows&url=advancedsearchanimetrending', 'kids_anime2.png', 'playlist.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Highly Rated[/COLOR]', 'tvshows&url=advancedsearchanimehighlyrated', 'kids_anime2.png', 'DefaultTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Popular Anime[/COLOR]', 'tvshows&url=advancedsearchanimepopular', 'kids_anime2.png', 'DefaultTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]People Watching[/COLOR]', 'tvshows&url=advancedsearchanimepeoplewatching', 'kids_anime2.png', 'DefaultTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Top Anime Series[/COLOR]', 'tvshows&url=advancedsearchanimetopseries', 'kids_anime2.png', 'DefaultTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Anime Genres[/COLOR]', 'animeGenres', 'kids_anime2.png', 'DefaultTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Search Anime Series[/COLOR]', 'tvSearch', 'search4.png', 'DefaultTVShows.png')
        
        self.endDirectory()

    def system(self, lite=False):
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Accounts[/COLOR][/B]', 'accountsrd', 'icon2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Settings[/COLOR][/B]', 'allsettingsNavigator', 'icon2.png', 'DefaultTVShows.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Tools[/COLOR][/B]', 'alltoolsNavigator', 'icon2.png', 'DefaulTVShows.png')        

        self.endDirectory()
        
    def allsettings(self, lite=False):
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Resolver Settings[/COLOR][/B]', 'ResolveurlRDTorrent', 'icon2.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]RD Providers[/COLOR][/B]', 'openSettings&query=4.1', 'icon2.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Providers[/COLOR][/B]', 'openSettings&query=3.0', 'icon2.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]General[/COLOR][/B]', 'openSettings&query=0.0', 'icon2.png', 'DefaultAddonProgram.png')        

        self.endDirectory()
        
    def alltools(self, lite=False):
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Library[/COLOR][/B]', 'libraryNavigator', 'icon2.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Viewtypes[/COLOR][/B]', 'viewsNavigator', 'icon2.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Clear cache...[/COLOR][/B]', 'clearCache', 'icon2.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Clear providers...[/COLOR][/B]', 'clearSources', 'icon2.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Clear search history...[/COLOR][/B]', 'clearCacheSearch', 'icon2.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Clear Meta cache...[/COLOR][/B]', 'clearMetaCache', 'icon2.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Clear all cache[/COLOR][/B]', 'clearAllCache', 'icon2.png', 'DefaultAddonProgram.png')        

        self.endDirectory()                                               
            

    def endDirectory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


