import xbmc
import xbmcgui
import xbmcaddon
import os
import streaming
import sqlite3

ADDONID = 'script.ivueguide'
ADDON = xbmcaddon.Addon(ADDONID)

profilePath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
databasePath = os.path.join(profilePath, 'master.db')
conn = sqlite3.connect(databasePath, detect_types=sqlite3.PARSE_DECLTYPES)    	
c = conn.cursor()
player = xbmc.Player()

program = sys.argv[1]
channelTitle = sys.argv[2]
channelName = sys.argv[3]
description = sys.argv[4]

programTitle  = '[COLOR orange][B]%s[/B][/COLOR]' % program.replace(' (?)', '')

def askUser():

    dialog = xbmcgui.Dialog() 
    yes=dialog.yesno("Reminder", programTitle+' '+description, 'Would you like to watch it?', nolabel='Dismiss', yeslabel='Watch', autoclose=10 * 1000);

    if yes:	
        getStreams(channelTitle)
    else: 
        pass

def getStreams(channel):
    dialog = xbmcgui.Dialog()
    result = streaming.StreamsService(ADDON).detectReminder(channel)

    if len(result) < 1:
        dialog.ok('Sorry, we could not detect a stream for %s' % channel, '', 'Please use iVue creator to link more streams')
        return None

    if not getCustomStreamUrl(channelName):

        import gui
        r = gui.ChooseStreamAddonDialog(result)
        r.doModal()
        if r.stream is not None:
            if ADDON.getSetting('ignore.stream') == 'false':
                setCustomStreamUrl(channelName,r.stream)
            playChannel(r.stream)
    else:
        playChannel(getCustomStreamUrl(channelName))


def playChannel(url):
    if url:

        if url.isdigit():
            command = \
                '{"jsonrpc": "2.0", "id":"1", "method": "Player.Open","params":{"item":{"channelid":%s}}}' \
                % url
            xbmc.executeJSONRPC(command)
            return

        if url[0:9] == 'plugin://':
            if ADDON.getSetting('alternative.playback') == 'true':
                xbmc.executebuiltin('XBMC.RunPlugin(%s)' % url)
            elif ADDON.getSetting('enable.osd') == 'true' and ADDON.getSetting('alternative.playback') != 'true':
                player.play(item=url, windowed=True)
            else:
                player.play(item=url)
        else:
            player.play(item=url)

    return url is not None

def setCustomStreamUrl(channelId, stream_url):
    if stream_url is not None:
        c.execute("UPDATE channels SET stream_url=? WHERE id=?", [stream_url.decode('utf-8', 'ignore'), channelId])
        c.execute("DELETE FROM custom_stream_url WHERE channel=?", [channelId])
        c.execute("INSERT INTO custom_stream_url(channel, stream_url) VALUES(?, ?)",
                  [channelId, stream_url.decode('utf-8', 'ignore')])
        conn.commit()
        c.close()


def getCustomStreamUrl(channelId):
    c.execute("SELECT stream_url FROM custom_stream_url WHERE channel=?", [channelId])
    stream_url = c.fetchone()
    conn.commit()

    if stream_url:
        return stream_url[0]
    else:
        return None


if __name__ == '__main__':
    askUser()
