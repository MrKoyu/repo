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

import re, urllib, urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.shaanig.se']
        self.base_link = 'https://www.shaanig.se/'
        self.search_link = '?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except BaseException:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except BaseException:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except BaseException:
            return

    def sources(self, url, hostDict, hostprDict):

        try:
            sources = []

            if url is None: return sources
            scraper = cfscrape.create_scraper()
            headers = {'User-Agent': client.agent(),
                       "Referer": self.base_link}
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            year = data['year']
            query = '%s' % data['tvshowtitle'] if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)
            r = scraper.get(url, headers=headers).content

            posts = client.parseDOM(r, 'div', attrs={'class':'ml-item'})

            items = []
            for post in posts:
                try:
                    t = client.parseDOM(post, 'a', ret='oldtitle')[0]
                    u = client.parseDOM(post, 'a', ret='href')[0]
                    try:
                        y = re.findall('[\.|\(|\[|\s](\d{4})[\.|\)|\]|\s]', t, re.I)[-1].upper()
                    except BaseException:
                        y = client.parseDOM(post, 'a', attrs={'rel':'tag'})[0]
                    items += [(t, u, y)]
                except BaseException:
                    pass
            urls = []
            for item in items:
                try:
                    link = item[1] if item[1].startswith('http') else 'https:%s' % item[1]
                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d+E\d+|S\d+|3D)(\.|\)|\]|\s|)(.+|)', '', item[0], flags=re.I)
                    if not cleantitle.get(t) == cleantitle.get(title): raise Exception()
                    if not item[2] == year: raise Exception()
                    if 'series' in link:
                        r = client.request(link)
                        sep = 'season-%d-episode-%d' % (int(data['season']), int(data['episode']))
                        url = client.parseDOM(r, 'a', ret='href')
                        url = [i for i in url if sep in i][0]
                    else: url = link

                    r = scraper.get(url, headers=headers).content
                    data = client.parseDOM(r, 'div', attrs={'id':'list-dl'})
                    urls = client.parseDOM(r, 'source', ret='src')
                    urls += client.parseDOM(data, 'a', ret='href')

                except BaseException:
                    pass
            for item in urls:
                try:
                    if 'ouo.io' in item:
                        url = item.split('?s=')[1]
                    elif 'linkshrink' in item:
                        url = item.split('=')[1]
                    else:
                        url = item
                    if 'openload' in url: raise Exception()
                    url = 'https:%s' % url if not url.startswith('http') else url
                    quality, info = source_utils.get_release_quality(url, url)
                    info = ' | '.join(info)
                    url = urllib.quote(url, '?:/.-_')
                    sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                                    'direct': False, 'debridonly': False})
                except BaseException:
                    pass

            return sources
        except BaseException:
            return sources

    def resolve(self, url):
        return url