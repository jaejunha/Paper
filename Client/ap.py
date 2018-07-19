import os

def giveAlert(str_error):
	list_command = {'arg_s': 'Help > python client.py scan <interface name>',
        		'status': 'Help > Check your interface status',
			'arg_c': 'Help > python client.py change <interface name> <AP id>',
			'input': 'Help > Check your input',
        		}
        print list_command[str_error]

def getInterface():
	file_in, file_out, file_error = os.popen3('iwconfig')
	list_result = file_out.read().split('\n')
	for str_result in list_result:
		if 'ESSID' in str_result:
			str_interface = str_result.split(' ')[0]
			str_essid = str_result.split('ESSID:')[1]
			if 'off/any' in str_essid:
				essid = 'X'
			print 'Interface: ' + str_interface + ', AP: ' + str_essid

def scanESSID(str_interface, bool_print = True):
	file_in, file_out, file_error = os.popen3('iwlist ' + str_interface + ' scanning')
	if file_error.read():
		giveAlert('status')
	else:
		list_essid = []
		list_result = file_out.read().split('\n')
		if list_result:
			for str_result in list_result:
				if str_result.find('ESSID:') > 0:
					list_essid.append(str_result.split('ESSID:')[1][1:-1])
			if bool_print:
				print 'Conntectable AP List:'
			        print '========================================================='
		       		for str_essid in list_essid:
		       	        	print str_essid
	      			print '========================================================='
			return list_essid

def changeESSID(str_interface, str_essid):
	if str_essid in scanESSID(str_interface, False): 
		file_in, file_out, file_error = os.popen3('iwconfig ' + str_interface + ' essid ' + str_essid)
		if file_error.read():
			giveAlert('input')
		else:
			file_in, file_out, file_error = os.popen3('iwconfig ' + str_interface)
	        	str_result = file_out.read().split('\n')[0]
			print file_out.read() 
	                if 'off/any' in str_result.split('ESSID:')[1]:
				giveAlert('input')
			else:
				print 'Success connection: ' + str_essid
	else:
		giveAlert('input')
