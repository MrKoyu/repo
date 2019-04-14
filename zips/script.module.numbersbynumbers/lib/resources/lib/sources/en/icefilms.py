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

import re, urlparse, random, urllib, time

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import control
from resources.lib.modules import dom_parser2
from resources.lib.modules import log_utils
from resources.lib.modules import cfscrape
from resources.lib.modules import workers


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['icefilms.info']
        self.base_link = 'http://www.icefilms.info'
        self.search_link = urlparse.urljoin(self.base_link, 'search.php?q=%s+%s&x=0&y=0')
        self.list_url = urlparse.urljoin(self.base_link,
                                         'membersonly/components/com_iceplayer/video.php?h=374&w=631&vid=%s&img=')
        self.post = 'url=&iqs=&captcha=+&secret=%s&id=%s&s=%s&m=%s&t=%s'

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

    def search_movie(self, title, year):
        try:
            clean_title = cleantitle.geturl(title)
            search_url = self.search_link % (clean_title.replace('-', '+'), year)
            r = self.scraper.get(search_url).content
            if 'Search results for' not in r:
                for i in range(0, 5):
                    r = self.scraper.get(search_url).content
                    if 'Search results for' in r: break
            r = dom_parser2.parse_dom(r, 'td')
            r = [dom_parser2.parse_dom(i, 'a', req='href') for i in r if "<div class='number'" in i.content]
            r = [(urlparse.urljoin(self.base_link, i[0].attrs['href'])) for i in r if
                 title.lower() in i[0].content.lower() and year in i[0].content]
            url = r[0]
            url = url[:-1]
            url = url.split('?v=')[1]
            url = self.list_url % url
            return url
        except Exception:
            return

    def search_tvshow(self, tvshowtitle, year, season, episode):
        try:
            clean_title = cleantitle.geturl(tvshowtitle)
            search_url = self.search_link % (clean_title.replace('-', '+'), year)
            r = self.scraper.get(search_url).content
            if 'Search results for' not in r:
                for i in range(0, 5):
                    r = self.scraper.get(search_url).content
                    if 'Search results for' in r: break
            r = dom_parser2.parse_dom(r, 'td')
            r = [dom_parser2.parse_dom(i, 'a', req='href') for i in r if "<div class='number'" in i.content]
            r = [(urlparse.urljoin(self.base_link, i[0].attrs['href'])) for i in r if
                 tvshowtitle.lower() in i[0].content.lower() and year in i[0].content]
            url = r[0]

            if not url: return
            sep = '%dx%02d' % (int(season), int(episode))
            r = self.scraper.get(url).content
            if '<span class=list>' not in r:
                for i in range(0, 5):
                    r = self.scraper.get(url).content
                    if '<span class=list>' in r: break
            r = dom_parser2.parse_dom(r, 'span', attrs={'class': 'list'})
            r1 = dom_parser2.parse_dom(r, 'br')
            r1 = [dom_parser2.parse_dom(i, 'a', req='href') for i in r1]
            try:
                if int(season) == 1 and int(episode) == 1:
                    url = dom_parser2.parse_dom(r, 'a', req='href')[1].attrs['href']
                else:
                    for i in r1:
                        if sep in i[0].content:
                            url = urlparse.urljoin(self.base_link, i[0].attrs['href'])
            except Exception:
                pass
            url = url[:-1]
            url = url.split('?v=')[1]
            url = self.list_url % url
            return url
        except BaseException:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            self._sources = []

            if not url: return self._sources

            self.scraper = cfscrape.create_scraper()

            data = urlparse.parse_qs(url)

            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            content = 'show' if 'tvshowtitle' in data else 'movie'
            if content == 'movie':
                url = self.search_movie(data['title'], data['year'])
            else:
                url = self.search_tvshow(data['tvshowtitle'], data['year'], data['season'], data['episode'])

            if not url: return self._sources

            self.hostDict = hostDict
            self.hostprDict = hostprDict

            referer = url

            html = self.scraper.get(url).content
            match = re.search('lastChild\.value="([^"]+)"(?:\s*\+\s*"([^"]+))?', html)

            secret = ''.join(match.groups(''))
            match = re.search('"&t=([^"]+)', html)
            t = match.group(1)
            match = re.search('(?:\s+|,)s\s*=(\d+)', html)
            s_start = int(match.group(1))

            match = re.search('(?:\s+|,)m\s*=(\d+)', html)
            m_start = int(match.group(1))

            threads = []

            for fragment in dom_parser2.parse_dom(html, 'div', {'class': 'ripdiv'}):
                match = re.match('<b>(.*?)</b>', fragment.content)
                if match:
                    q_str = match.group(1).replace(' ', '').upper()
                    if '1080' in q_str:
                        quality = 'FHD'
                    elif '720' in q_str:
                        quality = 'HD'
                    elif '4k' in q_str.lower():
                        quality = 'UHD'
                    else:
                        quality = 'SD'
                else:
                    quality = 'SD'

                pattern = '''onclick='go\((\d+)\)'>([^<]+)(<span.*?)</a>'''
                for match in re.finditer(pattern, fragment.content):
                    link_id, label, host_fragment = match.groups()
                    s = s_start + random.randint(3, 1000)
                    m = m_start + random.randint(21, 1000)
                    post = self.post % (secret, link_id, s, m, t)
                    url = urlparse.urljoin(self.base_link,
                                           'membersonly/components/com_iceplayer/video.php-link.php?s=%s&t=%s' % (
                                           link_id, t))

                    threads.append(workers.Thread(self._get_sources, url, post, host_fragment, quality, referer))

            [i.start() for i in threads]
            [i.join() for i in threads]

            return self._sources
        except BaseException:
            return self._sources

    def _get_sources(self, url, post, host_fragment, quality, referer):
        try:
            url = {'link': url, 'post': post, 'referer': referer}
            url = urllib.urlencode(url)
            valid = True
            host_size = re.sub('(</?[^>]*>)', '', host_fragment)
            host = re.search('([a-zA-Z]+)', host_size)
            host = host.group(1)
            if host.lower() in str(self.hostDict):
                debrid_only = False
            elif host.lower() in str(self.hostprDict):
                debrid_only = True
            else:
                valid = False

            if valid:
                info = []

                try:
                    size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+) (?:GB|GiB|MB|MiB))', host_size)[-1]
                    div = 1 if size.endswith(('GB', 'GiB')) else 1024
                    size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
                    size = '%.2f GB' % size
                    info.append(size)
                except Exception:
                    pass

                info = ' | '.join(info)
                self._sources.append({
                    'source': host,
                    'info': info,
                    'quality': quality,
                    'language': 'en',
                    'url': url,
                    'direct': False,
                    'debridonly': debrid_only
                })
        except BaseException:
            pass

    def resolve(self, url):
        try:
            scraper = cfscrape.create_scraper()
            data_dict = urlparse.parse_qs(url)
            data_dict = dict([(i, data_dict[i][0]) if data_dict[i] else (i, '') for i in data_dict])
            link = data_dict['link']
            post = data_dict['post']
            referer = data_dict['referer']
            for u in range(0, 10):
                disc = scraper.get(referer).content
                if 'WATCH IT NOW' in disc: break
            for i in range(0, 10):
                getheaders = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-GB,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Referer': referer}
                r = scraper.post(link, data=post, headers=getheaders)
                match = re.search('url=(http.*)', r.url)
                if match:
                    return urllib.unquote_plus(match.group(1))
            return
        except Exception:
            return