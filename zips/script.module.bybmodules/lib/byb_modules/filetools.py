import os 
import Date_Time_Maths
import datetime

def file_check(filename,create):
	''' 
		filename = path to file
		create =  create file in not exists yes or 1/no or 0
		Return 1 if file exists, 2 if not exists and created, 3 not exists or created
	''' 
	if os.path.exists(filename):
		return 1
	if not os.path.exists(filename):
		if create == 'yes' or 1:
			file=open(filename,'a')
			file.close()
			return  2
		else:
			return 3

def file_mod_datetime(File):
	'''returns a datetime of when file was last modified
		file = path of file 
	''' 
	if os.path.exists(File):
		mod_date = os.path.getmtime(File)
		mod_date = datetime.datetime.fromtimestamp(mod_date)
	else:
		mod_date = None
	return mod_date


def file_rewrite_timepass(file,t1,frame,t2_frame):
	''' returns true or false if file last modified date is within time frame 
		file = path to file
		# frame can be a dict containing all or some of  {'day':'0','hour':'0','minute':'5'} or a int value of seconds
		# t2_frame is the area of frame in relation to t2 so options are 'before', 'after' or 'both'
		# example within_time_frame(t1 = datetime.datetime.now(),t2 = datetime.datetime.fromtimestamp(os.path.getmtime(File)),frame = {'minute':'5'},t2_frame = 'after')
	'''
	t2 = file_mod_datetime(file)
	if not t2 == None:
		timepass = Date_Time_Maths.within_time_frame(t1,t2,frame,t2_frame)
		if timepass == True:
			return True
		if timepass == False:
			return False
	else:
		return False