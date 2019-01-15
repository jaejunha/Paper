from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import urllib2
import re

p = re.compile(r'[0-9]+kbit')

def changeBitrate(str_url):
	if p.search(str_url):
		str_before = p.search(str_url).group()
		str_after = '100kbit'
		return str_url.replace(str_before, str_after)
	else:
		return str_url

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
	str_url = changeBitrate(self.path)
	print str_url
	self._set_headers()
        self.wfile.write(urllib2.urlopen(str_url).read())

def runServer(port):
	HTTPServer(('',int(port)), Handler).serve_forever()
