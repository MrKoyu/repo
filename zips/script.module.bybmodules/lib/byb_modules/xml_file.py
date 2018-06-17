import koding 
import xbmc_executebuiltin


def xml_item_count(source, block, tag_to_count):
	''' source == route to file can either be a url or special path
	block == master tag 
	tag_to_count == tag you wish to count
	returns a int value of count
	'''
	count = 0 
	if source.startswith('http'):
		source = koding.Open_URL(url=source,cookiejar=source)
	elif source.startswith('special'):
		source = koding.Physical_Path(source)
		source = koding.Text_File(source,'r')
	else:
		message = 'xml %s source not correct unable to count'%source
		koding.dolog(message,line_info=True)
		xbmc_executebuiltin.Notify(message=message)
	source_details = koding.Parse_XML(source, block, tag_to_count)
	for items in source_details:
		count += 1
	return count
