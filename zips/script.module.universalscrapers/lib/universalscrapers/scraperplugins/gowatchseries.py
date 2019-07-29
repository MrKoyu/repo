# -*- coding: utf-8 -*-
# 30/10/2018 -BUG

import re, xbmcaddon, time
import urllib, urlparse, requests
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, clean_search, filter_host, send_log,error_log
from universalscrapers.modules import client

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class thewatchseries(Scraper):
    domains = ['gowatchseries.co', 'gowatchseries.tv']
    name = "GoWatchSeries"
    sources = []


    def __init__(self):
        self.base_link = 'https://gowatchseries.tv/'
        self.sources = []


    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            scrape = urllib.quote_plus(clean_search(title))
            start_url = '%s/search.html?keyword=%s' % (self.base_link, scrape)
            html = client.request(start_url)
            thumbs = re.compile('<ul class="listing items">(.+?)</ul> ',re.DOTALL).findall(html)
            thumb = re.compile('href="(.+?)".+?alt="(.+?)"',re.DOTALL).findall(str(thumbs))
            for link, link_title in thumb:
                if clean_title(title).lower() == clean_title(link_title).lower():
                    page_link = urlparse.urljoin(self.base_link, link)
                    holdpage = client.request(page_link)
                    datecheck = re.compile('<span>Release: </span>(.+?)</li>',re.DOTALL).findall(holdpage)[0]
                    if year in datecheck:
                        movie_link = re.compile('<li class="child_episode".+?href="(.+?)"',re.DOTALL).findall(holdpage)[0]
                        movie_link = urlparse.urljoin(self.base_link, movie_link)
                        self.get_source(movie_link,title,year,'','',start_time)
                    else:pass
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources


    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_time = time.time()
            scrape = urllib.quote_plus(clean_search(title))
            start_url = '%s/search.html?keyword=%s' %(self.base_link, scrape)
            html = client.request(start_url)
            thumbs = re.compile('<ul class="listing items">(.+?)</ul> ',re.DOTALL).findall(html)
            thumb = re.compile('href="(.+?)".+?alt="(.+?)"',re.DOTALL).findall(str(thumbs))  
            for link, link_title in thumb:
                if clean_title(title) in clean_title(link_title):
                    season_chk = '-season-%s' %season
                    if not season_chk in link:
                        continue
                    page_link = urlparse.urljoin(self.base_link, link)
                    holdpage = client.request(page_link)
                    series_links = re.compile('<li class="child_episode".+?href="(.+?)"',re.DOTALL).findall(holdpage)
                    for movie_link in series_links:
                        episode_chk = '-episode-%sBOLLOX' %episode
                        spoof_link = movie_link + 'BOLLOX'
                        if episode_chk in spoof_link:
                            movie_link = urlparse.urljoin(self.base_link, movie_link)
                            self.get_source(movie_link,title,year,season,episode,start_time)
                    else:
                        pass
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)


    def get_source(self, movie_link, title, year, season, episode, start_time):
        try:
            html = client.request(movie_link)
            links = client.parseDOM(html, 'li', ret='data-video')
            count = 0 
            for link in links:
                if 'vidcloud' in link:
                    continue
                elif 'openload' in link:
                    try:
                        chk = requests.get(link).content
                        rez = re.compile('"description" content="(.+?)"',re.DOTALL).findall(chk)[0]
                        if '1080' in rez:
                            res='1080p'
                        elif '720' in rez:
                            res='720p'
                        else:
                            res ='DVD'
                    except: res = 'DVD'
                    count +=1
                    self.sources.append({'source': 'Openload', 'quality': res, 'scraper': self.name, 'url': link,'direct': False})
                elif 'streamango.com' in link:
                    get_res=requests.get(link).content
                    try:
                        res = re.compile('{type:"video/mp4".+?height:(.+?),',re.DOTALL).findall(get_res)[0]
                        count +=1
                        self.sources.append({'source': 'Streamango', 'quality': res, 'scraper': self.name, 'url': link,'direct': False})
                    except:
                        pass
                else:
                    host = link.split('//')[1].replace('www.','')
                    host = host.split('/')[0].split('.')[0].title()
                    count +=1
                    self.sources.append({'source': host, 'quality': 'DVD','scraper': self.name,'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year, season=season,episode=episode)
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)


