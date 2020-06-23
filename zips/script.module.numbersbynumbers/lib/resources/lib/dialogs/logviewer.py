# -*- coding: utf-8 -*-

#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

import os
import re
import traceback

import xbmc
import xbmcgui
import xbmcaddon

from resources.lib.dialogs import themecontrol
from resources.lib.modules import control, log_utils


def LogViewer(logfile=None):
    class LogViewver_Window(xbmcgui.WindowXMLDialog):
        # until now we have a blank window, the onInit function will parse your xml file
        def onInit(self):
            self.colors = themecontrol.ThemeColors()

            self.title = 101
            self.msg = 102
            self.scrollbar = 103
            self.upload = 201
            self.kodi = 202
            self.kodiold = 203
            self.addonlog = 204
            self.okbutton = 205

            self.logfile = os.path.join(log_utils.LOGPATH, logfile)

            self.logmsg = log_utils.readLog(self.logfile)
            self.titlemsg = "%s: %s" % (control.addonName(), logfile)
            self.showdialog()

        def showdialog(self):
            self.setProperty('dhtext', self.colors.dh_color)
            self.getControl(self.title).setLabel(self.titlemsg)
            self.getControl(self.msg).setText(log_utils.highlightText(self.logmsg))
            self.setFocusId(self.scrollbar)

        def onClick(self, controlId):
            if controlId == self.okbutton:
                self.close()
            elif controlId == self.upload:
                self.close()
                upload_check = log_utils.uploadLog(self.logmsg)
                if upload_check[0]:
                    data = 'Post this url or scan QRcode for your log, together with a problem description, in the Bug Report tool: %s' % (upload_check[1])
                    log_utils.showResult(data, upload_check[1])
            elif controlId == self.kodi:
                filename = 'kodi.log'
                self.logfile = os.path.join(log_utils.LOGPATH, filename)
                self.logmsg = log_utils.readLog(self.logfile)

                if len(self.logmsg) < 10:
                    self.titlemsg = "%s: View Log Error" % control.addonName()
                    self.getControl(self.msg).setText("Log File Does Not Exists Or Is Too Large!")
                else:
                    self.titlemsg = "%s: %s" % (control.addonName(), filename.replace(log_utils.LOGPATH, ''))
                    self.getControl(self.title).setLabel(self.titlemsg)
                    self.getControl(self.msg).setText(log_utils.highlightText(self.logmsg))
                    self.setFocusId(self.scrollbar)
            elif controlId == self.kodiold:
                filename = 'kodi.old.log'
                self.logfile = os.path.join(log_utils.LOGPATH, filename)
                self.logmsg = log_utils.readLog(self.logfile)

                if len(self.logmsg) < 10:
                    self.titlemsg = "%s: View Log Error" % control.addonName()
                    self.getControl(self.msg).setText("Log File Does Not Exists!")
                else:
                    self.titlemsg = "%s: %s" % (control.addonName(), filename.replace(log_utils.LOGPATH, ''))
                    self.getControl(self.title).setLabel(self.titlemsg)
                    self.getControl(self.msg).setText(log_utils.highlightText(self.logmsg))
                    self.setFocusId(self.scrollbar)
            elif controlId == self.addonlog:
                filename = 'numbers.log'
                self.logfile = os.path.join(log_utils.LOGPATH, filename)
                self.logmsg = log_utils.readLog(self.logfile)

                if len(self.logmsg) < 10:
                    self.titlemsg = "%s: View Log Error" % control.addonName()
                    self.getControl(self.msg).setText("Log File Does Not Exists!")
                else:
                    self.titlemsg = "%s: %s" % (control.addonName(), filename.replace(log_utils.LOGPATH, ''))
                    self.getControl(self.title).setLabel(self.titlemsg)
                    self.getControl(self.msg).setText(log_utils.highlightText(self.logmsg))
                    self.setFocusId(self.scrollbar)

        def onAction(self, action):
            if action == themecontrol.ACTION_PREVIOUS_MENU or action == themecontrol.ACTION_NAV_BACK:
                self.close()


    viewer = LogViewver_Window('LogViewer.xml', themecontrol.skinModule(), themecontrol.skinTheme(), '1080i', logfile=logfile)
    viewer.doModal()
    del viewer
