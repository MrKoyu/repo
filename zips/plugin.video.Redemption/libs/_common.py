import byb_modules as BYB 
import datetime
import _Edit
import koding
import xbmc
from ._addon import *

from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP

Dolog   = koding.dolog
OpenURL = koding.Open_URL

def ChannelColor(string):
	ColorList = []
	color1 = _Edit.ChannelTxtColor1
	color2 = _Edit.ChannelTxtColor2
	split  = _Edit.ChannelTxtSplit
	spoint = _Edit.ChannelTxtSpoint
	if color1 != '': 
		ColorList.append(color1) 
	else: pass
	if color2 != '': 
		ColorList.append(color2) 
	else: pass
	if color1 == '' and color2 == '':
		return string
	if split == '':
		split = None
	if spoint == '':
		spoint = None
	elif spoint != '':
		spoint = int(spoint)
	string = BYB.String_Color(string,ColorList,split,spoint)
	return string

def ItemColor(string):
	ColorList = []
	color1 = _Edit.ItemTxtColor1
	color2 = _Edit.ItemTxtColor2
	split  = _Edit.ItemTxtSplit
	spoint = _Edit.ItemTxtSpoint
	if color1 != '': 
		ColorList.append(color1) 
	else: pass
	if color2 != '': 
		ColorList.append(color2) 
	else: pass
	if color1 == '' and color2 == '':
		return string
	if split == '':
		split = None
	if spoint == '':
		spoint = None
	elif spoint != '':
		spoint = int(spoint)
	string = BYB.String_Color(string,ColorList,split,spoint)
	return string
	
def SingleColor(string,color):
	ColorList = []
	if color != '':
		ColorList.append(color)
		string = BYB.String_Color(string,ColorList)
	else:
		string = string
	return string

def Delimiter():
	delimiter = _Edit.TxtDelimiter
	spaces    = _Edit.TxtDelimiterAddSpaces
	color     = _Edit.TxtDelimiterColor
	Spaces    = _Edit.TxtDelimiterAddSpacesAmount
	if spaces.lower() == 'both':
		delimiter = delimiter.center(Spaces*2)
	elif spaces.lower() == 'after':
		delimiter = delimiter.ljust(Spaces)
	elif spaces.lower() == 'before':
		delimiter = delimiter.rjust(Spaces) 
	if color == '' and spaces == '':
		string = delimiter
	elif color != '':
		string = '[COLOR '+str(color)+']'+delimiter+'[/COLOR]'
	elif color == '':
		string = delimiter
	return string




def PopUpNotice():
	raw_notice = OpenURL(_Edit.PopUpNotice,timeout=500,cookiejar=BYB.cookie_name_create(_Edit.PopUpNotice))
	xml_notice = BeautifulSOAP(raw_notice, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
	BYB.headers_create(addon_cache,table='pop_message',headers='popupdate,displaydate')
	show = False
	if isinstance(xml_notice,BeautifulSOAP):
		if len(xml_notice('notify'))>0:
			NotifingData = xml_notice('notify')
			for NotifyData in NotifingData:
				message = ''
				date = None
				header = ''
				freq = ''
				try:
					header = NotifyData('header')[0].string
					freq = NotifyData('freq')[0].string
					message = NotifyData('message')[0].string
					date = NotifyData('date')[0].string
				except:pass
	DisplayDateCheck = BYB.check_is_in_DB_table(addon_cache,table='pop_message',row_header='displaydate',check_item=datetime.datetime.today().strftime('%Y-%m-%d'))
	OnceDisplayCheck = BYB.check_is_in_DB_table(addon_cache,table='pop_message',row_header='popupdate',check_item=date)
	BYB.write_to_DB(addon_cache,table='pop_message',headers='popupdate,displaydate',items=(date,datetime.datetime.today().strftime('%Y-%m-%d')))
	Dolog(datetime.datetime.today().strftime('%Y-%m-%d'),line_info=True)
	Dolog(BYB.check_is_in_DB_table(addon_cache,table='pop_message',row_header='displaydate',check_item=datetime.datetime.today().strftime('%Y-%m-%d')),line_info=True)
	if freq == 'every':
		show = True
	elif freq =='daily' and DisplayDateCheck==False:
		Dolog('show daily',line_info=True)
		show = True
	elif freq == 'once' and OnceDisplayCheck==False:
		show = True
	else:
		Dolog('key word for freq wrong either every,daily,once')
	if show == True:
		if len(message) > 0:
			try:
				from libs import customgui
				customgui.PopUpDialog(header=header,text = message)
			except:
				BYB.Notify(title='Error',message='Error in displaying Pop Up Message')
		else:
			BYB.Notify(title='Error',message='Error in displaying Pop Up Message')
	else:
		pass
		