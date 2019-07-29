# -*- coding: utf-8 -*-
# Universal Scrapers
#checked 29/10/2018

import re, xbmcaddon, time
import urllib, requests
from universalscrapers.common import clean_title, clean_search, filter_host, send_log, error_log
from universalscrapers.scraper import Scraper

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")
User_Agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4'


class Watchepisodes(Scraper):
    domains = ['watchepisodes4.com']
    name = "WatchEpisodes4"


    def __init__(self):
        self.base_link = 'https://www.watchepisodes4.com/'
        self.sources = []


    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            scrape = clean_search(title.lower())
            start_url = '%ssearch/ajax_search?q=%s' %(self.base_link,scrape)
            headers = {'User_Agent':User_Agent}
            html = requests.get(start_url, headers=headers,timeout=5).content
            regex = re.compile('"value":"(.+?)","seo":"(.+?)"',re.DOTALL).findall(html) 
            for name,link_title in regex:
                if not clean_title(title).lower() == clean_title(name).lower():
                    continue
                show_page = self.base_link + link_title
                format_grab = 'season-%s-episode-%s-' %(season, episode)
                headers = {'User_Agent':User_Agent}
                linkspage = requests.get(show_page, headers=headers,timeout=5).content
                series_links = re.compile('<div class="el-item.+?href="(.+?)"',re.DOTALL).findall(linkspage)
                for episode_url in series_links:
                    if not format_grab in episode_url:
                        continue
                    self.get_sources(episode_url,title,year,season,episode,start_time)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources


    def get_sources(self, episode_url, title, year, season, episode, start_time):
        try:
            headers = {'User_Agent':User_Agent}
            links = requests.get(episode_url,headers=headers,timeout=5).content   
            LINK = re.compile('<div class="link-number".+?data-actuallink="(.+?)"',re.DOTALL).findall(links)
            count = 0            
            for final_url in LINK:
                if final_url in str(self.sources):
                    continue
                host = final_url.split('//')[1].replace('www.','')
                host = host.split('/')[0].lower()
                if not filter_host(host):
                    continue
                host = host.split('.')[0].title()
                if host in str(self.sources):
                    continue
                count += 1
                if count < 25:
                    self.sources.append({'source': host, 'quality': 'DVD', 'scraper': self.name, 'url': final_url, 'direct': False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year, season=season,episode=episode)
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources


