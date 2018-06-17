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

import re,traceback,urllib,urlparse,base64
import requests

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils
from resources.lib.modules import log_utils

session = requests.Session()

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['cooltvseries.com']
        self.base_link = 'https://cooltvseries.com'
        self.show_link = '%s/%s/season-%s/'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            failure = traceback.format_exc()
            log_utils.log('CoolTV - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            urldata = urlparse.parse_qs(url)
            urldata = dict((i, urldata[i][0]) for i in urldata)
            tvshowtitle = urldata['tvshowtitle'].replace(' ', '-').lower()
            start_url = self.show_link  % (self.base_link,tvshowtitle,season)

            html = client.request(start_url)
            container = client.parseDOM(html, 'div', attrs={'class':'dwn-box'})[0]
            Links = client.parseDOM(container, 'a', ret='href')

            for epi_url in Links:
                if cleantitle.get(title) in cleantitle.get(epi_url):
                    return epi_url
        except:
            failure = traceback.format_exc()
            log_utils.log('CoolTV - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None: return sources

            html = client.request(url)
            try:
                iframe = client.parseDOM(html, 'iframe', attrs = {'class': 'embed-responsive-item'}, ret='src')[0]
                host = iframe.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                sources.append({'source':host,'quality':'SD','language': 'en','url':iframe,'direct':False,'debridonly':False})
            except:
                flashvar = client.parseDOM(html, 'param', attrs = {'name': 'flashvars'}, ret='value')[0]
                link = flashvar.split('file=')[1]
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                sources.append({'source':host,'quality':'SD','language': 'en','url':link,'direct':False,'debridonly':False})

            containers = client.parseDOM(html, 'div', attrs={'class':'dwn-box'})

            for list in containers:
                link = client.parseDOM(list, 'a', attrs={'rel':'nofollow'}, ret='href')[0]
                redirect = client.request(link, output='geturl')
                quality,info = source_utils.get_release_quality(redirect)
                sources.append({'source':'DirectLink','quality':quality,'language': 'en','url':redirect,'info':info,'direct':True,'debridonly':False})
            return sources
        except:
            failure = traceback.format_exc()
            log_utils.log('CoolTV - Exception: \n' + str(failure))
            return

    def resolve(self, url):
        return url


