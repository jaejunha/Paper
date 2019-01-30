import os
import json
import sys

import collector as Collector

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
		Collector.run(sys.argv[1], dic_server["SDN_Collector"])
