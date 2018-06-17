# -*- coding: utf-8 -*-
#
# FTV Guide
# Copyright (C) 2015 Thomas Geppert [bluezed]
# bluezed.apps@gmail.com
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
import xbmc, xbmcgui
import os
import urllib, urllib2
import datetime
import zlib, utils, base64, time, zipfile, shutil
import base64
addon_id = 'script.ivueguide'
databasePath = xbmc.translatePath('special://profile/addon_data/script.ivueguide')

for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "tmp" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				pass
		else:
			continue

for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "tempfile.zip" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				pass
		else:
			continue

def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
	try:
		percent = min((numblocks*blocksize*100)/filesize, 100)
		print 'done' +str(percent)+'%'
		dp.update(percent)
	except:
		percent = 100
		dp.update(percent)
	if dp.iscanceled():
		raise Exception("Cancelled")
		dp.close()

def extract(_in, _out):
	dp = xbmcgui.DialogProgress()
	zin    = zipfile.ZipFile(_in,  'r')
	nFiles = float(len(zin.infolist()))
	count  = 0
	for item in zin.infolist():
		count += 1
		update = count / nFiles * 100
		zin.extract(item, _out)

class FileFetcher(object):
    INTERVAL_ALWAYS = 0
    INTERVAL_12 = 1
    INTERVAL_24 = 2
    INTERVAL_48 = 3
    INTERVAL_72 = 4
    INTERVAL_96 = 5
    INTERVAL_120 = 6

    FETCH_ERROR = -1
    FETCH_NOT_NEEDED = 0
    FETCH_OK = 1
    
    basePath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ivueguide'))
    filePath = ''
    fileUrl = ''
    addon = None
    def __init__(self, fileName, addon):

        folderPath = utils.folder()

	self.addon = addon
	self.filePath = os.path.join(self.basePath, fileName)

	if fileName == utils.get_setting(addon_id,'xmltv.url'):		
		self.fileUrl = fileName
		self.fileName = fileName.split('/')[-1]
		self.filePath = os.path.join(self.basePath, 'custom.xml')
		
	elif fileName == utils.get_setting(addon_id,'xmltv.url') and fileName.endswith(".zip"):		
		self.fileUrl = fileName
		self.fileName = fileName.split('/')[-1]
		self.filePath = os.path.join(self.basePath, 'custom.xml')
		
	elif fileName == utils.get_setting(addon_id,'sub.xmltv.url'):		
		self.fileUrl = fileName
		self.fileName = fileName.split('/')[-1]
		self.filePath = os.path.join(self.basePath, utils.get_setting(addon_id,'sub.xmltv')+'.xml')
		
	else:
		self.fileUrl = folderPath + fileName.replace('.xml', '.zip')
        # make sure the folder is actually there already!
        if not os.path.exists(self.basePath):
            os.makedirs(self.basePath)

    def fetchFile(self):
        retVal = self.FETCH_NOT_NEEDED
        fetch = False
        if not os.path.exists(self.filePath):  # always fetch if file doesn't exist!
            fetch = True
        else:
            interval = int(self.addon.getSetting('xmltv.interval'))
            if interval <> self.INTERVAL_ALWAYS:
                modTime = datetime.datetime.fromtimestamp(os.path.getmtime(self.filePath))
                td = datetime.datetime.now() - modTime
                # need to do it this way cause Android doesn't support .total_seconds() :(
                diff = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10 ** 6
                if ((interval == self.INTERVAL_12 and diff >= 43200) or
                        (interval == self.INTERVAL_24 and diff >= 86400) or
                        (interval == self.INTERVAL_48 and diff >= 172800) or
                        (interval == self.INTERVAL_72 and diff >= 259200) or
                        (interval == self.INTERVAL_96 and diff >= 345600) or
                        (interval == self.INTERVAL_120 and diff >= 432000)):
                    fetch = True
            else:
                fetch = True

        if fetch:

            tmpFile = os.path.join(self.basePath, 'tmp')
            f = open(tmpFile, 'wb')

            try:
                if self.fileUrl == utils.get_setting(addon_id,'xmltv.url') and self.fileUrl.endswith('.zip'):
                    dp = xbmcgui.DialogProgress()
                    zipPath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ivueguide', 'custom_tempfile.zip'))
                    zipurl = self.fileUrl
                    dp.create("iVue","Downloading guide data",'')
                    urllib.urlretrieve(zipurl,zipPath,lambda nb, bs, fs, url=zipurl: _pbhook(nb,bs,fs,zipurl,dp))
                    f.close()

                elif self.fileUrl.endswith('.zip'):
                    dp = xbmcgui.DialogProgress()
                    zipPath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ivueguide', 'tempfile.zip'))
                    zipurl = self.fileUrl
                    dp.create("iVue","Downloading guide data",'')
                    urllib.urlretrieve(zipurl,zipPath,lambda nb, bs, fs, url=zipurl: _pbhook(nb,bs,fs,zipurl,dp))
                    f.close()

                else:
                    request = urllib2.Request(self.fileUrl)
                    tmpData = urllib2.urlopen(request)
                    data = tmpData.read()
                    if tmpData.info().get('content-encoding') == 'gzip':
                        data = zlib.decompress(data, zlib.MAX_WBITS + 16)
                    f.write(data)
                    f.close()


            except urllib2.HTTPError, e:
		    if e.code == 401:
                        utils.notify(addon_id, 'Connection Error !!! Please Try Again')
		    else:
		        utils.notify(addon_id, e)  

            basePath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ivueguide'))
            zipPath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ivueguide', 'tempfile.zip'))
            customzipPath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ivueguide', 'custom_tempfile.zip'))
            tempzipPath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ivueguide', 'custom_tempfile'))
            customPath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ivueguide', 'custom.xml'))
            if os.path.exists(zipPath):
                if os.path.exists(self.filePath):
                    os.remove(self.filePath)
                os.remove(tmpFile)

                extract(zipPath, basePath)
                os.remove(zipPath)
                retVal = self.FETCH_OK
                xbmc.log('[script.ivueguide] file %s was downloaded' % self.filePath, xbmc.LOGDEBUG)

            if os.path.exists(customzipPath):
                if os.path.exists(self.filePath):
                    os.remove(self.filePath)
                os.remove(tmpFile)

                extract(customzipPath, tempzipPath)
                for filename in os.listdir(tempzipPath):
                    if os.path.exists(customPath):
                        os.remove(customPath)
                    os.rename(os.path.join(tempzipPath, filename), customPath)
                    shutil.rmtree(tempzipPath)        
                os.remove(customzipPath)
                retVal = self.FETCH_OK
                xbmc.log('[script.ivueguide] file %s was downloaded' % self.filePath, xbmc.LOGDEBUG)

            if os.path.exists(tmpFile):
                if os.path.getsize(tmpFile) > 256:
                    if os.path.exists(self.filePath):
                        os.remove(self.filePath)
                    os.rename(tmpFile, self.filePath)
                    retVal = self.FETCH_OK
                    xbmc.log('[script.ivueguide] file %s was downloaded' % self.filePath, xbmc.LOGDEBUG)
                else:
                    retVal = self.FETCH_ERROR
        return retVal