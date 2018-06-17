# -*- coding: UTF-8 -*-

"""
 weblogin
 by Anarchintosh @ xbmcforums
 Copyleft (GNU GPL v3) 2011 onwards

 this example is configured for Fantasti.cc login
 See for the full guide please visit:
 http://forum.xbmc.org/showthread.php?p=772597#post772597


 USAGE:
 in your default.py put:

 import weblogin
 logged_in = weblogin.doLogin('a-path-to-save-the-cookie-to','the-username','the-password')

 logged_in will then be either True or False depending on whether the login was successful.
"""

import os
import re
import urllib,urllib2
import cookielib
import koding
import web
### TESTING SETTINGS (will only be used when running this file independent of your addon)
# Remember to clear these after you are finished testing,
# so that your sensitive details are not in your source code.
# These are only used in the:  if __name__ == "__main__"   thing at the bottom of this script.
myusername = 'david'
mypassword = 'L7bp55##123'
#note, the cookie will be saved to the same directory as weblogin.py when testing


def check_login(source,username):
    
    #the string you will use to check if the login is successful.
    #you may want to set it to:    username     (no quotes)
    logged_in_string = 'Welcome to '

    #search for the string in the html, without caring about upper or lower case
    if re.search(logged_in_string,source,re.IGNORECASE):
        return True
    else:
        return False


def doLogin(login_url):

    ''' to call login,source_data = weblogin.dologin(login_url)  

    login_url = site to login into e.g login_url = 'http://p.xxe.press/login.php'
    '''

    source_data = ''
    Addon_Name    = koding.Addon_Info(id='name')
    Addon_Version = koding.Addon_Info(id='version')
    Addon_Profile = koding.Addon_Info(id='profile')
    Cookie_Folder = os.path.join(Addon_Profile,'cookies')
    cookie_name = web.cookie_name_create(login_url)
    cookiepath = os.path.join(Cookie_Folder,str(cookie_name)+'.lwp')
    cookiepath =  koding.Physical_Path(cookiepath)
    username = koding.Addon_Setting('username')
    password = koding.Addon_Setting('password')

    #delete any old version of the cookie file
    try:
        os.remove(cookiepath)
    except:
        pass
    koding.dolog('UserName = %s %s Password = %s %s'%(username,len(username),password,len(password)),line_info=True)
    koding.dolog('cookiepath = %s'%cookiepath,line_info=True)
    if len(username) == 0  or len(password) == 0:
        yesno = koding.YesNo_Dialog(title=str(Addon_Name)+' Login for'+str(login_url),message='There is no UserName or Password set, would you like to set it now?')
        if yesno == True:
            koding.Open_Settings()
        else:
            return False
    if username and password:
        #the header used to pretend you are a browser
        header_string = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
	#build the form data necessary for the login
        login_data = urllib.urlencode({'username':username, 'password':password})
        #build the request we will make
        req = urllib2.Request(login_url, login_data)
        req.add_header('User-Agent',header_string)
        #initiate the cookielib class
        cj = cookielib.LWPCookieJar()
        #install cookielib into the url opener, so that cookies are handled
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        #do the login and get the response
        response = opener.open(req)
        source = response.read()
        source_data += str(source)
        response.close()
        #check the received html for a string that will tell us if the user is logged in
        #pass the username, which can be used to do this.
        login = check_login(source,username)
        #if login suceeded, save the cookiejar to disk
        if login == True:
            cj.save(cookiepath)
        #return whether we are logged in or not
        return login,source_data
    else:
        return False

#code to enable running the .py independent of addon for testing
if __name__ == "__main__":
    if myusername is '' or mypassword is '':
        print 'YOU HAVE NOT SET THE USERNAME OR PASSWORD!'
    else:
        logged_in = doLogin(os.getcwd(),myusername,mypassword)
        print 'LOGGED IN:',logged_in
