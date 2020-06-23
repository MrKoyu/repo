# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

'''
2020/01/04: Switched from modal to show
'''

import traceback

import xbmc
import xbmcgui
import xbmcaddon

from resources.lib.dialogs import themecontrol
from resources.lib.modules import control, log_utils


def OK_Dialog(title, msg):
    class OK_Box(xbmcgui.WindowXMLDialog):
        # until now we have a blank window, the onInit function will parse your xml file
        def onInit(self):
            self.colors = themecontrol.ThemeColors()

            self.title = 1
            self.body = 2
            self.okbtn = 5

            self.getControl(self.title).setLabel(title)
            self.setProperty('dhtext', self.colors.dh_color)
            self.setProperty('btnfocus', self.colors.btn_focus)
            self.getControl(self.body).setText(msg)

            xbmc.sleep(100)
            # this puts the focus on the top item of the container
            self.setFocusId(self.getCurrentContainerId())
            self.setFocus(self.getControl(self.okbtn))
            xbmc.executebuiltin("Dialog.Close(busydialog)")

        def onClick(self, controlId):
            if (controlId == self.okbtn):
                self.close()

        def onAction(self, action):
            if action == themecontrol.ACTION_PREVIOUS_MENU or action == themecontrol.ACTION_NAV_BACK:
                self.close()

    ok = OK_Box('Dialog_OK.xml', themecontrol.skinModule(), themecontrol.skinTheme(), '1080i', title=title, msg=msg)
    ok.show()
    del ok