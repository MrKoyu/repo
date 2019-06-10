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
import traceback
import urlparse

from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import log_utils
from resources.lib.modules import proxy


class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['xwatchseries.to', 'onwatchseries.to', 'itswatchseries.to']
        self.base_link = 'https://www1.swatchseries.to'
        self.search_link = 'https://www1.swatchseries.to/search/%s'
        self.scraper = cfscrape.create_scraper()

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            q = cleantitle.query(tvshowtitle)
            r = self.scraper.get(self.search_link % q, headers={'referer': self.base_link}).content
            r = client.parseDOM(r, 'div', attrs={'valign': '.+?'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), client.parseDOM(i, 'a'))
                 for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if i[0] and i[1] and i[2]]
            return r[0][0]
        except:
            traceback.print_exc()
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return

            r = self.scraper.get(url, headers={'referer': self.base_link}).content

            r = client.parseDOM(r, 'li', attrs={'itemprop': 'episode'})

            t = cleantitle.get(title)

            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'span', attrs={'itemprop': 'name'}),
                  re.compile('(\d{4}-\d{2}-\d{2})').findall(i)) for i in r]
            r = [(i[0], i[1][0].split('&nbsp;')[-1], i[2])
                 for i in r if i[1]] + [(i[0], None, i[2]) for i in r if not i[1]]
            r = [(i[0], i[1], i[2][0]) for i in r if i[2]] + [(i[0], i[1], None) for i in r if not i[2]]
            r = [(i[0][0], i[1], i[2]) for i in r if i[0]]

            url = [i for i in r if t == cleantitle.get(i[1]) and premiered == i[2]][:1]
            if not url:
                url = [i for i in r if t == cleantitle.get(i[1])]
            if len(url) > 1 or not url:
                url = [i for i in r if premiered == i[2]]
            if len(url) > 1 or not url:
                raise Exception()

            return url[0][0]
        except:
            failure = traceback.format_exc()
            log_utils.log('XWatchSeries - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None:
                return sources

            r = self.scraper.get(url, headers={'referer': self.base_link}).content
            links = client.parseDOM(r, 'a', ret='href', attrs={'target': '.+?'})
            links = [x for y, x in enumerate(links) if x not in links[:y]]

            for i in links:
                try:
                    url = i
                    url = proxy.parse(url)
                    url = urlparse.parse_qs(urlparse.urlparse(url).query)['r'][0]
                    url = url.decode('base64')
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if host not in hostDict:
                        continue;
                    host = host.encode('utf-8')
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False,
                                    'debridonly': False})
                except:
                    pass

            return sources
        except:
            failure = traceback.format_exc()
            log_utils.log('XWatchSeries - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
