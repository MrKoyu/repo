# -*- coding: utf-8 -*-

'''
 ███▄    █  █    ██  ███▄ ▄███▓ ▄▄▄▄   ▓█████  ██▀███    ██████ 
 ██ ▀█   █  ██  ▓██▒▓██▒▀█▀ ██▒▓█████▄ ▓█   ▀ ▓██ ▒ ██▒▒██    ▒ 
▓██  ▀█ ██▒▓██  ▒██░▓██    ▓██░▒██▒ ▄██▒███   ▓██ ░▄█ ▒░ ▓██▄   
▓██▒  ▐▌██▒▓▓█  ░██░▒██    ▒██ ▒██░█▀  ▒▓█  ▄ ▒██▀▀█▄    ▒   ██▒
▒██░   ▓██░▒▒█████▓ ▒██▒   ░██▒░▓█  ▀█▓░▒████▒░██▓ ▒██▒▒██████▒▒
░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░░▒▓███▀▒░░ ▒░ ░░ ▒▓ ░▒▓░▒ ▒▓▒ ▒ ░
░ ░░   ░ ▒░░░▒░ ░ ░ ░  ░      ░▒░▒   ░  ░ ░  ░  ░▒ ░ ▒░░ ░▒  ░ ░
   ░   ░ ░  ░░░ ░ ░ ░      ░    ░    ░    ░     ░░   ░ ░  ░  ░  
         ░    ░            ░    ░         ░  ░   ░           ░  
                                     ░                          

    NuMb3r5 Add-on

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
'''

import sys,urllib,urlparse

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

action = params.get('action')

name = params.get('name')

title = params.get('title')

year = params.get('year')

imdb = params.get('imdb')

tvdb = params.get('tvdb')

tmdb = params.get('tmdb')

season = params.get('season')

episode = params.get('episode')

tvshowtitle = params.get('tvshowtitle')

premiered = params.get('premiered')

url = params.get('url')

image = params.get('image')

meta = params.get('meta')

select = params.get('select')

query = params.get('query')

source = params.get('source')

content = params.get('content')

docu_category = params.get('docuCat')

docu_watch = params.get('docuPlay')

windowedtrailer = params.get('windowedtrailer')
windowedtrailer = int(windowedtrailer) if windowedtrailer in ("0","1") else 0

if action is None:
    from resources.lib.indexers import navigator
    from resources.lib.modules import cache
    cache.cache_version_check()
    navigator.navigator().root()

if action == 'boxsetsNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().root()
    
elif action == 'actionNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().action()
    
elif action == 'actionliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().action(lite=True)

elif action == 'adventureNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().adventure()
    
elif action == 'adventureliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().adventure(lite=True)
    
elif action == 'animationNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().animation()
    
elif action == 'animationliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().animation(lite=True)
    
elif action == 'comedyNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().comedy()
    
elif action == 'comedyliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().comedy(lite=True)
    
elif action == 'crimeNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().crime()
    
elif action == 'crimeliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().crime(lite=True)
    
elif action == 'dramaNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().drama()
    
elif action == 'dramaliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().drama(lite=True)
    
elif action == 'familyNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().family()
    
elif action == 'familyliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().family(lite=True)
    
elif action == 'fantasyNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().fantasy()
    
elif action == 'fantasyliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().fantasy(lite=True)

elif action == 'horrorNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().horror()
    
elif action == 'horrorliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().horror(lite=True)
    
elif action == 'mysteryNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().mystery()
    
elif action == 'mysteryliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().mystery(lite=True)
    
elif action == 'romanceNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().romance()
    
elif action == 'romanceliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().romance(lite=True)
    
elif action == 'scifiNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().scifi()
    
elif action == 'scifiliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().scifi(lite=True)
    
elif action == 'thrillerNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().thriller()
    
elif action == 'thrillerliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().thriller(lite=True)
    
elif action == 'westernNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().western()
    
elif action == 'westernliteNavigator':
    from resources.lib.indexers import bxsets
    bxsets.navigator().western(lite=True)

elif action == 'boxsetKingsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().boxsetKings()

elif action == 'docuMainNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().documain()    

elif action == 'musicMainNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().musicmain()

elif action == 'musicradioMainNavigator2':
    from resources.lib.indexers import navigator
    navigator.navigator().musicradiomain()
           
elif action == 'sportsMainNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().sportsmain()                   

elif action == 'collectionsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().collections()

elif action == 'collectionActors':
    from resources.lib.indexers import navigator
    navigator.navigator().collectionActors()

elif action == 'collectionBoxset':
    from resources.lib.indexers import navigator
    navigator.navigator().collectionBoxset()

elif action == 'collectionBoxsetKids':
    from resources.lib.indexers import navigator
    navigator.navigator().collectionBoxsetKids()

elif action == 'collectionBest':
    from resources.lib.indexers import navigator
    navigator.navigator().collectionBest()

elif action == 'collectionHolidays':
    from resources.lib.indexers import navigator
    navigator.navigator().collectionHolidays()

elif action == 'collectionLifetime':
    from resources.lib.indexers import navigator
    navigator.navigator().collectionLifetime()

elif action == 'collectionTrakt':
    from resources.lib.indexers import navigator
    navigator.navigator().collectionTrakt()        

elif action == 'collections':
    from resources.lib.indexers import collections
    collections.collections().get(url)    

elif action == 'movies2':
    from resources.lib.indexers import movies2
    movies2.movies().get(url)

elif action == 'boxsetgenres':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().boxsetgenres()        

elif action == 'movieFavourites':
    from resources.lib.indexers import movies
    movies.movies().favourites()    

elif action == 'newsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().news()

elif action == 'movieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies()

elif action == 'movieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies(lite=True)

elif action == 'mymovieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies()

elif action == 'mymovieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies(lite=True)

elif action == 'docuHeaven':
    from resources.lib.indexers import docu
    if not docu_category == None:
        docu.documentary().docu_list(docu_category)
    elif not docu_watch == None:
        docu.documentary().docu_play(docu_watch)
    else:
        docu.documentary().root()    

elif action == 'tvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows()

elif action == 'tvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows(lite=True)

elif action == 'mytvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows()

elif action == 'mytvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows(lite=True)

elif action == 'kidzoneNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().kidzone()
    
elif action == 'kidsboxsetsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().kidsboxsets()
    
elif action == 'waltdisneyNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().waltdisney()
    
elif action == 'kidsmoviesNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().kidsmovies()

elif action == 'movieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies()

elif action == 'movieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies(lite=True)

elif action == 'mymovieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies()

elif action == 'mymovieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies(lite=True)

elif action == 'randomNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().random()

elif action == 'randomMoviesNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().randomflix()

elif action == 'justLegoNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().justlego()

elif action == 'gamersNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().gamers()    

elif action == 'fitnessMainNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().fitnessmain()

elif action == 'musicRandomMainNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().musicrandommain()        

elif action == 'docMainNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().docmain()            
    
elif action == 'superheroNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().superhero()

elif action == 'animemovieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().animemovies()

elif action == 'animetvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().animetvshows()

elif action == 'animeGenres':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().animegenres()

elif action == 'kidstvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().kidstvshows()

elif action == 'mytvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows()

elif action == 'mytvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows(lite=True)
    
elif action == 'teentvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().teentv()
    
elif action == 'toddlerNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().toddlertv()   
    
elif action == 'tvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows()

elif action == 'tvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows(lite=True)

elif action == 'requestsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().requests()

elif action == 'systemNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().system()

elif action == 'allsettingsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().allsettings()

elif action == 'alltoolsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().alltools()

elif action == 'jenNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().jenaddons()

elif action == 'meditativemind':
    from resources.lib.indexers import lists
    lists.indexer().root_meditativemind()    

elif action == 'technohead':
    from resources.lib.indexers import lists
    lists.indexer().root_technohead()

elif action == 'musicchoice':
    from resources.lib.indexers import lists
    lists.indexer().root_musicchoice() 

elif action == 'musicchannels':
    from resources.lib.indexers import lists
    lists.indexer().root_musicchannels()       

elif action == 'musicvideos':
    from resources.lib.indexers import lists
    lists.indexer().root_musicvideos()    

elif action == 'nowmusic':
    from resources.lib.indexers import lists
    lists.indexer().root_nowmusic()

elif action == 'worldradio':
    from resources.lib.indexers import lists
    lists.indexer().root_worldradio()

elif action == 'ukradio':
    from resources.lib.indexers import lists
    lists.indexer().root_ukradio()

elif action == 'mcaudio':
    from resources.lib.indexers import lists
    lists.indexer().root_mcaudio()                    

elif action == 'screensaver':
    from resources.lib.indexers import lists
    lists.indexer().root_screensaver()                

elif action == '247':
    from resources.lib.indexers import lists
    lists.indexer().root_247()

elif action == 'jentools':
    from resources.lib.indexers import lists
    lists.indexer().root_jentools()

elif action == 'builds':
    from resources.lib.indexers import lists
    lists.indexer().root_builds()

elif action == 'jenlist1':
    from resources.lib.indexers import lists
    lists.indexer().root_personal()                            

elif action == 'learningtv':
    from resources.lib.indexers import lists
    lists.indexer().root_learningtv()

elif action == 'knowledge':
    from resources.lib.indexers import lists
    lists.indexer().root_knowledge()

elif action == 'gamersplayground':
    from resources.lib.indexers import lists
    lists.indexer().root_gamersplayground()

elif action == 'gamerslibrary':
    from resources.lib.indexers import lists
    lists.indexer().root_gamerslibrary()        

elif action == 'justlegobrickfilms':
    from resources.lib.indexers import lists
    lists.indexer().root_justlegobrickfilms()

elif action == 'justlegofootball':
    from resources.lib.indexers import lists
    lists.indexer().root_justlegofootball()

elif action == 'justlegogamers':
    from resources.lib.indexers import lists
    lists.indexer().root_justlegogamers()

elif action == 'justlegolittletoys':
    from resources.lib.indexers import lists
    lists.indexer().root_justlegolittletoys()

elif action == 'justlegoparody':
    from resources.lib.indexers import lists
    lists.indexer().root_justlegoparody()                    

elif action == 'documentaries':
    from resources.lib.indexers import lists
    lists.indexer().root_documentaries() 

elif action == 'russell':
    from resources.lib.indexers import lists
    lists.indexer().root_russell()

elif action == 'docutube':
    from resources.lib.indexers import lists
    lists.indexer().root_docutube()    

elif action == 'athleanx':
    from resources.lib.indexers import lists
    lists.indexer().root_athleanx()    

elif action == 'eyecandy':
    from resources.lib.indexers import lists
    lists.indexer().root_eyecandy()    

elif action == 'ufc':
    from resources.lib.indexers import lists
    lists.indexer().root_ufc()

elif action == 'jens':
    from resources.lib.indexers import lists
    lists.indexer().root_jens()            

elif action == 'radio':
    from resources.lib.indexers import lists
    lists.indexer().root_radio()           

elif action == 'eimportalmovies':
    from resources.lib.indexers import lists
    lists.indexer().root_eimportalmovies()

elif action == 'eimportalshows':
    from resources.lib.indexers import lists
    lists.indexer().root_eimportalshows()

elif action == 'accountsrd':
    from resources.lib.indexers import lists
    lists.indexer().root_accountsrd()

elif action == 'speedtest':
    from resources.lib.indexers import lists
    lists.indexer().root_speedtest()

elif action == 'directory':
    from resources.lib.indexers import lists
    lists.indexer().get(url)

elif action == 'qdirectory':
    from resources.lib.indexers import lists
    lists.indexer().getq(url)

elif action == 'xdirectory':
    from resources.lib.indexers import lists
    lists.indexer().getx(url)

elif action == 'developer':
    from resources.lib.indexers import lists
    lists.indexer().developer()                

elif 'youtube' in str(action):
    from resources.lib.indexers import lists
    lists.indexer().youtube(url, action)

elif action == 'browser':
    from resources.lib.indexers import lists
    sports.resolver().browser(url)                                   

elif action == 'downloadNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().downloads()

elif action == 'libraryNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().library()

elif action == 'toolNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tools()

elif action == 'searchNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().search()

elif action == 'viewsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().views()

elif action == 'clearCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCache()

elif action == 'clearAllCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheAll()

elif action == 'clearMetaCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheMeta()

elif action == 'clearCacheSearch':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheSearch()
elif action == 'infoCheck':
    from resources.lib.indexers import navigator
    navigator.navigator().infoCheck('')

elif action == 'movies':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'moviePage':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'movieWidget':
    from resources.lib.indexers import movies
    movies.movies().widget()

elif action == 'movieSearch':
    from resources.lib.indexers import movies
    movies.movies().search()

elif action == 'movieSearchnew':
    from resources.lib.indexers import movies
    movies.movies().search_new()

elif action == 'movieSearchterm':
    from resources.lib.indexers import movies
    movies.movies().search_term(name)

elif action == 'moviePerson':
    from resources.lib.indexers import movies
    movies.movies().person()

elif action == 'movieGenres':
    from resources.lib.indexers import movies
    movies.movies().genres()

elif action == 'movieLanguages':
    from resources.lib.indexers import movies
    movies.movies().languages()

elif action == 'movieCertificates':
    from resources.lib.indexers import movies
    movies.movies().certifications()

elif action == 'movieYears':
    from resources.lib.indexers import movies
    movies.movies().years()

elif action == 'moviePersons':
    from resources.lib.indexers import movies
    movies.movies().persons(url)

elif action == 'movieUserlists':
    from resources.lib.indexers import movies
    movies.movies().userlists()

elif action == 'tvshows':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvshowPage':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvSearch':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search()

elif action == 'tvSearchnew':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search_new()

elif action == 'tvSearchterm':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search_term(name)

elif action == 'tvPerson':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().person()

elif action == 'tvGenres':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().genres()

elif action == 'tvNetworks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().networks()

elif action == 'tvNetworksKids':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().networkskids()

elif action == 'tvNetworksPremium':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().networkspremium()            

elif action == 'tvLanguages':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().languages()

elif action == 'tvCertificates':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().certifications()

elif action == 'tvPersons':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().persons(url)

elif action == 'tvUserlists':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().userlists()

elif action == 'seasons':
    from resources.lib.indexers import episodes
    episodes.seasons().get(tvshowtitle, year, imdb, tvdb)

elif action == 'episodes':
    from resources.lib.indexers import episodes
    episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, episode)

elif action == 'calendar':
    from resources.lib.indexers import episodes
    episodes.episodes().calendar(url)

elif action == 'tvWidget':
    from resources.lib.indexers import episodes
    episodes.episodes().widget()

elif action == 'calendars':
    from resources.lib.indexers import episodes
    episodes.episodes().calendars()

elif action == 'episodeUserlists':
    from resources.lib.indexers import episodes
    episodes.episodes().userlists()

elif action == 'refresh':
    from resources.lib.modules import control
    control.refresh()

elif action == 'queueItem':
    from resources.lib.modules import control
    control.queueItem()

elif action == 'openSettings':
    from resources.lib.modules import control
    control.openSettings(query)

elif action == 'artwork':
    from resources.lib.modules import control
    control.artwork()

elif action == 'addView':
    from resources.lib.modules import views
    views.addView(content)

elif action == 'moviePlaycount':
    from resources.lib.modules import playcount
    playcount.movies(imdb, query)

elif action == 'episodePlaycount':
    from resources.lib.modules import playcount
    playcount.episodes(imdb, tvdb, season, episode, query)

elif action == 'tvPlaycount':
    from resources.lib.modules import playcount
    playcount.tvshows(name, imdb, tvdb, season, query)

elif action == 'trailer':
    from resources.lib.modules import trailer
    trailer.trailer().play(name, url, windowedtrailer)

elif action == 'traktManager':
    from resources.lib.modules import trakt
    trakt.manager(name, imdb, tvdb, content)

elif action == 'authTrakt':
    from resources.lib.modules import trakt
    trakt.authTrakt()

elif action == 'urlResolver':
    try:
        import resolveurl
    except Exception:
        pass
    resolveurl.display_settings()

elif action == 'ResolveUrlTorrent':
    from resources.lib.modules import control
    control.openSettings(query, "script.module.resolveurl")    

elif action == 'download':
    import json
    from resources.lib.modules import sources
    from resources.lib.modules import downloader
    try: downloader.download(name, image, sources.sources().sourcesResolve(json.loads(source)[0], True))
    except: pass

elif action == 'docuHeaven':
    from resources.lib.indexers import docu
    if not docu_category == None:
        docu.documentary().docu_list(docu_category)
    elif not docu_watch == None:
        docu.documentary().docu_play(docu_watch)
    else:
        docu.documentary().root()    

elif action == 'play':
    from resources.lib.indexers import lists
    if not content == None:
        lists.player().play(url, content)
    else:
        from resources.lib.modules import sources
        sources.sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)

elif action == 'play1':
    from resources.lib.indexers import lists
    if not content == None:
        lists.player().play(url, content)
    else:
        from resources.lib.modules import sources
        sources.sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)

elif action == 'addItem':
    from resources.lib.modules import sources
    sources.sources().addItem(title)

elif action == 'playItem':
    from resources.lib.modules import sources
    sources.sources().playItem(title, source)

elif action == 'alterSources':
    from resources.lib.modules import sources
    sources.sources().alterSources(url, meta)

elif action == 'clearSources':
    from resources.lib.modules import sources
    sources.sources().clearSources()

elif action == 'random':
    rtype = params.get('rtype')
    if rtype == 'movie':
        from resources.lib.indexers import movies
        rlist = movies.movies().get(url, create_directory=False)
        r = sys.argv[0]+"?action=play"
    elif rtype == 'episode':
        from resources.lib.indexers import episodes
        rlist = episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, create_directory=False)
        r = sys.argv[0]+"?action=play"
    elif rtype == 'season':
        from resources.lib.indexers import episodes
        rlist = episodes.seasons().get(tvshowtitle, year, imdb, tvdb, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=episode"
    elif rtype == 'show':
        from resources.lib.indexers import tvshows
        rlist = tvshows.tvshows().get(url, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=season"
    from resources.lib.modules import control
    from random import randint
    import json
    try:
        rand = randint(1,len(rlist))-1
        for p in ['title','year','imdb','tvdb','season','episode','tvshowtitle','premiered','select']:
            if rtype == "show" and p == "tvshowtitle":
                try: r += '&'+p+'='+urllib.quote_plus(rlist[rand]['title'])
                except: pass
            else:
                try: r += '&'+p+'='+urllib.quote_plus(rlist[rand][p])
                except: pass
        try: r += '&meta='+urllib.quote_plus(json.dumps(rlist[rand]))
        except: r += '&meta='+urllib.quote_plus("{}")
        if rtype == "movie":
            try: control.infoDialog(rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except: pass
        elif rtype == "episode":
            try: control.infoDialog(rlist[rand]['tvshowtitle']+" - Season "+rlist[rand]['season']+" - "+rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except: pass
        control.execute('RunPlugin(%s)' % r)
    except:
        control.infoDialog(control.lang(32537).encode('utf-8'), time=8000)

elif action == 'movieToLibrary':
    from resources.lib.modules import libtools
    libtools.libmovies().add(name, title, year, imdb, tmdb)

elif action == 'moviesToLibrary':
    from resources.lib.modules import libtools
    libtools.libmovies().range(url)

elif action == 'tvshowToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().add(tvshowtitle, year, imdb, tvdb)

elif action == 'tvshowsToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().range(url)

elif action == 'updateLibrary':
    from resources.lib.modules import libtools
    libtools.libepisodes().update(query)

elif action == 'service':
    from resources.lib.modules import libtools
    libtools.libepisodes().service()

elif action == 'ShowChangelog':
    from resources.lib.modules import changelog
    changelog.get()    
