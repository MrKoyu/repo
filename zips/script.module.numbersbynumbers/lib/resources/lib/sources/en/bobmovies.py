# -*- coding: UTF-8 -*-

'''
    Numbers Add-on

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

import re,traceback,urllib,urlparse,base64
import requests

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['bobmovies.online']
        self.base_link = 'https://bobmovies.online/'
        self.goog = 'https://www.google.com/search?q=bobmovies.online+'
        

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            scrape = cleantitle.get_simple(title)
            google = '%s%s'%(self.goog,scrape.replace(' ','+'))
            get_page = requests.get(google).content
            log_utils.log('Scraper bobmovies - Movie - title: ' + str(title))
            log_utils.log('Scraper bobmovies - Movie - search_id: ' + str(scrape))

            match = re.compile('<a href="(.+?)"',re.DOTALL).findall(get_page)
            for url1 in match:
                if '/url?q=' in url1:
                    if self.base_link in url1 and 'google' not in url1:
                        url2 = url1.split('/url?q=')[1]
                        url2 = url2.split('&amp')[0]
                        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
                        html = requests.get(url2,headers=headers,timeout=5).content
                        results = re.compile('<div class="page_film_top full_film_top">.+?<h1>(.+?)</h1>.+?<td class="name">Quality:</td><td><a href=.+?">(.+?)</a>.+?<td class="name">Year:</td><td><a href=.+?">(.+?)</a>',re.DOTALL).findall(html)
                        for item_title, qual, date  in results:
                            if not scrape == cleantitle.get_simple(item_title):
                                continue
                            if not year in date: 
                                continue
                            log_utils.log('Scraper bobmovies - Movie - url2: ' + str(url2))
                            return url2    
            return
        except:
            failure = traceback.format_exc()
            log_utils.log('BobMovies - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            if url == None: return
            sources = []

            headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
            html = client.request(url,headers=headers)

            vidpage = re.compile('id="tab-movie".+?data-file="(.+?)"',re.DOTALL).findall(html)
        
            for link in vidpage:
                if 'trailer' not in link.lower():
                    link = urlparse.urljoin(self.base_link, link)
                    sources.append({'source':'DirectLink','quality':'SD','language': 'en','url':link,'info':[],'direct':True,'debridonly':False})
            other_links = re.findall('data-url="(.+?)"',html)
            for link in other_links:
                if link.startswith('//'):
                    link = 'http:'+link
                    sources.append({'source':'DirectLink','quality':'SD','language': 'en','url':link,'info':[],'direct':False,'debridonly':False})
                else:
                    sources.append({'source':'DirectLink','quality':'SD','language': 'en','url':link,'info':[],'direct':False,'debridonly':False})


            return sources
        except:
            failure = traceback.format_exc()
            log_utils.log('BobMovies - Exception: \n' + str(failure))
            return

    def resolve(self, url):
        return url