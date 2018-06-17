import os

import xbmcaddon
import xbmcvfs
from ..plugin import Plugin


PATH = xbmcaddon.Addon().getAddonInfo("path")


class Local(Plugin):
    name = "local"

    def get_xml(self, url):
        if url.startswith("file://"):
            url = url.replace("file://", "")
            xml_file = xbmcvfs.File(os.path.join(PATH, "xml", url))
            xml = xml_file.read()
            xml_file.close()
            return xml

    def get_xml_uncached(self, url):
        return self.get_xml(url)
