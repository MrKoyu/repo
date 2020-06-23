# -*- coding: utf-8 -*-
# created by Venom for Openscrapers (updated url 6-13-2020)

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

import json
import urllib
import urlparse

from openscrapers.modules import cleantitle
from openscrapers.modules import client
from openscrapers.modules import source_utils


class source:
	def __init__(self):
		self.priority = 32
		self.language = ['en']
		self.domains = ['watchepisodeseries1.com']
		self.base_link = 'https://www.watchepisodeseries1.com'
		self.search_link = '/home/search?q=%s' # json search


	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			# url = tvshowtitle.replace(" ", "+")
			url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
			url = urllib.urlencode(url)
			return url
		except:
			source_utils.scraper_error('WATCHEPISODESERIES1')
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
			source_utils.scraper_error('WATCHEPISODESERIES1')
			return


	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			if url is None:
				return sources

			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			title = data['tvshowtitle']
			hdlr = 's%02de%02d' % (int(data['season']), int(data['episode']))
			query = urllib.quote_plus(cleantitle.getsearch(title))
			surl = urlparse.urljoin(self.base_link, self.search_link % query)
			r = client.request(surl, XHR=True)
			r = json.loads(r)
			r = r['series']

			for i in r:
				tit = i['original_name']
				if cleantitle.get(title) != cleantitle.get(tit):
					continue
				slink = '/' + i['seo_name']
				slink = urlparse.urljoin(self.base_link, slink)
				r = client.request(slink)
				data = client.parseDOM(r, 'div', attrs={'class': 'el-item\s*'})
				ep = [i for i in client.parseDOM(data, 'a', ret='href') if hdlr in i.lower()][0]
				r = client.request(ep)
				links = client.parseDOM(r, 'a', attrs={'class': 'watch-button'}, ret='href')

				for link in links:
					list = client.request(link)
					url = client.parseDOM(list, 'a', attrs={'class': 'watch-button actWatched'}, ret='href')[0]
					try:
						valid, host = source_utils.is_host_valid(url, hostDict)
						if not valid:
							continue
						sources.append({'source': host, 'quality': '720p', 'info': '', 'language': 'en', 'url': url,
										'direct': False, 'debridonly': False})
					except:
						source_utils.scraper_error('WATCHEPISODESERIES1')
						return sources
			return sources
		except:
			source_utils.scraper_error('WATCHEPISODESERIES1')
			return sources


	def resolve(self, url):
		return url