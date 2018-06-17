import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, sys, time, xbmcvfs


log_path   =  xbmc.translatePath('special://logpath/')

mode='run_log'

def Log_Viewer():
    log_path = xbmc.translatePath('special://logpath')
    
    xbmc_log_path = os.path.join(log_path, 'kodi.log')
    if os.path.exists(xbmc_log_path)==True: Text_Boxes('Kodi Log', xbmc_log_path)
    
    xbmc_log_path = os.path.join(log_path, 'xbmc.log')
    if os.path.exists(xbmc_log_path)==True: Text_Boxes('xbmc Log', xbmc_log_path)
    
    xbmc_log_path = os.path.join(log_path, 'tvmc.log')
    if os.path.exists(xbmc_log_path)==True: Text_Boxes('tvmc Log', xbmc_log_path)    

    xbmc_log_path = os.path.join(log_path, 'fmc.log')
    if os.path.exists(xbmc_log_path)==True: Text_Boxes('fmc Log', xbmc_log_path)

    xbmc_log_path = os.path.join(log_path, 'smc.log')
    if os.path.exists(xbmc_log_path)==True: Text_Boxes('smc Log', xbmc_log_path)



def Log_Viewer_ver():
    log_path = xbmc.translatePath('special://logpath')
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if version < 14:
        log = os.path.join(log_path, 'xbmc.log')
        Text_Boxes('XBMC Log', log)
    else:
        log = os.path.join(log_path, 'kodi.log')
        Text_Boxes('Kodi Log', log)



def Text_Boxes(heading,anounce):
  class TextBox():
    WINDOW=10147
    CONTROL_LABEL=1
    CONTROL_TEXTBOX=5
    def __init__(self,*args,**kwargs):
      xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, ))
      self.win=xbmcgui.Window(self.WINDOW)
      xbmc.sleep(500)
      self.setControls()
    def setControls(self):
      self.win.getControl(self.CONTROL_LABEL).setLabel(heading)
      try: f=open(anounce); text=f.read()
      except: text=anounce
      self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
      return
  TextBox()  


if mode=='run_log' : Log_Viewer()

