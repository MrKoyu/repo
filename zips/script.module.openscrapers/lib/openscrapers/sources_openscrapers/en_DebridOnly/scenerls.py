# -*- coding: utf-8 -*-
# modified by Venom for Openscrapers

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
from openscrapers.modules import debrid
from openscrapers.modules import source_utils


class source:
	def __init__(self):
		self.priority = 21
		self.language = ['en']
		self.domains = ['scene-rls.com', 'scene-rls.net']
		self.base_link = 'http://scene-rls.net'
		self.search_link = '/?s=%s'


	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'title': title, 'year': year}
			url = urllib.urlencode(url)
			return url
		except:
			return


	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
			url = urllib.urlencode(url)
			return url
		except:
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
			return


	def sources(self, url, hostDict, hostprDict):
		scraper = cfscrape.create_scraper()
		sources = []
		try:
			if url is None:
				return sources

			if debrid.status() is False:
				return sources

			hostDict = hostprDict + hostDict

			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			title = title.replace('&', 'and').replace('Special Victims Unit', 'SVU')

			hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

			query = '%s %s' % (title, hdlr)
			query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)

			try:
				url = self.search_link % urllib.quote_plus(query)
				url = urlparse.urljoin(self.base_link, url)
				# log_utils.log('url = %s' % url, log_utils.LOGDEBUG)

				r = scraper.get(url).content
				posts = client.parseDOM(r, 'div', attrs={'class': 'post'})

				items = []
				dupes = []
				for post in posts:
					try:
						content = client.parseDOM(post, "div", attrs={"class": "postContent"})
						size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', content[0])[0]
						u = client.parseDOM(content, "h2")
						u = client.parseDOM(u, 'a', ret='href')
						u = [(i.strip('/').split('/')[-1], i, size) for i in u]
						items += u
					except:
						source_utils.scraper_error('SCENERLS')
						pass

			except:
				source_utils.scraper_error('SCENERLS')
				pass

			for item in items:
				try:
					name = item[0]
					name = client.replaceHTMLCodes(name)
					if source_utils.remove_lang(name):
						return

					t = name.split(hdlr)[0].replace(data['year'], '').replace('(', '').replace(')', '').replace('&', 'and')
					if cleantitle.get(t) != cleantitle.get(title):
						continue

					if hdlr not in name:
						continue

					# check year for reboot/remake show issues if year is available-crap shoot
					# if 'tvshowtitle' in data:
						# if re.search(r'([1-3][0-9]{3})', name):
							# if not any(value in name for value in [data['year'], str(int(data['year'])+1), str(int(data['year'])-1)]):
								# continue

					quality, info = source_utils.get_release_quality(name, item[1])

					try:
						dsize, isize = source_utils._size(item[2])
						info.insert(0, isize)
					except:
						dsize = 0
						pass

					info = ' | '.join(info)

					url = item[1]
					if any(x in url for x in ['.rar', '.zip', '.iso', '.sample.']):
						continue

					url = client.replaceHTMLCodes(url)
					url = url.encode('utf-8')
					if url in str(sources):
						continue

					host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
					if not host in hostDict:
						continue

					host = client.replaceHTMLCodes(host)
					host = host.encode('utf-8')

					sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info,
									'direct': False, 'debridonly': True, 'size': dsize})
				except:
					source_utils.scraper_error('SCENERLS')
					pass

			return sources

		except:
			source_utils.scraper_error('SCENERLS')
			return sources


	def resolve(self, url):
		return url
