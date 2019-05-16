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
import urllib
import urlparse

from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domain = 'sceneddl.online'
        self.base_link = 'http://www.sceneddl.online'
        self.search_link = '/?s=%s'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        url = {'imdb': imdb, 'title': title, 'year': year}
        url = urllib.urlencode(url)
        return url

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
        url = urllib.urlencode(url)
        return url

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        url = urlparse.parse_qs(url)
        url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
        url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
        url = urllib.urlencode(url)
        return url

    def sources(self, url, hostDict, hostprDict):
        try:
            hostDict = hostDict + hostprDict

            sources = []
            query_bases = []
            options = []

            if url is None:
                return sources

            if not debrid.status():
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = (data['tvshowtitle'] if 'tvshowtitle' in data else data['title'])
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            # tvshowtitle
            if 'tvshowtitle' in data:
                query_bases.append('%s ' % (data['tvshowtitle'].replace("-", "")))
                if 'year' in data:
                    query_bases.append('%s %s ' % (data['tvshowtitle'], data['year']))
                options.append('S%02dE%02d' % (int(data['season']), int(data['episode'])))
                options.append('S%02d' % (int(data['season'])))
            else:
                query_bases.append('%s %s ' % (data['title'], data['year']))
                query_bases.append('%s ' % (data['title']))
                query_bases.append('2160p')
                query_bases.append('')

            for option in options:
                for query_base in query_bases:
                    q = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query_base + option)
                    q = q.replace("  ", " ").replace(" ", "+")
                    url = self.base_link + self.search_link % q
                    html = self.scraper.get(url)
                    if html.status_code == 200:
                        posts = client.parseDOM(html.content, "div", attrs={"class": "title"})
                        for post in posts:
                            url = client.parseDOM(post, "a", ret='href')
                            if len(url) > 0:
                                html = self.scraper.get(url[0])
                                if html.status_code == 200:
                                    quotes = client.parseDOM(html.content, "div", attrs={"class": "dlinks"})
                                    for quote in quotes:
                                        hrefs = client.parseDOM(quote, "a", ret='href')
                                        if not hrefs:
                                            continue
                                        for href in hrefs:
                                            quality = source_utils.check_sd_url(href)
                                            href = href.encode('utf-8')
                                            valid, host = source_utils.is_host_valid(href, hostDict)
                                            if any(x in href for x in ['.rar', '.zip', '.iso']):
                                                continue
                                            if not valid:
                                                continue
                                            if hdlr in href.upper() and cleantitle.get(title) in cleantitle.get(href):
                                                sources.append(
                                                    {'source': host, 'quality': quality, 'language': 'en', 'url': href,
                                                     'direct': False, 'debridonly': False})
                if len(sources) > 0:
                    return sources
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
