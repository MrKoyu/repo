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


from resources.lib.modules import trakt
from resources.lib.modules import cleantitle
from resources.lib.modules import cleangenre
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import metacache
from resources.lib.modules import playcount
from resources.lib.modules import workers
from resources.lib.modules import views
from resources.lib.modules import utils
from resources.lib.indexers import navigator

import os, sys, re, json, urllib, urlparse, datetime

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', ''))) if len(sys.argv) > 1 else dict()

action = params.get('action')






class tvshows:
    def __init__(self):
        self.list = []

        self.imdb_link = 'http://www.imdb.com'
        self.trakt_link = 'http://api.trakt.tv'
        self.tvmaze_link = 'http://www.tvmaze.com'
        self.logo_link = 'https://i.imgur.com/'
        self.tvdb_key = 'MUQ2MkYyRjkwMDMwQzQ0NA=='
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours=5))
        self.trakt_user = control.setting('trakt.user').strip()
        self.imdb_user = control.setting('imdb.user').replace('ur', '')
        self.fanart_tv_user = control.setting('fanart.tv.user')
        self.user = control.setting('fanart.tv.user') + str('')
        self.lang = control.apiLanguage()['tvdb']

        self.search_link = 'http://api.trakt.tv/search/show?limit=20&page=1&query='
        self.tvmaze_info_link = 'http://api.tvmaze.com/shows/%s'
        self.tvdb_info_link = 'http://thetvdb.com/api/%s/series/%s/%s.xml' % (
        self.tvdb_key.decode('base64'), '%s', self.lang)
        self.fanart_tv_art_link = 'http://webservice.fanart.tv/v3/tv/%s'
        self.fanart_tv_level_link = 'http://webservice.fanart.tv/v3/level'
        self.tvdb_by_imdb = 'http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s'
        self.tvdb_by_query = 'http://thetvdb.com/api/GetSeries.php?seriesname=%s'
        self.tvdb_image = 'http://thetvdb.com/banners/'

        self.persons_link = 'http://www.imdb.com/search/name?count=100&name='
        self.personlist_link = 'http://www.imdb.com/search/name?count=100&gender=male,female'
        self.popular_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&release_date=,date[0]&sort=moviemeter,asc&count=40&start=1'
        self.airing_link = 'http://www.imdb.com/search/title?title_type=tv_episode&release_date=date[1],date[0]&sort=moviemeter,asc&count=40&start=1'
        self.active_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=10,&production_status=active&sort=moviemeter,asc&count=40&start=1'
        self.premiere_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&languages=en&num_votes=10,&release_date=date[60],date[0]&sort=release_date,desc&count=40&start=1'
        self.rating_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=5000,&release_date=,date[0]&sort=user_rating,desc&count=40&start=1'
        self.views_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&release_date=,date[0]&sort=num_votes,desc&count=40&start=1'
        self.person_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&role=%s&sort=year,desc&count=40&start=1'
        self.genre_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&genres=%s&sort=moviemeter,asc&count=40&start=1'
        self.keyword_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&keywords=%s&sort=moviemeter,asc&count=40&start=1'
        self.language_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&count=40&start=1'
        self.certification_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&certificates=us:%s&sort=moviemeter,asc&count=40&start=1'
        self.trending_link = 'http://api.trakt.tv/shows/trending?limit=40&page=1'
        self.advancedsearchfamily_link = 'https://www.imdb.com/search/title?title_type=tv_series&release_date=2016-01-01,&genres=family'
        self.advancedsearchcartoons_link = 'https://www.imdb.com/search/title?title_type=tv_series,mini_series&genres=animation&num_votes=100,&release_date=,date[0]&genres=animation&sort=moviemeter,asc&count=40&start=1'
        self.advancedsearchclassiccartoons_link = 'https://www.imdb.com/list/ls052624514/?sort=alpha,asc&st_dt=&mode=detail&page=1'
        self.advancedsearchmarveltv_link  = 'https://www.imdb.com/list/ls026566277/?view=detail&sort=alpha,asc&title_type=tvSeries,miniSeries&start=1'
        self.advancedsearchhighly_link = 'https://www.imdb.com/search/title?title_type=tv_series&num_votes=15000,&genres=family&sort=user_rating,desc&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=186d3818-4564-4c2a-a20e-9054a8648eca&pf_rd_r=0JBMXKVJDMSKNGJKAZTV&pf_rd_s=center-22&pf_rd_t=60601&pf_rd_i=family-entertainment-guide&ref_=fea_fam_fam_ats_rank_fam_tv_sm'
        self.advancedsearchlegotv_link = 'https://www.imdb.com/search/title/?title=lego&title_type=tv_series&count=100'
        self.advancedsearchtransformers_link = 'https://www.imdb.com/search/title/?title=transformers&title_type=tv_series&count=100'
        self.advancedsearchretro_link = 'https://www.imdb.com/search/title?title_type=tv_series,tv_episode,tv_miniseries&release_date=1980-01-01,2000-12-31&genres=comedy,family&countries=us'
        self.advancedsearchteentv_link = 'https://www.imdb.com/search/title?certificates=US%3ATV-14&sort=moviemeter,asc'
        self.advancedsearchfreeformtv_link = 'https://www.imdb.com/list/ls063177895/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'

        self.advancedsearchanimepopular_link = 'https://www.imdb.com/search/title?count=100&keywords=anime&num_votes=2000,&explore=title_type&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3999419c-1229-4fa7-9240-55e83e21cecb&pf_rd_r=QG2EX199YPFDV4NNP6WW&pf_rd_s=right-1&pf_rd_t=15051&pf_rd_i=genre&title_type=tvSeries&ref_=adv_explore_rhs'
        self.advancedsearchanimepeoplewatching_link = 'https://www.imdb.com/search/title?count=100&keywords=anime&num_votes=2000,&explore=title_type&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3999419c-1229-4fa7-9240-55e83e21cecb&pf_rd_r=QG2EX199YPFDV4NNP6WW&pf_rd_s=right-1&pf_rd_t=15051&pf_rd_i=genre&title_type=tvSeries&sort=num_votes,desc&ref_=adv_explore_rhs'
        self.advancedsearchanimetrending_link = 'https://www.imdb.com/list/ls041266139/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
        self.advancedsearchanimehighlyrated_link = 'https://www.imdb.com/list/ls021457150/?sort=date_added,desc&st_dt=&mode=detail&page=1'
        self.advancedsearchanimetopseries_link = 'https://www.imdb.com/list/ls058654847/?sort=num_votes,desc&st_dt=&mode=detail&page=1'
        self.animegenre_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&genres=%s&keywords=anime&sort=moviemeter,asc&count=40&start=1&sort=alpha,asc'
        
        self.advancedsearchtoddler_link = 'https://www.imdb.com/list/ls021175534/?sort=release_date&mode=detail&page=1'
        self.advancedsearchnickjr_link = 'https://www.imdb.com/list/ls060197516/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
        self.advancedsearchdisneyjr_link = 'https://www.imdb.com/list/ls024059608/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
        self.advancedsearchnetflixkids_link = 'https://www.imdb.com/list/ls006497912/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
        self.advancedsearchnetflixshows_link = 'https://www.imdb.com/list/ls050522997/?sort=user_rating,desc&st_dt=&mode=detail&page=1'

        self.traktlists_link = 'http://api.trakt.tv/users/me/lists'
        self.traktlikedlists_link = 'http://api.trakt.tv/users/likes/lists?limit=1000000'
        self.traktlist_link = 'http://api.trakt.tv/users/%s/lists/%s/items'
        self.traktcollection_link = 'http://api.trakt.tv/users/me/collection/shows'
        self.traktwatchlist_link = 'http://api.trakt.tv/users/me/watchlist/shows'
        self.traktfeatured_link = 'http://api.trakt.tv/recommendations/shows?limit=40'
        self.imdblists_link = 'http://www.imdb.com/user/ur%s/lists?tab=all&sort=mdfd&order=desc&filter=titles' % self.imdb_user
        self.imdblist_link = 'http://www.imdb.com/list/%s/?view=detail&sort=alpha,asc&title_type=tvSeries,tvMiniSeries&start=1'
        self.imdblist2_link = 'http://www.imdb.com/list/%s/?view=detail&sort=date_added,desc&title_type=tvSeries,tvMiniSeries&start=1'
        self.imdbwatchlist_link = 'http://www.imdb.com/user/ur%s/watchlist?sort=alpha,asc' % self.imdb_user
        self.imdbwatchlist2_link = 'http://www.imdb.com/user/ur%s/watchlist?sort=date_added,desc' % self.imdb_user
        self.top250tv_link = 'https://www.imdb.com/list/ls008957859/?sort=num_votes,desc&st_dt=&mode=detail&page=1'
        


    def get(self, url, idx=True, create_directory=True):
        try:
            try:
                url = getattr(self, url + '_link')
            except:
                pass
														  
						

            try:
                u = urlparse.urlparse(url).netloc.lower()
            except:
                pass

            if u in self.trakt_link and '/users/' in url:
                try:
                    if not '/users/me/' in url: raise Exception()
                    if trakt.getActivity() > cache.timeout(self.trakt_list, url, self.trakt_user): raise Exception()
                    self.list = cache.get(self.trakt_list, 720, url, self.trakt_user)
                except:
                    self.list = cache.get(self.trakt_list, 0, url, self.trakt_user)

                if '/users/me/' in url and '/collection/' in url:
                    self.list = sorted(self.list, key=lambda k: utils.title_key(k['title']))

                if idx == True: self.worker()

            elif u in self.trakt_link and self.search_link in url:
                self.list = cache.get(self.trakt_list, 1, url, self.trakt_user)
                if idx == True: self.worker(level=0)

            elif u in self.trakt_link:
                self.list = cache.get(self.trakt_list, 24, url, self.trakt_user)
                if idx == True: self.worker()


            elif u in self.imdb_link and ('/user/' in url or '/list/' in url):
                self.list = cache.get(self.imdb_list, 0, url)
                if idx == True: self.worker()

            elif u in self.imdb_link:
                self.list = cache.get(self.imdb_list, 24, url)
                if idx == True: self.worker()


            elif u in self.tvmaze_link:
                self.list = cache.get(self.tvmaze_list, 168, url)
                if idx == True: self.worker()


            if idx == True and create_directory == True: self.tvshowDirectory(self.list)
            return self.list
        except:
            pass

        
    def animegenres(self):
        genres = [
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime Action[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'action', True),
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime Adventure[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'adventure', True),
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime Biography[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'biography', True),
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime Comedy[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'comedy', True),
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime Crime[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'crime', True),
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime Drama[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'drama', True),
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime Family[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'family', True),
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime Fantasy[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'fantasy', True),
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime Game-Show[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'game_show', True),
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime History[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'history', True),
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime Music[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'music', True),
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime Mystery[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'mystery', True),
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime Reality-TV[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'reality_tv', True),
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime Romance[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'romance', True),
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime Science Fiction[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'sci_fi', True),
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime Talk-Show[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'talk_show', True),
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime Thriller[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'thriller', True),
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime War[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'war', True),
            ('[B][COLOR dodgerblue]• [/COLOR][/B][COLOR ghostwhite]Anime Western[/COLOR][B][COLOR dodgerblue] •[/COLOR][/B]', 'western', True)

        ]

        for i in genres: self.list.append(
            {
                'name': cleangenre.lang(i[0], self.lang),
                'url': self.animegenre_link % i[1] if i[2] else self.keyword_link % i[1],
                'image': 'kids_anime2.png',
                'action': 'tvshows'
            })

        self.addDirectory(self.list)
        return self.list

    def boxsetgenres(self):
        genres = [
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Action[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'action', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Adventure[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'adventure', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Animation[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'animation', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Anime[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'anime', False),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Biography[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'biography', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Comedy[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'comedy', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Crime[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'crime', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Drama[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'drama', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Family[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'family', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Fantasy[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'fantasy', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Game-Show[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'game_show', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV History[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'history', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Horror[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'horror', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Music[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'music', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Musical[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'musical', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Mystery[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'mystery', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV News[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'news', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Reality-TV[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'reality_tv', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Romance[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'romance', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Science Fiction[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'sci_fi', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Sport[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'sport', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Talk-Show[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'talk_show', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Thriller[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'thriller', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV War[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'war', True),
            ('[B][COLOR yellow]• [/COLOR][/B][COLOR ghostwhite]TV Western[/COLOR][B][COLOR yellow] •[/COLOR][/B]', 'western', True)
        ]

        for i in genres: self.list.append(
            {
                'name': cleangenre.lang(i[0], self.lang),
                'url': self.genre_link % i[1] if i[2] else self.keyword_link % i[1],
                'image': 'boxsets3.png',
                'action': 'tvshows'
            })

        self.addDirectory(self.list)
        return self.list    
      

    def search(self):

        navigator.navigator().addDirectoryItem(32603, 'tvSearchnew', 'search5.png', 'DefaultTVShows.png')
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database

        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()

        try:
            dbcur.executescript("CREATE TABLE IF NOT EXISTS tvshow (ID Integer PRIMARY KEY AUTOINCREMENT, term);")
        except:
            pass

        dbcur.execute("SELECT * FROM tvshow ORDER BY ID DESC")

        lst = []

        delete_option = False
        for (id, term) in dbcur.fetchall():
            if term not in str(lst):
                delete_option = True
                navigator.navigator().addDirectoryItem(term, 'tvSearchterm&name=%s' % term, 'search5.png',
                                                       'DefaultTVShows.png')
                lst += [(term)]
        dbcur.close()

        if delete_option:
            navigator.navigator().addDirectoryItem(32605, 'clearCacheSearch', 'trash.png', 'DefaultAddonProgram.png')

        navigator.navigator().endDirectory()

    




    def search_new(self):
        t = control.lang(32010).encode('utf-8')
        k = control.keyboard('', t)
        k.doModal()
        q = k.getText() if k.isConfirmed() else None
						

        if (q is None or q == ''):
            return

        try:
            from sqlite3 import dbapi2 as database
        except Exception:
            from pysqlite2 import dbapi2 as database

        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()
        dbcur.execute("INSERT INTO tvshow VALUES (?,?)", (None, q))
        dbcon.commit()
        dbcur.close()
        url = self.search_link + urllib.quote_plus(q)
        self.get(url)




    def search_term(self, name):
        url = self.search_link + urllib.quote_plus(name)
        self.get(url)




    def person(self):
        try:
            control.idle()

            t = control.lang(32010).encode('utf-8')
            k = control.keyboard('', t)
            k.doModal()
            q = k.getText() if k.isConfirmed() else None

            if (q == None or q == ''):
                return

            url = self.persons_link + urllib.quote_plus(q)
            if int(control.getKodiVersion()) >= 18:
                self.persons(url)
            else:
                url = '%s?action=tvPersons&url=%s' % (sys.argv[0], urllib.quote_plus(url))
                control.execute('Container.Update(%s)' % url)
        except Exception:
            return


    def genres(self):
        genres = [
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Action[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'action', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Adventure[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'adventure', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Animation[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'animation', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Anime[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'anime', False),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Biography[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'biography', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Comedy[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'comedy', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Crime[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'crime', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Drama[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'drama', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Family[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'family', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Fantasy[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'fantasy', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Game-Show[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'game_show', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]History[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'history', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Horror[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'horror', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Music[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'music', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Musical[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'musical', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Mystery[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'mystery', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]News[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'news', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Reality-TV[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'reality_tv', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Romance[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'romance', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Science Fiction[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'sci_fi', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Sport[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'sport', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Talk-Show[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'talk_show', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Thriller[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'thriller', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]War[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'war', True),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Western[/COLOR][B][COLOR firebrick] •[/COLOR][/B]', 'western', True)
        ]

        for i in genres: self.list.append(
            {
                'name': cleangenre.lang(i[0], self.lang),
                'url': self.genre_link % i[1] if i[2] else self.keyword_link % i[1],
                'image': 'tv_genres.png',
                'action': 'tvshows'
            })

        self.addDirectory(self.list)
        return self.list

    def networks(self):
        networks = [
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]A&E[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/29/ae', 'https://i.imgur.com/xLDfHjH.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]ABC[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/3/abc', 'https://i.imgur.com/qePLxos.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]AMC[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/20/amc', 'https://i.imgur.com/ndorJxi.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]AT-X[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/167/at-x', 'https://i.imgur.com/JshJYGN.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Adult Swim[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/10/adult-swim', 'https://i.imgur.com/jCqbRcS.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Amazon[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/webchannels/3/amazon', 'https://i.imgur.com/ru9DDlL.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Animal Planet[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/92/animal-planet', 'https://i.imgur.com/olKc4RP.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Audience[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/31/audience-network', 'https://i.imgur.com/5Q3mo5A.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]BBC America[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/15/bbc-america', 'https://i.imgur.com/TUHDjfl.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]BBC Four[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/51/bbc-four', 'https://i.imgur.com/PNDalgw.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]BBC One[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/12/bbc-one', 'https://i.imgur.com/u8x26te.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]BBC Three[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/webchannels/71/bbc-three', 'https://i.imgur.com/SDLeLcn.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]BBC Two[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/37/bbc-two', 'https://i.imgur.com/SKeGH1a.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]BET[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/56/bet', 'https://i.imgur.com/ZpGJ5UQ.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Bravo[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/52/bravo', 'https://i.imgur.com/TmEO3Tn.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]CBC[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/36/cbc', 'https://i.imgur.com/unQ7WCZ.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]CBS[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/2/cbs', 'https://i.imgur.com/8OT8igR.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]CTV[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/48/ctv', 'https://i.imgur.com/qUlyVHz.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]CW[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/5/the-cw', 'https://i.imgur.com/Q8tooeM.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]CW Seed[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/webchannels/13/cw-seed', 'https://i.imgur.com/nOdKoEy.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Cartoon Network[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/11/cartoon-network', 'https://i.imgur.com/zmOLbbI.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Channel 4[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/45/channel-4', 'https://i.imgur.com/6ZA9UHR.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Channel 5[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/135/channel-5', 'https://i.imgur.com/5ubnvOh.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Cinemax[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/19/cinemax', 'https://i.imgur.com/zWypFNI.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Comedy Central[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/23/comedy-central', 'https://i.imgur.com/ko6XN77.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Crackle[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/webchannels/4/crackle', 'https://i.imgur.com/53kqZSY.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Discovery Channel[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/66/discovery-channel', 'https://i.imgur.com/8UrXnAB.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Discovery ID[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/89/investigation-discovery', 'https://i.imgur.com/07w7BER.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Disney Channel[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/78/disney-channel', 'https://i.imgur.com/ZCgEkp6.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Disney XD[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/25/disney-xd', 'https://i.imgur.com/PAJJoqQ.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]E! Entertainment[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/43/e', 'https://i.imgur.com/3Delf9f.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]E4[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/41/e4', 'https://i.imgur.com/frpunK8.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]FOX[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/4/fox', 'https://i.imgur.com/6vc0Iov.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]FX[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/13/fx', 'https://i.imgur.com/aQc1AIZ.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Freeform[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/26/freeform', 'https://i.imgur.com/f9AqoHE.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]HBO[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/8/hbo', 'https://i.imgur.com/Hyu8ZGq.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]HGTV[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/192/hgtv', 'https://i.imgur.com/INnmgLT.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Hallmark[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/50/hallmark-channel', 'https://i.imgur.com/zXS64I8.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]History Channel[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/53/history', 'https://i.imgur.com/LEMgy6n.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Hulu[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/webchannels/2/hulu', 'https://i.imgur.com/uSD2Cdw.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]ITV[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/35/itv', 'https://i.imgur.com/5Hxp5eA.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Lifetime[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/18/lifetime', 'https://i.imgur.com/tvYbhen.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]MTV[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/22/mtv', 'https://i.imgur.com/QM6DpNW.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]NBC[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/1/nbc', 'https://i.imgur.com/yPRirQZ.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]National Geographic[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/42/national-geographic-channel', 'https://i.imgur.com/XCGNKVQ.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Netflix[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/webchannels/1/netflix', 'https://i.imgur.com/jI5c3bw.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Nickelodeon[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/27/nickelodeon', 'https://i.imgur.com/OUVoqYc.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]PBS[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/85/pbs', 'https://i.imgur.com/r9qeDJY.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Showtime[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/9/showtime', 'https://i.imgur.com/SawAYkO.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Sky1[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/63/sky-1', 'https://i.imgur.com/xbgzhPU.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Starz[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/17/starz', 'https://i.imgur.com/Z0ep2Ru.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Sundance[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/33/sundance-tv', 'https://i.imgur.com/qldG5p2.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Syfy[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/16/syfy', 'https://i.imgur.com/9yCq37i.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]TBS[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/32/tbs', 'https://i.imgur.com/RVCtt4Z.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]TLC[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/80/tlc', 'https://i.imgur.com/c24MxaB.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]TNT[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/14/tnt', 'https://i.imgur.com/WnzpAGj.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]TV Land[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/57/tvland', 'https://i.imgur.com/1nIeDA5.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Travel Channel[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/82/travel-channel', 'https://i.imgur.com/mWXv7SF.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]TruTV[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/84/trutv', 'https://i.imgur.com/HnB3zfc.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Youtube Red[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/webchannels/43/youtube-premium', 'https://i.imgur.com/ZfewP1Y.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]USA[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/30/usa-network', 'https://i.imgur.com/Doccw9E.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]VH1[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/55/vh1', 'https://i.imgur.com/IUtHYzA.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]WGN[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/28/wgn-america', 'https://i.imgur.com/TL6MzgO.png')
        ]

        for i in networks: self.list.append(
            {'name': i[0], 'url': self.tvmaze_link + i[1], 'image': i[2], 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list

    def networkskids(self):
        networks = [
            ('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Cartoon Network[/COLOR]', '/networks/11/cartoon-network', 'https://i.imgur.com/zmOLbbI.png'),
            ('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Disney Channel[/COLOR]', '/networks/78/disney-channel', 'https://i.imgur.com/ZCgEkp6.png'),
            ('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Disney XD[/COLOR]', '/networks/25/disney-xd', 'https://i.imgur.com/PAJJoqQ.png'),
            ('[B][COLOR deepskyblue]• [/COLOR][/B][COLOR ghostwhite]Nickelodeon[/COLOR]', '/networks/27/nickelodeon', 'https://i.imgur.com/OUVoqYc.png'),
        ]

        for i in networks: self.list.append(
            {'name': i[0], 'url': self.tvmaze_link + i[1], 'image': i[2], 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list
        
    def networkspremium(self):
        networks = [
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]AMC[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/20/amc', 'https://i.imgur.com/ndorJxi.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Amazon[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/webchannels/3/amazon', 'https://i.imgur.com/ru9DDlL.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Animal Planet[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/92/animal-planet', 'https://i.imgur.com/olKc4RP.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]BBC America[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/15/bbc-america', 'https://i.imgur.com/TUHDjfl.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Bravo[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/52/bravo', 'https://i.imgur.com/TmEO3Tn.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Channel 4[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/45/channel-4', 'https://i.imgur.com/6ZA9UHR.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Channel 5[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/135/channel-5', 'https://i.imgur.com/5ubnvOh.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Cinemax[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/19/cinemax', 'https://i.imgur.com/zWypFNI.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Comedy Central[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/23/comedy-central', 'https://i.imgur.com/ko6XN77.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]FOX[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/4/fox', 'https://i.imgur.com/6vc0Iov.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]FX[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/13/fx', 'https://i.imgur.com/aQc1AIZ.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]HBO[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/8/hbo', 'https://i.imgur.com/Hyu8ZGq.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Hulu[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/webchannels/2/hulu', 'https://i.imgur.com/uSD2Cdw.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]ITV[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/35/itv', 'https://i.imgur.com/5Hxp5eA.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Lifetime[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/18/lifetime', 'https://i.imgur.com/tvYbhen.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]MTV[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/22/mtv', 'https://i.imgur.com/QM6DpNW.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]NBC[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/1/nbc', 'https://i.imgur.com/yPRirQZ.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]National Geographic[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/42/national-geographic-channel', 'https://i.imgur.com/XCGNKVQ.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Netflix[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/webchannels/1/netflix', 'https://i.imgur.com/jI5c3bw.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Showtime[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/9/showtime', 'https://i.imgur.com/SawAYkO.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Sky1[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/63/sky-1', 'https://i.imgur.com/xbgzhPU.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Starz[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/17/starz', 'https://i.imgur.com/Z0ep2Ru.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]Youtube Red[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/webchannels/43/youtube-premium', 'https://i.imgur.com/ZfewP1Y.png'),
            ('[B][COLOR blueviolet]• [/COLOR][/B][COLOR ghostwhite]USA[/COLOR][B][COLOR blueviolet] •[/COLOR][/B]', '/networks/30/usa-network', 'https://i.imgur.com/Doccw9E.png'),
        ]

        for i in networks: self.list.append(
            {'name': i[0], 'url': self.tvmaze_link + i[1], 'image': i[2], 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list        


    def languages(self):
        languages = [
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Arabic[/COLOR]', 'ar'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Bosnian[/COLOR]', 'bs'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Bulgarian[/COLOR]', 'bg'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Chinese[/COLOR]', 'zh'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Croatian[/COLOR]', 'hr'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Dutch[/COLOR]', 'nl'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]English[/COLOR]', 'en'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Finnish[/COLOR]', 'fi'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]French[/COLOR]', 'fr'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]German[/COLOR]', 'de'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Greek[/COLOR]', 'el'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Hebrew[/COLOR]', 'he'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Hindi[/COLOR]', 'hi'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Hungarian[/COLOR]', 'hu'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Icelandic[/COLOR]', 'is'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Italian[/COLOR]', 'it'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Japanese[/COLOR]', 'ja'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Korean[/COLOR]', 'ko'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Norwegian[/COLOR]', 'no'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Persian[/COLOR]', 'fa'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Polish[/COLOR]', 'pl'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Portuguese[/COLOR]', 'pt'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Punjabi[/COLOR]', 'pa'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Romanian[/COLOR]', 'ro'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Russian[/COLOR]', 'ru'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Serbian[/COLOR]', 'sr'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Spanish[/COLOR]', 'es'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Swedish[/COLOR]', 'sv'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Turkish[/COLOR]', 'tr'),
            ('[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]Ukrainian[/COLOR]', 'uk')
        ]

        for i in languages: self.list.append(
            {'name': str(i[0]), 'url': self.language_link % i[1], 'image': 'tv_international.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def certifications(self):
        certificates = ['[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]TV-G[/COLOR]', '[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]TV-PG[/COLOR]', '[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]TV-14[/COLOR]', '[B][COLOR firebrick]• [/COLOR][/B][COLOR ghostwhite]TV-MA[/COLOR]']

        for i in certificates: self.list.append(
            {'name': str(i), 'url': self.certification_link % str(i).replace('-', '_').lower(),
             'image': 'certificates2.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def certifications(self):
        certificates = ['TV-G', 'TV-PG', 'TV-14', 'TV-MA']

        for i in certificates: self.list.append(
            {'name': str(i), 'url': self.certification_link % str(i).replace('-', '_').lower(),
             'image': 'certificates2.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def persons(self, url):
        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.personlist_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in range(0, len(self.list)): self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def userlists(self):
        try:
            userlists = []
            if trakt.getTraktCredentialsInfo() == False: raise Exception()
            activity = trakt.getActivity()
        except:
            pass

        try:
            if trakt.getTraktCredentialsInfo() == False: raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlists_link,
                                            self.trakt_user): raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlists_link, self.trakt_user)
        except:
            pass
        try:
            self.list = []
            if self.imdb_user == '': raise Exception()
            userlists += cache.get(self.imdb_user_list, 0, self.imdblists_link)
        except:
            pass
        try:
            self.list = []
            if trakt.getTraktCredentialsInfo() == False: raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlikedlists_link,
                                            self.trakt_user): raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlikedlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlikedlists_link, self.trakt_user)
        except:
            pass

        self.list = userlists
        for i in range(0, len(self.list)): self.list[i].update({'image': 'userlists.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def trakt_list(self, url, user):
        try:
            dupes = []

            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            q.update({'extended': 'full'})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q

            result = trakt.getTraktAsJson(u)

            items = []
            for i in result:
                try:
                    items.append(i['show'])
                except:
                    pass
            if len(items) == 0:
                items = result
        except:
            return

        try:
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            if not int(q['limit']) == len(items): raise Exception()
            q.update({'page': str(int(q['page']) + 1)})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            next = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q
            next = next.encode('utf-8')
        except:
            next = ''

        for item in items:
            try:
                title = item['title']
                title = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', title)
                title = client.replaceHTMLCodes(title)

                year = item['year']
                year = re.sub('[^0-9]', '', str(year))

                if int(year) > int((self.datetime).strftime('%Y')): raise Exception()

                imdb = item['ids']['imdb']
                if imdb == None or imdb == '':
                    imdb = '0'
                else:
                    imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))

                tvdb = item['ids']['tvdb']
                tvdb = re.sub('[^0-9]', '', str(tvdb))

                if tvdb == None or tvdb == '' or tvdb in dupes: raise Exception()
                dupes.append(tvdb)

                try:
                    premiered = item['first_aired']
                except:
                    premiered = '0'
                try:
                    premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except:
                    premiered = '0'

                try:
                    studio = item['network']
                except:
                    studio = '0'
                if studio == None: studio = '0'

                try:
                    genre = item['genres']
                except:
                    genre = '0'
                genre = [i.title() for i in genre]
                if genre == []: genre = '0'
                genre = ' / '.join(genre)

                try:
                    duration = str(item['runtime'])
                except:
                    duration = '0'
                if duration == None: duration = '0'

                try:
                    rating = str(item['rating'])
                except:
                    rating = '0'
                if rating == None or rating == '0.0': rating = '0'

                try:
                    votes = str(item['votes'])
                except:
                    votes = '0'
                try:
                    votes = str(format(int(votes), ',d'))
                except:
                    pass
                if votes == None: votes = '0'

                try:
                    mpaa = item['certification']
                except:
                    mpaa = '0'
                if mpaa == None: mpaa = '0'

                try:
                    plot = item['overview']
                except:
                    plot = '0'
                if plot == None: plot = '0'
                plot = client.replaceHTMLCodes(plot)

                self.list.append(
                    {'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': studio,
                     'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'plot': plot,
                     'imdb': imdb, 'tvdb': tvdb, 'poster': '0', 'next': next})
            except:
                pass

        return self.list


    def trakt_user_list(self, url, user):
        try:
            items = trakt.getTraktAsJson(url)
        except:
            pass

        for item in items:
            try:
                try:
                    name = item['list']['name']
                except:
                    name = item['name']
                name = client.replaceHTMLCodes(name)

                try:
                    url = (trakt.slug(item['list']['user']['username']), item['list']['ids']['slug'])
                except:
                    url = ('me', item['ids']['slug'])
                url = self.traktlist_link % url
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list


    def imdb_list(self, url):
        try:
            dupes = []

            for i in re.findall('date\[(\d+)\]', url):
                url = url.replace('date[%s]' % i,
                                  (self.datetime - datetime.timedelta(days=int(i))).strftime('%Y-%m-%d'))

            def imdb_watchlist_id(url):
                return client.parseDOM(client.request(url), 'meta', ret='content', attrs={'property': 'pageId'})[0]

            if url == self.imdbwatchlist_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist_link % url

            elif url == self.imdbwatchlist2_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist2_link % url

            result = client.request(url)

            result = result.replace('\n', ' ')

            items = client.parseDOM(result, 'div', attrs={'class': 'lister-item .+?'})
            items += client.parseDOM(result, 'div', attrs={'class': 'list_item.+?'})
        except:
            return

        try:
            next = client.parseDOM(result, 'a', ret='href', attrs={'class': 'lister-page-next .+?'})
            if len(next) == 0:
                next = client.parseDOM(result, 'a', ret='href', attrs={'class': '.+?lister-page-next .+?'})						   

            if len(next) == 0:
                next = client.parseDOM(result, 'div', attrs={'class': 'pagination'})[0]
                next = zip(client.parseDOM(next, 'a', ret='href'), client.parseDOM(next, 'a'))
                next = [i[0] for i in next if 'Next' in i[1]]

            next = url.replace(urlparse.urlparse(url).query, urlparse.urlparse(next[0]).query)
            next = client.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for item in items:
            try:
                title = client.parseDOM(item, 'a')[1]
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = client.parseDOM(item, 'span', attrs={'class': 'lister-item-year.+?'})
                year += client.parseDOM(item, 'span', attrs={'class': 'year_type'})
                year = re.findall('(\d{4})', year[0])[0]
                year = year.encode('utf-8')

                if int(year) > int((self.datetime).strftime('%Y')): raise Exception()

                imdb = client.parseDOM(item, 'a', ret='href')[0]
                imdb = re.findall('(tt\d*)', imdb)[0]
                imdb = imdb.encode('utf-8')

                if imdb in dupes: raise Exception()
                dupes.append(imdb)

                try:
                    poster = client.parseDOM(item, 'img', ret='loadlate')[0]
                except:
                    poster = '0'
                if '/nopicture/' in poster: poster = '0'
                poster = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', poster)
                poster = client.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                rating = '0'
                try:
                    rating = client.parseDOM(item, 'span', attrs={'class': 'rating-rating'})[0]
                except:
                    pass
                try:
                    rating = client.parseDOM(rating, 'span', attrs={'class': 'value'})[0]
                except:
                    rating = '0'
                try:
                    rating = client.parseDOM(item, 'div', ret='data-value', attrs={'class': '.*?imdb-rating'})[0]
                except:
                    pass
                if rating == '' or rating == '-': rating = '0'
                rating = client.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                plot = '0'
                try:
                    plot = client.parseDOM(item, 'p', attrs={'class': 'text-muted'})[0]
                except:
                    pass
                try:
                    plot = client.parseDOM(item, 'div', attrs={'class': 'item_description'})[0]
                except:
                    pass
                plot = plot.rsplit('<span>', 1)[0].strip()
                plot = re.sub('<.+?>|</.+?>', '', plot)
                if plot == '': plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append(
                    {'title': title, 'originaltitle': title, 'year': year, 'rating': rating, 'plot': plot, 'imdb': imdb,
                     'tvdb': '0', 'poster': poster, 'next': next})
            except:
                pass

        return self.list


    def imdb_person_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'tr', attrs={'class': '.+? detailed'})
        except:
            return

        for item in items:
            try:
                name = client.parseDOM(item, 'a', ret='title')[0]
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = re.findall('(nm\d*)', url, re.I)[0]
                url = self.person_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = client.parseDOM(item, 'img', ret='src')[0]
                if not ('._SX' in image or '._SY' in image): raise Exception()
                image = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', image)
                image = client.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list


    def imdb_user_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'li', attrs={'class': 'ipl-zebra-list__item user-list'})
        except:
            pass

        for item in items:
            try:
                name = client.parseDOM(item, 'a')[0]
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = url = url.split('/list/', 1)[-1].strip('/')
                url = self.imdblist_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list


    def tvmaze_list(self, url):
        try:
            result = client.request(url)
            result = client.parseDOM(result, 'section', attrs={'id': 'this-seasons-shows'})

            items = client.parseDOM(result, 'div', attrs={'class': 'content auto cell'})
            items = [client.parseDOM(i, 'a', ret='href') for i in items]
            items = [i[0] for i in items if len(i) > 0]
            items = [re.findall('/(\d+)/', i) for i in items]
            items = [i[0] for i in items if len(i) > 0]
            items = items[:50]
        except:
            return

        def items_list(i):
            try:
                url = self.tvmaze_info_link % i

                item = client.request(url)
                item = json.loads(item)

                title = item['name']
                title = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', title)
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = item['premiered']
                year = re.findall('(\d{4})', year)[0]
                year = year.encode('utf-8')

                if int(year) > int((self.datetime).strftime('%Y')): raise Exception()

                imdb = item['externals']['imdb']
                if imdb == None or imdb == '':
                    imdb = '0'
                else:
                    imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                tvdb = item['externals']['thetvdb']
                tvdb = re.sub('[^0-9]', '', str(tvdb))
                tvdb = tvdb.encode('utf-8')

                if tvdb == None or tvdb == '': raise Exception()

                try:
                    poster = item['image']['original']
                except:
                    poster = '0'
                if poster == None or poster == '': poster = '0'
                poster = poster.encode('utf-8')

                premiered = item['premiered']
                try:
                    premiered = re.findall('(\d{4}-\d{2}-\d{2})', premiered)[0]
                except:
                    premiered = '0'
                premiered = premiered.encode('utf-8')

                try:
                    studio = item['network']['name']
                except:
                    studio = '0'
                if studio == None: studio = '0'
                studio = studio.encode('utf-8')

                try:
                    genre = item['genres']
                except:
                    genre = '0'
                genre = [i.title() for i in genre]
                if genre == []: genre = '0'
                genre = ' / '.join(genre)
                genre = genre.encode('utf-8')

                try:
                    duration = item['runtime']
                except:
                    duration = '0'
                if duration == None: duration = '0'
                duration = str(duration)
                duration = duration.encode('utf-8')

                try:
                    rating = item['rating']['average']
                except:
                    rating = '0'
                if rating == None or rating == '0.0': rating = '0'
                rating = str(rating)
                rating = rating.encode('utf-8')

                try:
                    plot = item['summary']
                except:
                    plot = '0'
                if plot == None: plot = '0'
                plot = re.sub('<.+?>|</.+?>|\n', '', plot)
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                try:
                    content = item['type'].lower()
                except:
                    content = '0'
                if content == None or content == '': content = '0'
                content = content.encode('utf-8')

                self.list.append(
                    {'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': studio,
                     'genre': genre, 'duration': duration, 'rating': rating, 'plot': plot, 'imdb': imdb, 'tvdb': tvdb,
                     'poster': poster, 'content': content})
            except:
                pass

        try:
            threads = []
            for i in items: threads.append(workers.Thread(items_list, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            filter = [i for i in self.list if i['content'] == 'scripted']
            filter += [i for i in self.list if not i['content'] == 'scripted']
            self.list = filter

            return self.list
        except:
            return


    def worker(self, level=1):
        self.meta = []
        total = len(self.list)

        self.fanart_tv_headers = {'api-key': 'NDZkZmMyN2M1MmE0YTc3MjY3NWQ4ZTMyYjdiY2E2OGU='.decode('base64')}
        if not self.fanart_tv_user == '':
            self.fanart_tv_headers.update({'client-key': self.fanart_tv_user})

        for i in range(0, total): self.list[i].update({'metacache': False})

        self.list = metacache.fetch(self.list, self.lang, self.user)

        for r in range(0, total, 40):
            threads = []
            for i in range(r, r + 40):
                if i <= total: threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            if self.meta: metacache.insert(self.meta)

        self.list = [i for i in self.list if not i['tvdb'] == '0']

        if self.fanart_tv_user == '':
            for i in self.list: i.update({'clearlogo': '0', 'clearart': '0'})


    def super_info(self, i):
        try:
            if self.list[i]['metacache'] == True: raise Exception()

            imdb = self.list[i]['imdb'] if 'imdb' in self.list[i] else '0'
            tvdb = self.list[i]['tvdb'] if 'tvdb' in self.list[i] else '0'

            if imdb == '0':
                try:
                    imdb = \
                    trakt.SearchTVShow(urllib.quote_plus(self.list[i]['title']), self.list[i]['year'], full=False)[0]
                    imdb = imdb.get('show', '0')
                    imdb = imdb.get('ids', {}).get('imdb', '0')
                    imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))

                    if not imdb: imdb = '0'
                except:
                    imdb = '0'

            if tvdb == '0' and not imdb == '0':
                url = self.tvdb_by_imdb % imdb

                result = client.request(url, timeout='10')

                try:
                    tvdb = client.parseDOM(result, 'seriesid')[0]
                except:
                    tvdb = '0'

                try:
                    name = client.parseDOM(result, 'SeriesName')[0]
                except:
                    name = '0'
                dupe = re.findall('[***]Duplicate (\d*)[***]', name)
                if dupe: tvdb = str(dupe[0])

                if tvdb == '': tvdb = '0'


            if tvdb == '0':
                url = self.tvdb_by_query % (urllib.quote_plus(self.list[i]['title']))

                years = [str(self.list[i]['year']), str(int(self.list[i]['year']) + 1),
                         str(int(self.list[i]['year']) - 1)]

                tvdb = client.request(url, timeout='10')
                tvdb = re.sub(r'[^\x00-\x7F]+', '', tvdb)
                tvdb = client.replaceHTMLCodes(tvdb)
                tvdb = client.parseDOM(tvdb, 'Series')
                tvdb = [(x, client.parseDOM(x, 'SeriesName'), client.parseDOM(x, 'FirstAired')) for x in tvdb]
                tvdb = [(x, x[1][0], x[2][0]) for x in tvdb if len(x[1]) > 0 and len(x[2]) > 0]
                tvdb = [x for x in tvdb if cleantitle.get(self.list[i]['title']) == cleantitle.get(x[1])]
                tvdb = [x[0][0] for x in tvdb if any(y in x[2] for y in years)][0]
                tvdb = client.parseDOM(tvdb, 'seriesid')[0]

                if tvdb == '': tvdb = '0'


            url = self.tvdb_info_link % tvdb
            item = client.request(url, timeout='10')
            if item == None: raise Exception()

            if imdb == '0':
                try:
                    imdb = client.parseDOM(item, 'IMDB_ID')[0]
                except:
                    pass
                if imdb == '': imdb = '0'
                imdb = imdb.encode('utf-8')


            try:
                title = client.parseDOM(item, 'SeriesName')[0]
            except:
                title = ''
            if title == '': title = '0'
            title = client.replaceHTMLCodes(title)
            title = title.encode('utf-8')

            try:
                year = client.parseDOM(item, 'FirstAired')[0]
            except:
                year = ''
            try:
                year = re.compile('(\d{4})').findall(year)[0]
            except:
                year = ''
            if year == '': year = '0'
            year = year.encode('utf-8')

            try:
                premiered = client.parseDOM(item, 'FirstAired')[0]
            except:
                premiered = '0'
            if premiered == '': premiered = '0'
            premiered = client.replaceHTMLCodes(premiered)
            premiered = premiered.encode('utf-8')

            try:
                studio = client.parseDOM(item, 'Network')[0]
            except:
                studio = ''
            if studio == '': studio = '0'
            studio = client.replaceHTMLCodes(studio)
            studio = studio.encode('utf-8')

            try:
                genre = client.parseDOM(item, 'Genre')[0]
            except:
                genre = ''
            genre = [x for x in genre.split('|') if not x == '']
            genre = ' / '.join(genre)
            if genre == '': genre = '0'
            genre = client.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')

            try:
                duration = client.parseDOM(item, 'Runtime')[0]
            except:
                duration = ''
            if duration == '': duration = '0'
            duration = client.replaceHTMLCodes(duration)
            duration = duration.encode('utf-8')

            try:
                rating = client.parseDOM(item, 'Rating')[0]
            except:
                rating = ''
            if 'rating' in self.list[i] and not self.list[i]['rating'] == '0':
                rating = self.list[i]['rating']
            if rating == '': rating = '0'
            rating = client.replaceHTMLCodes(rating)
            rating = rating.encode('utf-8')

            try:
                votes = client.parseDOM(item, 'RatingCount')[0]
            except:
                votes = ''
            if 'votes' in self.list[i] and not self.list[i]['votes'] == '0':
                votes = self.list[i]['votes']
            if votes == '': votes = '0'
            votes = client.replaceHTMLCodes(votes)
            votes = votes.encode('utf-8')

            try:
                mpaa = client.parseDOM(item, 'ContentRating')[0]
            except:
                mpaa = ''
            if mpaa == '': mpaa = '0'
            mpaa = client.replaceHTMLCodes(mpaa)
            mpaa = mpaa.encode('utf-8')

            try:
                cast = client.parseDOM(item, 'Actors')[0]
            except:
                cast = ''
            cast = [x for x in cast.split('|') if not x == '']
            try:
                cast = [(x.encode('utf-8'), '') for x in cast]
            except:
                cast = []
            if cast == []: cast = '0'

            try:
                plot = client.parseDOM(item, 'Overview')[0]
            except:
                plot = ''
            if plot == '': plot = '0'
            plot = client.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')

            try:
                poster = client.parseDOM(item, 'poster')[0]
            except:
                poster = ''
            if not poster == '':
                poster = self.tvdb_image + poster
            else:
                poster = '0'
            if 'poster' in self.list[i] and poster == '0': poster = self.list[i]['poster']
            poster = client.replaceHTMLCodes(poster)
            poster = poster.encode('utf-8')

            try:
                banner = client.parseDOM(item, 'banner')[0]
            except:
                banner = ''
            if not banner == '':
                banner = self.tvdb_image + banner
            else:
                banner = '0'
            banner = client.replaceHTMLCodes(banner)
            banner = banner.encode('utf-8')

            try:
                fanart = client.parseDOM(item, 'fanart')[0]
            except:
                fanart = ''
            if not fanart == '':
                fanart = self.tvdb_image + fanart
            else:
                fanart = '0'
            fanart = client.replaceHTMLCodes(fanart)
            fanart = fanart.encode('utf-8')

            try:
                artmeta = True
                # if self.fanart_tv_user == '': raise Exception()
                art = client.request(self.fanart_tv_art_link % tvdb, headers=self.fanart_tv_headers, timeout='10',
                                     error=True)
                try:
                    art = json.loads(art)
                except:
                    artmeta = False
            except:
                pass

            try:
                poster2 = art['tvposter']
                poster2 = [x for x in poster2 if x.get('lang') == self.lang][::-1] + [x for x in poster2 if
                                                                                      x.get('lang') == 'en'][::-1] + [x
                                                                                                                      for
                                                                                                                      x
                                                                                                                      in
                                                                                                                      poster2
                                                                                                                      if
                                                                                                                      x.get(
                                                                                                                          'lang') in [
                                                                                                                          '00',
                                                                                                                          '']][
                                                                                                                     ::-1]
                poster2 = poster2[0]['url'].encode('utf-8')
            except:
                poster2 = '0'

            try:
                fanart2 = art['showbackground']
                fanart2 = [x for x in fanart2 if x.get('lang') == self.lang][::-1] + [x for x in fanart2 if
                                                                                      x.get('lang') == 'en'][::-1] + [x
                                                                                                                      for
                                                                                                                      x
                                                                                                                      in
                                                                                                                      fanart2
                                                                                                                      if
                                                                                                                      x.get(
                                                                                                                          'lang') in [
                                                                                                                          '00',
                                                                                                                          '']][
                                                                                                                     ::-1]
                fanart2 = fanart2[0]['url'].encode('utf-8')
            except:
                fanart2 = '0'

            try:
                banner2 = art['tvbanner']
                banner2 = [x for x in banner2 if x.get('lang') == self.lang][::-1] + [x for x in banner2 if
                                                                                      x.get('lang') == 'en'][::-1] + [x
                                                                                                                      for
                                                                                                                      x
                                                                                                                      in
                                                                                                                      banner2
                                                                                                                      if
                                                                                                                      x.get(
                                                                                                                          'lang') in [
                                                                                                                          '00',
                                                                                                                          '']][
                                                                                                                     ::-1]
                banner2 = banner2[0]['url'].encode('utf-8')
            except:
                banner2 = '0'

            try:
                if 'hdtvlogo' in art:
                    clearlogo = art['hdtvlogo']
                else:
                    clearlogo = art['clearlogo']
                clearlogo = [x for x in clearlogo if x.get('lang') == self.lang][::-1] + [x for x in clearlogo if
                                                                                          x.get('lang') == 'en'][
                                                                                         ::-1] + [x for x in clearlogo
                                                                                                  if x.get('lang') in [
                                                                                                      '00', '']][::-1]
                clearlogo = clearlogo[0]['url'].encode('utf-8')
            except:
                clearlogo = '0'

            try:
                if 'hdclearart' in art:
                    clearart = art['hdclearart']
                else:
                    clearart = art['clearart']
                clearart = [x for x in clearart if x.get('lang') == self.lang][::-1] + [x for x in clearart if
                                                                                        x.get('lang') == 'en'][::-1] + [
                                                                                                                           x
                                                                                                                           for
                                                                                                                           x
                                                                                                                           in
                                                                                                                           clearart
                                                                                                                           if
                                                                                                                           x.get(
                                                                                                                               'lang') in [
                                                                                                                               '00',
                                                                                                                               '']][
                                                                                                                       ::-1]
                clearart = clearart[0]['url'].encode('utf-8')
            except:
                clearart = '0'

            item = {'title': title, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'poster': poster, 'poster2': poster2,
                    'banner': banner, 'banner2': banner2, 'fanart': fanart, 'fanart2': fanart2, 'clearlogo': clearlogo,
                    'clearart': clearart, 'premiered': premiered, 'studio': studio, 'genre': genre,
                    'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'cast': cast, 'plot': plot}
            item = dict((k, v) for k, v in item.iteritems() if not v == '0')
            self.list[i].update(item)

            if artmeta == False: raise Exception()

            meta = {'imdb': imdb, 'tvdb': tvdb, 'lang': self.lang, 'user': self.user, 'item': item}
            self.meta.append(meta)
        except:
            pass


    def tvshowDirectory(self, items):
        if items == None or len(items) == 0: control.idle(); sys.exit()

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()

        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')

        traktCredentials = trakt.getTraktCredentialsInfo()

        try:
            isOld = False; control.item().getArt('type')
        except:
            isOld = True

        indicators = playcount.getTVShowIndicators(
            refresh=True) if action == 'tvshows' else playcount.getTVShowIndicators()

        flatten = True if control.setting('flatten.tvshows') == 'true' else False

        watchedMenu = control.lang(32068).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(
            32066).encode('utf-8')

        unwatchedMenu = control.lang(32069).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(
            32067).encode('utf-8')

        queueMenu = control.lang(32065).encode('utf-8')

        traktManagerMenu = control.lang(32070).encode('utf-8')

        nextMenu = control.lang(32053).encode('utf-8')

        playRandom = control.lang(32535).encode('utf-8')

        addToLibrary = control.lang(32551).encode('utf-8')

        for i in items:
            try:
                label = i['title']
                systitle = sysname = urllib.quote_plus(i['originaltitle'])
                sysimage = urllib.quote_plus(i['poster'])
                imdb, tvdb, year = i['imdb'], i['tvdb'], i['year']

                meta = dict((k, v) for k, v in i.iteritems() if not v == '0')
                meta.update({'code': imdb, 'imdbnumber': imdb, 'imdb_id': imdb})
                meta.update({'tvdb_id': tvdb})
                meta.update({'mediatype': 'tvshow'})
                meta.update({'trailer': '%s?action=trailer&name=%s&tvdb=%s&season=1' % (sysaddon, urllib.quote_plus(label),tvdb)})
                if not 'duration' in i:
                    meta.update({'duration': '60'})
                elif i['duration'] == '0':
                    meta.update({'duration': '60'})
                try:
                    meta.update({'duration': str(int(meta['duration']) * 60)})
                except:
                    pass
                try:
                    meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except:
                    pass

                try:
                    overlay = int(playcount.getTVShowOverlay(indicators, tvdb))
                    if overlay == 7:
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass


                if flatten == True:
                    url = '%s?action=episodes&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s' % (
                    sysaddon, systitle, year, imdb, tvdb)
                else:
                    url = '%s?action=seasons&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s' % (
                    sysaddon, systitle, year, imdb, tvdb)

                cm = []

                cm.append(('Find similar',
                           'ActivateWindow(10025,%s?action=tvshows&url=https://api.trakt.tv/shows/%s/related,return)' % (
                               sysaddon, imdb)))

                cm.append((playRandom,
                           'RunPlugin(%s?action=random&rtype=season&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s)' % (
                           sysaddon, urllib.quote_plus(systitle), urllib.quote_plus(year), urllib.quote_plus(imdb),
                           urllib.quote_plus(tvdb))))

                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                cm.append((watchedMenu, 'RunPlugin(%s?action=tvPlaycount&name=%s&imdb=%s&tvdb=%s&query=7)' % (
                sysaddon, systitle, imdb, tvdb)))

                cm.append((unwatchedMenu, 'RunPlugin(%s?action=tvPlaycount&name=%s&imdb=%s&tvdb=%s&query=6)' % (
                sysaddon, systitle, imdb, tvdb)))

                if traktCredentials == True:
                    cm.append((traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&tvdb=%s&content=tvshow)' % (
                    sysaddon, sysname, tvdb)))

                if isOld == True:
                    cm.append((control.lang2(19033).encode('utf-8'), 'Action(Info)'))

                cm.append((addToLibrary,
                           'RunPlugin(%s?action=tvshowToLibrary&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s)' % (
                           sysaddon, systitle, year, imdb, tvdb)))

                item = control.item(label=label)

                art = {}

                if 'poster' in i and not i['poster'] == '0':
                    art.update({'icon': i['poster'], 'thumb': i['poster'], 'poster': i['poster']})
                # elif 'poster2' in i and not i['poster2'] == '0':
                # art.update({'icon': i['poster2'], 'thumb': i['poster2'], 'poster': i['poster2']})
                else:
                    art.update({'icon': addonPoster, 'thumb': addonPoster, 'poster': addonPoster})

                if 'banner' in i and not i['banner'] == '0':
                    art.update({'banner': i['banner']})
                # elif 'banner2' in i and not i['banner2'] == '0':
                # art.update({'banner': i['banner2']})
                elif 'fanart' in i and not i['fanart'] == '0':
                    art.update({'banner': i['fanart']})
                else:
                    art.update({'banner': addonBanner})

                if 'clearlogo' in i and not i['clearlogo'] == '0':
                    art.update({'clearlogo': i['clearlogo']})

                if 'clearart' in i and not i['clearart'] == '0':
                    art.update({'clearart': i['clearart']})

                if settingFanart == 'true' and 'fanart' in i and not i['fanart'] == '0':
                    item.setProperty('Fanart_Image', i['fanart'])
                # elif settingFanart == 'true' and 'fanart2' in i and not i['fanart2'] == '0':
                # item.setProperty('Fanart_Image', i['fanart2'])
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.setArt(art)
                item.addContextMenuItems(cm)
                item.setInfo(type='Video', infoLabels=meta)

                video_streaminfo = {'codec': 'h264'}
                item.addStreamInfo('video', video_streaminfo)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass

        try:
            url = items[0]['next']
            if url == '': raise Exception()

            icon = control.addonNext()
            url = '%s?action=tvshowPage&url=%s' % (sysaddon, urllib.quote_plus(url))

            item = control.item(label=nextMenu)

            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon})
            if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)

            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass

        control.content(syshandle, 'tvshows')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('tvshows', {'skin.estuary': 55, 'skin.confluence': 500})


    def addDirectory(self, items, queue=False):
        if items == None or len(items) == 0: control.idle(); sys.exit()

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

        queueMenu = control.lang(32065).encode('utf-8')

        playRandom = control.lang(32535).encode('utf-8')

        addToLibrary = control.lang(32551).encode('utf-8')

        for i in items:
            try:
                name = i['name']

                if i['image'].startswith('http'):
                    thumb = i['image']
                elif not artPath == None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb

                url = '%s?action=%s' % (sysaddon, i['action'])
                try:
                    url += '&url=%s' % urllib.quote_plus(i['url'])
                except:
                    pass

                cm = []

                cm.append((playRandom,
                           'RunPlugin(%s?action=random&rtype=show&url=%s)' % (sysaddon, urllib.quote_plus(i['url']))))

                if queue == True:
                    cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                try:
                    cm.append((addToLibrary, 'RunPlugin(%s?action=tvshowsToLibrary&url=%s)' % (
                    sysaddon, urllib.quote_plus(i['context']))))
                except:
                    pass

                item = control.item(label=name)

                item.setArt({'icon': thumb, 'thumb': thumb})
                if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)

                item.addContextMenuItems(cm)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass

        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


