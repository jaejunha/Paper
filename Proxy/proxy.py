import sys
import json
import http as HTTP
import rssi as RSSI

def getIP():
	f = open('server.json', 'r')
        json_data = json.load(f)
        f.close()
	return json_data["Server"]["SDN"], json_data["Server"]["Media"]

def openServer(port):
	HTTP.runServer(port)	

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print 'Help > python proxy.py <wlan interface> <port number>' 
	else:
		str_sdn, str_media = getIP()
		print str_sdn, str_media
		bool_error, dic_rssi = RSSI.getRSSI(sys.argv[1])
		if bool_error == False:
			print dic_rssi
			openServer(sys.argv[2])
