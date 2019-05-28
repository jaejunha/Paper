import os
import json
import sys

import machine as Machine

def getIP():
	f = open('server.json', 'r')
	json_data = json.load(f)
	f.close()
	return json_data["Server"]

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print 'Help > python client.py <wlan interface> <# ue>' 
	else:
		dic_server = getIP()
		Machine.run(sys.argv[1], int(sys.argv[2]), dic_server["SDN_Application"])
