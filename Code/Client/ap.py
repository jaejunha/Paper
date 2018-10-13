import os

def giveAlert(str_error):
	list_command = {'status': 'Help > Check your interface status',
			'arg': 'Help > python client.py change <AP id> <AP pwd>',
			'input': 'Help > Check your input'
        		}
        print list_command[str_error]

def scanESSID(bool_print = True):
	file_in, file_out, file_error = os.popen3('nmcli dev wifi list')
	if file_error.read():
		giveAlert('status')
	else:
		list_result = file_out.read().split('\n')
		list_essid = []
		if bool_print:
                       	print ''
                       	print 'AP List(Using nmcli command):'
                       	print '================================================================================='
		for str_result in list_result:
			if bool_print:
				if str_result:
					print str_result
				if str_result.find('SSID') >= 0:
					print '================================================================================='
			if str_result.find('SSID') < 0 and str_result:
				list_essid.append(str_result.split(' ')[3])
		if bool_print:
			print '================================================================================='
		return list_essid

def changeESSID(str_essid, str_pwd):
	if str_essid in scanESSID(False): 
       		if str_pwd:
			os.popen('nmcli dev wifi con ' + str_essid + ' password ' + str_pwd)
		else:
			os.popen('nmcli dev wifi con ' + str_essid)
	else:
		giveAlert('input')
