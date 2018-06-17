# -*- coding: utf-8 -*-

'''
    Numbers By Numbers Add-on

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


import re,traceback,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['filmfrantic.com']
        self.base_link = 'http://filmfrantic.com'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url  % (title.replace(':', ' ').replace(' ', '+'))

            search_results = client.request(url)
            match = re.compile('<article id=.+?href="(.+?)" title="(.+?)"',re.DOTALL).findall(search_results)
            for row_url, row_title in match:
                if cleantitle.get(title) in cleantitle.get(row_title):
                    if year in str(row_title):
                        return row_url
            return
        except:
            failure = traceback.format_exc()
            log_utils.log('FilmFrantic - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None: return sources
            html = client.request(url)

            links = re.compile(' <iframe src="(.+?)"',re.DOTALL).findall(html)

            for link in links:
                if '1080' in link:
                    quality = '1080p'
                elif '720' in link:
                    quality = '720p'
                else:
                    quality = 'SD'
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})
            return sources
        except:
            failure = traceback.format_exc()
            log_utils.log('FilmFrantic - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
