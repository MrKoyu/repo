# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @tantrumdev wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Numbers
# Addon id: Numbers
# Addon Provider: Numbers

import re,traceback,urllib,urlparse,base64
import requests

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import log_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.bnwmovies.com']
        self.base_link = 'http://www.bnwmovies.com/'
        self.search_link = '%s/search?q=bnwmovies.com+%s+%s'
        self.goog = 'https://www.google.co.uk'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            scrape = title.lower().replace(' ','+').replace(':', '')

            start_url = self.search_link %(self.goog,scrape,year)

            html = client.request(start_url)
            results = re.compile('href="(.+?)"',re.DOTALL).findall(html)
            for url in results:
                if self.base_link in url:
                    if 'webcache' in url:
                        continue
                    if cleantitle.get(title) in cleantitle.get(url):
                        chkhtml = client.request(url)
                        chktitle = re.compile('<title.+?>(.+?)</title>',re.DOTALL).findall(chkhtml)[0]
                        if cleantitle.get(title) in cleantitle.get(chktitle):
                            if year in chktitle:
                                return url
            return
        except:
            failure = traceback.format_exc()
            log_utils.log('BNWMovies - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None: return sources

            html = client.request(url)

            Links = re.compile('<source.+?src="(.+?)"',re.DOTALL).findall(html)
            for link in Links:
                sources.append({'source':'BNW','quality':'SD','language': 'en','url':link,'direct':True,'debridonly':False})
            return sources
        except:
            failure = traceback.format_exc()
            log_utils.log('BNWMovies - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url