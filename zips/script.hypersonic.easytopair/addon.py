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
        
    call = dialog.select('[COLOR steelblue]Hypersonic[/COLOR] [COLOR white]TV[/COLOR] [COLOR steelblue]Portal[/COLOR]', [
	'[COLOR deepskyblue]* [/COLOR] [COLOR white]Packages & Prices[/COLOR]',
	'[COLOR deepskyblue]* [/COLOR] [COLOR white]Request Trial[/COLOR]',
	'[COLOR deepskyblue]* [/COLOR] [COLOR white]Channel List[/COLOR]',
    '[COLOR deepskyblue]* [/COLOR] [COLOR white]Official Website[/COLOR]',
	'[COLOR deepskyblue]* [/COLOR] [COLOR white]Install Hypersonic apk[/COLOR]',])
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
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://subscribe.hypersonic-tv.com/home/pricing' ) )
    else:
        opensite = webbrowser . open('https://subscribe.hypersonic-tv.com/home/pricing')

def function2():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://subscribe.hypersonic-tv.com/home/trial' ) )
    else:
        opensite = webbrowser . open('https://subscribe.hypersonic-tv.com/home/trial')
        
def function3():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://subscribe.hypersonic-tv.com/home/channel' ) )
    else:
        opensite = webbrowser . open('https://subscribe.hypersonic-tv.com/home/channel')
		
def function4():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://hypersonic-tv.com' ) )
    else:
        opensite = webbrowser . open('http://hypersonic-tv.com')		
		
def function5():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://hypersonic-tv.com/hypersonic.apk' ) )
    else:
        opensite = webbrowser . open('http://hypersonic-tv.com/hypersonic.apk')
		
def function6():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( '' ) )
    else:
        opensite = webbrowser . open('')	
				
def function7():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( '' ) )
    else:
        opensite = webbrowser . open('')

def function8():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( '' ) )
    else:
        opensite = webbrowser . open('')

def function9():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( '' ) )
    else:
        opensite = webbrowser . open('')

def function10():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( '' ) )
    else:
        opensite = webbrowser . open('')

def function11():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( '' ) )
    else:
        opensite = webbrowser . open('')

def function12():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( '' ) )
    else:
        opensite = webbrowser . open('')		
		
 
def function13(): 0	

def function14():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( '' ) )
    else:
        opensite = webbrowser . open('')	

def function15():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( '' ) )
    else:
        opensite = webbrowser . open('')	

def function16():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( '' ) )
    else:
        opensite = webbrowser . open('')

def function17():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( '' ) )
    else:
        opensite = webbrowser . open('')

def function18():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( '' ) )
    else:
        opensite = webbrowser . open('')

def function19():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( '' ) )
    else:
        opensite = webbrowser . open('')	
		
def function20(): 0	

def function21():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( '' ) )
    else:
        opensite = webbrowser . open('')		
 
menuoptions()
