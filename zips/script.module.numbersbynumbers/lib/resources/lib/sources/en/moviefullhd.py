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

import re,urllib,urlparse, json
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser2
from resources.lib.modules import unjuice

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['moviefull-hd.com']
        self.base_link = 'https://moviefull-hd.org'
        self.search_link = '/search/%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except Exception:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except Exception:
            return
            
    def search(self, title, hdlr):
        try:

            title = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', title)
            query = urllib.quote_plus(title+' '+hdlr)
            url = urlparse.urljoin(self.base_link, self.search_link % query)
            #post = 'action=ajaxsearchpro_search&aspp=' + query + '&asid=1&asp_inst_id=1_1&options=current_page_id%3D21872%26qtranslate_lang%3D0%26asp_gen%255B%255D%3Dtitle%26customset%255B%255D%3Dmovie%26customset%255B%255D%3Dtvseries%26customset%255B%255D%3Dpost'
            r = client.request(url)
            r = dom_parser2.parse_dom(r, 'a', attrs={'class': 'suf-mosaic-post'}, req='href')
            r = [(i.attrs['href'], i.attrs['title']) for i in r]
            r = [(i[0]) for i in r if cleantitle.get(title) in cleantitle.get(i[1])]
            return r
        except Exception: return
        
    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return sources
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['title']
            hdlr = data['year']

            url = self.search(title, hdlr)
            if url is None: return sources

            for i in url:
                try:
                    info = []
                    if '3d' in i.lower(): info.append('3D')
                    info = ' | '.join(info)
                    r = client.request(i, redirect=False)
                    frame = client.parseDOM(r, 'iframe', ret='src')[0]
                    r = client.request(frame)

                    links = json.loads(re.findall('''sources:\s*(\[.+?\])''', r)[0])

                    for url in links:
                        quality, info2 = source_utils.get_release_quality(url['label'], url['label'])
                        header = '|User-Agent=%s&Referer=%s' % (urllib.quote(client.agent()), frame)
                        sources.append(
                            {'source': 'CDN', 'quality': quality, 'language': 'en', 'url': url['file'] + header,
                             'info': info, 'direct': True, 'debridonly': False})
                except Exception:
                    pass

            return sources
        except Exception:
            return sources
            
    def resolve(self, url):
        return url