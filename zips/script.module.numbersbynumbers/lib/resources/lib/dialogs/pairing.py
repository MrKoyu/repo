# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
#  As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

import re
import os
import traceback
import webbrowser

import xbmc
import xbmcaddon
import xbmcgui

from resources.lib.dialogs import themecontrol
from resources.lib.modules import client, control, log_utils


PAIR_LIST = [
    ("streamcherry", "https://streamcherry.com/pair",
     'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3RoZXJlYWxhdHJlaWRlcy9hdHJlaWRlc2V4dHJhcy9tYXN0ZXIvYXJ0d29yay9wYWlyaW5nL3N0cmVhbWNoZXJyeS5wbmc='),
    ("the_video_me", "https://vev.io/pair",
     'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3RoZXJlYWxhdHJlaWRlcy9hdHJlaWRlc2V4dHJhcy9tYXN0ZXIvYXJ0d29yay9wYWlyaW5nL3ZldmlvLnBuZw=='),
    ("vid_up_io", "https://vidup.io/pair",
     'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3RoZXJlYWxhdHJlaWRlcy9hdHJlaWRlc2V4dHJhcy9tYXN0ZXIvYXJ0d29yay9wYWlyaW5nL3ZpZHVwLnBuZw=='),
    ("vshare", "https://vshare.eu/pair",
     'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3RoZXJlYWxhdHJlaWRlcy9hdHJlaWRlc2V4dHJhcy9tYXN0ZXIvYXJ0d29yay9wYWlyaW5nL3ZzaGFyZWV1LnBuZw=='),
    ("flashx", "https://www.flashx.tv/?op=login&redirect=https://www.flashx.tv/pairing.php",
     'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3RoZXJlYWxhdHJlaWRlcy9hdHJlaWRlc2V4dHJhcy9tYXN0ZXIvYXJ0d29yay9wYWlyaW5nL2ZsYXNoeC5wbmc=')]

AUTH_LIST = [
    ("trakt", 'RunPlugin(plugin://plugin.video.numbersbynumbers/?action=authTrakt)',
     'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3RoZXJlYWxhdHJlaWRlcy9hdHJlaWRlc2V4dHJhcy9tYXN0ZXIvYXJ0d29yay9wYWlyaW5nL3RyYWt0LnBuZw=='),
    ("real_debrid", 'RunPlugin(plugin://script.module.resolveurl/?mode=auth_rd)',
     'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3RoZXJlYWxhdHJlaWRlcy9hdHJlaWRlc2V4dHJhcy9tYXN0ZXIvYXJ0d29yay9wYWlyaW5nL3JkLnBuZw=='),
    ("premiumize_me", 'RunPlugin(plugin://script.module.resolveurl/?mode=auth_pm)',
     'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3RoZXJlYWxhdHJlaWRlcy9hdHJlaWRlc2V4dHJhcy9tYXN0ZXIvYXJ0d29yay9wYWlyaW5nL3ByZW1pdW1pemUucG5n'),
    ("alldebrid", 'RunPlugin(plugin://script.module.resolveurl/?mode=auth_ad)',
     'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3RoZXJlYWxhdHJlaWRlcy9hdHJlaWRlc2V4dHJhcy9tYXN0ZXIvYXJ0d29yay9wYWlyaW5nL3JkLnBuZw==')]


def Pair_Dialog():
    class Pair_Window(xbmcgui.WindowXMLDialog):
        # until now we have a blank window, the onInit function will parse your xml file
        def onInit(self):
            self.last_selection = ''
            self.colors = themecontrol.ThemeColors()
            self.open_browser = control.setting('browser.pair')
            if self.open_browser == '' or self.open_browser == 'true':
                self.open_browser = True
            else:
                self.open_browser = False

            self.menu_list = 100
            self.menu = self.getControl(self.menu_list)
            self.browserbtn = 150
            self.OpenButton = self.getControl(self.browserbtn)
            self.OpenButton.setSelected(self.open_browser)
            self.right_pane = 200
            self.content = self.getControl(self.right_pane)

            self.setProperty('dhtext', self.colors.dh_color)
            self.setProperty('mhtext', self.colors.mh_color)
            self.setProperty('mttext', self.colors.mt_color)
            self.setProperty('fttext', self.colors.focus_textcolor)

            menu_items = []
            menu_items.append(control.item(label='Pairing'))
            menu_items.append(control.item(label='Authorize'))
            self.menu.addItems(menu_items)

            self.pairItems = []
            for item in PAIR_LIST:
                the_title = 'Pair for %s' % (item[0].replace('_', ' ').capitalize())
                the_item = control.item(label=the_title)
                the_icon = item[2].decode('base64')
                the_item.setArt({'icon': the_icon, 'thumb': the_icon})
                self.pairItems.append(the_item)

            self.authItems = []
            for item in AUTH_LIST:
                the_title = 'Authorize %s' % (item[0].replace('_', ' ').capitalize())
                the_item = control.item(label=the_title)
                the_icon = item[2].decode('base64')
                the_item.setArt({'icon': the_icon, 'thumb': the_icon})
                self.authItems.append(the_item)

            self.content.addItems(self.pairItems)

            xbmc.sleep(100)
            # this puts the focus on the top item of the container
            self.setFocusId(self.getCurrentContainerId())
            self.setFocus(self.getControl(self.menu_list))
            xbmc.executebuiltin("Dialog.Close(busydialog)")

        def onClick(self, controlId):
            if (controlId == self.browserbtn):
                if self.OpenButton.isSelected():
                    self.open_browser = True
                    control.setSetting('browser.pair', 'true')
                else:
                    self.open_browser = False
                    control.setSetting('browser.pair', 'false')
            elif (controlId == self.right_pane):
                selection = self.content.getListItem(self.content.getSelectedPosition()).getLabel()
                if 'Pair for' in selection:
                    self.pairHandler(selection)
                elif 'Authorize' in selection:
                    self.authHandler(selection)

        def onAction(self, action):
            if action == themecontrol.ACTION_PREVIOUS_MENU or action == themecontrol.ACTION_NAV_BACK:
                self.close()
            elif any(i == action for i in themecontrol.MENU_ACTIONS):
                try:
                    '''
                    self.last_selection is used so the same code does keep running while the mouse is
                    hovering over the same item during movement.
                    '''
                    if (self.getFocusId() > 0):
                        self.setFocusId(self.getFocusId())
                    if self.getFocusId() == self.menu_list:
                        try:
                            selection = self.menu.getListItem(self.menu.getSelectedPosition()).getLabel()
                            if self.last_selection != selection:
                                self.last_selection = selection
                                self.content.reset()
                                if selection == 'Pairing':
                                    self.content.addItems(self.pairItems)
                                elif selection == 'Authorize':
                                    self.content.addItems(self.authItems)
                        except Exception:
                            failure = traceback.format_exc()
                            log_utils.log('Fuck, it failed.\n' + failure)
                except Exception:
                    # Nothing has focus in this case, like when just moving the mouse around in general
                    pass

        def pairHandler(self, selection):
            self.close()

            pair_item = re.sub('\[.*?]', '', selection).replace('Pair for ', '').replace(' ', '_').lower()
            log_utils.log(selection)
            log_utils.log(pair_item)
            for item in PAIR_LIST:
                if str(item[0]) == pair_item:
                    site = item[1]
                    site_name = item[0].replace('_', ' ').capitalize()
                    break

            if self.open_browser:
                check_os = platform()
                if check_os == 'android':
                    xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' % (site))
                elif check_os == 'osx':
                    os.system("open " + site)
                else:
                    webbrowser.open(site)
            else:
                try:
                    from resources.lib.dialogs import ok
                    ok.OK_Dialog('%s Stream Authorization' % (site_name), 'Using a device on your network, visit the link below to authorize streams:[CR][CR]%s' % (site))
                except Exception:
                    failure = traceback.format_exc()
                    log_utils.log('Pairing - Exception: \n' + str(failure))
                    return

        def authHandler(self, selection):
            self.close()

            auth_item = re.sub('\[.*?]', '', selection).replace('Authorize ', '').replace(' ', '_').lower()
            func = None
            for item in AUTH_LIST:
                if str(item[0]) == auth_item:
                    func = item[1]
                    break

            if func is not None:
                xbmc.executebuiltin(func)

    pair = Pair_Window('Pair_Tool.xml', themecontrol.skinModule(), themecontrol.skinTheme(), '1080i')
    pair.doModal()
    del pair


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
