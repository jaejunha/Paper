import sys
import json
import http as HTTP

def openServer(port):
	HTTP.runServer(port)	

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print 'Help > python proxy.py <port number>' 
	else:
		f = open('server.json', 'r')
		json_data = json.load(f)
		str_sdn = json_data["Server"]["SDN"]
		str_media = json_data["Server"]["Media"]
		f.close()
		openServer(sys.argv[1])
