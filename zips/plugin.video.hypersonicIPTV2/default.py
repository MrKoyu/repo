import xbmc ,xbmcaddon ,xbmcgui ,xbmcplugin ,base64 ,os ,re ,unicodedata ,requests ,time ,string ,sys ,urllib ,urllib2 ,json ,urlparse ,datetime ,zipfile ,shutil ,plugintools #line:2
from resources .modules import client ,control ,tools ,shortlinks #line:3
from resources .ivue import ivuesetup #line:4
from datetime import date #line:5
import xml .etree .ElementTree as ElementTree #line:6
import difflib #line:7
addon_id ='plugin.video.hypersonicIPTV2'#line:11
selfAddon =xbmcaddon .Addon (id =addon_id )#line:12
selfAddon =xbmcaddon .Addon (id =addon_id )#line:13
icon =xbmc .translatePath (os .path .join ('special://home/addons/'+addon_id ,'icon.png'))#line:14
fanart =xbmc .translatePath (os .path .join ('special://home/addons/'+addon_id ,'fanart.jpg'))#line:15
apk =xbmc .translatePath (os .path .join ('special://home/addons/plugin.video.hypersonicIPTV2/resources/icons/icon1.png'))#line:16
search2 =xbmc .translatePath (os .path .join ('special://home/addons/plugin.video.hypersonicIPTV2/resources/icons/icon3.png'))#line:17
system =xbmc .translatePath (os .path .join ('special://home/addons/plugin.video.hypersonicIPTV2/resources/icons/icon5.png'))#line:18
airing =xbmc .translatePath (os .path .join ('special://home/addons/plugin.video.hypersonicIPTV2/resources/icons/icon2.png'))#line:19
cache =xbmc .translatePath (os .path .join ('special://home/addons/plugin.video.hypersonicIPTV2/resources/icons/icon4.png'))#line:20
speed =xbmc .translatePath (os .path .join ('special://home/addons/plugin.video.hypersonicIPTV2/resources/icons/icon6.png'))#line:21
account =xbmc .translatePath (os .path .join ('special://home/addons/plugin.video.hypersonicIPTV2/resources/icons/account.png'))#line:22
username =control .setting ('Username')#line:24
password =control .setting ('Password')#line:25
adultset =control .setting ('Adult.Set')#line:26
adultpwset =control .setting ('Adult.PWSet')#line:27
adultpw =control .setting ('Adult.PW')#line:28
host ='http://live.hypersonic-tv.com'#line:30
port ='83'#line:31
live_url ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_categories'%(host ,port ,username ,password )#line:33
vod_url ='%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host ,port ,username ,password )#line:34
series_url ='%s:%s/enigma2.php?username=%s&password=%s&type=get_series_categories'%(host ,port ,username ,password )#line:35
panel_api ='%s:%s/panel_api.php?username=%s&password=%s'%(host ,port ,username ,password )#line:36
play_url ='%s:%s/live/%s/%s/'%(host ,port ,username ,password )#line:37
All ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&'%(host ,port ,username ,password )#line:40
USA_Entertainment ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1'%(host ,port ,username ,password )#line:41
USA_Sports ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=689'%(host ,port ,username ,password )#line:42
USA_SPORTS_REGIONALS ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1159'%(host ,port ,username ,password )#line:43
UK_Entertainment ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=691'%(host ,port ,username ,password )#line:44
UK_Sports_2 ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=690'%(host ,port ,username ,password )#line:45
UK_Movies ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=693'%(host ,port ,username ,password )#line:46
UK_News ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1214'%(host ,port ,username ,password )#line:47
UK_Documentaries ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=692'%(host ,port ,username ,password )#line:48
UK_Kids ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=694'%(host ,port ,username ,password )#line:49
New_Canada ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1385'%(host ,port ,username ,password )#line:50
Canada ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=665'%(host ,port ,username ,password )#line:51
Canada_News ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1186'%(host ,port ,username ,password )#line:52
Canada_Movies ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1177'%(host ,port ,username ,password )#line:53
Canada_Reality ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1178'%(host ,port ,username ,password )#line:54
Canada_Kids ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1179'%(host ,port ,username ,password )#line:55
Canadian_Sports ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=713'%(host ,port ,username ,password )#line:56
EPL_SPFL_Eleven_Sports ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1383'%(host ,port ,username ,password )#line:57
CARIBBEAN ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1213'%(host ,port ,username ,password )#line:58
PPV___Live_Events ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=41'%(host ,port ,username ,password )#line:59
ESPN_PLUS ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1384'%(host ,port ,username ,password )#line:60
Music_Choice ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1392'%(host ,port ,username ,password )#line:61
TwentyFourSeven ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=18'%(host ,port ,username ,password )#line:62
NBC_GOLD___Premier_League ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1188'%(host ,port ,username ,password )#line:63
All_Sports ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=16'%(host ,port ,username ,password )#line:64
NFL_Package ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=10'%(host ,port ,username ,password )#line:65
NHL_Package ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=11'%(host ,port ,username ,password )#line:66
NBA_Package ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1484'%(host ,port ,username ,password )#line:67
MLB_Package ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1210'%(host ,port ,username ,password )#line:68
MLB_Backup_1 ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1210'%(host ,port ,username ,password )#line:69
MLS_Package ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1518'%(host ,port ,username ,password )#line:70
NCAAB ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=59'%(host ,port ,username ,password )#line:71
NCAAF ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1394'%(host ,port ,username ,password )#line:72
International_Sports ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=9'%(host ,port ,username ,password )#line:73
SOUTH_AMERICA ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1189'%(host ,port ,username ,password )#line:74
Australia ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1184'%(host ,port ,username ,password )#line:75
Africa ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=43'%(host ,port ,username ,password )#line:76
Albania ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=44'%(host ,port ,username ,password )#line:77
Arabic ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=56'%(host ,port ,username ,password )#line:78
Armenia ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=17'%(host ,port ,username ,password )#line:79
Belgium ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1320'%(host ,port ,username ,password )#line:80
Brazil ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=45'%(host ,port ,username ,password )#line:81
Bulgaria ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=53'%(host ,port ,username ,password )#line:82
Czech_Republic ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=26'%(host ,port ,username ,password )#line:83
USNEWS ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=65'%(host ,port ,username ,password )#line:84
EX_YU ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=28'%(host ,port ,username ,password )#line:85
EGYPT ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1367'%(host ,port ,username ,password )#line:86
France ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=47'%(host ,port ,username ,password )#line:87
German ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=52'%(host ,port ,username ,password )#line:88
Greek ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=29'%(host ,port ,username ,password )#line:89
Hungary ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=46'%(host ,port ,username ,password )#line:90
India ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=48'%(host ,port ,username ,password )#line:91
Indonesia ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1370'%(host ,port ,username ,password )#line:92
Irish ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1180'%(host ,port ,username ,password )#line:93
Israel ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1319'%(host ,port ,username ,password )#line:94
direct_test ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=662'%(host ,port ,username ,password )#line:95
Japan ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=34'%(host ,port ,username ,password )#line:96
Korea ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=35'%(host ,port ,username ,password )#line:97
Latino ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=24'%(host ,port ,username ,password )#line:98
Netherlands ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=36'%(host ,port ,username ,password )#line:99
Norway ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1382'%(host ,port ,username ,password )#line:100
Pakistan ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=54'%(host ,port ,username ,password )#line:101
Persian ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=22'%(host ,port ,username ,password )#line:102
Philippines ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1318'%(host ,port ,username ,password )#line:103
Polish ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=21'%(host ,port ,username ,password )#line:104
Portugal ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=55'%(host ,port ,username ,password )#line:105
Romania ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=50'%(host ,port ,username ,password )#line:106
Russia ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=49'%(host ,port ,username ,password )#line:107
Spain ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1174'%(host ,port ,username ,password )#line:108
Denmark ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=38'%(host ,port ,username ,password )#line:109
Sweden ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1330'%(host ,port ,username ,password )#line:110
Italy ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=33'%(host ,port ,username ,password )#line:111
Turkish ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=40'%(host ,port ,username ,password )#line:112
Adult ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=23'%(host ,port ,username ,password )#line:113
twentyfourseven_Kids ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1488'%(host ,port ,username ,password )#line:114
twentyfourseven_Movies ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=709'%(host ,port ,username ,password )#line:115
twentyfourseven_AG ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1477'%(host ,port ,username ,password )#line:116
twentyfourseven_HN ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1478'%(host ,port ,username ,password )#line:117
twentyfourseven_OU ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1479'%(host ,port ,username ,password )#line:118
twentyfourseven_VZ ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1480'%(host ,port ,username ,password )#line:119
twentyfourseven_ADULT ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1395'%(host ,port ,username ,password )#line:120
twentyfourseven_Latin ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1528'%(host ,port ,username ,password )#line:121
USA_Reality ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=706'%(host ,port ,username ,password )#line:122
ABC_LOCALS ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1529'%(host ,port ,username ,password )#line:123
CBS_LOCALS ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1530'%(host ,port ,username ,password )#line:124
FOX_LOCALS ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1531'%(host ,port ,username ,password )#line:125
NBC_LOCALS ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1532'%(host ,port ,username ,password )#line:126
USA_KIDS ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=702'%(host ,port ,username ,password )#line:127
USA__Movies ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=707'%(host ,port ,username ,password )#line:128
USA_Music ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1216'%(host ,port ,username ,password )#line:129
Nascar ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1401'%(host ,port ,username ,password )#line:130
USA_FOX_SPORTS_REGIONALS ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1520'%(host ,port ,username ,password )#line:131
SKY_SPORTS ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1525'%(host ,port ,username ,password )#line:132
BT_SPORTS ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1526'%(host ,port ,username ,password )#line:133
BBC_RED_BUTTON_SPORTS ='%s:%s/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=1527'%(host ,port ,username ,password )#line:134
Guide =xbmc .translatePath (os .path .join ('special://home/addons/plugin.video.hypersonicIPTV2/resources/catchup','guide.xml'))#line:136
GuideLoc =xbmc .translatePath (os .path .join ('special://home/addons/plugin.video.hypersonicIPTV2/resources/catchup','g'))#line:137
advanced_settings =xbmc .translatePath ('special://home/addons/'+addon_id +'/resources/advanced_settings')#line:139
advanced_settings_target =xbmc .translatePath (os .path .join ('special://home/userdata','advancedsettings.xml'))#line:140
USER_DATA =xbmc .translatePath (os .path .join ('special://home/userdata',''))#line:142
ADDON_DATA =xbmc .translatePath (os .path .join (USER_DATA ,'addon_data'))#line:143
tvprotvfol =xbmc .translatePath (os .path .join (ADDON_DATA ,'plugin.video.hypersonicIPTV2'))#line:144
tvprotvset =xbmc .translatePath (os .path .join (ADDON_DATA ,'settings.xml'))#line:145
ini =xbmc .translatePath (os .path .join ('special://home/addons/plugin.video.hypersonicIPTV2/resources/ivue','addons_index.ini'))#line:146
inizip =xbmc .translatePath (os .path .join ('special://home/addons/plugin.video.hypersonicIPTV2/resources/ivue','addons_index.zip'))#line:147
tmpini =xbmc .translatePath (os .path .join ('special://home/userdata',''))#line:148
ivuetarget =xbmc .translatePath (os .path .join ('special://home/userdata/addon_data/script.ivueguide/'))#line:149
ivueaddons2ini =xbmc .translatePath (os .path .join ('special://home/userdata/addon_data/script.ivueguide/addons2.ini'))#line:150
ivuecreate =xbmc .translatePath (os .path .join ('special://home/userdata/addon_data/plugin.video.IVUEcreator/'))#line:151
ivuecreateini =xbmc .translatePath (os .path .join ('special://home/userdata/addon_data/plugin.video.IVUEcreator/addons_index.ini'))#line:152
PVRSimple =xbmc .translatePath (os .path .join ('special://home/userdata/addon_data/pvr.iptvsimple/settings.xml'))#line:153
databasePath =xbmc .translatePath ('special://profile/addon_data/script.ivueguide')#line:154
subPath =xbmc .translatePath ('special://profile/addon_data/script.ivueguide/resources/ini')#line:155
pyPath =xbmc .translatePath ('special://profile/addon_data/script.ivueguide/resources/subs')#line:156
setupPath =xbmc .translatePath ('special://profile/addon_data/script.ivueguide/resources/guide_setups')#line:157
tvproaddons2ini =xbmc .translatePath ('special://profile/addon_data/script.ivueguide/addons2.ini')#line:158
dialog =xbmcgui .Dialog ()#line:159
def start ():#line:161
    if username =="":#line:162
        OOO00O0OO0OOO0OO0 =userpopup ()#line:163
        OOOO00O0OOOO000O0 =passpopup ()#line:164
        control .setSetting ('Username',OOO00O0OO0OOO0OO0 )#line:165
        control .setSetting ('Password',OOOO00O0OOOO000O0 )#line:166
        xbmc .executebuiltin ('Container.Refresh')#line:167
        O00OOO0O0000OOO0O ='%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host ,port ,OOO00O0OO0OOO0OO0 ,OOOO00O0OOOO000O0 )#line:168
        O00OOO0O0000OOO0O =tools .OPEN_URL (O00OOO0O0000OOO0O )#line:169
        if O00OOO0O0000OOO0O =="":#line:170
            OOO00000OOOOO00OO ="[COLOR red]Incorrect Login Details![/COLOR]"#line:171
            OO0000OO0OOOO0OO0 ="Please Re-enter"#line:172
            OOOOOOOOOO00OO000 ="To unlock your TV PRO go to:[COLORlime] https://gethypersonic.mytvpro.org[/COLOR]"#line:173
            xbmcgui .Dialog ().ok ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]',OOO00000OOOOO00OO ,OO0000OO0OOOO0OO0 ,OOOOOOOOOO00OO000 )#line:174
            start ()#line:175
        else :#line:176
            OOO00000OOOOO00OO ="[COLOR lime]Login Successfull![/COLOR]"#line:177
            OO0000OO0OOOO0OO0 ="Welcome to [COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]"#line:178
            OOOOOOOOOO00OO000 =('[COLOR blue]%s[/COLOR]'%OOO00O0OO0OOO0OO0 )#line:179
            xbmcgui .Dialog ().ok ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]',OOO00000OOOOO00OO ,OO0000OO0OOOO0OO0 ,OOOOOOOOOO00OO000 )#line:180
            addonsettings ('ADS2','')#line:181
            adult_settings ()#line:182
            xbmc .executebuiltin ('Container.Refresh')#line:183
            home ()#line:184
    else :#line:185
        O00OOO0O0000OOO0O ='%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host ,port ,username ,password )#line:186
        O00OOO0O0000OOO0O =tools .OPEN_URL (O00OOO0O0000OOO0O )#line:187
        if not O00OOO0O0000OOO0O =="":#line:188
            tools .addDir ('[B][COLOR yellow]Video On Demand App[/COLOR][/B]','','',apk ,fanart ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR]')#line:189
            tools .addDir ('[COLOR white]LIVE TV[/COLOR]','live',1 ,airing ,fanart ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR]')#line:190
            tools .addDir ('[COLOR white]SEARCH CHANNELS[/COLOR]','url',5 ,search2 ,fanart ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR]')#line:191
            tools .addDir ('[COLOR white]CLEAR CACHE[/COLOR]','CC',10 ,cache ,fanart ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR]')#line:192
            tools .addDir ('[COLOR white]TOOLS[/COLOR]','url',8 ,system ,fanart ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR]')#line:193
            tools .addDir ('[COLORwhite]MY ACCOUNT[/COLOR]','url',6 ,icon ,fanart ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR]')#line:194
            plugintools .set_view (plugintools .LIST )#line:195
            setView ()#line:196
def home ():#line:197
    tools .addDir ('[B][COLOR yellow]Video On Demand App[/COLOR][/B]','','',apk ,fanart ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR]')#line:198
    tools .addDir ('[COLOR white]LIVE TV[/COLOR]','live',1 ,airing ,fanart ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR]')#line:199
    tools .addDir ('[COLOR white]SEARCH CHANNELS[/COLOR]','url',5 ,search2 ,fanart ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR]')#line:200
    tools .addDir ('[COLOR white]CLEAR CACHE[/COLOR]','CC',10 ,cache ,fanart ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR]')#line:201
    tools .addDir ('[COLOR white]TOOLS[/COLOR]','url',8 ,system ,fanart ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR]')#line:202
    tools .addDir ('[COLORwhite]MY ACCOUNT[/COLOR]','url',6 ,icon ,fanart ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR]')#line:203
    plugintools .set_view (plugintools .LIST )#line:204
    setView ()#line:205
def guides ():#line:208
    if xbmc .getCondVisibility ('System.HasAddon(pvr.iptvsimple)'):#line:209
        tools .addDir ('[COLOR white]Simple PVR Client TV Guide[/COLOR]','pvr',7 ,guide ,fanart ,'')#line:210
    if xbmc .getCondVisibility ('System.HasAddon(pvr.iptvsimple)'):#line:211
        tools .addDir ('[COLOR white]Simple PVR Client Channels Guide[/COLOR]','pvr',45 ,icon ,fanart ,'')#line:212
    tools .addDir ('[COLOR white]Setup Simple PVR[/COLOR]','tv',11 ,guide ,fanart ,'')#line:213
    tools .addDir ('[COLOR white]iVue TV Guide[/COLOR]','pvr',44 ,guide ,fanart ,'')#line:214
    tools .addDir ('[COLOR white]Setup iVue TV Guide -Old-[/COLOR]','tv',15 ,guide ,fanart ,'')#line:215
    tools .addDir ('[COLOR white]Setup iVue TV Guide -New-[/COLOR]','tv',36 ,guide ,fanart ,'')#line:216
    tools .addDir ('[COLOR white]Reboot iVue TV Guide[/COLOR]','url',20 ,guide ,fanart ,'')#line:217
def settingsmenu ():#line:220
    tools .addDir ('[COLOR lime]* [/COLOR][COLOR white]Settings[/COLOR]','tv',39 ,icon ,account ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR]')#line:221
    tools .addDir ('[COLOR lime]* [/COLOR][COLOR white]Edit Advanced Settings[/COLOR]','ADS',10 ,icon ,account ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR]')#line:222
    tools .addDir ('[COLOR lime]* [/COLOR][COLOR white]Speed Test[/COLOR]','ST',10 ,speed ,account ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR]')#line:223
    plugintools .set_view (plugintools .MOVIES )#line:224
def SoftReset ():#line:227
    OO00OOOOOOOO0OO0O =["guides.ini","addons.ini","guide.xml","amylist.xml","teamexpat.xml","otttv.xml","guide2.xml","uk3.xml","guide3.xmltv","master.xml"]#line:228
    for OOOOOOO0O00OO0OO0 ,OO00000O0OOO0OOO0 ,O0OOOO00OO00OOO00 in os .walk (databasePath ,topdown =True ):#line:229
        OO00000O0OOO0OOO0 [:]=[O000OO0OOOO000000 for O000OO0OOOO000000 in OO00000O0OOO0OOO0 ]#line:230
        for OOOOOOOO000O0OO00 in O0OOOO00OO00OOO00 :#line:231
            if OOOOOOOO000O0OO00 in OO00OOOOOOOO0OO0O :#line:232
                try :#line:233
                    os .remove (os .path .join (OOOOOOO0O00OO0OO0 ,OOOOOOOO000O0OO00 ))#line:234
                except :#line:235
                    dialog .ok ('Soft Reset','Error Removing '+str (OOOOOOOO000O0OO00 ),'')#line:236
                    pass #line:237
            else :#line:238
                continue #line:239
    dialog .ok ('Ivue guide Soft reset','Please restart iVue TV Guide ','for changes to take effect.')#line:240
    home ()#line:241
def DESTROY_PATH (OOO0O00OO0OO00OOO ):#line:244
    shutil .rmtree (OOO0O00OO0OO00OOO ,ignore_errors =True )#line:245
def exit ():#line:247
    xbmc .executebuiltin ("XBMC.ActivateWindow(Home)")#line:248
    if os .path .exists (tvprotvfol ):#line:249
        DESTROY_PATH (tvprotvfol )#line:250
def livecategory (O000OO0OOO0OO0000 ):#line:253
    OO00O0O00OOO0OO0O =tools .OPEN_URL (live_url )#line:255
    OO0OOO000O0O00OO0 =tools .regex_get_all (OO00O0O00OOO0OO0O ,'<channel>','</channel>')#line:256
    for O0O000O0O000O0O0O in OO0OOO000O0O00OO0 :#line:257
        O00OOO0O0O00OO0OO =tools .regex_from_to (O0O000O0O000O0O0O ,'<title>','</title>')#line:258
        O00OOO0O0O00OO0OO =base64 .b64decode (O00OOO0O0O00OO0OO )#line:259
        OOO000O0OO0OO0O0O =tools .regex_from_to (O0O000O0O000O0O0O ,'<playlist_url>','</playlist_url>').replace ('<![CDATA[','').replace (']]>','')#line:260
        tools .addDir (O00OOO0O0O00OO0OO ,OOO000O0OO0OO0O0O ,2 ,icon ,fanart ,'')#line:261
        plugintools .set_view (plugintools .LIST )#line:262
def Livelist (OOOO000OO00OO00O0 ):#line:264
    OO00O000O000000OO =tools .OPEN_URL (OOOO000OO00OO00O0 )#line:265
    O0OO000OOOO0O0000 =tools .regex_get_all (OO00O000O000000OO ,'<channel>','</channel>')#line:266
    for OOOOO000000OOOO00 in O0OO000OOOO0O0000 :#line:267
        O0OOOOO000O0OOOOO =tools .regex_from_to (OOOOO000000OOOO00 ,'<title>','</title>')#line:268
        O0OOOOO000O0OOOOO =base64 .b64decode (O0OOOOO000O0OOOOO )#line:269
        xbmc .log (str (O0OOOOO000O0OOOOO ))#line:270
        try :#line:271
            O0OOOOO000O0OOOOO =re .sub ('\[.*?min ','-',O0OOOOO000O0OOOOO )#line:272
        except :#line:273
            pass #line:274
        O0O0OO00OOO000OOO =tools .regex_from_to (OOOOO000000OOOO00 ,'<desc_image>','</desc_image>').replace ('<![CDATA[','').replace (']]>','')#line:275
        OO0000OOO0OOO000O =tools .regex_from_to (OOOOO000000OOOO00 ,'<stream_url>','</stream_url>').replace ('<![CDATA[','').replace (']]>','')#line:276
        OOO0OOO0OO0OO0000 =tools .regex_from_to (OOOOO000000OOOO00 ,'<description>','</description>')#line:277
        tools .addDir (O0OOOOO000O0OOOOO ,OO0000OOO0OOO000O ,4 ,O0O0OO00OOO000OOO ,fanart ,base64 .b64decode (OOO0OOO0OO0OO0000 ))#line:278
    plugintools .set_view (plugintools .LIST )#line:279
def LiveInfolist (O00O00O000O000OOO ):#line:281
    O0OO00O0OOO000O0O =tools .OPEN_URL (O00O00O000O000OOO )#line:282
    O000OOO0O00000OO0 =tools .regex_get_all (O0OO00O0OOO000O0O ,'<channel>','</channel>')#line:283
    for O0OOOOO000O0O0000 in O000OOO0O00000OO0 :#line:284
        OO0O00OOOO0O0O000 =tools .regex_from_to (O0OOOOO000O0O0000 ,'<title>','</title>')#line:285
        OO0O00OOOO0O0O000 =base64 .b64decode (OO0O00OOOO0O0O000 )#line:286
        xbmc .log (str (OO0O00OOOO0O0O000 ))#line:287
        try :#line:288
            OO0O00OOOO0O0O000 =re .sub ('\[.*?min ','-',OO0O00OOOO0O0O000 )#line:289
        except :#line:290
            pass #line:291
        O0OOOO00O00OO0000 =tools .regex_from_to (O0OOOOO000O0O0000 ,'<desc_image>','</desc_image>').replace ('<![CDATA[','').replace (']]>','')#line:292
        O00OOOOOOOOO0O0O0 =tools .regex_from_to (O0OOOOO000O0O0000 ,'<stream_url>','</stream_url>').replace ('<![CDATA[','').replace (']]>','')#line:293
        O000OOO0OOOOOOOOO =tools .regex_from_to (O0OOOOO000O0O0000 ,'<description>','</description>')#line:294
        tools .addDir (OO0O00OOOO0O0O000 ,O00OOOOOOOOO0O0O0 ,4 ,O0OOOO00O00OO0000 ,fanart ,base64 .b64decode (O000OOO0OOOOOOOOO ))#line:295
    plugintools .set_view (plugintools .EPISODES )#line:296
def ivuetvguide ():#line:302
    if xbmc .getCondVisibility ('System.HasAddon(script.ivueguide)'):#line:303
        if not os .path .exists (tvproaddons2ini ):#line:304
            IVUEtvguidesetup ()#line:305
        else :#line:306
            EXIT ()#line:307
            xbmc .executebuiltin ('RunAddon(script.ivueguide)')#line:308
def simpletvguide ():#line:310
    if xbmc .getCondVisibility ('System.HasAddon(pvr.iptvsimple)'):#line:311
        if not os .path .exists (PVRSimple ):#line:312
            SIMPLEtvguidesetup ()#line:313
        else :#line:314
            EXIT ()#line:315
            xbmc .executebuiltin ('ActivateWindow(TVGuide)')#line:316
def simplechannels ():#line:318
    if xbmc .getCondVisibility ('System.HasAddon(pvr.iptvsimple)'):#line:319
        if not os .path .exists (PVRSimple ):#line:320
            SIMPLEtvguidesetup ()#line:321
        else :#line:322
            EXIT ()#line:323
            xbmc .executebuiltin ('ActivateWindow(TVChannels)')#line:324
def EXIT ():#line:326
    xbmc .executebuiltin ("XBMC.Container.Update(path,replace)")#line:327
    xbmc .executebuiltin ("XBMC.ActivateWindow(Home)")#line:328
def stream_video (OOOOOO0OO000O0O00 ):#line:330
    if adultpwset =="true":#line:331
        OOOOOOO00O00OO0OO ='XO','XXX','Adult','Adults','ADULT','ADULTS','adult','adults','Porn','PORN','porn','Porn','xxx','xx'#line:332
        if any (O0OOOO0OO00O0OOO0 in name for O0OOOO0OO00O0OOO0 in OOOOOOO00O00OO0OO ):#line:333
            OO00OOO0O0OOO0O0O =control .inputDialog (heading ='Enter Adult Password:')#line:334
            if OO00OOO0O0OOO0O0O ==control .setting ('Adult.PW'):#line:335
                OOOOOO0OO000O0O00 =str (OOOOOO0OO000O0O00 ).replace ('USERNAME',username ).replace ('PASSWORD',password )#line:336
                OO000O00O0OOO00OO =xbmcgui .ListItem ('',iconImage ='DefaultVideo.png',thumbnailImage =icon )#line:337
                OO000O00O0OOO00OO .setInfo (type ='Video',infoLabels ={'Title':'','Plot':''})#line:338
                OO000O00O0OOO00OO .setProperty ('IsPlayable','true')#line:339
                OO000O00O0OOO00OO .setPath (str (OOOOOO0OO000O0O00 ))#line:340
                xbmcplugin .setResolvedUrl (int (sys .argv [1 ]),True ,OO000O00O0OOO00OO )#line:341
            else :#line:342
                xbmc .executebuiltin ((u'XBMC.Notification("Parental Lock", "Incorrect Password!", 2000)'))#line:343
                return #line:344
        else :#line:345
            OOOOOO0OO000O0O00 =str (OOOOOO0OO000O0O00 ).replace ('USERNAME',username ).replace ('PASSWORD',password )#line:346
            OO000O00O0OOO00OO =xbmcgui .ListItem ('',iconImage ='DefaultVideo.png',thumbnailImage =icon )#line:347
            OO000O00O0OOO00OO .setInfo (type ='Video',infoLabels ={'Title':'','Plot':''})#line:348
            OO000O00O0OOO00OO .setProperty ('IsPlayable','true')#line:349
            OO000O00O0OOO00OO .setPath (str (OOOOOO0OO000O0O00 ))#line:350
            xbmcplugin .setResolvedUrl (int (sys .argv [1 ]),True ,OO000O00O0OOO00OO )#line:351
    else :#line:353
        OOOOOO0OO000O0O00 =str (OOOOOO0OO000O0O00 ).replace ('USERNAME',username ).replace ('PASSWORD',password )#line:354
        OO000O00O0OOO00OO =xbmcgui .ListItem ('',iconImage ='DefaultVideo.png',thumbnailImage =icon )#line:355
        OO000O00O0OOO00OO .setInfo (type ='Video',infoLabels ={'Title':'','Plot':''})#line:356
        OO000O00O0OOO00OO .setProperty ('IsPlayable','true')#line:357
        OO000O00O0OOO00OO .setPath (str (OOOOOO0OO000O0O00 ))#line:358
        xbmcplugin .setResolvedUrl (int (sys .argv [1 ]),True ,OO000O00O0OOO00OO )#line:359
def searchdialog ():#line:362
    O00000O00OOO00O0O =control .inputDialog (heading ='Search [COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR] :')#line:363
    if O00000O00OOO00O0O =="":#line:364
        return #line:365
    else :#line:366
        return O00000O00OOO00O0O #line:367
def search ():#line:370
    if mode ==3 :#line:371
        return False #line:372
    O00O0O00OOO0OO0O0 =searchdialog ()#line:373
    if not O00O0O00OOO0OO0O0 :#line:374
        xbmc .executebuiltin ("XBMC.Notification([COLORlime][B][I]Search is Empty[/I][/B][/COLOR],Aborting search,4000,"+icon +")")#line:375
        return #line:376
    xbmc .log (str (O00O0O00OOO0OO0O0 ))#line:377
    O0OO000000OO000OO =tools .OPEN_URL (panel_api )#line:378
    O0O0O00OOO00OOO0O =tools .regex_get_all (O0OO000000OO000OO ,'{"num":','epg')#line:379
    for O00000O0000OOOO00 in O0O0O00OOO00OOO0O :#line:380
        OO0O00OOO00OO0O0O =tools .regex_from_to (O00000O0000OOOO00 ,'name":"','"').replace ('\/','/')#line:381
        O0O000OO0OO00OO00 =tools .regex_from_to (O00000O0000OOOO00 ,'"stream_id":"','"')#line:382
        O000O00OO00O0000O =tools .regex_from_to (O00000O0000OOOO00 ,'stream_icon":"','"').replace ('\/','/')#line:383
        if O00O0O00OOO0OO0O0 in OO0O00OOO00OO0O0O .lower ():#line:384
            tools .addDir (OO0O00OOO00OO0O0O ,play_url +O0O000OO0OO00OO00 +'.ts',4 ,O000O00OO00O0000O ,fanart ,'')#line:385
        elif O00O0O00OOO0OO0O0 not in OO0O00OOO00OO0O0O .lower ()and O00O0O00OOO0OO0O0 in OO0O00OOO00OO0O0O :#line:386
            tools .addDir (OO0O00OOO00OO0O0O ,play_url +O0O000OO0OO00OO00 +'.ts',4 ,O000O00OO00O0000O ,fanart ,'')#line:387
def addonsettings (O00OOOOOO0O00O0OO ,O0OO00O0000O0O000 ):#line:391
    if O00OOOOOO0O00O0OO =="CC":#line:392
        tools .clear_cache ()#line:393
    elif O00OOOOOO0O00O0OO =="AS":#line:394
        xbmc .executebuiltin ('Addon.OpenSettings(%s)'%addon_id )#line:395
    elif O00OOOOOO0O00O0OO =="ADS":#line:396
        O00OO0O0O00OO0OOO =xbmcgui .Dialog ().select ('Edit Advanced Settings',['[COLOR dodgerblue]* [/COLOR][COLOR lime][I]Amazon Firestick[/I][/COLOR]','[COLOR dodgerblue]* [/COLOR][COLOR lime][I]2GB Ram or Higher[/I][/COLOR]','[COLOR dodgerblue]* [/COLOR][COLOR lime][I]Zero Cache[/I][/COLOR]','[COLOR dodgerblue]* [/COLOR][COLOR lime][I]Nvidia Shield[/I][/COLOR]','[COLOR dodgerblue]* [/COLOR][COLOR lime][I]Disable Advanced Settings[/I][/COLOR]'])#line:397
        if O00OO0O0O00OO0OOO ==0 :#line:398
            advancedsettings ('stick')#line:399
            xbmcgui .Dialog ().ok ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]','[COLOR lime]Set Advanced Settings[/COLOR]')#line:400
        elif O00OO0O0O00OO0OOO ==1 :#line:401
            advancedsettings ('firetv')#line:402
            xbmcgui .Dialog ().ok ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]','[COLOR lime]Set Advanced Settings[/COLOR]')#line:403
        elif O00OO0O0O00OO0OOO ==2 :#line:404
            advancedsettings ('lessthan')#line:405
            xbmcgui .Dialog ().ok ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]','[COLOR lime]Set Advanced Settings[/COLOR]')#line:406
        elif O00OO0O0O00OO0OOO ==3 :#line:407
            advancedsettings ('morethan')#line:408
            xbmcgui .Dialog ().ok ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]','[COLOR lime]Set Advanced Settings[/COLOR]')#line:409
        elif O00OO0O0O00OO0OOO ==4 :#line:410
            advancedsettings ('shield')#line:411
            xbmcgui .Dialog ().ok ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]','[COLOR lime]Set Advanced Settings[/COLOR]')#line:412
        elif O00OO0O0O00OO0OOO ==5 :#line:413
            advancedsettings ('remove')#line:414
            xbmcgui .Dialog ().ok ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]','[COLOR lime]Advanced Settings Removed[/COLOR]')#line:415
    elif O00OOOOOO0O00O0OO =="ADS2":#line:416
        O00OO0O0O00OO0OOO =xbmcgui .Dialog ().select ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]  Select Your Device',['[COLOR lime][I]Amazon Firestick[/I][/COLOR]','[COLOR lime][I]2GB Ram or Higher[/I][/COLOR]','[COLOR lime][I]Zero Cache[/I][/COLOR]','[COLOR lime][I]Nvidia Shield[/I][/COLOR]'])#line:417
        if O00OO0O0O00OO0OOO ==0 :#line:418
            advancedsettings ('stick')#line:419
            xbmcgui .Dialog ().ok ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]','[COLOR lime]Set Advanced Settings[/COLOR]')#line:420
        elif O00OO0O0O00OO0OOO ==1 :#line:421
            advancedsettings ('firetv')#line:422
            xbmcgui .Dialog ().ok ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]','[COLOR lime]Set Advanced Settings[/COLOR]')#line:423
        elif O00OO0O0O00OO0OOO ==2 :#line:424
            advancedsettings ('lessthan')#line:425
            xbmcgui .Dialog ().ok ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]','[COLOR lime]Set Advanced Settings[/COLOR]')#line:426
        elif O00OO0O0O00OO0OOO ==3 :#line:427
            advancedsettings ('morethan')#line:428
            xbmcgui .Dialog ().ok ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]','[COLOR lime]Set Advanced Settings[/COLOR]')#line:429
        elif O00OO0O0O00OO0OOO ==4 :#line:430
            advancedsettings ('shield')#line:431
            xbmcgui .Dialog ().ok ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]','[COLOR lime]Set Advanced Settings[/COLOR]')#line:432
    elif O00OOOOOO0O00O0OO =="tv":#line:433
        ivueint ()#line:434
    elif O00OOOOOO0O00O0OO =="ST":#line:436
        xbmc .executebuiltin ('Runscript("special://home/addons/plugin.video.hypersonicIPTV2/resources/modules/speedtest.py")')#line:437
    elif O00OOOOOO0O00O0OO =="META":#line:438
        if 'ON'in O0OO00O0000O0O000 :#line:439
            xbmcaddon .Addon ().setSetting ('meta','false')#line:440
            xbmc .executebuiltin ('Container.Refresh')#line:441
        else :#line:442
            xbmcaddon .Addon ().setSetting ('meta','true')#line:443
            xbmc .executebuiltin ('Container.Refresh')#line:444
    elif O00OOOOOO0O00O0OO =="LO":#line:445
        xbmcaddon .Addon ().setSetting ('Username','')#line:446
        xbmcaddon .Addon ().setSetting ('Password','')#line:447
        xbmc .executebuiltin ('XBMC.ActivateWindow(Videos,addons://sources/video/)')#line:448
        xbmc .executebuiltin ('Container.Refresh')#line:449
    elif O00OOOOOO0O00O0OO =="UPDATE":#line:450
        if 'ON'in O0OO00O0000O0O000 :#line:451
            xbmcaddon .Addon ().setSetting ('update','false')#line:452
            xbmc .executebuiltin ('Container.Refresh')#line:453
        else :#line:454
            xbmcaddon .Addon ().setSetting ('update','true')#line:455
            xbmc .executebuiltin ('Container.Refresh')#line:456
def advancedsettings (O0000OO000O0O000O ):#line:459
    if O0000OO000O0O000O =='stick':#line:460
        OOOO000O0O00O00OO =open (os .path .join (advanced_settings ,'stick.xml'))#line:461
    elif O0000OO000O0O000O =='firetv':#line:462
        OOOO000O0O00O00OO =open (os .path .join (advanced_settings ,'firetv.xml'))#line:463
    elif O0000OO000O0O000O =='lessthan':#line:464
        OOOO000O0O00O00OO =open (os .path .join (advanced_settings ,'zero.xml'))#line:465
    elif O0000OO000O0O000O =='morethan':#line:466
        OOOO000O0O00O00OO =open (os .path .join (advanced_settings ,'shield.xml'))#line:467
    elif O0000OO000O0O000O =='remove':#line:468
        os .remove (advanced_settings_target )#line:469
    try :#line:471
        OOOO00O0O00OO00O0 =OOOO000O0O00O00OO .read ()#line:472
        O0OOOO0OOOOOO00OO =open (advanced_settings_target ,mode ='w+')#line:473
        O0OOOO0OOOOOO00OO .write (OOOO00O0O00OO00O0 )#line:474
        O0OOOO0OOOOOO00OO .close ()#line:475
    except :#line:476
        pass #line:477
def pvrsetup ():#line:480
    correctPVR ()#line:481
    killxbmc ()#line:482
    return #line:483
def asettings ():#line:486
    OO000O0O00OOO00OO =xbmcgui .Dialog ().yesno ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]','Please Select The RAM Size of Your Device',yeslabel ='Less than 1GB RAM',nolabel ='More than 1GB RAM')#line:487
    if OO000O0O00OOO00OO :#line:488
        lessthan ()#line:489
    else :#line:490
        morethan ()#line:491
def morethan ():#line:494
        OO000O0OOO000OO00 =open (os .path .join (advanced_settings ,'shield.xml'))#line:495
        O0OO0OOOO00OOOO0O =OO000O0OOO000OO00 .read ()#line:496
        OOOOO000OOOO00OOO =open (advanced_settings_target ,mode ='w+')#line:497
        OOOOO000OOOO00OOO .write (O0OO0OOOO00OOOO0O )#line:498
        OOOOO000OOOO00OOO .close ()#line:499
def lessthan ():#line:502
        OO0000OOOO00OOOOO =open (os .path .join (advanced_settings ,'zero.xml'))#line:503
        O0OO0000000O0OO0O =OO0000OOOO00OOOOO .read ()#line:504
        O0OO0OOOO0OO0OOO0 =open (advanced_settings_target ,mode ='w+')#line:505
        O0OO0OOOO0OO0OOO0 .write (O0OO0000000O0OO0O )#line:506
        O0OO0OOOO0OO0OOO0 .close ()#line:507
def userpopup ():#line:510
    O000OO0OO0OOOO0O0 =xbmc .Keyboard ('','heading',True )#line:511
    O000OO0OO0OOOO0O0 .setHeading ('Enter Username')#line:512
    O000OO0OO0OOOO0O0 .setHiddenInput (False )#line:513
    O000OO0OO0OOOO0O0 .doModal ()#line:514
    if (O000OO0OO0OOOO0O0 .isConfirmed ()):#line:515
        O00OO00OO0OOO0O00 =O000OO0OO0OOOO0O0 .getText ()#line:516
        return O00OO00OO0OOO0O00 #line:517
    else :#line:518
        return False #line:519
def passpopup ():#line:522
    O00O0O0O0O00000OO =xbmc .Keyboard ('','heading',True )#line:523
    O00O0O0O0O00000OO .setHeading ('Enter Password')#line:524
    O00O0O0O0O00000OO .setHiddenInput (False )#line:525
    O00O0O0O0O00000OO .doModal ()#line:526
    if (O00O0O0O0O00000OO .isConfirmed ()):#line:527
        O0OO0000OOOOOOOOO =O00O0O0O0O00000OO .getText ()#line:528
        return O0OO0000OOOOOOOOO #line:529
    else :#line:530
        return False #line:531
def accountinfo ():#line:534
    OO0O000OOO0000000 =json .load (urllib2 .urlopen (panel_api ))#line:535
    O0000OO0OO0OO0O00 =["0"," ","null"]#line:536
    O000O0O0OOOOO00OO =datetime .date .today ()#line:537
    OOOOO00O0OOO0OO00 =OO0O000OOO0000000 ['user_info']#line:538
    O0OO0O000OO0O00OO =OOOOO00O0OOO0OO00 ['username']#line:539
    OO00OOOO00O00O0O0 =OOOOO00O0OOO0OO00 ['status']#line:540
    O0000OO000O00O000 =OOOOO00O0OOO0OO00 ['created_at']#line:541
    OO0OO0O0OO0O000O0 =datetime .datetime .fromtimestamp (int (O0000OO000O00O000 )).strftime ('%H:%M %m/%d/%Y')#line:542
    OOOOO000OOO000O00 =OOOOO00O0OOO0OO00 ['active_cons']#line:543
    O0OOOOOOOOO0OOOO0 =OOOOO00O0OOO0OO00 ['max_connections']#line:544
    OOO0O00OO0OO000OO =OOOOO00O0OOO0OO00 ['exp_date']#line:545
    if OOO0O00OO0OO000OO ==None :#line:546
        OOO00000OOOOO0O0O ='Never'#line:547
    else :#line:548
        OOO00000OOOOO0O0O =datetime .datetime .fromtimestamp (int (OOO0O00OO0OO000OO )).strftime ('%H:%M %m/%d/%Y')#line:549
    tools .addDir ('[COLOR dodgerblue]   Hypersonic [COLOR white]IPTV2[/COLOR]','','',icon ,account ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR]')#line:550
    tools .addDir ('[COLOR lime]* [/COLOR][COLOR white]Username :[/COLOR] '+O0OO0O000OO0O00OO ,'','',icon ,account ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR][CR][COLORwhite]Please report any channel issues in the Telegram support chat group.[CR]We are there 24/7 to help you to have the best streaming experience you deserve.[/COLOR][CR][COLOR lime]t.me/joinchat/[CR]C0Xm8kLuekY7UZWQ5u85lQ[/COLOR]')#line:551
    tools .addDir ('[COLOR lime]* [/COLOR][COLOR white]Expire Date:[/COLOR] '+OOO00000OOOOO0O0O ,'','',icon ,account ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR][CR][COLORwhite]Please report any channel issues in the Telegram support chat group.[CR]We are there 24/7 to help you to have the best streaming experience you deserve.[/COLOR][CR][COLOR lime]t.me/joinchat/[CR]C0Xm8kLuekY7UZWQ5u85lQ[/COLOR]')#line:552
    tools .addDir ('[COLOR lime]* [/COLOR][COLOR white]Account Status :[/COLOR] '+OO00OOOO00O00O0O0 ,'','',icon ,account ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR][CR][COLORwhite]Please report any channel issues in the Telegram support chat group.[CR]We are there 24/7 to help you to have the best streaming experience you deserve.[/COLOR][CR][COLOR lime]t.me/joinchat/[CR]C0Xm8kLuekY7UZWQ5u85lQ[/COLOR]')#line:553
    tools .addDir ('[COLOR lime]* [/COLOR][COLOR white]Current Connections:[/COLOR] '+OOOOO000OOO000O00 ,'','',icon ,account ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR][CR][COLORwhite]Please report any channel issues in the Telegram support chat group.[CR]We are there 24/7 to help you to have the best streaming experience you deserve.[/COLOR][CR][COLOR lime]t.me/joinchat/[CR]C0Xm8kLuekY7UZWQ5u85lQ[/COLOR]')#line:554
    tools .addDir ('[COLOR lime]* [/COLOR][COLOR white]Allowed Connections:[/COLOR] '+O0OOOOOOOOO0OOOO0 ,'','',icon ,account ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR][CR][COLORwhite]Please report any channel issues in the Telegram support chat group.[CR]We are there 24/7 to help you to have the best streaming experience you deserve.[/COLOR][CR][COLOR lime]t.me/joinchat/[CR]C0Xm8kLuekY7UZWQ5u85lQ[/COLOR]')#line:555
    tools .addDir ('[COLOR lime]* [/COLOR][COLOR white]Created:[/COLOR] '+OO0OO0O0OO0O000O0 ,'','',icon ,account ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR][CR][COLORwhite]Please report any channel issues in the Telegram support chat group.[CR]We are there 24/7 to help you to have the best streaming experience you deserve.[/COLOR][CR][COLOR lime]t.me/joinchat/[CR]C0Xm8kLuekY7UZWQ5u85lQ[/COLOR]')#line:556
    tools .addDir ('[COLOR lime]* [/COLOR][COLOR white]Log Out[/COLOR]','LO',10 ,icon ,account ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR]')#line:557
    tools .addDir ('To reactivate account please visit:[CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR]',All ,2 ,icon ,account ,'[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR][CR][COLOR white]DISCOVER THE FUTURE OF LIVE TV[/COLOR][CR][COLORlime]https://gethypersonic.mytvpro.org[/COLOR][CR][B][COLOR yellow]Please download our APP for VOD[/COLOR][/B][CR][COLOR white]FileLinked code: 60517827[CR][COLOR lime]http://hypersonic-tv.com/[CR]hypersonic.apk[/COLOR]')#line:558
    plugintools .set_view (plugintools .MOVIES )#line:559
def correctPVR ():#line:562
    O0OO0OOO0OO0OOO0O =xbmcaddon .Addon ('plugin.video.hypersonicIPTV2')#line:564
    OO00O0OOO0O0000O0 =O0OO0OOO0OO0OOO0O .getSetting (id ='Username')#line:565
    O0O0O0OOOOO00OO0O =O0OO0OOO0OO0OOO0O .getSetting (id ='Password')#line:566
    O0O0O0000000OOOO0 ='{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":true},"id":1}'#line:567
    O000OOOO0OOOOO0O0 ='{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}'#line:568
    OOOO00000OO00O0OO ='{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.demo","enabled":false},"id":1}'#line:569
    O00OO0O000OO0OO0O ="http://live.hypersonic-tv.com:83/get.php?username="+OO00O0OOO0O0000O0 +"&password="+O0O0O0OOOOO00OO0O +"&type=m3u_plus&output=ts"#line:570
    O0OOOO0O000000O00 ="http://live.hypersonic-tv.com:83/xmltv.php?username="+OO00O0OOO0O0000O0 +"&password="+O0O0O0OOOOO00OO0O #line:571
    xbmc .executeJSONRPC (O0O0O0000000OOOO0 )#line:573
    xbmc .executeJSONRPC (O000OOOO0OOOOO0O0 )#line:574
    xbmc .executeJSONRPC (OOOO00000OO00O0OO )#line:575
    OO0OO0O0O00OOOO0O =xbmcaddon .Addon ('pvr.iptvsimple')#line:577
    OO0OO0O0O00OOOO0O .setSetting (id ='m3uUrl',value =O00OO0O000OO0OO0O )#line:578
    OO0OO0O0O00OOOO0O .setSetting (id ='epgUrl',value =O0OOOO0O000000O00 )#line:579
    OO0OO0O0O00OOOO0O .setSetting (id ='m3uCache',value ="false")#line:580
    OO0OO0O0O00OOOO0O .setSetting (id ='epgCache',value ="false")#line:581
def ivueint ():#line:583
    ivuesetup .iVueInt ()#line:584
    xbmcgui .Dialog ().ok ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]','iVue Integration Complete')#line:585
    xbmc .executebuiltin ('ActivateWindow(10025,"plugin://plugin.video.IVUEcreator/update_addon/plugin.video.hypersonicIPTV2",return)')#line:586
    xbmc .executebuiltin ("XBMC.ActivateWindow(Home)")#line:587
def ivueint2 ():#line:589
    ivuesetup .iVueInt2 ()#line:590
    xbmcgui .Dialog ().ok ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]','[COLORlime]iVue Integration Complete[/COLOR]')#line:591
    home ()#line:592
def SIMPLEtvguidesetup ():#line:595
    OO000OOO00OOOOO0O =xbmcgui .Dialog ().yesno ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]','[COLORlime]Would you like us to setup Simple PVR Guide for you?[/COLOR]')#line:596
    if OO000OOO00OOOOO0O :#line:597
        pvrsetup ()#line:598
    else :#line:599
        home ()#line:600
def IVUEtvguidesetup ():#line:602
    O00OO00000OO0OO00 =xbmcgui .Dialog ().yesno ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]','[COLORlime]Would You like us to Setup iVue TV Guide for You?[/COLOR]')#line:603
    if O00OO00000OO0OO00 :#line:604
        ivueint ()#line:605
    else :#line:606
        home ()#line:607
def ivue_settings ():#line:609
    xbmc .executebuiltin ("Addon.OpenSettings(script.ivueguide)")#line:610
def HypersonicIPTV2_settings ():#line:612
    xbmc .executebuiltin ("Addon.OpenSettings(plugin.video.hypersonicIPTV2)")#line:613
def setView ():#line:616
    xbmc .executebuiltin ("Container.SetViewMode(50)")#line:617
def killxbmc (over =None ):#line:619
    OO0OOO0OO0OOO000O =xbmcgui .Dialog ().yesno ('Force Close Kodi','[COLOR white]You are about to close Kodi','Would you like to continue?[/COLOR]',nolabel ='[B][COLOR red] No Cancel[/COLOR][/B]',yeslabel ='[B][COLOR green]Force Close Kodi[/COLOR][/B]')#line:620
    if OO0OOO0OO0OOO000O :#line:621
        os ._exit (1 )#line:622
    else :#line:623
        home ()#line:624
def adultpopup ():#line:626
    O0000OOOO0OOO0O0O =xbmc .Keyboard ('','heading',True )#line:627
    O0000OOOO0OOO0O0O .setHeading ('[COLORlime]Enter Adult Password[/COLOR]')#line:628
    O0000OOOO0OOO0O0O .setHiddenInput (False )#line:629
    O0000OOOO0OOO0O0O .doModal ()#line:630
    if (O0000OOOO0OOO0O0O .isConfirmed ()):#line:631
        O00OO000OO000OO00 =O0000OOOO0OOO0O0O .getText ()#line:632
        return O00OO000OO000OO00 #line:633
    else :#line:634
        return False #line:635
def adult_settings ():#line:637
    OO0OOO0O0O0OO0O0O =xbmcgui .Dialog ().yesno ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]','[COLORlime]Would you like to HIDE[/COLOR] [COLOR deeppink]Adult Menu[/COLOR]?','[COLORlime]You can always change this in settings later on.[/COLOR]')#line:638
    if OO0OOO0O0O0OO0O0O :#line:639
        control .setSetting ('Adult.Set','true')#line:640
        pass #line:641
    else :#line:642
        control .setSetting ('Adult.Set','false')#line:643
        pass #line:644
    OO0OOO0O0O0OO0O0O =xbmcgui .Dialog ().yesno ('[COLOR dodgerblue]Hypersonic [COLOR white]IPTV2[/COLOR]','[COLORlime]Would you like to PASSWORD PROTECT[/COLOR] [COLOR deeppink]Adult Channels[/COLOR]?','[COLORlime]You can always change this in settings later on.[/COLOR]')#line:645
    if OO0OOO0O0O0OO0O0O :#line:646
        control .setSetting ('Adult.PWSet','true')#line:647
        OOO0O0OOO0000000O =adultpopup ()#line:648
        control .setSetting ('Adult.PW',OOO0O0OOO0000000O )#line:649
    else :#line:650
        control .setSetting ('Adult.PWSet','false')#line:651
        pass #line:652
def testarea ():#line:655
    OO000O0OOO000O000 =xbmc .translatePath (os .path .join ('special://home/userdata/addon_data/plugin.video.hypersonicIPTV2/categories.db'))#line:656
    OOO00000OO0O00O0O =[]#line:657
    if os .path .isfile (OO000O0OOO000O000 ):#line:659
        os .remove (OO000O0OOO000O000 )#line:660
    OO0OO00O0O0OOO00O =tools .OPEN_URL (live_url )#line:663
    O00000O0O0O00O0OO =tools .regex_get_all (OO0OO00O0O0OOO00O ,'<channel>','</channel>')#line:664
    for O000OO00OO0O0O0OO in O00000O0O0O00O0OO :#line:665
            OO00O0O0OOOOO0000 =tools .regex_from_to (O000OO00OO0O0O0OO ,'<title>','</title>')#line:666
            OO00O0O0OOOOO0000 =base64 .b64decode (OO00O0O0OOOOO0000 )#line:667
            OO00O0O0OOOOO0000 =re .sub (' ','_',OO00O0O0OOOOO0000 )#line:668
            OO00O0O0OOOOO0000 =re .sub ('&','_',OO00O0O0OOOOO0000 )#line:669
            OO00O0O0OOOOO0000 =re .sub ('\/','_',OO00O0O0OOOOO0000 )#line:670
            OO00O0O0OOOOO0000 =re .sub ('\+','_',OO00O0O0OOOOO0000 )#line:671
            xbmc .log (str (OO00O0O0OOOOO0000 ))#line:672
            try :#line:673
                OO00O0O0OOOOO0000 =re .sub ('\[.*?min ','-',OO00O0O0OOOOO0000 )#line:674
            except :#line:675
                pass #line:676
            OOO0OO0O000OOOO00 =tools .regex_from_to (O000OO00OO0O0O0OO ,'<category_id>','</category_id>')#line:677
            OOOO0O000OOO000OO ="%s = %s\n"%(OO00O0O0OOOOO0000 ,OOO0OO0O000OOOO00 )#line:678
            OOO00000OO0O00O0O .append (OOOO0O000OOO000OO )#line:679
    for O0OOOO00OO0O0OO0O in OOO00000OO0O00O0O :#line:681
        O000OO0OOOO00O0O0 =open (OO000O0OOO000O000 ,mode ='a')#line:682
        O000OO0OOOO00O0O0 .write (O0OOOO00OO0O0OO0O )#line:683
        O000OO0OOOO00O0O0 .close ()#line:684
def changenumbers (OO0O00OOOO0OO0O00 ):#line:688
    OO000O00OO000OOO0 ={'1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine','10':'ten','11':'eleven','12':'twelve',}#line:691
    for O00O0OO00OO000O00 ,OOO0OO0OO00OOOOOO in OO000O00OO000OOO0 .iteritems ():#line:693
        if O00O0OO00OO000O00 in OO0O00OOOO0OO0O00 :#line:694
            OO0O00OOOO0OO0O00 =OO0O00OOOO0OO0O00 .replace (O00O0OO00OO000O00 ,OOO0OO0OO00OOOOOO )#line:695
    return OO0O00OOOO0OO0O00 #line:697
def num2day (O00OOOO00OOO0O0OO ):#line:699
    if O00OOOO00OOO0O0OO =="0":#line:700
        OOOOOO00O0O0OOOO0 ='monday'#line:701
    elif O00OOOO00OOO0O0OO =="1":#line:702
        OOOOOO00O0O0OOOO0 ='tuesday'#line:703
    elif O00OOOO00OOO0O0OO =="2":#line:704
        OOOOOO00O0O0OOOO0 ='wednesday'#line:705
    elif O00OOOO00OOO0O0OO =="3":#line:706
        OOOOOO00O0O0OOOO0 ='thursday'#line:707
    elif O00OOOO00OOO0O0OO =="4":#line:708
        OOOOOO00O0O0OOOO0 ='friday'#line:709
    elif O00OOOO00OOO0O0OO =="5":#line:710
        OOOOOO00O0O0OOOO0 ='saturday'#line:711
    elif O00OOOO00OOO0O0OO =="6":#line:712
        OOOOOO00O0O0OOOO0 ='sunday'#line:713
    return OOOOOO00O0O0OOOO0 #line:714
setView ()#line:716
params =tools .get_params ()#line:717
url =None #line:718
name =None #line:719
mode =None #line:720
iconimage =None #line:721
description =None #line:722
query =None #line:723
type =None #line:724
try :#line:726
    url =urllib .unquote_plus (params ["url"])#line:727
except :#line:728
    pass #line:729
try :#line:730
    name =urllib .unquote_plus (params ["name"])#line:731
except :#line:732
    pass #line:733
try :#line:734
    iconimage =urllib .unquote_plus (params ["iconimage"])#line:735
except :#line:736
    pass #line:737
try :#line:738
    mode =int (params ["mode"])#line:739
except :#line:740
    pass #line:741
try :#line:742
    description =urllib .unquote_plus (params ["description"])#line:743
except :#line:744
    pass #line:745
try :#line:746
    query =urllib .unquote_plus (params ["query"])#line:747
except :#line:748
    pass #line:749
try :#line:750
    type =urllib .unquote_plus (params ["type"])#line:751
except :#line:752
    pass #line:753
if mode ==None or url ==None or len (url )<1 :#line:755
    start ()#line:756
elif mode ==1 :#line:758
    livecategory (url )#line:759
elif mode ==2 :#line:761
    Livelist (url )#line:762
elif mode ==3 :#line:764
    vod (url )#line:765
elif mode ==4 :#line:767
    stream_video (url )#line:768
elif mode ==5 :#line:770
    search ()#line:771
elif mode ==6 :#line:773
    accountinfo ()#line:774
elif mode ==7 :#line:776
    simpletvguide ()#line:777
elif mode ==8 :#line:779
    settingsmenu ()#line:780
elif mode ==9 :#line:782
    xbmc .executebuiltin ('ActivateWindow(busydialog)')#line:783
    tools .Trailer ().play (url )#line:784
    xbmc .executebuiltin ('Dialog.Close(busydialog)')#line:785
elif mode ==10 :#line:787
    addonsettings (url ,description )#line:788
elif mode ==11 :#line:790
    SIMPLEtvguidesetup ()#line:791
elif mode ==15 :#line:793
    ivueint ()#line:794
elif mode ==17 :#line:796
    shortlinks .Get ()#line:797
elif mode ==19 :#line:799
    get ()#line:800
elif mode ==20 :#line:802
    SoftReset ()#line:803
elif mode ==25 :#line:805
    LiveInfolist (url )#line:806
elif mode ==27 :#line:808
    guides ()#line:809
elif mode ==36 :#line:811
    ivueint2 ()#line:812
elif mode ==37 :#line:814
    series (url )#line:815
elif mode ==38 :#line:817
    ivue_settings ()#line:818
elif mode ==39 :#line:820
    HypersonicIPTV2_settings ()#line:821
elif mode ==40 :#line:823
    simpletvguide ()#line:824
elif mode ==44 :#line:826
    ivuetvguide ()#line:827
elif mode ==45 :#line:829
    simplechannels ()#line:830
xbmcplugin .endOfDirectory (int (sys .argv [1 ]))#line:837

