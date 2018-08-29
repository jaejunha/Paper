import os
import sys
import json

import http as HTTP
import rssi as RSSI

def getIP():
	f = open('server.json', 'r')
        json_data = json.load(f)
        f.close()
	return json_data["Server"] 

def openServer(port):
	file_in, file_out, file_error = os.popen3('iwconfig ' + sys.argv[1])
	if file_error.read().find("No such device") < 0:
		HTTP.runServer(port)	

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Help > python proxy.py <wlan interface>' 
	else:
		dic_server = getIP()
		RSSI.runRSSICollector(sys.argv[1], dic_server["SDN_RSSI"])
		openServer(dic_server["Proxy"]["PORT"])
