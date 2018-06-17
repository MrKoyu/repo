#      Copyright (C) 2015 Justin Mills
#      
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import xbmcgui, utils

addon_id = 'script.ivueguide'
dlg = xbmcgui.Dialog()


def setUrl():
	user = utils.set_setting(addon_id, 'userurl', 'http://ivuetvguide.com/ivueguide/') 
	url = utils.set_setting(addon_id, 'mainurl', 'http://ivuetvguide.com/ivueguide/')
	logos = utils.set_setting(addon_id, 'logos', 'http://raw.githubusercontent.com/totaltec2014/ivue2/master/logos/')
