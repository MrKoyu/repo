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


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['putlockerr.is','putlockers.movie'] 
        self.base_link = 'https://www5.putlockerr.is'
        self.search_link = '/embed/%s/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.base_link + self.search_link % imdb
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = client.request(url)
            try:
                match = re.compile('<iframe src="(.+?)://(.+?)/(.+?)"').findall(r)
                for http,host,url in match: 
                    url = '%s://%s/%s' % (http,host,url)
                    sources.append({'source': host,'quality': 'HD','language': 'en','url': url,'direct': False,'debridonly': False})
            except:
                return
        except Exception:
            return
        return sources

    def resolve(self, url):
        return url