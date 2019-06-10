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
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import debrid
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser2

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['ultrahdindir.com']
        self.base_link = 'http://ultrahdindir.com'
        self.post_link = '/index.php?do=search'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except BaseException:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return sources

            if debrid.status() is False:
                raise Exception()

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            # query = '%s %s' % (data['title'], data['year'])
            # query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            #
            # url = urlparse.urljoin(self.base_link, self.post_link)
            #
            # post = 'do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=%s' % urllib.quote_plus(query)
            post = {'query': data['imdb']}
            url = urlparse.urljoin(self.base_link, 'engine/ajax/search.php')
            r = client.request(url, post=post)
            urls = client.parseDOM(r, 'a', ret='href')
            urls = [i for i in urls if not data['imdb'] in i]

            hostDict = hostprDict + hostDict
            links = []
            for u in urls:
                try:
                    data = client.request(u)
                    data = re.findall('</iframe>(.+?)QuoteEEnd--><br /><br', data, re.DOTALL)[0]
                    links += re.findall('''start--><b>(.+?)</b>.+?<b><a href=['"](.+?)['"]''', data, re.DOTALL)

                except BaseException:
                    pass
            links = [(i[0], i[1]) for i in links if not 'vip' in i[0].lower()]
            for name, url in links:
                    try:
                        name = re.sub('<.+?>', '', name)
                        if '4K' in name:
                            quality = '4K'

                        elif '1080p' in name:
                            quality = '1080p'
                        elif '720p' in name:
                            quality = '720p'
                        else:
                            quality = 'SD'

                        info = []
                        if '3D' in name or '.3D.' in url:
                            info.append('3D')
                            quality = '1080p'
                        if any(i in ['hevc', 'h265', 'x265'] for i in name): info.append('HEVC')

                        info = ' | '.join(info)

                        url = client.replaceHTMLCodes(url)
                        url = url.encode('utf-8')
                        if any(x in url for x in ['.rar', '.zip', '.iso', 'turk']): raise Exception()

                        if 'ftp' in url:
                            host = 'CDN'
                            direct = True
                        else:
                            valid, host = source_utils.is_host_valid(url, hostDict)
                            if not valid: raise Exception()
                            host = host
                            direct = False

                        host = client.replaceHTMLCodes(host)
                        host = host.encode('utf-8')

                        sources.append({'source': host, 'quality': quality, 'language': 'en',
                                        'url': url, 'info': info, 'direct': direct, 'debridonly': True})
                    except BaseException:
                        pass

            return sources
        except BaseException:
            return sources


    def resolve(self, url):
        return url


