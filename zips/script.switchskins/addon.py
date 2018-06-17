###################################################################################
#(_)                                                                              #
# |________________________________________________                               #
# |*  *  *  *  *  *  * |##########################|                               #
# | *  *  *  *  *  *  *|==========================|                               #
# |*  *  *  *  *  *  * |##########################|                               #
# | *  *  *  *  *  *  *|==========================|                               #
# |*  *  *  *  *  *  * |##########################|      If your going to copy    #
# | *  *  *  *  *  *  *|==========================|         this addon just       #
# |*  *  *  *  *  *  * |##########################|         give credit!!!!       #
# |--------------------|==========================|                               #
# |###############################################|                               #
# |===============================================|                               #
# |###############################################|                               #
# |===============================================|                               #
# |###############################################|                               #
# |-----------------------------------------------|                               #
# |                                                                               #
# |    Pairing Add-on                                                             #
# |    Copyright (C) 2017 FTG                                                     #
# |                                                                               #
# |    This program is free software: you can redistribute it and/or modify       #
# |    it under the terms of the GNU General Public License as published by       #
# |    the Free Software Foundation, either version 3 of the License, or          #
# |    (at your option) any later version.                                        #
# |                                                                               #
# |    This program is distributed in the hope that it will be useful,            #
# |    but WITHOUT ANY WARRANTY; without even the implied warranty of             #
# |    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
# |    GNU General Public License for more details.                               #
# |                                                                               #
###################################################################################
#                                                                                 #
#                          Do not DELETE the credits file!!!                      #
#                                                                                 #
###################################################################################

import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys,random,urllib2,urllib,glob,re

ADDON_ID       = 'script.switchskins'
fanart         = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID , 'fanart.jpg'))
icon           = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'icon.png'))
HOME           = xbmc.translatePath('special://home/')
ADDONS         = os.path.join(HOME,      'addons')
USERDATA       = os.path.join(HOME,      'userdata')
ADDOND         = os.path.join(USERDATA,  'addon_data')
DIALOG         = xbmcgui.Dialog()

def MainMenu():
	addItem('Current Skin -- %s' % currSkin(),'url','',icon,fanart,'')
	addItem('------Auto Mode Below-------','url','',icon,fanart,'')
	addItem('Choose Skin ','url',1,icon,fanart,'')
	addItem('------Manual Modes Below-------','url','',icon,fanart,'')
	addItem('Confluence','url',2,icon,fanart,'')
	addItem('Estuary','url',3,icon,fanart,'')
	addItem('Estouchy','url',4,icon,fanart,'')
        addItem('Aeonmq7','url',5,icon,fanart,'')
        addItem('Aeonmq7.Krypton.mod','url',6,icon,fanart,'')
        addItem('Aeonmq8','url',7,icon,fanart,'')
	addItem('Aeon Nox ','url',8,icon,fanart,'')
	addItem('Aeon Nox Silvo','url',9,icon,fanart,'')
	addItem('Amber','url',10,icon,fanart,'')
	addItem('Apple TV','url',11,icon,fanart,'')
	addItem('Arctic.Zephyr','url',12,icon,fanart,'')
        addItem('Arctic.Zephyr.plus','url',13,icon,fanart,'')
	addItem('Bello 6','url',14,icon,fanart,'')
        addItem('Bello.6.nero','url',15,icon,fanart,'')
        addItem('Bello.6.sonar','url',16,icon,fanart,'')
	addItem('Black Glass','url',17,icon,fanart,'')
	addItem('Box','url',18,icon,fanart,'')
	addItem('Chroma','url',19,icon,fanart,'')
	addItem('Eminence 2','url',20,icon,fanart,'')
	addItem('FTV Skin','url',21,icon,fanart,'')
	addItem('Fuse Neue','url',22,icon,fanart,'')
	addItem('Grid','url',23,icon,fanart,'')
	addItem('Horizon','url',24,icon,fanart,'')
        addItem('Konfluence','url',25,icon,fanart,'')
	addItem('Metropolis','url',26,icon,fanart,'')
	addItem('Mimic','url',27,icon,fanart,'')
	addItem('Nebula','url',28,icon,fanart,'')
	addItem('Omni','url',29,icon,fanart,'')
	addItem('Pellucid','url',30,icon,fanart,'')
	addItem('Phenomenal','url',31,icon,fanart,'')
	addItem('Raiper','url',32,icon,fanart,'')
	addItem('Revolve','url',33,icon,fanart,'')
	addItem('Titan','url',34,icon,fanart,'')
	addItem('Transparency','url',35,icon,fanart,'')
	addItem('Unity','url',36,icon,fanart,'')
	addItem('Xperience 1080','url',37,icon,fanart,'')
        addItem('Xonfluence','url',38,icon,fanart,'')
        addItem('Xonfluence.mod','url',39,icon,fanart,'')

#Example how to add more Skins
#addItem('Skin Name','url',5,icon,fanart,'') The number will be the mode at the bottom
#addItem('Skin Name','url',6,icon,fanart,'') The number will be the mode at the bottom

def skinWIN():
	idle()
	fold = glob.glob(os.path.join(ADDONS, 'skin*'))
	addonnames = []; addonids = []
	for folder in sorted(fold, key = lambda x: x):
		foldername = os.path.split(folder[:-1])[1]
		xml = os.path.join(folder, 'addon.xml')
		if os.path.exists(xml):
			f      = open(xml)
			a      = f.read()
			match  = parseDOM(a, 'addon', ret='id')
			addid  = foldername if len(match) == 0 else match[0]
			try: 
				add = xbmcaddon.Addon(id=addid)
				addonnames.append(add.getAddonInfo('name'))
				addonids.append(addid)
			except:
				pass
	selected = []; choice = 0
	skin = ["Current Skin -- %s" % currSkin()] + addonnames
	choice = DIALOG.select("Select the Skin you want to swap with.", skin)
	if choice == -1: return
	else: 
		choice1 = (choice-1)
		selected.append(choice1)
		skin[choice] = "%s" % ( addonnames[choice1])
	if selected == None: return
	for addon in selected:
		swapSkins(addonids[addon])

def currSkin():
	return xbmc.getSkinDir('Container.PluginName')

def swapSkins(skin, title="Error"):
	old = 'lookandfeel.skin'
	value = skin
	current = getOld(old)
	new = old
	setNew(new, value)
	x = 0
	while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 100:
		x += 1
		xbmc.sleep(100)
	if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
		xbmc.executebuiltin('SendClick(11)')
	return True

def getOld(old):
	try:
		old = '"%s"' % old 
		query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":%s}, "id":1}' % (old)
		response = xbmc.executeJSONRPC(query)
		response = simplejson.loads(response)
		if response.has_key('result'):
			if response['result'].has_key('value'):
				return response ['result']['value'] 
	except:
		pass
	return None

def setNew(new, value):
	try:
		new = '"%s"' % new
		value = '"%s"' % value
		query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (new, value)
		response = xbmc.executeJSONRPC(query)
	except:
		pass
	return None

def idle():
	return xbmc.executebuiltin('Dialog.Close(busydialog)')

def parseDOM(html, name=u"", attrs={}, ret=False):
	# Copyright (C) 2010-2011 Tobias Ussing And Henrik Mosgaard Jensen

	if isinstance(html, str):
		try:
			html = [html.decode("utf-8")]
		except:
			html = [html]
	elif isinstance(html, unicode):
		html = [html]
	elif not isinstance(html, list):
		return u""

	if not name.strip():
		return u""

	ret_lst = []
	for item in html:
		temp_item = re.compile('(<[^>]*?\n[^>]*?>)').findall(item)
		for match in temp_item:
			item = item.replace(match, match.replace("\n", " "))

		lst = []
		for key in attrs:
			lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=[\'"]' + attrs[key] + '[\'"].*?>))', re.M | re.S).findall(item)
			if len(lst2) == 0 and attrs[key].find(" ") == -1:
				lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=' + attrs[key] + '.*?>))', re.M | re.S).findall(item)

			if len(lst) == 0:
				lst = lst2
				lst2 = []
			else:
				test = range(len(lst))
				test.reverse()
				for i in test:
					if not lst[i] in lst2:
						del(lst[i])

		if len(lst) == 0 and attrs == {}:
			lst = re.compile('(<' + name + '>)', re.M | re.S).findall(item)
			if len(lst) == 0:
				lst = re.compile('(<' + name + ' .*?>)', re.M | re.S).findall(item)

		if isinstance(ret, str):
			lst2 = []
			for match in lst:
				attr_lst = re.compile('<' + name + '.*?' + ret + '=([\'"].[^>]*?[\'"])>', re.M | re.S).findall(match)
				if len(attr_lst) == 0:
					attr_lst = re.compile('<' + name + '.*?' + ret + '=(.[^>]*?)>', re.M | re.S).findall(match)
				for tmp in attr_lst:
					cont_char = tmp[0]
					if cont_char in "'\"":
						if tmp.find('=' + cont_char, tmp.find(cont_char, 1)) > -1:
							tmp = tmp[:tmp.find('=' + cont_char, tmp.find(cont_char, 1))]

						if tmp.rfind(cont_char, 1) > -1:
							tmp = tmp[1:tmp.rfind(cont_char)]
					else:
						if tmp.find(" ") > 0:
							tmp = tmp[:tmp.find(" ")]
						elif tmp.find("/") > 0:
							tmp = tmp[:tmp.find("/")]
						elif tmp.find(">") > 0:
							tmp = tmp[:tmp.find(">")]

					lst2.append(tmp.strip())
			lst = lst2
		else:
			lst2 = []
			for match in lst:
				endstr = u"</" + name

				start = item.find(match)
				end = item.find(endstr, start)
				pos = item.find("<" + name, start + 1 )

				while pos < end and pos != -1:
					tend = item.find(endstr, end + len(endstr))
					if tend != -1:
						end = tend
					pos = item.find("<" + name, pos + 1)

				if start == -1 and end == -1:
					temp = u""
				elif start > -1 and end > -1:
					temp = item[start + len(match):end]
				elif end > -1:
					temp = item[:end]
				elif start > -1:
					temp = item[start + len(match):]

				if ret:
					endstr = item[end:item.find(">", item.find(endstr)) + 1]
					temp = match + temp + endstr

				item = item[item.find(temp, item.find(match)) + len(temp):]
				lst2.append(temp)
			lst = lst2
		ret_lst += lst

	return ret_lst

def addItem(name, url, mode, iconimage, fanart, description=None):
	if description == None: description = ''
	description = '[COLOR white]' + description + '[/COLOR]'
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
	liz.setProperty( "fanart_Image", fanart )
	liz.setProperty( "icon_Image", iconimage )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def get_params():
		param=[]
		paramstring=sys.argv[2]
		if len(paramstring)>=2:
				params=sys.argv[2]
				cleanedparams=params.replace('?','')
				if (params[len(params)-1]=='/'):
						params=params[0:len(params)-2]
				pairsofparams=cleanedparams.split('&')
				param={}
				for i in range(len(pairsofparams)):
						splitparams={}
						splitparams=pairsofparams[i].split('=')
						if (len(splitparams))==2:
								param[splitparams[0]]=splitparams[1]
								
		return param

params=get_params(); name=None; url=None; mode=None; iconimage=None; fanartimage=None
try: name=urllib.unquote_plus(params["name"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: fanartimage=urllib.quote_plus(params["fanartimage"])
except: pass

if mode is None or url is None or len(url)<1: 
	MainMenu()#change to skinWIN() to open select window automaticly
elif mode==1:skinWIN()
elif mode==2:swapSkins('skin.confluence')
elif mode==3:swapSkins('skin.estuary')
elif mode==4:swapSkins('skin.estouchy')
elif mode==5:swapSkins('skin.aeonmq7')
elif mode==6:swapSkins('skin.aeonmq7.Krypton.mod')
elif mode==7:swapSkins('skin.aeonmq8')
elif mode==8:swapSkins('skin.aeon.nox.5')
elif mode==9:swapSkins('skin.aeon.nox.silvo')
elif mode==10:swapSkins('skin.amber')
elif mode==11:swapSkins('skin.apptv')
elif mode==12:swapSkins('skin.arctic.zephyr')
elif mode==13:swapSkins('skin.arctic.zephyr.plus')
elif mode==14:swapSkins('skin.bello.6')
elif mode==15:swapSkins('skin.bello.6.nero')
elif mode==16:swapSkins('skin.bello.6.sonar')
elif mode==17:swapSkins('skin.blackglassnova')
elif mode==18:swapSkins('skin.box')
elif mode==19:swapSkins('skin.chroma')
elif mode==20:swapSkins('skin.eminence.2')
elif mode==21:swapSkins('skin.ftv')
elif mode==22:swapSkins('skin.fuse.neue')
elif mode==23:swapSkins('skin.grid')
elif mode==24:swapSkins('skin.horizon')
elif mode==25:swapSkins('skin.konfluence')
elif mode==26:swapSkins('skin.metropolis')
elif mode==27:swapSkins('skin.mimic')
elif mode==28:swapSkins('skin.nebula')
elif mode==29:swapSkins('skin.omni')
elif mode==30:swapSkins('skin.pellucid')
elif mode==31:swapSkins('skin.phenomenal')
elif mode==32:swapSkins('skin.rapier')
elif mode==33:swapSkins('skin.revolve')
elif mode==34:swapSkins('skin.titan')
elif mode==35:swapSkins('skin.transparency')
elif mode==36:swapSkins('skin.unity')
elif mode==37:swapSkins('skin.xperience1080')
elif mode==38:swapSkins('skin.xonfluence')
elif mode==39:swapSkins('skin.xonfluence.mod')

# How to add more modes 
#elif mode==4:swapSkins('Exact skin folder')
#elif mode==5:swapSkins('Exact skin folder')
xbmcplugin.endOfDirectory(int(sys.argv[1]))

