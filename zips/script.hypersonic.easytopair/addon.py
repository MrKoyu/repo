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
        
    call = dialog.select('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR] Easy To Pair[/COLOR]', [
	'[B][COLOR white]=-=-=-=-=[/COLOR][/B][B][COLOR=gold]  FREE 24hs TRIAL  [/COLOR][/B][B][COLOR white]=-=-=-=-=[/COLOR][/B]',
	'[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][COLOR=ghostwhite]      Subscribe For a Free 24hs Weekday Trial[/COLOR]',
	'[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR][COLOR=ghostwhite]      Hypersonic IPTV2 Packages[/COLOR]',
	'[B][COLOR white]=-=-=-=-=[/COLOR][/B][B][COLOR=gold]  UNLOCK YOUR TV PRO  [/COLOR][/B][B][COLOR white]=-=-=-=-=[/COLOR][/B]',
	'[COLOR forestgreen][B]*[/COLOR][COLOR gold]*[/COLOR][COLOR ghostwhite]*[/COLOR][COLOR mediumblue]*[/B][/COLOR]      [COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR] Website',])
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
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( '' ) )
    else:
        opensite = webbrowser . open('')

def function2():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://getnow.hypersonic-tv.com/home/freetrial' ) )
    else:
        opensite = webbrowser . open('http://getnow.hypersonic-tv.com/home/freetrial')
        
def function3():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://getnow.hypersonic-tv.com/home/pricing' ) )
    else:
        opensite = webbrowser . open('http://getnow.hypersonic-tv.com/home/pricing')
		
def function4():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( '' ) )
    else:
        opensite = webbrowser . open('')		
		
def function5():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://getnow.hypersonic-tv.com' ) )
    else:
        opensite = webbrowser . open('http://getnow.hypersonic-tv.com')
		
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
        opensite = webbrowser . open('http://getnow.hypersonic-tv.com/home/freetrial')	

def function15():
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( '' ) )
    else:
        opensite = webbrowser . open('http://getnow.hypersonic-tv.com/home/pricing')	

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
