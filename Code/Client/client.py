import os
import sys
import json

import rssi as RSSI

def getIP():
	f = open('server.json', 'r')
        json_data = json.load(f)
        f.close()
	return json_data["Server"] 

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Help > python client.py <wlan interface>' 
	else:
		dic_server = getIP()
		RSSI.runRSSICollector(sys.argv[1], dic_server["SDN_RSSI"])
