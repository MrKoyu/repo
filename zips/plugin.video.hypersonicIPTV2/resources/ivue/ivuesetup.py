# -*- coding: utf-8 -*-

# Deleting this file cripples the entire addon

#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
# http://kodi.wiki/view/How-to:Write_Python_Scripts
################################################

import urllib2,xbmc,xbmcgui,os,shutil,zipfile,re,string,time
import datetime
from resources.modules import control
from resources.modules import downloader
from resources.modules import tools


username     =  control.setting('Username')
password     =  control.setting('Password')
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ini          =  xbmc.translatePath(os.path.join('special://home/addons/plugin.video.hypersonicIPTV2/resources/ivue','addons_index.ini'))
drxini          =  xbmc.translatePath(os.path.join('special://home/addons/plugin.video.hypersonicIPTV2/resources/ivue','addons2.ini.ini'))
inizip       = 	xbmc.translatePath(os.path.join('special://home/addons/plugin.video.hypersonicIPTV2/resources/ivue','addons_index.zip'))
tmpini       =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ivuetarget   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.ivueguide/'))
ivueaddons2ini   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.ivueguide/addons2.ini'))
ivuecreate   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.IVUEcreator/'))
ivuecreateini   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.IVUEcreator/addons_index.ini'))
ivuecreateini2   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.IVUEcreator/custom_channels.ini'))
iVue_SETTINGS = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.ivueguide','settings.xml'))
UseriVueSets = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.ivueguide','oldsettings.xml'))
iVueSet = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.hypersonicIPTV2/resources/ivue','ivuesettings.xml'))
iVueFold = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.hypersonicIPTV2/resources/ivue'))
iVue_DATA = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.ivueguide/'))

V_drxskinpath = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.ivueguide/resources/skins/'))
V_drxskin = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.ivueguide/resources/skins/Hypersonic TV'))
V_drxaddons2ini = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.ivueguide','addons2.ini'))
V_drxcatini = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.ivueguide','categories.ini'))
V_drxsetxml = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.ivueguide','settings.xml'))



path_to_channels = xbmc.translatePath('special://profile/addon_data/script.ivueguide/amylist.xml')
timeshift = xbmc.translatePath('special://profile/addon_data/script.ivueguide/timezone.ini')
shifttime     = control.setting('shift.time')
realamylist = "http://ivuetvguide.com/ivueguide/amylist.zip"


if shifttime == "0":
	shifttime = "-1:00"
if shifttime == "1":
	shifttime = "-2:00"
if shifttime == "2":
	shifttime = "-3:00"
if shifttime == "3":
	shifttime = "-4:00"
if shifttime == "4":
	shifttime = "-5:00"
if shifttime == "5":
	shifttime = "-6:00"
if shifttime == "6":
	shifttime = "-7:00"
if shifttime == "7":
	shifttime = "-8:00"
if shifttime == "8":
	shifttime = "-9:00"
if shifttime == "9":
	shifttime = "-10:00"
if shifttime == "10":
	shifttime = "-11:00"
if shifttime == "11":
	shifttime = "-12:00"
if shifttime == "12":
	shifttime = "+12:00"
if shifttime == "13":
	shifttime = "+11:00"
if shifttime == "14":
	shifttime = "+10:00"
if shifttime == "15":
	shifttime = "+9:00"
if shifttime == "16":
	shifttime = "+8:00"
if shifttime == "17":
	shifttime = "+7:00"
if shifttime == "18":
	shifttime = "+6:00"
if shifttime == "19":
	shifttime = "+5:00"
if shifttime == "20":
	shifttime = "+4:00"
if shifttime == "21":
	shifttime = "+3:00"
if shifttime == "22":
	shifttime = "+2:00"
if shifttime == "23":
	shifttime = "+1:00"

	


def iVueInt2():
	xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
	xbmc.executebuiltin('RunAddon(plugin.video.hypersonicIPTV2)')
	xbmc.executebuiltin("ActivateWindow(busydialog)")
	dp = xbmcgui.DialogProgress()
	dp.create("[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]","Setting up iVue",'', 'Please Wait')


	if not os.path.exists(iVue_DATA):
		os.makedirs(iVue_DATA)
		
	if os.path.isfile(V_drxaddons2ini):	
		os.remove(V_drxaddons2ini)

	if os.path.isfile(iVue_SETTINGS):
		os.remove(iVue_SETTINGS)
		
	if os.path.isfile(V_drxcatini):
		os.remove(V_drxcatini)
		
	if os.path.isfile(timeshift):	
		os.remove(timeshift)
		

	dp.create("[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]","Locating Files",'', 'Please Wait')
	amylist_install('amylist.xml',realamylist)
	downloader.download(drxsetxml, V_drxsetxml, dp)	
	downloader.download(drxaddons2ini, V_drxaddons2ini, dp)
	downloader.download(drxcatini, V_drxcatini, dp)
	
	#if os.path.isfile(V_drxskin):
		#os.remove(V_drxskin)
		
	#drxskin_install('Durex_TV',drxskins)
		
	dp.create("[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]","Adding Information",'', 'Please Wait')
	a = open(V_drxaddons2ini).read()
	b = a.replace('<HypersonicIPTV2UN>',username).replace('<HypersonicIPTV2PW>',password)
	f = open(V_drxaddons2ini, mode='w')
	f.write(str(b))
	f.close()
	
	alist = []
	shift = []
	z = open(path_to_channels).read()
	all_chan = tools.regex_get_all(z,'<channel id="','</channel>')
	for a in all_chan:
		amychannel = tools.regex_from_to(a,'<display-name lang="en">','</display-name>')
		alist.append(amychannel)
		alist.sort()
		
	for e in alist:
		line = '%s = %s\n'%(e,shifttime)
		shift.append(line)
		
		
	for g in shift:
		l = open(timeshift, mode='a')
		l.write(g)

	xbmc.executebuiltin("Dialog.Close(busydialog)")
		

def iVueInt():
	xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
	xbmc.executebuiltin('RunAddon(plugin.video.hypersonicIPTV2)')
	xbmc.executebuiltin("ActivateWindow(busydialog)")
	dp = xbmcgui.DialogProgress()
	dp.create("[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]","Copying ini",'', 'Please Wait')
	
	if not os.path.isfile(ivuecreateini):
		if not os.path.exists(ivuecreate):
			os.makedirs(ivuecreate)
	shutil.copyfile(ini, ivuecreateini)	
	
	if not os.path.isfile(ivuecreateini2):
		if not os.path.exists(ivuecreate):
			os.makedirs(ivuecreate)
	shutil.copyfile(ini, ivuecreateini2)	
	
	
	a = open(ivuecreateini).read()
	b = a.replace('<HypersonicIPTV2UN>',username).replace('<HypersonicIPTV2PW>',password)
	f = open(ivuecreateini, mode='w')
	f.write(str(b))
	f.close()
		
	if not xbmc.getCondVisibility('System.HasAddon(script.ivueguide)'):
		install('iVue','https://raw.githubusercontent.com/totaltec2014/ivue2/master/script.ivueguide/script.ivueguide-3.0.3.zip')
		install('iVue','https://raw.githubusercontent.com/totaltec2014/ivue2/master/xbmc.repo.ivueguide/xbmc.repo.ivueguide-0.0.1.zip')
		xbmc.executebuiltin("UpdateAddonRepos")
		xbmc.executebuiltin("UpdateLocalAddons")
		time.sleep(5)

	if not xbmc.getCondVisibility('System.HasAddon(xbmc.repo.ivueguide)'):
		install('iVue','https://raw.githubusercontent.com/totaltec2014/ivue2/master/xbmc.repo.ivueguide/xbmc.repo.ivueguide-0.0.1.zip')
		xbmc.executebuiltin("UpdateAddonRepos")
		xbmc.executebuiltin("UpdateLocalAddons")
		time.sleep(5)
		
	if os.path.isfile(ivueaddons2ini):
		os.remove(ivueaddons2ini)

	if not os.path.isfile(iVue_SETTINGS):
		if not os.path.exists(iVue_DATA):
			os.makedirs(iVue_DATA)
		shutil.copyfile(iVueSet, iVue_SETTINGS)
	else:
		os.remove(iVue_SETTINGS)
		xbmc.log('Old iVue settings deleted')
		if not os.path.exists(iVue_DATA):
			os.makedirs(iVue_DATA)
		shutil.copyfile(iVueSet, iVue_SETTINGS)
	xbmc.executebuiltin("Dialog.Close(busydialog)")
	
	
	
def unzip(_in, _out, dp):
	__in = zipfile.ZipFile(_in,  'r')
	
	nofiles = float(len(__in.infolist()))
	count   = 0
	
	try:
		for item in __in.infolist():
			count += 1
			update = (count / nofiles) * 100
			
			if dp.iscanceled():
				dialog = xbmcgui.Dialog()
				dialog.ok(AddonTitle, 'Process was cancelled.')
				
				sys.exit()
				dp.close()
			
			try:
				dp.update(int(update))
				__in.extract(item, _out)
			
			except Exception, e:
				print str(e)

	except Exception, e:
		print str(e)
		return False
		
	return True	
	
def amylist_install(name,url):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]","Installing Channel List...",'', 'Please Wait')
    lib=os.path.join(path, 'amylist.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = iVue_DATA
    time.sleep(3)
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]","Installing Channel List...",'', 'Please Wait')
    dp.update(0,"", "Installing Channel List... Please Wait")
    unzip(lib,addonfolder,dp)
    
def drxskin_install(name,url):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]","Installing Skin...",'', 'Please Wait')
    lib=os.path.join(path, 'Hypersonic_TV.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = V_drxskinpath
    time.sleep(3)
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]","Installing Skin...",'', 'Please Wait')
    dp.update(0,"", "Installing Skin... Please Wait")
    unzip(lib,addonfolder,dp)
    
def install(name,url):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]","Installing iVue TV Guide...",'', 'Please Wait')
    lib=os.path.join(path, 'content.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://home','addons'))
    time.sleep(3)
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR steelblue]Hypersonic [COLOR white]IPTV2[/COLOR]","Installing iVue TV Guide...",'', 'Please Wait')
    dp.update(0,"", "Installing iVue TV Guide... Please Wait")
    print '======================================='
    print addonfolder
    print '======================================='
    unzip(lib,addonfolder,dp)
	

def Clean_Names_MYADDONID(Clean_Name,tmpFile):
    if os.path.exists(tmpFile):
        os.remove(tmpFile)
    os.rename(Clean_Name, tmpFile)
    s=open(tmpFile).read()

    s=s.replace('UK: AMC SD','AMC UK SD')
    s=s.replace('USA/CA: VH1','VH1 USA')
    s=s.replace('USA/CA: E! ENTERTAINMENT SD','E! ENTERTAINMENT USA SD')
    s=s.replace('USA/CA: DISCOVERY CHANNEL','DISCOVERY US')
    s=s.replace('USA/CA: NAT GEO WILD HD','NAT GEO WILD USA HD')
    s=s.replace('USA/CA: NATIONAL GEOGRAPHIC HD','NATIONAL GEOGRAPHIC CHANNEL USA HD')
    s=s.replace('USA/CA: ANIMAL PLANET HD','ANIMAL PLANET US HD')
    s=s.replace('USA/CA: INVESTIGATION DISCOVERY HD','ID US HD')
    s=s.replace('USA/CA: DISNEY CHANNEL HD','DISNEY CHANNEL USA HD')
    s=s.replace('USA/CA: NICKELODEON HD','NICKELODEON US HD')
    s=s.replace('USA/CA: NICK JR HD','NICK JR USA HD')
    s=s.replace('USA/CA: NICKTOONS HD','NICKTOONS USA HD')
    s=s.replace('USA/CA: CARTOON NETWORK HD','CARTOON NETWORK USA HD')
    s=s.replace('USA/CA: FOX HD','FOX USTV')
    s=s.replace('USA/CA: LIFETIME HD','LIFETIME USA HD')
    s=s.replace('USA/CA: SYFY HD','SYFY USA HD')
    s=s.replace('USA/CA: COMEDY CENTRAL HD','COMEDY CENTRAL US HD')
    s=s.replace('USA/CA: NICK JR HD','NICKJR US HD')
    s=s.replace('USA/CA: CI NETWORK HD','CI US')
    s=s.replace('UK: SYFY','SYFY UK')
    s=s.replace('SKY ARTS SD','SKY ARTS 1 SD')
    s=s.replace('TLC HD','TLC USA HD')
    s=s.replace('COMEDY CENTRAL EXTRA','COMEDY CENTRAL XTRA')
    s=s.replace('GOOD FOOD SD','GOOD FOOD UK SD')
    s=s.replace('(HD)NFL: ','NFL ')
    s=s.replace('(HD)NFLFOX: ','NFL ')
    s=s.replace(' # ','')
    s=s.replace(' - ','')
    s=s.replace(' - .','')
    s=s.replace('(HD)NFLN Redzone: 		','NFL ')
    s=s.replace('(HD)NFLN: ','NFL')
    s=s.replace('(HD)NFLNBC:','NFL NBC')
    s=s.replace('CA: ','')
    s=s.replace('[COLOR Normal \e[1mBold]','')
    s=s.replace('CA: ','')
    s=s.replace('USA: ','')
    s=s.replace('ML:','ML')
    s=s.replace('NL: ','')
    s=s.replace('XXX: ','')	
    s=s.replace('SkySports','Sky Sports')		
    s=s.replace('UK:  ','')
    s=s.replace('UK: ','')
    s=s.replace('BBC 1','BBC ONE')
    s=s.replace('BBC 2','BBC TWO')
    s=s.replace('ITV SD','ITV1 SD')
    s=s.replace('ITV HD','ITV1 HD')
    s=s.replace('Uk: ','')
    s=s.replace('SKY CINEMA HITS','SKY CINEMA SHOWCASE')
    s=s.replace('SKY CINEMA CRIME & THRILLER','SKY CINEMA THRILLER')
    s=s.replace('SKY CINEMA SCI FI & HORROR','SKY CINEMA SCI-FI AND HORROR')
    s=s.replace('SKY ONE','Sky1')
    s=s.replace('SKY TWO','Sky2')
    s=s.replace('[COLOR white]','')	
    s=s.replace('USA/','')
    s=s.replace('PL: ','Polish ')
    s=s.replace('INT: ','')
    s=s.replace('FR: ','French ')
    s=s.replace('ES: ','Spanish ')
    s=s.replace('DE: ','German ')
    s=s.replace('AR: ','Arabic ')
    s=s.replace('MIO SPORTS 102','MIO 102 SPORTS')
    s=s.replace('MIO SPORTS 103','MIO 103 SPORTS')
    s=s.replace('MIO SPORTS 104','MIO 104 SPORTS')
    s=s.replace('MIO SPORTS 105','MIO 105 SPORTS')
    s=s.replace('MIO SPORTS 106','MIO 106 SPORTS')
    s=s.replace('MIO SPORTS 107','MIO 107 SPORTS')
    s=s.replace('BEIN HD','BEIN-SPORTS')
    s=s.replace('UNIVERSAL HD','UNIVERSAL CHANNEL HD')
    s=s.replace('UNIVERSAL SD','UNIVERSAL CHANNEL SD')
    s=s.replace('HALLMARK HD','HALLMARK CHANNEL HD')
    s=s.replace('NATIONAL GEOGRAPHIC SD','NATIONAL GEOGRAPHIC CHANNEL SD')
    s=s.replace('NATIONAL GEOGRAPHIC HD','NATIONAL GEOGRAPHIC CHANNEL HD')
    s=s.replace('DISCOVERY HOME & HEALTH SD','DISCOVERY HOME AND HEALTH SD')
    s=s.replace('SKY SPORTS 1 HD BACKUP','SKY SPORTS 1 BACKUP HD')
    s=s.replace('SKY SPORTS 2 HD BACKUP','SKY SPORTS 2 BACKUP HD')
    s=s.replace('SKY SPORTS 3 HD BACKUP','SKY SPORTS 3 BACKUP HD')
    s=s.replace('SKY SPORTS 4 HD BACKUP','SKY SPORTS 4 BACKUP HD')
    s=s.replace('SKY SPORTS 5 HD BACKUP','SKY SPORTS 5 BACKUP HD')
    s=s.replace('SKY SPORTS F1 HD BACK UP','SKY SPORTS F1 BACKUP HD')
    s=s.replace('SKY SPORTS NEWS HQ','SKY SPTS NEWS')
    s=s.replace('SKY SPTS NEWS HD','SKY SPORTS NEWS HD')
    s=s.replace('SKY SPTS NEWS HDS','SKY SPORTS NEWS HDS')
    s=s.replace('BT SPORT 1 HD 2','BT SPORT 1 BACKUP HD')
    s=s.replace('BT SPORT 2 HD 2','BT SPORT 2 BACKUP HD')
    s=s.replace('BT SPORT 3 HD 2','BT SPORT 3 BACKUP HD')
    s=s.replace('EUROSPORT 1','BRITISH EUROSPORT')
    s=s.replace('NBC EXTRA TIME','NotUsedNBCEXTRATIME')
    s=s.replace('BOXNATION','BOX NATION')
    s=s.replace('LIVE NHL','NHL Center Ice')
    s=s.replace('LIVE NBA','NBA LEAGUE PASS')
    s=s.replace('LIVE NFL','NFL SUNDAY TICKET')
    s=s.replace('PAC12','PAC-12')
    s=s.replace('PAC 12','PAC-12')
    s=s.replace('BEIN-SPORTS 1','BEIN-SPORTS-1HD')
    s=s.replace('BEIN-SPORTS 2','BEIN-SPORTS-2HD')
    s=s.replace('BEIN-SPORTS 3','BEIN-SPORTS-3HD')
    s=s.replace('BEIN-SPORTS 4','BEIN-SPORTS-4HD')
    s=s.replace('BEIN-SPORTS 5','BEIN-SPORTS-5HD')
    s=s.replace('BEIN-SPORTS 6','BEIN-SPORTS-6HD')
    s=s.replace('BEIN-SPORTS 7','BEIN-SPORTS-7HD')
    s=s.replace('BEIN-SPORTS 8','BEIN-SPORTS-8HD')
    s=s.replace('BEIN-SPORTS 9','BEIN-SPORTS-9HD')
    s=s.replace('BEIN-SPORTS 10','BEIN-SPORTS-10HD')
    s=s.replace('BEIN-SPORTS 11','BEIN-SPORTS-11HD')
    s=s.replace('BEIN-SPORTS 12','BEIN-SPORTS-12HD')
    s=s.replace('ASTRO SPORTS HD 1','ASTRO SUPERSPORT 1 HD')
    s=s.replace('ASTRO SPORTS HD 2','ASTRO SUPERSPORT 2 HD')
    s=s.replace('ASTRO SPORTS HD 3','ASTRO SUPERSPORT 3 HD')
    s=s.replace('ASTRO SPORTS HD 4','ASTRO SUPERSPORT 4 HD')
    s=s.replace('SETANTA IRELAND','EIR SPORTS 1')
    s=s.replace('SETANTA SPORTS 1','EIR SPORTS 2')
    s=s.replace('HISTORY HD','HISTORY US HD')
    s=s.replace('DISCOVERY SCIENCE SD','DISCOVERY SCIENCE UK SD')
    s=s.replace('DISCOVERY SCIENCE HD','DISCOVERY SCIENCE USA HD')
    s=s.replace('DISCOVERY CRIME AND INVESTIGATION','CI')
    s=s.replace('ID SD','ID SD UK')
    s=s.replace('CI SD','CI SD UK')
    s=s.replace('JR. TOO','NICK JR TOO UK')
    s=s.replace('THE CW','CW')
    s=s.replace('SPIKE HD','SPIKE US HD')
    s=s.replace('A&E TV HD','A AND E HD')
    s=s.replace('STARZ EDGE HD','STARZ EDGEEAST HD')
    s=s.replace('CINEMAX MOREMAX HD','MOREMAX HD')
    s=s.replace('CINEMAX HD','CINEMAX EAST HD')
    s=s.replace('NICKELODEON USA HD','NICKELODEONEAST HD')
    s=s.replace('CNN HD','CNN HD USA')
    s=s.replace('CTV HD','CTV CANADA HD')
    s=s.replace('TENNIS CHANNEL','THE TENNIS CHANNEL')
    s=s.replace('BEIN USA','BEIN SPORTS')
    s=s.replace('TV3 SD','TV3 IRISH SD')
    s=s.replace('DRAMA SD','DRAMA UK SD')
    s=s.replace('AMC HD','AMC US')
    s=s.replace('TRU TV HD','TRUTV US HD')
    s=s.replace('.m3u8','.ts')

    f=open(Clean_Name,'a')
    f.write(s)
    f.close()
    os.remove(tmpFile)
    return
