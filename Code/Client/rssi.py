import os
import json
import threading
import time
import sys
import socket
import re

class AsyncTask:
	def __init__(self, mac, interface, ip, port):
		self.interface = interface
		self.mac = mac
		self.ip = ip
		self.port = port
	
	def monitorRSSI(self):
		try:
			socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			socket_server.connect((self.ip, self.port))
		except :
			print 'Help > Please check server status'
			socket_server.close()
			sys.exit(1) 
   		bool_error, dic_rssi = getRSSI(self.interface, self.mac)
	        if bool_error == True:
			socket_server.close()
		        sys.exit(1)
		socket_server.sendall(dic_rssi + '\n')
		print socket_server.recv(1024).strip()
		socket_server.close()
		threading.Timer(2, self.monitorRSSI).start()
	
def runRSSICollector(interface, server):
	str_mac = getMAC(interface)
	at = AsyncTask(interface, str_mac, server["IP"], int(server["PORT"]))
	at.monitorRSSI()

def getMAC(interface):
	file_in, file_out, file_error = os.popen3('ifconfig ' + interface)
	str_line = file_out.read().split('\n')[0]
	p = re.compile('[a-f0-9]{0,2}:.{0,2}:.*:.*:.*:.{0,2}')
	m = p.search(str_line)
	return m.group().replace(':','').rjust(16,'0')

def getAP():
        file_in, file_out, file_error = os.popen3('iwconfig')
        str_line = file_out.read()
        p = re.compile('".*"')
        m = p.search(str_line)
        return m.group().replace('"','')

def getRSSI(interface, mac):
        dic_rssi = {}
        file_in, file_out, file_error = os.popen3('iwlist ' + interface + ' scan')
        if file_error.read():
                print 'Help > Check wlan interface name'
                return True, dic_rssi
        else:
                str_result = file_out.read().split('\n')
                str_ap = ''
		str_signal = ''
                for str_line in str_result:
			if str_line.find('ESSID:') >= 0:
				p = re.compile('".*"')
				m = p.search(str_line)
				str_ap = m.group().replace('"','')
				dic_rssi[str_ap] = str_signal
			if str_line.find('Signal level') >= 0:
				p = re.compile('-[0-9]*')
				m = p.search(str_line)
				str_signal = m.group().strip()
                return False, json.dumps({"AP": getAP(), "MAC": mac, "RSSI": list(dic_rssi.items())})