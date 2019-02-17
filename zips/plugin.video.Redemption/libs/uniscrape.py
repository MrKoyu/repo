# -*- coding: utf-8 -*-
import byb_modules as BYB
import _Edit
import koding
import random
import re
import sys
import universalscrapers
import xbmc 
import xbmcgui
import xbmcplugin
from ._addon import *
from ._common import *

if      setting_resolve     == "resolveurl":from resolveurl import resolve 
elif    setting_resolve     == "urlresolver":from urlresolver import resolve 


#use mode 600-700
# Examples of string
'''
searchmovies = '#search=movies:name=:year=:imdb=:debrid='
searchtv = '#search=tv:name=:show_year=:year=:season=:episode=:imdb=:tvdb=:debrid='
searchmusic = '#search=music:name=:artist=:debrid='
'''
class uniscraper():

	List            = []
	playlist        = []
	CoScraper_links = 0
	p1080           = 0
	p720            = 0
	p480            = 0
	HD              = 0
	SD              = 0
	DVD             = 0
	CAM             = 0
	OTHER           = 0
	line2linksqual  = ''


	def __init__(self,*args,**kwargs):
		self.Icon              = kwargs.get('iconimage',addon_icon)
		self.SortMethod        = _Edit.UniSortMethod
		self.SortReverse       = _Edit.UniSortReverse
		self.DialogSelect      = _Edit.UniDialogSelect
		self.UniShowProgress   = _Edit.UniShowProgress
		self.DialogBoxColor1   = _Edit.DialogBoxColor1
		self.DialogBoxColor2   = _Edit.DialogBoxColor2
		self.Dolog             = koding.dolog
		self.ReleventScrapers  = universalscrapers.relevant_scrapers
		self.DL                = Delimiter()
		if setting_true("uniscrapedialog") and self.DialogSelect == True:
			self.dialogselect = True
			self.movie_scraper = universalscrapers.scrape_movie_with_dialog
			self.tv_scraper    = universalscrapers.scrape_episode_with_dialog
			self.music_scraper = universalscrapers.scrape_song_with_dialog
		else:
			self.dialogselect = False
			self.movie_scraper = universalscrapers.scrape_movie
			self.tv_scraper    = universalscrapers.scrape_episode
			self.music_scraper = universalscrapers.scrape_song
		self.RSL = self.ReleventScrapers()
		self.dp  = xbmcgui.DialogProgress()


	def RSLnames(self,RSL):
		RSLNames = []
		for names in RSL:
			names = str(names)
			name = names.lstrip("<class 'universalscrapers.scraperplugins.").rstrip(">").strip("'").split('.')[-1]
			if name != None or name != '':
				RSLNames.append(name)
		return RSLNames

	def LineOne(self,noRSL):
		Line1 = SingleColor('Completed ',self.DialogBoxColor1)+SingleColor(self.CoScraper_links,self.DialogBoxColor2)+SingleColor(' of ',self.DialogBoxColor1)+SingleColor(noRSL,self.DialogBoxColor2)+SingleColor(' Scrapers',self.DialogBoxColor1)
		return Line1

	def LineTwo(self):
		Line2 = SingleColor('Links Found ',self.DialogBoxColor1)+SingleColor(len(self.List),self.DialogBoxColor2)
		return Line2

	def Run(self,name,url,fanart):
		self.SearchType(name,url,fanart)


	def SearchType(self,name,url,fanart):
		url = url.replace('=:','=none:')
		if url.endswith('debrid='):url=url+'false'
		if url.startswith('#search=movies'):
			match = re.compile('name=(.+?):year=(.+?):imdb=(.+?):debrid=(.+$)').findall(str(url))
			for Name,Year,Imdb,Debrid in match:
				if Name == '#name':
					if '[COLOR' in name:
						Name = self.NameClean(name)
					else:Name = name
				if Year == 'none':
					Year = ''
				if Imdb == 'none':
					Imdb = ''
				Debrid = True if Debrid=='true' else False
				if len(Name) > 0:
					self.movies(title=Name,year=Year,imdb=Imdb,debrid=Debrid,fanart=fanart)
					self.Dolog('searching movies with universalscrapers',line_info=True)
				else:
					self.Dolog('Not enough detail in #search=movie string '+url,line_info=True)
		elif url.startswith('#search=tv'):
			match = re.compile('name=(.+?):show_year=(.+?):year=(.+?):season=(.+?):episode=(.+?):imdb=(.+?):tvdb=(.+?):debrid=(.+$)').findall(str(url))
			for Name,ShowYear,Year,Season,Episode,Imdb,Tvdb,Debrid in match:
				if Name == '#name':
					if '[COLOR' in name:
						Name = self.NameClean(name)
					else:Name = name
				if ShowYear == 'none':
					ShowYear = ''
				if Year == 'none':
					Year = ''
				if Season == 'none':
					Season = ''
				if Episode == 'none':
					Episode = ''
				if Imdb == 'none':
					Imdb = ''
				if Tvdb == 'none': 
					Tvdb = ''
				Debrid = True if Debrid=='true' else False
				if len(Name) > 0 and len(Season) > 0 and len(Episode) > 0:
					self.tvshow(title=Name, show_year=ShowYear, year=Year, season=Season, episode=Episode, imdb=Imdb, tvdb=Tvdb, debrid=Debrid )
				else:
					self.Dolog('Not enough detail in #search=tvshow string '+url,line_info=True)
		elif url.startswith('#search=music'):
			match = re.compile('name=(.+?):artist=(.+?):debrid=(.+$)').findall(str(url))
			for Name,Artist,Debrid in match:
				if Name == '#name':
					if '[COLOR' in name:
						Name = NameClean(name)
					else:Name = name 
				if Artist == 'none':
					Artist = ''
				Debrid = True if Debrid == 'true' else False
				if len(Name) > 0 and len(Artist) > 0:
					self.music(title, artist, debrid)
				else:
					self.Dolog('Not enough detail in #search=music string '+url,line_info=True)
		else:
			self.Dolog('In correct format of search string '+url,line_info=True)
			return

	def movies(self,title,year,imdb,debrid,fanart):
		if self.dialogselect == False:
			self.dp.create(SingleColor('Searching for ',self.DialogBoxColor1)+SingleColor(title,self.DialogBoxColor2))
			noRSL = len(universalscrapers.relevant_scrapers())
			scraper = self.movie_scraper
			links_scraper = scraper(title,year,imdb)
			#try:
			for scraper_links in links_scraper():
				if self.dp.iscanceled():
					break 
				self.CoScraper_links +=1
				Percent = float(100.00/noRSL)*self.CoScraper_links
				self.dp.update(int(Percent),line1=self.LineOne(noRSL))
				if scraper_links is not None:
					random.shuffle(scraper_links)
					for scraper_link in scraper_links:
						quality = scraper_link.get('quality','')
						self.QuailtyCounter(quality)
						self.QualityString()
						self.List.append(scraper_link)
						self.dp.update(int(Percent),line2=self.LineTwo(),line3= self.line2linksqual)
						self.line2linksqual = ''
			self.ListSortRead(fanart)
			#except:pass
		else:
			selected = self.movie_scraper(title,year,imdb)
			if selected:
				self.WithDialogPlay(selected)



	def tvshow(self,title, show_year, year, season, episode, imdb, tvdb, debrid):
		if self.dialogselect == False:
			self.dp.create(SingleColor('Searching for Season ',self.DialogBoxColor1)+SingleColor(str(season),self.DialogBoxColor2)+SingleColor(' Episode ',self.DialogBoxColor1)+SingleColor(str(episode),self.DialogBoxColor2)+self.DL+SingleColor(title,self.DialogBoxColor1))
			noRSL = len(universalscrapers.relevant_scrapers())
			scraper = self.tv_scraper
			links_scraper = scraper(title, show_year, year, season, episode, imdb, tvdb)
			try:
				for scraper_links in links_scraper():
					if self.dp.iscanceled():
						break 
					self.CoScraper_links +=1
					Percent = float(100.00/noRSL)*self.CoScraper_links
					self.dp.update(int(Percent),line1=self.LineOne(noRSL))
					if scraper_links is not None:
						random.shuffle(scraper_links)
						for scraper_link in scraper_links:
							quality = scraper_link.get('quality','')
							self.QuailtyCounter(quality)
							self.QualityString()
							self.List.append(scraper_link)
							self.dp.update(int(Percent),line2=LineTwo(),line3= self.line2linksqual)
							self.line2linksqual = ''
					self.ListSortRead(fanart)
			except:pass
		else:
			selected = self.tv_scraper(title, show_year, year, season, episode, imdb, tvdb)
			if selected:
				self.WithDialogPlay(selected)
				

	def music(self, title, artist, debrid):
		if self.dialogselect == False:
			self.dp.create(self.SingleColor('Searching for ',self.DialogBoxColor1)+str(SingleColor(title,self.DialogBoxColor2))+SingleColor(' by ',self.DialogBoxColor1)+str(SingleColor(artist,self.DialogBoxColor2)))
			scraper = self.music_scraper
			links_scraper = scraper(title, artist, debrid)

			try:
				for scraper_links in links_scraper():
					if self.dp.iscanceled():
						break
						self.CoScraper_links +=1
					Percent = float(100.00/noRSL)*self.CoScraper_links
					self.dp.update(int(Percent),line1=self.LineOne(noRSL))
					if scraper_links is not None:
						random.shuffle(scraper_links)
						for scraper_link in scraper_links:
							quality = scraper_link.get('quality','')
							self.QuailtyCounter(quality)
							self.QualityString()
							self.List.append(scraper_link)
							self.dp.update(int(Percent),line2=LineTwo(),line3= self.line2linksqual)
							self.line2linksqual = ''
					self.ListSortRead(fanart)
			except:pass
		else:
			selected = self.music_scraper(title,artist,debrid)
			if selected:
				self.WithDialogPlay(selected)

	def ListSortRead(self,fanart):
		self.Dolog(self.List,line_info=True)
		count = 1
		if len(self.List) > 0:
			if self.SortMethod != '':
				List = sorted(List, key=lambda k: k[str(self.SortMethod)],reverse = True)
			for results in self.List:
				playlink = results.get('url','')
				source = results.get('source','')
				quality = results.get('quality','')
				scraper = results.get('scraper','')
				direct = results.get('direct',False)
				title = SingleColor(str(count).ljust(3),_Edit.ItemTxtColor1)+self.DL+SingleColor(str(scraper),_Edit.ItemTxtColor2)+self.DL+SingleColor(source,_Edit.ItemTxtColor1)+self.DL+SingleColor(quality,_Edit.ItemTxtColor2)
				if direct == False:
					playlink,resolved = self.PlayLinkResolve(playlink)
					if resolved == True:
						self.playlist.append({'title':title,'playlink':playlink,'direct':direct})
						count += 1
					else:pass
				elif direct == True:	
					self.playlist.append({'title':title,'playlink':playlink,'direct':direct})
					count += 1
			self.ListDisplay(fanart)

	def WithDialogPlay(self,selected):
		playlink = selected['url']
		direct = selected['direct']
		if direct == False:
			try:
				resolved = resolve(playlink)
				xbmc.Player().play(resolved,xbmcgui.ListItem(title))
			except:
				self.Dolog('Scraper TV show with Dialog Unable to play with resolver '+resolved,line_info=True)
				pass
		elif direct == True:
			try:
				xbmc.Player().play(playlink,xbmcgui.ListItem(title))
			except:
				self.Dolog('Scraper TV Show with Dialog Unable to play direct '+playlink,line_info=True)
				pass

	def ListDisplay(self,fanart):
		self.dp.close()
		for items in self.playlist:
			Name = items.get('title','Data Missing')
			PlayLink = items.get('playlink','')
			direct = items.get('direct','')
			if direct != '':
				self.Icon = self.Icon if self.Icon != None else addon_icon
				if direct == True:
					mode = 12
					BYB.addDir_file(Name.encode('utf-8'),PlayLink,mode,self.Icon,fanart,'','','','')
				elif direct == False:
					mode = 19
					BYB.addDir_file(Name.encode('utf-8'),PlayLink,mode,self.Icon,fanart,'','','','',showcontext='pair',contextmode=106)

	def NameClean(self,name):
		match = re.compile(r'(\[.+?\])').findall(str(name))
		for remove in match:
			name = name.replace(remove,'')
		return name

				 
	def PlayLinkResolve(self,url):
		if setting_resolve == 'resolveurl':
			import resolveurl as RESOLVE
		elif setting_resolve == 'urlresolver':
			import urlresolver as RESOLVE
		hmf = RESOLVE.HostedMediaFile(url)
		if hmf.valid_url() == True:
			#url = hmf.resolve()
			resolved = True
		else:
			resolved = False
		return url,resolved

	def QuailtyCounter(self,quality):
		if 'sd' in quality.lower():
			self.SD += 1
		elif '720' in quality:
			self.p720 +=1
		elif 'dvd' in quality.lower():
			self.DVD +=1
		elif '1080' in quality:
			self.p1080 += 1
		elif 'cam' in quality.lower():
			self.CAM += 1
		elif 'hd' in quality.lower():
			self.HD +=1
		elif '480' in quality:
			self.p480 += 1
		else:
			self.OTHER += 1

	def QualityString(self):
		if self.p1080 > 0:
			self.line2linksqual += SingleColor('1080 ',self.DialogBoxColor1)+SingleColor(str(self.p1080),self.DialogBoxColor2)+self.DL
		if self.HD > 0:
			self.line2linksqual += SingleColor('HD ',self.DialogBoxColor1)+SingleColor(str(self.HD),self.DialogBoxColor2)+self.DL
		if self.DVD >0:
			self.line2linksqual += SingleColor('DVD ',self.DialogBoxColor1)+SingleColor(str(self.DVD),self.DialogBoxColor2)+self.DL
		if self.p720 >0:
			self.line2linksqual += SingleColor('720 ',self.DialogBoxColor1)+SingleColor(str(self.p720),self.DialogBoxColor2)+self.DL
		if self.SD > 0:
			self.line2linksqual += SingleColor('SD ',self.DialogBoxColor1)+SingleColor(str(self.SD),self.DialogBoxColor2)+self.DL
		if self.p480 > 0:
			self.line2linksqual += SingleColor('480 ',self.DialogBoxColor1)+SingleColor(str(self.p480),self.DialogBoxColor2)+self.DL
		if self.CAM > 0:
			self.line2linksqual += SingleColor('CAM ',self.DialogBoxColor1)+SingleColor(str(self.CAM),self.DialogBoxColor2)+self.DL
		if self.OTHER > 0:
			self.line2linksqual += SingleColor('OTHER ',self.DialogBoxColor1)+SingleColor(str(self.OTHER),self.DialogBoxColor2)+self.DL

'''
	def scrape_movie(self, title, year, imdb, debrid = False):

    scrapes scraper site for movie links
    Args:
        title: movie title -> str
        year: year the movie came out -> str
        imdb: imdb identifier -> str
        debrid: boolean indicating whether to use debrid links if available -> bool
    Returns:
        a list of video sources represented by dicts with format:
          {'source': video source (str), 'quality': quality (str), 'scraper': scraper name (str) , 'url': url (str), 'direct': bool}

        pass

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):

    scrapes scraper site for episode links
    Args:
        title: title of the tv show -> str
        show_year: year tv show started -> str
        year: year episode premiered -> str
        season: season number of the episode -> str
        episode: episode number -> str
        imdb: imdb identifier -> str
        tvdb: tvdb identifier -> str
        debrid: boolean indicating whether to use debrid links if available -> bool
    Returns:
        a list of video sources represented by dicts with format:
          {'source': video source (str), 'quality': quality (str), 'scraper': scraper name (str) , 'url': url (str), 'direct': bool}

        pass

    def scrape_music(self, title, artist, debrid = False):

    scrapes scraper site for song links
    Args:
        title: song title -> str
        artist: song artist -> str
        debrid: boolean indicating whether to use debrid links if available -> bool
    Returns:
        a list of music sources represented by dicts with format:
          {'source': music source (str), 'quality': quality (str), 'scraper': scraper name (str) , 'url': url (str), 'direct': bool}

        pass
'''
