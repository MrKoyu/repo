import xbmcaddon
# 2018-05-13 
#####--Addon details--#####
'''change name to that of your addon, same as file name'''
addon = xbmcaddon.Addon('plugin.video.Redemption') 

####--Route to text file--######
'''change Mainbase URL link to the URL of your 1st text file or home text file and encode using encoder If you have a backup of txt on another server put URL in backup will swap servers if a error occurs'''
MainBase = 'http://redemption.wf/RedemptionText/home.txt'
BackUp   = ''
PopUpNotice = ''

####----Search Functions----####
''' True if you wish to search for this content within addon or False if not, Search movie and tv will use the TMDB api to pull list of movies or tv shows relating to the search then will search the addon for that content, Search Content will take a direct input string and search the addon this is mainly for addons that are not movie or tv content and not using the TMDB api Key, You can also customize the message for the search input keyboard '''
Enable_Search_Dir = True
Search_Movies     = False
Search_Tv         = False
Search_Content    = True
Search_Content_KeyBoardMsg = '[COLORyellow]REDEMPTION SEARCH[/COLOR]'
#####-----TMDB------######
####----TMDB Lists----####
"""For return on TMDB Movie lists you can either search addon for content or use uni scraper to find content in TMDBMovieList enter either 'search_addon' or 'search_internet' as a string """
TMDBMovieList = 'search_addon'

####---API Keys--####
'''if you are to use own api key and wish to use it in addon for all insert here also in settings is a place to enter the key Edit UseTMDB to False, api key requires encoding the same way as MainBase is  '''
UseTMDB  = True
TMDB_api = 'NzQxMWI4ZWQ5YWM1Y2JhMTU4NGJiN2FkMTA3ZjZjODc='
#####-----Text-----#####
'''where several strings are joined to create a name for a directory input your delimiter, if you would like a space before and or after the delimiter modify TxtDelimiterAddSpaces to both,after,before'''
TxtDelimiter = '|'
TxtDelimiterAddSpaces = 'Both'
TxtDelimiterAddSpacesAmount = 2
TxtDelimiterColor = 'orange'
#####---Text Color---#####
'''Enter text color you wish the title to be if just a color is required set TxtColor1 to a color, if splitting for 2 colors add TxtColor2, TxtSplit is point of change color can be space or word, if word is used a value must be entered in TxtSpoint so if 2 is enter the color will change at 2nd letter of the word it will only do the 1st 2 words of the string same with using space '''
#####-----Channel text color set up----#####
ChannelTxtColor1 = 'blue'
ChannelTxtColor2 = 'blue'
ChannelTxtSplit  = 'space'
ChannelTxtSpoint = ''
#####-----Item text color set up -----#####
ItemTxtColor1    = 'red'
ItemTxtColor2    = 'red'
ItemTxtSplit     = 'word'
ItemTxtSpoint    = '2'
####-----Dialog Boxes-----#####
'''Colors for pop up dialog boxes text '''
DialogBoxColor1 = 'redwhite'
DialogBoxColor2 = 'pinkblue'

#####--Art Work--#####
'''Change these paths if you wish to use custom art work for hard coded sections favorites,settings,history, DailyMotion, Search ,Next page or YouTube icons, 5 icons are already stored but you may wish to use your own to change you can either replace the icons in the resources/art folder remember to keep the name the same or put a URL in the paths below. If you wish to use custom fanart for theses sections enter a URL in to the path else the standard fanart will be used'''
DailyMotionIcon   = ''
DailyMotionFanart = ''
FavoriteIcon      = 'https://icons-for-free.com/free-icons/png/512/2203510.png'
FavoriteFanart    = 'https://wallpaperplay.com/walls/full/d/e/f/301291.jpg'
HistoryIcon       = 'https://ya-webdesign.com/images/chrome-svg-history-19.png'
HistoryFanart     = 'https://i.pinimg.com/originals/ff/ca/db/ffcadb414b6dd0a706fd9ac872f0b229.jpg'
NextPageIcon      = 'https://pngimage.net/wp-content/uploads/2018/06/next-page-png-5.png'
SearchIcon        = 'https://www.freeiconspng.com/uploads/search-icon-png-0.png'
SearchFanart      = 'https://fanart.tv/fanart/movies/4247/moviebackground/scary-movie-5292f278cf069.jpg'
SettingIcon       = 'https://image.flaticon.com/icons/png/512/60/60473.png'
SettingFanart     = 'http://www.technocrazed.com/wp-content/uploads/2015/12/black-wallpaper-to-set-as-background-19.jpg'
TmdbIcon          = 'https://png.pngtree.com/svg/20170330/imdb_10168.png'
TmdbFanart        = 'https://static1.squarespace.com/static/51b3dc8ee4b051b96ceb10de/t/5ba53ddac83025ebed0e9081/1537555934228/?format=2500w'
YouTubeIcon       = 'http://1.bp.blogspot.com/-l6CibjUu4g4/UWsB-y62XLI/AAAAAAAAAbo/yTuA0DLlmho/s1600/YouTube-02.png' #channel listings only text file and hard code YouTube Search 
YouTubeFanart     = 'https://i.pinimg.com/originals/83/76/96/83769692c62267e444a44a7efee90336.jpg'
'''You tube search list does not pull any fanart if default will be standard fanart of addon if you would like to use custom enter URL in between speech marks empty speech marks will use default'''
YT_SearchFanart = 'https://wallpapercave.com/wp/wp2212270.jpg'
'''Podcast info puller use icon image as fanart most images pulled are good enough to use as fanart set to False if you wish to use addon fanart'''
PodcastFanart = False

#####--PodCast--#####
'''For using the Podcast RSS puller you can preset the length of the list of returned Podcasts if you wish to restrict the length of list change PodcastListSetLength to True and PodcastListLength enter the value as a int of the number wanting returned also in user settings the end user may set there own amount '''
PodcastListSetLength = False
PodcastListLength = ''


#####-----Universal Scrapers-----#####
'''Show progress dialog of scrapers running if False standard rotating circle will show 
For the order in which the links will be listed, UniSortMethods 'quality','source', if left blank a Random sort method will be applied, changing UniSortReverse to True will reverse order the list only works in combination with UniSortMethod if a string is added ie 'quality'
if UniDialogSelect is True the returned list will be displayed as a dialog select box, False will be displayed as standard directory   '''
UniShowProgress = False
UniSortMethod = ''
UniSortReverse = False
UniDialogSelect = False 

######-------Tools settings-------######
''''To display tool/setting directory use True to Hide use false'''
Enable_ToolsSetting_Dir = False

#####-----Pop Up Dialog-----#####
'''Header and Body BaseColor is "white" or "black",Header and Body BaseTrans is how transparent the base is 50, 75 or 100 as a percentage, colors can be sent as word that kodi uses or as a hex code '''
guiHeaderBaseColor = 'white'
guiHeaderBaseTrans = '100'
guiHeaderColor = 'lime'
guiHeaderTxtColor = 'orangered'
guiHeaderTxtShadow = 'white'
guiBodyBaseColor = 'white'
guiBodyBaseTrans = '75'
guiBodyColor     = 'mediumblue'
guiBodyTxtColor = 'white'
guiBodyTxtShadow = 'navy'
guiSliderBarColor = 'yellow'
guiSliderColorNoFocus = 'yellowgreen'
guiSliderColorFocus = 'gold'
guiButtonColorNoFocus = 'violet'
guiButtonColorFocus = 'purple'
guiButtonTxtColor = 'cyan'

#####--Hard Coding settings--###(Not function yet!!!!)
'''use text files as source of content and menu's it is possible to use a mixture of both'''
HCS_text = True
'''use hard coded directories change to true if you want to use other methods of adding content other then text files'''
HCS_addDir = False

'''#####-----Update notes -------#######
2018-06-25 Added variable to  disable search menu,Added variable to disable tools settings menu
2018-06-04 Added Variables for custom gui dialogs,Added variable for search addon pop up message on keyboard
2018-05-24 Added variables for TMDB Lists
2018-05-13 Added variables for string delimiter 
2018-05-06 Added Variables for text color 
2018-04-30 Added variables for My TMDB and Search
2018-04-17 Added backup server option 
2018-04-16 Added Podcast settings
2018-04-11 Added TMDB settings 
2018-04-09 Added option for History Icon and fanart'''