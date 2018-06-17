import time
import xbmc
import os
import xbmcgui
import urllib2
import webbrowser


def menuoptions():
    dialog = xbmcgui.Dialog()
    funcs = (
        function1,
        function2,
        function3,
		function4,
		function5,
		function6,
		function7,
		function8,
		function9,
		function10,
		function11,
		function12,
		function13,
		function14,
		function15,
		function16,
		function17,
		function18,
		function19,
		function20,
		function21
        )
        
    call = dialog.select('[COLOR forestgreen][B]C[/COLOR][COLOR gold]D[/COLOR][COLOR ghostwhite]T[/COLOR][COLOR mediumblue]V[/B][/COLOR] [COLOR ghostwhite]EASY TO PAIR[/COLOR]', [
	'[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite]      Alluc[/COLOR][/B]', 
    '[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite]      Tmdb[/COLOR][/B]',
    '[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite]      Imdb[/COLOR][/B]',
	'[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite]      Trakt TV[/COLOR][/B]',
	'[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite]      Ororo TV[/COLOR][/B]',
	'[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite]      OpenLoad[/COLOR][/B]',
	'[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite]      The Video Me[/COLOR][/B]',
    '[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite]      Vid Up Me[/COLOR][/B]',
    '[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite]      Streamlord[/COLOR][/B]',
    '[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite]      Moviesplanet TV[/COLOR][/B]',
    '[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite]      vShare.eu[/COLOR][/B]',
    '[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite]      Real-Debrid[/COLOR][/B]',
	'[B][COLOR white]=-=-=-=-=[/COLOR][/B][B][COLOR=gold]  RECOMMENDED  [/COLOR][/B][B][COLOR white]=-=-=-=-=[/COLOR][/B]',
	'[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite]      Kodi Apps[/COLOR][/B]',
	'[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite]      YouTube Channel[/COLOR][/B]',
	'[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite]      Facebook Group[/COLOR][/B]',
	'[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite]      Follow me on Twitter[/COLOR][/B]',
	'[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite]      CellarDoorTV Website[/COLOR][/B]',
	'[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite]      Click here to say thanks to[/COLOR][/B] [COLOR forestgreen][B]C[/COLOR][COLOR gold]D[/COLOR][COLOR ghostwhite]T[/COLOR][COLOR mediumblue]V[/B][/COLOR]',
	'[B][COLOR white]=-=-=-=-=[/COLOR][/B][B][COLOR=gold]  UNLOCK YOUR TV PRO  [/COLOR][/B][B][COLOR white]=-=-=-=-=[/COLOR][/B]',
	'[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][B][COLOR=ghostwhite][B][COLOR steelblue]      Hypersonic[/COLOR][/B] [B][COLOR white]IPTV2[/COLOR][/B]',])
    # dialog.selectreturns
    #   0 -> escape pressed
    #   1 -> first item
    #   2 -> second item
    if call:
        # esc is not pressed
        if call < 0:
            return
        func = funcs[call-21]
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

def function1():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://accounts.alluc.ee' ) )
    else:
        opensite = webbrowser . open('https://accounts.alluc.ee/')

def function2():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://www.themoviedb.org/account/signup' ) )
    else:
        opensite = webbrowser . open('https://www.themoviedb.org/account/signup')
        
def function3():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://m.imdb.com/ap/register?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.imdb.com%2Fap-signin-handler&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=imdb_mobile_web_us&openid.mode=checkid_setup&siteState=eyJvcGVuaWQuYXNzb2NfaGFuZGxlIjoiaW1kYl9tb2JpbGVfd2ViX3VzIiwicmVkaXJlY3RUbyI6Imh0dHA6Ly9tLmltZGIuY29tLz9yZWZfPW1fbG9naW4ifQ&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&&tag=imdbtag_reg-20' ) )
    else:
        opensite = webbrowser . open('https://m.imdb.com/ap/register?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.imdb.com%2Fap-signin-handler&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=imdb_mobile_web_us&openid.mode=checkid_setup&siteState=eyJvcGVuaWQuYXNzb2NfaGFuZGxlIjoiaW1kYl9tb2JpbGVfd2ViX3VzIiwicmVkaXJlY3RUbyI6Imh0dHA6Ly9tLmltZGIuY29tLz9yZWZfPW1fbG9naW4ifQ&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&&tag=imdbtag_reg-20')
		
def function4():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://trakt.tv/join' ) )
    else:
        opensite = webbrowser . open('https://trakt.tv/join')		
		
def function5():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://ororo.tv/en/users/sign_up' ) )
    else:
        opensite = webbrowser . open('https://ororo.tv/en/users/sign_up')
		
def function6():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://olpair.com/' ) )
    else:
        opensite = webbrowser . open('https://olpair.com/')	
				
def function7():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://thevideo.me/pair' ) )
    else:
        opensite = webbrowser . open('https://thevideo.me/pair')

def function8():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://vidup.me/pair' ) )
    else:
        opensite = webbrowser . open('https://vidup.me/pair')

def function9():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://www.streamlord.com/register.html' ) )
    else:
        opensite = webbrowser . open('http://www.streamlord.com/register.html')

def function10():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://www.moviesplanet.tv/register' ) )
    else:
        opensite = webbrowser . open('https://www.moviesplanet.tv/register')

def function11():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://vshare.eu/pair' ) )
    else:
        opensite = webbrowser . open('http://vshare.eu/pair')

def function12():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://real-debrid.com/?id=946756' ) )
    else:
        opensite = webbrowser . open('http://real-debrid.com/?id=946756')		
		
 
def function13(): 0	

def function14():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://kodiapps.com/' ) )
    else:
        opensite = webbrowser . open('https://kodiapps.com/')	

def function15():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://www.youtube.com/user/willondon07/videos' ) )
    else:
        opensite = webbrowser . open('https://www.youtube.com/user/willondon07/videos')	

def function16():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://www.facebook.com/groups/193814617813542/' ) )
    else:
        opensite = webbrowser . open('https://www.facebook.com/groups/193814617813542/')

def function17():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://twitter.com/cellardoortv1?lang=en' ) )
    else:
        opensite = webbrowser . open('https://twitter.com/cellardoortv1?lang=en')

def function18():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://cellardoortv.wordpress.com' ) )
    else:
        opensite = webbrowser . open('https://cellardoortv.wordpress.com')

def function19():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://www.paypal.me/CellarDoorTV' ) )
    else:
        opensite = webbrowser . open('https://www.paypal.me/CellarDoorTV')	
		
def function20(): 0	

def function21():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://hypersonic-tv.com' ) )
    else:
        opensite = webbrowser . open('http://hypersonic-tv.com')		
 
menuoptions()
