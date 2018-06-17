# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import time
from threading import Timer
import xbmcgui
from ..Utils import *
from collections import deque
import ast
from ..OnClickHandler import OnClickHandler
ch = OnClickHandler()

# (1st label, 2nd label)
KEYS = (("1", "1?.,;:'-+_=\""),
        ("2", "ABC2"),
        ("3", "DEF3"),
        ("4", "GHI4"),
        ("5", "JKL5"),
        ("6", "MNO6"),
        ("7", "PQRS7"),
        ("8", "TUV8"),
        ("9", "WXYZ9"),
        ("DEL", "<--"),
        ("0", " 0!@#$%&*()"),
        ("KEYB", "CLASSIC"))

class T9Search(xbmcgui.WindowXMLDialog):

    def __init__(self, *args, **kwargs):
        self.callback = kwargs.get("call")
        self.search_str = kwargs.get("start_value", "")
        self.previous = False
        self.prev_time = 0
        self.timer = None
        self.color_timer = None
        self.setting_name = kwargs.get("history")
        setting_string = SETTING(self.setting_name)
        if self.setting_name and setting_string:
            self.last_searches = deque(ast.literal_eval(setting_string), maxlen=10)
        else:
            self.last_searches = deque(maxlen=10)

    def onInit(self):
        self.get_autocomplete_labels_async()
        self.update_search_label_async()
        listitems = []
        for i, item in enumerate(KEYS):
            li = {"label": "[B]%s[/B]" % item[0],
                  "label2": item[1],
                  "key": item[0],
                  "value": item[1],
                  "index": str(i)
                  }
            listitems.append(li)
        self.getControl(9090).addItems(create_listitems(listitems))
        self.setFocusId(9090)
        self.getControl(600).setLabel("[B]%s[/B]_" % self.search_str)

    def onClick(self, control_id):
        ch.serve(control_id, self)

    def onAction(self, action):
        ch.serve_action(action, self.getFocusId(), self)

    @ch.click(9090)
    def panel_click(self):
        self.set_t9_letter(letters=self.listitem.getProperty("value"),
                           number=self.listitem.getProperty("key"),
                           button=int(self.listitem.getProperty("index")))

    @ch.click(9091)
    def set_autocomplete(self):
        self.search_str = self.listitem.getLabel()
        self.getControl(600).setLabel("[B]%s[/B]_" % self.search_str)
        self.get_autocomplete_labels_async()
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(0.0, self.search, (self.search_str,))
        self.timer.start()

    @ch.action("parentdir", "*")
    @ch.action("parentfolder", "*")
    @ch.action("previousmenu", "*")
    def close_dialog(self):
        self.save_autocomplete()
        self.close()

    @ch.action("number0", "*")
    def set_0(self):
        self.set_t9_letter(letters=self.control.getListItem(10).getProperty("value"),
                           number=self.control.getListItem(10).getProperty("key"),
                           button=int(self.control.getListItem(10).getProperty("index")))

    @ch.action("number1", "*")
    @ch.action("number2", "*")
    @ch.action("number3", "*")
    @ch.action("number4", "*")
    @ch.action("number5", "*")
    @ch.action("number6", "*")
    @ch.action("number7", "*")
    @ch.action("number8", "*")
    @ch.action("number9", "*")
    def t_9_button_click(self):
        item_id = self.action_id - xbmcgui.REMOTE_1
        self.set_t9_letter(letters=self.control.getListItem(item_id).getProperty("value"),
                           number=self.control.getListItem(item_id).getProperty("key"),
                           button=int(self.control.getListItem(item_id).getProperty("index")))
    @ch.action("delete", "*")
    def delete_last_character(self):
        self.search_str = self.search_str[:-1]

    @run_async
    def update_search_label_async(self):
        while True:
            time.sleep(1)
            if int(time.time()) % 2 == 0:
                self.getControl(600).setLabel("[B]%s[/B]_" % self.search_str)
            else:
                self.getControl(600).setLabel("[B]%s[/B][COLOR 00FFFFFF]_[/COLOR]" % self.search_str)

    @run_async
    def get_autocomplete_labels_async(self):
        self.getControl(9091).reset()
        if self.search_str:
            listitems = get_autocomplete_items(self.search_str)
        else:
            listitems = list(self.last_searches)
        self.getControl(9091).addItems(create_listitems(listitems))

    def save_autocomplete(self):
        if not self.search_str:
            return None
        listitem = {"label": self.search_str}
        if listitem in self.last_searches:
            self.last_searches.remove(listitem)
        self.last_searches.appendleft(listitem)
        ADDON.setSetting(self.setting_name, str(list(self.last_searches)))

    def set_t9_letter(self, letters, number, button):
        now = time.time()
        time_diff = now - self.prev_time
        if number == "DEL":
            self.search_str = self.search_str[:-1]
        elif number == " ":
            if self.search_str:
                self.search_str += " "
        elif number == "KEYB":
            self.use_classic_search()
        elif self.previous != letters or time_diff >= 1:
            self.prev_time = now
            self.previous = letters
            self.search_str += letters[0]
            self.color_labels(0, letters, button)
        elif time_diff < 1:
            if self.color_timer:
                self.color_timer.cancel()
            self.prev_time = now
            idx = (letters.index(self.search_str[-1]) + 1) % len(letters)
            self.search_str = self.search_str[:-1] + letters[idx]
            self.color_labels(idx, letters, button)
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(1.0, self.search, (self.search_str,))
        self.timer.start()
        self.getControl(600).setLabel("[B]%s[/B]_" % self.search_str)
        self.get_autocomplete_labels_async()

    def use_classic_search(self):
        self.close()
        result = xbmcgui.Dialog().input(heading=LANG(16017),
                                        type=xbmcgui.INPUT_ALPHANUM)
        if result and result > -1:
            self.search_str = result
            self.callback(result)
            self.save_autocomplete()

    def search(self, search_str):
        self.callback(search_str)

    def color_labels(self, index, letters, button):
        letter = letters[index]
        label = "[COLOR=FFFF3333]%s[/COLOR]" % letter
        self.getControl(9090).getListItem(button).setLabel2(letters.replace(letter, label))
        self.color_timer = Timer(1.0, self.reset_color, (self.getControl(9090).getListItem(button),))
        self.color_timer.start()

    def reset_color(self, item):
        label = item.getLabel2()
        label = label.replace("[COLOR=FFFF3333]", "").replace("[/COLOR]", "")
        item.setLabel2(label)
