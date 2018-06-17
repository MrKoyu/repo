import _Edit
from xbmcaddon import Addon
from xbmc import translatePath
from os.path import join


# ADDON FUNCTIONS AND CLASSES
addon           = addon = Addon()
addoninfo       = addon.getAddonInfo
setting         = addon.getSetting
setting_true    = lambda x: bool(True if setting(str(x)) == "true" else False)
setting_set     = addon.setSetting

# ADDON VARIABLES

#ADDON SPECIFIC VARIABLES
addon_version   = addoninfo('version')
addon_name      = addoninfo('name')
addon_id        = addoninfo('id')
addon_icon      = addoninfo("icon")
addon_fanart    = addoninfo("fanart")

#ADDON PATH VARIABLES
addon_profile   = translatePath(addoninfo('profile').decode('utf-8'))
addon_path      = translatePath(addoninfo('path').decode('utf-8'))	
addon_favorites = join(addon_profile, 'favorites')
addon_history   = join(addon_profile, 'history')
addon_revision  = join(addon_profile, 'list_revision')
addon_source    = join(addon_profile, 'source_file')
addon_resources = join(addon_path, 'resources')
addon_art       = join(addon_resources,'art')

#ADDON SETTINGS
setting_debug   = setting('debug')
setting_resolve = setting("resolverURL")
setting_tmdb    = setting('tmdb_key')

#ADDON ARTWORK
fanart_DailyMotion      = addon_fanart                          if _Edit.DailyMotionFanart  == "" else _Edit.DailyMotionFanart
fanart_Favorite         = addon_fanart                          if _Edit.FavoriteFanart     == "" else _Edit.FavoriteFanart
fanart_History          = addon_fanart                          if _Edit.HistoryFanart      == "" else _Edit.HistoryFanart
fanart_Search           = addon_fanart                          if _Edit.SearchFanart       == "" else _Edit.SearchFanart
fanart_Setting          = addon_fanart                          if _Edit.SettingFanart      == "" else _Edit.SettingFanart
fanart_tmdb             = addon_fanart                          if _Edit.TmdbFanart         == "" else _Edit.TmdbFanart
fanart_YouTube          = addon_fanart                          if _Edit.YouTubeFanart      == "" else _Edit.YouTubeFanart
icon_DailyMotion        = join(addon_art,'dailymotion.png')     if _Edit.DailyMotionIcon    == "" else _Edit.DailyMotionIcon 
icon_Favorite           = join(addon_art,'favorite.png')        if _Edit.FavoriteIcon       == "" else _Edit.FavoriteIcon
icon_History            = join(addon_art,'history.png')         if _Edit.HistoryIcon        == "" else _Edit.HistoryIcon
icon_nextpage           = join(addon_art,'nextpage.png')        if _Edit.NextPageIcon       == "" else _Edit.NextPageIcon
icon_Search             = join(addon_art,'search.png')          if _Edit.SearchIcon         == "" else _Edit.SearchIcon
icon_Setting            = join(addon_art,'tools.png')           if _Edit.SettingIcon        == "" else _Edit.SettingIcon
icon_tmdb               = join(addon_art,'tmdb.png')            if _Edit.TmdbIcon           == "" else _Edit.TmdbIcon
icon_YouTube            = join(addon_art,'youtube.png')         if _Edit.YouTubeIcon        == "" else _Edit.YouTubeIcon
