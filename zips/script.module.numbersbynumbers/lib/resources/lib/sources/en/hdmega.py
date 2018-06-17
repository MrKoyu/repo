# -*- coding: utf-8 -*-

'''
    Numbers By Numbers Add-on

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

import re,traceback,urlparse,urllib,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['hdmega.net/']
        self.base_link = 'http://hdmega.net/'
        self.search_link = '/search-movies/%s.html'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(title)
            search_url = urlparse.urljoin(self.base_link, self.search_link % clean_title.replace('-', '+'))

            results = client.request(search_url)
            results = client.parseDOM(results, 'div', {'id': 'movie-featured'})
            results = [(client.parseDOM(i, 'a', ret='href'),
                  re.findall('.+?elease:\s*(\d{4})</', i),
                  re.findall('<b><i>(.+?)</i>', i)) for i in results]
            results = [(i[0][0], i[1][0], i[2][0]) for i in results if
                 (cleantitle.get(i[2][0]) == cleantitle.get(title) and i[1][0] == year)]
            url = results[0][0]

            return url
        except:
            failure = traceback.format_exc()
            log_utils.log('HDMega - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            failure = traceback.format_exc()
            log_utils.log('HDMega - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['premiered'], url['season'], url['episode'] = premiered, season, episode
            try:
                clean_title = cleantitle.geturl(url['tvshowtitle'])+'-season-%d' % int(season)
                search_url = urlparse.urljoin(self.base_link, self.search_link % clean_title.replace('-', '+'))
                search_results = client.request(search_url)
                parsed = client.parseDOM(search_results, 'div', {'id': 'movie-featured'})
                parsed = [(client.parseDOM(i, 'a', ret='href'), re.findall('<b><i>(.+?)</i>', i)) for i in parsed]
                parsed = [(i[0][0], i[1][0]) for i in parsed if cleantitle.get(i[1][0]) == cleantitle.get(clean_title)]
                url = parsed[0][0]
            except:
                pass
            data = client.request(url)
            data = client.parseDOM(data, 'div', attrs={'id': 'details'})
            data = zip(client.parseDOM(data, 'a'), client.parseDOM(data, 'a', ret='href'))
            url = [(i[0], i[1]) for i in data if i[0] == str(int(episode))]

            return url[0][1]
        except:
            failure = traceback.format_exc()
            log_utils.log('HDMega - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None: return sources

            html = client.request(url)
            try:
                v = re.findall('document.write\(Base64.decode\("(.+?)"\)', html)[0]
                b64 = base64.b64decode(v)
                url = client.parseDOM(b64, 'iframe', ret='src')[0]
                try:
                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url.replace('\/', '/'), 'direct': False, 'debridonly': False})
                except:
                    pass
            except:
                pass
            parsed = client.parseDOM(html, 'div', {'class': 'server_line'})
            parsed = [(client.parseDOM(i, 'a', ret='href')[0], client.parseDOM(i, 'p', attrs={'class': 'server_servername'})[0]) for i in parsed]
            if parsed:
                for i in parsed:
                    try:
                        host = re.sub('Server|Link\s*\d+', '', i[1]).lower()
                        url = i[0]
                        host = client.replaceHTMLCodes(host)
                        host = host.encode('utf-8')
                        if 'other'in host: continue
                        sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url.replace('\/', '/'), 'direct': False, 'debridonly': False})
                    except:
                        pass
            return sources
        except:
            failure = traceback.format_exc()
            log_utils.log('HDMega - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        if self.base_link in url:
            url = client.request(url)
            v = re.findall('document.write\(Base64.decode\("(.+?)"\)', url)[0]
            b64 = base64.b64decode(v)
            url = client.parseDOM(b64, 'iframe', ret='src')[0]
        return url
