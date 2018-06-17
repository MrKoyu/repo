# -*- coding: utf-8 -*-
'''
    Copyright (C) 2018 BigYidBuilds

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

import koding
import re
import requests
import byb_modules as BYB 

Details_list = []
Get = requests.get
Dolog = koding.dolog

artwork_url = 'https://image.tmdb.org/t/p/original'


def tmdb_movies_get_details(ID,tmdb_apikey):
    genre_list =[]
    url = "https://api.themoviedb.org/3/movie/%s?api_key=%s" %(ID,tmdb_apikey)
    artwork_url = 'https://image.tmdb.org/t/p/original%s'
    r = requests.get(url)
    config = r.json()
    poster_path = artwork_url %(config['poster_path'])
    backdrop_path = artwork_url %(config['backdrop_path'])
    title = config['original_title']
    overview = config['overview']
    ID = config['id'] 
    imdb_id = config['imdb_id']
    release_date = config['release_date']
    genres = config["genres"]
    for genre in genres:
        Genre = genre.get('name')
        genre_list.append(Genre)
    Details_list.append({'title':title ,'ID':str(ID),'overview':overview,'poster_path':poster_path,'backdrop_path':backdrop_path,'imdb_id':imdb_id,'release_date':release_date,'Genres':genre_list})
    

def tmdb_movies_get_images(ID,tmdb_apikey):
    url = 'https://api.themoviedb.org/3/movie/%s/images?api_key=%s' %(ID,tmdb_apikey)
    r = requests.get(url)
    config = r.json()
    print config

def tmdb_tv_show_get_details(ID,tmdb_apikey):
    genre_list = []
    url = 'https://api.themoviedb.org/3/tv/%s?api_key=%s' %(ID,tmdb_apikey)
    artwork_url = 'https://image.tmdb.org/t/p/original%s'
    r = requests.get(url)
    config = r.json()
    poster_path = artwork_url %(config['poster_path'])
    backdrop_path = artwork_url %(config['backdrop_path'])
    title = config['original_name']
    overview = config['overview']
    ID = config['id']
    genres = config["genres"]
    for genre in genres:
        Genre = genre.get('name')
        genre_list.append(Genre)
    Details_list.append({'ID':ID,'title':title,'overview':overview,'poster_path':poster_path,'backdrop_path':backdrop_path,'Genres':genre_list})

def tmdb_tv_show_get_episode_details(ID,tmdb_apikey,season,episode):
    url = 'https://api.themoviedb.org/3/tv/'+str(ID)+'/season/'+str(season)+'/episode/'+str(episode)+'?api_key='+str(tmdb_apikey)
    artwork_url = 'https://image.tmdb.org/t/p/original'
    r = requests.get(url)
    episodes = r.json()
    default = ''
    still_path = episodes.get('still_path',default)
    still_path = artwork_url+str(still_path)
    name = episodes.get('name',default)
    air_date = episodes.get('air_date',default)
    overview = episodes.get('overview',default)
    episode_number = episodes.get("episode_number",default)
    season_number = episodes.get("season_number",default)
    Details_list.append({'poster_path':still_path,'title':name,'release_date':air_date,'overview':overview,'episode_number':episode_number,'season_number':season_number})


def tmdb_tv_show_get_season_details(ID,tmdb_apikey,season):
    url = 'https://api.themoviedb.org/3/tv/'+str(ID)+'/season/'+str(season)+'?api_key='+str(tmdb_apikey)
    artwork_url = 'https://image.tmdb.org/t/p/original'
    r = requests.get(url)
    episodes = r.json()
    default = ''
    poster_path = artwork_url+str(episodes.get('poster_path',default))
    name = episodes.get('name',default)
    air_date = episodes.get('air_date',default)
    overview = episodes.get('overview',default)
    season_number = episodes.get("season_number",default)
    Details_list.append({'poster_path':poster_path,'title':name,'release_date':air_date,'overview':overview,'season_number':season_number})


def tmdb_tv_show_get_seasons(ID,tmdb_apikey):
    url = 'https://api.themoviedb.org/3/tv/%s?api_key=%s' %(ID,tmdb_apikey)
    artwork_url = 'https://image.tmdb.org/t/p/original%s'
    r = requests.get(url)
    config = r.json()
    seasons = config['seasons']
    for season in seasons:
        default = ''
        season_number =  season.get('season_number',default)
        poster_path = season.get('poster_path',default)
        poster_path = artwork_url %(poster_path)
        season_id = season.get('id',default)
        if season_number >= 1:
            Details_list.append({'ID':ID,'season_number':season_number,'poster_path':poster_path})

def tmdb_tv_show_get_season_episodes(ID,season_number,tmdb_apikey):
    url = 'https://api.themoviedb.org/3/tv/%s/season/%s?api_key=%s' %(ID,season_number,tmdb_apikey)
    artwork_url = 'https://image.tmdb.org/t/p/original%s'
    default = ''
    r = requests.get(url)
    config = r.json()
    #print config
    episodes = config.get('episodes',default)
    for episode in episodes:
        still_path = episode.get('still_path',default)
        name = episode.get('name',default)
        air_date = episode.get('air_date',default)
        overview = episode.get('overview',default)
        episode_number = episode.get("episode_number",default)
        season_number = episode.get("season_number",default)
        Details_list.append({'still_path':still_path,'name':name,'air_date':air_date,'overview':overview,'episode_number':episode_number,'season_number':season_number})

def tmdb_tv_show_get_season_episodes_external_ID(ID,season_number,episode_number):
    url = 'https://api.themoviedb.org/3/tv/%s/season/%s/episode/%s/external_ids' %(ID,season_number,episode_number)
    default = ''
    r = requests.get(url)
    config = r.json()
    imdb_id = config.get("imdb_id",default)
    freebase_mid = config.get('freebase_mid',default)
    freebase_id  = config.get('freebase_id',default)
    tvdb_id = config.get('tvdb_id',default)
    tvrage_id = config.get('tvrage_id',default)


def tmdb_check_key(tmdb_apikey):
    Token,StatusMessage,Success = tmdb_request_token(tmdb_apikey)
    if Success == True:
        koding.dolog('api key success')
    else:
        koding.dolog('api key check failed due to '+str(StatusMessage),line_info=True)


def tmdb_request_token(tmdb_apikey):
    url = 'https://api.themoviedb.org/3/authentication/token/new?api_key='+str(tmdb_apikey)
    r = requests.get(url)
    TokenRequest = r.json()
    Token = TokenRequest.get("request_token",'TokenMissing')
    StatusMessage = TokenRequest.get("status_message","NoErrorMessage")
    Success = TokenRequest.get('success','False')
    return Token,StatusMessage,Success


def tmdb_login(tmdb_apikey,tmdb_user,tmdb_password):
    Token,StatusMessage,Success = tmdb_request_token(tmdb_apikey)
    url ='https://api.themoviedb.org/3/authentication/token/validate_with_login?api_key='+str(tmdb_apikey)+'&username='+str(tmdb_user)+'&password='+str(tmdb_password)+'&request_token='+str(Token)
    if Success == True:
        r = requests.get(url)
        login = r.json()
        StatusMessageLogin = login.get("status_message","NoErrorMessage")
        SuccessLogin = login.get('success','False')
        if SuccessLogin == True:
            LogIn = True
        else:
            LogIn = False
        return LogIn,StatusMessageLogin
    else:
        LogIn = False
        return LogIn,StatusMessage


def tmdb_session(tmdb_apikey):
    Token,StatusMessage,Success = tmdb_request_token(tmdb_apikey)
    url = 'https://www.themoviedb.org/authenticate/'+str(Token)
    if Success == True:
        BYB.WebBrowse(url)
        auth = koding.YesNo_Dialog(title='TMDB Authentication',message='Has TMDB Authentication been granted?')
        if auth:
            Url = 'https://api.themoviedb.org/3/authentication/session/new?api_key='+str(tmdb_apikey)+'&request_token='+str(Token)
            r = requests.get(Url)
            session = r.json()
            Success = session.get('success','False')
            SessionId = session.get('session_id','')
            StatusMessage = session.get("status_message","NoErrorMessage")
            if Success == True and StatusMessage == 'NoErrorMessage':
                Auth = True
            else:
                Auth = False

        else:
            Auth = False
    else:
        Auth = False
    if Auth == False:
        koding.dolog('tmdb_session failed resason '+str(StatusMessage),line_info=True)
    return Auth,SessionId,StatusMessage



def tmdb_account_details(tmdb_apikey,session_id):
    url = 'https://api.themoviedb.org/3/account?api_key='+str(tmdb_apikey)+'&session_id='+str(session_id)
    r = requests.get(url)
    details = r.json()
    account_id = details.get('id','')
    return account_id


def tmdb_mylists(tmdb_apikey,session_id):
    account_id = tmdb_account_details(tmdb_apikey,session_id)
    url = 'https://api.themoviedb.org/3/account/'+str(account_id)+'/lists?api_key='+str(tmdb_apikey)+'&session_id='+str(session_id)
    r = requests.get(url)
    lists = r.json()


def tmdb_my_lists(tmdb_apikey,session_id,content_type,list_type):
    #content_type = movies or tv
    #list_type = favorite, rated or watchlist
    genre_list = []
    account_id = tmdb_account_details(tmdb_apikey,session_id)
    url =' https://api.themoviedb.org/3/account/'+str(account_id)+'/'+str(list_type)+'/'+str(content_type)+'?api_key='+str(tmdb_apikey)+'&session_id='+str(session_id)
    artwork_url = 'https://image.tmdb.org/t/p/original'
    Dolog(url,line_info=True)
    r = Get(url)
    data = r.json()
    Dolog(data,line_info=True)
    movies = data.get('results','')
    for movie in movies:
        poster_path = artwork_url+str(movie.get('poster_path',''))
        backdrop_path = artwork_url+str(movie.get('backdrop_path',''))
        title = movie.get('name','')
        if title == '':
            title = movie.get('original_title','Title Missing')
        overview = movie.get('overview','Description Missing')
        ID = movie.get('id','') 
        imdb_id = movie.get('imdb_id','')
        release_date = movie.get('release_date','Release Date Missing')
        Details_list.append({'title':title ,'ID':str(ID),'overview':overview,'poster_path':poster_path,'backdrop_path':backdrop_path,'imdb_id':imdb_id,'release_date':release_date,'Genres':genre_list})


def tmdb_search(tmdb_apikey,search_type,search_term,total_pages='all'):
    '''Search type's are 'company', 'collection', 'keyword', 'movie', 'multi', 'person' and 'tv'
    movie and tv show return complete others require work to complete
    by puttin a value in total pages it will only return that amount of pages in the list 
     '''
    genre_list = []
    search_term = search_term.replace(' ','%20')
    if total_pages == 'all':
        url = 'https://api.themoviedb.org/3/search/'+str(search_type)+'?api_key='+str(tmdb_apikey)+'&query='+str(search_term)
    else:
        url = 'https://api.themoviedb.org/3/search/'+str(search_type)+'?api_key='+str(tmdb_apikey)+'&query='+str(search_term)+'&page='+str(total_pages)
    Dolog(url,line_info=True)
    r = Get(url)
    search_data = r.json()
    if search_type == 'movie' or search_type == 'tv':
        data_results = search_data.get('results','')
        for result in data_results:
            poster_path = artwork_url+str(result.get('poster_path',''))
            backdrop_path = artwork_url+str(result.get('backdrop_path',''))
            title = result.get('original_title','')
            if title=='':
                title = result.get('name','')
            if title=='':
                title = result.get('original_name','Title Missing')
            overview = result.get('overview','Description Missing')
            ID = result.get('id','') 
            imdb_id = result.get('imdb_id','')
            release_date = result.get('release_date','Release Date Missing')
            try:
                genres = result.get("genres","")
                for genre in genres:
                    Genre = genre.get('name')
                    genre_list.append(Genre)
            except:pass 
            Details_list.append({'title':title ,'ID':str(ID),'overview':overview,'poster_path':poster_path,'backdrop_path':backdrop_path,'imdb_id':imdb_id,'release_date':release_date,'Genres':genre_list})










    
