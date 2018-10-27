# -*- coding: UTF-8 -*-

'''
    Numbers Add-on

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
import base64
import requests
from time import time

from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['ondarewatch.com', 'dailytvfix.com']
        self.base_link = 'http://www.dailytvfix.com'
        self.search_link = self.base_link + '/ajax/search.php'
        self.ua = client.randomagent()

        # Search headers for 'http://www.dailytvfix/ajax/search.php'.
        self.search_headers = {
            'Host': self.base_link.replace('http://', '', 1),
            'User-Agent': self.ua,
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': self.base_link + '/',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1'
        }


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            possible_titles = set(
                (title.lower(),) + tuple((alias['title'].lower() for alias in aliases) if aliases else ())
            )
            json_data = self._ajax_post(title.lower())
            for entry in json_data:
                if 'movie' in entry['meta'].lower():
                    if entry['title'].lower() in possible_titles:
                        url = self.base_link + entry['permalink']
                        return url
            return None
        except:
            return None


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvshowtitle = tvshowtitle.lower()
            possible_titles = set(
                (tvshowtitle,) + tuple((alias['title'] for alias in aliases) if aliases else ())
            )
            best_guesses = [ ]
            json_data = self._ajax_post(tvshowtitle)
            for entry in json_data:
                if 'tv' in entry['meta'].lower():
                    entry_title_lower = entry['title'].lower()
                    if entry_title_lower in possible_titles:
                        best_guesses.append(entry['permalink'])
                    elif (tvshowtitle in entry_title_lower and year in entry_title_lower):
                        # For special cases like 'The Flash' vs 'The Flash 2014', make the entry
                        # that matches the most (including year) be prepended.
                        best_guesses.insert(0, entry['permalink'])
            if best_guesses:
                url = self.base_link + best_guesses[0]
                return url
        except:
            return None


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        return url + '/season/%s/episode/%s' % (season, episode)


    def sources(self, url, hostDict, hostprDict):
        sources = [ ]        
        
        try:
            # If in the future there's a Cloudflare challenge, use client.request() instead.
            r = requests.get(url, headers={'User-Agent': self.ua}, timeout=10)
        except:
            r = type('_dummy', (object,), {'ok': False})
            
        if r.ok:            
            match = re.findall("] = '(.+?)'", r.text, re.DOTALL)
            for iframe_blob in match:
                iframe = base64.b64decode(iframe_blob)
                temp = re.search('src="(.+?)"', iframe, re.DOTALL|re.IGNORECASE)
                if temp:
                    host_url = temp.group(1).strip() # strip() because sometimes there's an '\r' at the end.
                else:
                    continue

                if 'openload' in host_url:
                    quality = 'HD'
                    # Avoids some duplicate Openload links, both of these come up:
                    # https://openload.co/embed/dVdG-TGRkZc/Ready.Player.One.2018.(...)
                    # https://openload.co/embed/dVdG-TGRkZc
                    for source in sources:
                        if ((len(host_url) < len(source['url']) and host_url in source['url'])
                            or (len(host_url) > len(source['url']) and source['url'] in host_url)):
                            continue
                else:
                    quality = 'SD'

                hoster = host_url.split('//', 1)[1].replace('www.', '', 1)
                hoster = hoster[ : hoster.find('/')]
                sources.append(
                    {
                        'source': hoster,
                        'quality': quality,
                        'language': 'en',
                        'url': host_url,
                        'direct': False,
                        'debridonly': False
                    }
                )
        return sources


    def _ajax_post(self, query):
        data = {'limit': 15, 'q': query, 'timestamp': int(time() * 1000)}
        r = requests.post(self.search_link, data=data, headers=self.search_headers, timeout=8)
        if r.ok and r.text != 'Restricted access':
            json_data = r.json()
            return json_data if (len(json_data) > 1 or json_data[0]['meta'].lower() != 'more') else ()
        else:
            return ()
        
    def resolve(self, url):
        return url


    def _debug(self, name, val):
        import xbmc
xbmc.log('DAREWATCH > %s %s' % (name, str(val)), xbmc.LOGWARNING)