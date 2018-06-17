# -*- coding: utf-8 -*-
'''
    Copyright (C) 2018 BYB

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
import koding
from HTMLParser import HTMLParser
import dateutil.parser as dparser


class YouTube_Scraper():

	domain = ['https://www.youtube.com/']
	CHANNEL_INFO = []
	CHANNEL_SEARCH =[]
	CHANNEL_VIDEO = []
	CHANNEL_PLAYLIST = []
	SEARCH_VIDEO = []

	def __init__(self):
		self.CookieJar = 'youtube'
		self.baseURL   = 'https://www.youtube.com/'
		self.searchURL = 'results?search_query='
		self.playLINK  = 'plugin://plugin.video.youtube/play/?video_id='
		self.artWORK   = 'https://i.ytimg.com/vi/%s/hqdefault.jpg'

	def channel_info(self,channel_url):
		if channel_url.endswith('/'):
			about_url = channel_url+'about'
		if not channel_url.endswith('/'):
			about_url = channel_url+'/about'
		html = koding.Open_URL(about_url, cookiejar=self.CookieJar,timeout=20)
		match = re.compile('<title>(.+?)</title>.+?',re.DOTALL).findall(html)
		match2 = re.compile('<link itemprop="thumbnailUrl" href="(.+?)">',re.DOTALL).findall(html)
		match3 = re.compile('background-image: url\((.+?)\)',re.DOTALL).findall(html)
		match4 = re.compile('<div class="about-description branded-page-box-padding" >.+?<pre>(.+?)</pre>.+?</div>',re.DOTALL).findall(html)
		for title in match:
			title = ' '.join(title.split())
		for icon in match2:
			icon = icon
		for artwork in match3:
			artwork = artwork.split('=')[0]
			artwork = 'https:'+artwork
		if len(match4) >= 1:
			for description  in match4:
				description = ' '.join(description.split())
		if not len(match4) >= 1:
			description = ''
		self.CHANNEL_INFO.append({'title':title,'description':description,'icon':icon,'artwork':artwork,'channel_url':channel_url})

	def channel_search(self,channel,search_item):
		if not channel.endswith('/'):
			channel = channel+'/'
		url = channel+'search?query=%s' %(search_item.lower())
		html = koding.Open_URL(url, cookiejar=self.CookieJar,timeout=20)
		match = re.compile('<h3 class="yt-lockup-title ">.+? title="(.+?)".+?href="(.+?)".+?<div class="yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2" dir="ltr">(.+?)</div>',re.DOTALL).findall(html)
		for title,url2,description in match:
			try:
				title = HTMLParser().unescape(title)
			except:pass
			title = (title).replace('&amp;','&')
			page_url = 'https://www.youtube.com%s' %url2
			playlink = url2.replace('/watch?v=','')
			artwork = 'https://i.ytimg.com/vi/%s/hqdefault.jpg' %playlink
			playlink = 'plugin://plugin.video.youtube/play/?video_id=%s' %playlink
			description = (description).replace("&#39;","'")
			match3 = re.compile('(<.*?>)',re.DOTALL).findall(str(description))
			for unwanted in match3:
				if len(match3) >= 1:
					description = (description).replace((unwanted),'')
				else:
					description = description
			html2 = koding.Open_URL(page_url, cookiejar=self.CookieJar,timeout=20)
			match2 = re.compile('itemprop="datePublished" content="(.+?)"',re.DOTALL).findall(html2)
			for date in match2:
				date = dparser.parse(date,fuzzy=True)
				date = date.strftime('%Y-%m-%d')
				self.CHANNEL_SEARCH.append({'date':date,'title':title,'playlink':playlink,'artwork':artwork,'description':description})
				
	def channel_video(self,channel_url):
	    if channel_url.endswith('/'):
	        video_url = channel_url+'videos'
	    if not channel_url.endswith('/'):
	        video_url = channel_url+'/videos'
	    html = koding.Open_URL(video_url, cookiejar=self.CookieJar,timeout=20)
	    match = re.compile('<div class="yt-lockup-content">.+?title="(.+?)".+?href="(.+?)"',re.DOTALL).findall(html)
	    for title,vid_id in match:
			page_url = 'https://www.youtube.com'+vid_id
			title = (title).replace('&quot;','"').replace("&#39;","'")
			try:
				title = HTMLParser().unescape(title)
			except:pass
			vid_id = (vid_id).replace('/watch?v=','')
			icon = 'https://i.ytimg.com/vi/%s/hqdefault.jpg' %vid_id
			playlink = 'plugin://plugin.video.youtube/play/?video_id=%s' %vid_id
			html2 = koding.Open_URL(page_url, cookiejar=self.CookieJar,timeout=20)
			match2 = re.compile('<strong class="watch-time-text">Published on (.+?)</strong>.+?<p id="eow-description" class="" >(.+?)</p></div>',re.DOTALL).findall(html2)
			for date,description in match2:
				description = (description).replace('<br />',' ')
				match3 = re.compile('(<.*?>)',re.DOTALL).findall(str(description))
				for unwanted in match3:
					if len(match3) >= 1:
						description = (description).replace((unwanted),'')
					else:
						description = description
				koding.dolog(title)
				self.CHANNEL_VIDEO.append({'title':title,'playlink':playlink,'icon':icon,'date':date,'description':description})
				
	def channel_playlist(self,channel_url):
		if channel_url.endswith('/'):
			playlist_url = channel_url+'playlists'
		if not channel_url.endswith('/'):
			playlist_url = channel_url+'/playlists'
		html = koding.Open_URL(playlist_url, cookiejar=self.CookieJar,timeout=20)
		match = re.compile('<div class="yt-lockup-content">(.+?)</div>',re.DOTALL).findall(html)
		for block in match:              
			Match = re.compile('<h3 class="yt-lockup-title ">.+?title="(.+?)".+?href="(.+?)"',re.DOTALL).findall(str(block))
			for playlist_name,playlist_url in Match:
				playlist_url = 'https://www.youtube.com'+playlist_url
				self.CHANNEL_PLAYLIST.append({'playlist_name':playlist_name,'playlist_url':playlist_url})
				
	def channel_playlist_video(self,playlist_url):
		html = koding.Open_URL(playlist_url, cookiejar=self.CookieJar,timeout=20)
		match = re.compile('<tr class="pl-video yt-uix-tile(.+?)<span class="video-thumb  yt-thumb yt-thumb-72"',re.DOTALL).findall(html)
		for block in match:
			match2 = re.compile('data-video-id="(.+?)"',re.DOTALL).findall(str(block))
			match3 = re.compile('data-title="(.+?)"',re.DOTALL).findall(str(block))      
			for vid_id in match2:
				playlink = 'plugin://plugin.video.youtube/play/?video_id=%s' %vid_id
				icon = 'https://i.ytimg.com/vi/%s/hqdefault.jpg' %vid_id
				url = 'https://www.youtube.com/watch?v=%s' %vid_id
				html2 = koding.Open_URL(url, cookiejar=self.CookieJar,timeout=20)
				match4 = re.compile('<strong class="watch-time-text">Published on (.+?)</strong>.+?<p id="eow-description" class="" >(.+?)</div>',re.DOTALL).findall(html2)
				for date,description in match4:
					description = (description).replace('<br />',' ')
					match5 = re.compile('(<.*?>)',re.DOTALL).findall(str(description))
					for unwanted in match5:
						if len(match3) >= 1:
							description = (description).replace((unwanted),'')
						else:
							description = description
			for title in match3:
				title = title
			self.CHANNEL_VIDEO.append({'title':title,'playlink':playlink,'icon':icon,'date':date,'description':description})
				
	def video_single(self,url):
		html = koding.Open_URL(url, cookiejar=self.CookieJar,timeout=20)
		match = re.compile('<span id="eow-title" class="watch-title" dir="ltr" title="(.+?)"',re.DOTALL).findall(html)
		match2 = re.compile('<p id="eow-description" class="" >(.+?)</p>',re.DOTALL).findall(html)
		match3 = re.compile('<meta itemprop="datePublished" content="(.+?)">',re.DOTALL).findall(html)
		koding.dolog(match,my_debug = True)
		for title in match:
			title = title
		for description in match2:
			match4 = re.compile('(<.*?>)',re.DOTALL).findall(str(description))
			for unwanted in match4:
				if len(match4) >= 1:
					description = (description).replace((unwanted),'')
				else:
					description = description
		for date in match3:
			date = date
		vid_id = url.split('v=')[1]
		playlink = 'plugin://plugin.video.youtube/play/?video_id=%s' %vid_id
		icon = 'https://i.ytimg.com/vi/%s/hqdefault.jpg' %vid_id
		self.CHANNEL_VIDEO.append({'title':title,'playlink':playlink,'icon':icon,'date':date,'description':description})

	def search(self,search_item):
		url = self.baseURL+self.searchURL+search_item.replace(' ','+')
		html = koding.Open_URL(url, cookiejar=self.CookieJar,timeout=20)
		match = re.compile('<h3 class="yt-lockup-title ">(.+?)</span></li></ul></button>',re.DOTALL).findall(html)
		for block in match:
			match2 = re.compile('<a href="(.+?)".+?title="(.+?)".+?Play now',re.DOTALL).findall(str(block))
			for vid_id,title in match2:
				try:
					title = HTMLParser().unescape(title)
				except:pass
				if vid_id.startswith('/watch?v='):
					vid_id = vid_id.split('v=')[1]
				playlink = self.playLINK+vid_id
				icon = self.artWORK %vid_id
				self.SEARCH_VIDEO.append({'playlink':playlink,'title':title,'icon':icon})

	
		
		

			
