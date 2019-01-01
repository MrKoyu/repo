# -*- coding: utf-8 -*-
# Universal Scrapers Bug
#checked 2/11/2018

import re, time, xbmcaddon
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, clean_search, get_rd_domains, send_log, error_log
from universalscrapers.modules import client, cfscrape

User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class twoddl(Scraper):
    domains = ['2ddl.ws']
    name = "TwoDDL"
    sources = []

    def __init__(self):
        self.base_link = 'http://2ddl.ws'


    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            if not debrid:
                return self.sources
            start_url = "%s/?s=%s" % (self.base_link, title.replace(' ', '+').lower())
            headers = {'User-Agent': client.agent()}
            scraper = cfscrape.create_scraper()
            OPEN = scraper.get(start_url, headers=headers).content

            content = re.compile('<h2><a href="(.+?)"', re.DOTALL).findall(OPEN)
            for url in content:
                self.get_source(url, title, year, '', '', start_time)

        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            if not debrid:
                return self.sources
            season_url = "0%s" % season if len(season) < 2 else season
            episode_url = "0%s" % episode if len(episode) < 2 else episode
            sea_epi = 's%se%s' % (season_url, episode_url)

            start_url = "%s/?s=%s+%s" % (self.base_link, title.replace(' ', '+').lower(), sea_epi)

            headers = {'User-Agent': client.agent()}
            scraper = cfscrape.create_scraper()
            OPEN = scraper.get(start_url, headers=headers).content
            content = re.compile('<h2><a href="([^"]+)"', re.DOTALL).findall(OPEN)
            for url in content:
                if not clean_title(title).lower() in clean_title(url).lower():
                    continue
                self.get_source(url, title, year, season, episode, start_time)

        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def get_source(self, url, title, year, season, episode, start_time):
        try:
            headers = {'User-Agent': client.agent()}
            scraper = cfscrape.create_scraper()
            links = scraper.get(url, headers=headers).content
            LINK = re.compile('href="([^"]+)" rel="nofollow"', re.DOTALL).findall(links)
            count = 0
            for url in LINK:
                if any(x in url for x in ['.rar', '.zip', '.iso']):continue

                if '1080' in url:
                    res = '1080p'
                elif '720' in url:
                    res = '720p'
                elif 'HDTV' in url:
                    res = 'HD'
                else:
                    res = "SD"

                host = url.split('//')[1].replace('www.', '')
                host = host.split('/')[0].lower()

                rd_domains = get_rd_domains()
                if host in rd_domains:
                    count += 1
                    self.sources.append(
                        {'source': host, 'quality': res, 'scraper': self.name, 'url': url, 'direct': False, 'debridonly': True})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year, season=season, episode=episode)

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources


#twoddl().scrape_movie('Deadpool 2', '2018', '', False)
