import sys
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer

Protocol = "HTTP/1.1"

if sys.argv[1:]:
	port = int(sys.argv[1])
else:
	port = 9000

server_address = ("", port)

class myHandler(BaseHTTPRequestHandler):

	def do_HEAD(self):
		self.send_response(200)
		self.send_header("Content_type", "text/html")
		self.end_headers()

	def do_GET(self):
		parsed_path = urlparse.urlparse(self.path)
		message_parts = [
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                '',
                ]
		message = '\r\n'.join(message_parts)
		self.send_response(200)
		self.send_header("Content_type", "text/html")
		self.end_headers()
		self.wfile.write(message)
		'''
		if(parsed_path == "/"):
			self.wfile.write("<html><head><title>It works!</title></head>")
			self.wfile.write("<body><p>Test</p>")
			self.wfile.write("<body><p>Test again</p>")
			self.wfile.write("</body></html>")
		else:
			self.wfile.write(message)
		'''

if __name__ == '__main__':
	httpd = HTTPServer(server_address, myHandler)

	sa = httpd.socket.getsockname()
	print "Serving HTTP on", sa[0], "port", sa[1], "..."
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()

