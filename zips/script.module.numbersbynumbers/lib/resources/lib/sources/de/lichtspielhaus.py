# -*- coding: utf-8 -*-

"""
    Flixnet Add-on

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
"""

import re
import urllib
import urlparse
import itertools
import HTMLParser

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['lichtspielhaus.stream']
        self.base_link = 'http://lichtspielhaus.stream'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search([localtitle] + source_utils.aliases_to_array(aliases))
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases))
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = self.__search([localtvshowtitle] + source_utils.aliases_to_array(aliases))
            if not url and tvshowtitle != localtvshowtitle: url = self.__search([tvshowtitle] + source_utils.aliases_to_array(aliases))
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            s = '-%sx%s/' % (season, episode)

            url = url.rstrip('/')
            url = '/episode' + url + s

            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            query = urlparse.urljoin(self.base_link, url)
            r = client.request(query)

            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'TpRwCont'})
            r = dom_parser.parse_dom(r, 'main')

            options1 = dom_parser.parse_dom(r, 'li', attrs={'class': 'STPb'})
            options2 = dom_parser.parse_dom(r, 'div', attrs={'class': 'TPlayerTb'})

            for o1,o2 in itertools.izip(options1,options2):
                if 'trailer' in o1[1].lower():
                    continue
                elif '1080p' in o1[1].lower():
                    quality = '1080p'
                elif '720p' in o1[1].lower():
                    quality = 'HD'
                else:
                    quality = 'SD'

                s = '(?<=src=\")(.*?)(?=\")'
                if re.match(s, o2[1]) is not None:
                    url = re.search(s, o2[1]).group()
                else:
                    h = HTMLParser.HTMLParser()
                    h = h.unescape(o2[1])
                    url = re.search(s, h).group()

                valid, hoster = source_utils.is_host_valid(url, hostDict)
                if not valid: continue

                sources.append({'source': hoster, 'quality': quality, 'language': 'de', 'url': url, 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def __search(self, titles):
        try:
            query = self.search_link % (urllib.quote_plus(cleantitle.query(titles[0])))
            query = urlparse.urljoin(self.base_link, query)

            t = [cleantitle.get(i) for i in set(titles) if i]

            r = client.request(query)

            r = dom_parser.parse_dom(r, 'ul', attrs={'class': 'MovieList'})
            r = dom_parser.parse_dom(r, 'li', attrs={'class': 'TPostMv'})
            r = dom_parser.parse_dom(r, 'a')

            for i in r:
                title = dom_parser.parse_dom(i, 'h2', attrs={'class': 'Title'})
                title = cleantitle.get(title[0][1])
                if title in t:
                    return source_utils.strip_domain(i[0]['href'])
        except:
            return
