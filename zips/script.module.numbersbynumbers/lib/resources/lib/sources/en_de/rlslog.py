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
import requests

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import dom_parser2


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['rlslog.me']
        self.base_link = 'http://rlslog.me/'
        self.search_link = '?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(title).replace('-', '+').replace(': ', '+')
            url = urlparse.urljoin(self.base_link, self.search_link % clean_title).lower()
            url = {'url': url, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except Exception:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None:
                return sources

            if debrid.status() is False:
                raise Exception()

            data = urlparse.parse_qs(url)

            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s s%02de%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) if\
                'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query_alt = '%s %s s%02de%02d' % (data['tvshowtitle'], data['year'], int(data['season']), int(data['episode'])) if\
                'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])

            url = self.search_link % urllib.quote_plus(query).lower()
            url = urlparse.urljoin(self.base_link, url)
            url_alt = self.search_link % urllib.quote_plus(query_alt).lower()
            url_alt = urlparse.urljoin(self.base_link, url_alt)

            r = requests.get(url).content

            items = dom_parser2.parse_dom(r, 'h3')
            if items is None and 'tvshowtitle' in data:
                r = requests.get(url).content
                items = dom_parser2.parse_dom(r, 'h3')
                if items is None: return sources

            items = [dom_parser2.parse_dom(i.content, 'a', req=['href']) for i in items]
            items = [(i[0].content, i[0].attrs['href']) for i in items]

            hostDict = hostprDict + hostDict

            for item in items:
                try:
                    name = item[0]
                    name = client.replaceHTMLCodes(name)
                    url = item[1]
                    
                    r = requests.get(url).content
                    links = dom_parser2.parse_dom(r, 'a', req=['href'])
                    links = [i.attrs['href'] for i in links]
                    for url in links:
                        try:
                            if hdlr in url:
                                fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*)(\.|\)|\]|\s)', '', name.upper())
                                fmt = re.split('\.|\(|\)|\[|\]|\s|\-', fmt)
                                fmt = [i.lower() for i in fmt]

                                if any(i.endswith(('subs', 'sub', 'dubbed', 'dub')) for i in fmt): raise Exception()
                                if any(i in ['extras'] for i in fmt): raise Exception()

                                if '2160p' in fmt: quality = '4K'
                                elif '1080p' in fmt: quality = '1080p'
                                elif '720p' in fmt: quality = '720p'
                                else: quality = 'SD'
                                if any(i in ['dvdscr', 'r5', 'r6'] for i in fmt): quality = 'SCR'
                                elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in fmt): quality = 'CAM'

                                info = []

                                if '3d' in fmt:
                                    info.append('3D')

                                try:
                                    size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+) (?:GB|GiB|MB|MiB))', name[2])[-1]
                                    div = 1 if size.endswith(('GB', 'GiB')) else 1024
                                    size = float(re.sub('[^0-9|/.|/,]', '', size))/div
                                    size = '%.2f GB' % size
                                    info.append(size)
                                except Exception:
                                    pass

                                if any(i in ['hevc', 'h265', 'x265'] for i in fmt): info.append('HEVC')

                                info = ' | '.join(info)

                                if not any(x in url for x in ['.rar', '.zip', '.iso']):
                                    url = client.replaceHTMLCodes(url)
                                    url = url.encode('utf-8')

                                    host = re.findall('([\w]+[.][\w]+)$',
                                                      urlparse.urlparse(url.strip().lower()).netloc)[0]
                                    if host in hostDict:
                                        host = client.replaceHTMLCodes(host)
                                        host = host.encode('utf-8')

                                        sources.append(
                                            {'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
                        except Exception:
                            pass
                except Exception:
                    pass
            check = [i for i in sources if not i['quality'] == 'CAM']
            if check:
                sources = check

            return sources
        except Exception:
            return

    def resolve(self, url):
        return url
