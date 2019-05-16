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

import re, urllib, urlparse, json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser2 as dom


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['moviescouch.co']
        self.base_link = 'https://moviescouch.co'
        self.post_link = '/wp-admin/admin-ajax.php'

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
            if url is None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title, year = data['title'], data['year']
            post = 'action=ajaxsearchlite_search&aslp={0}&asid=1&' \
                   'options=qtranslate_lang%3D0%26set_exactonly' \
                   '%3Dchecked%26set_intitle%3DNone%26set_inpages%3DNone%26customset%255B%255D%3' \
                   'Damy_movie%26customset%255B%255D%3Dvc4_templates%26customset%255B%255D%3Dvc_grid_item%26' \
                   'customset%255B%255D%3Damn_mi-lite'.format(urllib.quote_plus(cleantitle.getsearch(title)))

            post_link = urlparse.urljoin(self.base_link, self.post_link)
            data = client.request(post_link, post=post, referer=self.base_link)
            items = dom.parse_dom(data, 'a', req='href')
            item = [(i.attrs['href']) for i in items
                    if cleantitle.get(title) == cleantitle.get(i.content.split(year)[0].lstrip())][0]
            r = client.request(item)
            quality = re.findall('Quality:(.+?)</p>', r, re.DOTALL)[0]
            FN = client.parseDOM(r, 'input', ret='value', attrs={'name': 'filename'})[0]
            FS = client.parseDOM(r, 'input', ret='value', attrs={'name': 'fileservername'})[0]
            FSize = client.parseDOM(r, 'input', ret='value', attrs={'name': 'filesize'})[0]
            post = 'filename={0}&filesize={1}&fileservername={2}&filepath=downloads'.format(urllib.quote_plus(FN),
                                                                                            urllib.quote_plus(FSize),
                                                                                            FS)
            plink2 = 'https://moviescouch.co/download.php'
            headers = {'Referer': 'https://moviescouch.co/downloading/'}
            pdata = client.request(plink2, post=post, redirect=False, headers=headers, output='extended')
            link = pdata[2]['Location']
            link = '{0}|Referer={1}'.format(urllib.quote(link, '.:/*&^%$#@!_-+='), item)
            quality, info = source_utils.get_release_quality(quality, FN)
            info.append(FSize)
            info = ' | '.join(info)
            sources.append(
                {'source': 'GVIDEO', 'quality': quality, 'language': 'en', 'url': link, 'direct': True,
                 'info': info, 'debridonly': False})

            return sources
        except BaseException:
            return sources

    def resolve(self, url):
        return url
