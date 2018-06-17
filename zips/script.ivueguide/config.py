import xbmc, xbmcgui, shutil, urllib2, urllib, os, xbmcaddon, zipfile, time, re
import shutil
import utils
import xbmcvfs

addon_id = 'script.ivueguide'
addon_name = xbmcaddon.Addon(addon_id)
HOME = addon_name.getAddonInfo('path')
ICON = os.path.join(HOME, 'icon.png')
PACKAGES       = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages'))
TEMP =	  addon_name.getSetting('tempskin')
USER_AGENT     = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

#Karls changes

ivue = utils.folder()
d = xbmcgui.Dialog()
dp = xbmcgui.DialogProgress()
path = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ivueguide', 'resources', 'skins'))
xmlData = xbmc.translatePath('special://profile/addon_data/script.ivueguide/resources/config/Data.txt')
logoData = xbmc.translatePath('special://profile/addon_data/script.ivueguide/resources/config/Logo.txt')
catData = xbmc.translatePath('special://profile/addon_data/script.ivueguide/resources/categories/')	
ivue = utils.folder()
players = ivue+'/playable/unplayable.txt'
FOAlist = ''
proglist = []
try:
    FOAlist = urllib2.urlopen(players).read().splitlines()
except:
    pass
for item in FOAlist:
    proglist.append(item)	
prnum=""
try:
    prnum= sys.argv[ 1 ]
except:
    pass

def openURL(url):
	  req = urllib2.Request(url)
	  req.add_header('User-Agent', USER_AGENT)
	  response = urllib2.urlopen(req)
	  link=response.read()
	  response.close()
	  return link

def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
	try:
		percent = min((numblocks*blocksize*100)/filesize, 100)
		print 'done' +str(percent)+'%'
		dp.update(percent)
	except:
		percent = 100
		dp.update(percent)
	if dp.iscanceled():
		raise Exception("Cancelled")
		dp.close()
		
def radio(play, path):
    for item in proglist:
        try:
            if item.split(' =')[0] == str(play):
	        location = str(path).split('url=')[1].split('%3A80')[0]
		if item.split('= ')[1] == location :
		    return True
                else:
                    return False
        except:
            if item == str(play):
		return False
            else:
                return True

def extract(_in, _out):
	dp = xbmcgui.DialogProgress()
	zin    = zipfile.ZipFile(_in,  'r')
	nFiles = float(len(zin.infolist()))
	count  = 0
	for item in zin.infolist():
		count += 1
		update = count / nFiles * 100
		zin.extract(item, _out)


def Custom():
	  folder = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages', 'customskin'))
	  if not os.path.exists(folder):
	      os.makedirs(folder)
	  choice = xbmc.Keyboard('','[COLOR fffea800][B]ENTER ZIP URL[/B][/COLOR]')
	  choice.setDefault(addon_name.getSetting('customSkin.url'))
	  choice.setHiddenInput(False)
	  choice .doModal()
	  input= choice.getText()
	  zipSkin = os.path.join(PACKAGES,'Custom.zip') 
	  dp.create("iVue","downloading skin from %s" % input,'')
	  urllib.urlretrieve(input,zipSkin,lambda nb, bs, fs, url=input: _pbhook(nb,bs,fs,input,dp))
	  extract(zipSkin, folder) 
	  time.sleep(1)
	  skinName = os.walk(folder).next()[1]
	  join = os.path.join(folder, *(skinName))
	  set = '%s' % join
	  addon_name.setSetting('customSkin.url', input)
	  splitName = os.path.basename(join)
	  SkinFolder = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ivueguide', 'resources', 'skins', '%s' % splitName))
	  if os.path.exists(SkinFolder):
	      shutil.rmtree(SkinFolder)
	  shutil.move(join, SkinFolder)
	  addon_name.setSetting('skin', splitName)
	  addon_name.setSetting('customSkin.enabled', 'false') 
	  shutil.rmtree(folder)
	  d.ok('Ivue', 'Download complete', '',"%s is now set as current skin" % splitName) 

def listskins():
    files = [] 
    if os.path.exists(path):
        for name in os.listdir(path): 
            files.append(name)
        skin = d.select("ivue", files)
        if skin == -1:
            return
        else:
            selected = files[skin]
            addon_name.setSetting('skin', selected)
            if selected == 'Transparent Vue':
                addon_name.setSetting('transparent.enabled', 'true')
            else:
                addon_name.setSetting('transparent.enabled', 'false')
    else:
        d.ok('Ivue', 'Skin Folder Missing', '',"Please run iVue to complete setup")

def getskins():
    folder = ivue+'/skins/'
    view = openURL(folder)
    match=re.compile('<a href="(.*?)">').findall(view)
    notneeded = ['/ivueguide/', 'index.htmlofflineforabit', '/ivueguide//','/ivueguidexml//', 'skins.zip']
    files = [] 
    for name in match:
        if not name in notneeded:
            name = re.sub(r'%20', ' ', name)
            name = re.sub(r'.zip', '', name)
            if not name in os.listdir(path):
                files.append(name)
    skin = d.select("ivue", files)
    if skin == -1:
        return
    else:
        selected = files[skin]
        zipurl = ivue+'/skins/%s.zip' % (selected).replace(' ', '%20') 
        zipfile = os.path.join(PACKAGES,"%s.zip" % selected) 
        dp.create("iVue","Downloading %s" % selected,'')
        urllib.urlretrieve(zipurl,zipfile,lambda nb, bs, fs, url=zipurl: _pbhook(nb,bs,fs,zipurl,dp))
        extract(zipfile, path) 
        time.sleep(1)
        dp.close() 
        if os.path.exists(path + "/%s" % selected): 
            addon_name.setSetting('skin', '%s' % selected)
            addon_name.setSetting('download.skin', '')
            if selected == 'Transparent Vue':
                addon_name.setSetting('transparent.enabled', 'true')
            else:
                addon_name.setSetting('transparent.enabled', 'false')
            d.ok('Ivue', 'Download complete', '', '%s is now set as current skin' % selected)
        else:
            d.ok('Ivue', 'Download failed', 'Please try downloading again')
 
def delskins():
    files = [] 
    if os.path.exists(path):
        for name in os.listdir(path): 
            files.append(name)
        skin = d.select("ivue", files)
        if skin == -1:
            return
        else:
            selected = files[skin]
            installed = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ivueguide', 'resources', 'skins', '%s' % selected))
            shutil.rmtree(installed)
            if not os.path.exists(installed):
                d.ok("iVue", '','%s has been successfully removed' % selected, " [COLOR gold]Brought To You By iVue[/COLOR]")
            else:
                d.ok("iVue", '','%s was not removed' % selected, " [COLOR gold]Please try again[/COLOR]")
    else:
        d.ok('Ivue', 'No skins installed', '',"Please run iVue to complete setup")

def customiseSkin():
        skin = d.select('Skin Colours',  ['Main Colour', 'Focus Colour', 'Reminder Colour (no focus)', 'Reminder Colour (focus)'])
        if skin == -1:
            return
        if skin == 0:
            customiseColours('Main')

        if skin == 1:
            customiseColours('Focus')

        if skin == 2:
            customiseColours('Reminder')

        if skin == 3:
            customiseColours('RemFocus')

def customiseColours(texture):
        if texture == 'focusTexture':
            header = 'Select focus texture colour'
            destination = 'tvguide-program-grey-focus.png'

        if texture == 'remTexture':
            header = 'Select reminder texture colour'
            destination = 'tvguide-program-red.png'

        if texture == 'remFocusTexture':
            header = 'Select reminder focus texture colour'
            destination = 'tvguide-program-red-focus.png'

        if texture == 'backgroundTexture':
            header = 'Select main background texture colour'
            colourDialog = d.browseSingle(type=2, heading=header, shares='files', mask='.png', useThumbs=True, treatAsFolder=True, defaultt='special://profile/addon_data/script.ivueguide/resources/skins/Transparent Vue/media/colors/')
            if colourDialog:
                try:
                    colour = str(colourDialog).split('colors/')[1].split('.png')[0]
                    if not colour == '':
                        customisebg(colour)
                except:
                    pass

        else:
            colourDialog = d.browse(type=2, heading=header, shares='files', mask='.png', useThumbs=True, treatAsFolder=False, defaultt='special://profile/addon_data/script.ivueguide/resources/skins/Transparent Vue/media/colors/')
            if colourDialog > 0:
                colour = str(colourDialog).split('colors/')[1].split('.png')[0]
                shutil.copy(xbmc.translatePath(colourDialog), os.path.join(utils.SkinDir, 'Transparent Vue', 'media', destination))
                addon_name.setSetting(texture, '[COLOR %s]%s[/COLOR]' % (colour, colour))


def customisebg(colour):
        if addon_name.getSetting('skin') == 'Transparent Vue':
            dirs = os.listdir(os.path.join(utils.SkinDir, 'Transparent Vue', '720p'))
            for file in dirs:
                file = os.path.join(utils.SkinDir, 'Transparent Vue', '720p', file)
                f1=open(file,'r').read()
                match=re.compile('<texture colordiffuse="(.*?)"').findall(f1)
                if match:
                    f1=open(file,'r').read() 
                    f2=open(file,'w') 
                    m=f1.replace(str(match[0]),str(colour))
                    f2.write(m)       
                    f2.close()
        d.ok("iVue", '',' SUCCESSFUL :)', " [COLOR gold]Brought To You By iVue[/COLOR]")
        addon_name.setSetting('backgroundTexture', '[COLOR %s]%s[/COLOR]' % (colour, colour))

def updater():
	message = 'Checking addon Updates'
	xbmc.executebuiltin('XBMC.Notification(%s, %s, 2000, %s)' % (addon_id, message, ICON))
	xbmc.executebuiltin("XBMC.UpdateaddonRepos()")
	d.ok("iVue", '',' CHECKING FOR REPO UPDATES SUCCESSFUL :)', " [COLOR gold]Brought To You By iVue[/COLOR]")
	return
			
	
def setXmlUrl():
    if os.path.exists(xmlData):
	xml = open(xmlData).read()
        matches = re.compile('name="(.*?)".+?url="(.*?)"').findall(xml)
        subbedaddons = {}
            
	for name, value in matches:
            subbedaddons[name] = value
			
        names = sorted(subbedaddons)
 
        selection = d.select('[COLOR fffea800]Xmls[/COLOR]', names)
        if selection < 0:
            return
        else:
            sub_name = names[selection]
            link = subbedaddons[sub_name]
            addon_name.setSetting('sub.xmltv', sub_name)
            addon_name.setSetting('sub.xmltv.url', link)
            try:
                check_files = sub_name.split(' (')[0]
            except:
                check_files = sub_name

            if os.path.exists(os.path.join(catData,check_files+'.ini')) and not addon_name.getSetting('categories.path') == check_files:
                yes_pressed = d.yesno('[COLOR ffff7e14][B]IVUE SETUP[/B][/COLOR]', 'Do you wish to use ' +check_files+ ' categories',nolabel='no',yeslabel='yes')
                if yes_pressed:
                    addon_name.setSetting('categories.path', check_files)
            if (os.path.exists(logoData) and not addon_name.getSetting('sub.logos') == check_files) or (os.path.exists(logoData) and not int(addon_name.getSetting('logos.source')) == 1):
	        logos = open(logoData).read()
                matches = re.compile('name="(.*?)".+?logo="(.*?)"').findall(logos)
            
	        for name, value in matches:
                    if name == check_files:
                        yes_pressed = d.yesno('[COLOR ffff7e14][B]IVUE SETUP[/B][/COLOR]', 'Do you wish to use ' +check_files+ ' logo pack',nolabel='no',yeslabel='yes')
                        if yes_pressed:
                            addon_name.setSetting('logos.source', '1')
                            addon_name.setSetting('sub.logos', check_files)
                            addon_name.setSetting('sub.logos.url', value)
            d.ok('iVue', 'Please press ok in settings dialog to confirm changes, then reload guide for changes to take affect', '')

		
def setlogoUrl():
    if os.path.exists(logoData):
	logos = open(logoData).read()
        matches = re.compile('name="(.*?)".+?logo="(.*?)"').findall(logos)
        subbedaddons = {}
            
	for name, value in matches:
            subbedaddons[name] = value
			
        names = sorted(subbedaddons)
 
        selection = d.select('[COLOR fffea800]Logo Packs[/COLOR]', names)
        if selection < 0:
            return
        else:
            sub_name = names[selection]
            link = subbedaddons[sub_name]
            addon_name.setSetting('sub.logos', sub_name)
            addon_name.setSetting('sub.logos.url', link)

   




def setcat():
    subbedaddons = []
    if os.path.exists(catData):
	
	for file in os.listdir(catData):
            subbedaddons.append(file.replace('.ini', ''))
			
        names = sorted(subbedaddons)
 
        selection = d.select('[COLOR fffea800]Categories file[/COLOR]', names)
        if selection < 0:
            return
        else:
            sub_name = names[selection]
            addon_name.setSetting('categories.path', sub_name)
 


if prnum == 'Custom':
    Custom()
 
elif prnum == 'List':
    listskins()


elif prnum == 'Get':
    getskins()


elif prnum == 'Delete':
    delskins()

elif prnum == 'Update':
    updater()
	
elif prnum == 'setxml':
    setXmlUrl()
	
elif prnum == 'logo':
    setlogoUrl()

elif prnum == 'setcat':
    setcat()

elif prnum == 'customiseSkin':
    customiseSkin()

elif prnum == 'backgroundTexture':
    customiseColours('backgroundTexture')

elif prnum == 'focusTexture':
    customiseColours('focusTexture')

elif prnum == 'remTexture':
    customiseColours('remTexture')

elif prnum == 'remFocusTexture':
    customiseColours('remFocusTexture')
