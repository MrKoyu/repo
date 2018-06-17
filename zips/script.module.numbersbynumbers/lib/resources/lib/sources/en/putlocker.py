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


import re,urllib,urlparse,json,base64,time

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream
from resources.lib.modules import source_utils



class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['putlocker.systems', 'putlocker-movies.tv', 'cartoonhd.website', 'cartoonhd.online', 'cartoonhd.cc']
        self.base_link = 'https://cartoonhd.in'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': title})
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def searchShow(self, title, season, episode, aliases, headers):
        try:
            for alias in aliases:
                url = '%s/show/%s/season/%01d/episode/%01d' % (self.base_link, cleantitle.geturl(alias['title']), int(season), int(episode))
                url = client.request(url, headers=headers,output='geturl', timeout='10')
                if not url == None and url != self.base_link: break
            return url
        except:
            return

    def searchMovie(self, title, year, aliases, headers):
        try:
            for alias in aliases:
                url = '%s/full-movie/%s' % (self.base_link, cleantitle.geturl(alias['title']))
                url = client.request(url, headers=headers, output='geturl', timeout='10')
                if not url == None and url != self.base_link: break
            if url == None:
                for alias in aliases:
                    url = '%s/full-movie/%s-%s' % (self.base_link, cleantitle.geturl(alias['title']), year)
                    url = client.request(url, headers=headers, output='geturl', timeout='10')
                    if not url == None and url != self.base_link: break

            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            imdb = data['imdb']
            aliases = eval(data['aliases'])
            headers = {}

            if 'tvshowtitle' in data:
                url = self.searchShow(title, int(data['season']), int(data['episode']), aliases, headers)
            else:
                url = self.searchMovie(title, data['year'], aliases, headers)

            r = client.request(url, headers=headers, output='extended', timeout='10')

            if not imdb in r[0]: raise Exception()


            cookie = r[4] ; headers = r[3] ; result = r[0]

            try:
                r = re.findall('(https:.*?redirector.*?)[\'\"]', result)
                for i in r:
                    try:
                        sources.append(
                            {'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'language': 'en',
                             'url': i, 'direct': True, 'debridonly': False})
                    except:
                        pass
            except:
                pass

            try: auth = re.findall('__utmx=(.+)', cookie)[0].split(';')[0]
            except: auth = 'false'
            auth = 'Bearer %s' % urllib.unquote_plus(auth)
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
            headers['Authorization'] = auth
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            headers['Accept-Encoding'] = 'gzip,deflate,br'
            headers['Referer'] = url

            u = '/ajax/tnembedr.php'
            self.base_link = client.request(self.base_link, headers=headers, output='geturl')
            u = urlparse.urljoin(self.base_link, u)

            action = 'getEpisodeEmb' if '/episode/' in url else 'getMovieEmb'

            elid = urllib.quote(base64.encodestring(str(int(time.time()))).strip())

            token = re.findall("var\s+tok\s*=\s*'([^']+)", result)[0]

            idEl = re.findall('elid\s*=\s*"([^"]+)', result)[0]

            post = {'action': action, 'idEl': idEl, 'token': token, 'elid': elid}
            post = urllib.urlencode(post)
            cookie += ';%s=%s'%(idEl,elid)
            headers['Cookie'] = cookie

            r = client.request(u, post=post, headers=headers, cookie=cookie, XHR=True)
            r = str(json.loads(r))
            r = re.findall('\'(http.+?)\'', r) + re.findall('\"(http.+?)\"', r)

            for i in r:
                #try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'language': 'en', 'url': i, 'direct': True, 'debridonly': False})
                #except: pass
                if 'googleusercontent' in i or 'blogspot' in i:
                    try:
                        newheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                               'Accept': '*/*',
                               'Host': 'lh3.googleusercontent.com',
                               'Accept-Language': 'en-US,en;q=0.8,de;q=0.6,es;q=0.4',
                               'Accept-Encoding': 'identity;q=1, *;q=0',
                               'Referer': url,
                               'Connection': 'Keep-Alive',
                               'X-Client-Data': 'CJK2yQEIo7bJAQjEtskBCPqcygEIqZ3KAQjSncoBCKijygE=',
                               'Range': 'bytes=0-'
                          }
                        resp = client.request(i, headers=newheaders, redirect=False, output='extended', timeout='10')
                        loc = resp[2]['Location']
                        c = resp[2]['Set-Cookie'].split(';')[0]
                        i = '%s|Cookie=%s' % (loc, c)
                        urls, host, direct = [{'quality': 'SD', 'url': i}], 'gvideo', True    
                                            
                    except: 
                        pass

                try:
                    #direct = False
                    quali = 'SD'
                    quali = source_utils.check_sd_url(i)
                    if 'googleapis' in i:
                        sources.append({'source': 'gvideo', 'quality': quali, 'language': 'en', 'url': i, 'direct': True, 'debridonly': False})
                        continue
                    valid, hoster = source_utils.is_host_valid(i, hostDict)
                    if not urls or urls == []:
                        urls, host, direct = source_utils.check_directstreams(i, hoster)
                    if valid:
                         for x in urls:
                             if host == 'gvideo':
                                 try:
                                     x['quality'] = directstream.googletag(x['url'])[0]['quality']
                                 except: 
                                     pass

                             sources.append({'source': host, 'quality': x['quality'], 'language': 'en', 'url': x['url'], 'direct': direct, 'debridonly': False})                             
                    else:
                        sources.append({'source': 'CDN', 'quality': quali, 'language': 'en', 'url': i, 'direct': True, 'debridonly': False})
                except: pass

            return sources
        except:
            return sources


    def resolve(self, url):
        if 'google' in url and not 'googleapis' in url:
            return directstream.googlepass(url)
        else:
            return url

