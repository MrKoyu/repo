# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 06-17-2019 by JewBMX in Scrubs.
# modified by Venom (added cfscrape 4-3-2020)

#  ..#######.########.#######.##....#..######..######.########....###...########.#######.########..######.
#  .##.....#.##.....#.##......###...#.##....#.##....#.##.....#...##.##..##.....#.##......##.....#.##....##
#  .##.....#.##.....#.##......####..#.##......##......##.....#..##...##.##.....#.##......##.....#.##......
#  .##.....#.########.######..##.##.#..######.##......########.##.....#.########.######..########..######.
#  .##.....#.##.......##......##..###.......#.##......##...##..########.##.......##......##...##........##
#  .##.....#.##.......##......##...##.##....#.##....#.##....##.##.....#.##.......##......##....##.##....##
#  ..#######.##.......#######.##....#..######..######.##.....#.##.....#.##.......#######.##.....#..######.

'''
    OpenScrapers Project
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
import urllib
import urlparse

from openscrapers.modules import cfscrape
from openscrapers.modules import cleantitle
from openscrapers.modules import client
from openscrapers.modules import directstream
from openscrapers.modules import source_utils


class source:
	def __init__(self):
		self.priority = 39
		self.language = ['en']
		self.domains = ['series9.to']
		self.base_link = 'https://www5.series9.to'
		self.search_link = '/movie/search/%s'
		self.scraper = cfscrape.create_scraper()


	def matchAlias(self, title, aliases):
		try:
			for alias in aliases:
				if cleantitle.get(title) == cleantitle.get(alias['title']):
					return True
		except:
			source_utils.scraper_error('SERIES9')
			return False


	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			aliases.append({'country': 'us', 'title': title})
			url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
			url = urllib.urlencode(url)
			return url
		except:
			source_utils.scraper_error('SERIES9')
			return


	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			aliases.append({'country': 'us', 'title': tvshowtitle})
			url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
			url = urllib.urlencode(url)
			return url
		except:
			source_utils.scraper_error('SERIES9')
			return


	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if url is None:
				return
			url = urlparse.parse_qs(url)
			url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
			url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
			url = urllib.urlencode(url)
			return url
		except:
			source_utils.scraper_error('SERIES9')
			return


	def searchShow(self, title, season, aliases, headers):
		try:
			title = cleantitle.normalize(title)
			search = '%s Season %01d' % (title, int(season))
			url = urlparse.urljoin(self.base_link, self.search_link % cleantitle.geturl(search))
			r = self.scraper.get(url).content
			r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
			r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
			r = [(i[0], i[1], re.findall('(.*?)\s+-\s+Season\s+(\d)', i[1])) for i in r]
			r = [(i[0], i[1], i[2][0]) for i in r if len(i[2]) > 0]
			url = [i[0] for i in r if self.matchAlias(i[2][0], aliases) and i[2][1] == season][0]
			url = urlparse.urljoin(self.base_link, '%s/watching.html' % url)
			return url
		except:
			source_utils.scraper_error('SERIES9')
			return


	def searchMovie(self, title, year, aliases, headers):
		try:
			title = cleantitle.normalize(title)
			url = urlparse.urljoin(self.base_link, self.search_link % cleantitle.geturl(title))
			r = self.scraper.get(url).content
			r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
			r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='oldtitle'))
			results = [(i[0], i[1], re.findall('\((\d{4})', i[1])) for i in r]
			try:
				r = [(i[0], i[1], i[2][0]) for i in results if len(i[2]) > 0]
				url = [i[0] for i in r if self.matchAlias(i[1], aliases) and (year == i[2])][0]
			except:
				url = None
				pass
			if url is None:
				try:
					url = [i[0] for i in results if self.matchAlias(i[1], aliases)][0]
				except:
					return
			url = urlparse.urljoin(self.base_link, '%s/watching.html' % url)
			return url
		except:
			source_utils.scraper_error('SERIES9')
			return


	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			if url is None:
				return sources
			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
			aliases = eval(data['aliases'])
			headers = {}
			if 'tvshowtitle' in data:
				ep = data['episode']
				url = '%s/film/%s-season-%01d/watching.html?ep=%s' % (
					self.base_link, cleantitle.geturl(data['tvshowtitle']), int(data['season']), ep)
				r = self.scraper.get(url).content
				if url is None:
					url = self.searchShow(data['tvshowtitle'], data['season'], aliases, headers)
			else:
				url = self.searchMovie(data['title'], data['year'], aliases, headers)
				if url is None:
					url = '%s/film/%s/watching.html?ep=0' % (self.base_link, cleantitle.geturl(data['title']))
			if url is None:
				return sources
			r = self.scraper.get(url).content
			r = client.parseDOM(r, 'div', attrs={'class': 'les-content'})
			if 'tvshowtitle' in data:
				ep = data['episode']
				links = client.parseDOM(r, 'a', attrs={'episode-data': ep}, ret='player-data')
			else:
				links = client.parseDOM(r, 'a', ret='player-data')
			for link in links:
				if '123movieshd' in link or 'seriesonline' in link:
					r = self.scraper.get(link).content
					r = re.findall('(https:.*?redirector.*?)[\'\"]', r)
					for i in r:
						try:
							sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'],
							                'language': 'en', 'url': i, 'direct': True, 'debridonly': False})
						except:
							source_utils.scraper_error('SERIES9')
							pass
				else:
					try:
						host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(link.strip().lower()).netloc)[0]
						if not host in hostDict:
							continue
						host = client.replaceHTMLCodes(host)
						host = host.encode('utf-8')
						sources.append({'source': host, 'quality': 'SD', 'info': '', 'language': 'en', 'url': link, 'direct': False,
						                'debridonly': False})
					except:
						source_utils.scraper_error('SERIES9')
						pass
			return sources
		except:
			source_utils.scraper_error('SERIES9')
			return sources


	def resolve(self, url):
		if "google" in url:
			return directstream.googlepass(url)
		else:
			return url