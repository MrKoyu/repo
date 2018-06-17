# -*- coding: utf-8 -*-
"""
urlresolver XBMC Addon
Copyright (C) 2011 t0mm0

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
from __generic_resolver__ import GenericResolver


class RapidVideoResolver(GenericResolver):
    name = "rapidvideo.com"
    domains = ["rapidvideo.com", "raptu.com", "bitporno.com"]
    pattern = '(?://|\.)((?:rapidvideo|raptu|bitporno)\.com)/(?:[ev]/|embed/|\?v=)?([0-9A-Za-z]+)'

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://{host}/embed/{media_id}')
