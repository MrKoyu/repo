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
 
import os,sys,urlparse,xbmc,xbmcaddon,xbmcgui,base64,urllib2

from resources.lib.dialogs import notification
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
    ADDON_ID      = xbmcaddon.Addon().getAddonInfo('id')
    HOMEPATH      = xbmc.translatePath('special://home/')
    ADDONSPATH    = os.path.join(HOMEPATH, 'addons')
    THISADDONPATH = os.path.join(ADDONSPATH, ADDON_ID)
    NEWSFILE      = base64.b64decode(b'aHR0cHM6Ly9jZWxsYXJkb29ydHYuY29tL251bWJlcnMvY2hhbmdlbG9nL2NoYW5nZWxvZy54bWw=')
    LOCALNEWS     = os.path.join(THISADDONPATH, 'information.txt')

    def root(self):
        if self.getMenuEnabled('navi.movies') == True:
            self.addDirectoryItem(32001, 'movieNavigator', 'home_movies.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.tvshows') == True:
            self.addDirectoryItem(32002, 'tvNavigator', 'home_tvshows.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.kidzone') == True:    
            self.addDirectoryItem(70004, 'kidzoneNavigator', 'home_kids.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.collections') == True: 
            self.addDirectoryItem(32711, 'collectionsNavigator', 'home_collections.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.tvNetworks') == True:
            self.addDirectoryItem(32708, 'tvNetworks', 'home_networks.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.boxsetKings') == True:     
            self.addDirectoryItem(32709, 'boxsetKingsNavigator', 'home_boxsets.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.docu') == True:         
            self.addDirectoryItem(32700, 'docuMainNavigator', 'home_documentaries.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.247') == True:         
            self.addDirectoryItem(32713, '247', 'home_247.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.music') == True: 
            self.addDirectoryItem(32727, 'musicMainNavigator', 'home_music.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.fitness') == True: 
            self.addDirectoryItem(32728, 'athleanx', 'home_fitness.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.screensaver') == True:     
            self.addDirectoryItem(32729, 'screensaver', 'home_screensaver.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.knowledge') == True:     
            self.addDirectoryItem(32730, 'knowledge', 'home_learning.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.ufc') == True:     
            self.addDirectoryItem(32731, 'ufc', 'home_sports.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.food') == True:     
            self.addDirectoryItem(90016, 'food', 'home_food.png', 'DefaultMovies.png')        
        if self.getMenuEnabled('navi.jens') == True:     
            self.addDirectoryItem(32734, 'jens', 'home_jen.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.personal.list') == True:
            self.addDirectoryItem(90009, 'jenlist1', 'home_myaddon.png', 'userlists.png')
        adult = True if control.setting('adult_pw') == 'PORN4ALL' else False
        if adult == True:
            self.addDirectoryItem(90012, 'xxx', 'home_iPunheta.png', 'DefaultMovies.png')        
        if self.getMenuEnabled('navi.system') == True:     
            self.addDirectoryItem(32008, 'systemNavigator', 'tools.png', 'DefaultTVShows.png')        

        self.addDirectoryItem(32010, 'searchNavigator', 'search5.png', 'DefaultFolder.png')

        self.endDirectory()

    def getMenuEnabled(self, menu_title):
        is_enabled = control.setting(menu_title).strip()
        if (is_enabled == '' or is_enabled == 'false'): return False
        return True

    def news(self):
            message=self.open_news_url(self.NEWSFILE)
            r = open(self.LOCALNEWS)
            compfile = r.read()       
            if len(message)>1:
                    if compfile == message:pass
                    else:
                            text_file = open(self.LOCALNEWS, "w")
                            text_file.write(message)
                            text_file.close()
                            compfile = message
            self.showText('NuMb3r5 Information:', compfile)

    def open_news_url(self, url):
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'klopp')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            print link
            return link

    def showText(self, heading, text):
        id = 10147
        xbmc.executebuiltin('ActivateWindow(%d)' % id)
        xbmc.sleep(500)
        win = xbmcgui.Window(id)
        retry = 50
        while (retry > 0):
            try:
                xbmc.sleep(10)
                retry -= 1
                win.getControl(1).setLabel(heading)
                win.getControl(5).setText(text)
                quit()
                return
            except: pass
    
    def movies(self, lite=False):
        self.addDirectoryItem(32003, 'mymovieliteNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')
        if self.getMenuEnabled('navi.eimMovies') == True:
            self.addDirectoryItem(32714, 'eimportalmovies', 'movies_portal.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.randomMovies') == True:
            self.addDirectoryItem(32726, 'randomMoviesNavigator', 'movies_random.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.eyecandy') == True:
            self.addDirectoryItem(32732, 'eyecandy', 'movies_eyecandy.png', 'DefaultMovies.png') 
        if self.getMenuEnabled('navi.movieTheaters') == True:
            self.addDirectoryItem(32022, 'movies&url=theaters', 'movies_theaters.png', 'DefaultRecentlyAddedMovies.png')
        if self.getMenuEnabled('navi.movieTrending') == True:
            self.addDirectoryItem(32017, 'movies&url=trending', 'movies_watching.png', 'DefaultRecentlyAddedMovies.png')
        if self.getMenuEnabled('navi.movieGenres') == True:
            self.addDirectoryItem(32011, 'movieGenres', 'movies_genres.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.collectionsTop1000c') == True:
            self.addDirectoryItem(32715, 'movies&url=collectionstop1000c', 'movies_mytop1000.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movieYears') == True:
            self.addDirectoryItem(32012, 'movieYears', 'movies_years.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movieLanguages') == True:
            self.addDirectoryItem(32014, 'movieLanguages', 'movies_international.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviePersons') == True:
            self.addDirectoryItem(32013, 'moviePersons', 'movies_people.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviePopular') == True:
            self.addDirectoryItem(32018, 'movies&url=popular', 'movies_popular.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movieRomance') == True:
            self.addDirectoryItem(32716, 'movies&url=romance', 'movies_romance.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.marvel') == True:
            self.addDirectoryItem(32717, 'movies&url=marvel', 'movies_marvel.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.dc') == True:
            self.addDirectoryItem(32718, 'movies&url=dcmovies', 'movies_dc2.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.horror') == True:
            self.addDirectoryItem(32720, 'movies&url=tophorr', 'movies_horror.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.horror2') == True:
            self.addDirectoryItem(32721, 'movies&url=horror', 'movies_horror2.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.standup') == True:
            self.addDirectoryItem(32722, 'movies&url=standup', 'movies_standup.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.mostVoted') == True:
            self.addDirectoryItem(32019, 'movies&url=views', 'movies_voted.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.boxoffice') == True:
            self.addDirectoryItem(32020, 'movies&url=boxoffice', 'movies_ticket.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.oscars') == True:
            self.addDirectoryItem(32021, 'movies&url=oscars', 'movies_oscar.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movieLatest') == True:
            self.addDirectoryItem(32005, 'movieWidget', 'movies_latest.png', 'DefaultRecentlyAddedMovies.png')                    
        #self.addDirectoryItem(32028, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
        self.addDirectoryItem(32010, 'movieSearch', 'search1.png', 'DefaultMovies.png')

        self.endDirectory()


    def mymovies(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(90017, 'movies&url=onDeck', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)

        elif traktCredentials == True:
            self.addDirectoryItem(90017, 'movies&url=onDeck', 'trakt.png', 'DefaultMovies.png')
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
            self.addDirectoryItem(32031, 'movieliteNavigator', 'mymovies.png', 'DefaultMovies.png')
            #self.addDirectoryItem(32028, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'search1.png', 'DefaultMovies.png')

        self.endDirectory()


    def tvshows(self, lite=False):
        self.addDirectoryItem(32004, 'mytvliteNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')
        if self.getMenuEnabled('navi.eimShows') == True:
            self.addDirectoryItem(32723, 'eimportalshows', 'tv_portal.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.top250tv') == True:
            self.addDirectoryItem(32724, 'tvshows&url=top250tv', 'tv_imdb250.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.netflix') == True:
            self.addDirectoryItem(32725, 'tvshows&url=advancedsearchnetflixshows', 'tv_netflix.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.appletv') == True:
            self.addDirectoryItem(32733, 'tvshows&url=https://api.trakt.tv/users/mediashare2000/lists/apple-tv/items', 'tv_apple.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvGenres') == True:
            self.addDirectoryItem(32701, 'tvGenres', 'tv_genres.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvLanguages') == True:
            self.addDirectoryItem(32702, 'tvLanguages', 'tv_international.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvtrending') == True:
            self.addDirectoryItem(32704, 'tvshows&url=trending', 'tv_watching.png', 'DefaultRecentlyAddedEpisodes.png')
        if self.getMenuEnabled('navi.tvpopular') == True:
            self.addDirectoryItem(32705, 'tvshows&url=popular', 'tv_popular.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvhighlyRated') == True:
            self.addDirectoryItem(32023, 'tvshows&url=rating', 'tv_rated.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvmostVoted') == True:
            self.addDirectoryItem(32706, 'tvshows&url=views', 'tv_voted.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvairingToday') == True:
            self.addDirectoryItem(32024, 'tvshows&url=airing', 'tv_airing.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvreturningShows') == True:
            self.addDirectoryItem(32025, 'tvshows&url=active', 'tv_returning.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvnewShows') == True:
            self.addDirectoryItem(32026, 'tvshows&url=premiere', 'tv_latest.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32006, 'calendar&url=added', 'tv_episodes.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
        self.addDirectoryItem(32027, 'calendars', 'tv_calendar.png', 'DefaultRecentlyAddedEpisodes.png')
        #self.addDirectoryItem(32707, 'tvPerson', 'people-search2.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32010, 'tvSearch', 'search2.png', 'DefaultTVShows.png')

        self.endDirectory()


    def mytvshows(self, lite=False):
        try:
            self.accountCheck()

            if traktCredentials == True and imdbCredentials == True:
                self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
                self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
                self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')

            elif traktCredentials == True:
                self.addDirectoryItem(90017, 'calendar&url=onDeck', 'trakt.png', 'DefaultTVShows.png')
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
                self.addDirectoryItem(32031, 'tvliteNavigator', 'mytvshows.png', 'DefaultTVShows.png')
                #self.addDirectoryItem(32028, 'tvPerson', 'people-search2.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32010, 'tvSearch', 'search2.png', 'DefaultTVShows.png')

            self.endDirectory()
        except:
            print("ERROR")


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
        self.addDirectoryItem(32557, 'openSettings&query=15.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'library_update.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32559, control.setting('library.movie'), 'library_movies.png', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem(32560, control.setting('library.tv'), 'library_tvshows.png', 'DefaultTVShows.png', isAction=False)

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
            self.addDirectoryItem(32001, movie_downloads, 'mymovies.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(32002, tv_downloads, 'mytvshows.png', 'DefaultTVShows.png', isAction=False)

        self.endDirectory()


    def search(self):
        self.addDirectoryItem(90018, 'movieSearch', 'search.png', 'DefaultMovies.png')
        self.addDirectoryItem(90019, 'tvSearch', 'search.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90020, 'moviePerson', 'search.png', 'DefaultMovies.png')
        #self.addDirectoryItem(32030, 'tvPerson', 'people-search2.png', 'DefaultTVShows.png')

        self.endDirectory()

    def views(self):
        try:
            control.idle()

            items = [ (control.lang(90021).encode('utf-8'), 'movies'), (control.lang(90022).encode('utf-8'), 'tvshows'), (control.lang(90023).encode('utf-8'), 'seasons'), (control.lang(90024).encode('utf-8'), 'episodes') ]

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
            notification.infoDialog(msg=control.lang(32042).encode('utf-8'), style='WARNING')
            sys.exit()


    def infoCheck(self, version):
        try:
            notification.infoDialog(msg=control.lang(32074).encode('utf-8'), timer=5000)
            return '1'
        except:
            return '1'


    def clearCache(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear()
        notification.infoDialog(msg=control.lang(32610).encode('utf-8'), style='ERROR')

    def clearCacheMeta(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_meta()
        notification.infoDialog(msg=control.lang(32612).encode('utf-8'), style='ERROR')

    def clearCacheProviders(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_providers()
        notification.infoDialog(msg=control.lang(32057).encode('utf-8'), style='INFO')

    def clearCacheSearch(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_search()
        notification.infoDialog(msg=control.lang(32611).encode('utf-8'), style='ERROR')

    def clearCacheAll(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_all()
        notification.infoDialog(msg=control.lang(32620).encode('utf-8'), style='INFO')

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
        self.addDirectoryItem('[B][COLOR darkorange]• [/COLOR][/B][COLOR ghostwhite]Hallmark Collection[/COLOR][B][COLOR darkorange] •[/COLOR][/B]', 'movies&url=collectionswallmark', 'collections_hallmark.png', 'DefaultMovies.png')
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
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Boxset Kings[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'collectionBoxset', 'boxsets.png', 'boxsets1.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Boxset Genres[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'boxsetsNavigator', 'boxsets.png', 'boxsets1.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Boxsets[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'tvshows&url=popular', 'boxsets1.png', 'boxsets1.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Boxset Genres[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'boxsetgenres', 'boxsets1.png', 'boxsets1.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Search[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'movieSearch', 'search3.png', 'boxsets_search.png')
        
        self.endDirectory()

    def documain(self, lite=False):
        self.addDirectoryItem('[B][COLOR limegreen]• [/COLOR][/B][COLOR ghostwhite]Random Play[/COLOR][B][COLOR limegreen] •[/COLOR][/B]', 'random&rtype=movie&url=advancedsearchrandomflixdocumentary', 'doc_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR limegreen]• [/COLOR][/B][COLOR ghostwhite]DocuHeaven[/COLOR][B][COLOR limegreen] •[/COLOR][/B]', 'docuHeaven', 'doc_heaven.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR limegreen]• [/COLOR][/B][COLOR ghostwhite]Russell Brand[/COLOR][B][COLOR limegreen] •[/COLOR][/B]', 'russell', 'doc_russell.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR limegreen]• [/COLOR][/B][COLOR ghostwhite]DocuTube[/COLOR][B][COLOR limegreen] •[/COLOR][/B]', 'docutube', 'doc_utube.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR limegreen]• [/COLOR][/B][COLOR ghostwhite]Search[/COLOR][B][COLOR limegreen] •[/COLOR][/B]', 'tvSearch', 'search6.png', 'DefaultTVShows.png')
        
        self.endDirectory()

    def musicmain(self, lite=False):
        self.addDirectoryItem('[B][COLOR ffdaff4d]• [/COLOR][/B][COLOR ghostwhite]Radio[/COLOR][B][COLOR ffdaff4d] •[/COLOR][/B]', 'musicradioMainNavigator2', 'music_radio.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR ffdaff4d]• [/COLOR][/B][COLOR ghostwhite]Meditative[/COLOR][B][COLOR ffdaff4d] •[/COLOR][/B]', 'meditativemind', 'music_meditative.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR ffdaff4d]• [/COLOR][/B][COLOR ghostwhite]Techno Head[/COLOR][B][COLOR ffdaff4d] •[/COLOR][/B]', 'technohead', 'music_technohead.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR ffdaff4d]• [/COLOR][/B][COLOR ghostwhite]Music Choice[/COLOR][B][COLOR ffdaff4d] •[/COLOR][/B]', 'musicchoice', 'music_mc.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR ffdaff4d]• [/COLOR][/B][COLOR ghostwhite]Music Channels[/COLOR][B][COLOR ffdaff4d] •[/COLOR][/B]', 'musicchannels', 'music_channels.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR ffdaff4d]• [/COLOR][/B][COLOR ghostwhite]Music Videos[/COLOR][B][COLOR ffdaff4d] •[/COLOR][/B]', 'musicvideos', 'music_videos.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR ffdaff4d]• [/COLOR][/B][COLOR ghostwhite]Now Music[/COLOR][B][COLOR ffdaff4d] •[/COLOR][/B]', 'nowmusic', 'music_nowmusic2.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR ffdaff4d]• [/COLOR][/B][COLOR ghostwhite]Random Play[/COLOR][B][COLOR ffdaff4d] •[/COLOR][/B]', 'musicRandomMainNavigator', 'music_random.png', 'DefaultMovies.png')
        
        self.endDirectory()

    def musicradiomain(self, lite=False):
        self.addDirectoryItem('[B][COLOR ffdaff4d]• [/COLOR][/B][COLOR ghostwhite]World Radio[/COLOR][B][COLOR ffdaff4d] •[/COLOR][/B]', 'worldradio', 'music_radio.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR ffdaff4d]• [/COLOR][/B][COLOR ghostwhite]The UK Radio[/COLOR][B][COLOR ffdaff4d] •[/COLOR][/B]', 'ukradio', 'music_radio.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR ffdaff4d]• [/COLOR][/B][COLOR ghostwhite]Music Choice Audio[/COLOR][B][COLOR ffdaff4d] •[/COLOR][/B]', 'mcaudio', 'music_radio.png', 'DefaultMovies.png')
        
        self.endDirectory()

    def musicrandommain(self, lite=False):
        self.addDirectoryItem('[B][COLOR ffdaff4d]• [/COLOR][/B][COLOR ghostwhite]Random Music[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixmusic', 'music_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR ffdaff4d]• [/COLOR][/B][COLOR ghostwhite]Random Musical[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixmusical', 'music_random.png', 'DefaultRecentlyAddedMovies.png')
        
        self.endDirectory()                                

    def sportsmain(self, lite=False):
        self.addDirectoryItem('[B][COLOR crimson]• [/COLOR][/B][COLOR ghostwhite]UFC Replays[/COLOR][B][COLOR crimson] •[/COLOR][/B]', 'ufc', 'home_sports.png', 'DefaultMovies.png')
        
        self.endDirectory()

    def fitnessmain(self, lite=False):
        self.addDirectoryItem('[B][COLOR ff9f00ff]• [/COLOR][/B][COLOR ghostwhite]ATHLEAN-X™[/COLOR][B][COLOR ff9f00ff] •[/COLOR][/B]', 'athleanx', 'home_fitness.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR ff9f00ff]• [/COLOR][/B][COLOR ghostwhite]Motivational[/COLOR][B][COLOR ff9f00ff] •[/COLOR][/B]', 'motivational', 'home_fitness.png', 'DefaultMovies.png')
        
        self.endDirectory()        

    def collectionBoxset(self):
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]48 Hrs.[/COLOR] [COLOR yellow] (1982-1990)[/COLOR]', 'collections&url=fortyeighthours', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Ace Ventura[/COLOR] [COLOR yellow] (1994-1995)[/COLOR]', 'collections&url=aceventura', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Airplane[/COLOR] [COLOR yellow] (1980-1982)[/COLOR]', 'collections&url=airplane', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Airport[/COLOR] [COLOR yellow] (1970-1979)[/COLOR]', 'collections&url=airport', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]American Graffiti[/COLOR] [COLOR yellow] (1973-1979)[/COLOR]', 'collections&url=americangraffiti', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Anaconda[/COLOR] [COLOR yellow] (1997-2004)[/COLOR]', 'collections&url=anaconda', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Analyze This[/COLOR] [COLOR yellow] (1999-2002)[/COLOR]', 'collections&url=analyzethis', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Anchorman[/COLOR] [COLOR yellow] (2004-2013)[/COLOR]', 'collections&url=anchorman', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Austin Powers[/COLOR] [COLOR yellow] (1997-2002)[/COLOR]', 'collections&url=austinpowers', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Avengers[/COLOR] [COLOR yellow] (2008-2017)[/COLOR]', 'collections&url=avengers', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Back to the Future[/COLOR] [COLOR yellow] (1985-1990)[/COLOR]', 'collections&url=backtothefuture', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Bad Boys[/COLOR] [COLOR yellow] (1995-2003)[/COLOR]', 'collections&url=badboys', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Bad Santa[/COLOR] [COLOR yellow] (2003-2016)[/COLOR]', 'collections&url=badsanta', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Basic Instinct[/COLOR] [COLOR yellow] (1992-2006)[/COLOR]', 'collections&url=basicinstinct', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Batman[/COLOR] [COLOR yellow] (1989-2016)[/COLOR]', 'collections&url=batman', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Beverly Hills Cop[/COLOR] [COLOR yellow] (1984-1994)[/COLOR]', 'collections&url=beverlyhillscop', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Big Mommas House[/COLOR] [COLOR yellow] (2000-2011)[/COLOR]', 'collections&url=bigmommashouse', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Blues Brothers[/COLOR] [COLOR yellow] (1980-1998)[/COLOR]', 'collections&url=bluesbrothers', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Bourne[/COLOR] [COLOR yellow] (2002-2016)[/COLOR]', 'collections&url=bourne', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Bruce Almighty[/COLOR] [COLOR yellow] (2003-2007)[/COLOR]', 'collections&url=brucealmighty', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Caddyshack[/COLOR] [COLOR yellow] (1980-1988)[/COLOR]', 'collections&url=caddyshack', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Cheaper by the Dozen[/COLOR] [COLOR yellow] (2003-2005)[/COLOR]', 'collections&url=cheaperbythedozen', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Cheech and Chong[/COLOR] [COLOR yellow] (1978-1984)[/COLOR]', 'collections&url=cheechandchong', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Childs Play[/COLOR] [COLOR yellow] (1988-2004)[/COLOR]', 'collections&url=childsplay', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]City Slickers[/COLOR] [COLOR yellow] (1991-1994)[/COLOR]', 'collections&url=cityslickers', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Conan[/COLOR] [COLOR yellow] (1982-2011)[/COLOR]', 'collections&url=conan', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Crank[/COLOR] [COLOR yellow] (2006-2009)[/COLOR]', 'collections&url=crank', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Crocodile Dundee[/COLOR] [COLOR yellow] (1986-2001)[/COLOR]', 'collections&url=crodiledunde', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Da Vinci Code[/COLOR] [COLOR yellow] (2006-2017)[/COLOR]', 'collections&url=davincicode', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Daddy Day Care[/COLOR] [COLOR yellow] (2003-2007)[/COLOR]', 'collections&url=daddydaycare', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Dark Knight Trilogy[/COLOR] [COLOR yellow] (2005-2013)[/COLOR]', 'collections&url=darkknight', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Death Wish[/COLOR] [COLOR yellow] (1974-1994)[/COLOR]', 'collections&url=deathwish', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Delta Force[/COLOR] [COLOR yellow] (1986-1990)[/COLOR]', 'collections&url=deltaforce', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Die Hard[/COLOR] [COLOR yellow] (1988-2013)[/COLOR]', 'collections&url=diehard', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Dirty Dancing[/COLOR] [COLOR yellow] (1987-2004)[/COLOR]', 'collections&url=dirtydancing', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Dirty Harry[/COLOR] [COLOR yellow] (1971-1988)[/COLOR]', 'collections&url=dirtyharry', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Dumb and Dumber[/COLOR] [COLOR yellow] (1994-2014)[/COLOR]', 'collections&url=dumbanddumber', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Escape from New York[/COLOR] [COLOR yellow] (1981-1996)[/COLOR]', 'collections&url=escapefromnewyork', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Every Which Way But Loose[/COLOR] [COLOR yellow] (1978-1980)[/COLOR]', 'collections&url=everywhichwaybutloose', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Exorcist[/COLOR] [COLOR yellow] (1973-2005)[/COLOR]', 'collections&url=exorcist', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]The Expendables[/COLOR] [COLOR yellow] (2010-2014)[/COLOR]', 'collections&url=theexpendables', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Fantastic Four[/COLOR] [COLOR yellow] (2005-2015)[/COLOR]', 'collections&url=fantasticfour', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Fast and the Furious[/COLOR] [COLOR yellow] (2001-2017)[/COLOR]', 'collections&url=fastandthefurious', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Father of the Bride[/COLOR] [COLOR yellow] (1991-1995)[/COLOR]', 'collections&url=fatherofthebride', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Fletch[/COLOR] [COLOR yellow] (1985-1989)[/COLOR]', 'collections&url=fletch', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Friday[/COLOR] [COLOR yellow] (1995-2002)[/COLOR]', 'collections&url=friday', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Friday the 13th[/COLOR] [COLOR yellow] (1980-2009)[/COLOR]', 'collections&url=fridaythe13th', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Fugitive[/COLOR] [COLOR yellow] (1993-1998)[/COLOR]', 'collections&url=fugitive', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]G.I. Joe[/COLOR] [COLOR yellow] (2009-2013)[/COLOR]', 'collections&url=gijoe', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Get Shorty[/COLOR] [COLOR yellow] (1995-2005)[/COLOR]', 'collections&url=getshorty', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Gettysburg[/COLOR] [COLOR yellow] (1993-2003)[/COLOR]', 'collections&url=gettysburg', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Ghost Rider[/COLOR] [COLOR yellow] (2007-2011)[/COLOR]', 'collections&url=ghostrider', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Ghostbusters[/COLOR] [COLOR yellow] (1984-2016)[/COLOR]', 'collections&url=ghostbusters', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Gods Not Dead[/COLOR] [COLOR yellow] (2014-2016)[/COLOR]', 'collections&url=godsnotdead', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Godfather[/COLOR] [COLOR yellow] (1972-1990)[/COLOR]', 'collections&url=godfather', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Godzilla[/COLOR] [COLOR yellow] (1956-2016)[/COLOR]', 'collections&url=godzilla', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Grown Ups[/COLOR] [COLOR yellow] (2010-2013)[/COLOR]', 'collections&url=grownups', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Grumpy Old Men[/COLOR] [COLOR yellow] (2010-2013)[/COLOR]', 'collections&url=grumpyoldmen', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Guns of Navarone[/COLOR] [COLOR yellow] (1961-1978)[/COLOR]', 'collections&url=gunsofnavarone', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Halloween[/COLOR] [COLOR yellow] (1978-2009)[/COLOR]', 'collections&url=halloween', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Hangover[/COLOR] [COLOR yellow] (2009-2013)[/COLOR]', 'collections&url=hangover', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Hannibal Lector[/COLOR] [COLOR yellow] (1986-2007)[/COLOR]', 'collections&url=hanniballector', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Hellraiser[/COLOR] [COLOR yellow] (1987-1996)[/COLOR]', 'collections&url=hellraiser', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Honey I Shrunk the Kids[/COLOR] [COLOR yellow] (1989-1995)[/COLOR]', 'collections&url=honeyishrunkthekids', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Horrible Bosses[/COLOR] [COLOR yellow] (2011-2014)[/COLOR]', 'collections&url=horriblebosses', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Hostel[/COLOR] [COLOR yellow] (2005-2011)[/COLOR]', 'collections&url=hostel', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Hot Shots[/COLOR] [COLOR yellow] (1991-1996)[/COLOR]', 'collections&url=hotshots', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Hulk[/COLOR] [COLOR yellow] (2003-2008)[/COLOR]', 'collections&url=hulk', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Independence Day[/COLOR] [COLOR yellow] (1996-2016)[/COLOR]', 'collections&url=independenceday', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Indiana Jones[/COLOR] [COLOR yellow] (1981-2008)[/COLOR]', 'collections&url=indianajones', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Insidious[/COLOR] [COLOR yellow] (2010-2015)[/COLOR]', 'collections&url=insidious', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Iron Eagle[/COLOR] [COLOR yellow] (1986-1992)[/COLOR]', 'collections&url=ironeagle', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Iron Man[/COLOR] [COLOR yellow] (2008-2013)[/COLOR]', 'collections&url=ironman', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Jack Reacher[/COLOR] [COLOR yellow] (2012-2016)[/COLOR]', 'collections&url=jackreacher', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Jack Ryan[/COLOR] [COLOR yellow] (1990-2014)[/COLOR]', 'collections&url=jackryan', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Jackass[/COLOR] [COLOR yellow] (2002-2013)[/COLOR]', 'collections&url=jackass', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]James Bond[/COLOR] [COLOR yellow] (1963-2015)[/COLOR]', 'collections&url=jamesbond', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Jaws[/COLOR] [COLOR yellow] (1975-1987)[/COLOR]', 'collections&url=jaws', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Jeepers Creepers[/COLOR] [COLOR yellow] (2001-2017)[/COLOR]', 'collections&url=jeeperscreepers', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]John Wick[/COLOR] [COLOR yellow] (2014-2017)[/COLOR]', 'collections&url=johnwick', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Jumanji[/COLOR] [COLOR yellow] (1995-2005)[/COLOR]', 'collections&url=jumanji', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Jurassic Park[/COLOR] [COLOR yellow] (1993-2015)[/COLOR]', 'collections&url=jurassicpark', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Kick-Ass[/COLOR] [COLOR yellow] (2010-2013)[/COLOR]', 'collections&url=kickass', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Kill Bill[/COLOR] [COLOR yellow] (2003-2004)[/COLOR]', 'collections&url=killbill', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]King Kong[/COLOR] [COLOR yellow] (1933-2016)[/COLOR]', 'collections&url=kingkong', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Lara Croft[/COLOR] [COLOR yellow] (2001-2003)[/COLOR]', 'collections&url=laracroft', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Legally Blonde[/COLOR] [COLOR yellow] (2001-2003)[/COLOR]', 'collections&url=legallyblonde', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Lethal Weapon[/COLOR] [COLOR yellow] (1987-1998)[/COLOR]', 'collections&url=leathalweapon', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Look Whos Talking[/COLOR] [COLOR yellow] (1989-1993)[/COLOR]', 'collections&url=lookwhostalking', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Machete[/COLOR] [COLOR yellow] (2010-2013)[/COLOR]', 'collections&url=machete', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Magic Mike[/COLOR] [COLOR yellow] (2012-2015)[/COLOR]', 'collections&url=magicmike', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Major League[/COLOR] [COLOR yellow] (1989-1998)[/COLOR]', 'collections&url=majorleague', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Man from Snowy River[/COLOR] [COLOR yellow] (1982-1988)[/COLOR]', 'collections&url=manfromsnowyriver', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Mask[/COLOR] [COLOR yellow] (1994-2005)[/COLOR]', 'collections&url=mask', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Matrix[/COLOR] [COLOR yellow] (1999-2003)[/COLOR]', 'collections&url=matrix', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]The Mechanic[/COLOR] [COLOR yellow] (2011-2016)[/COLOR]', 'collections&url=themechanic', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Meet the Parents[/COLOR] [COLOR yellow] (2000-2010)[/COLOR]', 'collections&url=meettheparents', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Men in Black[/COLOR] [COLOR yellow] (1997-2012)[/COLOR]', 'collections&url=meninblack', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Mighty Ducks[/COLOR] [COLOR yellow] (1995-1996)[/COLOR]', 'collections&url=mightyducks', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Miss Congeniality[/COLOR] [COLOR yellow] (2000-2005)[/COLOR]', 'collections&url=misscongeniality', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Missing in Action[/COLOR] [COLOR yellow] (1984-1988)[/COLOR]', 'collections&url=missinginaction', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Mission Impossible[/COLOR] [COLOR yellow] (1996-2015)[/COLOR]', 'collections&url=missionimpossible', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Naked Gun[/COLOR] [COLOR yellow] (1988-1994)[/COLOR]', 'collections&url=nakedgun', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]National Lampoon[/COLOR] [COLOR yellow] (1978-2006)[/COLOR]', 'collections&url=nationallampoon', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]National Lampoons Vacation[/COLOR] [COLOR yellow] (1983-2015)[/COLOR]', 'collections&url=nationallampoonsvacation', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]National Treasure[/COLOR] [COLOR yellow] (2004-2007)[/COLOR]', 'collections&url=nationaltreasure', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Neighbors[/COLOR] [COLOR yellow] (2014-2016)[/COLOR]', 'collections&url=neighbors', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Night at the Museum[/COLOR] [COLOR yellow] (2006-2014)[/COLOR]', 'collections&url=nightatthemuseum', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Nightmare on Elm Street[/COLOR] [COLOR yellow] (1984-2010)[/COLOR]', 'collections&url=nightmareonelmstreet', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Now You See Me[/COLOR] [COLOR yellow] (2013-2016)[/COLOR]', 'collections&url=nowyouseeme', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Nutty Professor[/COLOR] [COLOR yellow] (1996-2000)[/COLOR]', 'collections&url=nuttyprofessor', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Oceans Eleven[/COLOR] [COLOR yellow] (2001-2007)[/COLOR]', 'collections&url=oceanseleven', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Odd Couple[/COLOR] [COLOR yellow] (1968-1998)[/COLOR]', 'collections&url=oddcouple', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Oh, God[/COLOR] [COLOR yellow] (1977-1984)[/COLOR]', 'collections&url=ohgod', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Olympus Has Fallen[/COLOR] [COLOR yellow] (2013-2016)[/COLOR]', 'collections&url=olympushasfallen', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Omen[/COLOR] [COLOR yellow] (1976-1981)[/COLOR]', 'collections&url=omen', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Paul Blart Mall Cop[/COLOR] [COLOR yellow] (2009-2015)[/COLOR]', 'collections&url=paulblart', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Pirates of the Caribbean[/COLOR] [COLOR yellow] (2003-2017)[/COLOR]', 'collections&url=piratesofthecaribbean', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Planet of the Apes[/COLOR] [COLOR yellow] (1968-2014)[/COLOR]', 'collections&url=planetoftheapes', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Police Academy[/COLOR] [COLOR yellow] (1984-1994)[/COLOR]', 'collections&url=policeacademy', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Poltergeist[/COLOR] [COLOR yellow] (1982-1988)[/COLOR]', 'collections&url=postergeist', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Porkys[/COLOR] [COLOR yellow] (1981-1985)[/COLOR]', 'collections&url=porkys', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Predator[/COLOR] [COLOR yellow] (1987-2010)[/COLOR]', 'collections&url=predator', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]The Purge[/COLOR] [COLOR yellow] (2013-2016)[/COLOR]', 'collections&url=thepurge', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Rambo[/COLOR] [COLOR yellow] (1982-2008)[/COLOR]', 'collections&url=rambo', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]RED[/COLOR] [COLOR yellow] (2010-2013)[/COLOR]', 'collections&url=red', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Revenge of the Nerds[/COLOR] [COLOR yellow] (1984-1987)[/COLOR]', 'collections&url=revengeofthenerds', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Riddick[/COLOR] [COLOR yellow] (2000-2013)[/COLOR]', 'collections&url=riddick', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Ride Along[/COLOR] [COLOR yellow] (2014-2016)[/COLOR]', 'collections&url=ridealong', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]The Ring[/COLOR] [COLOR yellow] (2002-2017)[/COLOR]', 'collections&url=thering', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]RoboCop[/COLOR] [COLOR yellow] (1987-1993)[/COLOR]', 'collections&url=robocop', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Rocky[/COLOR] [COLOR yellow] (1976-2015)[/COLOR]', 'collections&url=rocky', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Romancing the Stone[/COLOR] [COLOR yellow] (1984-1985)[/COLOR]', 'collections&url=romancingthestone', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Rush Hour[/COLOR] [COLOR yellow] (1998-2007)[/COLOR]', 'collections&url=rushhour', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Santa Clause[/COLOR] [COLOR yellow] (1994-2006)[/COLOR]', 'collections&url=santaclause', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Saw[/COLOR] [COLOR yellow] (2004-2010)[/COLOR]', 'collections&url=saw', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Sex and the City[/COLOR] [COLOR yellow] (2008-2010)[/COLOR]', 'collections&url=sexandthecity', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Shaft[/COLOR] [COLOR yellow] (1971-2000)[/COLOR]', 'collections&url=shaft', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Shanghai Noon[/COLOR] [COLOR yellow] (2000-2003)[/COLOR]', 'collections&url=shanghainoon', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Sin City[/COLOR] [COLOR yellow] (2005-2014)[/COLOR]', 'collections&url=sincity', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Sinister[/COLOR] [COLOR yellow] (2012-2015)[/COLOR]', 'collections&url=sinister', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Sister Act[/COLOR] [COLOR yellow] (1995-1993)[/COLOR]', 'collections&url=sisteract', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Smokey and the Bandit[/COLOR] [COLOR yellow] (1977-1986)[/COLOR]', 'collections&url=smokeyandthebandit', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Speed[/COLOR] [COLOR yellow] (1994-1997)[/COLOR]', 'collections&url=speed', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Spider-Man[/COLOR] [COLOR yellow] (2002-2017)[/COLOR]', 'collections&url=spiderman', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Stakeout[/COLOR] [COLOR yellow] (1987-1993)[/COLOR]', 'collections&url=stakeout', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Star Trek[/COLOR] [COLOR yellow] (1979-2016)[/COLOR]', 'collections&url=startrek', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Star Wars[/COLOR] [COLOR yellow] (1977-2015)[/COLOR]', 'collections&url=starwars', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Superman[/COLOR] [COLOR yellow] (1978-2016)[/COLOR]', 'collections&url=superman', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]The Sting[/COLOR] [COLOR yellow] (1973-1983)[/COLOR]', 'collections&url=thesting', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Taken[/COLOR] [COLOR yellow] (2008-2014)[/COLOR]', 'collections&url=taken', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Taxi[/COLOR] [COLOR yellow] (1998-2007)[/COLOR]', 'collections&url=taxi', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Ted[/COLOR] [COLOR yellow] (2012-2015)[/COLOR]', 'collections&url=ted', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Teen Wolf[/COLOR] [COLOR yellow] (1985-1987)[/COLOR]', 'collections&url=teenwolf', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Terminator[/COLOR] [COLOR yellow] (1984-2015)[/COLOR]', 'collections&url=terminator', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Terms of Endearment[/COLOR] [COLOR yellow] (1983-1996)[/COLOR]', 'collections&url=termsofendearment', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Texas Chainsaw Massacre[/COLOR] [COLOR yellow] (1974-2013)[/COLOR]', 'collections&url=texaschainsawmassacre', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]The Thing[/COLOR] [COLOR yellow] (1982-2011)[/COLOR]', 'collections&url=thething', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Thomas Crown Affair[/COLOR] [COLOR yellow] (1968-1999)[/COLOR]', 'collections&url=thomascrownaffair', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Transporter[/COLOR] [COLOR yellow] (2002-2015)[/COLOR]', 'collections&url=transporter', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Under Siege[/COLOR] [COLOR yellow] (1992-1995)[/COLOR]', 'collections&url=undersiege', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Universal Soldier[/COLOR] [COLOR yellow] (1992-2012)[/COLOR]', 'collections&url=universalsoldier', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Wall Street[/COLOR] [COLOR yellow] (1987-2010)[/COLOR]', 'collections&url=wallstreet', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Waynes World[/COLOR] [COLOR yellow] (1992-1993)[/COLOR]', 'collections&url=waynesworld', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Weekend at Bernies[/COLOR] [COLOR yellow] (1989-1993)[/COLOR]', 'collections&url=weekendatbernies', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Whole Nine Yards[/COLOR] [COLOR yellow] (2000-2004)[/COLOR]', 'collections&url=wholenineyards', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]X-Files[/COLOR] [COLOR yellow] (1998-2008)[/COLOR]', 'collections&url=xfiles', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]X-Men[/COLOR] [COLOR yellow] (2000-2016)[/COLOR]', 'collections&url=xmen', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]xXx[/COLOR] [COLOR yellow] (2002-2005)[/COLOR]', 'collections&url=xxx', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Young Guns[/COLOR] [COLOR yellow] (1988-1990)[/COLOR]', 'collections&url=youngguns', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Zoolander[/COLOR] [COLOR yellow] (2001-2016)[/COLOR]', 'collections&url=zoolander', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]Zorro[/COLOR] [COLOR yellow] (1998-2005)[/COLOR]', 'collections&url=zorro', 'boxsets18.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()

    def kidzone(self, lite=False):
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Kids Movies[/COLOR][B][COLOR deepskyblue] •[/COLOR][/B]', 'kidsmoviesNavigator', 'kids_movies.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Kids TV Shows[/COLOR][B][COLOR deepskyblue] •[/COLOR][/B]', 'kidstvNavigator', 'kids_shows.png', 'DefaultTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Youngsters[/COLOR][B][COLOR deepskyblue] •[/COLOR][/B]', 'toddlerNavigator', 'kids_youngsters.png', 'DefaulTVShows.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Anime Movies[/COLOR][B][COLOR deepskyblue] •[/COLOR][/B]', 'animemovieNavigator', 'kids_anime.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Anime TV Shows[/COLOR][B][COLOR deepskyblue] •[/COLOR][/B]', 'animetvNavigator', 'kids_anime2.png', 'DefaulTVShows.png')        

        self.endDirectory()

    def kidsmovies(self, lite=False):       
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Random Play[/COLOR]', 'randomNavigator', 'kids_random.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Kids Trending[/COLOR]', 'movies&url=advancedsearchtrending', 'kids_trending.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Animated Movies[/COLOR]', 'movies&url=advancedsearchanimation', 'kids_animated.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Kids Boxsets[/COLOR]', 'kidsboxsetsNavigator', 'kids_boxsets.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Top 10.000[/COLOR]', 'movies&url=advancedsearchtop10000', 'kids_top10000.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Walt Disney[/COLOR]', 'waltdisneyNavigator', 'kids_disney.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Dreamworks[/COLOR]', 'movies&url=advancedsearchdreamworks', 'kids_dreamworks.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Kids Horror[/COLOR]', 'movies&url=advancedsearchkidshorror', 'kids_horror.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Just Lego[/COLOR]', 'justLegoNavigator', 'kids_lego.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Teen Movies[/COLOR]', 'movies&url=https://api.trakt.tv/users/acerider/lists/movies-teen/items', 'kids_teen.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Gamers[/COLOR]', 'gamersNavigator', 'kids_gamers.png', 'DefaultMovies.png')
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
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Action[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixaction', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Adventure[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixadventure', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Animation[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixanimation', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Biography[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixbiography', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Comedy[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixcomedy', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Crime[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixcrime', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Documentary[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixdocumentary', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Drama[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixdrama', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Family[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixfamily', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Fantasy[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixfantasy', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Film Noir[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixfilmnoir', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random History[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixhistory', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Horror[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixhorror', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Music[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixmusic', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Musical[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixmusical', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Mystery[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixmystery', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Romance[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixromance', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random SciFi[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixscifi', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Short[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixshort', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Sport[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixsport', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Superhero[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixsuperhero', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Thriller[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixthriller', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random War[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixwar', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Random Western[/COLOR]', 'random&rtype=movie&url=advancedsearchrandomflixwestern', 'movies_random.png', 'DefaultRecentlyAddedMovies.png')
                
        self.endDirectory()

    def justlego(self, lite=False):
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Lego Movies[/COLOR]', 'movies&url=advancedsearchjustlego', 'kids_lego.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Brickfilms[/COLOR]', 'justlegobrickfilms', 'kids_lego3.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Football[/COLOR]', 'justlegofootball', 'kids_lego3.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Gamers[/COLOR]', 'justlegogamers', 'kids_lego3.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Little Toys[/COLOR]', 'justlegolittletoys', 'kids_lego3.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Parody[/COLOR]', 'justlegoparody', 'kids_lego3.png', 'DefaultRecentlyAddedMovies.png')
                
        self.endDirectory()

    def gamers(self, lite=False):
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Gamers Movies[/COLOR]', 'movies&url=advancedsearchgamers', 'kids_gamers.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Gamers Library[/COLOR]', 'gamerslibrary', 'kids_gamers.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Gamers Playground[/COLOR]', 'gamersplayground', 'kids_gamers.png', 'DefaultRecentlyAddedMovies.png')
                
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
        self.addDirectoryItem('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Classic Cartoons[/COLOR]', 'tvshows&url=advancedsearchclassiccartoons', 'kids_classic.png', 'DefaultTVShows.png')
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
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Information[/COLOR][/B]', 'newsNavigator', 'icon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Changelog[/COLOR][/B]', 'ShowChangelog', 'changelog.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Accounts[/COLOR][/B]', 'accountsrd', 'tools.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Settings[/COLOR][/B]', 'allsettingsNavigator', 'tools.png', 'DefaultTVShows.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Tools[/COLOR][/B]', 'alltoolsNavigator', 'tools.png', 'DefaulTVShows.png')
        #self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]iPair[/COLOR][/B]', 'pairTools', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]KODI Builds[/COLOR][/B]', 'builds', 'kodi.png', 'DefaultMovies.png')        

        self.endDirectory()
        
    def allsettings(self, lite=False):
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]NuMb3r5 Settings[/COLOR][/B]', 'openSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]JEN Settings[/COLOR][/B]', 'jentools', 'tools.png', 'DefaultMovies.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]ResolverURL[/COLOR][/B]', 'ResolveUrlTorrent', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Debrid Providers[/COLOR][/B]', 'openSettings&query=4.1', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Log Viewer[/COLOR][/B]', 'logViewer', 'tools.png', 'DefaultAddonProgram.png')        

        self.endDirectory()
        
    def alltools(self, lite=False):
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Library[/COLOR][/B]', 'libraryNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Viewtypes[/COLOR][/B]', 'viewsNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Clear cache...[/COLOR][/B]', 'clearCache', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Clear providers...[/COLOR][/B]', 'clearCacheProviders', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Clear search history...[/COLOR][/B]', 'clearCacheSearch', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Clear Meta cache...[/COLOR][/B]', 'clearMetaCache', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B][COLOR black]• [/COLOR][/B][B][COLOR ghostwhite]Clear all cache[/COLOR][/B]', 'clearAllCache', 'tools.png', 'DefaultAddonProgram.png')        

        self.endDirectory()                                               
            

    def endDirectory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


