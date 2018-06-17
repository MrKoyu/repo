import requests
import urlparse
import re
import resolveurl as urlresolver
import xbmc,xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

#for older movies/ comedies youtube (green street, g.i. joe retaliation)
class moviesfoundonline(Scraper):
    domains = ['http://moviesfoundonline.com']
    name = "MoviesFoundOnline"
    sources = []

    def __init__(self):
        self.base_link = 'http://moviesfoundonline.com'


    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                      
                                                                                        

            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))         
            #print 'moviesfoundonline - scrape_movie - start_url:  ' + start_url                                  
            
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content            
            
            match = re.compile('class="img-hover".+?href="(.+?)">(.+?)</a>',re.DOTALL).findall(html) 
            for item_url, name in match:
                #print 'moviesfoundonline - scrape_movie - name: '+name
                #print 'moviesfoundonline - scrape_movie - item_url: '+item_url                                
                #print 'moviesfoundonline - scrape_movie - year: '+year
                if year in name:
                    #print '>>>>>>>>>>>>>>>>>>>>>>>>year'+year                                                       
                    
                    if clean_title(search_id).lower() == clean_title(name).lower():     
                                                                                        
                        #print 'moviesfoundonline - scrape_movie - Send this URL: ' + item_url                             
                        self.get_source(item_url,title,year,start_time)                                      
            return self.sources
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return[]

            
    def get_source(self,item_url,title,year,start_time):
        try:
            count = 0
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(item_url,headers=headers,timeout=5).content             
            #print 'moviesfoundonline - scrape_movie - OPEN: '+OPEN
            Endlinks = re.compile('<iframe width=.+?src="(.+?)"',re.DOTALL).findall(OPEN)
            #print 'moviesfoundonline - scrape_movie - EndLinks: '+str(Endlinks)
            for link in Endlinks:
                #print 'moviesfoundonline - scrape_movie - link: '+str(link)
                if 'youtube' in link:
                    headers= {'User-Agent':User_Agent}
                    get_res= request.get(link,headers=headers,timeout=5).content
                    rez= re.compile('',re.DOTALL).findall(get_res)[0]
                    if '1080' in rez:
                        qual = '1080p'
                    elif '720' in rez:
                        qual = '720p'
                    else:
                        qual = 'DVD'
                    count+=1
                    self.sources.append({'source':'Youtube', 'quality':qual, 'scraper':self.name, 'url':link, 'direct':True})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return[]
