import os
import json
import threading
import time
import sys
import re

from socket import *

class AsyncTask:
	def __init__(self, interface, no, mac, ip, port):
		self.interface = interface
		self.no = no
		self.mac = mac
		self.ip = ip
		self.port = port
		
		print('current AP', getAP(self.interface))
	
	def operateMachine(self):
		while True:
			client = socket(AF_INET, SOCK_STREAM)
			client.connect((self.ip, self.port))
			raw = client.recv(1024).split(' ')[self.no]
			if raw.split('/')[1] != getAP(self.interface):
				os.popen('nmcli dev wifi con '+raw.split('/')[1])
				print('current AP', raw.split('/')[1])
			else:
				pass
			time.sleep(0.5)
	
def run(interface, no, server):
	str_mac = getMAC(interface)
	at = AsyncTask(interface, no, str_mac, server["IP"], int(server["PORT"]))
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
        file_in, file_out, file_error = os.popen3("iw "+interface+" scan | egrep 'signal|LOAD_AP'")

	str_result = file_out.read()	
#	if len(str_result) == 0:
#		print 'Help > Check wlan interface name'
#		return True, dic_rssi
	
        str_ap = ''
	str_signal = ''
        for str_line in str_result.split('\n'):
		if str_line.find('LOAD_AP') >= 0:
			p = re.compile("LOAD_AP\d")
			m = p.search(str_line)
			str_ap = m.group().strip()
			dic_rssi[str_ap] = str_signal
		else:
			p = re.compile('-\d+[^.]')
			m = p.search(str_line)
			if m:
				str_signal = m.group().strip()
	return False, json.dumps({"REQ": 360, "SUP": 240, "AP": getAP(interface), "MAC": mac, "RSSI": list(dic_rssi.items())})
