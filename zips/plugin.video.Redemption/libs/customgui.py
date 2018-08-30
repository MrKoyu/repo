import _Edit
import koding
import shutil
import xbmc
import xbmcgui
from libs._addon import *

Dolog = koding.dolog
header_base_png = '{}_{}_square.png'.format(_Edit.guiHeaderBaseColor,_Edit.guiHeaderBaseTrans)
body_base_png   = '{}_{}_square.png'.format(_Edit.guiBodyBaseColor,_Edit.guiBodyBaseTrans)

def PopUpDialog(header,text):
    try:
        shutil.copy(addon_icon,addon_media)
    except:
        Dolog('Unable to copy icon.png to media folder',line_info=True)
        pass
    d=_PopUpDialog('PopUpDialog.xml',addon_path,header=header,text=text,header_base_png=header_base_png,body_base_png=body_base_png)
    d.doModal()
    del d 

class _PopUpDialog(xbmcgui.WindowXMLDialog):
    def __init__(self,*args,**kwargs):
        self.WINDOW   = xbmcgui.Window(10000)
        self.header   = kwargs.get('header',addon_name)
        self.text     = kwargs.get('text','Text String is Missing')
        self.header_base_png = kwargs.get('header_base_png','white_50_square.png')
        self.body_base_png   = kwargs.get('body_base_png','white_50_square.png')
        self.WINDOW.setProperty('HEADER',self.header)
        self.WINDOW.setProperty('TEXT',self.text)
        self.WINDOW.setProperty('HEAD_BASE_PNG',self.header_base_png)
        self.WINDOW.setProperty('HEADCOLOR',_Edit.guiHeaderColor)
        self.WINDOW.setProperty('HEADTXTCOLOR',_Edit.guiHeaderTxtColor)
        self.WINDOW.setProperty('HEADTXTSHAD',_Edit.guiHeaderTxtShadow)
        self.WINDOW.setProperty('BODY_BASE_PNG',self.body_base_png)
        self.WINDOW.setProperty('BODYCOLOR',_Edit.guiBodyColor)
        self.WINDOW.setProperty('BODYTXTCOLOR',_Edit.guiBodyTxtColor)
        self.WINDOW.setProperty('BODYTXTSHAD',_Edit.guiBodyTxtShadow)
        self.WINDOW.setProperty('SLIDERBARBASECOLOR',_Edit.guiSliderBarColor)
        self.WINDOW.setProperty('SLIDERBARFOCUSCOLOR',_Edit.guiSliderColorFocus)
        self.WINDOW.setProperty('SLIDERBARNOFOCUSCOLOR',_Edit.guiSliderColorNoFocus)



def OkDialog(header,text):
        try:
            shutil.copy(addon_icon,addon_media)
        except:
            Dolog('Unable to copy icon.png to media folder',line_info=True)
            pass
        d=_OkDialog('OkDialog.xml',addon_path,header=header,text=text,header_base_png=header_base_png,body_base_png=body_base_png)
        d.doModal()
        del d 


class _OkDialog(xbmcgui.WindowXMLDialog):

    def __init__(self,*args,**kwargs):
        self.WINDOW          = xbmcgui.Window(10000)
        self.header          = kwargs.get('header',addon_name)
        self.text            = kwargs.get('text','Text String is Missing')
        self.header_base_png = kwargs.get('header_base_png','white_50_square.png')
        self.body_base_png   = kwargs.get('body_base_png','white_50_square.png')
        self.WINDOW.setProperty('HEADER',self.header)
        self.WINDOW.setProperty('TEXT',self.text)
        self.WINDOW.setProperty('HEAD_BASE_PNG',self.header_base_png)
        self.WINDOW.setProperty('HEADCOLOR',_Edit.guiHeaderColor)
        self.WINDOW.setProperty('HEADTXTCOLOR',_Edit.guiHeaderTxtColor)
        self.WINDOW.setProperty('HEADTXTSHAD',_Edit.guiHeaderTxtShadow)
        self.WINDOW.setProperty('BODY_BASE_PNG',self.body_base_png)
        self.WINDOW.setProperty('BODYCOLOR',_Edit.guiBodyColor)
        self.WINDOW.setProperty('BODYTXTCOLOR',_Edit.guiBodyTxtColor)
        self.WINDOW.setProperty('BODYTXTSHAD',_Edit.guiBodyTxtShadow)
        self.WINDOW.setProperty('BUTTONFOCUSCOLOR',_Edit.guiButtonColorFocus)
        self.WINDOW.setProperty('BUTTONCOLOR',_Edit.guiButtonColorNoFocus)
        self.WINDOW.setProperty('BUTTONTXTCOLOR',_Edit.guiButtonTxtColor)

 