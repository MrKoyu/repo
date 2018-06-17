# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import xbmc
import xbmcgui
from ..Utils import *
from ..TheMovieDB import *
from ..WindowManager import wm
from ..OnClickHandler import OnClickHandler
from .. import VideoPlayer
PLAYER = VideoPlayer.VideoPlayer()
ch = OnClickHandler()


class DialogBaseInfo(object):
    ACTION_PREVIOUS_MENU = [92, 9]
    ACTION_EXIT_SCRIPT = [13, 10]

    def __init__(self, *args, **kwargs):
        super(DialogBaseInfo, self).__init__(*args, **kwargs)
        self.logged_in = check_login()
        self.dbid = kwargs.get('dbid')
        self.bouncing = False
        self.data = None
        self.yt_listitems = []
        self.info = {}

    def onInit(self, *args, **kwargs):
        super(DialogBaseInfo, self).onInit()
        HOME.setProperty("ImageColor", self.info.get('ImageColor', ""))
        self.window = xbmcgui.Window(self.window_id)
        self.window.setProperty("type", self.type)
        self.window.setProperty("tmdb_logged_in", self.logged_in)
        # present for jurialmunkey
        HOME.setProperty("ExtendedInfo_fanart", self.info.get("fanart", ""))

    def onAction(self, action):
        ch.serve_action(action, self.getFocusId(), self)

    def onClick(self, control_id):
        ch.serve(control_id, self)

    def onFocus(self, control_id):
        if control_id == 20000:
            if not self.bouncing:
                self.bounce("up")
            self.setFocusId(self.last_focus)
            self.last_focus = control_id
        elif control_id == 20001:
            if not self.bouncing:
                self.bounce("down")
            self.setFocusId(self.last_focus)
            self.last_focus = control_id
        else:
            self.last_focus = control_id

    @run_async
    def bounce(self, identifier):
        self.bouncing = True
        self.window.setProperty("Bounce.%s" % identifier, "true")
        xbmc.sleep(200)
        self.window.clearProperty("Bounce.%s" % identifier)
        self.bouncing = False

    def fill_lists(self):
        for container_id, listitems in self.listitems:
            try:
                self.getControl(container_id).reset()
                self.getControl(container_id).addItems(create_listitems(listitems))
            except:
                log("Notice: No container with id %i available" % container_id)

        @ch.action("contextmenu", 150)
        @ch.action("contextmenu", 250)
        def right_click_sets_and_similar(self):
            item_id = self.listitem.getProperty("id")
            dbid = self.listitem.getProperty("dbid")
            if self.type == "TVShow":
                tmdbids = get_tvshow_ids(item_id)
                tvdb = tmdbids['tvdb_id']
                if dbid: listitems = [LANG(208)]
                else: listitems = [LANG(13401) % LANG(36902)]
            else:
                imdb = get_imdb_id_from_movie_id(item_id)
                listitems = [LANG(208)]
            if dbid: listitems += [LANG(32233)]
            else: listitems += [LANG(32232)]
            if self.logged_in:
                listitems += [LANG(14076)]
                listitems += [LANG(32107)]
            selection = xbmcgui.Dialog().select(heading=LANG(32151), list=listitems)
            if selection == 0:
                if self.type == "TVShow":
                    if dbid:
                        show_playlist = xbmc.translatePath("special://profile/playlists/video/%s.xsp" % tvdb)
                        if os.path.exists(show_playlist):
                            xbmc.executebuiltin("PlayMedia("+show_playlist+")")
                            self.close()
                        else:
                            xbmc.executebuiltin("ActivateWindow(videos,videodb://tvshows/titles/%s/)" % dbid)
                            self.close()
                    else:
                        xbmc.executebuiltin("ActivateWindow(10025,plugin://plugin.video.metalliq-forqed/tv/tvdb/%s,return)" % tvdb)
                        self.close()
                else:
                    if dbid: url = "temp"
                    else:
                        dbid = 0
                        url = "plugin://plugin.video.metalliq-forqed/movies/play/tmdb/%s/%s" % (item_id, SETTING("player_main_movie"))
                    PLAYER.qlickplay(url, listitem=None, window=self, dbid=dbid)
            if selection == 1:
                if self.type == "TVShow":
                    if dbid:
                        show_path = xbmc.translatePath("special://profile/addon_data/plugin.video.metalliq-forqed/TVShows/%s" % tvdb)
                        if os.path.exists(show_path):
                            try:
                                shutil.rmtree(show_path)
                                xbmc.executebuiltin("RunScript(script.extendedinfo,info=afteradd)")
                                xbmc.executebuiltin("CleanLibrary(video)")
                            except: pass
                    else:
                        xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq-forqed/movies/add_to_library/tmdb/%s)" % item_id)
                        xbmc.executebuiltin("RunScript(script.extendedinfo,info=afteradd)")
                else:
                    if dbid:
                        movie_path = xbmc.translatePath("special://profile/addon_data/plugin.video.metalliq-forqed/Movies/%s" % imdb)
                        if os.path.exists(movie_path):
                            try:
                                shutil.rmtree(movie_path)
                                xbmc.executebuiltin("RunScript(script.extendedinfo,info=afteradd)")
                                xbmc.executebuiltin("CleanLibrary(video)")
                            except: pass
                    else:
                        xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq-forqed/movies/add_to_library/tmdb/%s)" % item_id)
                        xbmc.executebuiltin("RunScript(script.extendedinfo,info=afteradd)")
            if selection == 2:
                change_fav_status(media_id=item_id, media_type="movie", status=str(not bool(self.account_states["favorite"])).lower())
                self.update_states()
            if selection == 3:
                xbmc.executebuiltin("ActivateWindow(busydialog)")
                account_lists = get_account_lists()
                listitems = ["%s (%i)" % (i["name"], i["item_count"]) for i in account_lists]
                listitems.insert(0, LANG(32139))
                listitems.append(LANG(32138))
                xbmc.executebuiltin("Dialog.Close(busydialog)")
                index = xbmcgui.Dialog().select(heading=LANG(32136), list=listitems)
                if index == 0:
                    listname = xbmcgui.Dialog().input(heading=LANG(32137), type=xbmcgui.INPUT_ALPHANUM)
                    if not listname:
                        return None
                    list_id = create_list(listname)
                    xbmc.sleep(1000)
                    change_list_status(list_id=list_id, movie_id=item_id, status=True)
                elif index == len(listitems) - 1:
                    self.remove_list_dialog(account_lists)
                elif index > 0:
                    change_list_status(account_lists[index - 1]["id"], item_id, True)
                    self.update_states()

    @ch.click(1250)
    @ch.click(1350)
    def open_image(self):
        listitems = next((v for (i, v) in self.listitems if i == self.control_id), None)
        index = self.control.getSelectedPosition()
        pos = wm.open_slideshow(listitems=listitems, index=index)
        self.control.selectItem(pos)

    @ch.action("contextmenu", 1250)
    def thumbnail_options(self):
        if not self.info.get("dbid"):
            return None
        selection = xbmcgui.Dialog().select(heading=LANG(22080),
                                            list=[LANG(32006)])
        if selection == 0:
            path = self.listitem.getProperty("original")
            media_type = self.window.getProperty("type")
            params = '"art": {"poster": "%s"}' % path
            get_kodi_json(method="VideoLibrary.Set%sDetails" % media_type,
                          params='{ %s, "%sid":%s }' % (params, media_type.lower(), self.info['dbid']))

    @ch.action("contextmenu", 1350)
    def fanart_options(self):
        if not self.info.get("dbid"):
            return None
        selection = xbmcgui.Dialog().select(heading=LANG(22080),
                                            list=[LANG(32007)])
        if selection == 0:
            path = self.listitem.getProperty("original")
            media_type = self.window.getProperty("type")
            params = '"art": {"fanart": "%s"}' % path
            get_kodi_json(method="VideoLibrary.Set%sDetails" % media_type,
                          params='{ %s, "%sid":%s }' % (params, media_type.lower(), self.info['dbid']))

    @ch.action("contextmenu", 1150)
    @ch.action("contextmenu", 350)
    def download_video(self):
        selection = xbmcgui.Dialog().select(heading=LANG(22080),
                                            list=[LANG(33003)])
        if selection == 0:
            youtube_id = self.listitem.getProperty("youtube_id")
            import YDStreamExtractor
            vid = YDStreamExtractor.getVideoInfo(youtube_id,
                                                 quality=1)
            YDStreamExtractor.handleDownload(vid)

    @ch.action("parentdir", "*")
    @ch.action("parentfolder", "*")
    def previous_menu(self):
        onback = self.window.getProperty("%i_onback" % self.control_id)
        if onback:
            xbmc.executebuiltin(onback)
        else:
            self.close()
            wm.pop_stack()

    @ch.action("previousmenu", "*")
    def exit_script(self):
        self.close()

    @run_async
    def get_youtube_vids(self, search_str):
        try:
            youtube_list = self.getControl(350)
        except:
            return None
        result = search_youtube(search_str, limit=15)
        if not self.yt_listitems:
            self.yt_listitems = result.get("listitems", [])
            if "videos" in self.data:
                vid_ids = [item["key"] for item in self.data["videos"]]
                self.yt_listitems = [i for i in self.yt_listitems if i["youtube_id"] not in vid_ids]
        youtube_list.reset()
        youtube_list.addItems(create_listitems(self.yt_listitems))

    def open_credit_dialog(self, credit_id):
        info = get_credit_info(credit_id)
        listitems = []
        if "seasons" in info["media"]:
            listitems += handle_tmdb_seasons(info["media"]["seasons"])
        if "episodes" in info["media"]:
            listitems += handle_tmdb_episodes(info["media"]["episodes"])
        if not listitems:
            listitems += [{"label": LANG(19055)}]
        listitem, index = wm.open_selectdialog(listitems=listitems)
        if listitem["media_type"] == "episode":
            wm.open_episode_info(prev_window=self,
                                 season=listitems[index]["season"],
                                 episode=listitems[index]["episode"],
                                 tvshow_id=info["media"]["id"])
        elif listitem["media_type"] == "season":
            wm.open_season_info(prev_window=self,
                                season=listitems[index]["season"],
                                tvshow_id=info["media"]["id"])

    def update_states(self):
        if not self.account_states:
            return None
        pass_dict_to_skin(data=get_account_props(self.account_states),
                          prefix="movie.",
                          window_id=self.window_id)
