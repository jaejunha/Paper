import socket
import time
import os
import json

str_ap = ''
bool_handover = False

def getIP():
	f = open('server.json', 'r')
	json_data = json.load(f)
	f.close()
	return json_data["Server"]

if __name__ == '__main__':
	while True:
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#dic_server = getIP()
		server.connect(('141.223.65.55', 12345))
		server.send('hello')
		str_msg = server.recv(65535)
		int_command = int(str_msg[1])
		if int_command == 2:
			if str_ap != str_msg.split(' ')[1]:
				str_ap = str_msg.split(' ')[1]
				print str_ap
				bool_handover = True
				os.popen('nmcli dev wifi con '+str_ap)
			else:
				pass	
		server.close()
		if bool_handover == True:
			time.sleep(20)
			bool_handover = False
		else:
			print 'sending RSSI...'
