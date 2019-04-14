# -*- coding: utf-8 -*-

'''
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
from resources.lib.modules import client,cleantitle,source_utils, cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['deepmovie.ch']
        self.base_link = 'https://www.deepmovie.ch'
        self.search_link = '/%s/'
        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.base_link + self.search_link % imdb
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = self.scraper.get(url).content
            try:
                qual = re.compile('class="quality">(.+?)<').findall(r)
                for i in qual:
                    if 'HD' in i:
                        quality = 'HD'
                    else:
                        quality = 'SD'
                match = re.compile('<iframe.+?src="(.+?)"').findall(r)
                for url in match:
                    info = i
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if 'youtube' in host: continue
                    if valid:
                        sources.append({ 'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False })
            except:
                return
        except Exception:
            return
        return sources


    def resolve(self, url):
        return url

