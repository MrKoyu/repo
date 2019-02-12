# -*- coding: utf-8 -*-

'''
    Some Add-on

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


#######################################################################
#Import Modules Section
import xbmc,xbmcaddon
import os,re
#######################################################################

def Apply_Theme(new_theme):
    try:
        __settings__ = xbmcaddon.Addon(id='plugin.video.movietheaterbutter')
        __settings__.setSetting("appearance.1", new_theme)
        print '[MTB] #### Theme Setter: Theme Set To ' + str(new_theme)
    except:
        pass
