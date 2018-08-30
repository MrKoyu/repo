import urllib2
import re
from  BeautifulSoup import BeautifulSoup,BeautifulSOAP,BeautifulStoneSoup


base_url = 'http://retrovision.tv/tags/'
url = '{}adventure/'.format(base_url)
pages = ['1']
ReturnList = []

def getUrl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


def all_movies():
	TotalPage = page_counter(url)
	for i in range(int(TotalPage)):
		Url = '{}page/{}/'.format(url,i+1)
		html = getUrl(Url)
		match= re.compile('<article(.+?)</article>',re.DOTALL).findall(html)
		for block in match:
			match2 = re.compile('<a href="(.+?)".+?title="(.+?)">.+?src="(.+?)"',re.DOTALL).findall(str(block))
			for pageurl,title,icon in match2: 
				html2 = getUrl(pageurl)
				match3 = re.compile('<div class="entry-content">(.+?)<a href="(.*mp4)">',re.DOTALL).findall(html2)
				for rawdescription,playlink in match3:
					Rdescription = unicode(BeautifulStoneSoup(rawdescription, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))
					RDescription=BeautifulSoup(Rdescription)
					description=RDescription.text
					ReturnList.append({'title':title.encode('utf-8'),'playlink':playlink,'icon':icon,'description':description})

					




def page_counter(url):
	html=getUrl(url)
	match=re.compile('<a class="next page-numbers" href="(.+?)">',re.DOTALL).findall(html)
	if len(match)>0:
		for page in match:
			Page = page.rstrip('/').split('/')[-1]
			if Page not in pages:
				pages.append(Page)
				page_counter(page)
	else:
		pass
	totalpage = max(pages)
	return totalpage





if __name__ == '__main__':
	all_movies()
	

