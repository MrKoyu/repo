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

import re,urllib,urlparse,os

from resources.lib.modules import cleantitle
from resources.lib.modules import dom_parser2
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['tvdownload.net']
        self.base_link = 'http://tvdownload.net/'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            query = cleantitle.geturl(title).replace('-','+') + '+' + year
            url2 = urlparse.urljoin(self.base_link, self.search_link % query)
            url = {'imdb': imdb, 'title': title, 'year': year, 'url': url2, 'content': 'movie'}
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
            if url is None: return
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            tvshowtitle = data['tvshowtitle']
            year = data['year']

            query = '%s+s%02de%02d' % (cleantitle.geturl(tvshowtitle).replace('-','+'), int(season),int(episode))
            url2 = urlparse.urljoin(self.base_link, self.search_link % (query))
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url = {'imdb': imdb, 'title': title, 'year': year, 'url': url2, 'content': 'episdoe', 'tvshowtitle': tvshowtitle, 'season': season, 'episode': episode, 'premiered': premiered}
            url = urllib.urlencode(url)
            return url
        except Exception:
            return

    def sources(self, url, hostDict, hostprDict):

        sources = []

        try:
            if url is None: return sources

            if debrid.status() is False: raise Exception()

            hostDict = hostprDict + hostDict

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            ref_url = url = data['url']

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            hdlr2 = 'season-%01d-episode-%01d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else ''
            imdb = data['imdb']

            content = 'episode' if 'tvshowtitle' in data else 'movie'
            season = data['season'] if 'season' in data else '0'
            episode = data['episode'] if 'episode' in data else '0'
            premiered = data['premiered'] if 'premiered' in data else '0'
            _headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}
            r = client.request(url, headers=_headers)
            posts = dom_parser2.parse_dom(r, 'article', {'class': ['post','excerpt']})
            posts = [(dom_parser2.parse_dom(i, 'a', req=['href','title']), i.content) for i in posts if imdb in i.content or title.lower() in i.content.lower() and hdlr.lower() in i.content.lower()]
            posts = [(i[0][0].attrs['title'], i[0][0].attrs['href'], i[1]) for i in posts]
            items = []

            for item in posts:
                data = []
                try:
                    name = item[0]
                    name = client.replaceHTMLCodes(name)

                    if content == 'episode':
                        if not hdlr2.lower() in item[1].lower():
                            if not premiered.replace('-','').replace('+','') in item[1].lower().replace('-','').replace('+',''): raise Exception()

                    url = item[1]
                    r = client.request(url, headers=_headers)
                    data += client.parseDOM(r, 'div', attrs={'id': 'content'})
                    data += client.parseDOM(r, 'div', attrs={'id': 'comments'})
                    urls = dom_parser2.parse_dom(data, 'a', req='href')
                    urls = [i.attrs['href'] for i in urls]
                    for url in urls:
                        try:
                            if any(x in url for x in ['.rar.', '.zip.', '.iso.']) or any(
                                url.endswith(x) for x in ['.rar', '.zip', '.iso']): raise Exception()
                            url = client.replaceHTMLCodes(url)
                            url = url.encode('utf-8')

                            valid, host = source_utils.is_host_valid(url, hostDict)
                            if not valid: continue
                            host = client.replaceHTMLCodes(host)
                            host = host.encode('utf-8')

                            quality, info = source_utils.get_release_quality(url)

                            try:
                                size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+) (?:GB|GiB|MB|MiB))', item[2])[-1]
                                div = 1 if size.endswith(('GB', 'GiB')) else 1024
                                size = float(re.sub('[^0-9|/.|/,]', '', size))/div
                                size = '%.2f GB' % size
                                info.append(size)
                            except Exception:
                                pass

                            info = ' | '.join(info)

                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
                        except Exception: pass
                except Exception: pass
            return sources
        except Exception:
             return sources

    def resolve(self, url):
        return url
