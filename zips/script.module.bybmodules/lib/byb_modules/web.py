import re 



def cookie_name_create(url):
	cookie_name =  (url.split('//',1)[1]).split('/',1)[0]
	match = re.compile('[^a-z]').findall(str(cookie_name))
	for items in match:
		cookie_name = cookie_name.replace(str(items),'_')
	return cookie_name
    
