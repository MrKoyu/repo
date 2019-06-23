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

import re, requests

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['movieminions.net']
        self.base_link = 'https://movieminions.net/english-movies/movies'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_query(title)
            title = '%s.%s' % (title, year)
            self.title = title.replace('-', '.')
            year = '-%s/' % year
            url = self.base_link + year
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            result = url
            try:
                r = requests.get(result, timeout=10).content
                r = client.parseDOM(r, "table", attrs={"id": "list"})
                for r in r:
                    r = re.compile('a title=".+?" data-xyz="(.+?)"').findall(r)
                    for url in r:
                        if not self.title in url: continue
                        url = 'http://' + url
                        quality = source_utils.check_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
            except:
                return
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
