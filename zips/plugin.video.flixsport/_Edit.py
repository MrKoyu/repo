import xbmcaddon
# 2018-04-17 
#####--Addon details--#####
'''change name to that of your addon, same as file name'''
addon = xbmcaddon.Addon('plugin.video.flixsport') 


####--Route to text file--######
'''change Mainbase URL link to the URL of your 1st text file or home text file and encode using encoder If you have a backup of txt on another server put URL in backup will swap servers if a error occurs'''
MainBase = 'aHR0cDovL21ybnVtYmVycy54eXovU3BvcnRzZmxpeE1haW4xLnhtbA=='
BackUp   = 'http://bigyidbuilds.com/oka_backup_txt/example_text_files/podcast/podcast_channel.txt'


####----Search Functions----####
''' True if you wish to search for this content within addon or False if not, Search movie and tv will use the TMDB api to pull list of movies or tv shows relating to the search then will search the addon for that content Search Content will take a direct input string and search the addon this is mainly for addons that are not movie or tv content and not using the TMDB api Key '''
Search_Movies  = True
Search_Tv      = True
Search_Content = True



####---API Keys--####
'''if you are to use own api key and wish to use it in addon for all insert here also in settings is a place to enter the key Edit UseTMDB to False api key requires encoding  '''
UseTMDB  = True
TMDB_api = '30e2ba911c0ecc1b3577da9cb85b46f3'

#####---Text Color---#####(not complete yet)
'''Enter text color you wish the title to be '''
ChannelTxtColor = ''
ItemTxtColor = ''

#####--Art Work--#####
'''Change these paths if you wish to use custom art work for hard coded sections favorites,settings,history, DailyMotion, Search ,Next page or YouTube icons, 5 icons are already stored but you may wish to use your own to change you can either replace the icons in the resources/art folder remember to keep the name the same or put a URL in the paths below. If you wish to use custom fanart for theses sections enter a URL in to the path else the standard fanart will be used'''
DailyMotionIcon   = ''
DailyMotionFanart = ''
FavoriteIcon      = ''
FavoriteFanart    = ''
HistoryIcon       = ''
HistoryFanart     = ''
NextPageIcon      = ''
SearchIcon        = ''
SearchFanart      = ''
SettingIcon       = ''
SettingFanart     = ''
TmdbIcon          = ''
TmdbFanart        = ''
YouTubeIcon       = '' #channel listings only text file and hard code YouTube Search 
YouTubeFanart     = ''
'''You tube search list does not pull any fanart if default will be standard fanart of addon if you would like to use custom enter URL in between speech marks empty speech marks will use default'''
YT_SearchFanart = ''
'''Podcast info puller use icon image as fanart most images pulled are good enough to use as fanart set to False if you wish to use addon fanart'''
PodcastFanart = True

#####--PodCast--#####
'''For using the Podcast RSS puller you can preset the length of the list of returned Podcasts if you wish to restrict the length of list change PodcastListSetLength to True and PodcastListLength enter the value as a int of the number wanting returned also in user settings the end user may set there own amount '''
PodcastListSetLength = False
PodcastListLength = ''

#####--Hard Coding settings--###(Not function yet!!!!)
'''use text files as source of content and menu's it is possible to use a mixture of both'''
HCS_text = True
'''use hard coded directories change to true if you want to use other methods of adding content other then text files'''
HCS_addDir = False

'''#####-----Update notes -------#######
2018-04-30 Added variables for My TMDB and Search
2018-04-17 Added backup server option 
2018-04-16 Added Podcast settings
2018-04-11 Added TMDB settings 
2018-04-09 Added option for History Icon and fanart'''