# -*- coding: utf-8 -*-
import koding
import os
import resolveurl
import sys
import urllib
import urlparse
import xbmc
import xbmcgui
import xbmcplugin
import xbmc_executebuiltin

def end_of_directory(cache_to_disc=True):
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=cache_to_disc)

#used in resolveurl tester
def get_plugin_url(queries):
    try:
        query = urllib.urlencode(queries)
    except UnicodeEncodeError:
        for k in queries:
            if isinstance(queries[k], unicode):
                queries[k] = queries[k].encode('utf-8')
        query = urllib.urlencode(queries)

    return sys.argv[0] + '?' + query

#used in resolveurl tester
def parse_query(query):
    q = {'mode': 'main'}
    if query.startswith('?'): query = query[1:]
    queries = urlparse.parse_qs(query)
    for key in queries:
        if len(queries[key]) == 1:
            q[key] = queries[key][0]
        else:
            q[key] = queries[key]
    return q

def set_content(content):
    xbmcplugin.setContent(int(sys.argv[1]), content)


class xbmc_player():

	def __init__(self):
		self.f4m = ['.ts','.m3u8','.f4m']
		self.Play = xbmc.Player()
		self.SportdevilToPlay = ('http://sstream.net/','http://mamahd.in','http://cricfree.sc')
		self.f4mToPlay = ('.ts','.m3u8','.f4m')


	def UrlDefine(self,url,name):
		if not url.startswith('http') and not url.startswith('plugin:'):
			url = 'http:{}'.format(url)
		if url.startswith(self.SportdevilToPlay):
			url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url={url}'.format(url=url)
		if url.endswith('.ts'):
			url =  'plugin://plugin.video.f4mTester/?url={url}&amp;streamtype=TSDOWNLOADER&amp;name={name}'.format(url=urllib.quote_plus(url),name=name)
		if url.endswith('.m3u8'):
			url =  'plugin://plugin.video.f4mTester/?url={url}&amp;streamtype=HLSRETRY&amp;name={name}'.format(url=urllib.quote_plus(url),name=name)
		if url.endswith('.f4m'):
			url = 'plugin://plugin.video.f4mTester/?url={url}&amp;name={name}'.format(url=urllib.quote_plus(url),name=name)
		if '|' in url and any(x in url for x in self.f4m):
			_url = url.split('|')[0]
			if _url.endswith('.ts'):
				url =  'plugin://plugin.video.f4mTester/?url={url}&amp;streamtype=TSDOWNLOADER&amp;name={name}'.format(url=urllib.quote_plus(url),name=name)
			if _url.endswith('.m3u8'):
				url =  'plugin://plugin.video.f4mTester/?url={url}&amp;streamtype=HLSRETRY&amp;name={name}'.format(url=urllib.quote_plus(url),name=name)
			if _url.endswith('.f4m'):
				url = 'plugin://plugin.video.f4mTester/?url={url}&amp;name={name}'.format(url=urllib.quote_plus(url),name=name)
		else:
			url = url
		koding.dolog('UrlDefine= {}'.format(url),line_info=True)
		return url

	def PlayMethod(self,url):
		if url.startswith('plugin://plugin'):
			playmethod='plugin'
		elif url.startswith('http'):
			playmethod = 'http'
		else:
			xbmc_executebuiltin.Notify(message='url format not correct',times=5000)
			koding.dolog('url format not correct %s'%url,line_info=True)
			playmethod = 'false'
		koding.dolog('PlayMethod = %s  %s'%(playmethod,url),line_info=True)
		return url,playmethod

	def pluginplay(self,url,name):
		try:
			xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
		except:pass
		try:
			liz = xbmcgui.ListItem(name, iconImage=iconimage)
			liz.setInfo(type='Video', infoLabels={'Title':name})
			self.Play.play(url,liz)
		except:pass

	def httpplay(self,url,name):
		liz = xbmcgui.ListItem(name)
		liz.setInfo(type='Video', infoLabels={'Title':name})
		hmf = resolveurl.HostedMediaFile(url)
		koding.dolog('resolveurl HostedMediaFile = %s'%hmf.valid_url(),line_info=True)
		if hmf.valid_url() == True:
			try:
				stream_url = hmf.resolve()
			except Exception as e:
				koding.dolog('{} {}'.format(url,e),line_info=True)
				xbmc_executebuiltin.Notify('{}'.format(e),times=5000 )
				return
		else:
			stream_url=url
		try:
			xbmc.Player().play(stream_url,liz)
		except Exception as e:
			koding.dolog('{} {}'.format(url,e),line_info=True)
			xbmc_executebuiltin.Notify('{}'.format(e),times=5000 )
			return

	def play(self,url,name=''):
		if name == '':
			name = url 
		url = xbmc_player().UrlDefine(url)
		url,playmethod = xbmc_player().PlayMethod(url)
		if not playmethod == 'false':
			if playmethod == 'plugin':
				koding.dolog('plugin PlayMethod = %s  %s'%(playmethod,url),line_info=True)
				xbmc_player().pluginplay(url)
			elif playmethod == 'http':
				koding.dolog('http PlayMethod = %s  %s'%(playmethod,url),line_info=True)
				xbmc_player().httpplay(url,name)
			else:
				xbmc_executebuiltin.Notify(message='PlayMethod not correct',times=5000)
				koding.dolog('PlayMethod not correct  %s'%url,line_info=True)
				pass
		else:pass 


def ReadXbmcLog():
	kodi_log = open(os.path.join(xbmc.translatePath('special://home/'),'kodi.log'))
	text     = kodi_log.read()
	return text


def KeyBoard(msg,default=''):
	text = ''
	kb = xbmc.Keyboard()
	kb.setDefault(default)
	kb.setHeading(msg)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
	return text


def KeyBoardNumeric(Type,msg):
	'''	Param	Name	Format
		0	ShowAndGetNumber	(default format: #)
		1	ShowAndGetDate	(default format: DD/MM/YYYY)
		2	ShowAndGetTime	(default format: HH:MM)
		3	ShowAndGetIPAddress	(default format: #.#.#.#)
	'''
	dialog = xbmcgui.Dialog()
	number_string = dialog.numeric(Type,msg)
	return number_string
