# -*- coding: utf-8 -*-
import koding



Dolog = koding.dolog 

def String_Color(string,color,Split=None,Spoint=None):
	'''
	string is string to change 
	color should be sent through as a list of colors max 2  
	split is either 'space' or 'word' if you wish to have 2 color string 
	Spoint is how many letters of the word if you wish the word or 2 colours 
	'''
	SpointA = Spoint
	SpointB = Spoint
	ColorString = ''
	if not '[COLOR' in string:
		if Split == None and Spoint == None:
			ColorString += '[COLOR '+str(color[0])+']'+str(string)+'[/COLOR]'
		elif Split == 'space' and Spoint == None:
			if ' ' in string:
				splitstring = string.split(' ',1)
				ColorString = '[COLOR '+str(color[0])+']'+str(splitstring[0])+' [/COLOR][COLOR '+str(color[1])+']'+str(splitstring[1])+'[/COLOR]'
			else:
				ColorString = '[COLOR '+str(color[0])+']'+str(string)+'[/COLOR]'
		elif Split == 'word' and NumberIsInt(Spoint):
			if ' ' in string:
				splitstring = string.split(' ',1)
				if Spoint >= len(splitstring[0]):
					SpointA = len(splitstring[0])-1
				if Spoint >= len(splitstring[1]):
					SpointB = len(splitstring[1])-1
				Asplitpos = splitstring[0][SpointA]
				Bsplitpos = splitstring[1][SpointB]
				try:
					Astringsplit = splitstring[0].split(Asplitpos,1)
					ColorString += '[COLOR '+str(color[0])+']'+str(Astringsplit[0])+'[/COLOR]'
					ColorString += '[COLOR '+str(color[1])+']'+str(Asplitpos)+str(Astringsplit[1])+'[/COLOR]'
				except:
					try:
						ColorString += '[COLOR '+str(color[0])+']'+str(splitstring[0])+'[/COLOR] '
					except:
						ColorString += splitstring[0]+' '
				try:
					Bstringsplit = splitstring[1].split(Bsplitpos,1)
					ColorString += ' [COLOR '+str(color[0])+']'+str(Bstringsplit[0])+'[/COLOR]'
					ColorString += '[COLOR '+str(color[1])+']'+str(Bsplitpos)+str(Bstringsplit[1])+'[/COLOR]'
				except:
					try:
						ColorString += '[COLOR '+str(color[0])+']'+str(splitstring[1])+'[/COLOR] '
					except:
						ColorString += splitstring[1]
			else:
				if Spoint >= len(string):
					Spoint = len(string)-1
					print Spoint
				try:
					splitpos = string[Spoint]
					print splitpos
				except:pass
				try:
					Astringsplit = string.split(splitpos,1)
					ColorString += '[COLOR '+str(color[0])+']'+str(Astringsplit[0])+'[/COLOR] [COLOR '+str(color[1])+']'+str(splitpos)+str(Astringsplit[1])+'[/COLOR]'
				except:
					try:
						ColorString += '[COLOR {}]{}[/COLOR]'.format(color[0],string)
					except:
						ColorString = string
		else:
			ColorString = string
	else:
		ColorString = string
	return ColorString

def NumberIsInt(x):
	try:
		x = int(x)
		return True
	except ValueError:
		Dolog(str(x)+'ValueError',line_info=True) 
		return False
	except TypeError:
		Dolog(str(x)+'TypeError',line_info=True) 
		return False




if __name__ == '__main__':
	STRING = String_Color(string='lady bird',color=['blue','white'],Split='word',Spoint=2)
	TF = NumberIsInt(None)
	print STRING
	#print TF