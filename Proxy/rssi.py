import os
import json
import threading
import time
import sys
import socket

class AsyncTask:
	def __init__(self, interface, ip, port):
		self.interface = interface
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
   		bool_error, dic_rssi = getRSSI(self.interface)
	        if bool_error == True:
			socket_server.close()
		        sys.exit(1)
		socket_server.sendall(dic_rssi + '\n')
                print socket_server.recv(1024).strip()
		socket_server.close()
		threading.Timer(2, self.monitorRSSI).start()
	
def runRSSICollector(interface, server):
	at = AsyncTask(interface, server["IP"], int(server["PORT"]))
	at.monitorRSSI()

def getRSSI(interface):
        dic_rssi = {}
        file_in, file_out, file_error = os.popen3('iw dev ' + interface + ' station dump')
        if file_error.read():
                print 'Help > Check wlan interface name'
                return True, dic_rssi
        else:
                str_result = file_out.read().split('\n')
                str_addr = ''
                for str_line in str_result:
                        if str_line.find('Station') >= 0:
                                str_addr = str_line.split(' ')[1]
                        if str_line.find('signal') >= 0:
                                dic_rssi[str_addr] = str_line.split('\t')[2].split(' ')[0]
                return False, json.dumps({"RSSI": dic_rssi})
