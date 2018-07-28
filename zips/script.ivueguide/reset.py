import time
import os, shutil
import xbmc
import xbmcgui
import xbmcaddon

databasePath = xbmc.translatePath('special://profile/addon_data/script.ivueguide')
subPath = xbmc.translatePath('special://profile/addon_data/script.ivueguide/resources/ini')
pyPath = xbmc.translatePath('special://profile/addon_data/script.ivueguide/resources/subs')
setupPath = xbmc.translatePath('special://profile/addon_data/script.ivueguide/resources/guide_setups')
fullPath = xbmc.translatePath('special://profile/addon_data/script.ivueguide')
dialog = xbmcgui.Dialog()

def SoftReset():	
    clearFiles = ["guides.ini", "addons.ini", "program.db","program_category.ini", "iVue.ini", "categories.ini"]
    keepFiles = ["settings.xml"]
    for root, dirs, files in os.walk(databasePath,topdown=True):
	    dirs[:] = [d for d in dirs if d not in ['skins']]
	    for name in files:
		    if name.endswith(".xml") and name not in keepFiles:
			    try:
				    os.remove(os.path.join(root,name))
			    except:
				    dialog.ok('Soft Reset', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using Soft Reset[/COLOR]')
				    pass
		    elif name in clearFiles:
			    try:
				    os.remove(os.path.join(root,name))
			    except:
				    dialog.ok('Soft Reset', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using Soft Reset[/COLOR]')
				    pass
		    else:
			    continue
    dialog.ok('Ivue guide Soft reset', 'Please restart for ','the changes to take effect','[COLOR yellow]Thank you for using Soft Reset[/COLOR]')


def HardReset():
    try:
	    shutil.rmtree(fullPath,ignore_errors=True, onerror=None)
	    if not os.path.exists(fullPath):
		    dialog.ok('Ivue guide Hard reset', 'Please restart for ','the changes to take effect','[COLOR yellow]Thank you for using Hard Reset[/COLOR]')
	    else:
		    dialog.ok('Ivue guide Hard reset', 'Failed to remove some files','[COLOR yellow]Please try again[/COLOR]')
    except:				   
	    dialog.ok('Ivue guide Hard reset', 'Failed to remove some files','[COLOR yellow]Please try again[/COLOR]')



def addons2():			
    for root, dirs, files in os.walk(databasePath,topdown=True):
	    dirs[:] = [d for d in dirs]
	    for name in files:
		    if "addons2.ini" in name:
			    try:
				    os.remove(os.path.join(root,name))
				    if not os.path.exists(os.path.join(root,name)):
				        dialog.ok('iVue %s Reset' % name, 'Please restart for ','the changes to take effect','[COLOR yellow]Thank you for using iVue Reset[/COLOR]')     
			    except:				   
				    dialog.ok('iVue %s Reset' % name, 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using iVue Reset[/COLOR]')



def purgeDB():			
    for root, dirs, files in os.walk(databasePath,topdown=True):
	    dirs[:] = [d for d in dirs]
	    for name in files:
		    if "master.db" in name:
			    try:
				    os.remove(os.path.join(root,name))
				    if not os.path.exists(os.path.join(root,name)):
				        dialog.ok('iVue %s Reset' % name, 'Please restart for ','the changes to take effect','[COLOR yellow]Thank you for using iVue Reset[/COLOR]')             
			    except:				   
				    dialog.ok('iVue %s Reset' % name, 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using iVue Reset[/COLOR]')

def WipeSetups():
    try:
	    shutil.rmtree(setupPath,ignore_errors=True, onerror=None)
	    if not os.path.exists(setupPath):
		    dialog.ok('iVue Guide Setup Reset', 'Please restart for ','the changes to take effect','[COLOR yellow]Thank you for using iVue Reset[/COLOR]')     
    except:				   
	    dialog.ok('iVue Guide Reset', 'Error Removing XML Setups','','[COLOR yellow]Thank you for using iVue Reset[/COLOR]')


prnum=""
try:
    prnum= sys.argv[ 1 ]
except:
    pass

if prnum == 'soft':
    SoftReset()
 
elif prnum == 'hard':
    HardReset()

elif prnum == 'addons2':
    addons2()

elif prnum == 'purge':
    purgeDB()

elif prnum == 'setups':
    WipeSetups()

