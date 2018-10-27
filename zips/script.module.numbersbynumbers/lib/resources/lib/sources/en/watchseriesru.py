# -*- coding: UTF-8 -*-

'''
    Numbers Add-on

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
from resources.lib.modules import cleantitle
from resources.lib.modules import client

class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['watch-series.ru']
		self.base_link = 'https://watch-series.ru'
		self.search_link = '/series/%s-season-%s-episode-%s'

	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			url = cleantitle.geturl(tvshowtitle)
			return url
		except:
			return
 
	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url: return
			tvshowtitle = url
			url = self.base_link + self.search_link % (tvshowtitle, season, episode)
			return url
		except:
			return

	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			r = client.request(url)
			try:
				match = re.compile('data-video="http(.+?)"><div class=".+?">(.+?)</div>').findall(r)
				for url, source in match: 
					url = 'http' + url
					source = source.replace('OpenUpload','Openload')
					sources.append({
						'source': source,
						'quality': 'SD',
						'language': 'en',
						'url': url,
						'direct': False,
						'debridonly': False
					})
			except:
				return
		except Exception:
			return
		return sources

	def resolve(self, url):
		return url