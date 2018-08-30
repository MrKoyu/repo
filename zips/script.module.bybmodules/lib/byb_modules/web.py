import koding
import re
import webbrowser
import xbmc
import xbmcaddon 
import xbmcgui
from byb_modules import String_Color



def cookie_name_create(url):
	cookie_name =  (url.split('//',1)[1]).split('/',1)[0]
	match = re.compile('[^a-z]').findall(str(cookie_name))
	for items in match:
		cookie_name = cookie_name.replace(str(items),'_')
	return cookie_name
	

# Thanks Bugatsinho for the pairing code
class PairTool():

	def __init__(self,*args,**kwargs):
		self.dialog      = xbmcgui.Dialog()
		self.headercolor = kwargs.get('headercolor')
		self.itemcolor   = kwargs.get('itemcolor')
		self.header      = String_Color(string='{}  Pairing Tool'.format(xbmcaddon.Addon(koding.Caller(my_return='addon')).getAddonInfo('name')),color=self.headercolor) if self.headercolor != None else '{}  Pairing Tool'.format(xbmcaddon.Addon(koding.Caller(my_return='addon')).getAddonInfo('name'))
		self.OpenLoad    = String_Color(string='Open Load',color=self.itemcolor)    if self.itemcolor != None else 'Open Load'
		self.TheVideoMe  = String_Color(string='Viv Io',color=self.itemcolor) if self.itemcolor != None else 'Viv Io'
		self.VidUpMe     = String_Color(string='Vid Up Me',color=self.itemcolor)    if self.itemcolor != None else 'Vid Up Me'
		self.FlashxTV    = String_Color(string='Flashx TV',color=self.itemcolor)    if self.itemcolor != None else 'Flashx TV'
		self.menuoptions()
		


	def menuoptions(self):
		funcs = (
			self.function1,
			self.function2,
			self.function3,
			self.function4
			)
		call = self.dialog.select(self.header, [self.OpenLoad,self.TheVideoMe,self.VidUpMe,self.FlashxTV])
		# dialog.selectreturns
		#   0 -> escape pressed
		#   1 -> first item
		#   2 -> second item
		if call:
			# esc is not pressed
			if call < 0:
				return
			func = funcs[call-4]
			return func()
		else:
			func = funcs[call]
			return func()
		return 

	def platform():
		if xbmc.getCondVisibility('system.platform.android'):
			return 'android'
		elif xbmc.getCondVisibility('system.platform.linux'):
			return 'linux'
		elif xbmc.getCondVisibility('system.platform.windows'):
			return 'windows'
		elif xbmc.getCondVisibility('system.platform.osx'):
			return 'osx'
		elif xbmc.getCondVisibility('system.platform.atv2'):
			return 'atv2'
		elif xbmc.getCondVisibility('system.platform.ios'):
			return 'ios'

	myplatform = platform()

	def function1(self):
		if self.myplatform == 'android': # Android 
			opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://olpair.com/pair' ) )
		else:
			opensite = webbrowser . open('https://olpair.com/pair')

	def function2(self):
		if self.myplatform == 'android': # Android 
			opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://vev.io/pair' ) )
		else:
			opensite = webbrowser . open('https://vev.io/pair')

	def function3(self):
		if self.myplatform == 'android': # Android 
			opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://vidup.me/pair' ) )
		else:
			opensite = webbrowser . open('http://vidup.me/pair')      
		
			
	def function4(self):
		if self.myplatform == 'android': # Android 
			opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://www.flashx.tv/pairing.php' ) )
		else:
			opensite = webbrowser . open('https://www.flashx.tv/pairing.php')



