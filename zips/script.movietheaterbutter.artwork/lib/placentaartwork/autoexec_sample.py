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


import xbmcvfs,xbmcgui
from movietheaterbutterartwork import theme_setter

def main():
    try:
        theme_setter.Apply_Theme('Collusion')
        xbmcvfs.delete('special://userdata/autoexec.py')
    except Exception, e:
        xbmcvfs.delete('special://userdata/autoexec.py')

if __name__ == '__main__':
    main()