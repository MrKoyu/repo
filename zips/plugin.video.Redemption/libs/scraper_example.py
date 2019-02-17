import byb_modules as BYB
from ._addon import *
from ._common import *
from HTMLParser import HTMLParser

if      setting_resolve     == "resolveurl":                                            import resolveurl as RESOLVE
elif    setting_resolve     == "urlresolver" and hasaddon('script.module.urlresolver'):  import urlresolver as RESOLVE
else:
    setting_set('resolverURL','resolveurl')     
    import resolveurl as RESOLVE

def index():
	BYB.addDir(ChannelColor('RetroClassic Movies'),'',901,'https://i.pinimg.com/originals/4e/bf/1b/4ebf1bccb1c6d456ef934f39412a7aff.png',addon_fanart,'','','','')


def retroclassic():
	#call scraper from folder
	from .scrapers import retrovision
	#run scraper
	retrovision.all_movies()
	#return list of dicts from scraper
	for items in retrovision.ReturnList:
		#HTMLPareser cleans up any text that is still in html code
		Description = HTMLParser().unescape(items.get('description',''))
		Description = Description.encode('utf-8')
		BYB.addDir_file(ItemColor(items.get('title','')),items.get('playlink',''),902,items.get('icon',''),addon_fanart,Description,'','','')
	del retrovision.ReturnList[:]


def Play(url):
	Play = xbmc.Player()
	host = RESOLVE.HostedMediaFile(url)
	ValidUrl = host.valid_url()
	if ValidUrl == True :
		playlink = RESOLVE.resolve(url)
	else:
		playlink = url
	try:
		Play.play(playlink)
	except:pass
