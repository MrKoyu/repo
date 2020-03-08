# -*- coding: utf-8 -*-
"""
    Its saturday plugin
    Copyright (C) 2018,
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


    Returns the its saturday cartoon list

    <dir>
    <title>Its Sauturday Cartoons</title>
    <itsat>toons/1</itsat>
    </dir>
   
    --------------------------------------------------------------

"""



import requests,re,os,xbmc,xbmcaddon
import base64,pickle,koding,time,sqlite3
from koding import route
from ..plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list, display_data, clean_url
from resources.lib.external.airtable.airtable import Airtable
from unidecode import unidecode

CACHE_TIME = 86400  # change to wanted cache time in seconds

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
AddonName = xbmc.getInfoLabel('Container.PluginName')
home_folder = xbmc.translatePath('special://home/')
user_data_folder = os.path.join(home_folder, 'userdata')
addon_data_folder = os.path.join(user_data_folder, 'addon_data')
database_path = os.path.join(addon_data_folder, addon_id)
database_loc = os.path.join(database_path, 'database.db')
start = 'https://www.itsaturday.com'


class ITS_Saturday(Plugin):
    name = "its_saturday"

    def process_item(self, item_xml):
        if "<itsat>" in item_xml:
            item = JenItem(item_xml)
            if "toons" in item.get("itsat", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_its_sat_cartoons",
                    'url': item.get("itsat", ""),
                    'folder': True,
                    'imdb': "0",
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
            elif "next" in item.get("itsat", ""):
                item = JenItem(item_xml)
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_its_sat_cartoons_main",
                    'url': item.get("itsat", ""),
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

@route(mode='open_its_sat_cartoons', args=["url"])
def open_movies(url):
    pins = "" 
    xml = "" 
    pg = int(url.split("/")[-1]) 
    sturl = "https://www.itsaturday.com"
    html = requests.get(sturl).content
    block = re.compile('<!-- Composite End -->(.+?)</p>',re.DOTALL).findall(html)
    match = re.compile('href="(.+?)".+?data-src="(.+?)".+?title="(.+?)"',re.DOTALL).findall(str(block))
    sorted_name = sorted(match, key=lambda match:match[0])
    if pg == 1:
        pins = "PLuginitssaturdaypage1"
        xml += "<dir>"\
               "<title>Page 1   A-C</title>"\
               "<thumbnail></thumbnail>"\
               "<itsat>toons/2</itsat>"\
               "</dir>" 
        xml += "<dir>"\
               "<title>Page 2   C-G</title>"\
               "<thumbnail></thumbnail>"\
               "<itsat>toons/3</itsat>"\
               "</dir>"
        xml += "<dir>"\
               "<title>Page 3   G-M</title>"\
               "<thumbnail></thumbnail>"\
               "<itsat>toons/4</itsat>"\
               "</dir>"
        xml += "<dir>"\
               "<title>Page 4   M-P</title>"\
               "<thumbnail></thumbnail>"\
               "<itsat>toons/5</itsat>"\
               "</dir>"
        xml += "<dir>"\
               "<title>Page 5   P-T</title>"\
               "<thumbnail></thumbnail>"\
               "<itsat>toons/6</itsat>"\
               "</dir>"
        xml += "<dir>"\
               "<title>Page 6   T</title>"\
               "<thumbnail></thumbnail>"\
               "<itsat>toons/7</itsat>"\
               "</dir>"
        xml += "<dir>"\
               "<title>Page 7   T-W</title>"\
               "<thumbnail></thumbnail>"\
               "<itsat>toons/8</itsat>"\
               "</dir>"
        xml += "<dir>"\
               "<title>Page 8   W-Z</title>"\
               "<thumbnail></thumbnail>"\
               "<itsat>toons/9</itsat>"\
               "</dir>"                                                                                                         
    elif pg == 2:
        pins = "PLuginitssaturdaypage2"
        Items = fetch_from_db2(pins)
        if Items: 
            display_data(Items) 
        else:        
            pg1 = sorted_name[0:200]
            xml += open_page(pg1)
    elif pg == 3:
        pins = "PLuginitssaturdaypage3"
        Items = fetch_from_db2(pins)
        if Items: 
            display_data(Items) 
        else:        
            pg1 = sorted_name[200:400]
            xml += open_page(pg1)
    elif pg == 4:
        pins = "PLuginitssaturdaypage4"
        Items = fetch_from_db2(pins)
        if Items: 
            display_data(Items) 
        else:        
            pg1 = sorted_name[400:600]
            xml += open_page(pg1)
    elif pg == 5:
        pins = "PLuginitssaturdaypage5"
        Items = fetch_from_db2(pins)
        if Items: 
            display_data(Items) 
        else:        
            pg1 = sorted_name[600:800]
            xml += open_page(pg1)
    elif pg == 6:
        pins = "PLuginitssaturdaypage6"
        Items = fetch_from_db2(pins)
        if Items: 
            display_data(Items) 
        else:        
            pg1 = sorted_name[800:1000]
            xml += open_page(pg1)
    elif pg == 7:
        pins = "PLuginitssaturdaypage7"
        Items = fetch_from_db2(pins)
        if Items: 
            display_data(Items) 
        else:        
            pg1 = sorted_name[1000:1200]
            xml += open_page(pg1)
    elif pg == 8:
        pins = "PLuginitssaturdaypage8"
        Items = fetch_from_db2(pins)
        if Items: 
            display_data(Items) 
        else:        
            pg1 = sorted_name[1200:1400]
            xml += open_page(pg1)
    elif pg == 9:
        pins = "PLuginitssaturdaypage9"
        Items = fetch_from_db2(pins)
        if Items: 
            display_data(Items) 
        else:        
            pg1 = sorted_name[1400:]
            xml += open_page(pg1)                                                

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)

@route(mode='open_its_sat_cartoons_main', args=["url"])
def open_movies(url):
    pins = "PLuginitssaturday"+url
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else:    
        xml = ""
        url = url.split("/")[-1]
        sturl = "%s%s%s" % (start,"/",url)
        html = requests.get(sturl).content
        match = re.compile('<i class="fa fa-expand">.+?class="h3 bold">(.+?)<.+?poster=\"(.+?)\".+?src=\"(.+?)\"',re.DOTALL).findall(html)
        block = re.compile('<div class="sidebar col-3 rounded-bottom">(.+?)href=https://www.fastemoji.com/',re.DOTALL).findall(html)
        match2 = re.compile('href="(.+?)"',re.DOTALL).findall(str(block))
        print match
        for name, poster, link in match:
            name = name.replace("&nbsp; ","")
            poster = poster.replace(".jpg.jpg",".jpg")
            fin_link = "%s%s" % (start,link)
            xml += "<item>"\
                   "<title>%s</title>"\
                   "<thumbnail>%s</thumbnail>"\
                   "<link>%s</link>"\
                   "</item>" % (name,poster,fin_link)        
            for link2 in match2:
                url2 = "%s%s" % (start,link2)
                html2 = requests.get(url2).content
                match3 = re.compile('<i class="fa fa-expand">.+?class="h3 bold">(.+?)<.+?poster=\"(.+?)\".+?src=\"(.+?)\"',re.DOTALL).findall(html2)
                for name, poster, link in match3:
                    name = name.replace("&nbsp; ","").replace("&#8211;","-")
                    poster = poster.replace(".jpg.jpg",".jpg")
                    fin_link = "%s%s" % (start,link)
                    xml += "<item>"\
                           "<title>%s</title>"\
                           "<thumbnail>%s</thumbnail>"\
                           "<link>%s</link>"\
                           "</item>" % (name,poster,fin_link)   
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)

def open_page(pg1):
    xml = ""
    for link, image, name in pg1:
        name = name.replace("\\xe2\\x80\\x93","-").replace("&#039;","`").replace("&amp;","&").replace("\\xc3\\x86","Ae")
        fin_link = "%s%s" % (start,link)
        fin_img = "%s%s" % (start,image)
        xml += "<dir>"\
               "<title>%s</title>"\
               "<thumbnail>%s</thumbnail>"\
               "<itsat>next%s</itsat>"\
               "</dir>" % (name,fin_img,link)
    return xml               

def fetch_from_db2(url):
    koding.reset_db()
    url2 = clean_url(url)
    match = koding.Get_All_From_Table(url2)
    if match:
        match = match[0]
        if not match["value"]:
            return None   
        match_item = match["value"]
        try:
                result = pickle.loads(base64.b64decode(match_item))
        except:
                return None
        created_time = match["created"]
        print created_time + "created"
        print time.time() 
        print CACHE_TIME
        test_time = float(created_time) + CACHE_TIME 
        print test_time
        if float(created_time) + CACHE_TIME <= time.time():
            koding.Remove_Table(url2)
            db = sqlite3.connect('%s' % (database_loc))        
            cursor = db.cursor()
            db.execute("vacuum")
            db.commit()
            db.close()
            display_list2(result, "video", url2)
        else:
            pass                     
        return result
    else:
        return []

def remove_non_ascii(text):
    return unidecode(text)

