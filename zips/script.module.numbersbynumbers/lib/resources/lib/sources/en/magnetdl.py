'''
    Created by others
    Refactored for lambdascrapers
    Nov 20 2018
'''

import re, requests, xbmc, xbmcaddon
from resolveurl.plugins.premiumize_me import PremiumizeMeResolver
from resources.lib.modules import source_utils

class source:

    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domain = 'http://www.magnetdl.com'
        self.api_key = PremiumizeMeResolver.get_setting('password')
        self.search_link = 'http://www.magnetdl.com/%s/%s/'
        self.checkc = 'https://www.premiumize.me/api/torrent/checkhashes?apikey=%s&hashes[]=%s&apikey=%s'
        self.pr_link = 'https://www.premiumize.me/api/transfer/directdl?apikey=%s&src=magnet:?xt=urn:btih:%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'title': title, 'year': year}
            return url
        except:
            print("Unexpected error in MagnetDL Script: episode", sys.exc_info()[0])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            return url

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = tvshowtitle
            return url
        except:
            print("Unexpected error in MagnetDL Script: TV", sys.exc_info()[0])
            return url
        return url

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            url = url
            url = {'tvshowtitle': url, 'season': season, 'episode': episode, 'premiered': premiered}
            return url
        except:
            print("Unexpected error in MagnetDL Script: episode", sys.exc_info()[0])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            return url

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            with requests.Session() as s:
                headers = {"Referer": self.domain,\
                           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                           "Host": "www.magnetdl.com",
                           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}
                if 'episode' in url:
                    iep = url['episode'].zfill(2)
                    ise = url['season'].zfill(2)
                    se = 's' + ise + 'e' + iep
                    sel = url['tvshowtitle'].replace(' ','-') + '-' + se
                    
                else:
                    sel = url['title'].replace(' ','-') + '-' + url['year']
                    
                sel = sel.lower()
                gs = s.get(self.search_link % (sel[0], sel), headers=headers).text
                gl = re.compile('ih:(.*?)\W.*?ef\W+.*?tle\W+(.*?)[\'"].*?\d</td.*?d>(.*?)<', re.I).findall(gs)
                for hass,nam,siz in gl:
                    checkca = s.get(self.checkc % (self.api_key, hass, self.api_key)).text
                    quality = source_utils.check_sd_url(nam)
                    if 'finished' in checkca:
                        url = self.pr_link % (self.api_key, hass)
                        sources.append({
                            'source': 'cached',
                            'quality': quality,
                            'language': 'en',
                            'url': url,
                            'direct': False,
                            'debridonly': False,
                            'info': siz+'|'+nam,
                        })  
            return sources
        except:
            print("Unexpected error in MagnetDL Script: Sources", sys.exc_info()[0])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            return sources

        
    def resolve(self, url):
        try:
            getpl = requests.get(url).text
            sl = re.compile('link.*?"(h.*?)["\'].\n.*?s.*?http', re.I).findall(getpl)[0]
            url = sl.replace('\\','')
            return url
        except:
            print("Unexpected error in MagnetDL Script: episode", sys.exc_info()[0])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            return url