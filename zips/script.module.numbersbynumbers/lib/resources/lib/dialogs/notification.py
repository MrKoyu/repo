# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################


import traceback

import xbmc
import xbmcgui
import xbmcaddon

from resources.lib.dialogs import themecontrol
from resources.lib.modules import control, log_utils


def infoDialog(title="NuMb3r5", msg='', style='INFO', timer=3000):
    class Notify_Box(xbmcgui.WindowXMLDialog):
        # until now we have a blank window, the onInit function will parse your xml file
        def onInit(self):
            self.colors = themecontrol.ThemeColors()

            self.sounds = themecontrol.ThemeSounds()
            notifyAudio = self.sounds.notifyinfo
            if style == 'INFO':
                notifyAudio = self.sounds.notifyinfo
            elif style == 'WARNING':
                notifyAudio = self.sounds.notifywarning
            elif style == 'ERROR':
                notifyAudio = self.sounds.notifyerror

            self.title = 401
            self.msg = 402

            self.getControl(self.title).setLabel(title)
            self.setProperty('dhtext', self.colors.dh_color)
            self.getControl(self.msg).setLabel(msg)
            self.setProperty('dttext', self.colors.dt_color)

            self.showdialog(notifyAudio)

        def showdialog(self, notifyAudio):
            xbmc.playSFX(notifyAudio)
            xbmc.sleep(100)
            # this puts the focus on the top item of the container
            self.setFocusId(self.getCurrentContainerId())
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            xbmc.sleep(timer)
            self.close()

        def onClick(self, controlId):
            pass

        def onAction(self, action):
            pass

    ok = Notify_Box('Dialog_Notification.xml', themecontrol.skinModule(), themecontrol.skinTheme(), '1080i', title=title, msg=msg, style=style, timer=timer)
    ok.doModal()
    del ok