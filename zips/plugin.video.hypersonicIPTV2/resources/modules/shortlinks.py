import xbmc,xbmcgui,requests
from resources.modules import control,tools


username     = control.setting('Username')
password     = control.setting('Password')
def Get():
	xbmc.executebuiltin("ActivateWindow(busydialog)")
	m3u  = 'http://main.tvstreams.xyz%3A83%2Fget.php%3Fusername%3D'+username+'%26password%3D'+password+'%26type%3Dm3u_plus%26output%3Dts'
	epg  = 'http://main.tvstreams.xyz%3A83%2Fxmltv.php%3Fusername%3D'+username+'%26password%3D'+password
	auth = 'http://main.tvstreams.xyz:83/enigma2.php?username='+username+'&password='+password+'&type=get_vod_categories'
	auth = tools.OPEN_URL(auth)
	if not auth=="":
		request  = 'https://tinyurl.com/create.php?source=indexpage&url='+m3u+'&submit=Make+TinyURL%21&alias='
		xbmc.log(str(request))
		request2 = 'https://tinyurl.com/create.php?source=indexpage&url='+epg+'&submit=Make+TinyURL%21&alias='
		m3u = tools.OPEN_URL(request)
		epg = tools.OPEN_URL(request2)
		xbmc.log(str(epg))
		shortm3u = tools.regex_from_to(m3u,'<div class="indent"><b>','</b>')
		shortepg = tools.regex_from_to(epg,'<div class="indent"><b>','</b>')
		xbmc.executebuiltin("Dialog.Close(busydialog)")
		xbmcgui.Dialog().ok('[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]','[COLOR blue]M3U URL: [/COLOR]%s'%shortm3u,'','[COLOR blue]EPG URL: [/COLOR]%s'%shortepg)
	else:
		return