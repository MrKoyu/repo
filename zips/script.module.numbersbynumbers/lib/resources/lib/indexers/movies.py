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
from resources.lib.modules import cleangenre
from resources.lib.modules import cleantitle
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import metacache
from resources.lib.modules import playcount
from resources.lib.modules import workers
from resources.lib.modules import views
from resources.lib.modules import utils
from resources.lib.indexers import navigator
from resources.lib.modules import log_utils										   

import os, sys, re, json, urllib, urlparse, datetime, xbmc

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', ''))) if len(sys.argv) > 1 else dict()

action = params.get('action')




class movies:
    def __init__(self):
        self.list = []

        self.imdb_link = 'http://www.imdb.com'
        self.trakt_link = 'http://api.trakt.tv'
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours=5))
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.year_date = (self.datetime - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        self.today_date = (self.datetime).strftime('%Y-%m-%d')
        self.trakt_user = control.setting('trakt.user').strip()
        self.imdb_user = control.setting('imdb.user').replace('ur', '')
        self.tm_user = control.setting('tm.user')
        self.fanart_tv_user = control.setting('fanart.tv.user')
        self.user = str(control.setting('fanart.tv.user')) + str(control.setting('tm.user'))
        self.lang = control.apiLanguage()['trakt']
        self.hidecinema = control.setting('hidecinema')

        self.search_link = 'http://api.trakt.tv/search/movie?limit=20&page=1&query='
        self.fanart_tv_art_link = 'http://webservice.fanart.tv/v3/movies/%s'
        self.fanart_tv_level_link = 'http://webservice.fanart.tv/v3/level'
        self.tm_art_link = 'http://api.themoviedb.org/3/movie/%s/images?api_key=%s&language=en-US&include_image_language=en,%s,null' % (
        '%s', self.tm_user, self.lang)
        self.tm_img_link = 'https://image.tmdb.org/t/p/w%s%s'

        self.persons_link = 'http://www.imdb.com/search/name?count=100&name='
        self.personlist_link = 'http://www.imdb.com/search/name?count=100&gender=male,female'
        self.person_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&role=%s&sort=year,desc&count=40&start=1'
        self.keyword_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&release_date=,date[0]&keywords=%s&sort=moviemeter,asc&count=40&start=1'
        self.oscars_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&groups=oscar_best_picture_winners&sort=year,desc&count=40&start=1'
        self.theaters_link = 'https://www.imdb.com/search/title?title_type=feature&num_votes=1000,&release_date=date[365],date[0]&sort=moviemeter,asc&count=40&start=1'
        self.year_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&year=%s,%s&sort=moviemeter,asc&count=40&start=1'
		
        if self.hidecinema == 'true':
            self.popular_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&groups=top_1000&release_date=,date[90]&sort=moviemeter,asc&count=40&start=1'
            self.views_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&sort=num_votes,desc&release_date=,date[90]&count=40&start=1'
            self.featured_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&release_date=date[365],date[90]&sort=moviemeter,asc&count=40&start=1'
            self.genre_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&release_date=,date[90]&genres=%s&sort=moviemeter,asc&count=40&start=1'
            self.language_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&release_date=,date[90]&count=40&start=1'
            self.certification_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&certificates=us:%s&sort=moviemeter,asc&release_date=,date[90]&count=40&start=1'
            self.boxoffice_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&sort=boxoffice_gross_us,desc&release_date=,date[90]&count=40&start=1'
        else:
            self.popular_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&groups=top_1000&sort=moviemeter,asc&count=40&start=1'
            self.views_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&sort=num_votes,desc&count=40&start=1'
            self.featured_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&release_date=date[365],date[60]&sort=moviemeter,asc&count=40&start=1'
            self.genre_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&release_date=,date[0]&genres=%s&sort=moviemeter,asc&count=40&start=1'
            self.language_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&count=40&start=1'
            self.certification_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&certificates=us:%s&sort=moviemeter,asc&count=40&start=1'
            self.boxoffice_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&sort=boxoffice_gross_us,desc&count=40&start=1'
            self.advancedsearchkidshorror_link = 'https://www.imdb.com/list/ls052297683/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.advancedsearchanimation_link = 'https://www.imdb.com/search/title?title_type=feature&num_votes=10000,&genres=animation&certificates=US%3AG,US%3APG,US%3APG-13&sort=user_rating,desc'
            self.advancedsearchtrending_link = 'https://www.imdb.com/search/title?title_type=feature&genres=animation,family&sort=moviemeter,asc&page=1&ref_=adv_prv'
            self.advancedsearchdreamworks_link = 'https://www.imdb.com/list/ls068935612/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.advancedsearchdisneyland_link = 'https://www.imdb.com/list/ls052303324/?sort=release_date,desc&st_dt=&mode=detail&page=1'
            self.advancedsearchdisneymovietv_link = 'https://www.imdb.com/search/keyword/?keywords=disney-channel-original-movie&ref_=kw_ref_typ&sort=moviemeter,asc&mode=detail&page=1&title_type=tvMovie'
            self.advancedsearchpixar_link = 'https://www.imdb.com/search/title?title_type=feature&locations=Pixar+Animation+Studios+-+1200+Park+Avenue,+Emeryville,+California,+USA'
            self.advancedsearchchronological_link = 'https://www.imdb.com/list/ls070880401/?sort=list_order,asc&st_dt=&mode=detail&page=1'
            self.advancedsearchliveaction_link = 'https://www.imdb.com/list/ls056913461/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.advancedsearchnature_link = 'https://www.imdb.com/search/title?companies=co0236496'
            self.advancedsearchmarvelstudios_link = 'https://www.imdb.com/list/ls000024621/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.advancedsearchdcuniverse_link = 'https://www.imdb.com/list/ls000024643/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.advancedsearchdcvsmarvel_link = 'https://www.imdb.com/list/ls065237713/?sort=alpha,asc&st_dt=&mode=detail&page=1'
            self.advancedsearchdcanimation_link  = 'https://www.imdb.com/list/ls068125936/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.advancedsearchmarvelanimation_link = 'https://www.imdb.com/list/ls025759115/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.advancedsearchtop10000_link = 'https://www.imdb.com/search/title/?count=1000&genres=family&production_status=released&title_type=feature&view=simple'
            self.advancedsearchjustlego_link = 'https://www.imdb.com/list/ls040509959/?sort=release_date,desc&st_dt=&mode=detail&page=1'
            self.advancedsearchgamers_link = 'https://www.imdb.com/search/keyword/?keywords=based-on-video-game&sort=moviemeter,asc&mode=detail&page=1'

            self.advancedsearchanimegrownup_link = 'https://www.imdb.com/search/keyword/?keywords=anime%2Cfemale-nudity&sort=num_votes,desc&mode=detail&page=1&ref_=kw_ref_key'
            self.advancedsearchanimemostviewed_link = 'https://www.imdb.com/list/ls004037854/?sort=release_date,desc&st_dt=&mode=detail&page=1'
            self.advancedsearchanimehighlyrated_link = 'https://www.imdb.com/search/title?count=100&keywords=anime&num_votes=2000,&explore=title_type&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3999419c-1229-4fa7-9240-55e83e21cecb&pf_rd_r=XP4M7Q29XXN28VM9Z00Q&pf_rd_s=right-1&pf_rd_t=15051&pf_rd_i=genre&title_type=movie&sort=num_votes,desc&ref_=adv_explore_rhs'
            self.advancedsearchanimetrending_link = 'https://www.imdb.com/search/title?count=100&keywords=anime&num_votes=2000,&explore=title_type&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3999419c-1229-4fa7-9240-55e83e21cecb&pf_rd_r=4TSXV0JKMKVBW4YXCN93&pf_rd_s=right-1&pf_rd_t=15051&pf_rd_i=genre&sort=year,desc&title_type=movie&ref_=adv_explore_rhs'

            self.advancedsearchrandomflixaction_link = 'https://www.imdb.com/search/title/?genres=action&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_1'
            self.advancedsearchrandomflixadventure_link = 'https://www.imdb.com/search/title/?title_type=feature&num_votes=10000,&genres=action&genres=Adventure&languages=en&explore=genres&ref_=adv_explore_rhs'
            self.advancedsearchrandomflixanimation_link = 'https://www.imdb.com/search/title/?genres=animation&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_3'
            self.advancedsearchrandomflixbiography_link = 'https://www.imdb.com/search/title/?genres=biography&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_4'
            self.advancedsearchrandomflixcomedy_link = 'https://www.imdb.com/search/title/?genres=comedy&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_5'
            self.advancedsearchrandomflixcrime_link = 'https://www.imdb.com/search/title/?genres=crime&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_6'
            self.advancedsearchrandomflixdocumentary_link = 'https://www.imdb.com/search/title/?languages=en&sort=user_rating,desc&title_type=documentary&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_7'
            self.advancedsearchrandomflixdrama_link = 'https://www.imdb.com/search/title/?genres=drama&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_8'
            self.advancedsearchrandomflixfamily_link = 'https://www.imdb.com/search/title/?genres=family&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_9'
            self.advancedsearchrandomflixfantasy_link = 'https://www.imdb.com/search/title/?genres=fantasy&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_10'
            self.advancedsearchrandomflixfilmnoir_link = 'https://www.imdb.com/search/title/?genres=film-noir&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_11'
            self.advancedsearchrandomflixhistory_link = 'https://www.imdb.com/search/title/?genres=history&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_12'
            self.advancedsearchrandomflixhorror_link = 'https://www.imdb.com/search/title/?genres=horror&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_13'
            self.advancedsearchrandomflixmusic_link = 'https://www.imdb.com/search/title/?genres=music&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_14'
            self.advancedsearchrandomflixmusical_link = 'https://www.imdb.com/search/title/?genres=musical&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_15'
            self.advancedsearchrandomflixmystery_link = 'https://www.imdb.com/search/title/?genres=mystery&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_16'
            self.advancedsearchrandomflixromance_link = 'https://www.imdb.com/search/title/?genres=romance&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_17'
            self.advancedsearchrandomflixscifi_link = 'https://www.imdb.com/search/title/?genres=sci-fi&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_18'
            self.advancedsearchrandomflixshort_link = 'https://www.imdb.com/search/title/?languages=en&sort=user_rating,desc&title_type=short&num_votes=3000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_19'
            self.advancedsearchrandomflixsport_link = 'https://www.imdb.com/search/title/?genres=sport&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_20'
            self.advancedsearchrandomflixsuperhero_link = 'https://www.imdb.com/search/title/?keywords=superhero&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_21'
            self.advancedsearchrandomflixthriller_link = 'https://www.imdb.com/search/title/?genres=thriller&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_22'
            self.advancedsearchrandomflixwar_link = 'https://www.imdb.com/search/title/?genres=war&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_23'
            self.advancedsearchrandomflixwestern_link = 'https://www.imdb.com/search/title/?genres=western&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=d0addcab-e8f0-45ef-9965-515319b79038&pf_rd_r=H2CRPQZEDQJVHB6GNDK5&pf_rd_s=right-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvtre_24'

            self.collectionsforeign_link = 'https://www.imdb.com/list/ls079108574/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionstruestory_link = 'https://www.imdb.com/list/ls076521870/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsdrama_link = 'https://www.imdb.com/list/ls059223247/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionscrime_link = 'https://www.imdb.com/list/ls076521250/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsdocu_link = 'https://www.imdb.com/list/ls066567004/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsaction_link = 'https://www.imdb.com/list/ls076521467/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsmystery_link = 'https://www.imdb.com/list/ls076523709/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionscomedy_link = 'https://www.imdb.com/list/ls076523084/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionssports_link = 'https://www.imdb.com/list/ls076523017/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsanimation_link = 'https://www.imdb.com/list/ls071466272/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsfather_link = 'https://www.imdb.com/list/ls068335911/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsmother_link = 'https://www.imdb.com/list/ls021611065/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionspsychological_link = 'https://www.imdb.com/list/ls066150075/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionstwist_link = 'https://www.imdb.com/list/ls066370089/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsdialogue_link = 'https://www.imdb.com/list/ls068371010/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsrevenge_link = 'https://www.imdb.com/list/ls066797820/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionshumor_link = 'https://www.imdb.com/list/ls068193810/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionswar_link = 'https://www.imdb.com/list/ls068103631/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsjornalism_link = 'https://www.imdb.com/list/ls024737060/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsroadtrip_link = 'https://www.imdb.com/list/ls066135354/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionspolitical_link = 'https://www.imdb.com/list/ls066312970/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsmental_link = 'https://www.imdb.com/list/ls066746282/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionskillers_link = 'https://www.imdb.com/list/ls063841856/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionswestern_link = 'https://www.imdb.com/list/ls066568329/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsinspirational_link = 'https://www.imdb.com/list/ls066222382/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsmusic_link = 'https://www.imdb.com/list/ls066191116/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsromance_link = 'https://www.imdb.com/list/ls066159310/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsspy_link = 'https://www.imdb.com/list/ls066367722/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsfilm_link = 'https://www.imdb.com/list/ls066916316/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionstimetravel_link = 'https://www.imdb.com/list/ls066184124/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsgangster_link = 'https://www.imdb.com/list/ls066176690/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionssurvival_link = 'https://www.imdb.com/list/ls064685738/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsfeelgood_link = 'https://www.imdb.com/list/ls021615613/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionschild_link = 'https://www.imdb.com/list/ls062630867/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsprison_link = 'https://www.imdb.com/list/ls066502835/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsoldage_link = 'https://www.imdb.com/list/ls069248253/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsoneroom_link = 'https://www.imdb.com/list/ls066746643/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsdisaster_link = 'https://www.imdb.com/list/ls062746803/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionscourtroom_link = 'https://www.imdb.com/list/ls066198904/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsdarkcomedy_link = 'https://www.imdb.com/list/ls066399600/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionssuperhero_link = 'https://www.imdb.com/list/ls066789806/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsheists_link = 'https://www.imdb.com/list/ls066780524/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsteen_link = 'https://www.imdb.com/list/ls066113037/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsaddiction_link = 'https://www.imdb.com/list/ls066788382/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionszombie_link = 'https://www.imdb.com/list/ls066165115/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsactionhero_link = 'https://www.imdb.com/search/keyword/?keywords=action-hero&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=7846868c-8414-4178-8f43-9ad6b2ef0baf&pf_rd_r=N2RAG179F05MS9C7TEF4&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=moka&ref_=kw_1&sort=num_votes,desc&mode=detail&page=1'
            self.collectionshackers_link = 'https://www.imdb.com/list/ls000393956/?sort=user_rating,desc&st_dt=&mode=detail&page=1'
            self.collectionsbestforeign_link = 'https://www.imdb.com/list/ls052393071/?sort=release_date,desc&st_dt=&mode=detail&page=1'
            self.collectionsinterforeign_link = 'https://www.imdb.com/list/ls009876733/?sort=user_rating,desc&st_dt=&mode=detail&page=1'
            self.collectionsinterbrazilian_link = 'https://www.imdb.com/list/ls066191890/?sort=user_rating,desc&st_dt=&mode=detail&page=1'
            self.collectionsinterasian_link = 'https://www.imdb.com/list/ls002750040/?ref_=otl_2&sort=user_rating,desc&st_dt=&mode=detail&page=1'
            self.collectionsinterhindi_link = 'https://www.imdb.com/list/ls051594496/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionsinterbollywood_link = 'https://www.imdb.com/list/ls071881610/?sort=release_date,desc&st_dt=&mode=detail&page=1'
            self.collectionsinterbollywooderotic_link = 'https://www.imdb.com/list/ls042765938/?sort=release_date,desc&st_dt=&mode=detail&page=1'
            self.collectionsinterfrench_link = 'https://www.imdb.com/list/ls009250657/?sort=user_rating,desc&st_dt=&mode=detail&page=1'
            self.collectionsintergerman_link = 'https://www.imdb.com/list/ls054028609/?ref_=otl_1&sort=user_rating,desc&st_dt=&mode=detail&page=1'

            self.collectionstop1000a_link = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating'
            self.collectionstop1000c_link = 'https://www.imdb.com/list/ls006266261/?sort=release_date,desc&st_dt=&mode=detail&page=1'
            self.collectionswallmark_link = 'https://www.imdb.com/list/ls069761801/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.collectionslifetime_link = 'https://www.imdb.com/list/ls073816184/?st_dt=&mode=detail&page=1&sort=user_rating,desc'
            self.collectionslifetimeb_link = 'https://www.imdb.com/list/ls062591941/?st_dt=&mode=detail&page=1&sort=user_rating,desc'

            self.holidayschristmas_link = 'https://www.imdb.com/list/ls000096828/?sort=moviemeter,asc&st_dt=&mode=detail&page=1'
            self.holidaysthanksgiven_link = 'https://www.imdb.com/search/keyword/?keywords=thanksgiving&sort=num_votes,desc&mode=detail&page=1'
            self.holidayhalloween_link = 'https://www.imdb.com/list/ls066256768/?ref_=tt_rls_4&sort=num_votes,desc&st_dt=&mode=detail&page=1'
            self.holidayeaster_link = 'https://www.imdb.com/list/ls062665509/?sort=num_votes,desc&st_dt=&mode=detail&page=1'
            self.holidayindependence_link = 'https://www.imdb.com/list/ls063503978/?sort=num_votes,desc&st_dt=&mode=detail&page=1'
            self.holidayvalentines_link = 'https://www.imdb.com/list/ls050296477/?sort=num_votes,desc&st_dt=&mode=detail&page=1'
            self.holidaypatricks_link = 'https://www.imdb.com/list/ls063934595/?start=1&view=detail&defaults=1&lists=ls063934595&sort=num_votes,desc&st_dt=&mode=detail&page=1'

        self.added_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&languages=en&num_votes=500,&production_status=released&release_date=%s,%s&sort=release_date,desc&count=20&start=1' % (
        self.year_date, self.today_date)
        self.trending_link = 'http://api.trakt.tv/movies/trending?limit=40&page=1'
        self.romance_link  = 'https://www.imdb.com/list/ls026566049/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.marvel_link  = 'https://www.imdb.com/list/ls026566277/?view=detail&sort=alpha,asc&title_type=video,movie,tvMovie&start=1'
        self.dcmovies_link  = 'https://www.imdb.com/list/ls026562887/?view=detail&sort=alpha,asc&title_type=video,movie,tvMovie&start=1'    
        self.dcanimate_link  = 'https://www.imdb.com/list/ls026564052/?view=detail&sort=alpha,asc&title_type=video,movie,tvMovie,&start=1'
        self.tophorr_link  = 'https://www.imdb.com/list/ls027380456/?sort=release_date,desc&st_dt=&mode=detail&page=1'
        self.horror_link  = 'https://www.imdb.com/list/ls026598996/?view=detail&sort=release_date,desc&title_type=video,movie,tvMovie,&start=1'
        self.standup_link  = 'https://www.imdb.com/list/ls026316432/?view=detail&sort=alpha,asc&title_&start=1'
        self.traktlists_link = 'http://api.trakt.tv/users/me/lists'
        self.traktlikedlists_link = 'http://api.trakt.tv/users/likes/lists?limit=1000000'
        self.traktlist_link = 'http://api.trakt.tv/users/%s/lists/%s/items'
        self.traktcollection_link = 'http://api.trakt.tv/users/me/collection/movies'
        self.traktwatchlist_link = 'http://api.trakt.tv/users/me/watchlist/movies'
        self.traktfeatured_link = 'http://api.trakt.tv/recommendations/movies?limit=40'
        self.trakthistory_link = 'http://api.trakt.tv/users/me/history/movies?limit=40&page=1'
        self.imdblists_link = 'http://www.imdb.com/user/ur%s/lists?tab=all&sort=mdfd&order=desc&filter=titles' % self.imdb_user
        self.imdblist_link = 'http://www.imdb.com/list/%s/?view=detail&sort=alpha,asc&title_type=movie,short,tvMovie,tvSpecial,video&start=1'
        self.imdblist2_link = 'http://www.imdb.com/list/%s/?view=detail&sort=date_added,desc&title_type=movie,short,tvMovie,tvSpecial,video&start=1'
        self.imdbwatchlist_link = 'http://www.imdb.com/user/ur%s/watchlist?sort=alpha,asc' % self.imdb_user
        self.imdbwatchlist2_link = 'http://www.imdb.com/user/ur%s/watchlist?sort=date_added,desc' % self.imdb_user



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
                    if url == self.trakthistory_link: raise Exception()
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


            if idx == True and create_directory == True: self.movieDirectory(self.list)
            return self.list
        except:
            pass


    def widget(self):
        setting = control.setting('movie.widget')

        if setting == '2':
            self.get(self.trending_link)
        elif setting == '3':
            self.get(self.popular_link)
        elif setting == '4':
            self.get(self.theaters_link)
        elif setting == '5':
            self.get(self.added_link)
        else:
            self.get(self.featured_link)

    def search(self):

        navigator.navigator().addDirectoryItem(32603, 'movieSearchnew', 'search5.png', 'DefaultMovies.png')
        try:
            from sqlite3 import dbapi2 as database
        except Exception:
            from pysqlite2 import dbapi2 as database

        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()

        try:
            dbcur.executescript("CREATE TABLE IF NOT EXISTS movies (ID Integer PRIMARY KEY AUTOINCREMENT, term);")
        except Exception:
            pass

        dbcur.execute("SELECT * FROM movies ORDER BY ID DESC")
        lst = []

        delete_option = False
        for (id, term) in dbcur.fetchall():
            if term not in str(lst):
                delete_option = True
                navigator.navigator().addDirectoryItem(term, 'movieSearchterm&name=%s' % term, 'search5.png', 'DefaultMovies.png')
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
        except:
            from pysqlite2 import dbapi2 as database

        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()
        dbcur.execute("INSERT INTO movies VALUES (?,?)", (None, q))
        dbcon.commit()
        dbcur.close()
        url = self.search_link + urllib.quote_plus(q)
        self.get(url)

    def search_term(self, name):
        url = self.search_link + urllib.quote_plus(name)
        self.get(url)

    def person(self):
        try:
            t = control.lang(32010).encode('utf-8')
            k = control.keyboard('', t)
            k.doModal()
            q = k.getText() if k.isConfirmed() else None

            if (q is None or q == ''):
                return

            url = self.persons_link + urllib.quote_plus(q)
            self.persons(url)
        except:
            return


    def genres(self):
        genres = [
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Action[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'action', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Adventure[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'adventure', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Animation[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'animation', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Anime[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'anime', False),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Biography[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'biography', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Comedy[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'comedy', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Crime[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'crime', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Documentary[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'documentary', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Drama[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'drama', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Family[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'family', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Fantasy[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'fantasy', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]History[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'history', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Horror[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'horror', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Music[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'music', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Musical[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'musical', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Mystery[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'mystery', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Romance[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'romance', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Science Fiction[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'sci_fi', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Sport[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'sport', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Thriller[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'thriller', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]War[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'war', True),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Western[/COLOR][B][COLOR blue] •[/COLOR][/B]', 'western', True)
        ]

        for i in genres: self.list.append(
            {
                'name': cleangenre.lang(i[0], self.lang),
                'url': self.genre_link % i[1] if i[2] else self.keyword_link % i[1],
                'image': 'genres.png',
                'action': 'movies'
            })

        self.addDirectory(self.list)
        return self.list    


    def languages(self):
        languages = [
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Arabic[/COLOR]', 'ar'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Bosnian[/COLOR]', 'bs'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Bulgarian[/COLOR]', 'bg'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Chinese[/COLOR]', 'zh'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Croatian[/COLOR]', 'hr'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Dutch[/COLOR]', 'nl'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]English[/COLOR]', 'en'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Finnish[/COLOR]', 'fi'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]French[/COLOR]', 'fr'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]German[/COLOR]', 'de'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Greek[/COLOR]', 'el'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Hebrew[/COLOR]', 'he'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Hindi[/COLOR]', 'hi'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Hungarian[/COLOR]', 'hu'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Icelandic[/COLOR]', 'is'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Italian[/COLOR]', 'it'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Japanese[/COLOR]', 'ja'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Korean[/COLOR]', 'ko'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Macedonian[/COLOR]', 'mk'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Norwegian[/COLOR]', 'no'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Persian[/COLOR]', 'fa'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Polish[/COLOR]', 'pl'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Portuguese[/COLOR]', 'pt'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Punjabi[/COLOR]', 'pa'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Romanian[/COLOR]', 'ro'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Russian[/COLOR]', 'ru'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Serbian[/COLOR]', 'sr'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Slovenian[/COLOR]', 'sl'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Spanish[/COLOR]', 'es'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Swedish[/COLOR]', 'sv'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Turkish[/COLOR]', 'tr'),
            ('[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]Ukrainian[/COLOR]', 'uk')
        ]

        for i in languages: self.list.append(
            {'name': str(i[0]), 'url': self.language_link % i[1], 'image': 'languages.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list    


    def certifications(self):
        certificates = ['[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]G[/COLOR]', '[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]PG[/COLOR]', '[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]PG-13[/COLOR]', '[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]R[/COLOR]', '[B][COLOR blue]• [/COLOR][/B][COLOR ghostwhite]NC-17[/COLOR]']

        for i in certificates: self.list.append(
            {'name': str(i), 'url': self.certification_link % str(i).replace('-', '_').lower(),
             'image': 'certificates.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def years(self):
        year = (self.datetime.strftime('%Y'))

        for i in range(int(year) - 0, 1900, -1): self.list.append(
            {'name': str(i), 'url': self.year_link % (str(i), str(i)), 'image': 'years.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def persons(self, url):
        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.personlist_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in range(0, len(self.list)): self.list[i].update({'action': 'movies'})
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
        for i in range(0, len(self.list)): self.list[i].update({'image': 'userlists.png', 'action': 'movies'})
        self.addDirectory(self.list, queue=True)
        return self.list


    def trakt_list(self, url, user):
        try:
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            q.update({'extended': 'full'})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q

            result = trakt.getTraktAsJson(u)

            items = []
            for i in result:
                try:
                    items.append(i['movie'])
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
                title = client.replaceHTMLCodes(title)

                year = item['year']
                year = re.sub('[^0-9]', '', str(year))

                if int(year) > int((self.datetime).strftime('%Y')): raise Exception()

                imdb = item['ids']['imdb']
                if imdb == None or imdb == '': raise Exception()
                imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))

                tmdb = str(item.get('ids', {}).get('tmdb', 0))

                try:
                    premiered = item['released']
                except:
                    premiered = '0'
                try:
                    premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except:
                    premiered = '0'

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

                try:
                    tagline = item['tagline']
                except:
                    tagline = '0'
                if tagline == None: tagline = '0'
                tagline = client.replaceHTMLCodes(tagline)

                self.list.append(
                    {'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'genre': genre,
                     'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'plot': plot,
                     'tagline': tagline, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'poster': '0', 'next': next})
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
                next = client.parseDOM(result, 'div', attrs={'class': 'list-pagination'})[0]
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
                try:
                    year = re.compile('(\d{4})').findall(year)[0]
                except:
                    year = '0'
                year = year.encode('utf-8')

                if int(year) > int((self.datetime).strftime('%Y')): raise Exception()

                imdb = client.parseDOM(item, 'a', ret='href')[0]
                imdb = re.findall('(tt\d*)', imdb)[0]
                imdb = imdb.encode('utf-8')

                try:
                    poster = client.parseDOM(item, 'img', ret='loadlate')[0]
                except:
                    poster = '0'
                if '/nopicture/' in poster: poster = '0'
                poster = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', poster)
                poster = client.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                try:
                    genre = client.parseDOM(item, 'span', attrs={'class': 'genre'})[0]
                except:
                    genre = '0'
                genre = ' / '.join([i.strip() for i in genre.split(',')])
                if genre == '': genre = '0'
                genre = client.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                try:
                    duration = re.findall('(\d+?) min(?:s|)', item)[-1]
                except:
                    duration = '0'
                duration = duration.encode('utf-8')

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

                try:
                    votes = client.parseDOM(item, 'div', ret='title', attrs={'class': '.*?rating-list'})[0]
                except:
                    votes = '0'
                try:
                    votes = re.findall('\((.+?) vote(?:s|)\)', votes)[0]
                except:
                    votes = '0'
                if votes == '': votes = '0'
                votes = client.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')

                try:
                    mpaa = client.parseDOM(item, 'span', attrs={'class': 'certificate'})[0]
                except:
                    mpaa = '0'
                if mpaa == '' or mpaa == 'NOT_RATED': mpaa = '0'
                mpaa = mpaa.replace('_', '-')
                mpaa = client.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')

                try:
                    director = re.findall('Director(?:s|):(.+?)(?:\||</div>)', item)[0]
                except:
                    director = '0'
                director = client.parseDOM(director, 'a')
                director = ' / '.join(director)
                if director == '': director = '0'
                director = client.replaceHTMLCodes(director)
                director = director.encode('utf-8')

                try:
                    cast = re.findall('Stars(?:s|):(.+?)(?:\||</div>)', item)[0]
                except:
                    cast = '0'
                cast = client.replaceHTMLCodes(cast)
                cast = cast.encode('utf-8')
                cast = client.parseDOM(cast, 'a')
                if cast == []: cast = '0'

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
                    {'title': title, 'originaltitle': title, 'year': year, 'genre': genre, 'duration': duration,
                     'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'cast': cast, 'plot': plot,
                     'tagline': '0', 'imdb': imdb, 'tmdb': '0', 'tvdb': '0', 'poster': poster, 'next': next})
            except:
                pass

        return self.list


    def imdb_person_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'div', attrs={'class': '.+?etail'})
        except:
            return

        for item in items:
            try:
                name = client.parseDOM(item, 'img', ret='alt')[0]
		name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = re.findall('(nm\d*)', url, re.I)[0]
                url = self.person_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = client.parseDOM(item, 'img', ret='src')[0]
                # if not ('._SX' in image or '._SY' in image): raise Exception()
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
                url = url.split('/list/', 1)[-1].strip('/')
                url = self.imdblist_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list


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

        self.list = [i for i in self.list if not i['imdb'] == '0']

        self.list = metacache.local(self.list, self.tm_img_link, 'poster3', 'fanart2')

        if self.fanart_tv_user == '':
            for i in self.list: i.update({'clearlogo': '0', 'clearart': '0'})


    def super_info(self, i):
        try:
            if self.list[i]['metacache'] == True: raise Exception()

            imdb = self.list[i]['imdb']

            item = trakt.getMovieSummary(imdb)

            title = item.get('title')
            title = client.replaceHTMLCodes(title)

            originaltitle = title

            year = item.get('year', 0)
            year = re.sub('[^0-9]', '', str(year))

            imdb = item.get('ids', {}).get('imdb', '0')
            imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))

            tmdb = str(item.get('ids', {}).get('tmdb', 0))

            premiered = item.get('released', '0')
            try:
                premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
            except:
                premiered = '0'

            genre = item.get('genres', [])
            genre = [x.title() for x in genre]
            genre = ' / '.join(genre).strip()
            if not genre: genre = '0'

            duration = str(item.get('Runtime', 0))

            rating = item.get('rating', '0')
            if not rating or rating == '0.0': rating = '0'

            votes = item.get('votes', '0')
            try:
                votes = str(format(int(votes), ',d'))
            except:
                pass

            mpaa = item.get('certification', '0')
            if not mpaa: mpaa = '0'

            tagline = item.get('tagline', '0')

            plot = item.get('overview', '0')

            people = trakt.getPeople(imdb, 'movies')

            director = writer = ''
            if 'crew' in people and 'directing' in people['crew']:
                director = ', '.join([director['person']['name'] for director in people['crew']['directing'] if
                                      director['job'].lower() == 'director'])
            if 'crew' in people and 'writing' in people['crew']:
                writer = ', '.join([writer['person']['name'] for writer in people['crew']['writing'] if
                                    writer['job'].lower() in ['writer', 'screenplay', 'author']])

            cast = []
            for person in people.get('cast', []):
                cast.append({'name': person['person']['name'], 'role': person['character']})
            cast = [(person['name'], person['role']) for person in cast]

            try:
                if self.lang == 'en' or self.lang not in item.get('available_translations',
                                                                  [self.lang]): raise Exception()

                trans_item = trakt.getMovieTranslation(imdb, self.lang, full=True)

                title = trans_item.get('title') or title
                tagline = trans_item.get('tagline') or tagline
                plot = trans_item.get('overview') or plot
            except:
                pass

            try:
                artmeta = True
                # if self.fanart_tv_user == '': raise Exception()
                art = client.request(self.fanart_tv_art_link % imdb, headers=self.fanart_tv_headers, timeout='10',
                                     error=True)
                try:
                    art = json.loads(art)
                except:
                    artmeta = False
            except:
                pass

            try:
                poster2 = art['movieposter']
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
                if 'moviebackground' in art:
                    fanart = art['moviebackground']
                else:
                    fanart = art['moviethumb']
                fanart = [x for x in fanart if x.get('lang') == self.lang][::-1] + [x for x in fanart if
                                                                                    x.get('lang') == 'en'][::-1] + [x
                                                                                                                    for
                                                                                                                    x in
                                                                                                                    fanart
                                                                                                                    if
                                                                                                                    x.get(
                                                                                                                        'lang') in [
                                                                                                                        '00',
                                                                                                                        '']][
                                                                                                                   ::-1]
                fanart = fanart[0]['url'].encode('utf-8')
            except:
                fanart = '0'

            try:
                banner = art['moviebanner']
                banner = [x for x in banner if x.get('lang') == self.lang][::-1] + [x for x in banner if
                                                                                    x.get('lang') == 'en'][::-1] + [x
                                                                                                                    for
                                                                                                                    x in
                                                                                                                    banner
                                                                                                                    if
                                                                                                                    x.get(
                                                                                                                        'lang') in [
                                                                                                                        '00',
                                                                                                                        '']][
                                                                                                                   ::-1]
                banner = banner[0]['url'].encode('utf-8')
            except:
                banner = '0'

            try:
                if 'hdmovielogo' in art:
                    clearlogo = art['hdmovielogo']
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
                if 'hdmovieclearart' in art:
                    clearart = art['hdmovieclearart']
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

            try:
                if self.tm_user == '': raise Exception()

                art2 = client.request(self.tm_art_link % imdb, timeout='10', error=True)
                art2 = json.loads(art2)
            except:
                pass

            try:
                poster3 = art2['posters']
                poster3 = [x for x in poster3 if x.get('iso_639_1') == self.lang] + [x for x in poster3 if
                                                                                     x.get('iso_639_1') == 'en'] + [x
                                                                                                                    for
                                                                                                                    x in
                                                                                                                    poster3
                                                                                                                    if
                                                                                                                    x.get(
                                                                                                                        'iso_639_1') not in [
                                                                                                                        self.lang,
                                                                                                                        'en']]
                poster3 = [(x['width'], x['file_path']) for x in poster3]
                poster3 = [(x[0], x[1]) if x[0] < 300 else ('300', x[1]) for x in poster3]
                poster3 = self.tm_img_link % poster3[0]
                poster3 = poster3.encode('utf-8')
            except:
                poster3 = '0'

            try:
                fanart2 = art2['backdrops']
                fanart2 = [x for x in fanart2 if x.get('iso_639_1') == self.lang] + [x for x in fanart2 if
                                                                                     x.get('iso_639_1') == 'en'] + [x
                                                                                                                    for
                                                                                                                    x in
                                                                                                                    fanart2
                                                                                                                    if
                                                                                                                    x.get(
                                                                                                                        'iso_639_1') not in [
                                                                                                                        self.lang,
                                                                                                                        'en']]
                fanart2 = [x for x in fanart2 if x.get('width') == 1920] + [x for x in fanart2 if x.get('width') < 1920]
                fanart2 = [(x['width'], x['file_path']) for x in fanart2]
                fanart2 = [(x[0], x[1]) if x[0] < 1280 else ('1280', x[1]) for x in fanart2]
                fanart2 = self.tm_img_link % fanart2[0]
                fanart2 = fanart2.encode('utf-8')
            except:
                fanart2 = '0'

            item = {'title': title, 'originaltitle': originaltitle, 'year': year, 'imdb': imdb, 'tmdb': tmdb,
                    'poster': '0', 'poster2': poster2, 'poster3': poster3, 'banner': banner, 'fanart': fanart,
                    'fanart2': fanart2, 'clearlogo': clearlogo, 'clearart': clearart, 'premiered': premiered,
                    'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa,
                    'director': director, 'writer': writer, 'cast': cast, 'plot': plot, 'tagline': tagline}
            item = dict((k, v) for k, v in item.iteritems() if not v == '0')
            self.list[i].update(item)

            if artmeta == False: raise Exception()

            meta = {'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'lang': self.lang, 'user': self.user, 'item': item}
            self.meta.append(meta)
        except:
            pass


    def movieDirectory(self, items):
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

        isPlayable = 'true' if not 'plugin' in control.infoLabel('Container.PluginName') else 'false'

        indicators = playcount.getMovieIndicators(
            refresh=True) if action == 'movies' else playcount.getMovieIndicators()

        playbackMenu = control.lang(32063).encode('utf-8') if control.setting('hosts.mode') == '2' else control.lang(
            32064).encode('utf-8')

        watchedMenu = control.lang(32068).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(
            32066).encode('utf-8')

        unwatchedMenu = control.lang(32069).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(
            32067).encode('utf-8')

        queueMenu = control.lang(32065).encode('utf-8')

        traktManagerMenu = control.lang(32070).encode('utf-8')

        nextMenu = control.lang(32053).encode('utf-8')

        addToLibrary = control.lang(32551).encode('utf-8')

        for i in items:
            try:
                label = '%s (%s)' % (i['title'], i['year'])
                imdb, tmdb, title, year = i['imdb'], i['tmdb'], i['originaltitle'], i['year']
                sysname = urllib.quote_plus('%s (%s)' % (title, year))
                systitle = urllib.quote_plus(title)

                meta = dict((k, v) for k, v in i.iteritems() if not v == '0')
                meta.update({'code': imdb, 'imdbnumber': imdb, 'imdb_id': imdb})
                meta.update({'tmdb_id': tmdb})
                meta.update({'mediatype': 'movie'})
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, urllib.quote_plus(label))})
                # meta.update({'trailer': 'plugin://script.extendedinfo/?info=playtrailer&&id=%s' % imdb})
                if not 'duration' in i:
                    meta.update({'duration': '120'})
                elif i['duration'] == '0':
                    meta.update({'duration': '120'})
                try:
                    meta.update({'duration': str(int(meta['duration']) * 60)})
                except:
                    pass
                try:
                    meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except:
                    pass

                poster = [i[x] for x in ['poster3', 'poster', 'poster2'] if i.get(x, '0') != '0']
                poster = poster[0] if poster else addonPoster
                meta.update({'poster': poster})

                sysmeta = urllib.quote_plus(json.dumps(meta))

                url = '%s?action=play1&title=%s&year=%s&imdb=%s&meta=%s&t=%s' % (
                sysaddon, systitle, year, imdb, sysmeta, self.systime)
                sysurl = urllib.quote_plus(url)

                path = '%s?action=play1&title=%s&year=%s&imdb=%s' % (sysaddon, systitle, year, imdb)


                cm = []

                cm.append(('Find similar',
                           'ActivateWindow(10025,%s?action=movies&url=https://api.trakt.tv/movies/%s/related,return)' % (
                               sysaddon, imdb)))

                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                try:
                    overlay = int(playcount.getMovieOverlay(indicators, imdb))
                    if overlay == 7:
                        cm.append(
                            (unwatchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=6)' % (sysaddon, imdb)))
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        cm.append(
                            (watchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=7)' % (sysaddon, imdb)))
                        meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass

                if traktCredentials == True:
                    cm.append((traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&imdb=%s&content=movie)' % (
                    sysaddon, sysname, imdb)))

                cm.append(
                    (playbackMenu, 'RunPlugin(%s?action=alterSources&url=%s&meta=%s)' % (sysaddon, sysurl, sysmeta)))

                if isOld == True:
                    cm.append((control.lang2(19033).encode('utf-8'), 'Action(Info)'))

                cm.append((addToLibrary,
                           'RunPlugin(%s?action=movieToLibrary&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s)' % (
                           sysaddon, sysname, systitle, year, imdb, tmdb)))

                item = control.item(label=label)

                art = {}
                art.update({'icon': poster, 'thumb': poster, 'poster': poster})

                if 'banner' in i and not i['banner'] == '0':
                    art.update({'banner': i['banner']})
                else:
                    art.update({'banner': addonBanner})

                if 'clearlogo' in i and not i['clearlogo'] == '0':
                    art.update({'clearlogo': i['clearlogo']})

                if 'clearart' in i and not i['clearart'] == '0':
                    art.update({'clearart': i['clearart']})


                if settingFanart == 'true' and 'fanart2' in i and not i['fanart2'] == '0':
                    item.setProperty('Fanart_Image', i['fanart2'])
                elif settingFanart == 'true' and 'fanart' in i and not i['fanart'] == '0':
                    item.setProperty('Fanart_Image', i['fanart'])
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.setArt(art)
                item.addContextMenuItems(cm)
                item.setProperty('IsPlayable', isPlayable)
                item.setInfo(type='Video', infoLabels=meta)

                video_streaminfo = {'codec': 'h264'}
                item.addStreamInfo('video', video_streaminfo)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
            except:
                pass

        try:
            url = items[0]['next']
            if url == '': raise Exception()

            icon = control.addonNext()
            url = '%s?action=moviePage&url=%s' % (sysaddon, urllib.quote_plus(url))

            item = control.item(label=nextMenu)

            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon})
            if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)

            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass

        control.content(syshandle, 'movies')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('movies', {'skin.estuary': 55, 'skin.confluence': 500})


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
                           'RunPlugin(%s?action=random&rtype=movie&url=%s)' % (sysaddon, urllib.quote_plus(i['url']))))

                if queue == True:
                    cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                try:
                    cm.append((addToLibrary, 'RunPlugin(%s?action=moviesToLibrary&url=%s)' % (
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
