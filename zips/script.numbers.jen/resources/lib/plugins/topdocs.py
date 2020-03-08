"""

    Copyright (C) 2018 MuadDib

    ----------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    @tantrumdev wrote this file.  As long as you retain this notice you can do 
    whatever you want with this stuff. Just Ask first when not released through
    the tools and parser GIT. If we meet some day, and you think this stuff is
    worth it, you can buy him a beer in return. - Muad'Dib
    ----------------------------------------------------------------------------


    Overview:

        Drop this PY in the plugins folder. See examples below on use.

    Version:
        2019.7.23:
            - Updated Clear Cache function to make use of "quiet_cache"
            
        2018.7.2:
            - Added Clear Cache function
            - Minor update on fetch cache returns

        2018.6.20:
            - Added caching to primary menus (Cache time is 3 hours)

        2018.5.17
            - Initial Release


    XML Explanations:
        Tags: 
            <topdocs></topdocs> - Displays the entry as category's contents


    Usage Examples:

        <dir>
            <title>9-11</title>
            <topdocs>tdcategory/911</topdocs>
        </dir>

        <dir>
            <title>Art and Artists</title>
            <topdocs>tdcategory/art-artists</topdocs>
        </dir>

        <dir>
            <title>Biography</title>
            <topdocs>tdcategory/biography</topdocs>
        </dir>

        <dir>
            <title>Comedy</title>
            <topdocs>tdcategory/comedy</topdocs>
        </dir>

        <dir>
            <title>Conspiracy</title>
            <topdocs>tdcategory/crime-conspiracy</topdocs>
        </dir>

        <dir>
            <title>Crime</title>
            <topdocs>tdcategory/crime</topdocs>
        </dir>

        <dir>
            <title>Drugs</title>
            <topdocs>tdcategory/drugs</topdocs>
        </dir>

        <dir>
            <title>Economics</title>
            <topdocs>tdcategory/economics</topdocs>
        </dir>

        <dir>
            <title>Environment</title>
            <topdocs>tdcategory/environment</topdocs>
        </dir>

        <dir>
            <title>Health</title>
            <topdocs>tdcategory/health</topdocs>
        </dir>

        <dir>
            <title>History</title>
            <topdocs>tdcategory/history</topdocs>
        </dir>

        <dir>
            <title>Media</title>
            <topdocs>tdcategory/media</topdocs>
        </dir>

        <dir>
            <title>Military and War</title>
            <topdocs>tdcategory/military-war</topdocs>
        </dir>

        <dir>
            <title>Mystery</title>
            <topdocs>tdcategory/mystery</topdocs>
        </dir>

        <dir>
            <title>Nature and Wildlife</title>
            <topdocs>tdcategory/nature-wildlife</topdocs>
        </dir>

        <dir>
            <title>Performing Arts</title>
            <topdocs>tdcategory/music-performing-arts</topdocs>
        </dir>

        <dir>
            <title>Philosophy</title>
            <topdocs>tdcategory/philosophy</topdocs>
        </dir>

        <dir>
            <title>Politics</title>
            <topdocs>tdcategory/politics</topdocs>
        </dir>

        <dir>
            <title>Psychology</title>
            <topdocs>tdcategory/psychology</topdocs>
        </dir>

        <dir>
            <title>Religion</title>
            <topdocs>tdcategory/religion</topdocs>
        </dir>

        <dir>
            <title>Science</title>
            <topdocs>tdcategory/science-technology</topdocs>
        </dir>

        <dir>
            <title>Sexuality</title>
            <topdocs>tdcategory/sex</topdocs>
        </dir>

        <dir>
            <title>Society</title>
            <topdocs>tdcategory/society</topdocs>
        </dir>

        <dir>
            <title>Sports</title>
            <topdocs>tdcategory/sports</topdocs>
        </dir>

        <dir>
            <title>Technology</title>
            <topdocs>tdcategory/technology</topdocs>
        </dir>

"""

import __builtin__
import base64,time
import json,re,requests,os,traceback,urlparse
import koding
import xbmc,xbmcaddon,xbmcgui
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util import dom_parser
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

CACHE_TIME = 10800  # change to wanted cache time in seconds

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon   = xbmcaddon.Addon().getAddonInfo('icon')

docu_link = 'https://topdocumentaryfilms.com/'
docu_cat_list = 'https://topdocumentaryfilms.com/category/'

class TopDocs(Plugin):
    name = "topdocs"
    priority = 200

    def process_item(self, item_xml):
        if "<topdocs>" in item_xml:
            item = JenItem(item_xml)
            if "tdcategory/" in item.get("topdocs", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "TDCats",
                    'url': item.get("topdocs", ""),
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
            result_item['fanart_small'] = result_item["fanart"]
            return result_item

    def clear_cache(self):
        skip_prompt = xbmcaddon.Addon().getSetting("quiet_cache")
        dialog = xbmcgui.Dialog()
        if skip_prompt == 'false':
            if dialog.yesno(xbmcaddon.Addon().getAddonInfo('name'), "Clear Top Documentaries Plugin Cache?"):
                koding.Remove_Table("topdocs_com_plugin")
        else:
            koding.Remove_Table("topdocs_com_plugin")
            

@route(mode='TDCats', args=["url"])
def get_tdcats(url):
    pins = ""
    url = url.replace('tdcategory/', '') # Strip our category tag off.
    orig_cat = url.split("/")[0]
    url = urlparse.urljoin(docu_cat_list, url)

    xml = fetch_from_db(url)
    if not xml:
        xml = ""
        try:
            html = requests.get(url).content
            doc_list = dom_parser.parseDOM(html, 'article', attrs={'class':'module'})
            for content in doc_list:
                try:
                    docu_info = re.compile('<h2>(.+?)</h2>',re.DOTALL).findall(content)[0]

                    docu_title = re.compile('<a.+?">(.+?)</a>',re.DOTALL).findall(docu_info)[0]
                    docu_title = docu_title.replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'").replace('&#8211;',' - ').replace('&#8217;',"'").replace('&#8216;',"'").replace('&#038;','&').replace('&acirc;','')
                    docu_summary = re.compile('<p>(.+?)</p>',re.DOTALL).findall(content)[0].replace('&quot;','"').replace('&#39;',"'").replace('&#8211;',' - ').replace('&#8217;',"'").replace('&#8216;',"'").replace('&#038;','&').replace('&acirc;','')
                    try:
                        docu_icon = re.compile('data-src="(.+?)"',re.DOTALL).findall(content)[0]
                    except:
                        docu_icon = re.compile('src="(.+?)"',re.DOTALL).findall(content)[0]


                    docu_url = re.compile('href="(.+?)"',re.DOTALL).findall(docu_info)[0]
                    docu_html = requests.get(docu_url).content

                    try:
                        docu_item = dom_parser.parseDOM(docu_html, 'meta', attrs={'itemprop':'embedUrl'}, ret='content')[0]
                    except:
                        docu_item = dom_parser.parseDOM(docu_html, 'iframe', ret='src')[0]

                    if 'http:' not in docu_item and  'https:' not in docu_item:
                        docu_item = 'https:' + docu_item
                    docu_url = docu_item

                    docu_title = replaceHTMLCodes(docu_title)

                    if 'youtube' in docu_url:
                        if 'videoseries' not in docu_url:
                            xml += "<item>"\
                                   "    <title>%s</title>"\
                                   "    <link>%s</link>"\
                                   "    <thumbnail>%s</thumbnail>"\
                                   "    <summary>%s</summary>"\
                                   "</item>" % (docu_title,docu_url,docu_icon,docu_summary)
                        else:
                            # videoseries stuff?
                            video_id = docu_url.split("=")[-1]
                            docu_url = 'plugin://plugin.video.youtube/playlist/%s/' % video_id
                            xml += "<item>"\
                                   "    <title>%s</title>"\
                                   "    <link>%s</link>"\
                                   "    <thumbnail>%s</thumbnail>"\
                                   "    <summary>%s</summary>"\
                                   "</item>" % (docu_title,docu_url,docu_icon,docu_summary)
                    elif 'vimeo' in docu_url or 'dailymotion' in docu_url:
                        xml += "<item>"\
                               "    <title>%s</title>"\
                               "    <link>%s</link>"\
                               "    <thumbnail>%s</thumbnail>"\
                               "    <summary>%s</summary>"\
                               "</item>" % (docu_title,docu_url,docu_icon,docu_summary)
                    elif 'archive.org/embed' in docu_url:
                        docu_html = requests.get(docu_url).content
                        video_element = dom_parser.parseDOM(docu_html, 'source', ret='src')[0]
                        docu_url = urlparse.urljoin('https://archive.org/', video_element)
                        xml += "<item>"\
                               "    <title>%s</title>"\
                               "    <link>%s</link>"\
                               "    <thumbnail>%s</thumbnail>"\
                               "    <summary>%s</summary>"\
                               "</item>" % (docu_title,docu_url,docu_icon,docu_summary)
                    elif 'myspace' in docu_url or 'nfb.ca' in docu_url:
                        # most of these gone now so screw it lol, and no valid player know yet to work with nfb
                        continue
                    else:
                        xbmcgui.Dialog().ok('Unknown Host - ' + docu_title,str(docu_url)) 

                except:
                    continue

            try:
                navi_content = dom_parser.parseDOM(html, 'div', attrs={'class':'pagination module'})[0]
                if '>Next' in navi_content:
                    links = dom_parser.parseDOM(navi_content, 'a', ret='href')
                    link = links[(len(links)-1)]
                    page = link.split("/")[-2]
                    xml += "<dir>"\
                           "    <title>Next Page >></title>"\
                           "    <topdocs>tdcategory/%s/page/%s</topdocs>"\
                           "</dir>" % (orig_cat,page)
            except:
                pass
            save_to_db(xml, url)
        except:
            pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


def save_to_db(item, url):
    if not item or not url:
        return False
    try:
        koding.reset_db()
        koding.Remove_From_Table(
            "topdocs_com_plugin",
            {
                "url": url
            })

        koding.Add_To_Table("topdocs_com_plugin",
                            {
                                "url": url,
                                "item": base64.b64encode(item),
                                "created": time.time()
                            })
    except:
        return False


def fetch_from_db(url):
    koding.reset_db()
    topdocs_plugin_spec = {
        "columns": {
            "url": "TEXT",
            "item": "TEXT",
            "created": "TEXT"
        },
        "constraints": {
            "unique": "url"
        }
    }
    koding.Create_Table("topdocs_com_plugin", topdocs_plugin_spec)
    match = koding.Get_From_Table(
        "topdocs_com_plugin", {"url": url})
    if match:
        match = match[0]
        if not match["item"]:
            return None
        created_time = match["created"]
        if created_time and float(created_time) + CACHE_TIME >= time.time():
            match_item = match["item"]
            try:
                result = base64.b64decode(match_item)
            except:
                return None
            return result
        else:
            return None
    else:
        return None


def replaceHTMLCodes(txt):
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    txt = txt.replace("&quot;", "\"").replace("&amp;", "&")
    txt = txt.replace('&#8216;','\'').replace('&#8217;','\'').replace('&#038;','&').replace('&#8230;','....')
    txt = txt.strip()
    return txt


def remove_non_ascii(text):
    try:
        text = text.decode('utf-8').replace(u'\xc2', u'A').replace(u'\xc3', u'A').replace(u'\xc4', u'A')
    except:
        pass
    return unidecode(text)
