import socket
import os

def giveAlert(str_error):
    list_command = {'status': 'Help > Check your interface status'}
    print list_command[str_error]

def sendRSSI(str_host, CONST_INT_PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((str_host, CONST_INT_PORT))
    file_in, file_out, file_error = os.popen3('iw dev wlan0 station dump')
    if file_error.read():
        giveAlert('status')
    else:
        list_result = file_out.read().split('\n')
	list_rssi = []
	str_dev = ''
	str_rssi = ''
        for str_result in list_result:
	    if str_result.find('Station') >= 0:
		str_dev = str_result.split(' ')[1]
            elif str_result.find('signal:') >= 0:
		str_rssi = str_result.split(' ')[2].strip()
		list_rssi.append((str_dev, str_rssi))

	print list_rssi
	s.sendall("Hello\n")
	s.close()
