import os
import json
import threading
import time
import sys
import re

from socket import *

class AsyncTask:
	def __init__(self, interface, mac, ip, port):
		self.interface = interface
		self.mac = mac
		self.ip = ip
		self.port = port
		self.ap = getAP(self.interface)
		
		print('current AP', self.ap)
	
	def operateMachine(self):
		while True:
			client = socket(AF_INET, SOCK_STREAM)
			try:
				client.connect((self.ip, self.port))
			except:
				time.sleep(0.5)
				continue
			
			
			str_msgs = client.recv(1024).split(' ')
			for str_msg in str_msgs:
				if str_msg.split('/')[0] == "of:" + self.mac:
					ap = str_msg.split('/')[1]

					if ap == self.ap:
						break
					
					print("AP will be changed")

					os.popen('nmcli dev wifi con ' + ap)
					print('current AP', ap)
					self.ap = ap
					break
			time.sleep(0.5)
	
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
