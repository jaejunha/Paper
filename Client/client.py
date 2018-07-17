import os 
import re
p = re.compile('.*[^:]Link')

def getInterface():
	list_interface = []
	list_result = os.popen('ifconfig').read().split('\n')
	for str_result in list_result:
		m = p.match(str_result)
		if m:
			list_interface.append(m.group().split(' ')[0])
	return list_interface

def searchESSID(list_interface):
	list_essid = []
	for str_interface in list_interface:
		try:
			list_result = os.popen('iwlist ' + str_interface + ' scanning').read()
			if list_result.find('doesn\'t support scanning') == -1:
				list_result = list_result.split('\n')
				for str_result in list_result:
					if str_result.find('ESSID:') > 0:
						list_essid.append(str_result.split('ESSID:')[1][1:-1])
		except Exception:
			pass
	return list_essid

def printESSID(list_essid):
        for essid in list_essid:
                print essid

list_essid = searchESSID(getInterface())
printESSID(list_essid)
