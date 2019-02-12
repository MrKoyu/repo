# -*- coding: UTF-8 -*-
'''
    Updated and refactored by someone.
    Originally created by others.
'''
# Addon Name: MTB
# Addon id: plugin.video.movietheaterbutter
# Addon Provider: SomeBody


def get(version):
    try:
        import xbmc, xbmcgui, xbmcaddon, xbmcvfs

        f = xbmcvfs.File(xbmcaddon.Addon().getAddonInfo('changelog'))
        text = f.read()
        f.close()

        label = '%s - %s' % (xbmc.getLocalizedString(24054), xbmcaddon.Addon().getAddonInfo('name'))

        id = 10147

        xbmc.executebuiltin('ActivateWindow(%d)' % id)
        xbmc.sleep(100)

        win = xbmcgui.Window(id)

        retry = 50
        while (retry > 0):
            try:
                xbmc.sleep(10)
                win.getControl(1).setLabel(label)
                win.getControl(5).setText(text)
                retry = 0
            except Exception:
                retry -= 1

        return '1'
    except Exception:
        return '1'


