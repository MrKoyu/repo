# -*- coding: utf-8 -*-
"""

    Watch your tv
    Copyright (C) 2020, TonyH
    Version 1.0.0


    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    -------------------------------------------------------------

    Usage Examples:

<dir>
<title>Watch your tv</title>
<wytv>get</wytv>
</dir>

"""    

import requests,re,os,xbmc,xbmcaddon
import base64,pickle,koding,time,sqlite3
from koding import route
from ..plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list, display_data, clean_url
from resources.lib.external.airtable.airtable import Airtable
from unidecode import unidecode


CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
AddonName = xbmc.getInfoLabel('Container.PluginName')
home_folder = xbmc.translatePath('special://home/')
user_data_folder = os.path.join(home_folder, 'userdata')
addon_data_folder = os.path.join(user_data_folder, 'addon_data')
database_path = os.path.join(addon_data_folder, addon_id)
database_loc = os.path.join(database_path, 'database.db')
UA = "|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"

class Watch_yourtv(Plugin):
    name = "watch_yourtv"

    def process_item(self, item_xml):
        if "<wytv>" in item_xml:
            item = JenItem(item_xml)
            if "get" in item.get("wytv", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_watchyourtv_cats",
                    'url': item.get("wytv", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "Page" in item.get("wytv", ""):
                item = JenItem(item_xml)
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_watchyourtv_page",
                    'url': item.get("wytv", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item 

@route(mode='open_watchyourtv_cats', args=["url"])
def get_cats(url):
    pins = ""
    xml = ""
    base = "https://www.watchyour.tv"
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    headers = {'User-Agent': User_Agent}
    url = "https://www.watchyour.tv/index.php"
    html = requests.get(url, headers=headers).content
    block = re.compile('</style>(.+?)<br><br><br>',re.DOTALL).findall(html)
    data = re.compile('<a href="(.+?)".+?title="(.+?)".+?src="(.+?)"',re.DOTALL).findall(str(block))
    for page, name, logo in data:
        name = name.replace(" - Watch Live with DVR","").replace("\\","")
        logo = base+logo
        page = page.replace("watch", "dvr")
        page = "http://www.watchyour.tv/"+page
        xml +=  "<item>"\
                "<title>%s</title>"\
                "<thumbnail>%s</thumbnail>"\
                "<fanart></fanart>"\
                "<link>"\
                "<wytv>Page**%s**%s</wytv>"\
                "</link>"\
                "</item>" % (name,logo,name,page)         
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins) 
 
@route(mode='open_watchyourtv_page', args=["url"])
def get_page(url):
    pins = ""
    xml = ""
    base = "https://www.watchyour.tv"
    end = "-3600.m3u8"
    name = url.split("**")[1]
    url2 = url.split("**")[-1]
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    headers = {'User-Agent': User_Agent}
    html = requests.get(url2, headers=headers).content
    try:
        data = re.compile("\(document\).+?playfp2\('(.+?)','(.+?)'",re.DOTALL).findall(html)
        thumb = base+data[0][0]
        link = data[0][1].split("?")[0]
        link = link+UA
        xml +=  "<item>"\
                "<title>%s</title>"\
                "<thumbnail>%s</thumbnail>"\
                "<fanart></fanart>"\
                "<link>"\
                "<sublink>%s</sublink>"\
                "</link>"\
                "</item>" % (name,thumb,link) 
    except:
        pass       
    try:        
        data = re.compile('<div class="oc-item".+?id="(.+?)".+?<img src="(.+?)"',re.DOTALL).findall(html)
        for vid, thumb in data:
            thumb = base+thumb
            vid = vid.replace("oc-item","")
            blink = get_base(name)
            flink = blink+vid+end+UA
            xml +=  "<item>"\
                    "<title>%s</title>"\
                    "<thumbnail>%s</thumbnail>"\
                    "<fanart></fanart>"\
                    "<link>"\
                    "<sublink>%s</sublink>"\
                    "</link>"\
                    "</item>" % (name,thumb,flink)
    except:
        pass        
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins) 


def get_base(name):
    if "TVS Television Network" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-tvstn/index-"
    elif "TVS Classic Sports" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-tvs/index-"
    elif "TVS Boxing Network" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-tvs/index-"
    elif "TVS Turbo Network" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-tvsturbo/index-"
    elif "TVS Tavern TV" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-tavern/index-"
    elif "TVS Sports Network" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-tvssports/index-"
    elif "TVS Women's Sports Network" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-tvswsn/index-"
    elif "TVS Classic Movies" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-tvsclassicmovies/index-"
    elif "TVS Drive In Movie" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-tvsdriveinmovie/index-"
    elif "TVS Hollywood History" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-tvshollywoohistory/index-"
    elif "TVS Nostalgia Movies" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-tvsNostalgiaMovies/index-"
    elif "TVS Western Movie" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-tvswesternmovies/index-"
    elif "TVS Main Street" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-tvsmainst/index-"
    elif "TVS Frontier" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-tvsfrontier/index-"
    elif "TVS Nostalgia" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-nostalgia/index-"
    elif "TVS Flashback Network" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-TVSFlashback/index-"
    elif "TVS Hi Tops" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-hitops/index-"
    elif "TVS Travel Network" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-tvstravel/index-"
    elif "TVS Family Channel" in name:
        blink = "https://nrpus.bozztv.com/36bay2/gusa-TVSFamilyChannel/index-"
    return blink


def remove_non_ascii(text):
    return unidecode(text)
           
            