import os, xbmc, xbmcaddon

#########################################################
### User Edit Variables #################################
#########################################################
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')
ADDONTITLE     = '[COLOR lightskyblue]CellarDoorTV Wizard[/COLOR]'
EXCLUDES       = [ADDON_ID]
# Text File with build info in it.
BUILDFILE      = 'http://cellardoortv.com/cdtvtxt/newwiztxt/autobuilds.txt'
# How often you would list it to check for build updates in days
# 0 being every startup of kodi
UPDATECHECK    = 0
# Text File with apk info in it.
APKFILE        = 'http://cellardoortv.com/cdtvtxt/apk.txt'
# Text File with Youtube Videos urls.  Leave as 'http://' to ignore
YOUTUBETITLE   = 'Helpful Videos and Reviews'
YOUTUBEFILE    = 'http://cellardoortv.com/cdtvtxt/youtube.txt'
# Text File for addon installer.  Leave as 'http://' to ignore
ADDONFILE      = 'http://cellardoortv.com/cdtvtxt/addons.txt'
# Text File for advanced settings.  Leave as 'http://' to ignore
ADVANCEDFILE   = 'http://cellardoortv.com/cdtvtxt/Advanced.txt'

# Dont need to edit just here for icons stored locally
PATH           = xbmcaddon.Addon().getAddonInfo('path')
ART            = os.path.join(PATH, 'resources', 'art')

#########################################################
### THEMING MENU ITEMS ##################################
#########################################################
# If you want to use locally stored icons the place them in the Resources/Art/
# folder of the wizard then use os.path.join(ART, 'imagename.png')
# do not place quotes around os.path.join
# Example:  ICONMAINT     = os.path.join(ART, 'mainticon.png')
#           ICONSETTINGS  = 'http://aftermathwizard.net/repo/wizard/settings.png'
# Leave as http:// for default icon
ICONBUILDS     = 'http://cellardoortv.com/icons/thumbWIZARD/buildsicon.png'
ICONMAINT      = 'http://cellardoortv.com/icons/thumbWIZARD/toolsicon.png'
ICONAPK        = 'http://cellardoortv.com/icons/thumbWIZARD/APKicon.png'
ICONADDONS     = 'http://cellardoortv.com/icons/thumbWIZARD/freshstarticon.png'
ICONYOUTUBE    = 'http://cellardoortv.com/icons/thumbWIZARD/Youtubeicon.png'
ICONSAVE       = 'http://cellardoortv.com/icons/thumbWIZARD/backupicon.png'
ICONTRAKT      = 'http://cellardoortv.com/icons/thumbWIZARD/trakticon.png'
ICONREAL       = 'http://'
ICONLOGIN      = 'http://cellardoortv.com/icons/thumbWIZARD/forcecloseicon.png'
ICONCONTACT    = 'http://cellardoortv.com/icons/thumbWIZARD/Contact.png'
ICONSETTINGS   = 'http://cellardoortv.com/icons/thumbWIZARD/settingsicon.png'
# Hide the ====== seperators 'Yes' or 'No'
HIDESPACERS    = 'No'
# Character used in seperator
SPACER         = '*'

# You can edit these however you want, just make sure that you have a %s in each of the
# THEME's so it grabs the text from the menu item
COLOR1         = 'lightskyblue'
COLOR2         = 'white'
# Primary menu items   / %s is the menu item and is required
THEME1         = '[COLOR '+COLOR1+'][B][I][COLOR '+COLOR2+']CDTV[/COLOR][/B][/COLOR] [COLOR '+COLOR2+']%s[/COLOR][/I]'
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'
# Alternate items      / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'
# Current Build Header / %s is the menu item and is required
THEME4         = '[COLOR '+COLOR1+']Current Build:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Current Theme Header / %s is the menu item and is required
THEME5         = '[COLOR '+COLOR1+']Current Theme:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' dont hide
HIDECONTACT    = 'No'
# You can add \n to do line breaks
CONTACT        = 'Thank you for choosing CDTV Wizard.\r\n\r\nContact us on Facebook - follow me on Twitter or visit our website at http://cellardoortv.wordpress.com'
#Images used for the contact window.  http:// for default icon and fanart
CONTACTICON    = 'http://cellardoortv.com/icons/thumbWIZARD/W.png'
CONTACTFANART  = 'http://cellardoortv.com/icons/iconsWIZARD/iconWIZARD.png'
#########################################################

#########################################################
### AUTO UPDATE #########################################
########## FOR THOSE WITH NO REPO #######################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE     = 'No'
# Url to wizard version
WIZARDFILE     = 'http://cellardoortv.com/cdtvtxt/newwiztxt/autobuilds.txt'
#########################################################

#########################################################
### AUTO INSTALL ########################################
########## REPO IF NOT INSTALLED ########################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL    = 'Yes'
# Addon ID for the repository
REPOID         = 'repository.cdrepo'
# Url to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML   = 'https://raw.githubusercontent.com/MrKoyu/repo/master/addons.xml'
# Url to folder zip is located in
REPOZIPURL     = 'https://raw.githubusercontent.com/MrKoyu/repo/master/zips/'
#########################################################

#########################################################
### NOTIFICATION WINDOW##################################
#########################################################
# Enable Notification screen Yes or No
ENABLE         = 'Yes'
# Url to notification file
NOTIFICATION   = 'http://cellardoortv.com/cdtvtxt/notify.txt'
# Use either 'Text' or 'Image'
HEADERTYPE     = 'Text'
HEADERMESSAGE  = 'CDTV WIZARD'
# url to image if using Image 424x180
HEADERIMAGE    = ''
# Background for Notification Window
BACKGROUND     = 'http://cellardoortv.com/icons/backgrounds/fanart.jpg'
#########################################################