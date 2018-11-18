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

import re
import urllib
import urlparse
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils 
from resources.lib.modules import cfscrape

class source:
    def __init__(self):
        self.priority = 1                           
        self.language = ['en']                      
        self.domains = ['filepursuit.com']           
        self.base_link = 'https://filepursuit.com'  
        self.search_link = '/zearch/%s/' 
		self.scraper = cfscrape.create_scraper()
 
    def movie(self, imdb, title, localtitle, aliases, year):
       
        
       
        try:
           
            title = cleantitle.geturl(title)
            
            url = '%s+%s' % (title,year)
           
           
            return url
        except:
            return
           
    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        
        try:
           
           
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return
 
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url: return
           
           
            tvshowtitle = url
           
           
           
            season = '%02d' % int(season)
            episode = '%02d' % int(episode)
           
            
           
            url = '%s+s%se%s' % (tvshowtitle,str(season),str(episode))
           
           
            return url
        except:
            return
 
 
    def sources(self, url, hostDict, hostprDict):
       
      
       
        try:
            sources = []
            scraper = cfscrape.create_scraper()
           
            query = url
 
           
 
            url = self.base_link + self.search_link % query
 
 
            r = scraper.get(url).content
 
 
            try:
               
 
                match = re.compile('data-clipboard-text="(.+?)"').findall(r)
               
               
                for url in match:
               
               
                    if '2160' in url: quality = '4K'
                    elif '4k' in url: quality = '4K'
                    elif '1080' in url: quality = '1080p'
                    elif '720' in url: quality = 'HD'
                    elif '480' in url: quality = 'SD' 
                    else: quality = 'SD'
                   
                   
                    sources.append({
                        'source': 'Direct', 
                        'quality': quality, 
                        'language': 'en',   
                        'url': url,         
                        'direct': False,   
                        'debridonly': False 
                    })
            except:
                return
        except Exception:
            return
           
    
           
        return sources
 
    def resolve(self, url):
        return url