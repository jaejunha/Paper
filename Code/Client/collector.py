import os
import json
import threading
import time
import sys
import socket
import re

class AsyncTask:
	def __init__(self, interface, mac, ip, port):
		self.interface = interface
		self.mac = mac
		self.ip = ip
		self.port = port
	
	def operateMachine(self):
		try:
			socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			socket_server.connect((self.ip, self.port))
		except :
			print 'Help > Please check server status'
			socket_server.close()
			sys.exit(1) 
   		dic_rssi = getRSSI(self.interface, self.mac)
		socket_server.send(dic_rssi + '\n')

		bool_handover = False
		str_currentAP = getAP(self.interface)
		str_msg = socket_server.recv(65535)
                int_command = int(str_msg[1])
                if int_command == 2:
                        if str_currentAP != str_msg.split(' ')[1].strip():
                                str_currentAP = str_msg.split(' ')[1].strip()
                                print str_currentAP
                                bool_handover = True
                                os.popen('nmcli dev wifi con '+str_currentAP)
                        else:
                                pass    
                socket_server.close()

                if bool_handover == True:
                        bool_handover = False
			threading.Timer(20, self.operateMachine).start()
                else:
                        print 'sending RSSI...'
			threading.Timer(5, self.operateMachine).start()
	
def run(interface, server):
	str_mac = getMAC(interface)
	at = AsyncTask(interface, str_mac, server["IP"], int(server["PORT"]))
	at.operateMachine()

def getMAC(interface):
	file_in, file_out, file_error = os.popen3('ifconfig ' + interface)
	str_line = file_out.read().split('\n')[0]
	p = re.compile('[a-f\d]{0,2}:.{0,2}:.*:.*:.*:.{0,2}')
	m = p.search(str_line)
	return m.group().replace(':','').rjust(16,'0')

def getAP(interface):
        file_in, file_out, file_error = os.popen3('iwgetid ' + interface + ' -r')
        return file_out.read().strip() 

def getRSSI(interface, mac):
        dic_rssi = {}
        file_in, file_out, file_error = os.popen3('nmcli dev wifi list | grep LOAD_AP')
        str_result = file_out.read().split('\n')
        str_ap = ''
	str_signal = ''
        for str_line in str_result:
		if len(str_line) > 0:
			p = re.compile("'.*'")
			m = p.search(str_line)
			str_ap = m.group().replace("'","")
			p = re.compile('[^:\d]\d\d[^:\d]')
			m = p.findall(str_line)
			str_signal = m[1].strip()
			dic_rssi[str_ap] = str_signal
	return json.dumps({"REQ": 360, "SUP": 240, "AP": getAP(interface), "MAC": mac, "RSSI": list(dic_rssi.items())})
