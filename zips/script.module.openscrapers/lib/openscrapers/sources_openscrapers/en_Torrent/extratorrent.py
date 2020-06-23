# -*- coding: utf-8 -*-
# created by Venom for Openscrapers (added cfscrape 4-20-2020)(updated 5-16-2020)

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
from openscrapers.modules import client
from openscrapers.modules import debrid
from openscrapers.modules import source_utils
from openscrapers.modules import workers


class source:
	def __init__(self):
		self.priority = 2
		self.language = ['en']
		self.domains = ['extratorrent.ag']
		self.base_link = 'https://extratorrent.ag'
		self.search_link = '/search/?search=%s&new=1&x=53&y=11'
		self.min_seeders = 1


	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'title': title, 'year': year}
			url = urllib.urlencode(url)
			return url
		except:
			source_utils.scraper_error('EXTRATORRENT')
			return


	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
			url = urllib.urlencode(url)
			return url
		except:
			source_utils.scraper_error('EXTRATORRENT')
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
			source_utils.scraper_error('EXTRATORRENT')
			return


	def sources(self, url, hostDict, hostprDict):
		self.sources = []
		try:
			scraper = cfscrape.create_scraper()

			if url is None:
				return self.sources

			if debrid.status() is False:
				return self.sources

			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			self.title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			self.title = self.title.replace('&', 'and').replace('Special Victims Unit', 'SVU')

			self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
			self.year = data['year']

			query = '%s %s' % (self.title, self.hdlr)
			query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)

			urls = []
			url = self.search_link % urllib.quote_plus(query)
			url = urlparse.urljoin(self.base_link, url)
			urls.append(url)
			# urls.append('%s%s' % (url, '&page=2')) # next page seems broken right now
			# urls.append('%s%s' % (url, '&page=3'))
			# log_utils.log('urls = %s' % urls, log_utils.LOGDEBUG)

			links = []
			for x in urls:
				r = scraper.get(x).content
				if not r:
					continue
				list = client.parseDOM(r, 'tr', attrs={'class': 'tlr'})
				list += client.parseDOM(r, 'tr', attrs={'class': 'tlz'})
				for item in list:
					links.append(item)

			threads = []
			for link in links:
				threads.append(workers.Thread(self.get_sources, link))
			[i.start() for i in threads]
			[i.join() for i in threads]
			return self.sources
		except:
			source_utils.scraper_error('EXTRATORRENT')
			return self.sources


	def get_sources(self, link):
		try:
			url = 'magnet:%s' % (re.findall('a href="magnet:(.+?)"', link, re.DOTALL)[0])
			url = urllib.unquote_plus(url).replace('&amp;', '&').replace(' ', '.')
			url = url.split('&tr')[0]
			url = url.encode('ascii', errors='ignore').decode('ascii', errors='ignore')

			hash = re.compile('btih:(.*?)&').findall(url)[0]

			name = url.split('&dn=')[1]
			name = re.sub('[^A-Za-z0-9]+', '.', name).lstrip('.')
			if source_utils.remove_lang(name):
				return

			match = source_utils.check_title(self.title, name, self.hdlr, self.year)
			if not match:
				return

			if url in str(self.sources):
				return

			try:
				seeders = int(client.parseDOM(link, 'td', attrs={'class': 'sy'})[0].replace(',', ''))
				if self.min_seeders > seeders:
					return
			except:
				seeders = 0
				pass

			quality, info = source_utils.get_release_quality(name, url)

			try:
				size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', link)[0]
				dsize, isize = source_utils._size(size)
				info.insert(0, isize)
			except:
				source_utils.scraper_error('EXTRATORRENT')
				dsize = 0
				pass

			info = ' | '.join(info)

			self.sources.append({'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'quality': quality,
											'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
		except:
			source_utils.scraper_error('EXTRATORRENT')
			pass


	def resolve(self, url):
		return url