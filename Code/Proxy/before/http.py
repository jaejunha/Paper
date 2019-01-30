from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import urllib2
import re
import socket

p = re.compile(r'[0-9]+kbit')
dic_optimizer = None

def changeBitrate(str_url):
	if p.search(str_url):
		str_before = p.search(str_url).group()
		socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket_server.connect((dic_optimizer["IP"],int(dic_optimizer["PORT"])))
		socket_server.send(str_before.split('kbit')[0]+"\n")
		str_msg = socket_server.recv(1023)
		str_after = str_msg.split(' ')[1].strip()
		print "\nAdusted: "+str_after
		socket_server.close()
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
		str_url = changeBitrate(self.path)
		self._set_headers()
		try:
		       	self.wfile.write(urllib2.urlopen(str_url).read())	
		except:
			pass

def runServer(proxy, optimizer):
        global dic_optimizer
        dic_optimizer = optimizer
	HTTPServer(('',int(proxy["PORT"])), Handler).serve_forever()
