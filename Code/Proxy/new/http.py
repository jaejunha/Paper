from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import urllib2
import re
from socket import *

p = re.compile(r'[0-9]+kbit')
dic_application = None

def changeBitrate(str_url):
	if p.search(str_url):
		str_raw = p.search(str_url).group()
		str_before = str_raw
		
		socket_client = socket(AF_INET, SOCK_STREAM)
		socket_client.connect((dic_application["IP"],int(dic_application["PORT"])))
		str_raw = socket_client.recv(1024).split(' ')
		str_after = str_raw[0].split('/')[0]+'kbit'
		print("\nAdusted: "+str_after)
		socket_client.close()
		return str_url.replace(str_before, str_after)
	else:
		return str_url 

class Handler(BaseHTTPRequestHandler):
	def setup(self):
		BaseHTTPRequestHandler.setup(self)
		self.request.settimeout(2)
	def _set_headers(self):
	       	self.send_response(200)
	       	self.send_header('Content-type', 'text/html')
	        self.end_headers()

	def do_GET(self):
		if self.client_address[0] == '192.168.100.120':
			str_url = changeBitrate(self.path)
		else:
			str_url = self.path
		self._set_headers()
		try:
			data = urllib2.urlopen(str_url).read()
			self.wfile.write(data)
		except:
			print('abc')
			pass

def runServer(proxy, application):
	global dic_application
	dic_application = application
	HTTPServer(('',int(proxy["PORT"])), Handler).serve_forever()
