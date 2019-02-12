# -*- coding: UTF-8 -*-
'''
    Updated and refactored by someone.
    Originally created by others.
'''
# Addon Name: MTB
# Addon id: plugin.video.movietheaterbutter
# Addon Provider: SomeBody

import inspect
import json
import os
import re
import sys
import urllib
import urllib2
import urlparse

import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs


def download(name, image, url):

    if url is None:
        return

    from resources.lib.modules import control

    try:
        headers = dict(urlparse.parse_qsl(url.rsplit('|', 1)[1]))
    except Exception:
        headers = dict('')

    url = url.split('|')[0]

    content = re.compile('(.+?)\sS(\d*)E\d*$').findall(name)
    transname = name.translate(None, '\/:*?"<>|').strip('.')
    levels = ['../../../..', '../../..', '../..', '..']

    if len(content) == 0:
        dest = control.setting('movie.download.path')
        dest = control.transPath(dest)
        for level in levels:
            try:
                control.makeFile(os.path.abspath(os.path.join(dest, level)))
            except Exception:
                pass
        control.makeFile(dest)
        dest = os.path.join(dest, transname)
        control.makeFile(dest)
    else:
        dest = control.setting('tv.download.path')
        dest = control.transPath(dest)
        for level in levels:
            try:
                control.makeFile(os.path.abspath(os.path.join(dest, level)))
            except Exception:
                pass
        control.makeFile(dest)
        transtvshowtitle = content[0][0].translate(None, '\/:*?"<>|').strip('.')
        dest = os.path.join(dest, transtvshowtitle)
        control.makeFile(dest)
        dest = os.path.join(dest, 'Season %01d' % int(content[0][1]))
        control.makeFile(dest)

    ext = os.path.splitext(urlparse.urlparse(url).path)[1][1:]
    if ext not in ['mp4', 'mkv', 'flv', 'avi', 'mpg']:
        ext = 'mp4'
    dest = os.path.join(dest, transname + '.' + ext)

    sysheaders = urllib.quote_plus(json.dumps(headers))

    sysurl = urllib.quote_plus(url)

    systitle = urllib.quote_plus(name)

    sysimage = urllib.quote_plus(image)

    sysdest = urllib.quote_plus(dest)

    script = inspect.getfile(inspect.currentframe())
    cmd = 'RunScript(%s, %s, %s, %s, %s, %s)' % (script, sysurl, sysdest, systitle, sysimage, sysheaders)

    xbmc.executebuiltin(cmd)


def getResponse(url, headers, size):
    try:
        if size > 0:
            size = int(size)
            headers['Range'] = 'bytes=%d-' % size

        req = urllib2.Request(url, headers=headers)

        resp = urllib2.urlopen(req, timeout=30)
        return resp
    except Exception:
        return None


def done(title, dest, downloaded):
    playing = xbmc.Player().isPlaying()

    text = xbmcgui.Window(10000).getProperty('GEN-DOWNLOADED')

    if len(text) > 0:
        text += '[CR]'

    if downloaded:
        text += '%s : %s' % (dest.rsplit(os.sep)[-1], '[COLOR forestgreen]Download succeeded[/COLOR]')
    else:
        text += '%s : %s' % (dest.rsplit(os.sep)[-1], '[COLOR red]Download failed[/COLOR]')

    xbmcgui.Window(10000).setProperty('GEN-DOWNLOADED', text)

    if (not downloaded) or (not playing):
        xbmcgui.Dialog().ok(title, text)
        xbmcgui.Window(10000).clearProperty('GEN-DOWNLOADED')


def doDownload(url, dest, title, image, headers):

    headers = json.loads(urllib.unquote_plus(headers))

    url = urllib.unquote_plus(url)

    title = urllib.unquote_plus(title)

    image = urllib.unquote_plus(image)

    dest = urllib.unquote_plus(dest)

    file = dest.rsplit(os.sep, 1)[-1]

    resp = getResponse(url, headers, 0)

    if not resp:
        xbmcgui.Dialog().ok(title, dest, 'Download failed', 'No response from server')
        return

    try:
        content = int(resp.headers['Content-Length'])
    except Exception:
        content = 0

    try:
        resumable = 'bytes' in resp.headers['Accept-Ranges'].lower()
    except Exception:
        resumable = False

    # print "Download Header"
    # print resp.headers
    if resumable:
        print "Download is resumable"

    if content < 1:
        xbmcgui.Dialog().ok(title, file, 'Unknown filesize', 'Unable to download')
        return

    size = 1024 * 1024
    mb = content / (1024 * 1024)

    if content < size:
        size = content

    total = 0
    notify = 0
    errors = 0
    count = 0
    resume = 0
    sleep = 0

    if xbmcgui.Dialog().yesno(title + ' - Confirm Download', file, 'Complete file is %dMB' % mb,
                              'Continue with download?', 'Confirm', 'Cancel') == 1:
        return

    print 'Download File Size : %dMB %s ' % (mb, dest)

    # f = open(dest, mode='wb')
    f = xbmcvfs.File(dest, 'w')

    chunk = None
    chunks = []

    while True:
        downloaded = total
        for c in chunks:
            downloaded += len(c)
        percent = min(100 * downloaded / content, 100)
        if percent >= notify:
            xbmc.executebuiltin(
                "XBMC.Notification(%s,%s,%i,%s)" %
                (title + ' - Download Progress - ' + str(percent) + '%', dest, 10000, image))

            print 'Download percent : %s %s %dMB downloaded : %sMB File Size : %sMB' % (
                str(percent) + '%', dest, mb, downloaded / 1000000, content / 1000000)

            notify += 10

        chunk = None
        error = False

        try:
            chunk = resp.read(size)
            if not chunk:
                if percent < 99:
                    error = True
                else:
                    while len(chunks) > 0:
                        c = chunks.pop(0)
                        f.write(c)
                        del c

                    f.close()
                    print '%s download complete' % (dest)
                    return done(title, dest, True)

        except Exception, e:
            print str(e)
            error = True
            sleep = 10
            errno = 0

            if hasattr(e, 'errno'):
                errno = e.errno

            if errno == 10035:  # 'A non-blocking socket operation could not be completed immediately'
                pass

            if errno == 10054:  # 'An existing connection was forcibly closed by the remote host'
                errors = 10  # force resume
                sleep = 30

            if errno == 11001:  # 'getaddrinfo failed'
                errors = 10  # force resume
                sleep = 30

        if chunk:
            errors = 0
            chunks.append(chunk)
            if len(chunks) > 5:
                c = chunks.pop(0)
                f.write(c)
                total += len(c)
                del c

        if error:
            errors += 1
            count += 1
            print '%d Error(s) whilst downloading %s' % (count, dest)
            xbmc.sleep(sleep*1000)

        if (resumable and errors > 0) or errors >= 10:
            if (not resumable and resume >= 50) or resume >= 500:
                # Give up!
                print '%s download canceled - too many error whilst downloading' % (dest)
                return done(title, dest, False)

            resume += 1
            errors = 0
            if resumable:
                chunks = []
                # create new response
                print 'Download resumed (%d) %s' % (resume, dest)
                resp = getResponse(url, headers, total)
            else:
                # use existing response
                pass


if __name__ == '__main__':
    if 'downloader.py' in sys.argv[0]:
        doDownload(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
