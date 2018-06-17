import datetime
import dateutil.parser as dparser
import feedparser
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import koding

'''url is url of podcast rss feed
In Items() amount is the number to be returned working on 1 is most recent and working back, not putting a amount = x will return all the podcasts on the rss feed
return is a list of dicts 
Example code
PodcastRss = byb_scrapers.PodcastRss() 
PodcastRss.ItemInfo(url='https://rss.acast.com/thefightingcock',amount=5)
for items in PodcastRss.ITEM:
	title = items['title']
	description = items['description']
	'''  
class PodcastRss():

	CHANNEL = []
	ITEM = []

	def Channel(self,url):
		#pull all the channel information name,description and image
		ParseRSS = feedparser.parse(url)
		feed = ParseRSS.feed
		try:
			image = self._ImageResolve(feed.image)
		except:
			image = ''
		try:
			description = feed.description
		except:
			description = ''
		self.CHANNEL.append({'title':feed.title.encode('utf8'),'description':description.encode('utf8'),'image':image,'rss_url':url})

	def ChannelImage(self,url):
		#function for pulling artwork of channel
		ParseRSS = feedparser.parse(url)
		feed = ParseRSS.feed
		try:
			image = self._ImageResolve(feed.image)
		except:
			image = ''
		return image

	def Items(self,url,amount='all'):
		#pull a set amount of podcasts or all if amount is not determined (podcasts name,image,description,publish date and playlink)  in rss feed 
		ParseRSS = feedparser.parse(url)
		feed = ParseRSS.feed
		entries = ParseRSS.entries
		if str(amount).isdigit():
			amount = int(amount)
			for i in range(amount):
				try:
					image = self._ImageResolve(entries[i].image)
				except:
					image = self._ImageResolve(feed.image)
				playlink = self._PlayLinkResolve(entries[i].links)
				date = self._DateResolve(entries[i].published)
				try:
					description = entries[i].description
					description = HTMLParser().unescape(description)
					description = self._DescriptionClean(description)
				except:
					description = ''
				self.ITEM.append({'title':entries[i].title.encode('utf8'),'image':image,'description':description.encode('utf8'),'date':date,'playlink':playlink})
		elif amount=='all':
			for entry in entries:
				try:
					image = self._ImageResolve(entry.image)
				except:
					image = self._ImageResolve(feed.image) 
				playlink = self._PlayLinkResolve(entry.links)
				date = self._DateResolve(entry.published)
				try:
					description = entry.description
					description = HTMLParser().unescape(description)
					description = self._DescriptionClean(description)
				except:
					description = ''
				self.ITEM.append({'title':entry.title.encode('utf8'),'image':image,'description':description.encode('utf8'),'date':date,'playlink':playlink})
		else:
			pass
			koding.dolog('Podcast RSS Feed Wrong value entered for amount must be int value entered ='+str(amount)+' Url of rss = '+str(url),line_info=True)

	def ItemCount(self,url):
		ParseRSS = feedparser.parse(url)
		feed = ParseRSS.feed
		entries = ParseRSS.entries
		count = len(entries)
		return count 

	def PubDate(self,url,DateFormat='%Y%m%d'):
		# function to return last published date of latest podcast useful if caching the info to a database to save scraping everytime as most are only updated weekly , DateFormat is how you would like the date to be returned default is eg 20180413
		ParseRSS = feedparser.parse(url)
		feed = ParseRSS.feed
		entries = ParseRSS.entries
		try:
			date = feed.published
		except:
			date = entries[0].published
		date = self._DateResolve(date,DateFormat)
		return date

	def _DescriptionClean(self,text):
		soup = BeautifulSoup(text)
		text = soup.get_text()
		return text 

	def _ImageResolve(self,ImageDict):
		#internal function
		im = []
		im.append(ImageDict)
		for Image in im:
			ImageUrl = Image.get('href','')
		return ImageUrl

	def _PlayLinkResolve(self,LinkDict):
		#internal function
		for links in LinkDict:
			link = links.href
			if '.mp3' in link or '.m4a' in link:
				return link

	def _DateResolve(self,Date,DateFormat='%d-%b-%Y'):
		#internal function
		try:
			date = dparser.parse(Date,fuzzy=True)
			date = date.strftime(str(DateFormat))
		except:
			date = ''
		return date

if __name__ == '__main__':
	Test_urls = ['http://feeds.twit.tv/twit.xml',
	'https://rss.acast.com/thefightingcock',
'http://broadandhotspur.buzzsprout.com/78880.rss',
'http://cospurs.com/wp/feed/podcast/',
'http://feeds.soundcloud.com/users/soundcloud:users:142515494/sounds.rss',
'https://rss.acast.com/espurs',
'http://audioboom.com/channels/4902566.rss',
'http://www.spreaker.com/user/7564778/episodes/feed',
'http://rss.acast.com/ruletheroost',
'http://podcast.playbackmedia.co.uk/spurs.xml',
'http://feeds.soundcloud.com/users/soundcloud:users:124425344/sounds.rss',
'http://audioboom.com/channels/4871099.rss',
'http://cartilagefree.podbean.com/feed/']
	for url in Test_urls:
		Count = PodcastRss().ItemCount(url)
		PodcastRss().Items(url)
		PodcastRss().Channel(url)
		pubdate = PodcastRss().PubDate(url)
		print '#######-------CHANNELINFO '+str(url)+'--------#######'
		print PodcastRss.CHANNEL
		del PodcastRss.CHANNEL[:]
		print '######------PUBDATE '+str(url)+'------######'
		print pubdate
		print '######-------Item Count '+str(url)+'------#######'
		print Count
		print '######-------ITEMINFO '+str(url)+'-----######'
		print PodcastRss.ITEM
		del PodcastRss.ITEM[:]



'''https://rss.acast.com/thefightingcock',
'http://broadandhotspur.buzzsprout.com/78880.rss',
'http://cospurs.com/wp/feed/podcast/',
'http://feeds.soundcloud.com/users/soundcloud:users:142515494/sounds.rss',
'https://rss.acast.com/espurs',
'http://audioboom.com/channels/4902566.rss',
'http://www.spreaker.com/user/7564778/episodes/feed',
'http://rss.acast.com/ruletheroost',
'http://podcast.playbackmedia.co.uk/spurs.xml',
'http://feeds.soundcloud.com/users/soundcloud:users:124425344/sounds.rss',
'http://audioboom.com/channels/4871099.rss',
'http://cartilagefree.podbean.com/feed/'''