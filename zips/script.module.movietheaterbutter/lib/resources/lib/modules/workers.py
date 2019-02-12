# -*- coding: UTF-8 -*-
'''
    Updated and refactored by someone.
    Originally created by others.
'''
# Addon Name: MTB
# Addon id: plugin.video.movietheaterbutter
# Addon Provider: SomeBody

import threading


class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)
