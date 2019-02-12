# -*- coding: UTF-8 -*-
'''
    Updated and refactored by someone.
    Originally created by others.
'''
# Addon Name: MTB
# Addon id: plugin.video.movietheaterbutter
# Addon Provider: SomeBody

import requests
import os
import re
import time

import xbmcaddon


class webform(object):
    def __init__(self, key=''):
        self.bugs_url = 'http://www.tantrumtv.com/kodi-addon-bug-reports/'
        self.features_url = 'http://www.tantrumtv.com/kodi-addon-feature-requests/'
        self.user_agent = 'MuadDib/1.0 (Whatever; U; Want; en-GB; rv:1.0.0.0) MoonRat/2008092417 Arrakis/1.0.0'

    def bug_report(self):
        # Payload is the variables for the form, dipshit
        payload = {'huge_it_11_42': 'addon_name', 'huge_it_11_43': 'bug_description'}
        # Not yet implemented

    def feature_request(self):
        # Payload is the variables for the form, dipshit
        payload = {'huge_it_11_42': 'addon_name', 'huge_it_11_43': 'bug_description'}
        # Not yet implemented, and payload form is not yet made
