import xbmcaddon
import xbmc
import base64
import sys
Decode       = base64.decodestring

def WebBrowse(url):
  #################
  import webbrowser
  ##################################################
  BrowseOther     = webbrowser.open
  EBI           = xbmc.executebuiltin
  Cond           = lambda x: xbmc.getCondVisibility(str(x))
  BrowseAndroid    = lambda x:EBI(Decode('U3RhcnRBbmRyb2lkQWN0aXZpdHkoLGFuZHJvaWQuaW50ZW50LmFjdGlvbi5WSUVXLCwlcyk=')%(x))
  ##################################################
  Android = Decode('U3lzdGVtLlBsYXRmb3JtLkFuZHJvaWQ=')
  ##################################################
  if Cond(Android):BrowseAndroid((url))
  else:BrowseOther((url))
  ##################################################

def WebKeyboard(Heading=xbmcaddon.Addon().getAddonInfo(Decode('bmFtZQ=='))):
  kb = xbmc.Keyboard ('http://', Heading)
  kb.doModal()
  if (kb.isConfirmed()):
    return kb.getText()

#try:
  #if 'http://' in sys.argv[1]:
   # WebBrowse(sys.argv[1])
  #else:
    #WebBrowse(WebKeyboard('Type Your URL'))
#except:
  #WebBrowse(WebKeyboard('Type Your URL'))