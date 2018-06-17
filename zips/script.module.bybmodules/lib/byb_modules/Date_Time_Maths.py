import datetime
import math

def convert_seconds(x):
    # Day's
    days = x / 86400
    fraction, whole = math.modf(days)
    days = int(whole)
    # Hours
    hours = fraction * 24
    fraction, whole = math.modf(hours)
    hours = int(whole)
    # Minutes
    minutes = fraction * 60
    fraction, whole = math.modf(minutes)
    minutes = int(whole)
    # Seconds
    seconds = fraction * 60
    fraction, whole = math.modf(seconds)
    seconds = int(whole)
    return days, hours, minutes, seconds

def within_time_frame(t1,t2,frame,t2_frame):
	'''
		# frame can be a dict containing all or some of  {'day':'0','hour':'0','minute':'5'} or a int value of seconds
		# t2_frame is the area of frame in relation to t2 so options are 'before', 'after' or 'both'
		# example within_time_frame(t1 = datetime.datetime.now(),t2 = datetime.datetime.fromtimestamp(os.path.getmtime(File)),frame = {'minute':'5'},t2_frame = 'after')
	'''
	if type(frame) == dict:
		day = frame.get('day',0)
		hour = frame.get('hour',0)
		minute = frame.get('minute',0)
		Seconds = (int(day)*86400)+(int(hour)*3600)+(int(minute)*60)
	else:
		frame = seconds
	if t2_frame == 'both':
		t2_lower = t2 + datetime.timedelta(seconds=-Seconds)
		t2_upper = t2 + datetime.timedelta(seconds=Seconds)
	if t2_frame == 'after':
		t2_lower = t2
		t2_upper = t2 + datetime.timedelta(seconds=Seconds)
	if t2_frame =='before':
		t2_lower = t2 + datetime.timedelta(seconds=-Seconds)
		t2_upper = t2
	if t1 >= t2_lower and t2_upper >= t1:
		return True    
	else:
		return False



