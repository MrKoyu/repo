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
from resources.lib.modules import workers


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['iwantmyshow.tk', 'myvideolinks.net']
        self.base_link = 'http://myvideolinks.net'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
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
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except Exception:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            self._sources = []


            if url is None:
                return self._sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s S%02dE%02d' % (
            data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
            data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            check = query.lower() if 'tvshowtitle' in data else data['imdb']


            extra = 'http://myvideolinks.net/dl'

            url = '{extra}/?s={query}'.format(extra=extra, query=urllib.quote_plus(query))
            r = client.request(url, verify=False)
            posts = client.parseDOM(r, 'div', attrs={'class': 'post-meta'})
            if not posts and 'tvshowtitle' in data:
                url = '%s/?s=%s' % (extra,   urllib.quote_plus(cleantitle.geturl(title +' '+ hdlr)))
                r = client.request(url, headers={'User-Agent': client.agent()})
                posts += client.parseDOM(r, 'article')
                url = '%s/?s=%s' % (extra,  urllib.quote_plus(cleantitle.geturl(title)))
                r = client.request(url, headers={'User-Agent': client.agent()})
                posts += client.parseDOM(r, 'article')

            if not posts: return self._sources
            items = []
            for post in posts:
                if not check in post.lower(): continue
                try:
                    t = client.parseDOM(post, 'a', ret='title')[0]
                    u = client.parseDOM(post, 'a', ret='href')[0]
                    s = re.search('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', post)
                    s = s.groups()[0] if s else '0'
                    items += [(t, u, s, post)]
                except Exception:
                    pass
                threads = []
                for url in items: threads.append(
                    workers.Thread(self._get_source, url, hdlr, hostDict, hostprDict))
                [i.start() for i in threads]
                [i.join() for i in threads]


            return self._sources
        except Exception:
            return self._sources

    def _get_source(self, url, hdlr, hostDict, hostprDict):
        try:
            title, url, size, data = url[0], url[1], url[2], url[3]
            r = client.request(url, headers={'User-Agent': client.agent()})
            name = client.parseDOM(r, 'h4')[0]
            if 'S' in hdlr:
                data = client.parseDOM(r, 'div', attrs={'class': 'post-content'})[0]
                frames = client.parseDOM(data, 'a', ret='href')

            else:
                data = client.parseDOM(r, 'div', attrs={'class': 'post-content'})[0]
                data = client.parseDOM(data, 'ul')[0]
                frames = client.parseDOM(data, 'a', ret='href')

            quality, info = source_utils.get_release_quality(name, title)

            size_string = re.search('<strong>Size</strong>:(.+?)<strong>', r)
            if size_string:
                try:
                    size = \
                        re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+) (?:GB|GiB|MB|MiB))', size_string.groups()[0])[0]
                    div = 1 if size.endswith(('GB', 'GiB')) else 1024
                    size = float(re.sub('[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
                    size = '%.2f GB' % size
                    info.append(size)
                except Exception:
                    pass

            info = ' | '.join(info)
            for url in frames:
                url = urllib.quote(url, ':/!@#$%^&*()_+-=?')
                try:
                    if any(x in url for x in ['.rar.', '.zip.', '.iso.']) or any(
                            url.endswith(x) for x in ['.rar', '.zip', '.iso']): raise Exception()
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')
                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if host in hostDict:
                        host = client.replaceHTMLCodes(host)
                        host = host.encode('utf-8')
                        if quality == 'SD': quality, info2 = source_utils.get_release_quality(name, url)
                        self._sources.append(
                            {'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                             'direct': False,
                             'debridonly': False})
                    elif host in hostprDict:
                        host = client.replaceHTMLCodes(host)
                        host = host.encode('utf-8')
                        if quality == 'SD': quality, info2 = source_utils.get_release_quality(name, url)
                        self._sources.append(
                            {'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                             'direct': False,
                             'debridonly': True})
                    else:
                        continue
                except Exception:
                    pass
        except Exception:
            pass

    def resolve(self, url):
        try:
            return url
        except Exception:
            return