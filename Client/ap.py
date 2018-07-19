import os 

def getInterface():
	list_interface = []
	print ''
	print 'Checking Interfaces:'
	print '========================================================='
	list_result = os.popen('iwconfig').read().split('\n')
	for str_result in list_result:
		interface = str_result.split(' ')[0]
		if str_result.find('no wireless') < 0 and interface:
			print str_result	
			list_interface.append(interface)
	print '========================================================='
	print ''
	return list_interface

def searchESSID(list_interface):
	list_essid = []
	for str_interface in list_interface:
		try:
			list_result = os.popen('iwlist ' + str_interface + ' scanning').read()
			list_result = list_result.split('\n')
			for str_result in list_result:
				if str_result.find('ESSID:') > 0:
					list_essid.append(str_result.split('ESSID:')[1][1:-1])
		except Exception:
			pass
	return list_essid

def printESSID(list_essid):
	print 'Conntectable AP List:'
	print '========================================================='
        for essid in list_essid:
                print essid
	print '========================================================='
list_essid = searchESSID(getInterface())
printESSID(list_essid)
