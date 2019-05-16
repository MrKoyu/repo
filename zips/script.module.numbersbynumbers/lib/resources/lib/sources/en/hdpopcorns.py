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

import urllib, urlparse, re

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import cfscrape
from resources.lib.modules import dom_parser2

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['hdpopcorns.in']
        self.base_link = 'http://hdpopcorns.co'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None: return sources

            data = urlparse.parse_qs(url)

            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['title']

            hdlr = data['year']

            query = '%s %s' % (data['title'], data['year'])

            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)
            scraper = cfscrape.create_scraper()
            r = scraper.get(url).content
            posts = client.parseDOM(r, 'h2')
            for post in posts:
                try:
                    data = dom_parser2.parse_dom(post, 'a', req='href')[0]
                    t = data.attrs['title']
                    t2 = re.sub('(\.|\(|\[|\s)(\d{4}|S\d+E\d+|S\d+|3D|720p / 1080p|\d{3,}p)(\.|\)|\]|\s|)(.+|)', '', t, re.I)
                    y = re.findall('[\.|\(|\[|\s](S\d*E\d*|Season\s*\d*|\d{4})[\.|\)|\]|\s]', t)[-1]

                    if not (cleantitle.get(t2) == cleantitle.get(title) and y == hdlr): continue

                    link = data.attrs['href']
                    u = self.movie_links(link)

                    for item in u:
                        url = item[0][0]
                        quality, info = source_utils.get_release_quality(url, url)
                        try:
                            size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+) [M|G]B)', item[0][1])[-1]
                            div = 1 if size.endswith(' GB') else 1024
                            size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
                            size = '%.2f GB' % size
                            info.append(size)
                        except BaseException:
                            pass

                        info = ' | '.join(info)

                        url = client.replaceHTMLCodes(url)
                        url = url.encode('utf-8')

                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url,
                                        'info': info, 'direct': True, 'debridonly': False})
                except Exception:
                    pass

            return sources
        except BaseException:
            return sources

    def movie_links(self, link):
        try:
            scraper = cfscrape.create_scraper()
            data = scraper.get(link).content
            data = client.parseDOM(data, 'div', attrs={'class': 'thecontent'})[0]
            FN720p = client.parseDOM(data, 'input', ret='value', attrs={'name': 'FileName720p'})[0]
            FS720p = client.parseDOM(data, 'input', ret='value', attrs={'name': 'FileSize720p'})[0]
            FSID720p = client.parseDOM(data, 'input', ret='value', attrs={'name': 'FSID720p'})[0]
            FN1080p = client.parseDOM(data, 'input', ret='value', attrs={'name': 'FileName1080p'})[0]
            FS1080p = client.parseDOM(data, 'input', ret='value', attrs={'name': 'FileSize1080p'})[0]
            FSID1080p = client.parseDOM(data, 'input', ret='value', attrs={'name': 'FSID1080p'})[0]
            post = {'FileName720p': FN720p, 'FileSize720p': FS720p, 'FSID720p': FSID720p,
                    'FileName1080p': FN1080p, 'FileSize1080p': FS1080p, 'FSID1080p': FSID1080p,
                    'x': 173, 'y': 22}
            POST = client.request('%s/select-movie-quality.php' % self.base_link, post=post)
            #POST = self.scraper.post('http://hdpopcorns.com/select-movie-quality.php', data=post).text
            data = client.parseDOM(POST, 'div', attrs={'id': 'btn_\d+p'})
            u = zip([client.parseDOM(i, 'a', ret='href')[0],
                     re.findall('((?:\d+\.\d+|\d+\,\d+|\d+) (?:GB|GiB|MB|MiB))', i)[0]] for i in data)
            return u
        except Exception:
            pass

    def resolve(self, url):
        return url
