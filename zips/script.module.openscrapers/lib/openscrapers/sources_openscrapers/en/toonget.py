# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 08-24-2019 by JewBMX in Scrubs.

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

from openscrapers.modules import cleantitle
from openscrapers.modules import client
from openscrapers.modules import source_utils


class source:
	def __init__(self):
		self.priority = 35
		self.language = ['en']
		self.genre_filter = ['animation', 'anime']
		self.domains = ['toonget.net']
		self.base_link = 'https://toonget.net'


	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			title = cleantitle.geturl(title)
			url = '%s-%s' % (title, year)
			url = self.base_link + '/' + url
			return url
		except:
			source_utils.scraper_error('TOONGET')
			return


	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			url = cleantitle.geturl(tvshowtitle)
			return url
		except:
			source_utils.scraper_error('TOONGET')
			return


	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url:
				return
			if season == '1':
				url = self.base_link + '/' + url + '-episode-' + episode
			else:
				url = self.base_link + '/' + url + '-season-' + season + '-episode-' + episode
			return url
		except:
			source_utils.scraper_error('TOONGET')
			return


	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			if url is None:
				return sources
			r = client.request(url)
			match = re.compile('<iframe src="(.+?)"').findall(r)
			# log_utils.log('match = %s' % match, log_utils.LOGDEBUG)

			for url in match:
				r = client.request(url)
				if 'playpanda' in url:
					match = re.compile("url: '(.+?)',").findall(r)
				else:
					match = re.compile('file: "(.+?)",').findall(r)
				for url in match:
					url = url.replace('\\', '')
					if url in str(sources):
						continue

					quality, info = source_utils.get_release_quality(url)
					fileType = source_utils.getFileType(url)
					info.append(fileType)
					info = ' | '.join(info) if fileType else info[0]

					sources.append({'source': 'direct', 'quality': quality, 'language': 'en', 'url': url, 'info': info,
					                'direct': False, 'debridonly': False})
			return sources
		except:
			source_utils.scraper_error('TOONGET')
			return sources


	def resolve(self, url):
		return url