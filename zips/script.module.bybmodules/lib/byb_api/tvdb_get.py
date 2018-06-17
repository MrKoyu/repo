


from thetvdb import TheTvDb
from koding import dolog

api_key='12E8AAC46571E4C1'
tvdb = TheTvDb()

Series_info = []
Seasons = []
Season_number = []
Season_Episodes = []
Season_Episode = []
Episode_ID = []


def get_series_info(ID):
	series_info = tvdb.get_series(ID)
	Series_info.append(series_info)
		
'''
tvdb.get_series == {'rating': 7, 'art': {'posters': [u'http://thetvdb.com/banners/posters/79412-1.jpg', u'http://thetvdb.com/banners/posters/79412-2.jpg', u'http://thetvdb.com/banners/posters/79412-3.jpg'], 'banner': u'http://thetvdb.com/banners/graphical/79412-g.jpg', 'poster': u'http://thetvdb.com/banners/posters/79412-1.jpg'}, 'airdaytime.short': u'Fri ', 'airdaytime.label': u'Friday  - Network: Tokyo MX', 'plot': u'Ten years after the Holy War in Hong Kong, Mochizuki Jirou, aka the Silver Blade, and the lone hero who fought and defeated the Kowloon Children despite the loss of his lover, returns to Japan with his young brother, Mochizuki Kotaro. The two quickly discover that the Kowloon Children who survived the Holy War are seeking to infiltrate the \u201cSpecial Zone\u201d\u2014a thriving city protected by an invisible barrier that will not allow Kowloon Children entrance\u2014unless they\u2019re invited. Red Bloods refer to the humans; Black Bloods are the vampires, and the Mochizuki Brothers are Old Blood\u2014the last descendants of an elite clan of vampires. When Kotaro is abducted by one of the Kowloon Children, Jirou has no choice but to fight once more.', 'votes': 12, 'network': u'Tokyo MX', 'airdaytime': u'Friday  (Tokyo MX)', 'airtime': '', 'airday': u'Friday', 'status': u'Ended', 'rating.tvdb': 7, 'tvdb_id': 79412, 'imdbnumber': u'tt0878230', 'studio': [u'Tokyo MX'], 'genre': [u'Action', u'Animation', u'Comedy', u'Fantasy'], 'airdaytime.label.short': u'Fri  - Network: Tokyo MX', 'votes.tvdb': 12, 'airday.short': u'Fri', 'title': u'Black Blood Brothers', 'firstaired': u'2006-09-08', 'runtime': 1500}
'''		
	
def get_seasons(ID):
	series_seasons = tvdb.get_series_episodes(ID)
	for results in series_seasons:
		season = results['airedSeason']
		if season not in Seasons:
			Seasons.append(season)
			Season_number.append({'season_number':season})
			
def get_season_episodes_ID(ID,season):
	series_seasons = tvdb.get_series_episodes(ID)
	for results in series_seasons:
		Season = results['airedSeason']
		episode_ID = results['id']
		if Season == int(season):
			Episode_ID.append(episode_ID)

def get_season_episodes_list():			
	for episode_ID in Episode_ID:
		season_episodes = tvdb.get_episode(episode_ID)
		Season_Episodes.append(season_episodes)

def get_episode(episode_ID):
	season_episodes = tvdb.get_episode(episode_ID)
	Season_Episodes.append(season_episodes)
		
def get_season_episodes(ID,season):
	get_season_episodes_ID(ID,season)
	get_season_episodes_list()
	for Results in Season_Episodes:
		default = ''
		episode_name = Results.get('label',default)
		episode_plot = Results.get('plot',default)
		episode_date = Results.get('airdate',default)
		episode_artwork = Results.get('thumbnail',default)			
		Season_Episode.append({'episode_name':episode_name,'episode_plot':episode_plot,'episode_date':episode_date,'episode_artwork':episode_artwork})
		
'''
tvdb.get_episode = {'rating': 8, 'episode': 12, 'airdate': '24/11/2006', 'title': u'For The Eternity of Our Bloodline, I Devote Everything of This Blood', 'airdate.label': u'1x12. For The Eternity of Our Bloodline, I Devote Everything of This Blood (24/11/2006)', 'season': 1, 'writer': [], 'plot': u"Jirou defeats Cassa, and later on finds out that in the eleventh yard lies the remains of the kowloon king. Then he is told to be Mimiko's guardian. A bit after Jirou tells Mimiko to not tell Kotarou abiout him being the reincarnation of the sage, Eve. Jirou seems to have gotten a job, and they all live happily ever after!", 'label': u'1x12. For The Eternity of Our Bloodline, I Devote Everything of This Blood', 'director': [], 'firstaired': u'2006-11-24', 'gueststars': [], 'art': {}, 'thumbnail': u'http://thetvdb.com/banners/episodes/79412/313907.jpg'}
'''