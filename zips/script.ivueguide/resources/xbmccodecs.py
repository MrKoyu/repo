import xbmc
import xbmcgui, os
import json
import utils

databasePath = xbmc.translatePath('special://profile/Database')
addons27 = os.path.join(databasePath, 'Addons27.db')

jsonGetCodec = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue", "params":{"setting":"videoplayer.usemediacodec"}, "id":1}'
jsonSetCodec = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"videoplayer.usemediacodec", "value":%s},"id":1}'

codec = json.loads(xbmc.executeJSONRPC(jsonGetCodec))["result"]["value"]

jsonGetSurfaceCodec = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue", "params":{"setting":"videoplayer.usemediacodecsurface"}, "id":1}'
jsonSetSurfaceCodec = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"videoplayer.usemediacodecsurface", "value":%s},"id":1}'

surfaceCodec = json.loads(xbmc.executeJSONRPC(jsonGetSurfaceCodec))["result"]["value"]

if codec == False:
    media = 'Media Codec:  [COLOR red]Disabled[/COLOR]'
else: 
    media = 'Media Codec:  [COLOR lime]Enabled[/COLOR]'

if surfaceCodec == False:
    surfacemedia = 'Media Codec Surface:  [COLOR red]Disabled[/COLOR]'
else: 
    surfacemedia = 'Media Codec Surface:  [COLOR lime]Enabled[/COLOR]'

def setSurfaceCodec():
    if surfaceCodec == False:
        xbmc.executeJSONRPC(jsonSetSurfaceCodec % "true")
        utils.dialog.ok('iVue', "Media Codec (Surface) Enabled", "Please restart ivue for changes to take affect")
    else:
        xbmc.executeJSONRPC(jsonSetSurfaceCodec  % "false")
        utils.dialog.ok('iVue', "Media Codec (Surface) Disabled", "Please restart ivue for changes to take affect")

def setCodec():
    if codec == False:
        xbmc.executeJSONRPC(jsonSetCodec % "true")
        utils.dialog.ok('iVue', "Media Codec Enabled", "Please restart ivue for changes to take affect")
    else:
        xbmc.executeJSONRPC(jsonSetCodec  % "false")
        utils.dialog.ok('iVue', "Media Codec Disabled", "Please restart ivue for changes to take affect")

