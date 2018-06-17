
import byb_modules as BYB 
import koding
import xbmc




class Loggin():

	def __init__(self):
		self.LogInCount = []
		self.file=paths.CACHE_DB
		self.table='login'
		self.icon = paths.icon

	def Log_in(self):
		if settings.LOGIN_PREF == 'Never':
			return True
		elif settings.LOGIN_PREF == 'Once':
			BYB.table_names_DB(self.file)
			if len(BYB.TableNames) > 0:
				for tables in BYB.TableNames:
					if self.table == tables:
						checkdb = 1
					else:
						checkdb = 0
			else:
				checkdb = 0
			if checkdb == 0:
				self.once_login()
				BYB.readall_DB(self.file,self.table)
			elif checkdb == 1:
				BYB.readall_DB(self.file,self.table)
			for results in BYB.DB_list:
				User = results[0]
				PassWord = results[1]
				if User == settings.USERNAME and PassWord == settings.PASSWORD:
					koding.Notify(title='Loggin', message='Loggin successful', icon=self.icon)
					return True
				else:
					koding.Notify(title='Loggin',message='Cached User and Password do not match ',icon=self.icon)
					return False
		elif settings.LOGIN_PREF == 'Always':
			User,PassWord = self.enter_login()
			if User == settings.USERNAME and PassWord == settings.PASSWORD:
			    koding.Notify(title='Loggin', message='Loggin successful', icon=self.icon)
			    return True
			else:
			    koding.Notify(title='Loggin', message='Log In Fail', icon=self.icon)
			    yes_no = koding.YesNo_Dialog(title='Log In',message='Loggin failed would you like to try again')
			    if yes_no:
			        self.LogInCount.append(1)
			        LogginCount = sum(self.LogInCount)
			        koding.dolog('Loggin count = %s'%LogginCount,line_info=True)
			        if  LogginCount >= 3:
			            koding.Notify(title='Loggin',message='Attempted to Loggin 3 times unseccesfully no adult content will be shown',icon=self.icon)
			            return False
			        else:
			            self.Log_in()
			    else:
			        return False
		else:
			return False


	def once_login(self):
		#if settings.LOGIN_PREF != 'Never' and != 'Always':
		User,PassWord = self.enter_login()
		BYB.headers_create(self.file,self.table,headers='user,password')
		BYB.write_to_DB(self.file,self.table,headers='?, ?',items=(User,PassWord))
    		


   	def enter_login(self):
		kb = xbmc.Keyboard('default', 'heading', True)
		kb.setDefault('') # optional
		kb.setHeading('Enter UserName') # optional
		kb.setHiddenInput(True) # optional
		kb.doModal()
		if (kb.isConfirmed()):
		    User = kb.getText()
		kb.setHeading('Enter Password')
		kb.setHiddenInput(True)
		kb.doModal()
		if (kb.isConfirmed()):
		    PassWord = kb.getText()
		koding.dolog('UserName %s Password = %s'%(User,PassWord),line_info=True)
		return User,PassWord


'''	def Log_In():
		if settings.LOGIN_PREF == 'Always':
		    kb = xbmc.Keyboard('default', 'heading', True)
		    kb.setDefault('') # optional
		    kb.setHeading('Enter UserName') # optional
		    kb.setHiddenInput(True) # optional
		    kb.doModal()
		    if (kb.isConfirmed()):
		        User = kb.getText()
		    kb.setHeading('Enter Password')
		    kb.setHiddenInput(True)
		    kb.doModal()
		    if (kb.isConfirmed()):
		        PassWord = kb.getText()
		    koding.dolog('UserName %s Password = %s'%(User,PassWord),line_info=True)
		    if User == settings.USERNAME and PassWord == settings.PASSWORD:
		        koding.Notify(title='Loggin', message='Loggin successful', icon=icon)
		        return True
		    else:
		        koding.Notify(title='Loggin', message='Log In Fail', icon=icon)
		        yes_no = koding.YesNo_Dialog(title='Log In',message='Loggin failed would you like to try again')
		        if yes_no:
		            LogInCount.append(1)
		            LogginCount = sum(LogInCount)
		            koding.dolog('Loggin count = %s'%LogginCount,line_info=True)
		            if  LogginCount > 3:
		                koding.Notify(title='Loggin',message='Attempted to Loggin 3 times unseccesfully no adult content will be shown',icon=icon)
		                return False
		            else:
		                Log_In()
		        else:
		            return False '''